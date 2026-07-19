# Task: CSV Statistics Module

**Difficulty:** Medium · **Type:** Known-API (stdlib csv + pathlib) · **Primary axes:** rubric (structure/cohesion), first-pass quality

## Prompt

Write a Python module `csv_stats.py` that:

1. Reads a CSV file from a given path (use `pathlib.Path`).
2. Automatically detects which columns are numeric (int or float).
3. For each numeric column, computes: count, mean, median, min, max, standard deviation.
4. Writes a summary report to a text file: one line per column with the stats.

The module should be usable as both a script and an importable library:

```python
# As library
from csv_stats import compute_stats, write_report
stats = compute_stats(Path("data.csv"))
write_report(stats, Path("report.txt"))

# As script
# python csv_stats.py data.csv report.txt
```

## Constraints

- Use only stdlib: `csv`, `pathlib`, `statistics`, `sys`/`argparse`.
- Handle missing/non-numeric values in numeric columns gracefully (skip them with a warning count).
- Handle empty CSV and CSV with no numeric columns gracefully.
- No external dependencies (no pandas, no numpy).

## Requirements

- Type hints on all function signatures
- Docstrings on all public functions
- Tests in `test_csv_stats.py` that create a temp CSV and verify stats output

## Output

Write `csv_stats.py` and `test_csv_stats.py` in the working directory.
