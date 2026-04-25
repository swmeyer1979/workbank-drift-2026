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
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

from drift.rubric import build_prompt

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
BENCH = ROOT / "data" / "benchmarks.yaml"
RUNS = ROOT / "runs"

MODELS = {
    "opus_4_7":    {"vendor": "anthropic",  "id": "claude-opus-4-7"},
    "kimi_k2_6":   {"vendor": "openrouter", "id": "moonshotai/kimi-k2.6"},
    "gpt_5_5":     {"vendor": "openai",     "id": "gpt-5.5"},
    "grok_4_20":   {"vendor": "openrouter", "id": "x-ai/grok-4.20"},
}


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
    async def score(self, prompt: str) -> dict[str, Any]:
        raise NotImplementedError


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

    def __init__(self) -> None:
        from openai import AsyncOpenAI

        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY missing")
        self.client = AsyncOpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")


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
                done_ids.add(json.loads(line)["task_id"])

    with out.open("a") as f:
        sem = asyncio.Semaphore(8)

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

    enabled = args.raters.split(",") if args.raters else list(MODELS.keys())
    rater_factories = {
        "opus_4_7": AnthropicRater,
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
                   help="comma list: opus_4_7,gemini_3_pro,gpt_5_5")
    asyncio.run(amain(p.parse_args()))


if __name__ == "__main__":
    main()
