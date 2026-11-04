# Result

T-VINA-13b: merge the TecDoc 1Q2019 extract into vref.db. Plan approved with correction 01 (C1-C6). Base `11dfa95`.

## Status
completed

## Summary
New tool `labs/vinlab/tools/merge_tecdoc_extract.py` inserts **1,162** `engine_ref` rows (72 → 1,234) for extract
codes vref.db lacked. The 72 existing rows keep every value (row dump equal). The table is rebuilt once with the
builder DDL, so `has_maf`/`has_map` accept NULL; every new row writes NULL there and `o2_type ''`. Real VINs that
reach a row: `row_applied` **15 → 506**, exactly as the plan predicted. Every real-VIN change in euro, O₂, air
metering, induction, banks and cylinder count traces to a TecDoc-stated field (0 unattributed). A second run inserts
0 rows and leaves vref.db byte-identical. 20 new tests (18, plus 2 from review correction 02), 19 of 19 mutants
killed.

**Revision 02 (review correction 02), test file only, commit `2dfbbba`:**
`test_cylinder_heuristic_two_bank_hint_alone_is_skipped` isolates G2 (iii) (I4 map, unresolved no-row hint, V6 hint at
TecDoc 3.0 L, TecDoc 6 cylinders, NA, not V) and kills mutant M19, which restores the "map configuration is blank"
qualifier (`1 failed`; the other 19 tests pass under M19). `test_shipped_original_rows_match_the_pinned_base_digest`
checks the 72 original rows of the shipped vref.db (32 explicit columns, values typed) against the sha256
`89403096d8074357d62e94187c58c71664c73ab4bc47c5ca4d00dbf654625275`, pinned from
`git show 11dfa95:labs/vinlab/vinlab/data/vref.db`. A one-cell change in a throwaway copy moves the digest to
`398fc766…`. The tool, the builder and vref.db did not change (`git diff --stat 5bf69e5 HEAD -- labs/vinlab/tools
labs/vinlab/vinlab/data` is empty).

Skips (normalised codes, of 1,306): in vref 24; collision 44; status 0; no `my_start` 35; span gap (C3) 0; G1 map
banks 2 (EJ18, FB20); G2 cylinder heuristic 39.

**Collision codes (R2)**, not inserted: `169A4000 18K4F 18K4K 1E 1KR 1UZFE 2GRFE 4A 6FY A112A2000 A20NHT ADY APQ B12S1
B38A15A B48A20A B6 BDY BKY CDZ D16A8 F18A3 FA20 FE FS G4FG HFX JB K10B KDX KDY KFV KFW KFX KL LFW PT204 RFJ RFK RFN RFU
RFW RGX VK45DE`. Real VINs on them: **72** by the decoder's code-only lookup, of which **70** brand-agreeing (= P4).

**CoC (C6).** CoC columns stay NULL. The petrol CSV exists at
`D:/4DLab/4DLabV2/DBS/docs/vehicles_petrol_specimens.csv` (the plan wrongly called it absent; round 1 searched only
`C:`). Cowork ran `build_vref_db._enrich_from_csv` with `DBS_ROOT=D:/4DLab/4DLabV2/DBS` over the extract codes and
**0** gained a CoC value (correction 01). A NULL CoC adds `coc_null_target_lambda_v112` (`decoder.py:399-408`), and
the row removes `engine_not_in_vref`, so confidence stays PARTIAL (measured: no confidence change).

## Files changed
- `labs/vinlab/tools/merge_tecdoc_extract.py` (new)
- `labs/vinlab/vinlab/data/vref.db` (1,162 rows; table rebuilt with the builder DDL)
- `labs/vinlab/tools/build_vref_db.py` (`CREATE_ENGINE_REF` has_maf/has_map `INTEGER` + comment; migration guard C1)
- `labs/vinlab/tests/unit/test_vref_tecdoc_merge.py` (new in `5bf69e5`, 18 tests; `2dfbbba` adds 2, total 20)
- `labs/vinlab/tasks/progress_notes/T-VINA-13b.md` (note; untracked), this RESULT (untracked)
- `labs/vinlab/tasks/progress_notes/T-VINA-13b.blocker.json` (round-1 hand-back record, header-authorised; untracked)
- No dnalab, wired or ui fixture changed.

