# Result

## Status
completed

## Summary
An aborted session (`degradation_mode == FATAL_INCOMPLETE`) now shows a red `st.error` banner "Diagnosis stopped (<code>): <remediation>" instead of the severity banner. Added `abort_banner()` in `ui_payload.py`, a branch in `app.py`, and a new test file.

## Files changed
apps/ui/app.py, apps/ui/ui_payload.py, apps/ui/tests/test_t_coma_23_abort_banner.py (commit e8e4b8e); progress note and this RESULT.

## Commands executed
First action; Preconditions; `git apply rehearsal.patch`; `cp` and `cmp` of the test; the Verification steps 1-3; R4 base and mutant runs; one `git commit`.

## Validation evidence
Base P1: comlab 540 passed 4 skipped; wired 186; ui 73. After: comlab 540 passed 4 skipped; wired 186; ui 75; step 2 `2 passed` (base `2 failed`; mutant A `1 failed, 1 passed`); ruff `All checks passed!`; diff stat `3 files changed, 45 insertions(+), 2 deletions(-)`.

## Criteria
1. MET: step 1 and 2 counts and R4 base/mutant counts as named.
2. MET: ruff clean, P2 diff stat, one new commit after the spec commit; `git status --porcelain` lists only the note (and this RESULT).

## Decisions the task did not specify
- The commit message has no `Co-Authored-By` trailer: `bash_guard` refused the commit command while the trailer held the model name. The identity in `-c user.name=Claude` is set as AGENTS.md says.

## Pre-existing changes preserved
none present in `repo/` at start (`git status --porcelain` empty).

## Rollback
`git -C repo reset --hard 2c76bdf` on `fix/T-COMA-23`, or revert e8e4b8e.

## Remaining risks or uncertainties
Mutant A shows the app test fails when the branch is off; the abort payload `severity_level` is unchanged (R2).

Branch: fix/T-COMA-23
```
e8e4b8e fix(T-COMA-23): red error banner for an aborted session (F-D2-7)
2c76bdf coma: spec(T-COMA-23): red error banner for an aborted session (F-D2-7)
```
