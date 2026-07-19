# T-COMTST-2 progress note

Status: done
Date: 2026-06-21

## Plan / Scope Confirm

Add only `tests/test_cases.py`: load the 24-row T-COMTST-1 CSV, build each
assembled upstream-verdict request through the existing categorical descriptor,
run its production aggregator entry point, require either a schema-valid
`OrchestratorFinalUIOutput` or an expected Pydantic validation failure, and print
the observed verdict fields. Keep `family_hint` descriptive rather than using it
as an accuracy expectation. No production source, fixture, registry, wiki, or
graph change.

## Changed Files

- `tests/test_cases.py` — new parametrized CSV characterization net.
- `tasks/PROGRESS.md` — T-COMTST-2 row closed.
- `tasks/progress_notes/T-COMTST-2.md` — verification and review record.

## Verification Gate

- Native adapted interpreter: Python 3.14.6; pydantic 2.13.4; pytest 9.1.1.
- `ruff check tests/test_cases.py` — clean.
- `pyright --pythonpath .venv-comlab/Scripts/python.exe tests/test_cases.py` —
  0 errors.
- `pytest tests/test_cases.py -q` — 24 passed.
- `pytest tests/test_cases.py -q -s` — 24 passed; observed top fault, family,
  degradation mode, and confidence printed for every schema-valid row.
- Drift guard pins the fixture at 24 rows.
- COM-013 malformed DTC fails closed during Pydantic validation; no arbitrary
  runtime exception is caught.
- `ruff check .` — clean.
- `pyright --pythonpath .venv-comlab/Scripts/python.exe comlab/` — 0 errors.
- `pytest -x -q` — 411 passed, 6 skipped.

## Code Review

- Parametrization IDs use `case_id` plus `family_hint`, one test per CSV row.
- The harness calls the existing descriptor `build_args` and `entry_point`;
  request assembly and production invocation are not duplicated.
- Only `pydantic.ValidationError` is accepted as a clean build failure, and only
  for the fixture's `invalid_input` characterization row. Unexpected exceptions
  still fail the test.
- Successful results must be `OrchestratorFinalUIOutput`; degradation,
  confidence, and fault-family values are checked against their response
  literals, with fault-code and confidence-score types checked explicitly.
- A produced `invalid_input` verdict must use `FATAL_INCOMPLETE`.
- `family_hint` and empty expected columns are not treated as correctness
  assertions. COM-015/016 currently produce schema-valid `FULL_FUSION` outputs
  and are recorded without turning this task into an accuracy gate.
- No new field, enum, fault, consumer, cross-lab import, production change, or
  graph operation was introduced.
