# Result

## Status
completed

## Summary
`wired.diagnose` now fills `user_input_echo_audit` (vehicle group plus gas/obd/dtc groups when sent), including on both abort paths. The results pane shows it in a collapsed "Show what I typed →" expander. Done via Cowork's `apply_fix.py` and the two copied tests.

## Files changed
apps/wired/wired/composition.py, apps/ui/ui_payload.py, apps/ui/app.py (modified); apps/wired/tests/test_t_aud_10e_echo_audit.py, apps/ui/tests/test_t_aud_10e_input_echo.py (created); progress note and this RESULT.

## Commands executed
First action; preconditions; `$PY -I C:/4DApp/recheck/T-AUD-10e/apply_fix.py`; cp + cmp of the tests; Verification steps 1-4; R4 stash/base run and mutant run; commit 782f68b.

## Validation evidence
Base: ui 65 passed, wired 106 passed. After: ui 68 passed, wired 110 passed; new tests 4 passed / 3 passed. R4 base: 4 failed / 3 failed. Mutant: 2 failed, 2 passed. ruff: All checks passed! Diff stat: 3 files changed, 65 insertions(+), 2 deletions(-). Probe: `fields never referenced in app.py: ['is_fault_detected']`, `rendered: {'horizon': True, 'gas skipped disclosure': True}`.

## Criteria
1. MET: steps 1-2, R4 and step 4 as above.
2. MET: ruff clean, diff stat, one new commit 782f68b after spec commit; `git status --porcelain` lists only the note (and this RESULT).

## Decisions the task did not specify
- Restored the mutant by reverse `sed`, not `git restore`: the edit was uncommitted, so `git restore` would have discarded it.
- Commit has a second `-m` paragraph for the required attribution trailer.

## Pre-existing changes preserved
none present (clean start).

## Rollback
`git -C repo reset` is barred for main only; on this branch: `git revert 782f68b` or drop the commit before push.

## Remaining risks or uncertainties
Repo-wide comlab gate (508 passed, 4 skipped) NOT RUN; Cowork runs it at review.

branch: fix/T-AUD-10e
log (2fa1af3..HEAD):
782f68b feat(T-AUD-10e): wired echoes the typed inputs; the results pane shows them collapsed (F-C5-7)
a8b4196 spec(T-AUD-10e): wired echoes the typed inputs; the pane shows them collapsed (F-C5-7, PRD 5.5)
