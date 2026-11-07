# Result

## Status
completed

## Summary
Ran Cowork's apply_fix.py (R1-R4) and copied the R5 test. OBDLab docs now state the shipped package. The unknown-strategy raise is an ObdLabError subclass. The payload docstring names the six fields COMLab lacks.

## Files changed
The 12 files in Files to touch plus the new test, in one commit 3c2327f. The note and this RESULT are uncommitted.

## Commands executed
First action; the preconditions; census.sh; the new test (red); apply_fix.py; Verification steps 1-4.

## Validation evidence
Step 1: stale 0, notes 19, highidle 0, ast same labs/obdlab/obdlab/schemas/payload.py. Step 2: 394 passed, 2 skipped (base 2 failed, 392 passed, 2 skipped); All checks passed!. Step 3: corpus 314, differ 0, 106 passed, 503 passed, 4 skipped, 2 errors.

## Criteria
1 MET (step 1). 2 MET (step 2). 3 MET (step 3). 4 MET (commit on fix/T-AUD-17 after 343d490; status lists the note and RESULT only).

## Decisions the task did not specify
The commit has no trailer line: bash_guard refused the commit command with it.

## Pre-existing changes preserved
none (clean start).

## Rollback
git revert 3c2327f on fix/T-AUD-17.

## Remaining risks or uncertainties
Repo-wide gates (ui, registry) NOT RUN; Cowork runs them.

Branch: fix/T-AUD-17
```
3c2327f fix(T-AUD-17): OBDLab docs follow the code; AirMeteringStrategyError (ADR-0005); F-C4-10 payload note
```

## Revision 02
Status: completed. Ran `apply_fix_r02.py` (3 doc edits in `DLD_OBDLab.md` and `OBD_VOCABULARY.md`) and copied the exact-class test over `labs/obdlab/tests/unit/test_ve_strategy_error.py`. Second commit 4f30910.

Validation: step 1 `stale 0`, `notes 20`, `highidle 0`, `ast same labs/obdlab/obdlab/schemas/payload.py`. Step 2 `394 passed, 2 skipped`; `All checks passed!`. Step 3 `corpus 314`, `differ 0`, `106 passed`, `503 passed, 4 skipped, 2 errors`.

Criteria: 1 MET (step 1). 2 MET (step 2). 3 MET (step 3). 4 MET (4f30910 after d3e6b7b on fix/T-AUD-17; status lists the note and RESULT only).

Decisions the task did not specify: the commit has no trailer line (bash_guard refuses the word in a commit command, as at revision 01).

Rollback: `git revert 4f30910` on fix/T-AUD-17. Repo-wide gates (ui, registry): NOT RUN; Cowork runs them.

Branch: fix/T-AUD-17
```
4f30910 fix(T-AUD-17): revision 02 - STRESS_IDLE note, DLD fill defaults below table, exact-class test
d3e6b7b spec(T-AUD-17): revision 02 (second review: STRESS_IDLE note, DLD table, exact-class test, ObdEmissionsView wording)
3c2327f fix(T-AUD-17): OBDLab docs follow the code; AirMeteringStrategyError (ADR-0005); F-C4-10 payload note
```
