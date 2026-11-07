# Result

## Status
completed

## Summary
`RobustVINDecoder` no longer applies a VDS engine-map row with `majority_share` below 0.50 (strict). The H1 fuel guard still reads the row; the decode then gets no engine code, displacement or cylinders, the flag `vds_engine_weak` is set, and the grade is PARTIAL. One vocabulary row added; new test plus the revised `test_vref_banks_induction.py`.

## Files changed
`labs/vinlab/vinlab/decoder.py`, `labs/vinlab/docs/VIN_VOCABULARY.md`, `labs/vinlab/tests/unit/test_t_vina_11c_weak_share.py` (new), `labs/vinlab/tests/unit/test_vref_banks_induction.py`; the note and this RESULT (uncommitted).

## Commands executed
First action; preconditions; `$PY -I apply_fix.py`; `cp` and `cmp` of the two tests; R4 stash and mutant runs; Verification steps 1-3; one commit.

## Validation evidence
- Step 1: vinlab `389 passed, 8 skipped`; wired `113 passed`; ui `70 passed`. P1 base: `381 passed, 8 skipped`.
- Step 2: `25 passed`. R4 base `8 failed, 17 passed`; mutant `2 failed, 23 passed`.
- Step 3: ruff `All checks passed!`; `2 files changed, 20 insertions(+), 3 deletions(-)`; `git status --porcelain` shows only the note (and this RESULT).

## Criteria
1. MET: step 1-2 counts above; R4 `8 failed, 17 passed` and `2 failed, 23 passed`.
2. MET: ruff clean, diff stat as pinned, one new commit f005a0d after spec commit 68b86c3, status lists only the note and the RESULT.

## Decisions the task did not specify
- Mutant undone with `cp` of a saved copy, not a hand edit; the diff stat was identical afterwards.
- The commit has no attribution trailer: `bash_guard` refused a command holding the tool-name word, so the commit ran alone with a plain message.

## Pre-existing changes preserved
None present (clean tree at start).

## Rollback
On the branch: `git revert f005a0d`, or `git restore --source=0f5f570` on the four paths.

## Remaining risks or uncertainties
Repo-wide gates (comlab, dnalab) NOT RUN: Cowork runs them. The 0.50 floor rests on Cowork's held-out survey (P3), which I did not re-run.

Branch: `fix/T-VINA-11c`
Log `0f5f570..HEAD`:
```
f005a0d fix(T-VINA-11c): engine-map rows below majority_share 0.50 are not applied (vds_engine_weak, PARTIAL)
68b86c3 vina: spec(T-VINA-11c): engine-map rows below majority_share 0.50 are not applied (held-out code 0.336, displacement 0.497)
```
