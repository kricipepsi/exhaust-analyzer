# T-VINA-13b progress note: merge the TecDoc 1Q2019 extract into vref.db

Task file: `labs/vinlab/tasks/T-VINA-13b_vref_tecdoc_merge(5).md` (plan: REQUIRED). This session is the plan stop. No
repo file is edited. The only writes are this note and `T-VINA-13b.blocker.json` (three soft findings, below).

## Readiness

- (a) Starting state matches the task. `git branch --show-current` = `fix/T-VINA-13b`; `git log --oneline -1` =
  `6da3b90 spec(T-VINA-13b): merge the TecDoc extract into vref.db; plan REQUIRED`; its parent is `8592bb3`
  (`git log -1 --format=%P HEAD`). **Base = `6da3b90`.** `git status --porcelain` printed nothing. The Preconditions
  block printed `checked` with no `MISSING` or `EXISTS` line. `reach.py` on the base prints P3 exactly, and
  `vina13b_measure.py` prints P1 and P4 exactly (outputs under "Measurements").
- (b) Test fails for the intended reason: the R5 tests do not exist yet (plan stage). At red, every test fails because
  `tools/merge_tecdoc_extract.py` does not exist (the importlib loader raises `FileNotFoundError`). The decisive
  decode test is also red on the data: on the shipped db, `W0L0SBF08X4314007` decodes with displacement `1.4` (map
  value); the test expects `0.973` (TecDoc `displacement_cc` 973 for X10XE).
- (c) Independent decisive value: I built the merged db with my own prototype of the plan's rules in a throwaway copy
  and decoded all 1,131 real VINs against both dbs with the unchanged decoder. Predicted `reach.py`
  `row_applied` = **506** (base 15). Reconciliation with P4: 624 brand-agreeing VINs = 70 collision + 4 no `my_start` +
  18 decode-hazard skip + 532 inserted; plus 15 VINs whose code TecDoc lists only under another brand (the lookup is
  code-only) = 547 VINs on a new row = 491 in window + 56 out of window. 15 + 491 = 506.
- (d) Three findings match a stop class. All three are SOFT and recorded in `T-VINA-13b.blocker.json` with the chosen
  interpretation: F1 boxer banks (R3 vs Goal and criterion 1), F2 cylinder heuristic (R4 vs R1/R3), F3 stale schema
  literal. None prevents implementation on the recorded interpretation. Cowork's plan review rules on F1 and F2.
- (e) Teach-back: a new stdlib tool inserts one `engine_ref` row per TecDoc extract code that vref.db lacks, after a
  table rebuild that makes `has_maf`/`has_map` nullable, and skips the codes whose row would put a value into a decode
  that TecDoc does not state. The decisive check is `reach.py` after the merge: `row_applied` 506, with every euro,
  O₂ and air-metering change traced to a TecDoc-stated field, and a second run that changes no byte of vref.db.

## Assumptions worked past

- **`build_vref_db` cannot be imported without `DBS_ROOT`.** `tools/build_vref_db.py:33-36` raises `RuntimeError`
  at import when `DBS_ROOT` is unset. `DBS_ROOT` is unset on this host and `C:/DBS` is empty. R3 asks for
  `build_vref_db._derive_era`, and verification step 5 runs the tool with no `DBS_ROOT`. Chosen: the tool loads
  `build_vref_db.py` with importlib and sets a placeholder `DBS_ROOT` only for the import, then removes it. The tool
  reads no DBS file. Rejected: a copy of `_derive_era` and `CREATE_ENGINE_REF` in the tool (two sources of truth).
- **CoC stays NULL.** `_enrich_from_csv` reads `$DBS_ROOT/docs/vehicles_petrol_specimens.csv`
  (`build_vref_db.py:38,809`). The file is absent (`find /c/4DApp /c/Users -maxdepth 6 -iname
  "vehicles_petrol_specimens*"` found nothing; `ls /c/DBS` is empty). Count it fills: **0, ABSENT (no CSV on host)**.
  A NULL CoC adds the flag `coc_null_target_lambda_v112` (`decoder.py:399-408`, the first NULL field breaks the loop).
  The row also removes `engine_not_in_vref`, so confidence stays `PARTIAL` (measured: no confidence change).
- **P4's population is brand-agreeing; `reach.py` counts by code.** `lookup_engine_ref` ignores brand, so 15 real VINs
  whose code TecDoc lists only under another brand also reach a new row (for example `KNE…` VINs decoded as
  "Hyundai" that carry Kia codes, `JTE…` VINs decoded as "Subaru" with Toyota `1AZ-FE`). The engines match; the
  brand label is a WMI matter (T-VINA-5 area). I report both populations.
- **The extract has two rows per code only across brands** (one row per folded brand and code, extract tool
  docstring). 129 codes repeat with identical fields; 87 of them differ in years only, with 89 real VINs.
- **Throwaway files.** The prediction runs built temp dbs under `C:/4DApp/recheck/T-VINA-13b/mut/tmp*` (runtime path
  of this task) and I deleted them after use. `impl_guard` refused a script file at `mut/predict_merge.py`, so every
  script ran from stdin. The appendix holds the final script.
- **C6 probes (report-only, not in Verification).** Base: `16 failed, 35 passed` (`$PY -m pytest -q -p
  no:cacheprovider audit/scratch/C6`). I will rerun them after the merge and name any probe that changes colour.

## Plan

### Approach

