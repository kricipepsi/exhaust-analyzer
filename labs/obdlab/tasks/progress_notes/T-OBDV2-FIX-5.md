# T-OBDV2-FIX-5 — Unify the exception taxonomy

## Plan
We will unify the OBDLab exception taxonomy by introducing a single base class `ObdLabError` inheriting from `Exception` and reparenting `PIDValidationError` and `SemanticConsistencyError` under it. We will drop their inheritance from `ValueError` and `AssertionError`. Additionally, we will update Physics Gate 4 to raise `SemanticConsistencyError` instead of a bare `ValueError` to align with gates 1-3.

Named COMLab/composition catch-sites catching OBDLab exceptions across the JSON/exception boundary:
1. `apps/wired/harness/run_cases.py` (specifically `run_all_cases` at line 238, per-case crash isolation block)
2. `apps/wired/app.py` (specifically the main Streamlit `diagnose` call-site at line 1149)

Both catch sites catch generic `Exception` and will successfully handle the unified `ObdLabError` hierarchy.

## VERIFICATION GATE
- [x] `ruff check obdlab/ && npx pyright obdlab/` clean
- [x] `pytest -x -q` green
- [x] `grep` (Select-String) confirms `AssertionError` and `ValueError` removed from exceptions and semantic gate 4 raising
- [x] All 385 tests run clean

## CODE REVIEW
- [x] Verified that `SemanticConsistencyError` no longer subclasses `AssertionError`.
- [x] Verified that `PIDValidationError` no longer subclasses `ValueError`.
- [x] Confirmed that `_physics_gate_4` raises `SemanticConsistencyError`.
- [x] Verified that unit and integration tests are updated and pass.
