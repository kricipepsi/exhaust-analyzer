import csv
import statistics


def compute_stats(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    result = {}
    for col in rows[0].keys():               # BUG: IndexError when rows == []
        vals = [float(r[col]) for r in rows]  # BUG: ValueError on non-numeric/blank
        result[col] = {
            "count": len(vals),
            "mean": statistics.mean(vals),
            "median": statistics.median(vals),
            "min": min(vals),
            "max": max(vals),
            "stdev": statistics.stdev(vals),
        }
    return result


def write_report(stats, path):
    with open(path, "w") as f:
        for col, s in stats.items():
            f.write(col + ": " + str(s) + "\n")