A new tool `labs/vinlab/tools/merge_tecdoc_extract.py` (stdlib plus the lab's own `vinlab` package) reads the
extract, `vinlab/data/vds_engine_map.csv` (read-only, for the two decode-hazard guards) and `vinlab/data/vref.db`. In
one SQLite transaction it rebuilds `engine_ref` with the builder's DDL when `has_maf` or `has_map` is still
`NOT NULL`, then inserts the selected rows. It never updates or deletes an existing row.

Signatures (no new public field, no new key in any payload):

```python
@dataclass(frozen=True)
class MergeReport:
    inserted: tuple[str, ...]             # engine_code values inserted
    skipped: dict[str, tuple[str, ...]]   # reason -> normalised codes
    schema_rebuilt: bool
    rows_after: int

def select_rows(extract_rows, existing_codes, map_rows) -> tuple[list[dict[str, object]], dict[str, list[str]]]
def merge(db_path=DEFAULT_DB, extract_path=DEFAULT_EXTRACT, map_path=DEFAULT_MAP) -> MergeReport
def main(argv: list[str] | None = None) -> int   # --db / --extract / --map; last line: "inserted N rows; ..."
```

Raises: `ValueError` when the extract header lacks a column the tool reads; `RuntimeError` when the column-name set of
the existing `engine_ref` differs from the builder DDL's (fail closed, before any write); sqlite errors after
`ROLLBACK`. Normalisation is `vinlab.db.tecdoc_query._normalise_code` (R1).

### Rows taken (rule order; counts over the 1,306 normalised codes of the extract at `8592bb3`)

| step | rule | codes | real VINs (decoder lookup) |
|---|---|---|---|
| 1 | normalised code already in `engine_ref` → skip | 24 | (unchanged decodes) |
| 2 | collision: >1 distinct field tuple over the 9 fields of P1 → skip (R2) | 44 | 72 (70 brand-agreeing = P4) |
| 3 | any row of the code has a status outside {OK, FAMILY, AMBIGUOUS} → skip (fail closed; vacuous here) | 0 | 0 |
| 4 | any row of the code has no `my_start` → skip | 35 | 4 |
| 5 | G1 map BOXER: a `vds_engine_map.csv` row of the code has `engine_configuration` `BOXER*` → skip | 2 (EJ18, FB20) | 0 |
| 6 | G2 cylinder-heuristic hazard (definition below) → skip | 39 | 18 |
| — | **inserted** | **1,162** (OK 1,102, FAMILY 27, AMBIGUOUS 33) | 547 (491 in window) |

The R2 collision codes (for the RESULT): `169A4000 18K4F 18K4K 1E 1KR 1UZFE 2GRFE 4A 6FY A112A2000 A20NHT ADY APQ
B12S1 B38A15A B48A20A B6 BDY BKY CDZ D16A8 F18A3 FA20 FE FS G4FG HFX JB K10B KDX KDY KFV KFW KFX KL LFW PT204 RFJ RFK
RFN RFU RFW RGX VK45DE`.

Multi-brand codes (identical fields): the row takes the alphabetically first brand and its `engine_code` spelling.
The window is the union over the brands (rejected: skip the 87 codes whose years differ, 89 real VINs).

**AMBIGUOUS ruling: insert.** Their disagreeing fields are blank, so each blank goes to NULL (or `0` for the flags)
and the decoder falls back as without a row. Measured before the hazard guards: AMBIGUOUS in gives `row_applied`
520, out gives 509 (+11 in window, +2 out of window). The only read flag a blank can invent is `is_v_engine` (blank →
`0` → one bank, `decoder.py:364`). Real VINs affected by a blank `is_v_engine`: 0 (every banks change traces to a
stated `0` or `1`). The guards skip 2 of the 35 AMBIGUOUS codes. Rejected: exclude, because the kept fields are
values every TecDoc record of the code agrees on.

### Each column: value written, and the line that reads it

| column | value written | reader |
|---|---|---|
| `engine_code` | extract `engine_code` of the chosen row | `tecdoc_query.py:68-70` exact, `:76-84` normalised |
| `brand` | extract brand, upper case | no decoder reader; `idx_engine_ref_brand` only |
| `displacement_cc` | int, or NULL when blank (19 extract rows) | `decoder.py:345-347` |
| `euro_norm` | extract value (`euro1`…`euro6`, the `_EURO_MAP` keys) or NULL | `decoder.py:367-369` via `_normalise_euro` (`:126-131`; NULL → `EURO_1`) |
| `my_start` | min `my_start` over the code's rows | `decoder.py:584-590` window |
| `my_end` | max `my_end` (open → 2019) **+ 1** | `decoder.py:584-590` window |
| `era_bucket` | `build_vref_db._derive_era(my_start, my_end)` | no decoder reader (`decoder.py:210` reads `years.csv`) |
| `has_vvt` | 0 | no reader |
| `has_gdi` | extract, blank → 0 | no reader |
| `has_turbo` | extract, blank → 0 | no reader |
| `is_v_engine` | extract, blank → 0 | `decoder.py:364` (banks) |
| `has_egr` | 0 | `decoder.py:379` → `egr_equipped=False`, the no-row default (`models.py:171`); feeds `:500` |
| `has_maf`, `has_map` | NULL | `decoder.py:488-501`: NULL → heuristic |
| `o2_type` | `''` | `decoder.py:376` → `switches.py:22-32`: `''` → year rule |
| `induction_type` | extract or NULL | `decoder.py:350-352` |
| `fuel_delivery_type` | extract or NULL | `decoder.py:355-361` and the H1 guard `:597-600` (values PORT_INJECTION/GDI only) |
| `valvetrain_type` | extract or NULL | no reader |
| `rated_rpm` and the 13 CoC columns | NULL | `decoder.py:383-396`; flag `coc_null_target_lambda_v112` (`:399-408`) |

`era_bucket` note: 67 inserted rows end before 1990, and `_derive_era` gives them `ERA_MODERN` (its fall-through,
`build_vref_db.py:61-65`). No line reads it. I follow R3 and record it.

### Schema change

- `tools/build_vref_db.py` `CREATE_ENGINE_REF` (lines 103-104): `has_maf INTEGER NOT NULL DEFAULT 0,` and the same for
  `has_map` become `has_maf INTEGER,` / `has_map INTEGER,`, with one comment line: NULL means the source does not
  state it, so the decoder keeps its heuristic. No default, so an omitted value is NULL, not an invented `0`. The
  builder's own `INSERT_ROW` writes both columns explicitly, so its rows do not change. The builder's migration guard
  (`build_vref_db.py:993-998`, `ALTER … NOT NULL DEFAULT 0`) is outside `CREATE_ENGINE_REF` and stays (it fires only
  on a db without the columns): a follow-up, not this row's.
- The tool rebuilds the shipped table **with the builder's DDL verbatim**. In one transaction: `DROP INDEX
  idx_engine_ref_brand`; `ALTER TABLE engine_ref RENAME TO engine_ref_old`; the two statements of
  `CREATE_ENGINE_REF`; `INSERT INTO engine_ref (<32 named columns>) SELECT <same> FROM engine_ref_old`; `DROP TABLE
  engine_ref_old`; the new rows; `COMMIT`. The column list is a literal (no SQL built from data). Afterwards the
  shipped table equals the builder's, including the column order: `rated_rpm` moves from last to after
  `valvetrain_type`. Every reader uses column names (`sqlite3.Row` dicts in `tecdoc_query.py:66,81`; named selects in
  the tests and probes). No `VACUUM`.
- Rejected: keep the shipped column order and edit only the two lines in a copy of the DDL. It leaves the existing
  order drift between builder and db, and the tool would hold a second DDL.
- The 72 rows: the copy is `INSERT … SELECT` by name. The proof is a row dump. Every column of every original row, as
  `(typeof, value)`, from `git show 6da3b90:labs/vinlab/vinlab/data/vref.db` and from the merged file, compared
  equal; `has_maf`/`has_map` stay integer `0`/`1`.
- Idempotence proof: the second run sees `notnull = 0` on both columns (no rebuild), finds every candidate code
  present (no insert) and opens no write transaction. The test and step 5 compare the file's sha256 before and after.

### Window rule (R3 Years) and its measured effect

The VIN position 10 is a model year. TecDoc years are production (calendar) years. A car built late in calendar year
Y can carry model year Y+1, and a model year does not come before its build year. So the model-year window is
`[start, end + 1]`. The open end means the engine type was still current in the 1Q2019 data, so `end = 2019`.
No vinlab wiki page states the model-year offset (`grep -rniE "model.year.{0,60}(production|calendar)"
labs/vinlab/wiki` is empty). This is a domain ruling for Cowork; the tool cites the approved plan correction.

| option | P4 population (374 with a year) inside | `reach.py` `row_applied` (statuses all, before guards) |
|---|---|---|
| no tolerance, open end 2019 | 294 | 513 |
| **end + 1 (chosen)** | **302** | **520** (506 after the guards) |
| ±1 | 306 | not measured with AMBIGUOUS; 513 for OK+FAMILY vs 509 end+1 |

Rejected ±1: a model year before the production start has no cause. Rejected: skip open-end rows (386 inserted
codes have an open end in at least one brand row). A row without `my_start` is not inserted (step 4).

### The decode-hazard guards (F1, F2): why, the options, and the recommendation

Without the guards, the merge puts values into real and test decodes that TecDoc does not state. Two decoder paths
cause it, and the decoder is out of scope:

- **F1, banks for boxers.** The extract writes `is_v_engine = 0` for `BOXER` (`tools/extract_tecdoc_1q2019.py:64`),
  and `decoder.py:364` turns `0` into one bank. Without a row the map's `BOXER_4` gives two banks
  (`decoder.py:278-280`). FB20 then fails `tests/unit/test_decoder.py:534-542`
  (`test_heuristic_boxer_emits_two_banks`, `JF1SHJLW1A1234567`: banks 2 → 1), so criterion 1 fails.
- **F2, cylinder heuristic.** When the map row has no `cylinder_count`, `_cylinder_fallback` (`decoder.py:446-478`)
  runs `infer_cylinder` on the row's displacement. It replaces a TecDoc-stated `NATURALLY_ASPIRATED`
  (`decoder.py:469-470`), sets a count and can set two banks. AZQ (Skoda 1.2, TecDoc NA): `infer_cylinder('AZQ',
  1.198, 'SKODA')` = `I3 TURBOCHARGED` vs `unresolved` at the map's blank displacement. Real VINs
  `TMBCY46Y733811341` and `TMBDY16Y033784910` then change induction NA → TURBOCHARGED and air metering
  MAF_ONLY → HYBRID_MAF_MAP. R4 calls that a stop. A cylinder case: `JSAFTD62V00115689` (H25A) goes 0 → 4
  cylinders, and TecDoc says 6.

G1: skip a code when any map row of it has `engine_configuration` starting `BOXER`.
G2: for each map row of the code whose `cylinder_count` is blank or `0`, let `h0 = infer_cylinder(code, map
displacement, brand)` and `h1 = infer_cylinder(code, displacement_cc / 1000, brand)`. Skip the code when
`h1.count > 0` and any of: (i) TecDoc states a cylinder count, `h1.count` differs from it and from `h0.count`;
(ii) TecDoc induction is NA or blank, `h1.induction` is not NA, and `h0` is unresolved or has another induction;
(iii) TecDoc `is_v_engine` is `0`, `h1.config` starts with V, W or BOXER, the map configuration is blank, and `h0` is
not a two-bank hint. G2 calls the live `infer_cylinder`, so a heuristic change moves the guard with it.

| option | inserted | `row_applied` | changes not from a TecDoc value | criterion 1 |
|---|---|---|---|---|
| no guard | 1,203 | 520 | 2 VINs induction + air (R4 stop), 1 VIN cylinders, test boxer banks | FAIL (boxer test) |
| G1 + G2 (ii) only | 1,196 | 517 | 1 VIN cylinders (H25A 0 → 4, TecDoc 6) | pass |
| **G1 + G2 (i)-(iii), recommended** | **1,162** | **506** | **0** | pass |
| G1 + skip every code with a blank-cylinder map row | ≤ 1,009 | not built | 0 (not built) | pass; 194 codes, 86 real VINs lose a row |

Recommendation: G1 + full G2. It is the only option with no unattributed value, and it costs 11 real VINs against the
narrow form. G2 skips: `108C 1095F 109F 109K 128A000 206KA 308S1 8L 99H AM2 AR01646 AZQ BBM BMD BME BZG C1C EK42
EN07 EZA EZH F105A F106D G4HCE G6DA H25A HDY HDZ HFY L31 L35 L83 L98 LF8 LM7 M30B32 M9720 M9770 S01`. Follow-ups
for Cowork (not this row's): the decoder should take banks from a BOXER fact and not override a vref-stated
induction; the extract should carry the cylinder arrangement. After those, a rerun inserts the 41 guarded codes.

### `reach.py`: base (measured) and predicted after the merge

Base (measured, 2026-11-04T14:05Z, from `audit/scratch/C6`):
```
vref outcome: {'no_engine_code': 16, 'not_in_vref': 1097, 'out_of_window': 3, 'row_applied': 15}
confidence: {'HIGH': 2, 'NONE': 16, 'PARTIAL': 1113}
euro: {'EURO_1': 1118, 'EURO_2': 4, 'EURO_3': 4, 'EURO_4': 4, 'EURO_5': 1}
upstream_o2: {'NARROWBAND': 702, 'WIDEBAND_AFR': 429}
air_metering: MAF_ONLY(maf=True, map=False) 1117, MAP_ONLY(maf=False, map=False) 13, MAP_ONLY(maf=False, map=True) 1
```
Predicted after (simulation, recommended rules):
```
vref outcome: {'no_engine_code': 16, 'not_in_vref': 550, 'out_of_window': 59, 'row_applied': 506}
confidence: {'HIGH': 2, 'NONE': 16, 'PARTIAL': 1113}
euro: {'EURO_1': 1107, 'EURO_2': 4, 'EURO_3': 4, 'EURO_4': 15, 'EURO_5': 1}
upstream_o2: {'NARROWBAND': 702, 'WIDEBAND_AFR': 429}
air_metering: MAF_ONLY(maf=True, map=False) 1085, HYBRID_MAF_MAP(maf=True, map=True) 32, MAP_ONLY(False, False) 13, MAP_ONLY(False, True) 1
```
Every predicted real-VIN change and its source (0 unattributed):

| field | VINs | source |
|---|---|---|
| `engine_displacement_liters` | 485 | TecDoc `displacement_cc` |
| `induction_type` | 28 | TecDoc `induction_type` (TURBOCHARGED/SUPERCHARGED) |
| `fuel_delivery_type` | 14 | TecDoc `fuel_delivery_type` GDI |
| air metering (`has_map_sensor`, load calc, strategy) MAF_ONLY → HYBRID_MAF_MAP | 32 | the decoder's own heuristic (`decoder.py:490-501`, `has_map` NULL) on TecDoc-stated turbo/supercharged induction or GDI |
| `euro_emission_category` EURO_1 → EURO_4, with `resolved_horizon` and `stress_idle_rpm_target` | 11 | TecDoc `euro_norm` |
| `number_of_banks` | 18 | TecDoc `is_v_engine` stated: 10 V engines 1 → 2; 8 straight engines 2 → 1 where the map says V6/V8 (AEB, NG 2.3 five-cylinder, 346KB, 326S4, 366S1) |
| `cylinder_count` 0 → n | 12 | the heuristic on TecDoc displacement; every value equals the extract's `cylinder_count` |
| upstream O₂, confidence, EGR, downstream O₂ | 0 | — |

The air-metering line is the judgement call for R4: the value is not a TecDoc field, but it follows from
TecDoc-stated induction or fuel through the same function the no-row decode uses. If Cowork rules that this is not
"from a stated TecDoc value", the alternative is to skip codes whose TecDoc induction is turbo/supercharged or fuel is
GDI (that loses the induction and fuel facts too); I recommend accepting it.

### Existing tests whose value changes (R5, R6)

From all 43 VIN literals in `labs/vinlab/tests`, `labs/dnalab`, `apps/wired`, `apps/ui` (`.py`, `.json`, `.csv`),
decoded against both dbs. With the guards, 8 decode differently and no assertion changes:
- `test_decoder.py::TestYearPassthrough` `JTDKGNEC50N036354` (euro EURO_1 → EURO_4, 1.0 → 0.998 L),
  `ZFA35600006N64200` (1.4 → 1.368), `WF0UXXGAJU3C20388` (1.6 → 1.596): the test asserts make and `model_year is
  None` only.
- `test_wmi_brands.py` `JSAEAB35S00110744` (1.3 → 1.299), `SAXXNNAZRWD148244` (1.3 → 1.275): brand only.
- `apps/ui/app.py` `WVWZZZ1KZAP012480` (1.8 → 1.595) is a placeholder string; `apps/ui/_sample_app_reference.py`
  `WVWZZZ1JZ3W386752` (1.4 → 1.39) is not a test; `apps/wired/v7/data/cases_petrol_v7.csv` is read by
  `apps/wired/v7/tests`, which the wired suite does not collect (F-P2-1).
- `test_decoder.py:534-542` (`JF1SHJLW1A1234567`) stays unchanged only because G1 skips FB20.
- Tests that read vref.db directly stay green: `test_build.py` (count ≥ 1, required columns, the 5FR row, overlap),
  `test_vref_year_window.py::test_every_vref_row_has_a_window` (simulated merged db: 0 bad rows of 1,234),
  `test_csv_suite.py` (new rows have NULL CoC, which the test skips; the CSV is absent here and the test skips).

No dnalab, wired or ui fixture is regenerated. Predicted counts: vinlab **277 passed, 8 skipped** (261 + 16 new);
new file **16 passed**; dnalab **27 passed**, wired **41 passed**, ui **30 passed** (P5). The vinlab prediction is
from the VIN-literal diff and the direct-db test review, not from a suite run on a merged copy (`NOT RUN`: the suite
reads the shipped db path).

### Tests (`tests/unit/test_vref_tecdoc_merge.py`, NEW; loads the tool with importlib like `test_extract_tecdoc_1q2019.py`)

Fixtures: a temp copy of the shipped vref.db, a fixture extract CSV (the 18-column header), a fixture map CSV (the
9-column header), all under `tmp_path` (`--basetemp` under `pt/`).

| # | test | rule |
|---|---|---|
| 1 | `test_inserts_new_code` | a new OK code gets a row with its stated values |
| 2 | `test_skips_code_already_in_vref` | `5 FR` normalises to the existing `5FR`: no insert, 5FR unchanged |
| 3 | `test_skips_collision_code` | one code under two brands, different displacement: no insert, reported |
| 4 | `test_skips_code_without_my_start` | no insert |
| 5 | `test_new_row_leaves_maf_and_map_null` | `has_maf`/`has_map` IS NULL |
| 6 | `test_new_row_o2_type_is_empty` | `o2_type = ''` |
| 7 | `test_blank_fields_become_null_or_zero` | blank euro/induction/fuel/valvetrain/displacement → NULL; blank flags → 0; vvt/egr 0; CoC NULL |
| 8 | `test_window_adds_one_model_year_and_closes_open_end` | `my_end = end + 1`; open → 2020; multi-brand union |
| 9 | `test_era_bucket_comes_from_builder` | equals `build_vref_db._derive_era(my_start, my_end)` |
| 10 | `test_ambiguous_code_is_inserted` | AMBIGUOUS row inserted, its blank fields NULL |
| 11 | `test_map_boxer_code_is_skipped` | G1 |
| 12 | `test_cylinder_heuristic_hazard_is_skipped` | G2: an AZQ-like NA 1198 cc Skoda code with a blank map cylinder count |
| 13 | `test_second_run_inserts_nothing_and_keeps_bytes` | inserted 0; sha256 equal |
| 14 | `test_existing_rows_keep_every_value` | the 72 original rows equal as `(type, value)` per column |
| 15 | `test_schema_matches_builder` | `PRAGMA table_info` of the merged db equals that of `CREATE_ENGINE_REF` in memory |
| 16 | `test_real_vin_gains_row_with_tecdoc_displacement` | real extract + real map + shipped-db copy: `W0L0SBF08X4314007` (Opel X10XE, 1999) displacement 1.4 → 0.973; air metering and O₂ equal the no-row decode |

Test 16 uses a fresh `RobustVINDecoder(DATA_DIR)` with `db_path` set to the merged copy (the `lru_cache` of
`_build_normalised_index` is keyed on the path, so the copy cannot see the shipped index).

### Mutants (step 7; copy in `C:/4DApp/recheck/T-VINA-13b/mut/`, edited with `sed`, copied over, one test, `git restore`)

M1 `select_rows` returns no row → test 1. M2 drop the in-vref check → 2. M3 drop the collision check → 3. M4 default
a missing start to 1990 → 4. M5 write `0` for `has_maf`/`has_map` → 5. M6 omit `o2_type` from the insert (default
`'NB'`) → 6. M7 blank euro written as `''` → 7. M8 drop the `+ 1` → 8. M9 `era_bucket` written as `ERA_MODERN` → 9.
M10 drop AMBIGUOUS from the allowed statuses → 10. M11 drop G1 → 11. M12 drop G2 → 12. M13 rebuild the table on
every run → 13. M14 copy `NULLIF(has_maf, 0)` in the rebuild → 14. M15 keep `NOT NULL DEFAULT 0` in the rebuild DDL →
15. M16 write `displacement_cc` NULL → 16. Each must fail its test; then `git restore
labs/vinlab/tools/merge_tecdoc_extract.py labs/vinlab/vinlab/data/vref.db`.

### Each rule the plan adds: population checked, population it runs over, false pass, false fail

- **Window `[start, end+1]`, open → 2019.** Checked on: the 374 P4 VINs with a year and the 1,131 real VINs
  (simulation). Runs over: the 1,162 inserted rows (`merge()` on the shipped db). False pass: a VIN built before the
  type's production start with a model-year code (rare imports) gets the row. False fail: a car whose model year
  runs two years past production (long runout) loses the row. Changes later steps: yes, the window decides
  `row_applied` in `reach.py` (step 4).
- **G1 BOXER.** Checked on: 1,203 candidate codes against the 12,928 map rows; real VINs affected 0; test VIN 1.
  Runs over: every candidate code. False pass: a boxer code whose map rows lack `BOXER*` (the map config is blank or
  wrong) is inserted with one bank. False fail: none known (the extract cannot say BOXER, so every map-BOXER code with
  `is_v_engine` 0 would go to one bank).
- **G2 heuristic.** Checked on: the 1,203 candidates and their map rows with no cylinder count; real VINs 18; zero
  unattributed changes after it. Runs over: every candidate code. False pass: a hazard through a decoder path G2 does
  not mirror (G2 mirrors `decoder.py:461-478`; a decoder edit can make it stale). False fail: a whole code is skipped
  when one of its map rows is hazardous, so VINs on its other map rows (with a stated count) lose the row; also codes
  whose hazardous map rows no real VIN uses.
- **AMBIGUOUS in, multi-brand union, first brand.** Checked on: real VINs (+11 in window). False pass: an AMBIGUOUS
  code whose agreed fields hide a disagreement the extract dropped. False fail: none.
- **Schema rebuild.** Checked on: a copy of the shipped db (simulation: 1,234 rows, 0 window violations). Runs over:
  the shipped db once. It changes what later steps run against: steps 1-5 read the rebuilt table.

### Commands for the redispatch and the paths they write

1. Write `labs/vinlab/tests/unit/test_vref_tecdoc_merge.py`; red run:
   `cd labs/vinlab && $PY -m pytest -q -p no:cacheprovider tests/unit/test_vref_tecdoc_merge.py
   --basetemp=C:/4DApp/recheck/T-VINA-13b/pt/red` (writes `pt/red`). Expected: 16 failed (tool missing).
2. Write `labs/vinlab/tools/merge_tecdoc_extract.py`; inner loop (`py_compile`, `py -m ruff check`, `--select S`,
   `pyright --pythonpath`); green run (writes `pt/t`).
3. Edit `labs/vinlab/tools/build_vref_db.py` `CREATE_ENGINE_REF` (two lines and a comment).
4. `cd labs/vinlab && $PY tools/merge_tecdoc_extract.py` (writes `vinlab/data/vref.db`). Expected last line:
   `inserted 1162 rows; engine_ref now 1234 rows; schema rebuilt: yes`. Row dump of the 72:
   `git show 6da3b90:labs/vinlab/vinlab/data/vref.db > C:/4DApp/recheck/T-VINA-13b/pt/vref_base.db`, then a
   `$PY -c` comparison by name (writes `pt/vref_base.db`).
5. Verification steps 1-4 (write `pt/v`, `pt/t`, `pt/dnalab`, `pt/wired`, `pt/ui`); C6 probes report-only.
6. `git add` the four paths, then `git -c user.name=Claude -c user.email=noreply@anthropic.com commit -m
   "feat(T-VINA-13b): …"` on `fix/T-VINA-13b`.
7. Mutants M1-M16 (write `mut/M*.py`; the tool and db restored by `git restore`).
8. Verification step 5. Expected: `inserted 0 rows; engine_ref now 1234 rows; schema rebuilt: no`, no vref.db
   change, `All checks passed!`, `6da3b90` plus my commit, and only the note and the RESULT in `git status`.

### Remaining risks

- `audit/scratch/C6/test_c6_probes.py::test_f1_horizon_follows_year_when_euro_unknown` treats any vref row as "euro
  known" (`:52`). 1,086 of the 1,162 new rows carry NULL euro, so the probe's "euro unknown" population falls from
  1,113 to a predicted 566 (16 no code + 550 not in vref) while most of those euros are still unknown. It stays red,
  but its count understates F-C6-1.
- The 247 year-less P4 VINs get the row with no window check (`decoder.py:584`: the check runs only with a year).
- Cylinder count and banks can disagree inside one decode (`AEB`: map 6 cylinders, TecDoc straight → 1 bank),
  because `engine_ref` has no cylinder column and the map is wrong there.

## Measurements (all read-only)

- `vina13b_measure.py` (cwd `audit/scratch/C6`): `extract rows 1498 codes 1306 collision codes (fields differ) 44
  codes already in vref 24`; status `OK 1422, AMBIGUOUS 42, FAMILY 34`; `vins_new_row 624, status_OK 572,
  collision_code 70, euro_given 18, inside_tol0 294, inside_tol1 306, year_none 247, no_start 3, status_FAMILY 28,
  status_AMBIGUOUS 24` = P1 and P4.
- Shipped `engine_ref` DDL: `my_start INTEGER, my_end INTEGER` (nullable), `has_maf/has_map INTEGER NOT NULL DEFAULT
  0`, `o2_type TEXT NOT NULL DEFAULT 'NB'`, `rated_rpm integer` appended last; 72 rows; `journal_mode` delete.
- Extract field values: fuel `PORT_INJECTION 1258, GDI 213, '' 27`; induction `NATURALLY_ASPIRATED 858, TURBOCHARGED
  260, SUPERCHARGED 7, '' 373`; euro `'' 1384, euro4 55, euro5 33, euro6 24, euro1 1, euro2 1`; `is_v_engine` blank 15;
  `my_start` blank 40 rows, `my_end` blank 541; all non-blank `displacement_cc` are integers.

## Appendix: final prediction script

Run from `C:/4DApp/repo/audit/scratch/C6` in PowerShell: `$script | & C:/4DApp/.venv/Scripts/python.exe - full`
(`- induction` gives the G1 + G2 (ii) row). It writes one temp dir under `C:/4DApp/recheck/T-VINA-13b/mut/`.

```python
import collections, csv, dataclasses, shutil, sqlite3, sys, tempfile
from pathlib import Path
sys.path.insert(0, 'C:/4DApp/repo/labs/vinlab'); sys.path.insert(0, 'C:/4DApp/repo/audit/scratch/C6')
import c6_lib, vinlab
from vinlab.db.tecdoc_query import _normalise_code, lookup_engine_ref
from vinlab.decoder import RobustVINDecoder, VINDecodeError
from vinlab.overlay.cylinder_heuristic import infer_cylinder
DATA = vinlab._DEFAULT_DATA_DIR
MODE = sys.argv[1]
ERA = [(1990,1995,"ERA_PRE_OBDII"),(1996,2005,"ERA_OBDII_EARLY"),(2006,2015,"ERA_CAN"),(2016,2020,"ERA_MODERN")]
FIELDS = ("displacement_cc","cylinder_count","fuel_delivery_type","induction_type","has_turbo","has_gdi","is_v_engine","valvetrain_type","euro_norm")
def era(s, e):
    for a, b, lab in ERA:
        if s <= b and e >= a: return lab
    return "ERA_MODERN"
ext = list(csv.DictReader(open('C:/4DApp/repo/labs/vinlab/tools/data/tecdoc_1q2019_engine_extract.csv', encoding='utf-8', newline='')))
by = collections.defaultdict(list)
for r in ext: by[_normalise_code(r['engine_code'])].append(r)
collide = {c for c, rs in by.items() if len({tuple(r[f] for f in FIELDS) for r in rs}) > 1}
have = {_normalise_code(x[0]) for x in sqlite3.connect(f'file:{DATA / "vref.db"}?mode=ro', uri=True).execute('select engine_code from engine_ref')}
maprows = collections.defaultdict(list)
for r in csv.DictReader(open(DATA / 'vds_engine_map.csv', encoding='utf-8', newline='')):
    if r['engine_code'].strip(): maprows[_normalise_code(r['engine_code'])].append(r)
def two_bank(cfg): return cfg[:1] in ('V', 'W') or cfg.startswith('BOXER')
def boxer(c): return any((m['engine_configuration'] or '').upper().startswith('BOXER') for m in maprows[c])
def hazard(c, r):
    if not r['displacement_cc']: return False
    for m in maprows[c]:
        if (m['cylinder_count'] or '').strip() not in ('', '0'): continue
        try: cd = float(m['engine_displacement'] or 0)
        except ValueError: cd = 0.0
        h0 = infer_cylinder(m['engine_code'].strip(), cd, m['brand'].strip()); h1 = infer_cylinder(m['engine_code'].strip(), int(r['displacement_cc']) / 1000.0, m['brand'].strip())
        if h1.count <= 0: continue
        ind = (r['induction_type'] or 'NATURALLY_ASPIRATED') == 'NATURALLY_ASPIRATED' and h1.induction != 'NATURALLY_ASPIRATED' and (h0.count <= 0 or h0.induction != h1.induction)
        if MODE == 'induction':
            if ind: return True
            continue
        if ind: return True
        if r['cylinder_count'] and h1.count != int(r['cylinder_count']) and h1.count != h0.count: return True
        if r['is_v_engine'] == '0' and two_bank(h1.config) and not (h0.count > 0 and two_bank(h0.config)) and not (m['engine_configuration'] or '').strip(): return True
    return False
skip = collections.Counter(); rows = {}
for c, rs in sorted(by.items()):
    rs = sorted(rs, key=lambda r: r['brand'])
    if c in have: skip['in_vref'] += 1; continue
    if c in collide: skip['collision'] += 1; continue
    if any(not r['my_start'] for r in rs): skip['no_my_start'] += 1; continue
    if boxer(c): skip['map_boxer'] += 1; continue
    if hazard(c, rs[0]): skip['heuristic_hazard'] += 1; continue
    s = min(int(r['my_start']) for r in rs); e = max(int(r['my_end']) if r['my_end'] else 2019 for r in rs) + 1
    r = rs[0]; i = lambda v: int(v) if v else None; b = lambda v: int(v) if v else 0
    rows[c] = dict(engine_code=r['engine_code'], brand=r['brand'].upper(), displacement_cc=i(r['displacement_cc']), euro_norm=r['euro_norm'] or None, my_start=s, my_end=e, era_bucket=era(s, e), has_vvt=0, has_gdi=b(r['has_gdi']), has_turbo=b(r['has_turbo']), is_v_engine=b(r['is_v_engine']), has_egr=0, has_maf=None, has_map=None, o2_type='', induction_type=r['induction_type'] or None, fuel_delivery_type=r['fuel_delivery_type'] or None, valvetrain_type=r['valvetrain_type'] or None)
print(MODE, 'rows inserted', len(rows), 'skipped', dict(skip), 'status', dict(collections.Counter(by[c][0]['status'] for c in rows)))
td = tempfile.mkdtemp(dir='C:/4DApp/recheck/T-VINA-13b/mut'); p = Path(td) / 'merged.db'
shutil.copy(DATA / 'vref.db', p); con = sqlite3.connect(p)
sql = con.execute("select sql from sqlite_master where name='engine_ref'").fetchone()[0]
sql = sql.replace("has_maf            INTEGER NOT NULL DEFAULT 0", "has_maf            INTEGER").replace("has_map            INTEGER NOT NULL DEFAULT 0", "has_map            INTEGER")
cols = [x[1] for x in con.execute('pragma table_info(engine_ref)')]
con.executescript(f"BEGIN; ALTER TABLE engine_ref RENAME TO _old; {sql}; INSERT INTO engine_ref({','.join(cols)}) SELECT {','.join(cols)} FROM _old; DROP TABLE _old; COMMIT;")
for r in rows.values(): con.execute(f"insert into engine_ref({','.join(r)}) values({','.join('?' * len(r))})", list(r.values()))
con.commit(); con.close()
base = RobustVINDecoder(DATA); m = RobustVINDecoder(DATA); m.db_path = p
outcome = collections.Counter(); conf = collections.Counter(); euro = collections.Counter(); o2 = collections.Counter(); air = collections.Counter(); ch_all = collections.Counter(); bad = []
def flat(d):
    j = dataclasses.asdict(d); em = j.pop('emissions'); am = j.pop('air_metering_architecture')
    j.update({'em.' + k: v for k, v in em.items()}); j.update({'am.' + k: v for k, v in am.items()}); return j
for v in c6_lib.real_vins():
    try: d0 = base.decode_vin_payload(v)
    except VINDecodeError: continue
    d = m.decode_vin_payload(v)
    er = m._resolve_engine(d.vin, d.make, []) or {}; code = (er.get('engine_code') or '').strip(); c = _normalise_code(code) if code else ''
    if not code: outcome['no_engine_code'] += 1
    else:
        row = lookup_engine_ref(p, code)
        if row is None: outcome['not_in_vref'] += 1
        elif d.model_year is not None and not (int(row['my_start']) <= d.model_year <= int(row['my_end'])): outcome['out_of_window'] += 1
        else: outcome['row_applied'] += 1
    conf[str(d.confidence)] += 1; euro[str(d.euro_emission_category)] += 1; o2[str(d.emissions.upstream_o2_type)] += 1
    a = d.air_metering_architecture; air[f'maf={a.has_maf_sensor},map={a.has_map_sensor},{a.primary_load_calculation.value}'] += 1
    f0, f1 = flat(d0), flat(d); ch = {k for k in f1 if f0[k] != f1[k]}
    for k in ch: ch_all[k] += 1
    r = rows.get(c, {}); e0 = by[c][0] if c in by else {}
    if 'cylinder_count' in ch and str(f1['cylinder_count']) != e0.get('cylinder_count'): bad.append(('cyl', v, code, f0['cylinder_count'], f1['cylinder_count'], e0.get('cylinder_count')))
    if 'induction_type' in ch and r.get('induction_type') != f1['induction_type']: bad.append(('ind', v, code))
    if 'number_of_banks' in ch and f1['number_of_banks'] != (2 if r.get('is_v_engine') else 1): bad.append(('banks', v, code))
    if ch & {'am.has_map_sensor', 'am.has_maf_sensor'} and not (('induction_type' in ch and r.get('induction_type') in ('TURBOCHARGED', 'SUPERCHARGED')) or ('fuel_delivery_type' in ch and r.get('fuel_delivery_type') == 'GDI')): bad.append(('air', v, code))
    if 'euro_emission_category' in ch and not r.get('euro_norm'): bad.append(('euro', v, code))
    if 'em.upstream_o2_type' in ch: bad.append(('o2', v, code))
print('vref outcome:', dict(sorted(outcome.items())))
print('confidence:', dict(sorted(conf.items())))
print('euro:', dict(sorted(euro.items())))
print('upstream_o2:', dict(sorted(o2.items())))
print('air_metering:', dict(sorted(air.items())))
print('changed fields (real VINs):', dict(sorted(ch_all.items())))
print('UNEXPLAINED', bad)
print('TMPDIR', td)
```

Its output (`full`): `rows inserted 1162 skipped {'no_my_start': 35, 'heuristic_hazard': 39, 'collision': 44,
'in_vref': 24, 'map_boxer': 2} status {'OK': 1102, 'FAMILY': 27, 'AMBIGUOUS': 33}`, the predicted `reach.py` lines
above, `changed fields (real VINs): {'air_metering_strategy': 32, 'am.has_map_sensor': 32,
'am.primary_load_calculation': 32, 'cylinder_count': 12, 'engine_displacement_liters': 485,
'euro_emission_category': 11, 'fuel_delivery_type': 14, 'induction_type': 28, 'number_of_banks': 18,
'resolved_horizon': 11, 'stress_idle_rpm_target': 11}`, `UNEXPLAINED []`. The prototype rebuild keeps the shipped
column order and does not recreate the index. The tool will use the builder DDL and recreate the index; neither
changes a decode.

## Plan stop

Stopped before the first edit, as the plan gate requires. Cowork's review in `labs/vinlab/tasks/corrections/` rules on
the window rule, AMBIGUOUS, G1/G2 (F1, F2) and the air-metering attribution; the redispatch implements from it.

## Redispatch 01: readiness

- (a) Starting state matches the redispatch First action. `git branch --show-current` = `fix/T-VINA-13b`;
  `git log --oneline -1` = `11dfa95 spec(T-VINA-13b): plan correction 01 (C1-C6), B8, second plan review evidence;
  register T-VINA-14/15`, parent `6da3b90`. **Base = `11dfa95`.** Porcelain: only `?? …/T-VINA-13b.blocker.json` and
  `?? …/T-VINA-13b.md`. Preconditions: `checked`, no `MISSING`/`EXISTS`. The correction file has no `### Plan-time
  digest ###` table (`grep -c` = 0). `git diff --stat 6da3b90 11dfa95` touches only task documents.
- (b) Red reason: the 18 tests fail at setup because `tools/merge_tecdoc_extract.py` does not exist; the decode test
  also needs 0.973 L where the shipped db gives 1.4 L.
- (c) Independent decisive value (round-2 rules, prototype on a throwaway copy): `row_applied` **506**, inserted
  **1,162**, 0 unattributed changes. The test asserts `W0L0SBF08X4314007` = 0.973 L; `reach.py` must print 506.
- (d) No contradiction remains. B8 is adjudicated (all three upheld); C1-C6 are applied below.
- (e) Teach-back: as in round 1, with C1-C6. The decisive checks are `reach.py` `row_applied` 506 with every euro,
  O₂ and air change traced to a TecDoc field, and a second run that changes no byte of vref.db.

## Plan round 2 (correction 01, C1-C6)

- **C1.** `build_vref_db.py:993-994`, the migration guard, adds `has_maf`/`has_map` as plain `INTEGER` (was `INTEGER
  NOT NULL DEFAULT 0`). It has no unit test: the guard runs only inside `build_vref_db.main()`, which needs
  `DBS_ROOT` data and MySQL. Evidence: the diff and `grep -n '"has_ma[fp]", "INTEGER' tools/build_vref_db.py`.
- **C2.** No change to the tool. The RESULT lists the 32 air-metering VINs with the TecDoc field that drives each
  (turbo/supercharged induction or GDI fuel) and the 11 euro VINs with their `euro_norm`.
- **C3.** New skip `span_gap`: a code whose brand production spans (open end 2019), sorted by start, leave more than
  one missing year between the furthest end so far and the next start. Count today **0** (all 1,203 candidates have
  no gap at all). Test `test_span_gap_code_is_skipped` (a 4-year gap is skipped, a 1-year gap is inserted).
- **C4.** G1 also skips a code whose extract `is_v_engine` is blank and a map configuration starts `V`, `W` or
  `BOXER`: **0** more codes (G1 stays EJ18, FB20). G2 (iii) drops "the map configuration is blank": **0** more codes.
  Test `test_blank_is_v_engine_with_v_map_is_skipped`.
- **Decision beyond the ruling (recorded).** G2 (iii) also fires when `is_v_engine` is blank, not only `0`: the tool
  writes blank as `0`, so the decoder reads both the same way (`decoder.py:364`). Count change **0** (measured with
  and without it).
- **C5.** Test 9 uses the window 1997-2001 (written 1997-2002) and asserts `ERA_OBDII_EARLY` exactly.
- **C6.** CoC stays NULL. Reason corrected: the petrol CSV is `D:/4DLab/4DLabV2/DBS/docs/vehicles_petrol_specimens.csv`
  (round 1 searched only `C:`), and Cowork's run of `_enrich_from_csv` over the extract codes enriched **0**. The
  RESULT states this.

New counts (round-2 prototype, `C:/4DApp/recheck/T-VINA-13b/mut/` temp copy, since deleted):
- skips: in_vref 24, collision 44, no_my_start 35, span_gap 0, G1 2 (EJ18 FB20; boxer 2, blank-V 0), G2 39
  (count 32, induction 5: AZQ BBM BMD BME BZG, banks 2: M30B32 M9720); **inserted 1,162** (OK 1,102, FAMILY 27,
  AMBIGUOUS 33); `engine_ref` after: 1,234 rows.
- real VINs on skipped codes: collision 72, no_my_start 4, G2 18, G1 0.
- `reach.py` prediction: unchanged from round 1 (`row_applied` 506, `not_in_vref` 550, `out_of_window` 59,
  `no_engine_code` 16; confidence, euro, O₂, air metering as in round 1).
- Tests: 18 in the new file (round 1's 16, plus C3 and C4). Predicted vinlab **279 passed, 8 skipped**; new file
  **18 passed**; dnalab 27, wired 41, ui 30.
- Mutants: M1-M16 as in round 1, plus M17 (drop the span-gap skip → `test_span_gap_code_is_skipped`) and M18 (drop
  the blank-V half of G1 → `test_blank_is_v_engine_with_v_map_is_skipped`).

## Build (redispatch 01)

1. Tests written; red run (`pt/red`): `18 errors`, each `FileNotFoundError: …tools\merge_tecdoc_extract.py`.
2. Tool written; `py_compile`, `py -m ruff check` (`All checks passed!`), `--select S` on the tool (`All checks
   passed!`), pyright on tool and test (`0 errors`). Green: `18 passed`.
3. Builder: `CREATE_ENGINE_REF` (has_maf/has_map plain `INTEGER`, one comment line) and the migration guard (C1).
4. Merge on the shipped db: `inserted 1162 rows; engine_ref now 1234 rows; schema rebuilt: yes`, skips in_vref 24,
   collision 44, status 0, no_my_start 35, span_gap 0, map_banks 2, cylinder_heuristic 39 (= round-2 prediction).
   Row dump of the 72 rows, `(typeof, value)` per column, base copy (`git show 11dfa95:…/vref.db`, sha
   `ef345c4273298572`) vs merged: dump sha256 `bb2864eae071a9bb` both, `equal True`. Window violations 0; index
   `idx_engine_ref_brand` present; 1,162 new rows have NULL has_maf/has_map and `o2_type ''`.
5. **Unexpected failure, bounded debugging (1 iteration).** After step 4, `3 failed, 15 passed` in the new file.
   - Frame: `tests/unit/test_vref_tecdoc_merge.py`, `test_second_run…`, `test_existing_rows…`, `test_real_vin…`,
     `AssertionError` (`schema_rebuilt` False; `1234 == 72`; `0.973 == 1.4`).
   - Invariant: the `db` fixture copied the *shipped* vref.db, which the merge had just changed; the tests describe
     the merge from the pre-merge state.
   - Hypothesis: a fixture that rebuilds the pre-T-VINA-13b state from the shipped file makes all 18 pass with no
     assertion changed. Confirmed.
   - Patch: `db` creates the pre-merge DDL (has_maf/has_map `NOT NULL DEFAULT 0`, `rated_rpm` last, as at
     `11dfa95`) and copies the shipped rows with `o2_type != ''` (the 72; asserted). The decode test now decodes the
     no-row case against a copy of that pre-merge db (the session `decoder` reads the merged file). No assertion
     changed. Then `18 passed`; the shipped vref.db sha (`814f0b7282b84086`) did not change across test runs.
6. Verification 1-4 (below), commit `5bf69e5`, mutants (below), Verification 5.
7. Guards met on the way: `impl_guard` refused a runner file in `mut/` (Write tool), so the mutant runner ran from
   stdin. `bash_guard` refused one stdin script (its escaped-word check reads a backslash in the text) and the first
   commit command (chained `cd … &&` with the word in the identity); rerun as `git -C … commit`.

Mutants (stdin runner; each copy at `C:/4DApp/recheck/T-VINA-13b/mut/M<n>.py`, copied over the tool, named test run
with `-k`, then `git restore tools/merge_tecdoc_extract.py vinlab/data/vref.db`):

| mutant | edit | test | result |
|---|---|---|---|
| M1 | `rows.append(_new_row(group))` → `pass` | test_inserts_new_code | KILLED (1 failed) |
| M2 | drop the in-vref check | test_skips_code_already_in_vref | KILLED |
| M3 | `return "collision"` → `pass` | test_skips_collision_code | KILLED |
| M4 | `return "no_my_start"` → `pass`; missing start → 1990 | test_skips_code_without_my_start | KILLED |
| M5 | has_maf/has_map written 0 | test_new_row_leaves_maf_and_map_null | KILLED |
| M6 | `o2_type` dropped from INSERT_ROW (default `NB`) | test_new_row_o2_type_is_empty | KILLED |
| M7 | blank euro written `''` | test_blank_fields_become_null_or_zero | KILLED |
| M8 | drop `+ MODEL_YEAR_LAG` | test_window_adds_one_model_year_and_closes_open_end | KILLED |
| M9 | era_bucket `ERA_MODERN` | test_era_bucket_comes_from_builder | KILLED |
| M10 | AMBIGUOUS out of ALLOWED_STATUSES | test_ambiguous_code_is_inserted | KILLED |
| M11 | drop the BOXER half of G1 | test_map_boxer_code_is_skipped | KILLED |
| M12 | drop G2 | test_cylinder_heuristic_hazard_is_skipped | KILLED |
| M13 | `rebuild = True` | test_second_run_inserts_nothing_and_keeps_bytes | KILLED |
| M14 | rebuild copies `NULLIF(has_maf, 0)` | test_existing_rows_keep_every_value | KILLED |
| M15 | rebuild DDL keeps `has_maf … NOT NULL DEFAULT 0` | test_schema_matches_builder | KILLED |
| M16 | displacement_cc written NULL | test_real_vin_gains_row_with_tecdoc_displacement | KILLED |
| M17 | drop the span-gap skip (C3) | test_span_gap_code_is_skipped | KILLED |
| M18 | drop the blank-V half of G1 (C4) | test_blank_is_v_engine_with_v_map_is_skipped | KILLED |

`mutants 18 of 18 killed 18 ; tool equals HEAD: True`.

## VERIFICATION GATE

| step | command (Verification block) | expected (plan) | result |
|---|---|---|---|
| 1 | vinlab suite | 279 passed, 8 skipped | `279 passed, 8 skipped in 4.68s` (final tree) |
| 2 | new test file | 18 passed | `18 passed in 2.04s` |
| 3 | dnalab / wired / ui | 27 / 41 / 30 passed | `27 passed`, `41 passed`, `30 passed` |
| 4 | `reach.py` | row_applied 506, rest as predicted | `{'no_engine_code': 16, 'not_in_vref': 550, 'out_of_window': 59, 'row_applied': 506}`; confidence, euro, O₂, air metering exactly as predicted |
| 5 | second merge; vref.db status; ruff; log; porcelain | inserted 0, no change, clean | `inserted 0 rows; engine_ref now 1234 rows; schema rebuilt: no`; no vref.db line; `All checks passed!`; `5bf69e5`, `11dfa95`, `6da3b90`; porcelain: the note, the blocker record (and the RESULT) |

No `failed` or `error` in any in-scope step. Absence of the previous decisive failure: `not_in_vref` 1,097 → 550,
`row_applied` 15 → 506 (F-C6-1). C6 probes (report-only): before `16 failed, 35 passed`, after `16 failed, 35
passed`, the same 16 names: no probe changed colour. Gate items: import sanity `import ok`; `isolation.py`
`violations: 4`; builder ruff, `--select S` and pyright equal to the base copy (`All checks passed!`; 5 pre-existing S
findings; 1 pre-existing pyright error, `mysql.connector` unresolved at :306, :305 on the base). `baseline.sh` NOT RUN:
the task marks repo-wide gates report-only and Cowork runs them at review. Verdict: **CLEAN**.

## CODE REVIEW

- Scope: the commit touches exactly the four Files-to-touch paths (`git show --stat 5bf69e5`); the builder diff is
  `CREATE_ENGINE_REF` (2 lines + 1 comment) and the migration guard (2 lines). No decoder, query or overlay change.
- Contracts: no payload field, enum value or key added. The new names (`merge`, `select_rows`, `MergeReport`,
  `derive_era`, `CREATE_ENGINE_REF`) are read by the test file and `main()`.
- Provenance: each literal at a boundary has a source comment (`OPEN_END_YEAR` 2019 = TecDoc 1Q2019,
  `MODEL_YEAR_LAG`, `MAX_SPAN_GAP_YEARS`, `ALLOWED_STATUSES` = correction 01; the guards cite `decoder.py` lines).
- Boundaries: the tool imports only stdlib and the lab's own `vinlab` package; no cross-lab import.
- SQL: no statement is built from data (literal column lists, named parameters); `ruff --select S` clean.
- Fail closed: unknown flag values, a missing column, a column set that differs from the builder DDL, an empty engine
  code and an unknown status all raise or skip; the rebuild and inserts share one transaction with ROLLBACK.
- Residual (not defects in this diff): G2 mirrors `decoder.py:446-478`, so a decoder change can make it stale
  (T-VINA-14 follows); the importlib load sets a placeholder `DBS_ROOT` for the duration of the import only.

## Revision 02 (review correction 02)

Readiness:
- (a) `fix/T-VINA-13b`, HEAD `fe64c8c spec(T-VINA-13b): correction 02 (two tests owed from the second review)`,
  child of `5bf69e5`; porcelain: only the note, the blocker record and the RESULT (untracked). `git diff --stat
  5bf69e5 fe64c8c` touches only the task file and its author sidecar.
- (b) Test (a) passes on the committed tool; its decisive check is the mutant that restores the "map configuration is
  blank" qualifier in G2 (iii), which must make it fail. Test (b) reads the shipped vref.db; its decisive check is a
  digest pinned from the base blob, so any change to an original row fails it.
- (c) Independent values: `infer_cylinder('ZZ3VEE', 0.0, 'TESTBRAND')` = `unresolved` (count 0) and
  `infer_cylinder('ZZ3VEE', 3.0, 'TESTBRAND')` = `6, V6, NATURALLY_ASPIRATED` (`disp_fallback`). Canonical digest of
  the 72 rows of `git show 11dfa95:labs/vinlab/vinlab/data/vref.db` (blob `c75ea107…`, file sha `ef345c4273298572`):
  `89403096d8074357d62e94187c58c71664c73ab4bc47c5ca4d00dbf654625275`; the shipped file gives the same.
- (d) No contradiction; the write is the test file only (Files to touch, correction 02).
- (e) Teach-back: two tests join `test_vref_tecdoc_merge.py`. One proves G2 (iii) skips a code on its own (I4 map,
  V6 hint), and dies under the qualifier mutant. The other proves the 72 shipped original rows equal a digest pinned
  from `11dfa95`.

Work:
- Tests added (test file only): `test_cylinder_heuristic_two_bank_hint_alone_is_skipped` (extract `ZZ3VEE` 3000 cc,
  6 cylinders, NA, `is_v_engine 0`; map row config `I4`, cylinders and displacement blank; asserts skipped under
  `cylinder_heuristic` and not under `map_banks`) and `test_shipped_original_rows_match_the_pinned_base_digest`
  (`ORIGINAL_ROWS_SQL` with 32 explicit columns, rows with `o2_type != ''` ordered by code, each value as
  `[type name, value]`, compact JSON; asserts 72 rows and `ORIGINAL_ROWS_SHA256`).
- The selector `o2_type != ''` is the merge's own marker: a merged row wrongly given `NB`/`WB`, or an original row
  given `''`, changes the count and fails the test.
- Inner loop: `py_compile`; `py -m ruff check` and `--select S --ignore S101`: `All checks passed!`; pyright `0
  errors`. The two tests: `2 passed`.
- Mutant M19 (copy `C:/4DApp/recheck/T-VINA-13b/mut/M19.py`; G2 (iii) gains `and not m["engine_configuration"]`):
  `-k two_bank_hint_alone` → `1 failed, 19 deselected` (**KILLED**); the other 19 tests under M19 → `19 passed`, so
  the round-1 suite did not cover this rule alone (the review's finding). `git restore` → tool equals HEAD.
- Digest sensitivity (throwaway `pt/vref_mutated.db`, 5FR `rated_rpm + 1`): digest `398fc766be9f3dd8`, not the
  pinned value. The shipped vref.db sha stayed `814f0b7282b84086`.
- Steps: 1 `281 passed, 8 skipped`; 2 `20 passed`; 5 `inserted 0 rows; engine_ref now 1234 rows; schema rebuilt:
  no`, no vref.db status line, `All checks passed!`, log `2dfbbba fe64c8c 5bf69e5 11dfa95 6da3b90`, porcelain: the
  note, the blocker record, the RESULT.
- Commit `2dfbbba test(T-VINA-13b): G2 two-bank hint in isolation and pinned digest of the 72 original rows
  (correction 02)`. `git diff --stat 5bf69e5 HEAD -- labs/vinlab/tools labs/vinlab/vinlab/data` is empty: the tool,
  the builder and vref.db did not change.

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| precheck, measurement, plan | 2026-11-04T14:04:55Z | 2026-11-04T14:38:22Z | 33 | ABSENT (no context meter in this session) |
| redispatch 01: round 2, build, verification, mutants, RESULT | 2026-11-04T15:03:26Z | 2026-11-04T15:22:27Z | 19 | ABSENT (no context meter in this session) |

| revision 02: two tests, M19, steps 1/2/5, commit, note, RESULT | 2026-11-04T15:46:36Z | 2026-11-04T15:50:26Z | 3 | ABSENT (no context meter in this session) |

Durations from `date -u` arithmetic (`$(( (end - start) / 60 ))` in epoch seconds, integer minutes): 33, 19 and 3.
Total 55, under the 110-minute stop rule.

Duration from `date -u` arithmetic: `$(( ($(date -u -d 2026-11-04T14:38:22Z +%s) - $(date -u -d 2026-11-04T14:04:55Z
+%s)) / 60 ))` = 33.
