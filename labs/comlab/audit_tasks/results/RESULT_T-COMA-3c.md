# Result

## Status
completed

## Summary
REAL-002 in `apps/wired/v7/data/cases_petrol_v7.csv` is now `non_starter` / `ERR-NS-003` with oracle ref `06_fault_atlas_families.md#CONCEPT_FAMILIES`. `viability_note` keeps the old text and adds the lean_condition ERR-LC-003 repair finding.

## Files changed
- `apps/wired/v7/data/cases_petrol_v7.csv` (REAL-002 row, commit 2a3b0d6)
- `labs/comlab/audit_tasks/progress_notes/T-COMA-3c.md`, this RESULT

## Commands executed
`apply_fix.py`; the `### Verification ###` steps 1-5 as written; a pytest rerun filtered to `^FAILED`.

## Validation evidence
- step 1: `non_starter ERR-NS-003 06_fault_atlas_families.md#CONCEPT_FAMILIES lean_condition Lean_No_Start_Fuel_Pump`; numstat `1	1	apps/wired/v7/data/cases_petrol_v7.csv`
- step 2: `REAL-002 {'fault_family': 'PASS', 'fault_code': 'FAIL', 'state': 'PASS', 'confidence': 'PASS', 'perception_gap': 'FAIL', 'demotion_note_contains': 'NA'}`; before the edit `fault_family` was `FAIL`
- step 3: `corpus 314`, `differ 0`
- step 4: `2 failed, 47 passed` (the two P5 tests); registry `31 passed`
- step 5: only the note and RESULT untracked
- NOT RUN by me: the P5 "before" suite counts on the base (the task states them).

## Criteria
1. MET (step 1)
2. MET (steps 2, 3, 4)
3. MET (step 5; commit 2a3b0d6 after spec commit 4ab4bbf)

## Decisions the task did not specify
- The commit has no attribution trailer: bash_guard refused the command that held one.

## Pre-existing changes preserved
Working tree was clean at start.

## Rollback
`git revert 2a3b0d6` on `fix/T-COMA-3c`.

## Remaining risks or uncertainties
`fault_code` stays `FAIL` by R3 (NS-00x vs ERR-NS-00x). Out-of-scope curated registry files keep the v5 label.

Branch: `fix/T-COMA-3c`
```
2a3b0d6 data(T-COMA-3c): REAL-002 labelled non_starter ERR-NS-003, repair finding kept in viability_note
```
