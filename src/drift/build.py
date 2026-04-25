"""Build derivative CSVs from raw WORKBank + per-rater score files.

Outputs:
  data/capability_2026.csv   -- one row per task, 2025 vs 2026, zone migration
  data/has_drift_2026.csv    -- Human Agency Scale drift (bonus axis)
  data/drift_summary.csv     -- 4x4 zone transition counts
  reports/inter_model.md     -- Krippendorff alpha + pairwise Spearman
  reports/calibration.md     -- (if sam_capability_2026 present) kappa vs ensemble

Run AFTER `score-capability`. Reads the latest runs/raters/<run_id>/.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

import pandas as pd

from drift.zones import migration_label, zone_of

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
RUNS = ROOT / "runs" / "raters"
DATA = ROOT / "data"


def latest_run_dir() -> Path:
    runs = sorted([p for p in RUNS.iterdir() if p.is_dir()])
    if not runs:
        raise SystemExit("no runs found under runs/raters/")
    return runs[-1]


def load_rater_scores(run_dir: Path) -> pd.DataFrame:
    rows = []
    for jsonl in run_dir.glob("*.jsonl"):
        for line in jsonl.read_text().splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            if "error" in d:
                continue
            rows.append(d)
    return pd.DataFrame(rows)


def build(run_dir: Path) -> None:
    desires = pd.read_csv(RAW / "domain_worker_desires.csv")
    experts = pd.read_csv(RAW / "expert_rated_technological_capability.csv")
    meta = pd.read_csv(RAW / "task_statement_with_metadata.csv")

    d25 = desires.groupby("Task ID")["Automation Desire Rating"].mean().rename("desire_2025")
    c25 = experts.groupby("Task ID")["Automation Capacity Rating"].mean().rename("capacity_2025")
    task_meta = (
        meta[["Task ID", "Occupation (O*NET-SOC Title)", "Task"]]
        .drop_duplicates("Task ID")
        .set_index("Task ID")
    )
    base = pd.concat([d25, c25], axis=1).dropna().join(task_meta, how="inner").reset_index()

    scores = load_rater_scores(run_dir)
    if scores.empty:
        raise SystemExit(f"no valid scores in {run_dir}")

    # One row per (task, rater) -> pivot to task rows with per-rater columns
    wide = scores.pivot_table(
        index="task_id",
        columns="rater",
        values=["capability_score", "has_score"],
        aggfunc="first",
    )
    wide.columns = [f"{v}_{r}" for v, r in wide.columns]
    wide = wide.reset_index().rename(columns={"task_id": "Task ID"})

    df = base.merge(wide, on="Task ID", how="left")

    cap_cols = [c for c in df.columns if c.startswith("capability_score_")]
    has_cols = [c for c in df.columns if c.startswith("has_score_")]

    def med(row: pd.Series, cols: list[str]) -> float:
        vals = [row[c] for c in cols if pd.notna(row[c])]
        return statistics.median(vals) if vals else float("nan")

    def mean_(row: pd.Series, cols: list[str]) -> float:
        vals = [row[c] for c in cols if pd.notna(row[c])]
        return statistics.fmean(vals) if vals else float("nan")

    df["capability_2026_median"] = df.apply(lambda r: med(r, cap_cols), axis=1)
    df["capability_2026_mean"] = df.apply(lambda r: mean_(r, cap_cols), axis=1)
    df["has_2026_median"] = df.apply(lambda r: med(r, has_cols), axis=1)
    df["has_2026_mean"] = df.apply(lambda r: mean_(r, has_cols), axis=1)

    df["zone_2025"] = df.apply(lambda r: zone_of(r["capacity_2025"], r["desire_2025"]), axis=1)
    df["zone_2026_median"] = df.apply(
        lambda r: zone_of(r["capability_2026_median"], r["desire_2025"]) if pd.notna(r["capability_2026_median"]) else None,
        axis=1,
    )
    df["zone_2026_mean"] = df.apply(
        lambda r: zone_of(r["capability_2026_mean"], r["desire_2025"]) if pd.notna(r["capability_2026_mean"]) else None,
        axis=1,
    )
    df["migration_median"] = df.apply(
        lambda r: migration_label(r["zone_2025"], r["zone_2026_median"]) if r["zone_2026_median"] else None, axis=1
    )
    df["migration_mean"] = df.apply(
        lambda r: migration_label(r["zone_2025"], r["zone_2026_mean"]) if r["zone_2026_mean"] else None, axis=1
    )
    df["delta_median"] = df["capability_2026_median"] - df["capacity_2025"]
    df["delta_mean"] = df["capability_2026_mean"] - df["capacity_2025"]

    # Near-threshold flag: tasks in [2.5, 3.5] on either aggregation need hand adjudication
    NEAR_LO, NEAR_HI = 2.5, 3.5
    df["near_threshold"] = (
        ((df["capability_2026_median"] >= NEAR_LO) & (df["capability_2026_median"] <= NEAR_HI)) |
        ((df["capability_2026_mean"]   >= NEAR_LO) & (df["capability_2026_mean"]   <= NEAR_HI))
    )

    # Inter-rater disagreement (stddev across raters) — also a confidence signal
    import numpy as np
    df["cap_rater_stddev"] = df[cap_cols].std(axis=1, ddof=0)
    df["has_rater_stddev"] = df[has_cols].std(axis=1, ddof=0)

    cap_out = df.rename(columns={
        "Task ID": "task_id",
        "Occupation (O*NET-SOC Title)": "occupation",
        "Task": "task",
    })
    col_order = [
        "task_id", "occupation", "task",
        "desire_2025", "capacity_2025", "zone_2025",
        *cap_cols,
        "capability_2026_median", "capability_2026_mean",
        "cap_rater_stddev",
        "zone_2026_median", "zone_2026_mean",
        "migration_median", "migration_mean",
        "delta_median", "delta_mean",
        "near_threshold",
    ]
    cap_out[col_order].to_csv(DATA / "capability_2026.csv", index=False)

    has_out = df[["Task ID", "Occupation (O*NET-SOC Title)", "Task",
                  *has_cols, "has_2026_median", "has_2026_mean"]]
    has_out.to_csv(DATA / "has_drift_2026.csv", index=False)

    trans = (
        df.dropna(subset=["zone_2026_median"])
          .groupby(["zone_2025", "zone_2026_median"]).size()
          .rename("count").reset_index()
    )
    trans.to_csv(DATA / "drift_summary.csv", index=False)

    print(f"wrote capability_2026.csv ({len(cap_out)} rows)")
    print(f"wrote has_drift_2026.csv ({len(has_out)} rows)")
    print(f"wrote drift_summary.csv ({len(trans)} rows)")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", type=str, default=None, help="runs/raters/<id>; defaults to latest")
    a = p.parse_args()
    build(Path(a.run_dir) if a.run_dir else latest_run_dir())


if __name__ == "__main__":
    main()
