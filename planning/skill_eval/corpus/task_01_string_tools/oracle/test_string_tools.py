"""Hidden oracle tests for task_01_string_tools.

These tests are NOT shown to the coder. The runner uses them to verify correctness
after the coder has produced their solution.
"""

from __future__ import annotations

import importlib.util
import inspect
import re
import sys
from pathlib import Path


def _load_module(work_dir: Path) -> object:
    """Load string_tools module from a working directory."""
    spec = importlib.util.spec_from_file_location(
        "string_tools", str(work_dir / "string_tools.py")
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load string_tools.py from {work_dir}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["string_tools"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_count_vowels_basic(work_dir: Path) -> dict:
    """Verify count_vowels correctness."""
    mod = _load_module(work_dir)
    result = mod.count_vowels("Hello World")
    expected = {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}
    failures = []
    for v in "aeiou":
        if result.get(v, 0) != expected[v]:
            failures.append(f"vowel '{v}': got {result.get(v)}, expected {expected[v]}")
    return {"pass": len(failures) == 0, "failures": failures}


def test_count_vowels_case_insensitive(work_dir: Path) -> dict:
    """Verify vowels are counted case-insensitively."""
    mod = _load_module(work_dir)
    result = mod.count_vowels("AaEeIiOoUu")
    expected = {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}
    failures = []
    for v in "aeiou":
        if result.get(v, 0) != expected[v]:
            failures.append(f"vowel '{v}': got {result.get(v)}, expected {expected[v]}")
    return {"pass": len(failures) == 0, "failures": failures}


def test_count_vowels_empty(work_dir: Path) -> dict:
    """Verify empty input returns zero counts."""
    mod = _load_module(work_dir)
    result = mod.count_vowels("")
    expected = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    return {"pass": result == expected, "result": result}


def test_longest_word_basic(work_dir: Path) -> dict:
    """Verify longest_word returns correct word."""
    mod = _load_module(work_dir)
    result = mod.longest_word("the quick brown fox jumps")
    return {"pass": result == "quick", "got": result}


def test_longest_word_tie_first(work_dir: Path) -> dict:
    """Verify first of tied words is returned."""
    mod = _load_module(work_dir)
    result = mod.longest_word("cat dog bat")
    return {"pass": result == "cat", "got": result}


def test_longest_word_empty(work_dir: Path) -> dict:
    """Verify empty input returns None."""
    mod = _load_module(work_dir)
    result = mod.longest_word("")
    return {"pass": result is None, "got": result}


def test_is_palindrome_basic(work_dir: Path) -> dict:
    """Verify palindrome detection."""
    mod = _load_module(work_dir)
    cases = [
        ("racecar", True),
        ("A man a plan a canal Panama", True),
        ("hello", False),
        ("", True),
        ("a", True),
        ("No lemon, no melon", True),
    ]
    failures = []
    for text, expected in cases:
        got = mod.is_palindrome(text)
        if got != expected:
            failures.append(f"is_palindrome({text!r}): got {got}, expected {expected}")
    return {"pass": len(failures) == 0, "failures": failures}


def test_has_type_hints(work_dir: Path) -> dict:
    """Verify all functions have type hints."""
    mod = _load_module(work_dir)
    missing = []
    for name in ("count_vowels", "longest_word", "is_palindrome"):
        fn = getattr(mod, name, None)
        if fn is None:
            missing.append(f"{name}: not found")
            continue
        hints = inspect.getfullargspec(fn).annotations
        if not hints:
            missing.append(f"{name}: no annotations")
        elif "return" not in getattr(fn, "__annotations__", {}):
            missing.append(f"{name}: no return annotation")
    return {"pass": len(missing) == 0, "missing": missing}


def test_has_docstrings(work_dir: Path) -> dict:
    """Verify all public functions have docstrings."""
    mod = _load_module(work_dir)
    missing = []
    for name in ("count_vowels", "longest_word", "is_palindrome"):
        fn = getattr(mod, name, None)
        if fn is None:
            continue
        if not fn.__doc__ or len(fn.__doc__.strip()) < 5:
            missing.append(name)
    return {"pass": len(missing) == 0, "missing": missing}


def test_no_mutable_defaults(work_dir: Path) -> dict:
    """Verify no mutable default arguments."""
    source = (work_dir / "string_tools.py").read_text()
    # Check for common mutable default patterns
    mutable_patterns = [
        r"def \w+\(.*=\s*\[\]",    # def f(x=[])
        r"def \w+\(.*=\s*\{\}",    # def f(x={})
        r"def \w+\(.*=\s*set\(\)", # def f(x=set())
        r"def \w+\(.*=\s*dict\(\)",# def f(x=dict())
        r"def \w+\(.*=\s*list\(\)",# def f(x=list())
    ]
    found = []
    for pat in mutable_patterns:
        matches = re.findall(pat, source)
        if matches:
            found.extend(matches)
    return {"pass": len(found) == 0, "found": found}


def run_all(work_dir: Path) -> dict:
    """Run all oracle checks and return a summary."""
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
