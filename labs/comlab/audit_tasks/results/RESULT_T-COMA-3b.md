# Result

## Status
completed

## Summary
GASLab judges a `will_not_start` gas sample as a cranking sample (R1-R6). Applied with the rehearsed `apply_fix.py` plus the two rehearsed test files; the diff was read before commit.

## Files changed
The 12 code, test and doc paths in `### Files to touch ###` (commit 42ebcdc), plus the progress note and this RESULT.

## Commands executed
First action; preconditions; red-gate runs of the two new files on base; `apply_fix.py`; the full `### Verification ###` block; one commit.

## Validation evidence
- Step 1: `7 passed`; `215 passed, 2 skipped, 4 deselected`.
- Step 2: `5 passed`; `106 passed`; `5 failed, 504 passed, 4 deselected`; `31 passed`; `503 passed, 4 skipped, 2 errors`; `57 passed`.
- Step 3: `corpus 314`, `differ 5` (REAL-002 NS-001 0.95, REAL-003 NS-002 0.95, case_006 NS-004 1.0, case_007 NS-001 0.85, case_040 NS-005 1.0).
- Step 4: `All checks passed!`.
- Base (before the fix): new files `6 failed, 1 passed` and `3 failed, 2 passed`.

## Criteria
1. MET: step 1 output above.
2. MET: step 2 output above.
3. MET: `differ 5` and the five P2 lines.
4. MET: ruff clean; one commit on `fix/T-COMA-3b` after the spec commit; `git status --porcelain` showed only the note before the RESULT was written.

## Decisions the task did not specify
- The commit has no attribution trailer: bash_guard refused the command while the message held it.
- One commit, so the wiki and the vocabulary land with the code (GAS_VOCABULARY §18.3).

## Pre-existing changes preserved
None in `repo/` (status was empty at start). The 5 registry failures are the known `test_build_corpus.py` ones.

## Rollback
`git revert 42ebcdc` on `fix/T-COMA-3b`.

## Remaining risks or uncertainties
pyright and `ruff --select S` NOT RUN (not in the task's Verification). Repo-wide report-only gates are left to Cowork.

Branch: `fix/T-COMA-3b`
Log `57c6b04..HEAD`:
```
42ebcdc fix(T-COMA-3b): GASLab CRANKING bucket for will_not_start; NS-004/005 outrank NS-001
```
