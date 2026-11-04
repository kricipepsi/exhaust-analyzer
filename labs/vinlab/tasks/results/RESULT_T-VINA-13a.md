# Result

## Status
completed

## Summary
`labs/vinlab/tools/extract_tecdoc_1q2019.py` (stdlib only) reads 5 TecDoc 1Q2019 tables from
`D:/4DLab/4DLabV2/DBS/1Q2019/`, read-only. It writes `labs/vinlab/tools/data/tecdoc_1q2019_engine_extract.csv`:
**1,498 rows**, one per (folded brand, normalised code) pair of `vds_engine_map.csv` that TecDoc knows under an
allowed manufacturer. The run implements the approved plan with correction 01 (C1-C6). Every count equals the
plan-round-2 prediction. The real-VIN coverage is **642 of 1,115** (vref.db today 18; P5 brand-agreeing 631).
13 new tests pass (11, plus 2 from review correction 02), and 15 mutants each fail their named test (my 13, and
Cowork's `review/F2.py` and `F3.py`). A fresh run is byte-identical to the committed CSV.

Branch and log:
```
$ git -C C:/4DApp/repo branch --show-current
fix/T-VINA-13a
$ git -C C:/4DApp/repo log --oneline f0e26bb..HEAD
aa7cdbf test(T-VINA-13a): whole-part T1 key and blank-field ambiguity tests (correction 02)
7b87192 spec(T-VINA-13a): correction 02 file modes
6316a28 spec(T-VINA-13a): correction 02 (two tests owed from the second review)
f836bcf feat(T-VINA-13a): TecDoc 1Q2019 per-engine extract tool, tests and CSV (1,498 rows)
```
Base `f0e26bb` (`spec(T-VINA-13a): plan correction 01`); `git log --oneline 7ba9368..HEAD` = `aa7cdbf`, `7b87192`,
`6316a28`, `f836bcf`, `f0e26bb`, `e320768`. My commits: `f836bcf` (tool, test, CSV) and `aa7cdbf` (correction 02
tests; the tool and the CSV are unchanged).

## Files changed
- `labs/vinlab/tools/extract_tecdoc_1q2019.py` (CREATE, committed)
- `labs/vinlab/tools/data/tecdoc_1q2019_engine_extract.csv` (CREATE, committed; 1,499 lines with header, LF)
- `labs/vinlab/tests/unit/test_extract_tecdoc_1q2019.py` (CREATE in `f836bcf`; MODIFY in `aa7cdbf`, +2 tests)
- `labs/vinlab/tasks/progress_notes/T-VINA-13a.md` (CREATE, untracked)
- `labs/vinlab/tasks/results/RESULT_T-VINA-13a.md` (this file, untracked)
- Runtime only: `C:/4DApp/recheck/T-VINA-13a/pt/`, `out/run2.csv`, `mut/` (13 mutant copies).

## Commands executed
- First action, preconditions, and the vinlab suite on the base (`248 passed, 8 skipped`).
- Measurement scripts on stdin (no file written): CSV format, field counts, attribute vocabulary, the prototype.
- The red run, the green run, and verification steps 1-5 as written in the task.
- The real run: `cd labs/vinlab && DBS_ROOT=D:/4DLab/4DLabV2/DBS $PY tools/extract_tecdoc_1q2019.py` (8.9 s).
- `py -m ruff check`, `py -m ruff check --select S`, `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe`,
  `py_compile`, and the deployed-layout import check.
- The mutant driver (stdin script): copy to `mut/<name>.py`, copy over the tool, `pytest -k <test>`, `git restore`.

## Validation evidence
- Step 1: `261 passed, 8 skipped in 4.04s` (P6 248 + 13 new; before correction 02 it was `259 passed, 8 skipped`).
- Step 2: `13 passed in 1.47s` (before correction 02: `11 passed`). Red run before the tool existed: `11 errors`, all `FileNotFoundError` for the tool.
- Step 3: the tool printed its last 3 lines (below), then `identical`.
- Step 4: `real VINs: {'vins_with_code': 1115, 'vref_today': 18, 'extract': 642}`; hits by (tier, status):
  T0/AMBIGUOUS 1, T0/OK 376, T0A/OK 13, T1/AMBIGUOUS 23, T1/FAMILY 28, T1/OK 201.
- Step 5 (after `aa7cdbf`): `All checks passed!`; the log above; porcelain = the note (and this RESULT).
- pyright `0 errors`. ruff `--select S`: the tool is clean; the test shows S101 (`assert`), the pytest idiom.

### Coverage report (R6), from the real run's stdout
**Tables:** manufacturers 4,760 rows, engines 26,125, items_atributes 1,914,913, passengercars 69,871,
passengercars_link_engines 65,296. **Skipped for a wrong field count: 0 in every table.**

**Population:** 5,881 pairs (7 map rows have no code). Hits before the petrol filter: T0 1,138, T1 269, T0A 118.

**Rows per `match_tier` and `status` (1,498):**
| tier | OK | FAMILY | AMBIGUOUS | total |
|---|---|---|---|---|
| T0 | 1,117 | 0 | 2 | 1,119 |
| T1 | 189 | 34 | 40 | 263 |
| T0A | 116 | 0 | 0 | 116 |

**Population pairs with no row (4,383):** another manufacturer **412**, non-petrol **27** (all Diesel), no code
**3,944**. 1,498 + 412 + 27 + 3,944 = 5,881.
Another-manufacturer groups (369 groups, top lines): `MOTOGUZZI`→VW 6, `PEUGEOT`→CITROEN 6 (platform share),
`AUDI`→AUDIFAW 5 (JV, rejected alias), `HYUNDAI`→KIA 5 (platform share), `MATRA`→RENAULT 4, `JAGUAR`→AUDI 3,
`JAGUAR`→VW 3, `KAWASAKI`→SUZUKI 3, `LIVEWIRE`→VW 3, `MOTOGUZZI`→AUDI 3, `NISSAN`→NISSANDONGFENG 2 (JV),
`SKODA`→AUDI 2, `LANCE`→SEAT,VW 2.

**Fill rate per column (of 1,498):** brand, engine_code, match_tier, status, tecdoc_engine_ids, tecdoc_description,
n_cars 100%; displacement_cc 1,479 (98.7%); cylinder_count 1,497 (99.9%); fuel_delivery_type 1,471 (98.2%: GDI 213,
PORT_INJECTION 1,258); induction_type 1,125 (75.1%: NA 858, TURBOCHARGED 260, SUPERCHARGED 7); has_turbo 1,125
(75.1%); has_gdi 1,484 (99.1%); is_v_engine 1,483 (99.0%); valvetrain_type 1,396 (93.2%: DOHC 876, SOHC 448, OHV 69,
CIH 3); euro_norm 114 (7.6%: euro1 1, euro2 1, euro4 55, euro5 33, euro6 24); my_start 1,458 (97.3%); my_end 957
(63.9%); n_cars > 0 1,458 (97.3%).

**C3 twincharger (`Turbocharger/Compressor`) rows: 0** (33 petrol engines carry it; none is in a row).

**Codes under more than one brand with different field values:** 173 codes are rows under more than one brand; **44**
differ in at least one of the 9 fields: `169A4000 18K4F 18K4K 1E 1KR 1UZFE 2GRFE 4A 6FY A112A2000 A20NHT ADY APQ B12S1
B38A15A B48A20A B6 BDY BKY CDZ D16A8 F18A3 FA20 FE FS G4FG HFX JB K10B KDX KDY KFV KFW KFX KL LFW PT204 RFJ RFK RFN RFU
RFW RGX VK45DE`. T-VINA-13b keys vref.db by code only, so it must rule on these.

**Kept engines' FuelType** (for T-VINA-13b; EngineType is the H1 filter): Petrol 1,754, Super unleaded (95) 33,
Regular (91) unleaded 3, Petrol/Alcohol 36, Petrol/Gas 19, Petrol/Alcohol/Gas 3, Petrol/Electro 1.

**Real VINs (`coverage.py`):** 642 covered, against P5's brand-agreeing 631. The prediction was 642: T0+T1 go from 631 to 629
(1 VIN lost to the petrol rule, 1 to C1), and T0A adds 13.

### Mutants (R7 7): 15 of 15 killed
My 13 were run on the 11-test file (`1 failed, 10 deselected` each). I re-ran them on the 13-test file
(`1 failed, 12 deselected` each).
| mutant | test that kills it |
|---|---|
| M1 T0 compares raw Description | `test_t0_exact_hit` |
| M2 paren key dropped; M2b digit head keys emitted (C1) | `test_t1_paren_alias_hit_and_no_digit_head_key` |
| M3 manufacturer comparison skipped | `test_other_manufacturer_miss` |
| M4 `VOLKSWAGEN` alias deleted | `test_alias_table_hit` |
| M5 first id's value kept; M5b FAMILY never emitted (C2) | `test_ambiguity_blanks_disagreeing_field_and_family` |
| M6 EngineType filter removed | `test_non_petrol_excluded` |
| M7 `my_end` = max of closed ends only (C5) | `test_years_from_cars_with_open_end` |
| M8 field-count check removed | `test_short_row_skipped_and_counted` |
| M9 output unsorted (loop order and final sort) (C4) | `test_deterministic` |
| M10 fold without NFKD | `test_fold_matches_vinlab` |
| M11 petrol filter before tier choice (C6) | `test_petrol_order_diesel_t0_blocks_petrol_t1` |
| Cowork `review/F2.py`: whole-part key dropped (02 a) | `test_t1_whole_part_before_parentheses_hit` (survived the 11; now `1 failed, 12 deselected`) |
| Cowork `review/F3.py`: blanks ignored when comparing ids (02 b) | `test_ambiguity_blank_field_disagrees` (survived the 11; now `1 failed, 12 deselected`) |

## Criteria
| # | verdict | evidence |
|---|---|---|
| 1 | MET | step 1 `261 passed, 8 skipped`; step 2 `13 passed`; 15/15 mutants killed by named tests (incl. F2, F3) |
| 2 | MET | step 3 `identical` (committed CSV against `out/run2.csv`) |
| 3 | MET | every R6 figure above; `coverage.py` prints `extract` 642 (predicted 642; P5 631) |
| 4 | MET | `.venv-loop` ruff `All checks passed!`; `f836bcf`, `aa7cdbf` after the spec commits on `fix/T-VINA-13a`; porcelain lists only the note and this RESULT |

## Decisions the task did not specify
- The tool imports `os`, `sys`, `unicodedata`, `collections` and `dataclasses` beyond R1's list. All are stdlib.
  `os` is needed for the `DBS_ROOT` default, and `unicodedata` for `_fold_brand` parity.
- `--map` argument (default the shipped map), so the tests can pass a fixture map.
- `--out` under the DBS root is refused (`parser.error`), which enforces R1's "never writes under the DBS root".
- Strict ambiguity: a blank counts as a value (plan round 1, approved).
- `tecdoc_engine_ids` lists only the kept (petrol) ids, sorted as integers. `tecdoc_description` is the sorted
  distinct Descriptions, `;`-joined.
- Years are calendar years of `passengercars.From/To` (production dates, not model years). A `0000` `From` is
  ignored for `my_start`.
- `valvetrain_type` vocabulary `DOHC`/`SOHC`/`OHV`/`CIH` (vref.db has none: 72/72 NULL, no reader).
- Other-manufacturer means the code is a T0 or T1 key (after C1) under some manufacturer that is not allowed. For
  that reason C1 moved 47 other-manufacturer pairs and the 5 all-digit T1 pairs to no code (+52: 3,892 → 3,944).
- The test loader registers the module in `sys.modules` before `exec_module` (needed by `dataclasses`).
- Correction 02 grew the shared fixture (engines 54/55, map rows `BMW M52B20`, `RENAULT H4J`). The short-row test's
  expected engines count followed (`rows 13` → `rows 15`). No other existing assertion changed.

## Pre-existing changes preserved
At the redispatch the only pre-existing item was my own untracked note. `C:/4DApp` master (`LOOP_STATE.md` M, the
launcher `??`) was not touched. `labs/vinlab/tests/unit/__pycache__/test_wmi_brands…pyc` was there before and stays.
I removed only the 2 `.pyc` files my `py_compile` run wrote (ignored paths), and the empty `tools/__pycache__/`.

## Rollback
Correction 02 only: `git -C C:/4DApp/repo revert aa7cdbf`. Whole row: `git -C C:/4DApp/repo reset --keep f0e26bb` on
`fix/T-VINA-13a` (this also drops Cowork's `6316a28` and `7b87192`), or do not push. Delete the two untracked
task documents if the row is dropped. Nothing was written under `D:/`.

## Remaining risks or uncertainties
- JV aliases (`AUDI (FAW)` 5 pairs, `NISSAN (DONGFENG)` 2, and others) are excluded. Including `AUDIFAW` would add 5
  Audi rows; the ruling is Cowork's.
- my_start/my_end are calendar years from the linked cars. 36% of rows have an open `my_end`, because a linked car is
  still in production in TecDoc 1Q2019.
- `induction_type` is 75% filled (ChargeType is absent on 373 rows' engines). `euro_norm` is 7.6% filled: TecDoc
  rarely states it. T-VINA-13b needs its fallback (V9 class).
- T1 FAMILY rows (34) pool variants that agree on all 9 fields. They can still differ in power or in a field TecDoc
  does not state.
- The 44 cross-brand code collisions need a T-VINA-13b ruling before a code-keyed merge.
- Repo-wide gates (dnalab, wired, ui, `baseline.sh`, `isolation.py`): NOT RUN, because they are report-only and no
  shipped module changed. Cowork runs them.
