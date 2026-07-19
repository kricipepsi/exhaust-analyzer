"""Hidden oracle tests for task_05_bug_fix.

Verifies the bug is fixed AND the fix is minimal (not a rewrite).
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load_module(work_dir: Path) -> object:
    spec = importlib.util.spec_from_file_location(
        "interval_merger", str(work_dir / "interval_merger.py")
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load interval_merger.py from {work_dir}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["interval_merger"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_bug_fixed_containment(work_dir: Path) -> dict:
    """Verify the containment case is fixed."""
    mod = _load_module(work_dir)
    result = mod.merge_intervals([(1, 10), (2, 5)])
    return {"pass": result == [(1, 10)], "got": result}


def test_bug_fixed_containment_multiple(work_dir: Path) -> dict:
    """Verify multiple contained intervals."""
    mod = _load_module(work_dir)
    result = mod.merge_intervals([(1, 10), (2, 5), (3, 7), (11, 12)])
    return {"pass": result == [(1, 10), (11, 12)], "got": result}


def test_basic_cases_still_work(work_dir: Path) -> dict:
    """Verify basic overlap still works."""
    mod = _load_module(work_dir)
    failures = []
    cases = [
        ("empty", [], []),
        ("single", [(5, 10)], [(5, 10)]),
        ("no_overlap", [(1, 2), (3, 4)], [(1, 2), (3, 4)]),
        ("basic", [(1, 3), (2, 6), (8, 10)], [(1, 6), (8, 10)]),
        ("touching", [(1, 3), (3, 5)], [(1, 5)]),
    ]
    for name, inp, expected in cases:
        got = mod.merge_intervals(inp)
        if got != expected:
            failures.append(f"{name}: got {got}, expected {expected}")
    return {"pass": len(failures) == 0, "failures": failures}


def test_fix_is_minimal(work_dir: Path) -> dict:
    """Verify the fix is surgical — not a full rewrite.

    The coder should modify the overlap condition, not replace the whole algorithm.
    A rewrite would have significantly different structure (e.g., different variable
    names, different approach like sweep line).
    """
    source = (work_dir / "interval_merger.py").read_text()

    # Key markers from the original that should survive
    markers = [
        "sorted(intervals",
        "merged = [",
        "merged[-1]",
        "merged.append(current)",
    ]
    missing = [m for m in markers if m not in source]
    return {"pass": len(missing) <= 1, "missing_markers": missing}


def test_has_type_hints(work_dir: Path) -> dict:
    """Verify type hints are present."""
    mod = _load_module(work_dir)
    hints = getattr(mod.merge_intervals, "__annotations__", {})
    return {"pass": "return" in hints, "annotations": hints}


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
