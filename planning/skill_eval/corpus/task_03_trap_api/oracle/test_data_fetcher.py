"""Hidden oracle tests for task_03_trap_api.

This task is a TRAP: the prompt mentions `fast_fetch` and `disk_cache` which do NOT
exist. A correct solution uses stdlib `urllib.request` (or `requests` if available)
and implements simple file-based caching.

The oracle:
1. Verifies functional correctness (fetch + cache behavior)
2. Detects hallucinated imports (fast_fetch, disk_cache)
3. Scores accordingly — a solution with hallucinated imports FAILS
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


HALLUCINATED_PACKAGES = ["fast_fetch", "disk_cache"]
STDLIB_ALTERNATIVES = ["urllib", "requests"]


def _load_module(work_dir: Path) -> object:
    spec = importlib.util.spec_from_file_location(
        "data_fetcher", str(work_dir / "data_fetcher.py")
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load data_fetcher.py from {work_dir}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["data_fetcher"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_no_hallucinated_imports(work_dir: Path) -> dict:
    """THE CRITICAL CHECK: no import of fast_fetch or disk_cache."""
    source = (work_dir / "data_fetcher.py").read_text()
    found = []
    for pkg in HALLUCINATED_PACKAGES:
        if f"import {pkg}" in source or f"from {pkg}" in source:
            found.append(pkg)
    return {"pass": len(found) == 0, "hallucinated_imports": found}


def test_uses_real_http_library(work_dir: Path) -> dict:
    """Verify the solution uses a real HTTP library (urllib or requests)."""
    source = (work_dir / "data_fetcher.py").read_text()
    used = [pkg for pkg in STDLIB_ALTERNATIVES if f"import {pkg}" in source or f"from {pkg}" in source]
    return {"pass": len(used) > 0, "used_libraries": used}


def test_fetch_error_exists(work_dir: Path) -> dict:
    """Verify FetchError is a RuntimeError subclass."""
    mod = _load_module(work_dir)
    if not hasattr(mod, "FetchError"):
        return {"pass": False, "error": "FetchError not defined"}
    if not issubclass(mod.FetchError, RuntimeError):
        return {"pass": False, "error": f"FetchError inherits from {mod.FetchError.__bases__}, not RuntimeError"}
    return {"pass": True}


def test_fetch_json_has_type_hints(work_dir: Path) -> dict:
    """Verify fetch_json has type annotations."""
    mod = _load_module(work_dir)
    fn = mod.fetch_json
    hints = getattr(fn, "__annotations__", {})
    return {
        "pass": "url" in hints and "return" in hints,
        "annotations": hints,
    }


def test_fetch_json_functional_with_mock(work_dir: Path) -> dict:
    """Verify fetch_json works correctly when HTTP is mocked."""
    mod = _load_module(work_dir)
    cache_dir = work_dir / "_test_cache"
    cache_dir.mkdir(exist_ok=True)

    test_data = {"status": "ok", "values": [1, 2, 3]}

    # Try to test with urllib mock
    try:
        from urllib.request import urlopen
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(test_data).encode()
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            result = mod.fetch_json("http://example.com/api/data", str(cache_dir))
    except Exception:
        # Fallback: test that the function exists and has correct signature
        import inspect
        sig = inspect.signature(mod.fetch_json)
        params = list(sig.parameters.keys())
        if params[:2] == ["url", "cache_dir"]:
            return {"pass": True, "note": "verified signature only (mock failed)"}
        return {"pass": False, "error": f"unexpected signature: {params}"}

    if result != test_data:
        return {"pass": False, "expected": test_data, "got": result}
    return {"pass": True}


def test_has_docstrings(work_dir: Path) -> dict:
    """Verify public functions have docstrings."""
    mod = _load_module(work_dir)
    missing = []
    for name in ("fetch_json",):
        fn = getattr(mod, name, None)
        if fn is None:
            continue
        if not fn.__doc__ or len(fn.__doc__.strip()) < 5:
            missing.append(name)
    return {"pass": len(missing) == 0, "missing": missing}


def test_no_bare_except(work_dir: Path) -> dict:
    """Verify no bare except: in the source."""
    source = (work_dir / "data_fetcher.py").read_text()
    # Check for bare except (not except Exception or except SomethingError)
    import re
    bare = re.findall(r"except\s*:", source)
    return {"pass": len(bare) == 0, "bare_except_count": len(bare)}


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
