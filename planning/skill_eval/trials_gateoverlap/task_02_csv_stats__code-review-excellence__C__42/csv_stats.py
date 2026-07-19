from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean, median, stdev

StatsRow = dict[str, float | int]
StatsResult = dict[str, StatsRow]


def compute_stats(csv_path: Path) -> StatsResult:
    """Compute summary statistics for every numeric column in *csv_path*.

    Non-numeric and missing values are skipped (reviewed edge case). Returns an
    empty dict when the file has no rows or no numeric columns.
    """
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return {}
    numeric = _numeric_columns(rows)
    return {column: _summarize(values) for column, values in numeric.items()}


def write_report(stats: StatsResult, report_path: Path) -> None:
    """Write one summary line per column to *report_path* (every column reported)."""
    lines = [
        f"{column}: count={row['count']}, mean={row['mean']:.2f}, "
        f"min={row['min']:.2f}, max={row['max']:.2f}"
        for column, row in sorted(stats.items())
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


def _numeric_columns(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    columns: dict[str, list[float]] = {}
    for key in rows[0]:
        values: list[float] = []
        for row in rows:
            try:
                values.append(float(row[key]))
            except (ValueError, TypeError):
                continue   # skip non-numeric / missing cells gracefully
        if values:
            columns[key] = values
    return columns


def _summarize(values: list[float]) -> StatsRow:
    return {
        "count": len(values),
        "mean": round(mean(values), 4),
        "median": round(median(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "stdev": round(stdev(values), 4) if len(values) > 1 else 0.0,
    }
