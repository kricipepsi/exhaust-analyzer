from __future__ import annotations

import csv
import statistics


def compute_stats(path):
    with open(path) as handle:
        rows = list(csv.DictReader(handle))
    result = {}
    columns = rows[0].keys()                     # BUG: IndexError on empty file
    for column in columns:
        values = [float(row[column]) for row in rows]   # BUG: ValueError on text
        result[column] = {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stdev": statistics.stdev(values),
        }
    return result


def write_report(stats, path):
    lines = [f"{column}: {row}" for column, row in stats.items()]
    with open(path, "w") as handle:
        handle.write("\n".join(lines))
