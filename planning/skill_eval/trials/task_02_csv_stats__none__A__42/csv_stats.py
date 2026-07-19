import csv
import sys
from pathlib import Path
from statistics import mean, median, stdev


def compute_stats(path):
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        return {}

    numeric_cols = {}
    for key in rows[0]:
        vals = []
        for row in rows:
            try:
                vals.append(float(row[key]))
            except (ValueError, TypeError):
                pass
        if vals:
            numeric_cols[key] = vals

    result = {}
    for col, vals in numeric_cols.items():
        result[col] = {
            "count": len(vals),
            "mean": mean(vals),
            "median": median(vals),
            "min": min(vals),
            "max": max(vals),
            "stdev": stdev(vals) if len(vals) > 1 else 0.0,
        }
    return result


def write_report(stats, path):
    with open(path, "w") as f:
        for col, s in stats.items():
            f.write(f"{col}: count={s['count']}, mean={s['mean']:.2f}, median={s['median']:.2f}, min={s['min']:.2f}, max={s['max']:.2f}, stdev={s['stdev']:.2f}\n")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        stats = compute_stats(Path(sys.argv[1]))
        write_report(stats, Path(sys.argv[2]))
