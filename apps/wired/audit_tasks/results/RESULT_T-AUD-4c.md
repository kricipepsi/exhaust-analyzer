# Result

## Status
completed

## Summary
Gate 5 of `AnalyticsPreconditions.evaluate` blocks only a stated drive-cycle count below 1. An absent key or `None` now passes. The test `test_gate5_drive_cycles_none_fails` became `test_gate5_drive_cycles_unknown_passes` (None, absent).

## Files changed
- `labs/obdlab/obdlab/core/analytics_preconditions.py`
- `labs/obdlab/tests/unit/test_analytics_preconditions.py`
- `apps/wired/audit_tasks/progress_notes/T-AUD-4c.md`, this RESULT

## Commands executed
Task `### Verification ###` steps 1-4, plus two mutant runs. Each mutant was copied from `C:/4DApp/recheck/T-AUD-4c/mut/` over the source, then the source was restored from `good.py`.

## Validation evidence
- Red before fix: `2 failed, 29 passed`.
- Step 1: `83 passed` (revision 02). Step 2: obdlab `390 passed, 2 skipped`; wired `46 passed`; ui `30 passed`.
- Mutants: A (base default) 2 failed; B (gate removed) 1 failed, `test_gate5_codes_cleared_fails`; C (`drive_cycles < 2`) 1 failed, `test_gate5_codes_not_cleared_pass[1]`.
- Step 3 output:
  - FIX corpus-shape gates {'VALID': 289, 'O2_FAULT_ACTIVE': 3, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2, 'CKP_CMP_FAULT_ACTIVE': 1}
  - FIX ui-shape gates {'VALID': 293, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2}
  - ui-shape verdict changes 0 []
  - BASE lines equal FIX because the script imports the patched code (the spec expects this no-op).
- Step 4: `All checks passed!`.

## Criteria
1. MET: `83 passed` (revision 02 count); mutants A, B and C fail named tests.
2. MET: `390 passed, 2 skipped`; `46 passed`; `30 passed`.
3. MET: P2 lines printed, verdict changes 0.
4. MET: ruff clean; commit on `fix/T-AUD-4c` after the spec commit; `git status --porcelain` listed only the note (and this RESULT) after the commit.

## Decisions the task did not specify
- Parametrised the unknown test with ids `none` and `absent`; the absent case deletes the key.
- Revision 02: `test_gate5_codes_not_cleared_pass` is parametrised over 1 and 5; the production file is unchanged.
- The commit message has no attribution trailer: bash_guard refuses a command whose text names the assistant.

## Step 3 output (revision 02, as printed)
```
cases with OBD 297
corpus keys present: drive_cycles 0 active_dtcs 207
BASE corpus-shape gates {'VALID': 289, 'O2_FAULT_ACTIVE': 3, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2, 'CKP_CMP_FAULT_ACTIVE': 1}
BASE ui-shape gates     {'VALID': 293, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2}
FIX  corpus-shape gates {'VALID': 289, 'O2_FAULT_ACTIVE': 3, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2, 'CKP_CMP_FAULT_ACTIVE': 1}
FIX  ui-shape gates     {'VALID': 293, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2}
ui-shape verdict changes 0 []
```

## Pre-existing changes preserved
none (clean start).

## Rollback
`git revert 1750bc8 87c366e` on `fix/T-AUD-4c`, or reset the branch to `6dc64fc`.

## Remaining risks or uncertainties
Repo-wide report-only gates (comlab, dtclab, gaslab, dnalab) NOT RUN; Cowork runs them. pyright NOT RUN.

Branch: `fix/T-AUD-4c`
Log `6dc64fc..HEAD`:
```
1750bc8 test(T-AUD-4c): pin the gate-5 boundary with a drive-cycle count of 1
52af440 spec(T-AUD-4c): review revision 02 (gate-5 boundary test)
87c366e fix(T-AUD-4c): trim gate 5 reads an unknown drive-cycle count as unknown
```
