# Result

## Status
completed

## Summary
Removed the Fuel Blend, Mileage and High Idle "Measured λ (analyser)" inputs, which no code reads, plus their payload key and FIELD_HELP entries. Added the 4 rehearsed tests.

## Files changed
apps/ui/app.py, apps/ui/ui_payload.py, apps/ui/tests/test_ui.py (R3), apps/ui/tests/test_t_aud_4n_no_dead_inputs.py (new), the note and this RESULT.

## Commands executed
First action and preconditions; `git apply C:/4DApp/recheck/T-AUD-4n/rehearsal.patch`; the Verification steps 1-4; the P2 mutant run.

## Validation evidence
- Base: new file `4 failed in 2.26s`.
- Step 1: `4 passed in 2.24s`; ui `45 passed in 4.41s`.
- Step 2: wired `85 passed in 5.31s`.
- Step 3: `0`.
- Step 4: `All checks passed!`.
- Mutant (`"lambda_2500"` back in the float tuple): `1 failed, 3 passed`; failing test `test_payload_sends_no_lambda_2500`.

## Criteria
1 MET (step 1 and mutant above). 2 MET (`85 passed`). 3 MET (`0`). 4 MET (ruff clean; one commit on fix/T-AUD-4n after dd6aa13; porcelain lists only the note and this RESULT).

## Decisions the task did not specify
- The commit has no attribution trailer: bash_guard refused the first attempt that carried one.
- The new test file keeps the rehearsal's CRLF endings in the working copy (git warned it normalises to LF).

## Pre-existing changes preserved
none present (clean start).

## Rollback
`git revert 4b9d0e1` on fix/T-AUD-4n, or reset the branch to dd6aa13.

## Remaining risks or uncertainties
None known. Repo-wide gates were not run (report-only; Cowork runs them).

Branch: fix/T-AUD-4n
```
4b9d0e1 fix(T-AUD-4n): drop Fuel Blend, Mileage and High Idle measured lambda inputs no code reads (F-C4-6, F-C5-10 part)
```
(`git log --oneline dd6aa13..HEAD`; spec base dd6aa13, descendant of d10bb93.)
