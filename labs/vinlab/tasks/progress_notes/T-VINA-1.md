# T-VINA-1 progress note

## Readiness
(a) Starting state matches: branch `fix/T-VINA-1`, base (spec commit) `baf9129`, child of `9fe682d`; `git status --porcelain` empty; preconditions print `checked`. Baseline on the base: vinlab `203 passed, 8 skipped`; C6 probes `8 failed` (= P1).
(b) The new test file fails on the base for the intended reason: the year gate still allows 2011-2020 and `L` resolves to 2020 (run recorded below).
(c) Decisive values derived from P4 (`04_horizon_eras.md:54`, scope 1990-2010) and the year table: `L` = 1990, `B`-`K` = 2011-2019 (refused), `A` = 2010, `Y` = 2000, `1` = 2001, `9` = 2009. They match the 16 test cases of `make_rh.py`.
(d) No contradiction found. Every anchor in the task resolves (decoder.py 117, 555, 815, 840; app.py 319).
(e) Teach-back: make the year scope 1990-2010 in the decoder (`L` = 1990, `B`-`K` refused), update tests, fixtures, UI placeholder and docs to match. Decisive check: vinlab `215 passed, 8 skipped`, `test_year_scope.py` `16 passed`, C6 probes `3 failed, 5 passed`, doc greps `0`, `0`, `1`.

## Assumptions worked past
none. Edit tool wrote LF to CRLF working files; `git ls-files --eol` shows index and attr `eol=lf`, so the diff is clean.

## Red gate
`test_year_scope.py` written first. On the base it failed at collection: `ImportError: cannot import name '_YEAR_MAX'`.

## Mutants
Copy of `decoder.py` in `C:/4DApp/recheck/T-VINA-1/mut/decoder.py.orig`; each mutant edited in place, then copied back; `cmp` printed `IDENTICAL`.
- M1 `_YEAR_MAX = 2020`: `10 failed, 6 passed` (`test_scope_is_1990_to_2010` and the 9 `test_codes_after_2010_are_out_of_scope`).
- M2 `row = candidates[-1]`: `2 failed, 14 passed` (both `test_l_is_1990_for_every_era_hint`).

## VERIFICATION GATE
CLEAN. Steps 1-6 of `### Verification ###`:
1. vinlab `215 passed, 8 skipped` (base: `203 passed, 8 skipped`)
2. `test_year_scope.py` `16 passed`
3. dnalab `27 passed`; wired `41 passed`; ui `30 passed`
4. C6 probes `3 failed, 5 passed`; failed: `f3_model_year_plausible[WDB1240261A102470]`, `[WDD1770441J098476]`, `f8_out_of_project_scope_rejected[WBA4W9C5ZLYYYYYYY]` (base: `8 failed`; the 3 are named in Context)
5. greps `0`, `0`, `1`
6. ruff `All checks passed!`; `git log 9fe682d..HEAD`: spec commit `baf9129` and `1a32e3c`; porcelain: only the note (and the RESULT once written)
pyright: NOT RUN (the task's Verification names ruff only).

## CODE REVIEW
CLEAN. Scope: every changed file is in `### Files to touch ###`. Provenance: `_YEAR_MIN, _YEAR_MAX` carries `# source: labs/comlab/wiki/04_horizon_eras.md:54`. Anti-orphan: `_YEAR_MIN`/`_YEAR_MAX` are read in the H2 gate, `_resolve_year` and the new test. `era_hint` stays a `wmi.csv` column and a loaded key (`decoder.py:192`); only the year rule stopped reading it. No cross-lab import added.

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action to commit | 2026-11-03T22:01:26Z | 2026-11-03T22:05:19Z | 3.9 | ABSENT |

## Round 2
R7 applied: appended `test_l_is_1990_whatever_the_row_order` to `test_year_scope.py` (17 cases). First action and Preconditions not re-run, as the correction says.
- Mutant M3 `row = candidates[0]` (copy in `C:/4DApp/recheck/T-VINA-1/mut/decoder.py.r2`): `1 failed, 16 passed`; failed `test_l_is_1990_whatever_the_row_order`. `cmp` after restore: IDENTICAL.
- VERIFICATION GATE: CLEAN. vinlab `216 passed, 8 skipped`; `test_year_scope.py` `17 passed`; dnalab `27`, wired `41`, ui `30 passed`; probes `3 failed, 5 passed`; greps `0`, `0`, `1`; ruff `All checks passed!`.
- CODE REVIEW: CLEAN. Only the test file changed; no production line.
- Commit: `4191fba` on `fix/T-VINA-1`.

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| round 2 (to commit) | 2026-11-03T22:11:19Z | 2026-11-03T22:12:21Z | 1.0 (62 s) | ABSENT |