## Commands executed
From `C:/4DApp/repo` unless stated; `$PY` = `C:/4DApp/.venv/Scripts/python.exe`; `PYTHONDONTWRITEBYTECODE=1`.
- First action and Preconditions (both rounds); `reach.py` on the base (round 1).
- Red run: `cd labs/vinlab && $PY -m pytest -q -p no:cacheprovider tests/unit/test_vref_tecdoc_merge.py
  --basetemp=C:/4DApp/recheck/T-VINA-13b/pt/red` → `18 errors` (FileNotFoundError, tool missing).
- Inner loop on the tool and test: `py_compile`, `py -m ruff check`, `py -m ruff check --select S`, `py -m pyright
  --pythonpath C:/4DApp/.venv/Scripts/python.exe`.
- `git show 11dfa95:labs/vinlab/vinlab/data/vref.db > C:/4DApp/recheck/T-VINA-13b/pt/vref_base.db`; the merge
  `cd labs/vinlab && $PY tools/merge_tecdoc_extract.py`; the row-dump comparison (`$PY -c`, typeof and value per
  column).
- Verification steps 1-5 exactly as written in the task; C6 probes `$PY -m pytest -q -p no:cacheprovider
  audit/scratch/C6` before and after (report-only).
- `git add` of the four paths; `git -C C:/4DApp/repo -c user.name=Claude -c user.email=noreply@anthropic.com commit …`.
- Mutant runner (stdin) M1-M18, then `git restore tools/merge_tecdoc_extract.py vinlab/data/vref.db`.
- Gate items: import sanity, `audit/tools/isolation.py`, builder ruff/pyright against the base copy.
- Revision 02: `git show 11dfa95:labs/vinlab/vinlab/data/vref.db > C:/4DApp/recheck/T-VINA-13b/pt/vref_11dfa95.db`
  and the canonical digest (`$PY -c`); inner loop on the test file; mutant M19 (stdin runner, copy
  `mut/M19.py`, then `git restore`); the digest on a mutated throwaway copy `pt/vref_mutated.db`; steps 1, 2 and 5;
  `git add` of the test file and `git -C C:/4DApp/repo … commit` (`2dfbbba`).

## Validation evidence
`reach.py` (cwd `audit/scratch/C6`), before (base, measured 2026-11-04T14:05Z):
```
vref outcome: {'no_engine_code': 16, 'not_in_vref': 1097, 'out_of_window': 3, 'row_applied': 15}
confidence: {'HIGH': 2, 'NONE': 16, 'PARTIAL': 1113}
euro: {'EURO_1': 1118, 'EURO_2': 4, 'EURO_3': 4, 'EURO_4': 4, 'EURO_5': 1}
upstream_o2: {'NARROWBAND': 702, 'WIDEBAND_AFR': 429}
air_metering: MAF_ONLY(maf=True, map=False) 1117; MAP_ONLY(maf=False, map=False) 13; MAP_ONLY(maf=False, map=True) 1
```
After (step 4):
```
vref outcome: {'no_engine_code': 16, 'not_in_vref': 550, 'out_of_window': 59, 'row_applied': 506}
confidence: {'HIGH': 2, 'NONE': 16, 'PARTIAL': 1113}
euro: {'EURO_1': 1107, 'EURO_2': 4, 'EURO_3': 4, 'EURO_4': 15, 'EURO_5': 1}
upstream_o2: {'NARROWBAND': 702, 'WIDEBAND_AFR': 429}
air_metering: MAF_ONLY(maf=True, map=False) 1085; HYBRID_MAF_MAP(maf=True, map=True) 32; MAP_ONLY(maf=False, map=False) 13; MAP_ONLY(maf=False, map=True) 1
```
(air-metering keys abbreviated from the printed `AirMeteringArchitecture(...)` reprs; counts verbatim.)

