# Result

## Status
partial

## Summary
R1-R5 are implemented and committed on `fix/T-VINA-3`: VINLab drops a `vref.db` row whose `[my_start, my_end]` does not contain the decoded model year and adds flag `vref_year_out_of_window`. Criterion 2 is NOT MET: `apps/wired` oil case MW-009 regressed (fixtures use WBA4W9C5ZLYYYYYYY, now EURO_1).

## Files changed
decoder.py, test_decoder.py, test_models.py, test_vref_year_window.py (new), WBA4W9C5ZLYYYYYYY.json, VIN_VOCABULARY.md, plus the note and blocker.json.

## Commands executed
The Verification steps 1-6, the M1 mutant run, a decoder.py stash/pop to check the wired base, the blocker validator (OK).

## Validation evidence
- step 1: `229 passed, 8 skipped`; step 2: `3 passed`
- step 3: dnalab `27 passed`; wired `1 failed, 40 passed`; ui `30 passed`
- step 4: `8 passed, 43 deselected`; step 5: `1`; step 6: `All checks passed!`
- red gate: new test before R1 `2 failed, 1 passed`; M1 `4 failed, 225 passed, 8 skipped`
- wired failure: `tests/test_oil_cases.py::test_oil_cases_route_to_expected_faults`, `'MF-001' == 'MW-009'`; with decoder.py stashed, `41 passed`

## Criteria
1. MET: 229 passed 8 skipped, 3 passed, M1 4 failed.
2. NOT MET: dnalab 27 and ui 30 as expected; wired 1 failed, 40 passed (regression from R1, wired is out of write scope).
3. MET: `8 passed`.
4. MET: grep count 1.
5. MET: ruff clean; one commit 869db2a after spec commit d5c8c87; porcelain lists only the note and blocker.json (the RESULT adds itself).

## Decisions the task did not specify
- Kept R1-R5 as written and did not touch `apps/wired`; recorded the regression as a soft blocker (`progress_notes/T-VINA-3.blocker.json`).

## Pre-existing changes preserved
None existed; porcelain was empty at start.

## Rollback
`git -C repo reset` is barred; use `git revert 869db2a` on `fix/T-VINA-3`, or `git restore --source=d5c8c87 -- <paths>`.

## Remaining risks or uncertainties
Cowork must rule on the wired MW-009 fixture or expectation. Other oil fixtures using WBA4W9C5ZLYYYYYYY pass but now run with EURO_1 defaults.

fix/T-VINA-3
869db2a fix(T-VINA-3): vref.db row applied only inside its model-year window (F-C6-4)
d5c8c87 spec(T-VINA-3): vref.db row only inside its model-year window (F-C6-4); T-VINA-10 registered

## Round 2
Status: completed. R6 applied (`apps/wired/tests/fixtures/oil_cases/MW-009.json` vin line only). Verification: vinlab `229 passed, 8 skipped`, `3 passed`, dnalab `27 passed`, wired `41 passed`, ui `30 passed`, probes `8 passed`, grep `1`, ruff clean. Criterion 2: MET (wired 41 passed). Round-1 NOT MET is superseded.
```
fix/T-VINA-3
898f9b1 fix(T-VINA-3): R6 MW-009 oil case to its 5FR VIN
```
