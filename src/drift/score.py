"""Ensemble scoring pipeline.

Reads WORKBank tasks, builds a per-task prompt, queries three frontier models
in parallel, and writes per-rater scores to runs/raters/<run_id>/<model>.jsonl.

Does NOT join / aggregate / classify. That's build.py.

Usage:
    uv run score-capability --limit 50           # smoke test
    uv run score-capability --task-file calibration_sample.csv
    uv run score-capability                      # full 844
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import signal
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

from drift.rubric import RUBRIC, build_prompt

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
BENCH = ROOT / "data" / "benchmarks.yaml"
RUNS = ROOT / "runs"

MODELS = {
    "opus_4_7":    {"vendor": "anthropic",  "id": "claude-opus-4-7"},
    "codex_gpt_5_5_xhigh": {"vendor": "codex-oauth", "id": "gpt-5.5", "effort": "xhigh"},
    "kimi_k2_6":   {"vendor": "openrouter", "id": "moonshotai/kimi-k2.6"},
    "gpt_5_5":     {"vendor": "openai",     "id": "gpt-5.5"},
    "grok_4_20":   {"vendor": "openrouter", "id": "x-ai/grok-4.20"},
}
DEFAULT_RATERS = ["codex_gpt_5_5_xhigh", "kimi_k2_6", "gpt_5_5"]


@dataclass(frozen=True)
class TaskRow:
    task_id: int
    occupation: str
    task: str
    physical: float
    interpersonal: float
    uncertainty: float
    domain: float


def load_tasks(limit: int | None, task_file: str | None) -> list[TaskRow]:
    desires = pd.read_csv(RAW / "domain_worker_desires.csv")
    experts = pd.read_csv(RAW / "expert_rated_technological_capability.csv")
    meta = pd.read_csv(RAW / "task_statement_with_metadata.csv")

    priors = desires.groupby("Task ID").agg(
        physical=("Physical Action Requirement", "mean"),
        interpersonal=("Interpersonal Communication Requirement", "mean"),
        uncertainty=("Involved Uncertainty", "mean"),
        domain=("Domain Expertise Requirement", "mean"),
    )
    capacity = experts.groupby("Task ID").size().rename("expert_n")
    task_meta = meta[["Task ID", "Occupation (O*NET-SOC Title)", "Task"]].drop_duplicates("Task ID").set_index("Task ID")

    df = priors.join(capacity, how="inner").join(task_meta, how="inner").reset_index()

    if task_file:
        # Filter to a prebuilt sample (e.g. calibration_sample.csv)
        sub = pd.read_csv(ROOT / "data" / task_file)
        df = df[df["Task ID"].isin(sub["task_id"])]

    if limit:
        df = df.head(limit)

    rows = [
        TaskRow(
            task_id=int(r["Task ID"]),
            occupation=r["Occupation (O*NET-SOC Title)"],
            task=r["Task"],
            physical=float(r["physical"] or 0),
            interpersonal=float(r["interpersonal"] or 0),
            uncertainty=float(r["uncertainty"] or 0),
            domain=float(r["domain"] or 0),
        )
        for _, r in df.iterrows()
    ]
    return rows


def anchors_for_task(task: str) -> str:
    """Return the benchmark anchors block for this task.

    v0: pass all benchmarks; raters are instructed to cite only what applies.
    v1: route by task family (software / web / desktop / knowledge / math / ...).
    """
    bench = yaml.safe_load(BENCH.read_text())
    lines = []
    for bid, b in bench["benchmarks"].items():
        scores = b["scores"]
        line = f"- {bid} ({b['description']})"
        for m, s in scores.items():
            if s.get("score") is not None:
                line += f"\n    {m}: {s['score']}  source: {s.get('source','?')}"
        lines.append(line)
    return "\n".join(lines)


# ---- rater adapters ------------------------------------------------------------

class Rater:
    name: str
    concurrency = 8
    batch_size = 1

    async def score(self, prompt: str) -> dict[str, Any]:
        raise NotImplementedError


def _prepare_codex_home() -> Path:
    source = Path(os.environ.get("CODEX_SOURCE_HOME", Path.home() / ".codex"))
    target = Path(
        os.environ.get(
            "WORKBANK_CODEX_HOME",
            str(Path.home() / ".codex" / "tmp" / "workbank-drift-codex-oauth"),
        )
    )
    auth = source / "auth.json"
    if not auth.exists():
        raise RuntimeError(f"Codex OAuth auth missing at {auth}")

    target.mkdir(parents=True, exist_ok=True)
    os.chmod(target, 0o700)
    shutil.copyfile(auth, target / "auth.json")
    os.chmod(target / "auth.json", 0o600)
    (target / "config.toml").write_text(
        'model = "gpt-5.5"\nmodel_reasoning_effort = "xhigh"\n',
        encoding="utf-8",
    )
    return target


def _codex_result_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "task_id",
            "capability_score",
            "has_score",
            "justification",
            "cap_rule_fired",
            "benchmark_anchors",
            "llm_inferred",
            "confidence",
        ],
        "properties": {
            "task_id": {"type": "integer"},
            "capability_score": {"type": "integer", "minimum": 1, "maximum": 5},
            "has_score": {"type": "integer", "minimum": 1, "maximum": 5},
            "justification": {"type": "string"},
            "cap_rule_fired": {
                "type": "string",
                "enum": ["none", "physical", "interpersonal", "safety_critical", "novel_research"],
            },
            "benchmark_anchors": {"type": "array", "items": {"type": "string"}},
            "llm_inferred": {"type": "boolean"},
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        },
    }


def _write_codex_schema(codex_home: Path) -> Path:
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["results"],
        "properties": {
            "results": {
                "type": "array",
                "items": _codex_result_schema(),
            }
        },
    }
    path = codex_home / "workbank_rater_schema.json"
    path.write_text(json.dumps(schema), encoding="utf-8")
    os.chmod(path, 0o600)
    return path


def _parse_codex_jsonl(output: str) -> Any:
    text: str | None = None
    for line in output.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item") or {}
        if event.get("type") == "item.completed" and item.get("type") == "agent_message":
            text = item.get("text")
    if not text:
        raise ValueError(f"no Codex agent_message found in output tail: {output[-1000:]}")
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


class CodexOAuthRater(Rater):
    name = "codex_gpt_5_5_xhigh"
    concurrency = int(os.environ.get("CODEX_RATER_CONCURRENCY", "1"))
    batch_size = max(1, int(os.environ.get("CODEX_RATER_BATCH_SIZE", "8")))

    def __init__(self) -> None:
        self.codex_home = _prepare_codex_home()
        self.schema_path = _write_codex_schema(self.codex_home)
        self.codex = os.environ.get("CODEX_CLI_PATH") or shutil.which("codex")
        if not self.codex:
            raise RuntimeError("codex CLI missing")
        self.model = "gpt-5.5"
        self.timeout = int(os.environ.get("CODEX_RATER_TIMEOUT_SEC", "600"))

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(min=2, max=10))
    async def score(self, prompt: str) -> dict[str, Any]:
        raise RuntimeError("CodexOAuthRater requires score_rows")

    def _build_batch_prompt(self, rows: list[TaskRow], anchors_text: str) -> str:
        tasks = [
            {
                "task_id": row.task_id,
                "occupation": row.occupation,
                "task": row.task,
                "physical": round(row.physical, 2),
                "interpersonal": round(row.interpersonal, 2),
                "uncertainty": round(row.uncertainty, 2),
                "domain": round(row.domain, 2),
            }
            for row in rows
        ]
        return (
            f"{RUBRIC}\n\n"
            "Relevant 2026 benchmark anchors. Cite only anchors that apply to each task family:\n"
            f"{anchors_text}\n\n"
            "Rate every task in this JSON array. Return one JSON array with one result object per "
            "task under top-level key `results`, preserving each task_id. No extra text.\n\n"
            f"{json.dumps(tasks, ensure_ascii=False)}"
        )

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(min=2, max=10))
    async def score_rows(self, rows: list[TaskRow], anchors_text: str) -> list[dict[str, Any]]:
        env = os.environ.copy()
        env["CODEX_HOME"] = str(self.codex_home)
        prompt = self._build_batch_prompt(rows, anchors_text)
        wrapped = (
            "You are a data-pipeline rater. Do not use tools or inspect files. "
            "Return only valid JSON matching the requested schema.\n\n"
            f"{prompt}"
        )
        proc = await asyncio.create_subprocess_exec(
            self.codex,
            "exec",
            "--json",
            "--ephemeral",
            "--ignore-rules",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "--output-schema",
            str(self.schema_path),
            "-C",
            "/tmp",
            "-m",
            self.model,
            "-c",
            'model_reasoning_effort="xhigh"',
            "-",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=env,
            start_new_session=True,
        )
        try:
            out, _ = await asyncio.wait_for(proc.communicate(wrapped.encode()), timeout=self.timeout)
        except TimeoutError:
            try:
                os.killpg(proc.pid, signal.SIGTERM)
                await asyncio.wait_for(proc.wait(), timeout=5)
            except Exception:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            raise
        text = out.decode(errors="replace")
        if proc.returncode != 0:
            raise RuntimeError(f"codex exec failed {proc.returncode}: {text[-1000:]}")
        parsed = _parse_codex_jsonl(text)
        if not isinstance(parsed, dict) or not isinstance(parsed.get("results"), list):
            raise ValueError(f"expected Codex batch results object, got {type(parsed).__name__}")
        parsed = parsed["results"]
        by_id = {int(item["task_id"]): item for item in parsed}
        missing = [row.task_id for row in rows if row.task_id not in by_id]
        if missing:
            raise ValueError(f"Codex response missing task_ids: {missing}")
        return [by_id[row.task_id] for row in rows]


class AnthropicRater(Rater):
    name = "opus_4_7"

    def __init__(self) -> None:
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY missing")
        self.client = AsyncAnthropic(api_key=key)
        self.model = "claude-opus-4-7"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=20))
    async def score(self, prompt: str) -> dict[str, Any]:
        # Opus 4.7 deprecated the `temperature` parameter; omit it.
        resp = await self.client.messages.create(
            model=self.model,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        text = resp.content[0].text.strip()
        return _parse_json_loose(text)


class _OpenRouterRater(Rater):
    """Generic OpenRouter rater. Subclasses set `name` and `model`."""

    name = "openrouter"
    model = ""
    concurrency = int(os.environ.get("OPENROUTER_RATER_CONCURRENCY", "8"))

    def __init__(self) -> None:
        from openai import AsyncOpenAI

        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY missing")
        timeout = float(os.environ.get("OPENROUTER_RATER_TIMEOUT_SEC", "180"))
        self.client = AsyncOpenAI(api_key=key, base_url="https://openrouter.ai/api/v1", timeout=timeout)


class KimiRater(_OpenRouterRater):
    name = "kimi_k2_6"
    model = "moonshotai/kimi-k2.6"

    @retry(stop=stop_after_attempt(4), wait=wait_exponential(min=2, max=30))
    async def score(self, prompt: str) -> dict[str, Any]:
        resp = await self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        return _parse_json_loose(resp.choices[0].message.content)


class GrokRater(_OpenRouterRater):
    name = "grok_4_20"
    model = "x-ai/grok-4.20"

    @retry(stop=stop_after_attempt(4), wait=wait_exponential(min=2, max=30))
    async def score(self, prompt: str) -> dict[str, Any]:
        resp = await self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        return _parse_json_loose(resp.choices[0].message.content)


class OpenAIRater(Rater):
    name = "gpt_5_5"

    def __init__(self) -> None:
        from openai import AsyncOpenAI  # lazy import

        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY missing")
        self.client = AsyncOpenAI(api_key=key)
        self.model = "gpt-5.5"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=20))
    async def score(self, prompt: str) -> dict[str, Any]:
        # GPT-5.5 only supports temperature=1 (default); omit the param.
        resp = await self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        return _parse_json_loose(resp.choices[0].message.content)


def _parse_json_loose(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    parsed = json.loads(text)
    # Gemini occasionally wraps the object in a single-element array.
    if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
        parsed = parsed[0]
    if not isinstance(parsed, dict):
        raise ValueError(f"expected dict, got {type(parsed).__name__}")
    return parsed


# ---- main loop ------------------------------------------------------------------

async def score_one(rater: Rater, row: TaskRow, anchors_text: str) -> dict[str, Any]:
    prompt = build_prompt(
        occupation=row.occupation,
        task=row.task,
        physical=row.physical,
        interpersonal=row.interpersonal,
        uncertainty=row.uncertainty,
        domain=row.domain,
        anchors_text=anchors_text,
    )
    t0 = time.time()
    result = await rater.score(prompt)
    result["task_id"] = row.task_id
    result["rater"] = rater.name
    result["elapsed_ms"] = int((time.time() - t0) * 1000)
    return result


async def run_rater(rater: Rater, rows: list[TaskRow], run_dir: Path, anchors_text: str) -> None:
    out = run_dir / f"{rater.name}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    # Append mode: resumable
    done_ids: set[int] = set()
    if out.exists():
        for line in out.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                if "error" not in row:
                    done_ids.add(row["task_id"])

    with out.open("a") as f:
        sem = asyncio.Semaphore(rater.concurrency)

        if hasattr(rater, "score_rows"):
            pending = [row for row in rows if row.task_id not in done_ids]
            chunks = [pending[i:i + rater.batch_size] for i in range(0, len(pending), rater.batch_size)]

            async def bounded_chunk(chunk: list[TaskRow]) -> None:
                async with sem:
                    started = time.time()
                    try:
                        scored = await rater.score_rows(chunk, anchors_text)  # type: ignore[attr-defined]
                        elapsed_ms = int((time.time() - started) * 1000)
                        for result in scored:
                            result["rater"] = rater.name
                            result["elapsed_ms"] = elapsed_ms
                            f.write(json.dumps(result) + "\n")
                    except Exception as e:
                        for row in chunk:
                            err = {"task_id": row.task_id, "rater": rater.name, "error": str(e)[:300]}
                            f.write(json.dumps(err) + "\n")
                    f.flush()

            await asyncio.gather(*[bounded_chunk(chunk) for chunk in chunks])
            return

        async def bounded(row: TaskRow) -> None:
            if row.task_id in done_ids:
                return
            async with sem:
                try:
                    r = await score_one(rater, row, anchors_text)
                    f.write(json.dumps(r) + "\n")
                    f.flush()
                except Exception as e:
                    err = {"task_id": row.task_id, "rater": rater.name, "error": str(e)[:300]}
                    f.write(json.dumps(err) + "\n")
                    f.flush()

        await asyncio.gather(*[bounded(r) for r in rows])


async def amain(args: argparse.Namespace) -> None:
    load_dotenv(ROOT / ".env")
    rows = load_tasks(limit=args.limit, task_file=args.task_file)
    print(f"scoring {len(rows)} tasks")
    run_dir = RUNS / "raters" / args.run_id
    anchors_text = anchors_for_task("")

    enabled = args.raters.split(",") if args.raters else DEFAULT_RATERS
    rater_factories = {
        "opus_4_7": AnthropicRater,
        "codex_gpt_5_5_xhigh": CodexOAuthRater,
        "kimi_k2_6": KimiRater,
        "gpt_5_5": OpenAIRater,
        "grok_4_20": GrokRater,
    }
    raters = [rater_factories[n]() for n in enabled]
    for r in raters:
        extra = ""
        print(f"  rater: {r.name}{extra}")

    await asyncio.gather(*[run_rater(r, rows, run_dir, anchors_text) for r in raters])
    print(f"done -> {run_dir}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--task-file", type=str, default=None,
                   help="e.g. calibration_sample.csv to restrict to the 50-task calibration set")
    p.add_argument("--run-id", type=str, default=time.strftime("%Y%m%d-%H%M%S"))
    p.add_argument("--raters", type=str, default=None,
                   help="comma list; default: codex_gpt_5_5_xhigh,kimi_k2_6,gpt_5_5; optional: opus_4_7,grok_4_20")
    asyncio.run(amain(p.parse_args()))


if __name__ == "__main__":
    main()
