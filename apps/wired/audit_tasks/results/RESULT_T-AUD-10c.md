# Result

## Status
completed

## Summary
`apps/ui/app.py` no longer imports a lab. The VIN Lookup block calls the new `wired.composition.decode_vehicle`, which returns the composition's own `decode_vin(vin)`. Two new tests pin it.

## Files changed
- apps/wired/wired/composition.py (decode_vehicle; import `VinDNA`)
- apps/ui/app.py (import and call decode_vehicle)
- apps/wired/tests/test_t_aud_10c_decode_vehicle.py (new, 3 tests)
- apps/ui/tests/test_t_aud_10c_no_lab_import.py (new, 2 tests)
- progress note and this RESULT

## Commands executed
`apply_fix.py` via `$PY -I`; `cp` + `cmp` of the two tests; the Verification steps 1-4 on the base and after the edit; R4 stash and mutant; one commit.

## Validation evidence
- Base: ui `68 passed`, wired `110 passed`, probe `1 failed`.
- After: ui `70 passed`, wired `113 passed`, new tests `3 passed` / `2 passed`, ruff `All checks passed!`, probe `1 passed, 18 deselected`.
- R4: base `3 failed` / `2 failed`; mutant wired `1 failed, 2 passed`.
- `git diff --stat cd6fbca HEAD` over the two sources: `2 files changed, 12 insertions(+), 4 deletions(-)`.

## Criteria
1. MET: steps 1, 2, 4 and R4 give the stated counts.
2. MET: ruff clean, diff stat 12/4, one new commit 7101cb4 after spec commit 545746c; `git status --porcelain` lists only the note (and this RESULT).

## Decisions the task did not specify
- Commit message has no Co-Authored-By trailer: bash_guard refused the multi-line commit text that held it.

## Pre-existing changes preserved
None existed in repo/ (status was empty at start).

## Rollback
`git -C repo reset` is not allowed here; Cowork reverts commit 7101cb4 on `fix/T-AUD-10c` (`git revert`), or drops the branch.

## Remaining risks or uncertainties
Repo-wide gates (comlab `508 passed, 4 skipped`) were not run; the task leaves them to Cowork.

## Git
fix/T-AUD-10c
7101cb4 fix(T-AUD-10c): the UI decodes the VIN through wired.composition.decode_vehicle (F-C5-12)
(`git log --oneline cd6fbca..HEAD` also lists spec commit 545746c.)
