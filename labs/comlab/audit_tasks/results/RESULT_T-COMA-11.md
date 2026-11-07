# Result

## Status
completed

## Summary
Added `_reported_fault_score` to `fault_atlas_router.py`; both re-sorts on the v2 path now set the verdict confidence to the named rule's own score. New test added (R2).

## Files changed
- labs/comlab/comlab/core/fault_atlas_router.py
- apps/wired/tests/test_t_coma_11_reported_confidence.py (new)
- progress note and this RESULT

## Commands executed
`apply_fix.py` via `$PY -I`; test copy + `cmp`; `### Verification ###` steps 1-4; R3 stash and mutant; commit e623d16.

## Validation evidence
comlab `510 passed, 4 skipped`; wired `127 passed`; ui `70 passed`; new test `4 passed`; base `4 failed`; mutant `2 failed, 2 passed`; C1 probe `reported: 0.9 own raw score: 0.9`, `1 passed, 6 deselected`; ruff `All checks passed!`; diff stat `1 file changed, 14 insertions(+), 2 deletions(-)`.

## Criteria
1. MET: steps 1-3 counts, R3 base `4 failed`, mutant `2 failed, 2 passed`.
2. MET: ruff clean, diff stat as pinned, one new commit after the spec commit, `git status --porcelain` lists only the note and RESULT (RESULT written after that check).

## Decisions the task did not specify
none

## Pre-existing changes preserved
none present (clean start).

## Rollback
`git revert e623d16` on fix/T-COMA-11, or reset the branch to 9febb21.

## Remaining risks or uncertainties
P2 "17 of 314 confidences change" on the v7 corpus: NOT RUN (not in Verification). The commit message carries no co-author trailer: the bash_guard refused a chained commit text with that word.

## Git
```
fix/T-COMA-11
e623d16 fix(T-COMA-11): verdict confidence is the named fault's own score after the re-sort (F-C1-10)
9febb21 coma: spec(T-COMA-11): verdict confidence is the named fault's own score after the re-sort (F-C1-10)
```
