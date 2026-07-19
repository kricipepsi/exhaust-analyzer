"""Hidden oracle tests for task_04_refactor.

Tests that the refactored module preserves the original behavior AND improves quality.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load_module(work_dir: Path) -> object:
    spec = importlib.util.spec_from_file_location(
        "legacy_processor", str(work_dir / "legacy_processor.py")
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load legacy_processor.py from {work_dir}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["legacy_processor"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_behavior_preserved(work_dir: Path) -> dict:
    """Verify refactored code produces same results as original on standard input."""
    mod = _load_module(work_dir)

    readings = [
        {"sensor_id": "S1", "value": 75.0, "unit": "C"},
        {"sensor_id": "S2", "value": 30.0, "unit": "C"},
        {"sensor_id": "S3", "value": None, "unit": "C"},       # invalid
        {"sensor_id": "S4", "value": -5.0, "unit": "V"},       # invalid
        {"sensor_id": "S5", "value": 120.0, "unit": "rpm"},
        {"sensor_id": "S6", "value": 55.0, "unit": "C"},
        {"sensor_id": "S7", "value": 99.0, "unit": "pct"},
        {"sensor_id": "S8", "value": 200.0, "unit": "Pa"},     # alert > 50
    ]

    result = mod.process_readings(readings, threshold=50.0)

    failures = []
    if result["total_readings"] != 8:
        failures.append(f"total_readings: {result['total_readings']}")
    if result["valid_readings"] != 6:
        failures.append(f"valid_readings: {result['valid_readings']}")
    if result["invalid_readings"] != 2:
        failures.append(f"invalid_readings: {result['invalid_readings']}")
    if len(result["alerts"]) != 5:  # 75, 120, 55, 99, 200 are > 50
        failures.append(f"alerts count: {len(result['alerts'])}")

    return {"pass": len(failures) == 0, "failures": failures}


def test_behavior_empty_input(work_dir: Path) -> dict:
    """Verify empty input produces sensible output."""
    mod = _load_module(work_dir)
    result = mod.process_readings([], threshold=50.0)
    failures = []
    if result["total_readings"] != 0:
        failures.append(f"total_readings: {result['total_readings']}")
    if result["valid_readings"] != 0:
        failures.append(f"valid_readings: {result['valid_readings']}")
    if len(result["alerts"]) != 0:
        failures.append(f"alerts: {result['alerts']}")
    return {"pass": len(failures) == 0, "failures": failures}


def test_no_bare_except(work_dir: Path) -> dict:
    """Verify no bare except: in refactored code."""
    source = (work_dir / "legacy_processor.py").read_text()
    bare = re.findall(r"except\s*:", source)
    return {"pass": len(bare) == 0, "bare_except_count": len(bare)}


def test_no_mutable_defaults(work_dir: Path) -> dict:
    """Verify no mutable default arguments."""
    source = (work_dir / "legacy_processor.py").read_text()
    patterns = [
        r"def \w+\(.*=\s*\[\]",
        r"def \w+\(.*=\s*\{\}",
    ]
    found = []
    for pat in patterns:
        matches = re.findall(pat, source)
        found.extend(matches)
    return {"pass": len(found) == 0, "found": found}


def test_uses_modern_union_syntax(work_dir: Path) -> dict:
    """Verify X | Y used instead of Union[X, Y]."""
    source = (work_dir / "legacy_processor.py").read_text()
    uses_union = "Union[" in source
    uses_pipe = "|" in source
    # Pipe should appear in type hints; Union[...] should not
    return {"pass": not uses_union, "uses_old_union": uses_union}


def test_functions_extracted(work_dir: Path) -> dict:
    """Verify the refactored code has more than 1 function (i.e., was decomposed)."""
    source = (work_dir / "legacy_processor.py").read_text()
    fn_count = len(re.findall(r"^def \w+", source, re.MULTILINE))
    return {"pass": fn_count >= 3, "function_count": fn_count}


def test_has_type_hints(work_dir: Path) -> dict:
    """Verify process_readings has type hints."""
    mod = _load_module(work_dir)
    hints = getattr(mod.process_readings, "__annotations__", {})
    return {"pass": len(hints) >= 2, "annotations": hints}


def test_complexity_reduced(work_dir: Path) -> dict:
    """Verify max function length is reasonable (< 50 lines)."""
    source = (work_dir / "legacy_processor.py").read_text()
    lines = source.split("\n")
    # Find max function length
    in_fn = False
    fn_lines: list[int] = []
    current_count = 0
    for line in lines:
        if re.match(r"^def \w+", line):
            if in_fn:
                fn_lines.append(current_count)
            in_fn = True
            current_count = 0
        elif in_fn:
            current_count += 1
    if in_fn:
        fn_lines.append(current_count)

    max_len = max(fn_lines) if fn_lines else 0
    return {"pass": max_len < 50, "max_function_lines": max_len}


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
