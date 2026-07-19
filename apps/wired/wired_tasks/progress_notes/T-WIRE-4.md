# T-WIRE-4 — progress note

## Plan
Scope: T-WIRE-4 threads only the existing COMLab `enable_fatal_gates` constructor flag through the wired public seam: modify `apps/wired/wired/composition.py` so `diagnose(raw_inputs, *, enable_fatal_gates=False)` passes the flag to `LabPipelineAggregator`, modify `apps/wired/wired/run_case.py` to expose `--fatal-gates`, and create `apps/wired/tests/test_fatal_gate.py` plus `apps/wired/tests/fixtures/oil_cases/INVALID_sample.json`. Verification will run the task's py_compile, ruff, pyright from `apps/wired`, `pytest -x -q apps/wired/tests/test_fatal_gate.py`, and the CLI smoke `python -m wired.run_case --case INVALID_sample --fatal-gates`; no lab edits, graph rebuild, new mapped fields, or diagnostic logic are in scope.

## VERIFICATION GATE

VERIFICATION GATE — T-WIRE-4
1. Compile : PASS  (`/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/wired/composition.py apps/wired/wired/run_case.py apps/wired/tests/test_fatal_gate.py`)
2. Lint    : PASS  (`/agent_workspace/.venv-wired/bin/ruff check apps/wired/wired/composition.py apps/wired/wired/run_case.py apps/wired/tests/test_fatal_gate.py` -> OK)
3. Types   : PASS  (`cd apps/wired && /agent_workspace/.venv-wired/bin/pyright .` -> OK, 0 errors)
4. Tests   : PASS  (`/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired/tests/test_fatal_gate.py` -> 3 passed; affected suite `test_composition.py test_oil_cases.py test_tracing.py test_fatal_gate.py` -> 11 passed; CLI smoke `python -m wired.run_case --case INVALID_sample --fatal-gates` -> `fault_code=ERR-ABORT-001 confidence=0.00 degradation=FATAL_INCOMPLETE`)
5. Contract: PASS  (`diagnose(raw_inputs, *, enable_fatal_gates=False)` default-off; `run_case --fatal-gates` forwards true; grep found no `deferred`/`ARCHIVE`/`v2`/`v6` references in touched Python/test files)
6. Orphan  : N-A  (no new lab->COMLab mapped field or consumer)
Result: CLEAN

## CODE REVIEW

CODE REVIEW — T-WIRE-4
Scope         : PASS  (`composition.py`, `run_case.py`, `test_fatal_gate.py`, `INVALID_sample.json`, this progress note, and ledger only; all lines trace to flag passthrough deliverables)
Composition   : PASS  (only `wired` changed; no lab/COMLab edits; no diagnostic decision logic added; no deferred/legacy path)
Consumers     : PASS  (no new mapped fields; existing flag is consumed by `LabPipelineAggregator.__init__` / Stage-A fatal gates)
Literals      : PASS  (invalid fixture numerics cite `GAS_WIKI §6.1`; no new boundary constants in code)
Docstrings    : PASS  (changed public seams and tests retain docstrings)
Craft (WARN)  : flag threading stays at the composition seam; CLI exposes one boolean; invalid behavior is asserted through public `diagnose()` and `main()` surfaces.
Result: CLEAN
