# T-WIRE-2 — progress note

## Plan
Scope: T-WIRE-2 builds only the single-case oil runner surface: create `apps/wired/wired/run_case.py`, create oil-case JSON fixtures under `apps/wired/tests/fixtures/oil_cases/`, and create `apps/wired/tests/test_oil_cases.py`. The runner will load one fixture, call existing `wired.diagnose()`, and print `diagnostic_verdict.fault_code` plus confidence; tests will assert MW-002/MW-003/MW-009 route and MW-001/MW-008 follow `RINGS_PCV_TRIAGE_RULING.md` documented known-blocked expectations. Verification will run the task’s py_compile, ruff, pyright, CLI smoke for MW-002, and pytest command from `/agent_workspace`. No rule risk identified: no lab/COMLab edits, no graph rebuild, no new mapped fields/consumers.

## VERIFICATION GATE

VERIFICATION GATE — T-WIRE-2
1. Compile : PASS  (`/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/wired/run_case.py apps/wired/tests/test_oil_cases.py`)
2. Lint    : PASS  (`/agent_workspace/.venv-wired/bin/ruff check apps/wired/wired/run_case.py apps/wired/tests/test_oil_cases.py` -> OK)
3. Types   : PASS  (`cd apps/wired && /agent_workspace/.venv-wired/bin/pyright .` -> OK, 0 errors)
4. Tests   : PASS  (`/agent_workspace/.venv-wired/bin/python -m wired.run_case --case MW-002` -> `fault_code=MW-002 confidence=0.95`; `/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired/tests/test_oil_cases.py` -> 4 passed)
5. Contract: PASS  (`run_case.py` exposes `main()` and `load_case()`; five MW fixtures load; routed cases MW-002/MW-003/MW-009 return their expected verdicts; known-blocked MW-001/MW-008 assert current non-routes; grep found no `deferred`/`ARCHIVE`/`v2`/`v6` references in new Python files)
6. Orphan  : N-A  (no new lab->COMLab mapped field or consumer)
Result: CLEAN

## CODE REVIEW

CODE REVIEW — T-WIRE-2
Scope         : PASS  (changed files are the three deliverables plus this progress note and the ledger update)
Composition   : PASS  (runner calls existing `diagnose()` only; no lab/COMLab edits; no second-lab import from a lab; no deferred path)
Consumers     : PASS  (no new mapped fields; existing `diagnose()` output consumed at `diagnostic_verdict.fault_code`/`confidence_score`)
Literals      : PASS  (fixture numerics are sourced in `_provenance` from `OilburnCases.md`, `OIL_CASE_SIGNATURES_5FR.md`, archived T-WV2-2 routed baselines, and `RINGS_PCV_TRIAGE_RULING.md`; no boundary constants added to code)
Docstrings    : PASS  (`run_case.py` module and public helpers have docstrings)
Craft (WARN)  : runner is a thin CLI seam; fixtures are data only; no diagnostic branching added outside assertions for the documented T-PREP-WIRE-1 known-blocked cases; CLI is exercised through `main()`.
Result: CLEAN