Real-VIN field changes, decoded against the base copy and the merged file (0 unattributed):
`engine_displacement_liters` 485 (TecDoc `displacement_cc`), `induction_type` 28, `fuel_delivery_type` 14 (GDI),
air metering 32, `euro_emission_category` 11 (with `resolved_horizon` 11, `stress_idle_rpm_target` 11),
`number_of_banks` 18 (stated `is_v_engine`: 10 V engines 1 → 2; 8 straight engines 2 → 1 where the map says V6/V8:
AEB, NG, 346KB, 326S4, 366S1), `cylinder_count` 12 (0 → the extract's own count); O₂ 0; confidence 0.

**C2 list: air-metering changes (MAF_ONLY → HYBRID_MAF_MAP), each from a TecDoc-stated field through the unchanged
decoder heuristic (`decoder.py:490-501`, `has_map` NULL):**
`JTHBH1BL90A004863` 2AR-FSE fuel GDI; `JTHBK262502019539` 4GR-FSE fuel GDI; `SALLJGMY8MA126816` 20T4H induction
TURBOCHARGED; `SB1BJ56L80E028365` 1AZ-FSE fuel GDI; `TRUZZZ8J171037678` BWA TURBOCHARGED; `VF30U5FV8AS343942` 5FV
TURBOCHARGED; `VF34B5FTF9S216456` 5FT TURBOCHARGED; `VF34B5FXH9S073995` 5FX TURBOCHARGED; `VF34B5FXH9S076434` 5FX
TURBOCHARGED; `VF7Y3AX0000AX5507` RGY TURBOCHARGED; `W0L0EAR971N001258` Z20LET TURBOCHARGED; `WAUZZZ4BZYN125879` AEB
TURBOCHARGED; `WBAHL010X0DD66162` N73B60A* fuel GDI; `WMWMF71010TS21805` N14B16A* TURBOCHARGED; `WMWMF710X0TS13783`
N14B16A* TURBOCHARGED; `WMWMF73578TT89257` N14 TURBOCHARGED; `WMWMS3C54ATY51445` N14B16A* TURBOCHARGED;
`WMWRE31090TD38276` W11B16A* SUPERCHARGED; `WMWZP91000T551403` N14B16C* TURBOCHARGED; `WVWZZZ3BZ1E079146` AEB
TURBOCHARGED; `WVWZZZ50ZLK026205` PG SUPERCHARGED; `XLBLC193ERC469302` B18FT TURBOCHARGED; `YS3ED45C623005234` B205E
TURBOCHARGED; `YS3EF45C5X3035441` B205E TURBOCHARGED; `YV1945211T1187712` B200FT TURBOCHARGED; `YV1LS5702T2304662`
B5234FT TURBOCHARGED; `YV1MK685172001750` B5254T(3) TURBOCHARGED; `YV1RS49K212068541` B5204T5 TURBOCHARGED;
`YV1RS58K222150085` B5244T3 TURBOCHARGED; `YV1SZ58K711035255` B5244T3 TURBOCHARGED; `YV1VW1626WF170400` B4204S
TURBOCHARGED; `ZFA3340000P319674` 55263624 TURBOCHARGED. (32)

**Euro changes (EURO_1 → EURO_4), each from TecDoc `euro_norm` `euro4`:** `JMBSNCS3A4U007060` 4G18;
`JTDJG18C40N041061`, `JTDKG18C10N117985`, `JTDKG18C60N028123` 1KR-FE; `KMHDM51BP1U003929`, `KMHDN41BP5U108513` G4ED;
`KMHDN41DP4U854885`, `KMHHN61DP4U112297` G4GC; `VF34B5FXH9S073995`, `VF34B5FXH9S076434` 5FX; `XMCXNZ32A5F016006` 3A91.
(11)

Other evidence: the 72-row dump sha256 `bb2864eae071a9bb` before and after (`equal True`); vref.db sha
`814f0b7282b84086` after the merge, unchanged by the test runs, the mutant restore and the second merge run; C6
probes `16 failed, 35 passed` before and after, same names.

## Criteria
| # | criterion | status | evidence |
|---|---|---|---|
| 1 | vinlab suite and new file pass with the plan's counts; each R5 mutant fails a named test | MET | after revision 02: step 1 `281 passed, 8 skipped`, step 2 `20 passed` (before it: 279 / 18, the plan's counts); mutants 19 of 19 KILLED (M1-M18 note § Build; M19 note § Revision 02) |
| 2 | dnalab, wired, ui pass with the plan's counts; each changed value named | MET | `27 passed`, `41 passed`, `30 passed` (= P5); no downstream test value changed (plan § Existing tests) |
| 3 | `reach.py` prints the predicted `row_applied`; no unattributed euro, O₂ or air change | MET | step 4 `row_applied` 506 (predicted 506); attribution script `UNEXPLAINED []`; lists above |
| 4 | ruff passes; second run changes nothing; commits after the spec commit; porcelain only note and RESULT | MET | step 5 (rerun after `2dfbbba`): `All checks passed!`; `inserted 0 rows … schema rebuilt: no`, no vref.db status line; `5bf69e5` after `11dfa95`, `2dfbbba` after `fe64c8c`; porcelain lists the note, the RESULT and the header-authorised `T-VINA-13b.blocker.json` |

