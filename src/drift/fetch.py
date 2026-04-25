"""Fetch WORKBank CSVs from Hugging Face into data/raw/ (gitignored)."""

from __future__ import annotations

from pathlib import Path

import httpx

HF_BASE = "https://huggingface.co/datasets/SALT-NLP/WORKBank/resolve/main"

FILES = {
    "task_statement_with_metadata.csv":             "task_data/task_statement_with_metadata.csv",
    "expert_rated_technological_capability.csv":    "expert_ratings/expert_rated_technological_capability.csv",
    "domain_worker_desires.csv":                    "worker_data/domain_worker_desires.csv",
}

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with httpx.Client(follow_redirects=True, timeout=60) as client:
        for out_name, remote in FILES.items():
            url = f"{HF_BASE}/{remote}"
            dest = RAW_DIR / out_name
            print(f"fetch: {url} -> {dest}")
            r = client.get(url)
            r.raise_for_status()
            dest.write_bytes(r.content)
            print(f"  {dest.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
