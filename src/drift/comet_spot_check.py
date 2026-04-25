"""Drive Comet via CDP to attempt 20 sampled WORKBank tasks; capture responses for grading.

Comet must be running with --remote-debugging-port=9222.
Sam must be signed in (Pro account).

Output: runs/comet_spot_check/<task_id>.json with prompt + raw response text + metadata.
Then a separate grading pass scores each response 1-3 and computes κ vs predicted capability.
"""

from __future__ import annotations

import asyncio
import json
import re
import time
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_FILE = ROOT / "data" / "spot_check_sample.json"
OUT_DIR = ROOT / "runs" / "comet_spot_check"
CDP_URL = "http://localhost:9222"
PERPLEXITY_HOME = "https://www.perplexity.ai"

WAIT_AFTER_SUBMIT_S = 4         # initial settle
RESPONSE_POLL_INTERVAL_S = 5
RESPONSE_TIMEOUT_S = 240        # 4 min per task max


def _build_prompt(task: str, occupation: str) -> str:
    return (
        f"You are an AI assistant. Actually attempt this real workplace task — don't just describe how. "
        f"If you need data, files, or accounts I don't have, get as close as you can with example/synthetic data and clearly mark it. "
        f"After your attempt, end your reply with three labelled lines:\n"
        f"ATTEMPT_RESULT: <one of: completed | partial | failed>\n"
        f"WHAT_I_DID: <one sentence>\n"
        f"WHAT_BLOCKED_ME: <one sentence or 'nothing'>\n\n"
        f"Task: {task}\n\n"
        f"Occupation context: {occupation}"
    )


async def _wait_for_chat_url(page, timeout_s: int = 30) -> bool:
    """After submit, URL transitions to /search/<uuid>. Wait for that."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if "/search/" in page.url:
            return True
        await asyncio.sleep(0.5)
    return False


async def _wait_for_response_complete(page, timeout_s: int) -> str:
    """Wait for Comet's response to finish streaming. Detect via stop-button absence + DOM stability.

    Once on /search/<uuid>, the response area is a div containing prose. We extract
    everything after the user's question, polling for stability.
    """
    deadline = time.time() + timeout_s
    last_text = ""
    stable_iters = 0
    while time.time() < deadline:
        await asyncio.sleep(RESPONSE_POLL_INTERVAL_S)
        stop = await page.query_selector('button[aria-label*="Stop"]')
        # Find the assistant's response container — Perplexity uses prose-style divs
        # under the search container. Grab all text in the main response area.
        try:
            body_text = await page.evaluate(
                """() => {
                    // Get the chat content area; prefer dedicated container.
                    const main = document.querySelector('main') || document.body;
                    return main ? main.innerText : '';
                }"""
            )
        except Exception:
            body_text = ""
        if not stop and body_text == last_text and len(body_text) > 100:
            stable_iters += 1
            if stable_iters >= 2:
                return body_text
        else:
            stable_iters = 0
        last_text = body_text
    return last_text


async def run_task(page, task_id: int, task: str, occupation: str, predicted_cap: int) -> dict:
    out = {"task_id": task_id, "task": task, "occupation": occupation, "predicted_cap": predicted_cap}
    # Start fresh chat
    await page.goto(PERPLEXITY_HOME, wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(1.0)
    inp = await page.query_selector('[contenteditable="true"][role="textbox"]') or \
          await page.query_selector('[contenteditable="true"]')
    if not inp:
        out["error"] = "input not found"
        return out
    await inp.click()
    prompt = _build_prompt(task, occupation)
    out["prompt"] = prompt
    # Real keystrokes — execCommand doesn't trigger Perplexity's input handlers.
    # Speed up: paste via clipboard then trigger input event.
    await page.evaluate(
        "(text) => navigator.clipboard.writeText(text)",
        prompt,
    )
    # Cmd+V (mac) to paste
    await page.keyboard.press("Meta+V")
    await asyncio.sleep(0.5)
    await page.keyboard.press("Enter")
    # Wait for navigation to /search/
    if not await _wait_for_chat_url(page, timeout_s=20):
        out["error"] = "did not navigate to /search/ after submit"
        return out
    await asyncio.sleep(WAIT_AFTER_SUBMIT_S)
    response_text = await _wait_for_response_complete(page, RESPONSE_TIMEOUT_S)
    out["response_text"] = response_text
    # Extract attempt result tag if present
    m = re.search(r"ATTEMPT_RESULT:\s*(completed|partial|failed)", response_text, re.IGNORECASE)
    out["attempt_result_tag"] = m.group(1).lower() if m else None
    out["url"] = page.url
    out["timestamp"] = time.time()
    return out


async def amain() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sample = json.loads(SAMPLE_FILE.read_text())
    print(f"running {len(sample)} tasks against Comet")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0]
        # Reuse existing perplexity page or open new
        page = next((pg for pg in ctx.pages if "perplexity" in pg.url), None)
        if not page:
            page = await ctx.new_page()
        await page.bring_to_front()

        for i, t in enumerate(sample, 1):
            tid = t["task_id"]
            out_path = OUT_DIR / f"{tid}.json"
            if out_path.exists():
                print(f"  [{i}/{len(sample)}] task {tid} already done, skip")
                continue
            print(f"  [{i}/{len(sample)}] task {tid} ({t['occupation'][:30]}, pred_cap={t['predicted_cap']})")
            try:
                result = await run_task(page, tid, t["task"], t["occupation"], t["predicted_cap"])
            except Exception as e:
                result = {"task_id": tid, "error": str(e)[:300]}
            out_path.write_text(json.dumps(result, indent=2))
            print(f"      → result_tag={result.get('attempt_result_tag')} | response_len={len(result.get('response_text',''))}")


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
