"""pytest plugin (-p p4_guard): control (iii) import-path guard + per-failure exception type capture.

Env: P4_ROOT (copy root every guarded module must live under), P4_MODULES (comma list), P4_OUT (json).
"""

from __future__ import annotations

import importlib
import json
import os
import sys

import pytest

_ROOT = os.environ.get("P4_ROOT", "")
_MODS = [m for m in os.environ.get("P4_MODULES", "").split(",") if m]
_STATE: dict = {"modules": {}, "modules_end": {}, "failures": [], "guard_ok": None}

_ASSERTION_TYPES = {"AssertionError", "Failed"}  # Failed = pytest.fail / pytest.raises DID NOT RAISE


def _leaf_types(exc: BaseException) -> list[str]:
    if isinstance(exc, BaseExceptionGroup):
        out: list[str] = []
        for e in exc.exceptions:
            out.extend(_leaf_types(e))
        return out
    return [type(exc).__name__]


def _record(nodeid: str, when: str, exc: BaseException | None, typename: str | None = None) -> None:
    types = _leaf_types(exc) if exc is not None else [typename or "Unknown"]
    kind = "assertion" if all(t in _ASSERTION_TYPES for t in types) else "crash"
    _STATE["failures"].append({"nodeid": nodeid, "when": when, "types": sorted(set(types)),
                               "kind": kind})


def pytest_collection_finish(session):  # noqa: ARG001
    ok = True
    for m in _MODS:
        try:
            mod = importlib.import_module(m)
            f = os.path.realpath(mod.__file__ or "")
        except Exception as e:  # noqa: BLE001
            f = f"IMPORT-FAILED {type(e).__name__}"
        _STATE["modules"][m] = f
        ok = ok and f.startswith(_ROOT + os.sep)
    _STATE["guard_ok"] = ok
    if not ok:
        _flush()
        pytest.exit(f"P4 guard: module outside copy root: {_STATE['modules']}", returncode=99)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.failed:
        exc = call.excinfo.value if call.excinfo is not None else None
        _record(item.nodeid, rep.when, exc)


def pytest_collectreport(report):
    if report.failed:
        msg = str(report.longrepr)
        tn = "CollectionError"
        for cand in ("ModuleNotFoundError", "ImportError", "SyntaxError", "NameError",
                     "AttributeError", "TypeError"):
            if cand in msg:
                tn = cand
                break
        _record(report.nodeid, "collect", None, tn)


def _flush() -> None:
    out = os.environ.get("P4_OUT")
    if out:
        with open(out, "w") as fh:
            json.dump(_STATE, fh, sort_keys=True)


def pytest_sessionfinish(session, exitstatus):  # noqa: ARG001
    for m in _MODS:
        mod = sys.modules.get(m)
        _STATE["modules_end"][m] = os.path.realpath(mod.__file__) if mod and mod.__file__ else None
        if _STATE["modules_end"][m] and not _STATE["modules_end"][m].startswith(_ROOT + os.sep):
            _STATE["guard_ok"] = False
    _STATE["exitstatus"] = int(exitstatus)
    _flush()
