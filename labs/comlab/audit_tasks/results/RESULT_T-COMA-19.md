# Result

## Status
completed

## Summary
`SessionMetadata.resolved_horizon` is stripped and upper-cased, and a value outside the three `Horizon` values raises `ValidationError` (F-C1-15). The R2 pin test is renamed and inverted. The new test file is copied from Cowork's rehearsal.

## Files changed
- labs/comlab/comlab/schemas/ingestion.py
- labs/comlab/tests/unit/test_abort_incomplete.py
- labs/comlab/tests/unit/test_t_coma_19_known_horizon.py (new)
- the progress note and this RESULT

## Commands executed
`### Verification ###` steps 1-5 as written; R4 base and mutant runs; `git apply` of rehearsal.patch; `cp` plus `cmp` of the test.

## Validation evidence
comlab 524 passed, 4 skipped; wired 186 passed; ui 73 passed; step 2 11 passed (base 6 failed, 5 passed); probe 1 passed, 2 skipped with two `schema rejected` lines; v7 corpus changed 0 of 314; ruff All checks passed!; stat 3 files changed, 44 insertions(+), 4 deletions(-). Mutant A 2 failed, 9 passed; mutant B 5 failed, 6 passed.

## Criteria
1. MET: steps 1-4 and R4 counts equal P2, P3 and R4.
2. MET: ruff clean, P2 stat, one new commit c436a8b, status lists only the note and the RESULT.

## Decisions the task did not specify
- The commit message has no trailer line: bash_guard refused the first commit command that carried one.

## Pre-existing changes preserved
none present (clean start).

## Rollback
`git -C repo revert c436a8b` on fix/T-COMA-19. The commit is local.

## Remaining risks or uncertainties
pyright, ruff `--select S` and baseline.sh: NOT RUN (the task does not require them).

Branch: fix/T-COMA-19
```
c436a8b fix(T-COMA-19): reject unknown resolved_horizon, normalise case (F-C1-15)
7635132 coma: spec(T-COMA-19): unknown resolved_horizon rejected, case normalised (F-C1-15)
```
