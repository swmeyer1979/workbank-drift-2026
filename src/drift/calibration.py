"""Draw a stratified 50-task calibration sample for human hand-scoring.

Strata: 10 tasks per 2025 zone (40) + 10 uniform-random from the 844.
Output: data/calibration_sample.csv with columns for Sam to fill in by hand.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pandas as pd

from drift.zones import zone_of

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "calibration_sample.csv"

SEED = 424      # 2026-04-24
PER_ZONE = 10
N_RANDOM = 10


def main() -> None:
    desires = pd.read_csv(RAW / "domain_worker_desires.csv")
    experts = pd.read_csv(RAW / "expert_rated_technological_capability.csv")
    meta = pd.read_csv(RAW / "task_statement_with_metadata.csv")

    d = desires.groupby("Task ID")["Automation Desire Rating"].mean().rename("desire_2025")
    c = experts.groupby("Task ID")["Automation Capacity Rating"].mean().rename("capacity_2025")
    has_w = desires.groupby("Task ID")["Human Agency Scale Rating"].mean().rename("has_worker_2025")
    has_e = experts.groupby("Task ID")["Human Agency Scale Rating"].mean().rename("has_expert_2025")

    task_scores = pd.concat([d, c, has_w, has_e], axis=1).dropna(subset=["desire_2025", "capacity_2025"])

    meta_small = (
        meta[["Task ID", "Occupation (O*NET-SOC Title)", "Task", "O*NET-SOC Code"]]
        .drop_duplicates(subset=["Task ID"])
        .set_index("Task ID")
    )

    joined = task_scores.join(meta_small, how="inner").reset_index()
    joined["zone_2025"] = joined.apply(
        lambda r: zone_of(r["capacity_2025"], r["desire_2025"]), axis=1
    )

    rng = random.Random(SEED)
    picked: list[int] = []
    for zone in ["Green Light", "Red Light", "R&D Opportunity", "Low Priority"]:
        pool = joined[joined["zone_2025"] == zone]["Task ID"].tolist()
        k = min(PER_ZONE, len(pool))
        picked.extend(rng.sample(pool, k))

    remaining = [t for t in joined["Task ID"].tolist() if t not in picked]
    picked.extend(rng.sample(remaining, N_RANDOM))

    sample = joined[joined["Task ID"].isin(picked)].copy()
    sample = sample.sort_values(by=["zone_2025", "Task ID"]).reset_index(drop=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "task_id", "occupation", "onet_soc_code", "task",
            "desire_2025", "capacity_2025", "zone_2025",
            "has_worker_2025", "has_expert_2025",
            "sam_capability_2026",   # 1-5 Likert, TO FILL IN
            "sam_has_2026",          # 1-5 Likert, TO FILL IN
            "sam_notes",
        ])
        for _, r in sample.iterrows():
            w.writerow([
                r["Task ID"], r["Occupation (O*NET-SOC Title)"], r["O*NET-SOC Code"], r["Task"],
                round(r["desire_2025"], 3), round(r["capacity_2025"], 3), r["zone_2025"],
                round(r["has_worker_2025"], 3) if pd.notna(r["has_worker_2025"]) else "",
                round(r["has_expert_2025"], 3) if pd.notna(r["has_expert_2025"]) else "",
                "", "", "",
            ])

    print(f"wrote {OUT} ({len(sample)} tasks)")
    print(sample["zone_2025"].value_counts().to_string())


if __name__ == "__main__":
    main()
