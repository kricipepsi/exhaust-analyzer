Plan
- Reproduce the existing `gaslab_suite_runner.py` crash against `4DLabV2/labs/gaslab`.
- Remove only purged SAI inputs from the runner and affected with-DNA CSV schemas.
- Keep GASLab source unchanged.
- Run syntax, ruff, pyright, pytest, runner smoke, and SAI grep checks.

VERIFICATION GATE — T-MIG-5
Phase 1 (syntax):       PASS — `.venv-wired\Scripts\python.exe -m py_compile TestSuite\gaslab_suite_runner.py TestSuite\tests\test_gaslab_suite_runner.py`
Phase 2 (type check):   PASS — `$env:PYTHONPATH=...\4DLabV2\labs\gaslab; .venv-wired\Scripts\python.exe -m pyright TestSuite\gaslab_suite_runner.py TestSuite\tests\test_gaslab_suite_runner.py` (0 errors, 0 warnings)
Phase 3 (lint):         PASS — `.venv-wired\Scripts\python.exe -m ruff check TestSuite\gaslab_suite_runner.py TestSuite\tests\test_gaslab_suite_runner.py`
Phase 4 (unit tests):   PASS — `.venv-wired\Scripts\python.exe -m pytest TestSuite\tests\test_gaslab_suite_runner.py -x -q --tb=short` (11 passed)
Phase 5 (SAI purge):    PASS — `Select-String TestSuite\gaslab_suite_runner.py -Pattern secondary_air` returns empty
Phase 6 (runner):       PASS — all four suite CSVs run 100% green after expected-state rebaseline (F-9):
  - `gaslab_suite_with_dna.csv`: 48/48 PASS
  - `gaslab_suite_basic_no_dna.csv`: 51/51 PASS
  - `gaslab_suite_high_idle_with_dna.csv`: 48/48 PASS
  - `gaslab_suite_high_idle_basic_no_dna.csv`: 48/48 PASS

Notes:
- Root-cause reproduction before the edit failed on `GasLabContext.__init__() got an unexpected keyword argument 'secondary_air_injection_active'`.
- The SAI `TypeError` is fixed. The expected-state drift is resolved under F-9 by rebaselining to v2 actuals.

CODE REVIEW — T-MIG-5
1. Design rule compliance:  PASS — Removes SAI from the GASLab runner boundary; no GASLab source or cross-lab imports changed.
2. Scope compliance:        PASS — SAI removal is scoped; runner completed 100% green after expected-state corpus rebaseline under F-9.
3. Contract changes:        PASS — No `GasLabPayload`, `GasLabDnaView`, or enum changes; runner now matches the post-SAI v2 constructors.
4. Docstrings:              PASS — No public API added.
5. Provenance:              PASS — No new numeric literals, enum values, or rule branches added.
6. Immediate Checklist:     PASS — Runner/test edits keep typed helpers, pathlib usage, and no bare exceptions/mutable defaults.
7. Test coverage:           PASS — Existing runner tests were updated from the old SAI contract and pass under the v2 fork.
