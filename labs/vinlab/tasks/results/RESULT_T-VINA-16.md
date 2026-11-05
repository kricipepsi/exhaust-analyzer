# Result

## Status
completed

## Summary
`engine_ref` now has a nullable `cylinder_count` (TecDoc's count), and the decoder prefers a positive count to the VDS
map's count. The merge tool rebuilt the shipped `vref.db` with the new column and filled 1,225 existing counts. It
inserted the 34 codes that G2 used to skip, because a stated count now makes G2 return False. `engine_ref` went from
1,274 to 1,308 rows, 1,259 of them with a count. A new test pins the whole shipped table (row count and canonical-dump
sha256). Every count in P2-P5, as corrected by C1-C5 and revision 02 (step 1 `376 passed, 8 skipped`, step 2
`58 passed`), was reproduced exactly. All 17 named mutants fail their named tests.

**Revision 02** (review; test file only, commit `84c5aa0`): two mutants that survived the earlier tests now each fail
an isolating test. `test_counted_db_with_not_null_sensors_refuses` runs over `has_maf` only, `has_map` only and both
NOT NULL, and kills `all(...)` in place of `any(...)` (M15). `test_conflicting_counts_across_spellings_leave_null`
kills `_stated_counts` keyed on the raw `engine_code` (M16). The tool, the decoder, the builder and `vref.db` did not
change; the shipped-table digest did not change.

Branch and log (`git -C repo branch --show-current`; `git -C repo log --oneline daae97d..HEAD`, base = the newest spec
commit `daae97d`; and `git -C repo log --oneline 96d8a43..HEAD` for the whole build):
```
fix/T-VINA-16
84c5aa0 test(T-VINA-16): isolate the any() sensor refusal and the normalised count key (revision 02)
```
```
84c5aa0 test(T-VINA-16): isolate the any() sensor refusal and the normalised count key (revision 02)
daae97d spec(T-VINA-16): review revision 02 (two isolating merge tests)
324fd5a test(T-VINA-16): C2 refusal test fills only, so its mutant does not raise
52b834f fix(T-VINA-16): engine_ref cylinder_count from TecDoc; the decoder prefers it
```

## Files changed
- `labs/vinlab/tools/build_vref_db.py`: R1, the `cylinder_count INTEGER` line after `displacement_cc` and its comment
  line. Nothing else.
- `labs/vinlab/tools/merge_tecdoc_extract.py`: R2. The guard accepts the builder's columns with or without
  `cylinder_count`. A db without it is rebuilt. A db with it and NOT NULL `has_maf`/`has_map` is refused before any
  write (C2). `_stated_counts` and the NULL-only `BACKFILL_COUNT` do the backfill. `_new_row` writes the coalesced
  count. G2 returns False on a parsed positive count, test (i) is removed (C5). `MergeReport.backfilled` is added, the
  new last line is printed, and the docstring is updated.
- `labs/vinlab/vinlab/decoder.py`: R3, three lines plus a comment in `decode_vin_payload` between
  `_apply_vref_techmask` and `_cylinder_fallback`, on the in-window `db_dict`.
- `labs/vinlab/vinlab/data/vref.db`: the R2 run (sha256 prefix `88d5818782b8acff` → `660e81961e887038`).
- `labs/vinlab/tests/unit/test_vref_banks_induction.py`: T-D1-T-D4 (8 tests).
- `labs/vinlab/tests/unit/test_vref_tecdoc_merge.py`: T-M1, M2, M4, M5, M6, M8, M10, M11, M12, M13 new; T-M7
  parametrised over `""`/`"0"`; T-M3 rebuilt; T-M9 and `test_skips_code_already_in_vref` compare every column except
  `cylinder_count` (+11 tests). Revision 02 (`84c5aa0`): T-M13 parametrised over `has_maf`/`has_map`/both NOT NULL,
  and `test_conflicting_counts_across_spellings_leave_null` new (+3 items; the file now collects 41).
- `labs/vinlab/tasks/progress_notes/T-VINA-16.md` (plan, plan round 2, build log, gates, time) and this file.

Merge tool output on the shipped db (first run, step 6, `cwd=C:/4DApp/repo/labs/vinlab`):
```
skipped in_vref: 1226
skipped collision: 9
skipped status: 0
skipped no_my_start: 37
skipped span_gap: 0
skipped map_banks: 0
skipped cylinder_heuristic: 0
collision codes: 1E 2GRFE A112A2000 A20NHT B6 FA20 JB K10B LFW
inserted 34 rows; cylinder counts filled 1225; engine_ref now 1308 rows; schema rebuilt: yes
```
The 34 new codes (brand, `displacement_cc`, `cylinder_count`, V when `is_v_engine` 1): 108C (PEUGEOT, 954, 4), 1095F
(CITROEN, 1124, 4), 109F (PEUGEOT, 1124, 4), 109K (CITROEN, 1124, 4), 128A000 (FIAT, 1116, 4), 206KA (BMW, 1990, 6),
308S1 (BMW, 2997, 8, V), 8L (JAGUAR, 4235, 6), 99H (ROVER, 998, 4), AM2 (CITROEN, 602, 2), AR01646 (ALFA ROMEO, 2492,
6, V), C1C (RENAULT, 956, 4), EK42 (SUBARU, 665, 2), EN07 (SUBARU, 658, 4), EZA (DODGE, 5654, 8, V), EZH (DODGE, 5654,
8, V), F 106 D (FERRARI, 1991, 8, V), F105A (FERRARI, 2927, 8, V), G4HCE (GENESIS, 999, 4), G6DA (GENESIS, 3778, 6, V),
H25A (SUZUKI, 2493, 6, V), HDY (PEUGEOT, 1124, 4), HDZ (CITROEN, 1124, 4), HFY (PEUGEOT, 1124, 4), L-83 (CHEVROLET,
5328, 8, V), L31 (CHEVROLET, 5733, 8, V), L35 (CHEVROLET, 4300, 6, V), L98 (CHEVROLET, 5733, 8, V), LF8 (CHEVROLET, 7439,
8, V), LM7 (CHEVROLET, 5328, 8, V), M30B32 (BMW, 3210, 6), M97/20 (PORSCHE, 2687, 6), M97/70 (PORSCHE, 3600, 6), S01
(JEEP, 3960, 6). Rows with a NULL count after the merge: 49 (P2: 48 with no extract code + 1 with only blank counts).
Shipped-table digest: 1,308 rows × 33 columns,
`4ee7543717bfa80b95f32f97d584ca9390451c03138f25e3284d0251bfc13a42`.

## Commands executed
- First action, preconditions and the plan-time digest table (`sha256sum <path> | cut -c1-16`, all six equal).
- Red run: `pytest -q -p no:cacheprovider tests/unit/test_vref_tecdoc_merge.py tests/unit/test_vref_banks_induction.py
  --basetemp=C:/4DApp/recheck/T-VINA-16/pt/red` → `18 failed, 37 passed`.
- Step 6: a stdin script from `audit/scratch/C6` (decode the 1,131 `c6_lib.real_vins()`, run
  `$PY tools/merge_tecdoc_extract.py` with `cwd=C:/4DApp/repo/labs/vinlab`, `_build_normalised_index.cache_clear()`,
  decode again, diff, compare with `survey.out` S5). Then a one-liner for the digest.
- `### Verification ###` steps 1-5, verbatim (step 1 and step 2 run twice: after `52b834f` and after `324fd5a`).
- Mutants M1-M14 (stdin driver: copy to `C:/4DApp/recheck/T-VINA-16/mut/<id>_<file>`, edit the copy, copy it over, run
  the named test with `--basetemp=…/pt/<id>`, `git restore`), plus M13 again after `324fd5a`.
- The task-end gate: `py_compile`, `py -m ruff check`, `py -m ruff check --select S`, `py -m pyright --pythonpath
  C:/4DApp/.venv/Scripts/python.exe`, the import sanity line and `audit/tools/isolation.py`.
- Revision 02: First action, preconditions and the re-recorded digest table (all six equal); base steps 1 and 2
  (`373 passed, 8 skipped`, `55 passed`); M15 and M16 against the unedited merge file (`38 passed` each: survived);
  the edit; the 4 new items (`4 passed`); steps 1 and 2; commit `84c5aa0`; M15, M16 and M13 against the named test
  (copy in `C:/4DApp/recheck/T-VINA-16/mut/`, copy over, `--basetemp=…/pt/<id>`, `git restore`); `### Verification ###`
  steps 3-5 verbatim; `py_compile`, ruff, `ruff --select S` and pyright on the test file.

## Validation evidence
| step | expected | actual |
|---|---|---|
| 1 vinlab | `376 passed, 8 skipped` (revision 02) | `376 passed, 8 skipped in 7.79s` (build: `373 passed, 8 skipped in 7.59s`) |
| 2 named files | `58 passed` (revision 02) | `58 passed in 3.93s` (build: `55 passed in 3.74s`) |
| 3 dnalab / wired / ui | `27 passed` / `41 passed` / `30 passed` | `27 passed in 0.99s` / `41 passed in 3.31s` / `30 passed in 3.24s` |
| 4 reach | `{'no_engine_code': 12, 'not_in_vref': 468, 'out_of_window': 72, 'row_applied': 579}` | identical |
| 5 second run | `inserted 0 rows; cylinder counts filled 0; engine_ref now 1308 rows; schema rebuilt: no` | identical |
| 5 db status | no line | no line; sha256 prefix `660e81961e887038` before and after |
| 5 ruff (`.venv-loop`) | `All checks passed!` | `All checks passed!` |
| 5 log | spec and ledger commits, then mine | `84c5aa0`, `daae97d`, `324fd5a`, `52b834f`, `96d8a43`, `1bac3f3`, `d681469`, `53a06db` |
| 5 status | the note and the RESULT | see below |

Reach (step 4): **before** (base, P1) `{'no_engine_code': 12, 'not_in_vref': 483, 'out_of_window': 68, 'row_applied':
568}`; **after** `{'no_engine_code': 12, 'not_in_vref': 468, 'out_of_window': 72, 'row_applied': 579}`. The previous
decisive failures are now absent: `not_in_vref` is no longer 483, G2 no longer skips 34 codes (`cylinder_heuristic: 0`),
and AEB / NG / H25A no longer decode 6 / 6 / 0 cylinders (now 4 / 5 / 6, H25A with 2 banks).

Mutants (each named test: `1 failed`):
| id | rule | named test | failure |
|---|---|---|---|
| M1 | R1 NOT NULL DEFAULT 0 | `test_two_count_code_leaves_the_count_null` | `assert 0 is None` |
| M2 | R2 exact guard | `test_null_count_is_backfilled_from_a_single_count_code` | `RuntimeError: … columns differ` |
| M2b | R2 superset guard | `test_other_column_difference_refuses` | `DID NOT RAISE RuntimeError` |
| M3 | R2 rebuild on sensors only | `test_db_without_cylinder_count_is_rebuilt` | `no such column: cylinder_count` |
| M4 | R2 ≥ 1 count fills | `test_two_count_code_leaves_the_count_null` | `assert 1 == 0` |
| M5 | R2 no `IS NULL` | `test_stated_count_is_kept` | `assert 1 == 0` |
| M6 | R2 new row count None | `test_new_row_carries_the_coalesced_count` | `assert None == 4` |
| M7 | R2 no G2 early return | `test_cylinder_heuristic_two_bank_hint_with_stated_count_is_inserted` | `assert () == ('ZZ3VEE',)` |
| M8 | R2 G2 on `group[0]` | `test_g2_runs_on_the_coalesced_row` | `assert () == ('ZZ2GTW',)` |
| M9 | R2 `backfilled=0` | `test_null_count_is_backfilled_from_a_single_count_code` | `assert 0 == 1` |
| M10 | R3 deleted | `test_vref_count_replaces_map_count` | `assert 6 == 4` |
| M11 | R3 without `> 0` | `test_null_or_zero_vref_count_keeps_map_count[0]` | `assert 4 == 6` |
| M12 | one `UPDATE` of the shipped db | `test_shipped_engine_ref_matches_the_pinned_digest` | `'3cbbf67d78c1…' == '4ee7543717bf…'` |
| M13 | C2 refusal deleted | `test_counted_db_with_not_null_sensors_refuses` | `DID NOT RAISE RuntimeError` |
| M14 | C5 raw truthiness | `test_cylinder_heuristic_two_bank_hint_alone_is_skipped[0]` | `assert ('ZZ3VEE',) == ()` |
| M15 | C2 `all(...)` for `any(...)` (revision 02) | `test_counted_db_with_not_null_sensors_refuses` | `2 failed, 1 passed`: `[has_maf]`, `[has_map]` `DID NOT RAISE RuntimeError`; `[both]` passes (derived) |
| M16 | `_stated_counts` on the raw code (revision 02) | `test_conflicting_counts_across_spellings_leave_null` | `assert 1 == 0` (`backfilled=1`) |

Before the revision 02 edit, M15 and M16 each left the whole merge file green (`38 passed`). M13 re-run on the
parametrised test: `3 failed`, each `DID NOT RAISE RuntimeError`.

### R5: every real VIN whose decoded field changed (1,131 decoded; 71 VINs: cylinder 71, banks 1, displacement 11; induction, euro, O₂ type, air metering 0)

Cause key. **B**: the existing row's `engine_ref.cylinder_count`, filled by R2 from the extract's `cylinder_count`
and read by R3. **I**: the row inserted by R2: `cylinder_count` (extract `cylinder_count`), `displacement_cc` (extract
`displacement_cc`), and banks from `is_v_engine` (extract `is_v_engine` 1). Each set equals `survey.out` S5 (C1).

| VIN | make | code | change | cause |
|---|---|---|---|---|
| JSAFTD62V00115689 | SUZUKI | H25A | cyl 0→6; banks 1→2; disp 0.0→2.493 | I (6, is_v_engine 1, 2493 cc) |
| JSAGJB74V00141993 | SUZUKI | K15B | cyl 3→4 | B (4) |
| MA3EFA11S00202163 | SUZUKI | G10B | cyl 3→4 | B (4) |
| MA3EFB11S00161410 | SUZUKI | G10B | cyl 3→4 | B (4) |
| SAJAF51S73YD29577 | Jaguar | YB | cyl 4→6 | B (6) |
| SAJAF52SX2YC71204 | Jaguar | YB | cyl 4→6 | B (6) |
| SED52SUD2RV621223 | OPEL | C20NE | cyl 6→4 | B (4) |
| VF31AHDZE51969250 | Peugeot | HDZ | cyl 3→4; disp 1.1→1.124 | I (4, 1124 cc) |
| VF31AHFXF52787052 | Peugeot | HFX | cyl 3→4 | B (4) |
| VF31CHFXF52681707 | Peugeot | HFX | cyl 3→4 | B (4) |
| VF320AHD225121300 | Peugeot | HDZ | cyl 3→4; disp 1.1→1.124 | I (4, 1124 cc) |
| VF320CHD224363337 | Peugeot | HDZ | cyl 3→4; disp 1.1→1.124 | I (4, 1124 cc) |
| VF32AHFZE40514662 | Peugeot | HFZ | cyl 3→4 | B (4) |
| VF32CHFXF43308055 | Peugeot | HFX | cyl 3→4 | B (4) |
| VF32CHFZE40789228 | Peugeot | HFZ | cyl 3→4 | B (4) |
| VF32CHFZE40903096 | Peugeot | HFZ | cyl 3→4 | B (4) |
| VF37CHDZ231042415 | Peugeot | HDZ | cyl 3→4; disp 1.1→1.124 | I (4, 1124 cc) |
| VF7FCHFXB26734954 | CITROEN | HFX | cyl 3→4 | B (4) |
| VF7S0HDZF57157878 | CITROEN | HDZ | cyl 3→4; disp 1.1→1.124 | I (4, 1124 cc) |
| VF7S0HFXB57546281 | CITROEN | HFX | cyl 3→4 | B (4) |
| VF7S1HDZF57133610 | CITROEN | HDZ | cyl 3→4; disp 1.1→1.124 | I (4, 1124 cc) |
| VF7S1HFXB57478926 | CITROEN | HFX | cyl 3→4 | B (4) |
| VF7S1HFXB57756386 | CITROEN | HFX | cyl 3→4 | B (4) |
| VF7ZADA0016DA9064 | CITROEN | HDZ | cyl 3→4; disp 1.1→1.124 | I (4, 1124 cc) |
| VF7ZADB0007DB0700 | CITROEN | HDZ | cyl 3→4; disp 1.1→1.124 | I (4, 1124 cc) |
| VF7ZALH0030LH4160 | CITROEN | CDZ | cyl 3→4 | B (4) |
| VF7ZALJ0013LJ6093 | CITROEN | CDZ | cyl 3→4 | B (4) |
| VSSZZZ6HZWW062386 | SEAT | AER | cyl 3→4 | B (4) |
| W0L0JBF35X1116159 | Opel | X16XEL | cyl 6→4 | B (4) |
| W0L0JBF35X7074950 | Opel | X16XEL | cyl 6→4 | B (4) |
| W0L0SBF08W4005800 | Opel | X10XE | cyl 4→3 | B (3) |
| W0L0SBF08X4314007 | Opel | X10XE | cyl 4→3 | B (3) |
| W0L0TGF08X5128808 | Opel | X16XEL | cyl 6→4 | B (4) |
| W0L0TGF672B013571 | Opel | X16XEL | cyl 6→4 | B (4) |
| WAUZZZ4BZYN125879 | Audi | AEB | cyl 6→4 | B (4) |
| WAUZZZ8CZSA064263 | Audi | ADA | cyl 6→4 | B (4) |
| WAUZZZ8GZNA003486 | Audi | NG | cyl 6→5 | B (5) |
| WAUZZZ8GZSA005846 | Audi | NG | cyl 6→5 | B (5) |
| WBAAA310008496854 | BMW | 206EB | cyl 4→6 | B (6) |
| WBAAD51060AG07941 | BMW | 206KA | cyl 4→6; disp 2.0→1.99 | I (6, 1990 cc) |
| WBAAM11010JM47828 | BMW | 206S4 | cyl 4→6 | B (6) |
| WBAAM11040KF00230 | BMW | 206S4 | cyl 4→6 | B (6) |
| WBAAM110X0JM34916 | BMW | 206S4 | cyl 4→6 | B (6) |
| WBAAR11010JL52753 | BMW | 206S4 | cyl 4→6 | B (6) |
| WBABF11000JA32663 | BMW | 206S2 | cyl 4→6 | B (6; row `20 6 S2`) |
| WBABF61090EP34175 | BMW | 206S3 | cyl 4→6 | B (6) |
| WBABM11070JK07381 | BMW | 206S4 | cyl 4→6 | B (6) |
| WBABM11080JK06658 | BMW | 206S4 | cyl 4→6 | B (6) |
| WBACB21020AL80676 | BMW | 20 6 S2 | cyl 4→6 | B (6) |
| WBACE51060EN70353 | BMW | 206S3 | cyl 4→6 | B (6) |
| WBADD11000BN34739 | BMW | 206S3 | cyl 4→6 | B (6) |
| WBADD11020BN21085 | BMW | 206S3 | cyl 4→6 | B (6) |
| WBADD11030BN04344 | BMW | 206S3 | cyl 4→6 | B (6) |
| WBADM11010GP20616 | BMW | 206S4 | cyl 4→6 | B (6) |
| WBAGB41090DA55909 | BMW | 346KB | cyl 8→6 | B (6) |
| WBAHB11020GB32718 | BMW | 206KA | cyl 4→6; disp 2.0→1.99 | I (6, 1990 cc) |
| WBAHD21020BF36101 | BMW | 346KB | cyl 8→6 | B (6) |
| WBAHG51090GJ95949 | BMW | 206S2 | cyl 4→6 | B (6; row `20 6 S2`) |
| WBSAK050801894162 | BMW | 234EA | cyl 6→4 | B (4) |
| WBSDE91030GJ20140 | BMW | 508S1 | cyl 12→8 | B (8) |
| WBSHD91060BK03580 | BMW | 366S1 | cyl 8→6 | B (6) |
| WV2ZZZ7HZ6H007904 | Volkswagen | BKK | cyl 4→6 | B (6) |
| WVWZZZ3BZ1E079146 | Volkswagen | AEB | cyl 6→4 | B (4) |
| WVWZZZ6NZ1D110891 | Volkswagen | AER | cyl 3→4 | B (4) |
| WVWZZZ6XZ1W018642 | Volkswagen | AUC | cyl 3→4 | B (4) |
| YF7JMHFXC97059924 | CITROEN | HFX | cyl 3→4 | B (4) |
| YV1RS49K212068541 | Volvo | B5204T5 | cyl 4→5 | B (5) |
| ZAMCD39B000016113 | Maserati | M139 | cyl 6→8 | B (8) |
| ZAR93600000061356 | Alfa Romeo | AR36201 | cyl 4→6 | B (6) |
| ZAR93600000068984 | Alfa Romeo | AR36201 | cyl 4→6 | B (6) |
| ZFA18700000143151 | Fiat | 187A1000 | cyl 3→4 | B (4) |

No dnalab, wired or ui test changed value (step 3 = P5). The one test-tree VIN whose count changes,
`W0L0SBF08X4314007` (X10XE 4 → 3), is used only by `test_real_vin_gains_row_with_tecdoc_displacement`, which does not
assert the count (Plan § 5).

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 1 `376 passed, 8 skipped`; step 2 `58 passed` (the counts after C1-C5 and revision 02); M1-M16 and M2b (17) each fail the named test (table above) |
| 2 | MET | step 3: dnalab `27 passed`, wired `41 passed`, ui `30 passed` = P5; the plan names no changed value there, and none changed |
| 3 | MET | step 4 prints P3's reach line exactly; the R5 list has all 71 changed VINs, each with its TecDoc field. The three field sets equal `survey.out` S5 and their union is 71 (C1) |
| 4 | MET | ruff `All checks passed!`; the second run prints `inserted 0 rows; cylinder counts filled 0; engine_ref now 1308 rows; schema rebuilt: no` with no `vref.db` status line (prefix `660e81961e887038` before and after); `324fd5a` and `52b834f` sit on `fix/T-VINA-16` after `96d8a43`, and `84c5aa0` after `daae97d`; `git status --porcelain` lists the note and this RESULT only |

Final `git -C C:/4DApp/repo status --porcelain`:
```
?? labs/vinlab/tasks/progress_notes/T-VINA-16.md
?? labs/vinlab/tasks/results/RESULT_T-VINA-16.md
```

## Decisions the task did not specify
- `test_skips_code_already_in_vref` was not named by the plan or R4. Its default extract row states 4, so R2 now fills
  `5FR`. Its whole-row comparison now excludes `cylinder_count`, the same ruling R4 gives
  `test_existing_rows_keep_every_value` (note A6).
- T-M13 uses a fill-only extract (`5FR` 4). With the original insert extract, mutant M13 failed only through an
  incidental `IntegrityError` (NOT NULL `has_maf` on insert). Now it fails with `DID NOT RAISE` (second commit
  `324fd5a`, note A7).
- After C2, `rebuild` is `"cylinder_count" not in names`. A NOT NULL-sensor db without the column (the fixture) still
  rebuilds, and one with the column refuses, so the sensor test now feeds the refusal only.
- `backfilled` is the `executemany` `rowcount` only when there is something to fill, else 0 (note A8).
- R3 reads `db_dict`, the in-window row, so a count applies only inside the row's model-year window, like every other
  vref field (plan choice C1).
- Revision 02, how a variant table is built (note A9): SQLite cannot drop a NOT NULL constraint in place, so each case
  recreates the fixture table from `PRE_MERGE_DDL` with the other sensor's `NOT NULL DEFAULT 0` removed, adds
  `cylinder_count` and copies the rows. A `PRAGMA table_info` assertion checks the notnull flags before the merge.
- Revision 02: M13 was re-run on the parametrised test (not asked), because its named test changed shape (note A10).

## Pre-existing changes preserved
None: the working tree was clean apart from this task's own plan note (`?? …/progress_notes/T-VINA-16.md`, note A5).

## Rollback
Revert the three commits on `fix/T-VINA-16` (`git -C C:/4DApp/repo revert 84c5aa0 324fd5a 52b834f`). That restores
the six files, including `vref.db` at sha256 prefix `88d5818782b8acff`. Revision 02 alone: `git -C C:/4DApp/repo revert
84c5aa0` (the test file only). Nothing was pushed; `main` was not touched.

## Remaining risks or uncertainties
- TecDoc's count now overrides a contradicting map count on 71 real VINs (R3 by ruling). The plan cross-checked seven
  of them against TecDoc's own displacement and `is_v_engine` (§ 8). The rest are listed above for review but were not
  each checked against an outside source. Some are plausible map errors (BMW 206S4 2.0 L I6, Audi NG 2.3 L I5). Some
  are surprising and worth an expert look: Peugeot/Citroën HFX/HDZ/HFZ 1,124 cc 3 → 4 (TecDoc says 4, the TU1 is an I4,
  so plausible), and SUZUKI G10B 993 cc 3 → 4.
- R2 ignores brand. A vref row and an extract code that share a normalised code but are different engines get the
  extract's count. One known displacement mismatch is filled: `M96_03` PORSCHE, 3,387 cc vs 3,596 cc, 6 in both, so
  the count is right.
- The 49 NULL-count rows keep the map's count, which may be wrong (T-VINA-11b).
- The merged `vref.db` has 33 free pages from the rebuild (192,512 → 352,256 bytes; `PRAGMA integrity_check` `ok`). No
  VACUUM was run, because R2 says to run the tool once and a VACUUM would change the bytes the second-run check pins.
- Pre-existing, not caused by this task: `ruff --select S` reports 5 × S608 in `tools/build_vref_db.py` lines 401-481,
  and pyright reports 1 error, the unresolved `mysql.connector` at `build_vref_db.py:308`. Both are identical on the base
  file.
- The repo-wide suites and `baseline.sh` were NOT RUN (report-only; Cowork runs them at review).
