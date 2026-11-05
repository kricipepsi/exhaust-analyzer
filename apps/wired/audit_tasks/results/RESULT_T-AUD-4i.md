# Result

## Status
completed

## Summary
A wideband-AFR reading is now sent to OBDLab as lambda (`round(AFR / 14.7, 4)`); `WIDEBAND_LAMBDA` is unchanged.

## Files changed
- `apps/ui/ui_payload.py` (constant `WIDEBAND_AFR_STOICH = 14.7`; branch split)
- `apps/ui/tests/test_t_aud_4i_afr.py` (new)
- progress note and this RESULT

## Commands executed
The `### Verification ###` steps 1-4, plus a mutant run (sed the AFR branch to send the raw value, then restore).

## Validation evidence
- Step 1: new file `4 passed`; ui `34 passed`. Mutant: `3 failed, 1 passed`.
- Step 2: wired `62 passed`.
- Step 3 (rehearse.py, VIN WVWZZZ1KZAP012480):
  - AFR 10.0: sent 0.6803, lambda 0.6803, SF-002 delta -0.296894
  - AFR 14.7: sent 1.0, lambda 1.0, EF-004 delta 0.003106
  - AFR 20.0: sent 1.3605, lambda 1.3605, SF-001 delta 0.303106
- Step 4: `All checks passed!`; `git status --porcelain` shows only the note and RESULT after the commit.
- Repo-wide lab suites: NOT RUN (Cowork runs them at review).

## Criteria
1. MET: 4 passed, ui 34 passed, mutant 3 failed.
2. MET: wired 62 passed.
3. MET: `sent` equals `lambda` on all three lines (R3 effect below).
4. MET: ruff clean; commit cd83fe4 on `fix/T-AUD-4i` after the spec commit; status lists note and RESULT only.

R3, base to fixed per AFR: 10.0: SF-001 -> SF-002; 14.7: SF-001 -> EF-004 (the known F-C1-1/F-C2-4 behaviour); 20.0: SF-001 -> SF-001 (unchanged verdict).

## Decisions the task did not specify
- Test file written by hand in the shape of `apply_fix.py`, with the same cases.
- Commit has no Co-Authored-By trailer: `bash_guard` refused the command containing it.

## Pre-existing changes preserved
none in the clone (status was empty at start).

## Rollback
`git revert cd83fe4` on `fix/T-AUD-4i`, or `git restore` before any further commit.

## Remaining risks or uncertainties
Context at end is ABSENT. The EF-004 verdict at lambda 1.0 is out of scope (F-C1-1/F-C2-4).

branch: fix/T-AUD-4i
log (d9aa5c4..HEAD):
cd83fe4 fix(T-AUD-4i): wideband AFR reaches OBDLab as lambda (AFR / 14.7)
