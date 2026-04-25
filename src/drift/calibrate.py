"""Isotonic calibration from ensemble raw scores to human-consensus.

Fits on the 50-task calibration set (sam+r2 average as ground truth).
Monotonic-increasing mapping — preserves rank, corrects amplitude compression.
Leave-one-out cross-validation reported alongside.

Usage:
    from drift.calibrate import fit_calibration, load_calibration, apply_calibration
"""

from __future__ import annotations

import csv
import json
import pickle
import statistics
from pathlib import Path

import numpy as np
from sklearn.isotonic import IsotonicRegression

ROOT = Path(__file__).resolve().parents[2]
CAL_DIR = ROOT / "data" / "calibrators"


def _consensus() -> dict[int, tuple[float, float]]:
    sam = {}
    for r in csv.DictReader((ROOT / "data/calibration_rater1.csv").open()):
        sam[int(r["task_id"])] = (int(r["sam_capability_2026"]), int(r["sam_has_2026"]))
    r2 = {}
    for r in csv.DictReader((ROOT / "data/calibration_rater2.csv").open()):
        r2[int(r["task_id"])] = (int(r["rater2_capability_2026"]), int(r["rater2_has_2026"]))
    return {t: ((sam[t][0] + r2[t][0]) / 2, (sam[t][1] + r2[t][1]) / 2) for t in sam}


def _load_ensemble_raw(run_dir: Path) -> dict[int, tuple[float, float]]:
    """Return {task_id: (cap_median_float, has_median_float)} across all raters in run_dir."""
    per_rater: dict[str, dict[int, tuple[int, int]]] = {}
    for f in run_dir.glob("*.jsonl"):
        per_rater[f.stem] = {}
        for line in f.open():
            d = json.loads(line)
            if "error" in d:
                continue
            per_rater[f.stem][d["task_id"]] = (int(d["capability_score"]), int(d["has_score"]))
    task_ids = set.intersection(*[set(d.keys()) for d in per_rater.values()])
    out = {}
    for t in task_ids:
        caps = [per_rater[r][t][0] for r in per_rater]
        hases = [per_rater[r][t][1] for r in per_rater]
        out[t] = (statistics.median(caps), statistics.median(hases))
    return out


def fit_calibration(cal_run_dir: Path) -> dict:
    cons = _consensus()
    ens = _load_ensemble_raw(cal_run_dir)
    tids = sorted(set(cons) & set(ens))

    X_cap = np.array([ens[t][0] for t in tids])
    y_cap = np.array([cons[t][0] for t in tids])
    X_has = np.array([ens[t][1] for t in tids])
    y_has = np.array([cons[t][1] for t in tids])

    cap_iso = IsotonicRegression(out_of_bounds="clip", y_min=1.0, y_max=5.0).fit(X_cap, y_cap)
    has_iso = IsotonicRegression(out_of_bounds="clip", y_min=1.0, y_max=5.0).fit(X_has, y_has)

    # Leave-one-out cross-val
    def loocv(X, y):
        preds = []
        for i in range(len(X)):
            mask = np.ones(len(X), dtype=bool); mask[i] = False
            m = IsotonicRegression(out_of_bounds="clip", y_min=1.0, y_max=5.0).fit(X[mask], y[mask])
            preds.append(float(m.predict(np.array([X[i]]))[0]))
        preds = np.array(preds)
        return {
            "mae_loocv": float(np.mean(np.abs(preds - y))),
            "mae_raw":   float(np.mean(np.abs(X - y))),
        }

    cap_cv = loocv(X_cap, y_cap)
    has_cv = loocv(X_has, y_has)

    CAL_DIR.mkdir(parents=True, exist_ok=True)
    with (CAL_DIR / "cap_isotonic.pkl").open("wb") as f:
        pickle.dump(cap_iso, f)
    with (CAL_DIR / "has_isotonic.pkl").open("wb") as f:
        pickle.dump(has_iso, f)

    # Fit MAE (in-sample)
    fit_mae_cap = float(np.mean(np.abs(cap_iso.predict(X_cap) - y_cap)))
    fit_mae_has = float(np.mean(np.abs(has_iso.predict(X_has) - y_has)))

    summary = {
        "n_calibration_tasks": len(tids),
        "capability": {
            "mae_raw":      cap_cv["mae_raw"],
            "mae_fit":      fit_mae_cap,
            "mae_loocv":    cap_cv["mae_loocv"],
            "breakpoints":  [(float(x), float(cap_iso.predict(np.array([x]))[0])) for x in sorted(set(X_cap))],
        },
        "has": {
            "mae_raw":      has_cv["mae_raw"],
            "mae_fit":      fit_mae_has,
            "mae_loocv":    has_cv["mae_loocv"],
            "breakpoints":  [(float(x), float(has_iso.predict(np.array([x]))[0])) for x in sorted(set(X_has))],
        },
    }
    (CAL_DIR / "calibration_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def load_calibration() -> tuple[IsotonicRegression, IsotonicRegression]:
    with (CAL_DIR / "cap_isotonic.pkl").open("rb") as f:
        cap = pickle.load(f)
    with (CAL_DIR / "has_isotonic.pkl").open("rb") as f:
        has = pickle.load(f)
    return cap, has


def apply_calibration(cap_raw: float, has_raw: float) -> tuple[float, float]:
    cap_iso, has_iso = load_calibration()
    return (
        float(cap_iso.predict(np.array([cap_raw]))[0]),
        float(has_iso.predict(np.array([has_raw]))[0]),
    )
