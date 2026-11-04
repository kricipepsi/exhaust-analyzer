# Result

T-VINA-12 (F-R3-2): 11 car WMIs take the registry make; `build_wmi_map.py` picks among vPIC makes by the registry
majority. Plan approved with C1-C6 (`corrections/T-VINA-12_plan_correction_20261104.md`). Note:
`repo/labs/vinlab/tasks/progress_notes/T-VINA-12.md`.

## Status
completed

## Summary
- R1: 10 `wmi.csv` brand cells now hold the registry make in map spelling: `JTM`, `JTE` and `5TD` → `TOYOTA`;
  `KNE` → `KIA`; `ZAC`, `1C4` and `3C4` → `JEEP`; `1C3` → `CHRYSLER`; `3N1` → `NISSAN`; `VF8` → `RENAULT`. There is a
  new row `LSJ,MG,CHINA,modern`.
- R2 (`recheck/T-VINA-12/plan/rekey.py`, files 1+2 only, cp1250):
  - The old-brand map rows that W's own VINs reach are copied under the new brand (59 keys).
  - On 23 keys with a differing new-brand row, a files 1+2 vote decides: the old row wins 17 times (the new-brand row
    is deleted, the old row is re-keyed) and the existing row wins 6 times. A tie keeps the existing row.
  - Old-brand rows are unchanged. The result is 76 rows added, 17 deleted and 6 shares changed. Map: 12,928 → 12,987
    rows.
- R3: new `_pick_vpic_make` and `_registry_majority` (cp1250). The registry majority reaches `_load_vpic_wmis` as a
  parameter through `build(..., registry_make=None)` and a repeatable `--registry-csv` option. Without it the output is
  unchanged.
- R4/C5: 11 new make cases (4 C6 VINs, 7 registry VINs) and 4 P4 engine-floor cases. New `test_build_wmi_map.py`
  (9 tests, in-memory inputs).
- Held-out file 3: W `eng 1126 match 1004` (floors 1125/1001). C and N are equal to the base, line for line.

## Files changed
- `repo/labs/vinlab/vinlab/data/wmi.csv` (11+/10-)
- `repo/labs/vinlab/vinlab/data/vds_engine_map.csv` (82+/23-)
- `repo/labs/vinlab/tools/build_wmi_map.py`
- `repo/labs/vinlab/tests/unit/test_wmi_brands.py`
- `repo/labs/vinlab/tests/unit/test_build_wmi_map.py` (new)
- `repo/labs/vinlab/tasks/progress_notes/T-VINA-12.md` (new, uncommitted)
- `repo/labs/vinlab/tasks/results/RESULT_T-VINA-12.md` (this file, uncommitted)
- Runtime only: `C:/4DApp/recheck/T-VINA-12/plan/` (`rekey.py`, `diag.py`, `c5c6.py`, `data/`, `vinlab/` copy,
  `*.out`, `rekey.json`), `pt/`, `mut/`.

## Commands executed
- First action and Preconditions (match). Base P5 runs (vinlab 320/8, probes 14, dnalab 27, wired 41, ui 30).
- `$PY plan/rekey.py plan/data` (round 1, then round 2 with C1/C3) → `rekey.out`, `rekey2.out`, `rekey.json`.
- `join_check.py plan/data` → `plan/join_plan2.out`. `plan/diag.py` (the 1C4 diagnosis). `plan/c5c6.py` (C5 VINs,
  C6 Path B).
- Suites run on a copy of `labs/vinlab` with the planned data (`PYTHONPATH=plan/vinlab`) to predict the counts.
- Red run of step 2. Then the data copy, the tool edit, Verification steps 1-6, the mutants M1-M7, py_compile,
  ruff, `ruff --select S`, pyright, import sanity and `audit/tools/isolation.py`.

## Validation evidence
| step | expected (plan round 2) | got |
|---|---|---|
| 1 vinlab | `344 passed, 8 skipped` | `344 passed, 8 skipped in 8.36s` |
| 2 R3/R4 tests | `43 passed` | `43 passed in 1.58s` |
| 3 dnalab, wired, ui | 27, 41, 30 passed | `27 passed`, `41 passed`, `30 passed` |
| 4 C6 probes | `14 passed, 37 deselected` | `14 passed, 37 deselected` |
| 5 join | W 1126/1004, C 5071/4388, N 44941/40056 | `TOTAL W n 1667 eng 1126 match 1004 err 105`; `TOTAL C n 9215 eng 5071 match 4388 err 3192`; `TOTAL N n 50439 eng 44941 match 40056 err 3225` (every per-WMI line equals `plan/join_plan2.out`) |
| 6 ruff, log, porcelain | `All checks passed!` | `All checks passed!`; log below; porcelain lists the note and this RESULT |

