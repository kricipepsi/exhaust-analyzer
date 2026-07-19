from __future__ import annotations

import csv
import sys
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any

StatsRow = dict[str, float | int]
StatsResult = dict[str, StatsRow]


def compute_stats(csv_path: Path) -> StatsResult:
    """Read *csv_path* and compute summary statistics for every numeric column.

    Non-numeric and missing values are silently skipped.  Returns an empty
    dict when the CSV file has no rows or no numeric columns.
    """
    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rows.append(row)

    if not rows:
        return {}

    numeric_columns = _extract_numeric_columns(rows)
    return {col: _column_stats(vals) for col, vals in numeric_columns.items()}


def write_report(stats: StatsResult, report_path: Path) -> None:
    """Write a human-readable summary of *stats* to *report_path*."""
    lines: list[str] = []
    for col, s in sorted(stats.items()):
        lines.append(
            f"{col}: count={s['count']}, "
            f"mean={s['mean']:.2f}, median={s['median']:.2f}, "
            f"min={s['min']:.2f}, max={s['max']:.2f}, "
            f"stdev={s['stdev']:.2f}"
        )
    report_path.write_text("\n".join(lines), encoding="utf-8")


# ---- helpers ----

def _extract_numeric_columns(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    columns: dict[str, list[float]] = {}
    for key in rows[0]:
        vals: list[float] = []
        for row in rows:
            try:
                vals.append(float(row[key]))
            except (ValueError, TypeError):
                pass
        if vals:
            columns[key] = vals
    return columns


def _column_stats(values: list[float]) -> StatsRow:
    return {
        "count": len(values),
        "mean": round(mean(values), 4),
        "median": round(median(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "stdev": round(stdev(values), 4) if len(values) > 1 else 0.0,
    }


# ---- CLI ----

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compute CSV column statistics")
    parser.add_argument("csv_file", type=Path, help="Input CSV file")
    parser.add_argument("report_file", type=Path, help="Output report file")
    args = parser.parse_args()
    stats = compute_stats(args.csv_file)
    write_report(stats, args.report_file)
