from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean, median, stdev

# Public API — two functions with narrow, typed interfaces.
__all__ = ["compute_stats", "write_report"]


def compute_stats(csv_path: Path) -> dict[str, dict[str, float | int]]:
    """Return per-column statistics for numeric columns in *csv_path*."""
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return {}
    numeric = _collect_numeric(rows)
    return {col: _describe(values) for col, values in numeric.items()}


def write_report(stats: dict[str, dict[str, float | int]], report_path: Path) -> None:
    """Persist *stats* as a text summary at *report_path*."""
    report_path.write_text(_render(stats), encoding="utf-8")


# ---- internal: all complexity lives behind the two functions above ----

def _collect_numeric(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    for col in rows[0]:
        numbers = [float(r[col]) for r in rows if _is_numeric(r.get(col, ""))]
        if numbers:
            result[col] = numbers
    return result


def _is_numeric(value: str) -> bool:
    try:
        float(value)
    except (ValueError, TypeError):
        return False
    return True


def _describe(values: list[float]) -> dict[str, float | int]:
    return {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "min": min(values),
        "max": max(values),
        "stdev": stdev(values) if len(values) > 1 else 0.0,
    }


def _render(stats: dict[str, dict[str, float | int]]) -> str:
    lines = [
        f"{c}: count={v['count']}, mean={v['mean']:.2f}, median={v['median']:.2f}, "
        f"min={v['min']:.2f}, max={v['max']:.2f}, stdev={v['stdev']:.2f}"
        for c, v in sorted(stats.items())
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("report_file", type=Path)
    args = parser.parse_args()
    write_report(compute_stats(args.csv_file), args.report_file)
