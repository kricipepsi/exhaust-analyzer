# Result

## Status
completed

## Summary
Added `_TYPE_CODE_WMIS` and a rule in `_resolve_year`: a Mercedes-Benz or smart VIN with digits at positions 4-9 returns `model_year = None`. The North American form keeps the year. Updated the one test that asserted the bug, added 8 new cases and the wiki §10.6 paragraph.

## Files changed
`labs/vinlab/vinlab/decoder.py`, `labs/vinlab/tests/unit/test_decoder.py`, `labs/vinlab/tests/unit/test_type_code_year.py` (new), `labs/vinlab/wiki/10_decode_scope_rules.md`, plus the note and this RESULT.

## Commands executed
Task `### Verification ###` steps 1-6 unchanged; P1 baseline run before edits; new test run red before R1/R2; mutants M1 and M2 with `cmp` restore.

## Validation evidence
- vinlab suite: `224 passed, 8 skipped`. New file: `8 passed`.
- dnalab `27 passed`; wired `41 passed`; ui `30 passed`.
- Probes `-k "f3_model or f8_"`: `1 failed, 7 passed` (WBA4W9C5ZLYYYYYYY only; T-VINA-3). Before: `3 failed, 5 passed`.
- Doc grep `3`. ruff: `All checks passed!`.
- M1: `test_north_american_form_keeps_the_year` 3 failed. M2: `test_type_code_vin_has_no_year` 3 failed.

## Criteria
1. MET: steps 1, 2 and the mutants.
2. MET: step 3.
3. MET: step 4, `1 failed, 7 passed`.
4. MET: step 5, `3`.
5. MET: ruff clean; one commit `069e188` after the spec commit; `git status --porcelain` lists only the note (RESULT is written after that check and is the other expected entry).

## Decisions the task did not specify
none

## Pre-existing changes preserved
None existed; `git status --porcelain` was empty at the start.

## Rollback
`git -C C:/4DApp/repo revert 069e188` on `fix/T-VINA-2`, or `git reset` is not needed; the commit is local and unpushed.

## Remaining risks or uncertainties
Renault `VF1` is not covered (T-VINA-9). `WDB` still decodes as "Maybach" (T-VINA-5). pyright was not named by the task: NOT RUN.

Branch: `fix/T-VINA-2`
Log `02ebfba..HEAD`:
069e188 fix(T-VINA-2): Mercedes/smart numeric type code at 4-9 carries no year at position 10
0f8dc05 spec(T-VINA-2): Mercedes/smart type-code VINs carry no year at position 10 (F-C6-3 rest); T-VINA-9 registered

## Round 2
Applied correction 01 (R6): wording change in 3 places, new test `test_numeric_positions_outside_the_set_keep_the_year`, mutant M3 fails it. Re-ran Verification: vinlab `225 passed, 8 skipped`, new file `9 passed`, dnalab `27 passed`, wired `41 passed`, ui `30 passed`, probes `1 failed, 7 passed` (T-VINA-3's), doc grep `3`, ruff clean. Criteria 1-5: MET with those figures. Decisions the task did not specify: none.

Branch: `fix/T-VINA-2`
Log `02ebfba..HEAD`:
cbd1812 fix(T-VINA-2): R6 correction 01 - no unsourced position-10 meaning; WMI-condition test
2257cc9 spec(T-VINA-2): correction 01 (R6: no unsourced position-10 meaning; WMI-condition test)
069e188 fix(T-VINA-2): Mercedes/smart numeric type code at 4-9 carries no year at position 10
0f8dc05 spec(T-VINA-2): Mercedes/smart type-code VINs carry no year at position 10 (F-C6-3 rest); T-VINA-9 registered
