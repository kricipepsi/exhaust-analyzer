# Result

## Status
completed

## Summary
Removed the dead `fuel_pressure` entry from `_PID_DISPATCH` and RM-004's `fuel_pressure < 3000 kPa` row (R1); added a test that every dispatch field exists in its source schema.

## Files changed
- labs/comlab/registry/integration_shim.py (-1)
- labs/comlab/registry/rules/rich_mixture.json (-8)
- apps/wired/tests/test_t_coma_14_no_dead_pid.py (new, 39)
- progress note and this RESULT

## Commands executed
`### Verification ###` steps 1-5 as written; `rehearse.py`; `cp` + `cmp` of the test; R3 stash and mutant runs.

## Validation evidence
comlab `510 passed, 4 skipped`; wired `170 passed`; ui `70 passed`; new test `3 passed` (base `2 failed, 1 passed`, mutant `1 failed, 2 passed`); grep counts `0`,`0`; v7 corpus `changed 0 of 314`; ruff `All checks passed!`; diff stat `3 files changed, 39 insertions(+), 9 deletions(-)`.

## Criteria
1. MET: steps 1, 2, 4 and R3 as above.
2. MET: ruff clean, diff stat matches, one new commit 55d55d6 after d8f3cfb; `git status --porcelain` listed only the note (and now the RESULT).

## Decisions the task did not specify
none

## Pre-existing changes preserved
none (clean start)

## Rollback
`git revert 55d55d6` on `fix/T-COMA-14`.

## Remaining risks or uncertainties
Audit probe `audit/scratch/C1/test_c1_era_pids_deploy.py::test_fuel_pressure_pid_resolvable` now raises KeyError (expected per R4; not run, not edited). The commit message carries no trailer because `bash_guard` refused a message containing the attribution line.

Branch: fix/T-COMA-14
Log (`e531528..HEAD`):
55d55d6 fix(T-COMA-14): remove the dead fuel_pressure PID and RM-004 row (F-C1-21)
d8f3cfb coma: spec(T-COMA-14): remove the dead fuel_pressure PID and RM-004 row on it (F-C1-21)
