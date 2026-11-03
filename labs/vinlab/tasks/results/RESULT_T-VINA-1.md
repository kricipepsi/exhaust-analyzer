# Result

## Status
completed

## Summary
VINLab now reads the model year inside the project scope 1990-2010: `L` is 1990 for every WMI, codes `B`-`K` (2011-2019) are refused, and the docs state 1990-2010. R1-R6 done as the task states; P2 counts reproduced.

## Files changed
`labs/vinlab/vinlab/decoder.py`; `labs/vinlab/tests/unit/test_decoder.py`; `labs/vinlab/tests/unit/test_year_scope.py` (new); fixtures `WBA4W9C5ZLYYYYYYY.json` (2 values) and `1FA6P8CF0HXXXXXXX.json` (deleted); `apps/ui/app.py` (placeholder); vinlab `wiki/{00_index,10_decode_scope_rules,11_engine_resolution}.md`; `docs/{BDD,DLD,HLD,LLD,PRD}_VINLab.md`, `docs/VIN_VOCABULARY.md`. Plus the note and this RESULT.

## Commands executed
`### First action ###`, Preconditions, baseline (vinlab, probes), red-gate run, Verification steps 1-6, mutants M1 and M2 with `cmp`, `git` status/log, one commit.

## Validation evidence
Base: vinlab `203 passed, 8 skipped`; probes `8 failed`.
After: vinlab `215 passed, 8 skipped`; `test_year_scope.py` `16 passed`; dnalab `27 passed`; wired `41 passed`; ui `30 passed`; probes `3 failed, 5 passed`; greps `0`, `0`, `1`; ruff `All checks passed!`. M1 `10 failed`, M2 `2 failed`; `decoder.py` restored, `cmp` identical. Details in the note.

## Criteria
1. MET: steps 1, 2 (`215 passed, 8 skipped`; `16 passed`); M1 fails `test_scope_is_1990_to_2010` and 9 others, M2 fails `test_l_is_1990_for_every_era_hint` x2.
2. MET: step 3 (`27`, `41`, `30 passed`).
3. MET: step 4 `3 failed, 5 passed`; the 3 are WDB1240261A102470, WDD1770441J098476, WBA4W9C5ZLYYYYYYY (Context).
4. MET: step 5 prints `0`, `0`, `1`.
5. MET: ruff clean; one commit `1a32e3c` on `fix/T-VINA-1`; `git status --porcelain` lists only the note and the RESULT.
pyright: NOT RUN (not required by the task).

## Decisions the task did not specify
- Edits made with the Edit tool; it wrote LF to files that had CRLF in the working tree. Index and `.gitattributes` are `eol=lf`, so the commit diff is unaffected.
- Docs wording beyond the R6 rules (for example the `wiki/00_index.md` and `wiki/11` §11.1 and entry lines) follows R6.2 (one statement; `era_hint` rule removed). Headings and `{#…}` anchors kept, including the heading text "the `L` collision".
- `docs/DLD_VINLab.md` line `year: era_hint_unrecognised` and the VIN_VOCABULARY row were deleted, not reworded.
- The BDD scenario outline became one scenario ("The L year is 1990 for every WMI").

## Pre-existing changes preserved
None existed: `git status --porcelain` was empty at start.

## Rollback
`git -C C:/4DApp/repo revert 1a32e3c` on `fix/T-VINA-1`, or reset the branch to `baf9129`.

## Remaining risks or uncertainties
`WBA4W9C5ZLYYYYYYY` decodes with Euro 6 from `vref.db` (F-C6-4, T-VINA-3). Mercedes position-10 VINs stay red (T-VINA-2). Repo-wide lab suites not run (Cowork runs them).

Branch: `fix/T-VINA-1`
Log (`9fe682d..HEAD`):
```
1a32e3c fix(T-VINA-1): read the model year inside the 1990-2010 scope (F-C6-3, F-C6-8)
baf9129 spec(T-VINA-1): open the vina pack (T-AUD-9) and author T-VINA-1 (year scope 1990-2010)
```

## Round 2
Status: completed. R7 done: `test_l_is_1990_whatever_the_row_order` added; `test_year_scope.py` now has 17 cases.
- Validation: vinlab `216 passed, 8 skipped`; `test_year_scope.py` `17 passed`; dnalab `27`, wired `41`, ui `30 passed`; probes `3 failed, 5 passed`; greps `0`, `0`, `1`; ruff clean.
- Mutants: M1 `10 failed`, M2 `2 failed`, M3 (`row = candidates[0]`) `1 failed`, each restored byte-identical.
- Criteria 1-5: MET (criterion 1 now includes M3; criterion 5 lists the note and the RESULT only).
- Decisions the task did not specify: none.
- Files changed: `labs/vinlab/tests/unit/test_year_scope.py` only.
- Rollback: `git revert` the round-2 commit.

Branch: `fix/T-VINA-1`
Log (`9fe682d..HEAD`):
```
4191fba test(T-VINA-1): the in-scope year pick does not depend on row order (R7)
7b7134b spec(T-VINA-1): correction 01 (R7: in-scope pick test; Codex F1 upheld, F2 not)
1a32e3c fix(T-VINA-1): read the model year inside the 1990-2010 scope (F-C6-3, F-C6-8)
baf9129 spec(T-VINA-1): open the vina pack (T-AUD-9) and author T-VINA-1 (year scope 1990-2010)
```
