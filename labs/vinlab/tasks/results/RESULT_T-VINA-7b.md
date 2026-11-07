# Result

## Status
completed

## Summary
`RobustVINDecoder.validate_vin_checksum` now returns True first when `vin[0]` is outside the ISO 3780 North American codes 1-5, or the existing `wmi.csv` country bypass applies. Wiki §10.3 rows 1 and 3 updated. A new test file pins it.

## Files changed
- `repo/labs/vinlab/vinlab/decoder.py` (R1)
- `repo/labs/vinlab/wiki/10_decode_scope_rules.md` (R1)
- `repo/labs/vinlab/tests/unit/test_t_vina_7b_checksum_market.py` (R2, new)
- `repo/labs/vinlab/tasks/progress_notes/T-VINA-7b.md` and this RESULT (uncommitted)

## Commands executed
`apply_fix.py` (`-I`, from `C:/4DApp/repo`); `cp` + `cmp` of the test; `git stash push/pop` on `labs/vinlab/vinlab labs/vinlab/wiki`; one `sed` mutant and its `sed` restore; Verification steps 1-3; one commit.

## Validation evidence
- Step 1: vinlab `403 passed, 8 skipped` (base `393 passed, 8 skipped`); wired `113 passed`; ui `70 passed`.
- Step 2: `67 passed, 2 skipped`. Base code: `6 failed, 61 passed, 2 skipped`. Mutant: `1 failed, 66 passed, 2 skipped`.
- Step 3: `All checks passed!`; `2 files changed, 17 insertions(+), 5 deletions(-)`.
- Repo-wide gates (comlab, dnalab): NOT RUN, report-only, Cowork runs them.

## Criteria
1. MET: counts above match P2 and R3.
2. MET: ruff clean, P2 diff stat, one new commit `13d0492` after spec commit `05acf42`, `git status --porcelain` lists only the note and this RESULT.

## Decisions the task did not specify
- The mutant and its restore used `sed -i` on one line instead of an editor. The restored diff stat matches P2.
- The commit carries the session's `Co-Authored-By` trailer.
- The first commit attempt was refused by `bash_guard`; I reran it as one `git -C` command.

## Pre-existing changes preserved
none needed: `git status --porcelain` was empty at the start.

## Rollback
`git revert 13d0492` on `fix/T-VINA-7b`, or `git reset --hard 05acf42` on that branch only.

## Remaining risks or uncertainties
The 128 VINs still rejected (95 Nissan Mexico `3N1`) are out of scope. P3 registry counts were not re-run (Cowork's script, do not run).

Branch: `fix/T-VINA-7b`

`git log --oneline 14f9956..HEAD`:
```
13d0492 fix(T-VINA-7b): a non-NA ISO 3780 region skips the VIN check digit
05acf42 vina: spec(T-VINA-7b): a non-NA ISO 3780 region skips the check digit (registry rejections 10,334 -> 128)
```
