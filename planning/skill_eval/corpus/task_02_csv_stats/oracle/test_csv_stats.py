"""Hidden oracle tests for task_02_csv_stats."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path


def _load_module(work_dir: Path) -> object:
    spec = importlib.util.spec_from_file_location(
        "csv_stats", str(work_dir / "csv_stats.py")
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load csv_stats.py from {work_dir}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["csv_stats"] = mod
    spec.loader.exec_module(mod)
    return mod


def _make_test_csv(path: Path) -> None:
    """Create a test CSV file with mixed column types."""
    path.write_text(
        "name,age,score,temp,notes\n"
        "Alice,30,95.5,98.6,good\n"
        "Bob,25,88.0,99.1,ok\n"
        "Charlie,,92.3,98.9,\n"
        "Diana,28,invalid,97.8,excellent\n"
        "Eve,32,90.0,,fine\n"
    )


def test_compute_stats_basic(work_dir: Path) -> dict:
    """Verify compute_stats returns correct values for a normal CSV."""
    mod = _load_module(work_dir)
    csv_path = work_dir / "_test_data.csv"
    _make_test_csv(csv_path)

    stats = mod.compute_stats(csv_path)
    numeric_cols = {"age", "score", "temp"}
    got_cols = set(stats.keys())

    if got_cols != numeric_cols:
        return {"pass": False, "expected_cols": numeric_cols, "got_cols": got_cols}

    failures = []
    # age: 30, 25, (skip), 28, 32 → n=4
    if stats["age"]["count"] != 4:
        failures.append(f"age count: got {stats['age']['count']}, expected 4")
    # age mean = (30+25+28+32)/4 = 28.75
    if abs(stats["age"]["mean"] - 28.75) > 0.01:
        failures.append(f"age mean: got {stats['age']['mean']}, expected 28.75")
    # score: 95.5, 88.0, 92.3, (invalid), 90.0 → n=4
    if stats["score"]["count"] != 4:
        failures.append(f"score count: got {stats['score']['count']}, expected 4")

    return {"pass": len(failures) == 0, "failures": failures}


def test_compute_stats_empty_csv(work_dir: Path) -> dict:
    """Verify empty CSV is handled gracefully."""
    mod = _load_module(work_dir)
    csv_path = work_dir / "_test_empty.csv"
    csv_path.write_text("name,age\n")

    stats = mod.compute_stats(csv_path)
    return {"pass": stats == {}, "got": stats}


def test_compute_stats_no_numeric(work_dir: Path) -> dict:
    """Verify CSV with no numeric columns returns empty."""
    mod = _load_module(work_dir)
    csv_path = work_dir / "_test_nonum.csv"
    csv_path.write_text("name,city\nalice,nyc\nbob,la\n")

    stats = mod.compute_stats(csv_path)
    return {"pass": stats == {}, "got": stats}


def test_write_report(work_dir: Path) -> dict:
    """Verify write_report produces a readable file."""
    mod = _load_module(work_dir)
    csv_path = work_dir / "_test_data.csv"
    _make_test_csv(csv_path)
    report_path = work_dir / "_test_report.txt"

    stats = mod.compute_stats(csv_path)
    mod.write_report(stats, report_path)

    if not report_path.exists():
        return {"pass": False, "error": "report file not created"}

    content = report_path.read_text()
    for col in ("age", "score", "temp"):
        if col not in content:
            return {"pass": False, "error": f"column '{col}' not found in report"}

    return {"pass": True}


def test_no_external_imports(work_dir: Path) -> dict:
    """Verify no external dependencies (pandas, numpy, etc.)."""
    source = (work_dir / "csv_stats.py").read_text()
    banned = ["pandas", "numpy", "polars"]
    found = [pkg for pkg in banned if f"import {pkg}" in source or f"from {pkg}" in source]
    return {"pass": len(found) == 0, "found": found}


def test_uses_pathlib(work_dir: Path) -> dict:
    """Verify pathlib is used (per task spec)."""
    source = (work_dir / "csv_stats.py").read_text()
    return {"pass": "pathlib" in source or "from pathlib" in source}


def run_all(work_dir: Path) -> dict:
    results = {}
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn) and name != "run_all":
            try:
                results[name] = fn(work_dir)
            except Exception as exc:
                results[name] = {"pass": False, "error": str(exc)}
    total = len(results)
    passed = sum(1 for r in results.values() if r.get("pass"))
    return {
        "total_checks": total,
        "passed": passed,
        "failed": total - passed,
        "pass_pct": round(passed / total * 100, 1) if total > 0 else 0.0,
        "details": results,
    }
