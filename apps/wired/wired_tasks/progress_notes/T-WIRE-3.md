# T-WIRE-3 — progress note

## Plan
Scope: T-WIRE-3 adds env-gated OpenTelemetry observability only: create `apps/wired/wired/tracing.py`, modify `apps/wired/wired/composition.py` only to wrap `diagnose()`, DNA/GAS/OBD/DTC lab calls, and COMLab `process()` in spans, and create `apps/wired/tests/test_tracing.py`. Verification will run the task’s py_compile, ruff on `tracing.py`, pyright from `apps/wired`, and `pytest -x -q apps/wired/tests/test_tracing.py`; the tests must prove verdict equality with `WIRED_OTEL` unset vs set and prove spans emit only when enabled. Rule risk: `opentelemetry-sdk` may be absent, so the enabled-span test must skip with an explicit reason rather than adding a hard dependency; no lab edits, no graph rebuild, no mapping or verdict changes.

## VERIFICATION GATE

VERIFICATION GATE — T-WIRE-3
1. Compile : PASS  (`/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/wired/tracing.py apps/wired/wired/composition.py apps/wired/tests/test_tracing.py`)
2. Lint    : PASS  (`/agent_workspace/.venv-wired/bin/ruff check apps/wired/wired/tracing.py apps/wired/wired/composition.py apps/wired/tests/test_tracing.py` -> OK)
3. Types   : PASS  (`cd apps/wired && /agent_workspace/.venv-wired/bin/pyright .` -> OK, 0 errors)
4. Tests   : PASS  (`/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired/tests/test_tracing.py` -> 2 passed; extra regression `/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired/tests/test_oil_cases.py apps/wired/tests/test_tracing.py` -> 6 passed)
5. Contract: PASS  (`tracing.py` gates on `WIRED_OTEL`; `composition.py` wraps `wired.diagnose`, `lab.dnalab.build`, `lab.gaslab.process`, `lab.obdlab.translate`, `lab.dtclab.sanitize`, and `comlab.process`; grep found no `deferred`/`ARCHIVE`/`v2`/`v6` references in touched Python files)
6. Orphan  : N-A  (no new lab->COMLab mapped field or consumer)
Result: CLEAN

## CODE REVIEW

CODE REVIEW — T-WIRE-3
Scope         : PASS  (`tracing.py`, `composition.py`, `test_tracing.py`, this progress note, and ledger only; all lines trace to env-gated span deliverables)
Composition   : PASS  (no lab/COMLab edits; no second-lab import from a lab; no diagnostic branching; no deferred/legacy path)
Consumers     : PASS  (no new mapped fields; telemetry does not enter COMLab payloads)
Literals      : PASS  (no boundary numerics added; OBD test sample mirrors existing OBDLab warm-idle fixture shape)
Docstrings    : PASS  (`span()`, availability helpers, and new test helpers documented)
Craft (WARN)  : tracing seam is one contextmanager; imports stay dynamic so OTel remains optional and pyright stays clean; tests exercise public `diagnose()` rather than private mappers.
Result: CLEAN
