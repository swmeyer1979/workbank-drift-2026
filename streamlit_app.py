from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


def load_capability_rows(data_dir: Path = DATA_DIR) -> list[dict[str, str]]:
    path = data_dir / "capability_2026.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_drift_summary(data_dir: Path = DATA_DIR) -> list[dict[str, str]]:
    path = data_dir / "drift_summary.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def unique_values(rows: Iterable[dict[str, str]], column: str) -> list[str]:
    return sorted({row[column] for row in rows if row.get(column)})


def zone_counts(rows: Iterable[dict[str, str]], column: str = "zone_2026_median") -> dict[str, int]:
    return dict(Counter(row.get(column, "Unknown") or "Unknown" for row in rows))


def migration_counts(rows: Iterable[dict[str, str]], column: str = "migration_median") -> dict[str, int]:
    return dict(Counter(row.get(column, "Unknown") or "Unknown" for row in rows))


def near_threshold_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if row.get("near_threshold", "").lower() == "true"]


def filter_rows(
    rows: Iterable[dict[str, str]],
    *,
    occupation: str | None = None,
    migration: str | None = None,
    near_threshold_only: bool = False,
) -> list[dict[str, str]]:
    filtered = list(rows)
    if occupation:
        filtered = [row for row in filtered if row.get("occupation") == occupation]
    if migration:
        filtered = [row for row in filtered if row.get("migration_median") == migration]
    if near_threshold_only:
        filtered = near_threshold_rows(filtered)
    return filtered


def select_display_columns(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    columns = [
        "task_id",
        "occupation",
        "task",
        "zone_2025",
        "zone_2026_median",
        "migration_median",
        "capability_2026_median",
        "cap_rater_stddev",
        "near_threshold",
    ]
    return [{column: row.get(column, "") for column in columns} for row in rows]


def main() -> None:
    import streamlit as st

    rows = load_capability_rows()
    st.set_page_config(page_title="WORKBank Drift 2026", layout="wide")
    st.title("WORKBank Drift 2026")
    st.caption("Derivative task-level capability drift view. Worker preference remains fixed at 2025 values.")

    occupations = unique_values(rows, "occupation")
    migrations = unique_values(rows, "migration_median")

    with st.sidebar:
        st.header("Filters")
        occupation = st.selectbox("Occupation", [""] + occupations)
        migration = st.selectbox("Migration", [""] + migrations)
        near_threshold_only = st.checkbox("Near threshold only")

    filtered = filter_rows(
        rows,
        occupation=occupation or None,
        migration=migration or None,
        near_threshold_only=near_threshold_only,
    )
    threshold_count = len(near_threshold_rows(rows))

    c1, c2, c3 = st.columns(3)
    c1.metric("Tasks", len(rows))
    c2.metric("Filtered", len(filtered))
    c3.metric("Near threshold", threshold_count)

    left, right = st.columns(2)
    with left:
        st.subheader("2026 Zone Counts")
        st.table(zone_counts(filtered))
    with right:
        st.subheader("Migration Counts")
        st.table(migration_counts(filtered))

    st.subheader("Task Drilldown")
    st.dataframe(select_display_columns(filtered), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
