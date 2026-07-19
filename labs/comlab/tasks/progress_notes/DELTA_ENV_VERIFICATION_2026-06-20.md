# DELTA env diagnosis + verification record — 2026-06-20 (architect, Cowork)

Run on the **mandated** interpreter `C:\Workspace\.sandbox-py\bin\python3.14` (Python **3.14.5**, pydantic **2.13.4**, pytest **9.1.0**), executed under a Linux userland (the ELF interpreter cannot run under native Windows PowerShell). This record exists to clear the stale-ledger guard that tripped during the `T-COMV2-DELTA-2` session, which ran in a **broken** environment (DTCLab venv + pyright with no interpreter configured).

## Ground truth (mandated interpreter)

| Gate | Result |
|---|---|
| `ruff check` (delta files + schemas + tests) | **All checks passed** |
| `pytest tests/` | **370 passed · 2 failed · 12 skipped** |
| `pytest tests/unit/test_delta_engine.py` | **23 passed** (0 fail) |
| `pyright comlab/analytics/delta_engine.py comlab/core/lab_pipeline_aggregator.py --pythonpath .sandbox-py/bin/python3.14` | **0 errors, 0 warnings** |

## The 2 test failures are the known-red baseline (NOT delta)

```
FAILED tests/unit/test_fault_atlas_router_v2.py::test_v1_when_explicit_false
FAILED tests/unit/test_fault_atlas_router_v2.py::test_v2_when_explicit_true
  → ModuleNotFoundError: No module named 'registry'
```
The `registry` module is absent from this checkout (same family as the missing `v2-restructure/`). Pre-existing, documented in `DELTA_PICKUP_START_HERE.md`. Unrelated to the delta work.

## The "12 pyright errors" were environment false positives

Run **without** `--pythonpath`, pyright cannot resolve installed packages, so every `import pydantic` / `import opentelemetry` reports `reportMissingImports`. Pointed at the mandated interpreter, **delta_engine.py and the aggregator show 0 errors**. The only residual pyright findings are **pre-existing, non-delta**: `opentelemetry`/`registry` missing-module imports + `reportOptionalMemberAccess` nits in `fault_atlas_router.py` lines 594/928/931/1223 (old code paths, not the Phase-5 delta read at 768–788).

Root cause: `pyproject.toml [tool.pyright]` sets `extraPaths` but no interpreter/`venvPath`, so pyright has no way to find `.sandbox-py`'s packages unless told via `--pythonpath`.

## Conclusion

**DELTA-1 (1A–1D) is done and green on the mandated interpreter.** The 1D `done` flip was correct. `T-COMV2-DELTA-2` is **not** blocked by real breakage — it was blocked by an unrunnable interpreter on a PowerShell host. Resolve the environment (run under Linux/WSL, or sanction a native-Windows 3.14 venv + pyright config) and re-run the two greps; the guard will clear.

## Reproduce (from `labs/comlab`, under a Linux userland)
```bash
PY="$REPO/.sandbox-py/bin/python3.14"
$PY -m pytest tests/ -q
$PY -m pytest tests/unit/test_delta_engine.py -q
$PY -m pyright --pythonpath "$PY" comlab/analytics/delta_engine.py comlab/core/lab_pipeline_aggregator.py
```
