# Result

## Status
completed

## Summary
`_registry_majority` now skips brands holding U+FFFD. Its test has a second 16-char SUBARU row and three 0x98 0x98 rows, so removing the 17-char filter or the U+FFFD skip each fails it.

## Files changed
- labs/vinlab/tools/build_wmi_map.py (one condition)
- labs/vinlab/tests/unit/test_build_wmi_map.py (R2)
- labs/vinlab/tasks/progress_notes/T-VINA-19.md, labs/vinlab/tasks/results/RESULT_T-VINA-19.md

## Commands executed
First action; Preconditions; red gate on the base tool; Verification steps 1-3; mutants M1 and M2 with cmp restore.

## Validation evidence
- Step 1: 344 passed, 8 skipped. Step 2: 9 passed. Step 3: ruff All checks passed.
- Red gate on base tool: 1 failed. M1: 1 failed. M2: 1 failed. cmp after restore: identical.

## Criteria
1. MET: steps 1-2 give the P2 counts; M1 and M2 each give 1 failed.
2. MET: ruff clean; one commit 52de56f after the spec commit; git status shows only the note and the RESULT (the RESULT was written after that check).

## Decisions the task did not specify
- The commit has no Co-Authored-By trailer: bash_guard refused the command that held it.

## Pre-existing changes preserved
none present (clean start).

## Rollback
`git -C repo revert 52de56f` on fix/T-VINA-19, or discard the branch.

## Remaining risks or uncertainties
none.

Branch: fix/T-VINA-19
Log (8aeed6a..HEAD):
52de56f fix(T-VINA-19): _registry_majority skips U+FFFD brands; test kills the 17-char and U+FFFD mutants
c648dfc vina: T-VINA-19 spec (registry-majority filter hardening from T-VINA-12 review)
