# T-VINA-13a — progress note (implementer)

Task: `repo/labs/vinlab/tasks/T-VINA-13a_tecdoc_1q2019_extract(4).md` (plan: REQUIRED). Session 1 = precheck and plan
only. No file except this note was written. No code exists yet.

## Readiness challenge
- (a) **Starting state matches.** `git branch --show-current` = `fix/T-VINA-13a`; HEAD `e320768 spec(T-VINA-13a): …`,
  child of `7ba9368` (`git log --oneline -3`). Base = `e320768`. `git status --porcelain` empty. `db.sql ok`.
  Preconditions printed `checked`, no `MISSING`, no `EXISTS tool`. P6 re-measured on the base: `248 passed, 8 skipped`
  (step 1 command, `--basetemp=C:/4DApp/recheck/T-VINA-13a/pt/v`).
- (b) **Red test: not yet run.** R7 puts the test after approval. Intended red reason: the tool module
  `tools/extract_tecdoc_1q2019.py` does not exist, so the module-loading fixture fails each of the 10 tests
  (expected `10 failed` or `10 errors`, none passing).
- (c) **Decisive values, derived independently.** An in-memory prototype of the rules below (stdin script, no file
  written) on the real CSVs gives **1,503 rows** and **643 real VINs** covered (P5 brand-agreeing 631; +13 from the
  alias tier, −1 lost to the petrol rule). Cowork's `vina13_measure.py` re-run reproduces P3/P4/P5 exactly
  (5,881 / 32 / 1,138 / 274 / 79 / 43 / 119; 1,115 / 18 / 631).
- (d) **No contradiction blocks the work.** Two soft wording points are recorded below as assumptions (stdlib list;
  "head token"). Neither changes a criterion.
- (e) **Teach-back.** The deliverable is a stdlib tool that reads 5 TecDoc 1Q2019 tables read-only and writes one
  sorted CSV row per (folded brand, normalised code) pair of `vds_engine_map.csv` that TecDoc knows under an allowed
  manufacturer, with vref vocabulary fields and evidence. The decisive checks are a byte-identical fresh run (step 3)
  and `coverage.py` printing `vref_today` 18 and `extract` 643 (step 4).

## Assumptions worked past
1. **R1 module list.** R1 says "stdlib only (`csv`, `re`, `pathlib`, `argparse`)". R1 itself needs `os` (the
   `DBS_ROOT` default), and the R2 fold needs `unicodedata` (`_fold_brand` uses NFKD). I read the list as examples of
   stdlib, not a closed list. The tool imports `argparse, collections, csv, os, re, sys, unicodedata, pathlib`. No
   third-party import and no `vinlab` import.
2. **R3 "head token".** For a `X (Y)` Description, T1 keys are `Y`, the first whitespace token of `X`, and the whole of
   `X` normalised (`M52 B20 (206S4)` → `206S4`, `M52`, `M52B20`). The whole-`X` key adds 7 pairs (274 against 267).
   P3's 274 counts it, and R3's own example `M52 B20` is two tokens, so I take it as intended.
3. **Years are calendar years.** `passengercars.From/To` are production dates `YYYY-MM-01`, not model years.
   `my_start`/`my_end` take the calendar year. T-VINA-13b owns any model-year shift.

## Measurements (real CSVs, read-only; stdin scripts, nothing written)
- Format: all 5 files are UTF-8, no BOM, CRLF, 0 backslashes (no MySQL escapes), `"` present but literal
  (manufacturers 2, items_atributes 200). Field counts all equal db.sql's: engines 9 (26,125 rows), manufacturers 12
  (4,760), items_atributes 17 (1,914,913), passengercars 10 (69,871), passengercars_link_engines 2 (65,296).
  **Short rows on real data: 0 in every table.**
- Joins: every engine's `manufacturer` resolves (0 orphans); every link's car resolves (0 orphans); all 462,678
  `IsEngine=1` rows have `LinkitemType=Engine` and an `item_id` in engines. The only duplicated (item, AttributeType)
  is `Power` (kW and PS), which the tool does not read.
- `passengercars.From`: 20 rows `0000-00-00`; `To`: 19,191 rows `0000-00-00` (open). Years 1942-2019.

## Plan

### Approach
One pass per table into memory (about 183 MB of CSV, about 11 s for the read measured), then a pure join. Rejected:
loading SQLite first (R1 forbids non-CSV input and writing anything except `--out`).

