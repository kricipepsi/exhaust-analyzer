# Result

## Status
completed

## Summary
84 rows of `vds_engine_map.csv` (27 TecDoc-diesel keys) changed `PORT_INJECTION` to `DIESEL`, so the existing H1 guard rejects those VINs. New test `test_h1_diesel_map_rows.py` pins the rows and the BMW N47D20C VIN. `decoder.py` is unchanged.

## Files changed
- `labs/vinlab/vinlab/data/vds_engine_map.csv` (84 lines)
- `labs/vinlab/tests/unit/test_h1_diesel_map_rows.py` (new, 41 lines)
- `labs/vinlab/tasks/progress_notes/T-VINA-6.md`, `labs/vinlab/tasks/results/RESULT_T-VINA-6.md` (new, uncommitted)

## Commands executed
`C:/4DApp/.venv/Scripts/python.exe -I C:/4DApp/recheck/T-VINA-6/apply_fix.py` (from `repo`); `### Verification ###` steps 1-4; `git stash push` of the map, step 2, `git stash pop`; `cmp` of the test with the rehearsal copy; one commit.

## Validation evidence
- Step 1: `378 passed, 8 skipped`. Step 2: `2 passed`. Step 3: wired `85 passed`, ui `49 passed`.
- Step 2 with the base map: `2 failed`.
- Step 4: ruff `All checks passed!`; map numstat `84 84`.

## Criteria
1. MET: steps 1-3 give the P2 counts; the new test fails 2 of 2 with the base map.
2. MET: ruff passes; one commit `ee538f8` on `fix/T-VINA-6` after spec commit `302a954`; `git status --porcelain` lists only the note and this RESULT.

## Decisions the task did not specify
- The commit has no attribution trailer: the bash guard refused the first commit command that held one. I used the AGENTS.md commit form.
- I did not run the P1 base counts before the edit. The First action and Preconditions were the baseline; the base map's 0 `DIESEL` rows was confirmed with `grep -c`.

## Pre-existing changes preserved
none (clean tree at start).

## Rollback
Drop `ee538f8` on `fix/T-VINA-6` (Cowork; I may not reset), or `git restore --source=8b4d343` on the two paths.

## Remaining risks or uncertainties
Diesels TecDoc does not key (`K9K A7`, `F9Q G7`, `D4EA-V`) and the electric brands stay unchanged (T-VINA-6b). pyright was not run.

branch: `fix/T-VINA-6`
log (`8b4d343..HEAD`):
- ee538f8 fix(T-VINA-6): 84 TecDoc-diesel engine map rows carry DIESEL so the H1 guard fires
- 302a954 vina: spec(T-VINA-6): H1 fires on the shipped map (84 TecDoc-diesel rows -> DIESEL); register T-VINA-6b

## Revision 02

### Status
completed

### Summary
The test file is now byte-identical to `test_h1_diesel_map_rows_r02.py`: `ROWS_PER_KEY` pins the rows per key, the H1 test takes the real Toyota VIN `JT111GJ9000023441`, and `test_petrol_vin_still_decodes` takes `WBA4W9C5ZLYYYYYYY` and `WVWZZZ1KZAP012480`. No other file changed.

### Commands executed
`cp` and `cmp` of the r02 test; `### Verification ###` steps 1-4; `git checkout 302a954 -- <map>`, step 2, `git checkout HEAD -- <map>`; one commit.

### Validation evidence
- Step 1: vinlab `381 passed, 8 skipped`. Step 2: `5 passed`. Step 3: wired `85 passed`; ui `49 passed`.
- Step 2 with the base map: `3 failed, 2 passed` (the diesel-key test and both H1 VINs fail; the petrol controls pass).
- Step 4: ruff `All checks passed!`; numstat of the map `84 84`; the test `88 0` against `8b4d343`.

### Criteria
1. MET: steps 1-3 give the P2 counts; base map gives `3 failed, 2 passed`.
2. MET: ruff passes; one new commit `9e51f6d` after the revision 02 spec commit `3ee93cd`; `git status --porcelain` lists only the note and this RESULT.

### Decisions the task did not specify
- The commit has no attribution trailer: the bash guard refused the commit command that held one.

### Rollback
`git restore --source=3ee93cd labs/vinlab/tests/unit/test_h1_diesel_map_rows.py` or drop `9e51f6d` (Cowork).

### Remaining risks or uncertainties
Unchanged from the first run. pyright and `ruff --select S` NOT RUN.

branch: `fix/T-VINA-6`
log (`8b4d343..HEAD`):
```
9e51f6d test(T-VINA-6): pin rows per key, real Toyota VIN, two petrol controls (revision 02)
3ee93cd vina: spec(T-VINA-6) revision 02: test pins per-key rows, real Toyota VIN, petrol controls (second review)
ee538f8 fix(T-VINA-6): 84 TecDoc-diesel engine map rows carry DIESEL so the H1 guard fires
302a954 vina: spec(T-VINA-6): H1 fires on the shipped map (84 TecDoc-diesel rows -> DIESEL); register T-VINA-6b
```
