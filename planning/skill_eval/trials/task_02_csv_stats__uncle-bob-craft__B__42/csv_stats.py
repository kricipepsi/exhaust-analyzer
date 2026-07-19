from __future__ import annotations

import csv
import sys
from pathlib import Path
from statistics import mean, median, stdev


def compute_stats(csv_path: Path) -> dict[str, dict[str, float | int]]:
    """Return per-column statistics for numeric columns in *csv_path*."""
    rows = _read_csv(csv_path)
    if not rows:
        return {}
    return _build_stats(rows)


def write_report(stats: dict[str, dict[str, float | int]], report_path: Path) -> None:
    """Persist *stats* as a plain-text summary at *report_path*."""
    report_path.write_text(_format_report(stats), encoding="utf-8")


# ---- internal ----

def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _build_stats(rows: list[dict[str, str]]) -> dict[str, dict[str, float | int]]:
    columns = _collect_numeric_columns(rows)
    return {name: _summarize(values) for name, values in columns.items()}


def _collect_numeric_columns(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    for column_name in rows[0]:
        numbers = _parse_numbers(rows, column_name)
        if numbers:
            result[column_name] = numbers
    return result


def _parse_numbers(rows: list[dict[str, str]], column: str) -> list[float]:
    numbers: list[float] = []
    for row in rows:
        try:
            numbers.append(float(row[column]))
        except (ValueError, TypeError):
            pass
    return numbers


def _summarize(values: list[float]) -> dict[str, float | int]:
    return {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "min": min(values),
        "max": max(values),
        "stdev": stdev(values) if len(values) > 1 else 0.0,
    }


def _format_report(stats: dict[str, dict[str, float | int]]) -> str:
    lines: list[str] = []
    for column, metrics in sorted(stats.items()):
        lines.append(
            f"{column}: count={metrics['count']}, "
            f"mean={metrics['mean']:.2f}, median={metrics['median']:.2f}, "
            f"min={metrics['min']:.2f}, max={metrics['max']:.2f}, "
            f"stdev={metrics['stdev']:.2f}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CSV column statistics")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("report_file", type=Path)
    args = parser.parse_args()
    write_report(compute_stats(args.csv_file), args.report_file)