## Decisions the task did not specify
- G2 (iii) also fires on a blank `is_v_engine`, not only `0`: the tool writes blank as `0`, so the decoder reads both
  alike (`decoder.py:364`). Count change 0 (measured both ways).
- C3 "gap of more than one year" is measured as missing calendar years between the furthest span end so far and the
  next span start (open end 2019); a 1-year gap is allowed because the `end + 1` model-year window covers it. Count 0.
- Map cylinder counts that are not integers count as unknown, as in `decoder.py:270-274` (G2 runs for them).
- The `db` test fixture rebuilds the pre-T-VINA-13b table from the shipped file (the 72 rows with `o2_type != ''`, the
  pre-merge DDL), so the tests describe the merge from its real starting state after the shipped db is merged.
- The decode test compares the merged copy with a copy of that pre-merge db, not with the session decoder (which now
  reads the merged shipped file).
- Multi-brand codes take the alphabetically first brand and its spelling (as planned).

## Pre-existing changes preserved
Starting porcelain held only the round-1 note and blocker record (both mine, untracked); both kept. No other
modification or untracked file existed. `LOOP_STATE.md` and the ledger were not touched.

## Rollback
`git -C C:/4DApp/repo revert 5bf69e5` on `fix/T-VINA-13b` (or drop the commit before push). The base vref.db is
`git show 11dfa95:labs/vinlab/vinlab/data/vref.db`.

## Remaining risks or uncertainties
- `audit/scratch/C6/test_c6_probes.py::test_f1_horizon_follows_year_when_euro_unknown` counts any vref row as "euro
  known" (`:52`); 1,086 of the new rows carry NULL euro, so that probe's population fell from 1,113 to 566 while most
  of those euros are still unknown. It stays red; its count now understates F-C6-1.
- 247 year-less P4 VINs get the row with no window check (`decoder.py:584`).
- G2 mirrors `decoder.py:446-478`; a decoder change can make it stale. T-VINA-14 (banks from BOXER, keep a stated
  induction) should be followed by a rerun that inserts the 41 guarded codes.
- `era_bucket`: 67 new rows end before 1990 and get `ERA_MODERN` from `_derive_era`'s fall-through; no decoder line
  reads vref `era_bucket`.
- `engine_ref` has no cylinder column, so a decode can hold the map's wrong cylinder count next to TecDoc's bank
  count (AEB: 6 cylinders, 1 bank).
- The window's model-year offset (`end + 1`) has no vinlab wiki source; it rests on the approved plan.

## Branch and log
```
$ git -C C:/4DApp/repo branch --show-current
fix/T-VINA-13b
$ git -C C:/4DApp/repo log --oneline 11dfa95..HEAD
2dfbbba test(T-VINA-13b): G2 two-bank hint in isolation and pinned digest of the 72 original rows (correction 02)
fe64c8c spec(T-VINA-13b): correction 02 (two tests owed from the second review)
5bf69e5 feat(T-VINA-13b): merge the TecDoc 1Q2019 extract into vref.db
```
`fe64c8c` is Cowork's spec commit; `5bf69e5` and `2dfbbba` are mine.