### The tool: `labs/vinlab/tools/extract_tecdoc_1q2019.py`
Signatures (all module-level, `from __future__ import annotations`):
- `_fold_brand(raw: str) -> str`, `_normalise_code(raw: str) -> str`: copies of `vinlab.decoder._fold_brand` and
  `vinlab.db.tecdoc_query._normalise_code` (stdlib rule). A parity test pins them to the originals.
- `_table_columns(ddl: str, table: str) -> list[str]`: column names of `CREATE TABLE \`<table>\``; `ValueError` when the
  table is absent.
- `_read_table(src: Path, table: str, columns: list[str], skipped: Counter[str]) -> Iterator[dict[str, str]]`:
  `csv.reader(delimiter="\t", quoting=csv.QUOTE_NONE)`, `encoding="utf-8"`, `newline=""`; a row with
  `len(row) != len(columns)` increments `skipped[table]` and is dropped.
- `_code_keys(description: str) -> tuple[str, set[str]]`: the T0 key and the T1 keys (T1 keys exclude the T0 key and
  `""`).
- `_engine_fields(attrs: dict[str, str]) -> dict[str, str]`: the 9 derived fields of one engine (table below).
- `extract(dbs_root: Path, map_path: Path) -> tuple[list[dict[str, str]], dict[str, object]]`: rows and report data.
- `main(argv: list[str] | None = None) -> int`: `--dbs-root` (default `os.environ.get("DBS_ROOT")`; absent →
  `parser.error`, exit 2), `--map` (default `<tool dir>/../vinlab/data/vds_engine_map.csv`; the tests pass a fixture
  map), `--out` (default `<tool dir>/data/tecdoc_1q2019_engine_extract.csv`). It reads
  `<dbs-root>/1Q2019/install_database/db.sql` and `<dbs-root>/1Q2019/<table>.csv`. A missing file raises
  `FileNotFoundError` (fail loud, no partial output). It creates `--out`'s parent and writes only `--out`.
- Output: `csv.writer`, `lineterminator="\n"` (the repo's `.gitattributes` is `* text=auto eol=lf`, so the worktree
  file and a fresh run compare equal), UTF-8, header row, rows sorted by (folded brand, normalised code), a unique
  key.

### Population (R2)
Distinct (`_fold_brand(brand)`, `_normalise_code(engine_code)`) over map rows; a row whose normalised code is `""` is
not in the population (the report counts it). Measured: **5,881 pairs**. `brand` = `min()` of the map spellings of
the pair, `engine_code` = `min()` of its code spellings, independently (R4: "first spelling in sorted order"). 46 pairs
have more than one spelling (`BMW 184KA` / `18 4K A`; `N52B25A` / `N52B25A*`).

### Match tiers (R3), first non-empty wins
| tier | rule | measured pairs (all hits / after petrol) |
|---|---|---|
| `T0` | `_normalise_code(Description)` = code, `_fold_brand(manufacturer)` = brand | 1,138 / 1,119 |
| `T1` | code in `_code_keys(Description)[1]`, same manufacturer rule | 274 / 268 |
| `T0A` (added) | T0 code rule, manufacturer = the brand's alias in the table below | 118 / 116 |

- Precedence T0 → T1 → T0A; the hit ids of the first non-empty tier are the only candidates. The petrol filter runs
  after the tier is chosen (option (a)). Rejected (b), filter before choosing: a diesel exact code would then fall
  through to a petrol engine that only shares a token. Measured difference on the population: 0 pairs.
- **Why T0A is a tier.** R4 fixes the columns, so the tier label is the only place the row can say its manufacturer is
  an alias. Rejected: report alias hits as `T0` (loses the evidence T-VINA-13b needs). **No `T1A`**: an alias at T1
  adds 0 pairs on the real population, so it is not added (R3: a tier needs a measured count).
- T0A samples (random, seed 7): `VOLKSWAGEN AB` → VW `AB` (id 4005); `VOLKSWAGEN AXQ` → VW `AXQ` (16853);
  `GENESIS G4DJ` → HYUNDAI `G4DJ` (9400). T0: `MITSUBISHI 4B10` → `4B10`; `RENAULT Z7W712` → `Z7W 712`.
  T1: `BMW 234EA` → `S14 B23 (234EA)`; `BMW 358S2` → `M62 B35 (358S2)`.