The previous decisive failure is absent. Red run before the fix: `20 failed, 23 passed`. The probe VINs decoded as
`Subaru`, `Hyundai` and `MATRA`, and `LSJ` raised `VINDecodeError`. After the fix every case passes. Mutants M1-M7
each fail their named test (table in the note). pyright: 0 errors. Isolation: `violations: 4` (known). C6 Path B:
0 W VINs on the base and 0 on the plan data.

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 2 `43 passed`; the 4 probe VINs decode as `TOYOTA`, `TOYOTA`, `KIA`, `RENAULT`. M1-M4, M6 and M7 each fail a named test, and M5 fails `[JTE]` and `[KNE]` (note § Mutants) |
| 2 | MET | step 5: W 1126 ≥ 1125 and 1004 ≥ 1001; C 5071/4388; N 44941/40056. All equal the round-2 prediction |
| 3 | MET | steps 1, 3, 4 equal the predicted counts |
| 4 | MET | step 6: ruff `All checks passed!`; `7ea84b8`, `e34003b` follow the spec commits; porcelain lists only the note and the RESULT |

## Decisions the task did not specify
- The registry has a majority but no vPIC make folds to it: the tool keeps the last make (A3, accepted by Cowork).
- The fold in `_pick_vpic_make` is `vinlab.decoder._fold_brand`, so the pick folds exactly like the decoder's join.
- Unicode replacement: the registry is read with `errors="replace"` (cp1250 leaves 5 bytes undefined). A replaced
  engine code is quarantined.
- C5 VIN choice: the first files 1+2 petrol VIN, in file order, whose `D1-Znamka` is the P1 make and that decodes on
  the plan data.
- The R4 floors are the P4 counts (3, 4, 13, 6). The post-fix counts are higher (4, 5, 13, 8).
- Commit layout: 2 commits instead of the planned 3 (see Remaining risks); one local commit message was amended.
- Scripts in `plan/` were written to the system temp dir and copied in, because `impl_guard` skips `RUNTIME` lines (A1).

## Pre-existing changes preserved
The repo tree was clean at start. `C:/4DApp` `master` files (`LOOP_STATE.md`, `UNATTENDED_RULES.md`, the handoff, the
launcher) were not touched. Cowork's files in `recheck/T-VINA-12/` were only read.

## Rollback
On `fix/T-VINA-12`, `git revert e34003b 7ea84b8` undoes the work. Cowork's spec commits `2e544a3`, `6d23acd` and
`d08fdf6` stay. Nothing was pushed.

## Remaining risks or uncertainties
- `1C4` per WMI loses 2 file-3 matches (16 → 14; Chrysler Voyagers under a WMI the registry gives to Jeep). Cowork
  ruled that the totals bind (A2). The W margin over the floors is small (eng +1, match +3).
- 10 of the 23 vote winners have `majority_share` < 0.70 and now raise `vds_engine_ambiguous`. `JEEP_BU000` is 0.391,
  and `CHRYSLER_BJ51K` is 0.000 (neither code had a files 1+2 vote on that key).
- If the tool is rerun, it writes vPIC's spelling (`Toyota`, `Jeep`) where the data file now holds map spelling
  (`TOYOTA`). The decoder folds both the same way, but the CSV diff would be large. The tool was not run on real data
  (not required).
- `bash_guard` refused one commit message that held flag-like text. The tool commit and the test commit are therefore
  one commit, `e34003b`, and its message was amended locally to cover both. The branch has never been pushed.
- `vds_engine_map.csv` keeps the old-brand rows that W VINs used (for example `SUBARU` keys with Toyota engines). They
  are now reached only by the C WMIs, and C's join is unchanged.

```
$ git -C C:/4DApp/repo branch --show-current
fix/T-VINA-12
$ git -C C:/4DApp/repo log --oneline 8e8d121..HEAD
e34003b fix(T-VINA-12): build_wmi_map picks the vPIC make by registry majority; tests
7ea84b8 fix(T-VINA-12): 11 car WMIs take the registry make; re-key their engine-map rows
d08fdf6 vina: T-VINA-12 plan second review (evidence)
6d23acd vina: T-VINA-12 plan approved with corrections C1-C6
2e544a3 vina: T-VINA-12 spec (F-R3-2: 11 car WMIs take the registry make; held-out engine-join floors)
```

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| round 1: first action, baseline, plan | 2026-11-04T20:08:58Z | 2026-11-04T20:21:06Z | 12.1 | ABSENT |
| round 2: plan round 2, build, verify, mutants | 2026-11-04T20:43:44Z | 2026-11-04T20:51:57Z | 8.2 | ABSENT |
| round 2: note and RESULT | 2026-11-04T20:51:57Z | 2026-11-04T20:53:20Z | 1.4 | ABSENT |

Active total 21.7 min (12.1 + 8.2 + 1.4). Wall clock from first action to finish 44.4 min, which includes the plan
review wait.
