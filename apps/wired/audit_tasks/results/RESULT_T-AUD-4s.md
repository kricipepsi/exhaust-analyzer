# Result

## Status
completed

## Summary
The 31 numeric raw OBD channels in `_run_obdlab` now go through `_raw_obd_value`, with one range table `_OBD_RAW_RANGES` equal to the UI form's. `diagnose` aborts with `OBD_INPUT_OUT_OF_RANGE` before any lab runs.

## Files changed
- apps/wired/wired/composition.py (R1-R3)
- apps/wired/tests/test_t_aud_4s_raw_obd_checked.py (new, 12 tests)
- apps/ui/tests/test_t_aud_4s_raw_obd_ranges.py (new, 3 tests)
- progress note and this RESULT

## Commands executed
The task's `### Verification ###` steps 1-4; `apply_fix.py`; red-gate runs on base; M1 mutant run.

## Validation evidence
Base: `9 failed, 3 passed`; `3 failed`. Fix: `12 passed`; `3 passed`; wired `101 passed`; ui `52 passed`; comlab `525 passed, 4 skipped, 2 errors`; `corpus 314`, `differ 0`; f7 `3 passed, 9 deselected`; ruff `All checks passed!`.
M1: `2 failed, 10 passed` (`test_diagnose_aborts_out_of_range`, `test_diagnose_aborts_instead_of_crashing`).

## Criteria
1 MET (step 1 output above, M1 names above). 2 MET (comlab line). 3 MET (differ 0; 3 passed). 4 MET (ruff clean; one commit on fix/T-AUD-4s after spec; status below).

## Decisions the task did not specify
- Commit has no Co-Authored-By trailer: bash_guard refused the command text holding it.
- Wrote the note after the red gate and apply_fix run, not before.

## Pre-existing changes preserved
Working tree was clean at start.

## Rollback
`git revert 73f5ee9` on fix/T-AUD-4s, or reset the branch to a9507a7.

## Remaining risks or uncertainties
pyright not run (not in Verification). v1 router `o2_downstream` contract is T-AUD-4t.

## Branch
fix/T-AUD-4s
73f5ee9 fix(T-AUD-4s): range-check the 31 raw OBD channels with the UI form's ranges (F-C4-8)
