from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "streamlit_app.py"


def load_app():
    spec = importlib.util.spec_from_file_location("workbank_streamlit_app", APP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load streamlit_app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    app = load_app()
    rows = app.load_capability_rows(ROOT / "data")
    if len(rows) < 100:
        print("failed: expected task rows")
        return 1
    zones = app.zone_counts(rows)
    migrations = app.migration_counts(rows)
    near = app.near_threshold_rows(rows)
    filtered = app.filter_rows(rows, occupation=rows[0]["occupation"], near_threshold_only=False)
    display = app.select_display_columns(filtered[:3])
    checks = {
        "has_green_light": "Green Light" in zones,
        "has_migrations": bool(migrations),
        "has_near_threshold_rows": bool(near),
        "filter_returns_rows": bool(filtered),
        "display_columns_limited": bool(display) and set(display[0]).issuperset({"task_id", "occupation", "task"}),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        for name in failed:
            print(f"failed: {name}")
        return 1
    print("streamlit proof: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