### Brand-alias table (pinned in the tool; map brand fold → TecDoc manufacturer fold)
| map brand | TecDoc | rows added | why it is the same company |
|---|---|---|---|
| `VOLKSWAGEN` | `VW` | 75 (77 before petrol) | TecDoc's short name for Volkswagen AG |
| `GENESIS` | `HYUNDAI` | 37 | Genesis is a brand of Hyundai Motor Company |
| `FORD` | `FORDUSA` | 2 | Ford Motor Company, US catalogue |
| `BMWI` | `BMW` | 2 | BMW i is a BMW AG sub-brand |

Rejected candidates (written no row; counted under another-manufacturer): **joint ventures** `AUDI`→`AUDIFAW` 5,
`AUDI`→`VWFAW` 1, `NISSAN`→`NISSANDONGFENG` 2, `BMW`→`BMWBRILLIANCE` 1, `CITROEN`→`DSCAPSA` 2 (a JV is another company;
**Cowork: adding `AUDIFAW` is the one call I am least sure of — it adds 5 rows, all Audi engines**). **Platform shares**
(R3): `HYUNDAI`/`KIA` 5, `PEUGEOT`/`CITROEN` 6 (P4 said 5; with T1 keys counted as "TecDoc knows the code" it is 6),
`AUDI`/`SEAT`/`VW`, `KAWASAKI`/`SUZUKI` 3, `MATRA`/`RENAULT` 4. Motorcycle brands with VW codes (P4) stay misses
(T-VINA-12's).

### Petrol (H1)
Petrol `EngineType` values: `Petrol Engine` (13,852 engines), `Petrol Engine (two-stroke)` (8). Excluded: `Diesel`
12,101, `Electric Motor` 154, `Wankel` 10 (0 hits in the population, so this choice changes no row). Measured: 27 pairs
non-petrol (all `Diesel`); 0 matched pairs mix petrol and non-petrol ids. `FuelType` is not a filter (R4 names
`EngineType`). Among kept engines, FuelType `Petrol/Alcohol` 36, `Petrol/Gas` 19, `Petrol/Alcohol/Gas` 3,
`Petrol/Electro` 1: the RESULT reports these for T-VINA-13b.

### Field derivation (per engine id, then the ambiguity rule). Fill rates are of the 1,503 predicted rows.
| column | source → value | fill |
|---|---|---|
| `tecdoc_engine_ids` | kept (petrol) ids, numeric sort, `;`-joined | 100% |
| `tecdoc_description` | distinct `Description` of kept ids, sorted, `;`-joined (no Description contains `;`) | 100% |
| `displacement_cc` | Capacity `^(\d+) ccm$` → the integer; `ccm` (154 engines, electric) and `N - N ccm` (2) → blank | 98.7% |
| `cylinder_count` | NumberOfCylinders `^\d+$` | 99.9% |
| `fuel_delivery_type` | FuelMixture `Intake Manifold Injection/ Carburettor`, `Petrol Injection`, `Multipoint Injection`, `Motronic`, `Intake Manifold Injection` → `PORT_INJECTION`; `Direct Injection` → `GDI`; `Manifold Injection/Direct Injection` (dual, 11 ids in hits), carburettors, `Fuel Cell`, diesel pumps, absent → blank | 98.2% |
| `has_gdi` | `1` for `Direct Injection` and the dual value; `0` for the port set and the carburettor set; else blank | 99.1% |
| `induction_type` | `Naturally Aspirated Engine` → `NATURALLY_ASPIRATED`; `Turbo/Intercooler`, `Exhaust Turbocharger`, `Bi-Turbo/Intercooler`, `Turbo`, `Turbocharger/Compressor` (twincharger, as the old builder's `турбо/нагнетатель`), `Regulated 2-stage charging` → `TURBOCHARGED`; `Compressor`, `G-Charger` → `SUPERCHARGED`; `Charged`, `RAM-Air`, absent → blank | 75.0% |
| `has_turbo` | `1` if TURBOCHARGED, `0` if NATURALLY_ASPIRATED or SUPERCHARGED, else blank | 75.0% |
| `is_v_engine` | EngineConstruction `V`, `VR`, `W`, `V6`, `V8` → `1`; `Straight`, `BOXER`, `Rotor, wankel engine` → `0`; absent → blank | 99.0% |
| `valvetrain_type` | CylinderConstruction `DOHC`→`DOHC`, `SOHC/OHC`→`SOHC`, `OHV`→`OHV`, `CIH`→`CIH`; absent → blank. vref.db has no vocabulary here (72/72 NULL, no reader in `vinlab/` or `wired/`) | 93.1% |
| `euro_norm` | EmissionNorm `^Euro ?([1-6])( \(D\1\))?$` → `euroN`. Blank: two-norm values (`Euro4/Euro5` 5 ids in hits, `Euro5/Euro6` 1), `EEV`, `Euro 5/EEV`, `From Euro 4` (1), `Up to Euro N`, `ULEV2` (1), `D4`. Reason: none names one norm; no lower/upper guess | 7.6% |
| `my_start` | min `From` year over all linked cars of the kept ids, `0000` ignored; no car → blank | 97.3% |
| `my_end` | blank if any linked car has `To` `0000-00-00` or no car; else max `To` year | 64.0% |
| `n_cars` | distinct linked car ids, pooled | 100% (97.3% > 0) |

### Ambiguity
With more than one kept id, each of the 9 derived fields is kept only when every id gives the same value, **blank
counted as a value** (an id that states nothing does not agree). Otherwise the field is blank and `status` is
`AMBIGUOUS`. Rejected: ignore blanks (10 rows would become `OK` on a value only some ids state; head-token pools mix
distinct engines, so this risks a false value). Years and `n_cars` pool. Predicted: **T0 OK 1,117, T0 AMBIGUOUS 2,
T1 OK 228, T1 AMBIGUOUS 40, T0A OK 116** (1,503).

### No-row split (report)
Other-manufacturer 459 (the code is a T0 or T1 key under some manufacturer not allowed; includes the JV and platform
lines above), non-petrol 27, no code 3,892. 1,503 + 459 + 27 + 3,892 = 5,881.

### Stdout (step 3 takes `tail -3`)
Before the last three lines: one line per table `table <t>: rows <n>, skipped <k> (field count != <c>)`; the
population line; the other-manufacturer breakdown by (brand, TecDoc manufacturers), top 25; fill per column; code
collisions. Last three: `no_row other_manufacturer=459 non_petrol=27 no_code=3892`,
`rows T0/AMBIGUOUS=2 T0/OK=1117 T0A/OK=116 T1/AMBIGUOUS=40 T1/OK=228`, `wrote <out> rows=1503`.
Code collisions (R6): 173 codes are rows under more than one brand; 142 of them have different id sets, so the count
with different field values is at most 142 (the run measures it).

### Tests: `tests/unit/test_extract_tecdoc_1q2019.py` (NEW), the tool loaded by `importlib.util.spec_from_file_location`
A fixture writes `<tmp>/1Q2019/` with a minimal `install_database/db.sql` (the 5 CREATE TABLE blocks, real column
names) and the 5 tables, plus a fixture map CSV. No test reads `D:/`.
| # | test | rule | mutant (edit of the copy in `recheck/T-VINA-13a/mut/`) |
|---|---|---|---|
| 1 | `test_t0_exact_hit` (`RENAULT Z7W-712` ↔ `Z7W 712`) | T0 | compare raw Description, not normalised |
| 2 | `test_t1_paren_alias_hit` (`BMW 206S4` ↔ `M52 B20 (206S4)`) | T1 | drop the paren-group key |
| 3 | `test_other_manufacturer_miss` (`HYUNDAI` code only under `KIA`; counted) | manufacturer rule | skip the manufacturer comparison |
| 4 | `test_alias_table_hit` (`VOLKSWAGEN AXQ` ↔ VW `AXQ`, tier `T0A`) | alias | delete the `VOLKSWAGEN` entry |
| 5 | `test_ambiguity_blanks_disagreeing_field` (1598 vs 1595 ccm, same ChargeType) | ambiguity | keep the first id's value |
| 6 | `test_non_petrol_excluded` (Diesel only; counted non-petrol) | H1 | remove the EngineType filter |
| 7 | `test_years_from_cars_with_open_end` (one open `To` → `my_end` blank; closed → max) | years | max over non-open `To` only |
| 8 | `test_short_row_skipped_and_counted` (an 8-field engines row that would otherwise match) | R1 count | remove the field-count check |
| 9 | `test_deterministic` (two runs equal bytes, and a run on reversed input rows equals them) | sort | write rows unsorted |
| 10 | `test_fold_matches_vinlab` (`Citroën`, `LAND ROVER`, `N52B30A*` against vinlab's functions) | R2 parity | fold without NFKD |

Predicted counts: step 2 `10 passed`; step 1 `258 passed, 8 skipped`.

### Rules and gates added (population checked on → population run over)
| rule | checked on | runs over (command) | false pass | false fail |
|---|---|---|---|---|
| field-count skip | 5 real tables, 0 short rows | same, step 3 | a malformed row with the right count passes (0 backslashes measured, so no escaped tab) | none: counts equal the DDL everywhere |
| T0/T1 keys | 5,881 pairs × 26,125 engines | same, step 3 | head-token T1 joins a family code to its variants (handled as AMBIGUOUS, 40) | a code spelt differently (`C1EP760` vs `C1E 760`) stays a miss |
| alias table | 5,881 pairs | same | none known; each entry is a single company | JV brands excluded (11 pairs) |
| petrol filter | 1,530 matched pairs (1,138 + 274 + 118) | same | a petrol EngineType with FuelType `Petrol/Electro` (1 id) is kept | none measured |
| ambiguity (strict) | 79 multi-id pairs | same | none | 10 rows AMBIGUOUS only through a blank |
| determinism | fixture, test 9 | step 3 `cmp` | none | none |

Steps that change later inputs: step 3 of R7 writes the tracked CSV that verification steps 3 and 4 read; the commit
(R7 6) precedes the mutants, so `git restore` returns the committed tool; each mutant is restored before the next and
before step 5's `git status`.

### Commands and paths after approval
- `$PY -m pytest … tests/unit/test_extract_tecdoc_1q2019.py --basetemp=C:/4DApp/recheck/T-VINA-13a/pt/t` (red, then
  green).
- Real run: `cd labs/vinlab && DBS_ROOT=D:/4DLab/4DLabV2/DBS $PY tools/extract_tecdoc_1q2019.py` → writes
  `labs/vinlab/tools/data/tecdoc_1q2019_engine_extract.csv` only.
- Verification steps 1-5 as written; mutants in `C:/4DApp/recheck/T-VINA-13a/mut/`.
- `py -m ruff check`, `py -m ruff check --select S`, `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe` on
  the tool and the test.
- Commits on `fix/T-VINA-13a` by explicit path: the tool + test + CSV.

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| precheck + plan | 2026-11-04T12:47:27Z | 2026-11-04T12:55:45Z | 8 | ABSENT (no measure available in session) |
## Plan stop: handed back for Cowork's plan review (no blocker JSON: plan stops need none).

## Plan round 2 (redispatch, correction 01: C1-C6)
Redispatch start 2026-11-04T13:20:51Z. **Base = `f0e26bb`** (`spec(T-VINA-13a): plan correction 01 …`, child of
`e320768`). `git status --porcelain` = `?? labs/vinlab/tasks/progress_notes/T-VINA-13a.md` only, as First action
(Redispatch 01) states. The correction carries no `### Plan-time digest ###` table (`grep -c` = 0), so no digest check.

Readiness (round 2): (a) matches, above. (b) red run pending (step 2 of R7, next). (c) the round-2 prototype (stdin
script, same rules plus C1-C3) predicts 1,498 rows and 642 real VINs. (d) no contradiction. (e) unchanged, except the
decisive values are now 1,498 rows and `extract` 642.

Changes:
- **C1** — a head-token or whole-X T1 key that is all digits is not emitted; paren keys stay. T1 263 pairs (was 268
  after petrol): 5 pairs drop (`ZASTAVA 100`, `SKODA 136`, `FIAT 6132`, `PEUGEOT 106`, `PEUGEOT 118`). The same key
  set feeds "TecDoc knows the code", so the other-manufacturer count falls 459 → 412 and no-code rises 3,892 → 3,944.
- **C2** — new status `FAMILY`: all 9 fields agree but the kept ids carry more than one distinct normalised
  `Description`. `AMBIGUOUS` wins. 34 rows, all T1.
- **C3** — `Turbocharger/Compressor` → `induction_type` blank, `has_turbo` `1`. 33 petrol engines carry it; 0 of them
  are in a row, so no row changes. The RESULT reports the 0.
- **C4** — test 9 runs the fixture twice (equal bytes), then on the fixture map reversed, and asserts its bytes and its
  expected first and last data rows. Mutant: drop the output sort.
- **C5** — test 7 links one engine to one open and one closed car and asserts `my_end` blank (and `my_start` the min).
  Mutant: max over closed `To` only.
- **C6** — test 11 `test_petrol_order_diesel_t0_blocks_petrol_t1`: a diesel T0 hit plus a petrol T1 hit on one pair
  gives no row and counts non-petrol 1. Mutant: filter petrol before choosing the tier.

Tiers (no new tier beyond `T0A`, approved): T0 1,138 / 1,119 after petrol; T1 269 / 263; T0A 118 / 116.

Predicted rows by (tier, status): T0/OK 1,117, T0/AMBIGUOUS 2, T1/OK 189, T1/FAMILY 34, T1/AMBIGUOUS 40, T0A/OK 116
= **1,498**. No row: other-manufacturer 412, non-petrol 27, no code 3,944. 1,498 + 412 + 27 + 3,944 = 5,881.
Code collisions: 173 codes are rows under more than one brand; 44 differ in at least one of the 9 fields.

Real VINs (`coverage.py` step 4): `vins_with_code` 1,115, `vref_today` 18, **`extract` 642** (T0 377, T1 252, T0A 13).

Tests 1-11 (mutant → killing test):
1 T0 exact (raw Description compare → 1). 2 T1 paren alias, plus an all-digit head token emits no key (drop paren key
→ 2; emit digit keys → 2). 3 other-manufacturer miss (skip manufacturer compare → 3). 4 alias `T0A` (delete VOLKSWAGEN
entry → 4). 5 ambiguity blanks the disagreeing field, plus a `FAMILY` pool (keep first id's value → 5; never emit
FAMILY → 5). 6 non-petrol excluded (remove EngineType filter → 6). 7 years, open + closed car (C5). 8 short row skipped
and counted (remove field-count check → 8). 9 determinism (C4). 10 fold/normalise parity with vinlab (fold without
NFKD → 10). 11 petrol order (C6). Predicted: step 2 `11 passed`; step 1 `259 passed, 8 skipped`.

## Build (round 2)
- Red: `11 errors`, every one `FileNotFoundError: … tools\extract_tecdoc_1q2019.py` (tool absent): the intended
  reason.
- One bounded-debug loop (iteration 1 of 5). Frame: `@dataclass` in `spec.loader.exec_module`, `AttributeError:
  'NoneType' object has no attribute '__dict__'`. Invariant: `dataclasses` resolves the class's module through
  `sys.modules`. Hypothesis: the test loader does not register the module. Patch: `sys.modules[spec.name] = module`
  before `exec_module` (the standard importlib recipe), 1 line in the test. Result: `11 passed`.
- Commit `f836bcf` on `fix/T-VINA-13a` (the tool, the test, the CSV), by explicit path.

## VERIFICATION GATE
| step | command (task § Verification) | expected | observed |
|---|---|---|---|
| 1 | vinlab suite, `--basetemp=…/pt/v` | 259 passed, 8 skipped | `259 passed, 8 skipped in 3.41s` |
| 2 | new test file, `--basetemp=…/pt/t` | 11 passed | `11 passed in 1.22s` |
| 3 | fresh run to `out/run2.csv`, `cmp` | summary, then `identical` | `no_row other_manufacturer=412 non_petrol=27 no_code=3944` / `rows T0/AMBIGUOUS=2 T0/OK=1117 T0A/OK=116 T1/AMBIGUOUS=40 T1/FAMILY=34 T1/OK=189` / `wrote … rows=1498` / `identical` |
| 4 | `coverage.py` on the committed CSV | `vref_today` 18, `extract` 642 | `{'vins_with_code': 1115, 'vref_today': 18, 'extract': 642}` |
| 5 | `.venv-loop` ruff; `git log 7ba9368..HEAD`; porcelain | All checks passed; spec + mine; note (+RESULT) | `All checks passed!`; `f836bcf`, `f0e26bb`, `e320768`; `?? …/progress_notes/T-VINA-13a.md` |
| gate | `py_compile`; `py -m ruff check`; `py -m ruff check --select S` | clean | compiled; clean; tool clean, test S101 `assert` only (pytest idiom) |
| gate | `py -m pyright --pythonpath …` both files | 0 errors | `0 errors, 0 warnings, 0 informations` |
| gate | deployed-layout import `from wired import diagnose` | ok | `import ok` |
| gate | mutants (R7 7), 13 | each kills its test | 13/13 `1 failed, 10 deselected`; tool restored after each, `git diff` empty |
| repo-wide | dnalab, wired, ui suites; `baseline.sh`; `isolation.py` | report-only | NOT RUN: no shipped module changed; Cowork runs them at review |
The previous decisive failure (F-C6-1: real VINs reaching vref.db 18 of 1,115) is not changed by this row by design
(vref.db is T-VINA-13b's); the extract now covers 642 of 1,115.
Verdict: **CLEAN**.

## CODE REVIEW
- Scope: 3 committed files, all in Files to touch. No vref.db, decoder, map or builder change. CLEAN.
- Contracts: no COMLab payload field. The CSV's consumer is T-VINA-13b (named by the task); no code reads it yet,
  which is this row's design. NOTE.
- Provenance: every literal set is TecDoc vocabulary measured in the plan (value counts in § Measurements and Plan).
- Boundaries: stdlib only (no `vinlab` import in the tool); the fold and normaliser are copies, pinned by test 10.
- Nit: `rows.sort(...)` repeats the order the loop already gets from `sorted(spellings)`; harmless. Mutant M9 had to
  remove both to make the output unsorted.
- Uncertainty kept: years are calendar production years; JV brands excluded; FuelType bi-fuel engines kept
  (`Petrol/Alcohol` 36, `Petrol/Gas` 19, `Petrol/Alcohol/Gas` 3, `Petrol/Electro` 1 engine ids).

## Time (rounds 1 and 2)
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| round 1: precheck + plan | 2026-11-04T12:47:27Z | 2026-11-04T12:55:45Z | 8 | ABSENT (no in-session measure) |
| round 2: plan round 2 + build + verify + RESULT | 2026-11-04T13:20:51Z | 2026-11-04T13:29:08Z | 8 | ABSENT (no in-session measure) |
| total | | | 16 | |

## Revision 02 (review correction 02, task R5 "Ruled (02, review)")
Start 2026-11-04T13:53:41Z. State: HEAD `7b87192 spec(T-VINA-13a): correction 02 file modes` (after `6316a28`, on
`f836bcf`); porcelain = the note and the RESULT only. Files to touch: the test file MODIFY; the tool and the CSV
unchanged.
- **Before:** Cowork's `review/F2.py` (drops `soft.add(_normalise_code(m.group(1)))`, the whole-part key) and
  `review/F3.py` (`values = {… if e[f]} or {""}`, ignores blanks) each gave `11 passed` on the old test file:
  both survived (copy over the tool, run, `git restore`).
- **Added** (test file only): `test_t1_whole_part_before_parentheses_hit` (map `BMW M52B20` ↔ engine 20
  `M52 B20 (206S4)`, tier T1, ids `20`). `test_ambiguity_blank_field_disagrees` (map `RENAULT H4J` ↔ engines 54
  `H4J 700` and 55 `H4J 704`, with no ChargeType on 55: `AMBIGUOUS`, `induction_type` and `has_turbo` blank,
  `displacement_cc` 1598 kept).
- **Consequence:** the shared fixture now has 16 engines (15 read + 1 short), so the short-row test expects
  `table engines: rows 15, skipped 1` (was 13). That is the only change to an existing assertion. Rejected: a second
  fixture for the two tests (more helper code for the same check).
- **After:** F2: `-k test_t1_whole_part_before_parentheses_hit` → `1 failed, 12 deselected` (whole file
  `2 failed, 11 passed`; test 2's `no_code` count also moves). F3: `-k test_ambiguity_blank_field_disagrees` →
  `1 failed, 12 deselected` (whole file `1 failed, 12 passed`). The tool was restored after each one.
- My 13 mutants (M1-M11) were re-run on the grown fixture: 13/13 KILLED (`1 failed, 12 deselected` each).
- Steps: 1 `261 passed, 8 skipped`; 2 `13 passed`; 5 `All checks passed!`, log `aa7cdbf` `7b87192` `6316a28`
  `f836bcf` `f0e26bb` `e320768`, porcelain = note + RESULT. pyright on the test `0 errors`; ruff S: S101 only.
  `git diff --quiet HEAD -- labs/vinlab/tools/` holds: the tool and the CSV are unchanged, so steps 3 and 4 are as
  before (identical; extract 642).
- Commit `aa7cdbf test(T-VINA-13a): whole-part T1 key and blank-field ambiguity tests (correction 02)`.

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| revision 02 | 2026-11-04T13:53:41Z | 2026-11-04T13:56:40Z | 2 | ABSENT (no in-session measure) |
| total (3 rounds) | | | 18 | |
