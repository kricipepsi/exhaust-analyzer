# T-VINA-16 progress note: engine_ref cylinder_count from TecDoc; the decoder prefers it

Status: **completed** (`labs/vinlab/tasks/results/RESULT_T-VINA-16.md`). Plan approved
(`repo/labs/vinlab/tasks/corrections/T-VINA-16_plan_correction_20261105.md`, O1-O3, C1-C5); redispatched
2026-11-05T11:14:30Z to build (`plan: APPROVED`); commits `52b834f`, `324fd5a` on `fix/T-VINA-16`. Review revision 02
(test file only) redispatched 2026-11-05T11:55:46Z: commit `84c5aa0` (`## Revision 02` below). Ledger row left
`pending` for Cowork.

## Readiness challenge (revision 02, before the first edit)

Clock at First action: 2026-11-05T11:55:46Z. Scope: test file only (R4 "Ruled (02)"); tool, decoder and `vref.db` do
not change.
(a) **Starting state matches.** `git branch --show-current` = `fix/T-VINA-16`; `git log --oneline -3` = `daae97d
spec(T-VINA-16): review revision 02 (two isolating merge tests)` above `324fd5a` and `52b834f` (**revision-02 base for
the RESULT log: `daae97d`**). `git status --porcelain` = exactly `?? labs/vinlab/tasks/progress_notes/T-VINA-16.md` and
`?? labs/vinlab/tasks/results/RESULT_T-VINA-16.md`. Preconditions: `checked`, no `MISSING`. Plan-time digest table
(re-recorded at `324fd5a`) recomputed with `sha256sum <path> | cut -c1-16`: all six equal (`540b3452756e91e1`,
`c9980aec5b9b4b4e`, `33d16e0b135f90bf`, `660e81961e887038`, `e320dabd17096009`, `34f7b1cbcee73249`). Base counts:
step 2 `55 passed`, step 1 `373 passed, 8 skipped` (`--basetemp=…/pt/r2base_t`, `…/r2base_v`).
(b) **Tests fail for the intended reason:** the code does not change, so the red run is the mutant run. Before the
edit, each mutant is run against the current merge file (expected: it survives, the reason for revision 02); after
the edit, against the new tests (expected: `DID NOT RAISE RuntimeError` on the `has_maf`-only and `has_map`-only cases
for (a); `assert 1 == 0` on `backfilled` for (b)). Recorded under `## Revision 02`.
(c) **Independent values.** (a) `all(...)`: a variant with `has_maf` NOT NULL and `has_map` nullable gives notnull
flags (1, 0); `any` = True refuses, `all` = False passes the guard, `fills` = [(4, '5FR')], `rows` = [] (5FR is
`in_vref`), so the mutant commits and does not raise; the "both" case (1, 1) still refuses under `all` (2 of 3 cases
fail). (b) raw keys: `_stated_counts` gives {`5FR`: 4, `5 FR`: 6}, both single; the fixture's `5FR` normalises to
`5FR` (`tecdoc_query._normalise_code`: uppercase, alphanumeric only), so the mutant fills 4 and `backfilled` = 1; the
real rule keys both on `5FR`, {4, 6}, no fill, `backfilled` = 0. Counts: 55 + 2 (one test to three cases) + 1 = 58;
373 + 3 = 376 (matches the ruling).
(d) **No contradiction or missing decision.** The ruling names the test names, the cases, the mutants and the counts;
every write is the test file, the note or the RESULT. How to build a variant table with one sensor nullable is open:
recorded as A9 under `## Revision 02`.
(e) **Teach-back:** add three refusal cases (`has_maf` only, `has_map` only, both NOT NULL, each with `cylinder_count`,
each raising and leaving the bytes) and one conflicting-spelling test (`5FR` 4, `5 FR` 6 → NULL, `backfilled` 0). The
decisive check: `all(...)` for `any(...)` and raw-keyed `_stated_counts` each fail a named new test, and steps 1 and 2
read `376 passed, 8 skipped` and `58 passed`.

## Readiness challenge (redispatch, before the first edit)

(a) **Starting state matches.** `git branch --show-current` = `fix/T-VINA-16`; HEAD `96d8a43 spec(T-VINA-16): second
plan review evidence (ds-flash)`, a descendant of `3c2d512` (**base for the RESULT log: `96d8a43`**);
`git log --oneline 3c2d512..HEAD` = `96d8a43`, `1bac3f3`, `d681469`, `53a06db`. Preconditions: `checked`, no `MISSING`.
Plan-time digest table recomputed with `sha256sum <path> | cut -c1-16`: all six equal (`ddbd269f1e0599eb`,
`eac76884b6d52744`, `efa5c0654cfc3ce4`, `88d5818782b8acff`, `0f1f2a5ace2c0aa6`, `78ee90f39c2d4631`).
`git status --porcelain` = `?? labs/vinlab/tasks/progress_notes/T-VINA-16.md` only: this note, written at the plan stop
and cited by the approval (assumption A5).
(b) **Tests fail for the intended reason:** recorded at step 2 below (red run), with the decisive evidence from the
step-9 mutants (unchanged from the plan-phase line (b)).
(c) **Independent values:** unchanged from the plan-phase line (c); C2 and C5 add no new decisive value (each is a
refusal or a skip, checked by its mutant).
(d) **No contradiction or missing decision:** none. C1-C5 are additive to the plan and fit `### Files to touch ###`.
(e) **Teach-back:** unchanged from the plan-phase line (e), plus: a counted db with NOT NULL sensors refuses (C2), and
G2 treats `"0"` as unstated (C5).

## Readiness challenge (plan phase)

(a) **Starting state matches.** `git branch --show-current` = `fix/T-VINA-16`; HEAD `d681469 spec(T-VINA-16): …` (base for
the RESULT log); `git log --oneline 3c2d512..HEAD` = `d681469`, `53a06db`; `git diff --stat 3c2d512 HEAD` touches only 4
task documents (DISPATCH.md, PROGRESS.md, the task file, the authoring sidecar); `git status --porcelain` empty.
Preconditions printed `checked`, no `MISSING`. `sha256sum vref.db` prefix `88d5818782b8acff` (P1). engine_ref: 1,274 rows,
32 columns, no `cylinder_count` (PRAGMA read). P5 re-run on HEAD: vinlab `354 passed, 8 skipped`; the two named files
`36 passed`; dnalab `27 passed`; wired `41 passed`; ui `30 passed`. Step 4 on HEAD: `vref outcome: {'no_engine_code': 12,
'not_in_vref': 483, 'out_of_window': 68, 'row_applied': 568}` (P1).

(b) **Tests fail for the intended reason: NOT RUN yet** (the plan gate stops before the first edit; the tests are not
written). Predicted step-2 red run on the base, per new test, is in Plan § 4. The decoder fixture tests will fail on
the base with `no such column: cylinder_count` (the shipped db has no column until step 6). That is a real red but not
the decisive reason. The decisive evidence that they test R3 is mutant M10 at step 9 (R3 deleted, merged db present):
`assert 6 == 4`.

(c) **Independently derived values agree with the pins.** AEB: extract states 4 for AUDI and VOLKSWAGEN, map says V6/6
→ test expects 4. NG: extract AUDI 5, map V6/6 → 5. H25A: extract SUZUKI 2,493 cc, 6 cylinders, `is_v_engine` 1, map rows
blank → 6 cylinders, 2 banks. My read-only run of the R2 rules over the shipped db and the extract: backfill 1,225 rows
(P2); `select_rows` with the G2 early return: inserted 34, skipped in_vref 1,226, collision 9, status 0, no_my_start 37,
span_gap 0, map_banks 0, cylinder_heuristic 0 (P3). Rows after 1,274 + 34 = 1,308; rows with a count 1,225 + 34 = 1,259.
`reach_rehearsal.py` printed `{'no_engine_code': 12, 'not_in_vref': 468, 'out_of_window': 72, 'row_applied': 579}` (P3).
An R3-exact patch (`isinstance(c, int) and c > 0` on the in-window row dict) over `c6_lib.real_vins()`: decoded 1,131,
changed `cyl` 71, `banks` 1, `disp` 11; induction, euro, O₂, air metering and fuel delivery 0 (P4). The shipped-table
digest has no independent value before the merge: it is recorded at step 6 (R4 says so).

(d) **No contradiction or missing decision prevents implementation.** One spec detail needs a design choice, not a
hand-back: the rebuilt `test_g2_runs_on_the_coalesced_row` asks that the `_g2_cylinder_heuristic(group[0], …)` mutant
skip the code. G2 returns False on a blank displacement, so `group[0]` must state a displacement (3,000 cc) with a blank
count for G2 (iii) to fire on it (Plan § 4, T-M3). Verified: `infer_cylinder('ZZ2GTW', 3.0, 'TESTBRAND')` = 6, V6, NA;
at 0.0 L it is unresolved (count 0).

(e) **Teach-back.** engine_ref gains a nullable `cylinder_count` that the merge tool fills from TecDoc (1,225 existing rows
backfilled, 34 G2-skipped codes inserted, 1,308 rows), and the decoder takes a positive vref count before the map's
count and before `_cylinder_fallback`. The decisive checks are step 4 printing P3's reach line, the R5 list matching
P4's 71/1/11/0 with every change attributed to a TecDoc field, the shipped-table digest test, and each named mutant
failing its named test.

## Assumptions worked past

- A1. "State exactly one non-blank `cylinder_count`" means exactly one distinct integer value over the code's extract
  rows (two brands that both state 4 fill 4). This is how `survey.py` S2 counts it; the real population has no code
  with two values among existing rows (S2: `extract_multi` absent).
- A2. `COPY_ROWS` stays the current 32-column constant. It names only columns the old table has. See Plan § 2, choice C2.
- A3. The digest test reads `SELECT * FROM engine_ref ORDER BY engine_code` ("every column"), in PRAGMA order.
- A4. The plan stop needs no blocker JSON (the header says so). No stop class (a)-(d) fired.
- A5. (redispatch) `### First action ###` expects an empty `git status --porcelain`; it shows this note, untracked. The
  note is the plan the approval reviewed and is in my write scope, so this is not a starting-state defect. No blocker
  record is written.

## Plan

### 1. Approach, in R6 order (steps 2-10 run only after approval)

**R1, builder** (`tools/build_vref_db.py` `CREATE_ENGINE_REF`): add two lines after `displacement_cc INTEGER,`, matching
the existing `-- has_maf/has_map NULL: …` comment style:
```sql
    -- cylinder_count: TecDoc's count, NULL when the source does not state it (T-VINA-16)
    cylinder_count     INTEGER,
```
Nothing else in the builder changes (its `INSERT_ROW` names its columns, so a fresh build leaves the column NULL; T-VINA-20).

**R2, merge tool** (`tools/merge_tecdoc_extract.py`):
- `INSERT_ROW` names `cylinder_count` after `displacement_cc` (`:cylinder_count`).
- New constant `BACKFILL_COUNT = "UPDATE engine_ref SET cylinder_count = ? WHERE engine_code = ? AND cylinder_count IS NULL"`.
- New `_stated_counts(extract_rows: list[dict[str, str]]) -> dict[str, int]`: normalised code → its one stated count,
  only for codes whose non-blank `cylinder_count` values form exactly one distinct integer (all brands, any status).
  A non-integer value raises `ValueError` from `int()` (the real population has none: values are blank once, else 2-12).
- `MergeReport` gains `backfilled: int` (constructed by keyword only; no caller outside the tool and its test file:
  `grep -rn "MergeReport\|merge_tecdoc_extract" labs apps audit` finds none).
- `_g2_cylinder_heuristic`: first line becomes `if row["cylinder_count"] or not row["displacement_cc"]: return False`;
  the test (i) line `if row["cylinder_count"] and after.count != …` is deleted; the bank test (iii) is unchanged. Its
  docstring says a stated count is the decoder's count (R3), so `_cylinder_fallback` does not run.
- `_new_row` writes `"cylinder_count": _int_or_none(first["cylinder_count"])` (the coalesced row; blank → NULL).
- `merge()`:
  ```python
  names = {name for name, _ in columns}
  if names not in (builder_names, builder_names - {"cylinder_count"}):
      raise RuntimeError(...)                         # unchanged message
  rebuild = "cylinder_count" not in names or any(notnull for name, notnull in columns if name in ("has_maf", "has_map"))
  null_sql = "SELECT engine_code FROM engine_ref" + ("" if "cylinder_count" not in names else " WHERE cylinder_count IS NULL")
  stated = _stated_counts(extract_rows)
  fills = [(stated[_normalise_code(c)], c) for (c,) in conn.execute(null_sql) if _normalise_code(c) in stated]
  ...
  if rebuild or rows or fills:   # BEGIN IMMEDIATE; rebuild; backfilled = executemany(BACKFILL_COUNT, fills).rowcount; insert; COMMIT
  ```
  The two SQL strings are literals chosen by a branch, not formatted (no `S608`). Order inside the one transaction:
  rebuild, then backfill (existing rows only), then insert. No write happens when all three are empty, so a second run
  leaves the bytes unchanged.
- `main()` last line: `inserted N rows; cylinder counts filled N; engine_ref now N rows; schema rebuilt: yes|no`.
- Module docstring: states the column, the backfill rule, that a stated count makes G2 return False (test (i)
  retired), and the guard's two accepted column sets.

**R3, decoder** (`vinlab/decoder.py::RobustVINDecoder.decode_vin_payload`): three lines between the
`_apply_vref_techmask(...)` call and the `_cylinder_fallback(...)` call:
```python
# T-VINA-16 R3: TecDoc's stated count (engine_ref.cylinder_count) replaces the map's; NULL, 0 or no column keeps it
vref_cylinders = db_dict.get("cylinder_count")
if isinstance(vref_cylinders, int) and vref_cylinders > 0:
    _cylinder_count = vref_cylinders
```
`db_dict` is the in-window row (`{}` when absent or out of window), so the rule holds only inside the row's window,
like every other vref field. Signatures, return types and exceptions of every existing function stay the same.

**Step 6, the merge**: one stdin script (no file written) run from `audit/scratch/C6`: (i) decode the 1,131
`c6_lib.real_vins()` with the new decoder on the shipped db still at base (R3 is inert: no column); (ii) run
`$PY tools/merge_tecdoc_extract.py` as a subprocess and print its output; (iii) `_build_normalised_index.cache_clear()`
(it is `lru_cache`d per path and would miss the 34 new codes); (iv) decode again; (v) print every VIN whose cylinder
count, banks, displacement, induction, euro, O₂ type or air metering changed, with the engine code, whether its row was
backfilled or inserted, and the row's `cylinder_count`, `is_v_engine` and `displacement_cc`. Then compare the changed VIN
set with `survey.out` S5 (must be equal: 71 + 1 + 11). Then compute the digest with a stdin one-liner and write it into
the test.

### 2. Choices the task leaves open

| # | choice | taken | rejected | why |
|---|---|---|---|---|
| C1 | where R3 lives | inline in `decode_vin_payload`, after `_apply_vref_techmask` | inside `_apply_vref_techmask` | that would add a count to its 21-element return tuple and its signature; inline is 3 lines |
| C2 | `COPY_ROWS` | keep the 32-column constant | build the column list from the old table's PRAGMA | smallest change; it names only the old table's columns. A rebuilt db that already has `cylinder_count` (33 names, NOT NULL sensors) would lose its counts; no code in the repo can produce such a db (the builder DDL has nullable sensors, the shipped db and the fixture have 32 names). Recorded as a residual risk |
| C3 | backfill set | `cylinder_count IS NULL` rows (every row when the column is absent) | update all rows with a `CASE` | the NULL filter is in both the SELECT and the UPDATE, so a non-NULL count is never touched |
| C4 | `backfilled` value | `rowcount` of the backfill `executemany` | `len(fills)` | it reports rows changed, not rows planned |
| C5 | digest form | `SELECT *` ordered by `engine_code`, `[type name, value]`, compact JSON | an explicit column list | "every column": a later column change must re-pin the digest |
| C6 | R1 comment | a preceding `--` line | a trailing comment | matches the `has_maf/has_map` comment beside it |
| C7 | red-run order | R6 order as written (tests before DDL) | add the column in the test fixture when absent | that would be dead code after the merge; the intended-reason evidence is the step-9 mutants |

**Optional additions for Cowork to approve or strike** (each is +1 test; counts in § 5 include them):
- O1. The R4 PIN "vref NULL, map 6 → 6" is parametrised over `None` and `0` (R3 says 0 also keeps the map's count).
  Without it, mutant M11 has no killing test.
- O2. `test_db_without_cylinder_count_is_rebuilt`: the shipped db's own path (32 names, nullable sensors). The fixture
  db rebuilds anyway because its sensors are NOT NULL, so no R4 test reaches this branch. Kills M3.
- O3. `test_other_column_difference_refuses` (`# PIN`): one extra column → `RuntimeError`. Passes on the base (old
  behaviour). Kills M2b.

### 3. Population, false pass and false fail of each rule

| rule | checked on (command) | will run over | false pass | false fail | changes later steps |
|---|---|---|---|---|---|
| R2 backfill | shipped engine_ref 1,274 rows × extract 1,498 rows / 1,306 codes; my stdin re-derivation → 1,225 (P2) | the same, step 6 `$PY tools/merge_tecdoc_extract.py` | a vref row and an extract code that share a normalised code but are different engines: the count is filled anyway (brand is ignored by R2). One displacement disagreement > 50 cc: `M96_03` PORSCHE 3,387 vs 3,596 cc, 6 in both, so the count is right | a code with two stated counts stays NULL; on the real population that set is empty, so only the fixture test exercises it | yes: steps 7, 9 and the digest all read the merged `vref.db` |
| R2 G2 early return | coalesced rows not in vref: `cylinder_heuristic` 34 → 0 | step 6 | a TecDoc count that is wrong is inserted without a heuristic check (R3 prefers TecDoc by ruling) | none for a stated count. Bank test (iii) now sees only blank-count codes: 1 real code (`SFZ`), already `in_vref`, so (iii) evaluates no real code | yes: 34 new rows |
| R2 guard | the shipped db (32 names, nullable sensors) and the fixture db (32 names, NOT NULL sensors) | the same | a 32-name db of another meaning: none exists | none | no |
| R3 decoder | 1,131 real VINs, R3-exact patch on Cowork's rehearsal db → 71/1/11/0; 82 literal VINs in the vinlab, dnalab, wired and ui test trees → 1 change (below) | the 1,131 VINs (step 6 script, step 4) and all 4 suites (steps 1, 3) | a TecDoc count that is wrong replaces a right map count; the R5 list shows every case for review | the 49 NULL rows keep a map count that may be wrong (T-VINA-11b) | yes: the vinlab, dnalab, wired and ui suites see it |
| digest test | — (value exists only after step 6) | the shipped engine_ref after step 6: 1,308 rows × 33 columns; `vref.db` has no other table | a change outside engine_ref data (index definitions, page layout) | a later legitimate merge or schema change: intended, it forces a re-pin | no |

### 4. Tests (R4), with the predicted step-2 red result

`tests/unit/test_vref_banks_induction.py` (fixture rows by `vref_copy` on a `tmp_path` copy; real VINs on the shipped db):
| test | content | step-2 red (base) |
|---|---|---|
| T-D1 `test_vref_count_replaces_map_count` NEW | `V6_VIN` (XFX, map V6/6, MY 2008, window 2000-2020), `UPDATE … SET cylinder_count = 4 WHERE engine_code = 'XFX'` → 4 | `OperationalError: no such column` |
| T-D2 `test_null_or_zero_vref_count_keeps_map_count[None, 0]` NEW `# PIN` (O1 adds `0`) | `WAUZZZ4BZYN125879` (AEB, map V6/6, row window 1995-2006), count set NULL / 0 → 6 | `no such column` |
| T-D3 `test_vref_count_with_blank_map_count_skips_the_heuristic[1198, 3000]` NEW | `AZQ_VIN` (map blank count, displacement and configuration): `UPDATE … SET cylinder_count = 6, induction_type = NULL, displacement_cc = ? WHERE engine_code = 'AZQ'` → count 6, `NATURALLY_ASPIRATED`, 1 bank. The heuristic would give I3 TURBOCHARGED at 1,198 cc and V6 (2 banks) at 3,000 cc | `no such column` |
| T-D4 `test_real_vin_takes_the_tecdoc_count[AEB, NG, H25A]` NEW | shipped db: `WAUZZZ4BZYN125879` 4 cyl / 1 bank, `WAUZZZ8GZNA003486` 5 / 1, `JSAFTD62V00115689` 6 / 2 | AEB `6 == 4`, NG `6 == 5`, H25A `0 == 6` fail |

Existing tests there keep passing: `AZQ_ROW` is an `INSERT OR REPLACE` without the column, so `cylinder_count` is NULL
and the fallback still runs in the two induction tests.

`tests/unit/test_vref_tecdoc_merge.py` (fixture db: `PRE_MERGE_DDL`, 72 rows including `5FR`):
| test | content | step-2 red (base) |
|---|---|---|
| T-M1 `test_null_count_is_backfilled_from_a_single_count_code` NEW | extract `5FR` count 4 (two brands, both 4) → `5FR` row 4; `report.backfilled == 1` | `KeyError`/`AttributeError` |
| T-M2 `test_two_count_code_leaves_the_count_null` NEW | extract `5FR` BRANDA 4, BRANDB 6 → NULL; `backfilled == 0` | `KeyError` |
| T-M3 `test_g2_runs_on_the_coalesced_row` REBUILT | BRANDA `ZZ2GTW` 3,000 cc, count blank, is_v_engine 0; BRANDB 3,000 cc, count 6, is_v_engine 0; map TESTBRAND I4, blank count and displacement → inserted | `inserted == ()` (G2 (iii) fires) |
| T-M4 `test_stated_count_is_kept` NEW | run 1: extract `5FR` 4 → 4; run 2: extract `5FR` 6 → still 4, `backfilled == 0` | `KeyError` |
| T-M5 `test_new_row_carries_the_coalesced_count` NEW | `ZZ2CNT` BRANDA blank, BRANDB 4 → row 4; `ZZ9NEW` with count blank → NULL | `KeyError` |
| T-M6 `test_second_run_backfills_nothing` NEW | run 1 extract `5FR` 4 → `backfilled == 1`; run 2 same → 0, `inserted == ()`, file sha256 unchanged | `AttributeError` |
| T-M7 `test_cylinder_heuristic_two_bank_hint_alone_is_skipped` KEPT, name and skip | `ZZ3VEE` count now blank | passes (pre-existing behaviour) |
| T-M8 `test_cylinder_heuristic_two_bank_hint_with_stated_count_is_inserted` NEW twin | `ZZ3VEE` count 6 → inserted, `cylinder_heuristic == ()`, row count 6 | `inserted == ()` |
| T-M9 `test_existing_rows_keep_every_value` MODIFIED | compares every column except `cylinder_count` | passes (column absent) |
| T-M10 `test_shipped_engine_ref_matches_the_pinned_digest` NEW | shipped table: 1,308 rows; sha256 of the canonical dump (C5) = the value recorded at step 6 | `1274 == 1308` |
| T-M11 `test_db_without_cylinder_count_is_rebuilt` NEW (O2) | merge once, `ALTER TABLE engine_ref DROP COLUMN cylinder_count` (SQLite ≥ 3.35), merge with `5FR` 4 → `schema_rebuilt`, PRAGMA equals the builder, `5FR` 4 | `no such column` on the DROP |
| T-M12 `test_other_column_difference_refuses` NEW `# PIN` (O3) | merge once, `ADD COLUMN extra INTEGER`, merge → `RuntimeError` | passes (old guard refuses too) |

`test_inserts_new_code`, `test_stated_na_heuristic_code_is_inserted`, `test_schema_matches_builder`,
`test_shipped_original_rows_match_the_pinned_base_digest` (explicit 32 columns) and
`test_real_vin_gains_row_with_tecdoc_displacement` (asserts displacement, air metering and O₂ only; X10XE count goes 4
→ 3, not asserted) need no change.

### 5. Predicted counts

- Step 2: base 36 + banks file 8 (T-D1 1, T-D2 2, T-D3 2, T-D4 3) + merge file 9 (T-M1, M2, M4, M5, M6, M8, M10, M11,
  M12) = **`53 passed`**. Without O1/O2/O3: `50 passed`.
- Step 1: 354 + 17 = **`371 passed, 8 skipped`**. Without O1/O2/O3: `368 passed, 8 skipped`.
- Step 3: **P5 unchanged** (dnalab `27 passed`, wired `41 passed`, ui `30 passed`). Evidence: a stdin script collected
  every 17-character VIN literal in `labs/dnalab/tests`, `apps/wired/tests`, `apps/ui/tests` and `labs/vinlab/tests`
  (82 VINs) and decoded each before and after with the R3-exact patch on the rehearsal db. One changed:
  `W0L0SBF08X4314007` (X10XE, cylinder_count 4 → 3), used only by `test_real_vin_gains_row_with_tecdoc_displacement` in
  vinlab, which does not assert the count. **No dnalab, wired or ui test changes value; no fixture there is touched.**
- Step 4: `vref outcome: {'no_engine_code': 12, 'not_in_vref': 468, 'out_of_window': 72, 'row_applied': 579}` (P3). The
  15 VINs that leave `not_in_vref`: 11 apply a row (H25A 1, HDZ 8, 206KA 2) and 4 fall out of window (G4HCE 1, 99H 2,
  HDY 1; none of them changes a decoded field).
- Step 5: `inserted 0 rows; cylinder counts filled 0; engine_ref now 1308 rows; schema rebuilt: no`; no `vref.db` status
  line; `All checks passed!`.
- Merge first run (step 6): `inserted 34 rows; cylinder counts filled 1225; engine_ref now 1308 rows; schema rebuilt:
  yes`; skip lines as P3.
- Decode diff (R5): `cylinder_count` 71, `number_of_banks` 1 (H25A), displacement 11 (H25A 1, HDZ 8, 206KA 2); induction,
  euro, O₂ type, air metering 0. Attribution: a change on a VIN whose row existed comes from the backfilled
  `engine_ref.cylinder_count` (extract `cylinder_count`); on H25A, HDZ and 206KA it comes from the inserted row
  (`cylinder_count`; H25A banks from `is_v_engine` 1; displacement from `displacement_cc`). The RESULT lists all of them.

### 6. Mutants (step 9: copy the file to `C:/4DApp/recheck/T-VINA-16/mut/`, edit the copy, copy it over, run the named test, `git restore`)

| id | rule | mutant | killed by |
|---|---|---|---|
| M1 | R1 | `cylinder_count INTEGER NOT NULL DEFAULT 0` | T-M2 (0 is not None) |
| M2 | R2 guard | exact equality only (old guard) | T-M1 (`RuntimeError`) |
| M2b | R2 guard | accept any superset of the 32 names | T-M12 (O3) |
| M3 | R2 rebuild trigger | rebuild only on NOT NULL sensors | T-M11 (O2) |
| M4 | R2 backfill, one count | fill when ≥ 1 distinct count (take the first) | T-M2 |
| M5 | R2 backfill, non-NULL kept | drop `IS NULL` from the SELECT and the UPDATE | T-M4 |
| M6 | R2 new rows | `_new_row` writes `"cylinder_count": None` | T-M5 |
| M7 | R2 G2 stated count | delete the `row["cylinder_count"]` early return | T-M8 |
| M8 | R2 G2 coalesced row (named by R4) | `_skip_reason` calls `_g2_cylinder_heuristic(group[0], map_rows)` | T-M3 |
| M9 | R2 report | `backfilled=0` | T-M1 |
| M10 | R3 | delete the three R3 lines | T-D1 (`6 == 4`), T-D4[AEB] |
| M11 | R3, 0 keeps the map | `isinstance(vref_cylinders, int)` without `> 0` | T-D2[0] (AEB: fallback gives 4, not 6) (O1) |
| M12 | digest | `UPDATE engine_ref SET cylinder_count = 8 WHERE engine_code = 'AEB'` on the shipped db; `git restore labs/vinlab/vinlab/data/vref.db` | T-M10 |

Each mutant's test runs with `--basetemp=C:/4DApp/recheck/T-VINA-16/pt/m<N>`. After each: `git restore` the file (and the
db for M12), then `git status --porcelain` must be empty apart from the note and the RESULT.

### 7. Commands and the paths they write

- Edits (steps 2-5): the five files in `### Files to touch ###`. Step 6 writes `labs/vinlab/vinlab/data/vref.db` (via the
  tool), then the digest constant in `test_vref_tecdoc_merge.py`.
- pytest: `--basetemp=C:/4DApp/recheck/T-VINA-16/pt/{red,v,t,dnalab,wired,ui,m1…m12}`; always `PYTHONDONTWRITEBYTECODE=1`
  and `-p no:cacheprovider`.
- Inner loop on each edited `.py`: `$PY -m py_compile`, `py -m ruff check`, `py -m ruff check --select S`, then
  `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe <file>`.
- Step 8 commit: `git add` the 6 paths by name, then `git -c user.name=Claude -c user.email=noreply@anthropic.com commit -m
  "fix(T-VINA-16): …"` as its own command.
- Step 6/R5 scripts are stdin scripts: they write nothing. Mutant copies: `C:/4DApp/recheck/T-VINA-16/mut/`.
- Note and `labs/vinlab/tasks/results/RESULT_T-VINA-16.md` at the finish line. No push.

### 8. Residual risks named now

- C2: a rebuilt db that already has the column would lose its counts (no such db can be produced in the repo).
- TecDoc counts that disagree with the map are taken on trust by ruling (R3). Checked against TecDoc's own displacement
  and `is_v_engine` (stdin read of the extract and the map): `346KB` extract 3,430 cc, 6, not V (map 3.4 V8/8);
  `508S1` 4,941 cc, 8, V (map 4.9 V12/12); `366S1` 3,535 cc, 6, not V (map 3.5 V8/8); `M139` 4,244 cc, 8, V (map 4.2
  V6/6); `X10XE` 973 cc, 3 (map 1.4 I4/4); `206S4` 1,991 cc, 6 (map 2.0 I4/4); `C20NE` 1,998 cc, 4 (map 3.6/6, config
  `I4` or blank). In each the TecDoc row agrees with itself and the map does not; the map errors stay T-VINA-11b's.
  Not checked: the other 64 changed VINs individually; the R5 list in the RESULT gives each one with its field.
- Cowork's `survey.py` imports `M.INSERT_ROW`; after R2 its rehearsal insert names `cylinder_count` before the column
  exists. It is a pre-build survey, so this is noted only.

## Plan round 2

Approved with O1, O2 and O3 (all kept) and corrections C1-C5 (correction 01). Each change:
- **C1** (step 6): the decode diff compares three field sets with `survey.out` S5 (cylinder 71, banks 1, displacement
  11) and asserts their union is 71 VINs. It replaces "must be equal: 71 + 1 + 11" in § 1.
- **C2** (`merge()`): after the column guard, a db whose columns include `cylinder_count` while `has_maf` or `has_map`
  is NOT NULL raises `RuntimeError` before any write. With that refusal, `rebuild` is `"cylinder_count" not in names`
  (a 32-name db with NOT NULL sensors, the fixture, also lacks the column, so it still rebuilds). The C2 residual risk
  in § 8 is closed. NEW `test_counted_db_with_not_null_sensors_refuses` (T-M13): fixture db + `ADD COLUMN
  cylinder_count INTEGER` → `RuntimeError`, file sha256 unchanged. Mutant M13: delete the refusal → T-M13 fails.
- **C3** (step 6): the tool subprocess runs with `cwd=C:/4DApp/repo/labs/vinlab`.
- **C4** (T-M11, O2): works on the `db` fixture's `tmp_path` copy only; its comment says the first merge rebuilds the
  fixture with nullable sensors, so dropping the column reaches the 32-name, nullable-sensor branch (the shipped db's
  case).
- **C5** (`_g2_cylinder_heuristic`): the early return tests the parsed count:
  `stated = _int_or_none(row["cylinder_count"])`, `if (stated is not None and stated > 0) or not row["displacement_cc"]:
  return False`. T-M7 is parametrised over `""` and `"0"`; both skip. Mutant M14: raw truthiness
  (`if row["cylinder_count"] or …`) → T-M7[`"0"`] fails (inserted).

New counts: step 2 = 53 + 2 (T-M13, T-M7's second case) = **`55 passed`**; step 1 = 371 + 2 = **`373 passed, 8
skipped`**. Steps 3, 4 and 5 unchanged (P5; P3's reach line; the second-run line). Mutants: M1-M12 as § 6, plus M13
and M14.

## Build log (redispatch)

- **Step 2, red run** (tests written, no production edit): `pytest -q tests/unit/test_vref_tecdoc_merge.py
  tests/unit/test_vref_banks_induction.py --basetemp=…/pt/red` → `18 failed, 37 passed` (55 collected). Reasons, as
  § 4 predicted: `'MergeReport' object has no attribute 'backfilled'` (T-M1, M2, M4, M6, M11's twin), `KeyError:
  'cylinder_count'` (T-M5), `no such column: "cylinder_count"` (T-M11 DROP), `Regex pattern did not match` (T-M13: the
  old guard refuses with "columns differ"), `assert () == ('ZZ2GTW',)` (T-M3), `assert () == ('ZZ3VEE',)` (T-M8),
  `assert 1274 == 1308` (T-M10), `no such column: cylinder_count` (T-D1-T-D3, the shipped db before step 6), and T-D4
  `6 == 4`, `6 == 5`, `0 == 6`. T-M7 (both cases) and T-M12 passed on the base, as predicted (PIN, old behaviour).
- **Steps 3-5**: builder DDL (2 lines), tool, decoder (3 lines plus a comment). After them, before step 6: `10 failed,
  45 passed`. Nine were the shipped-db tests (no column yet). **One was not predicted:**
  `test_skips_code_already_in_vref` compares the whole `5FR` row with a pre-merge `before` that has no
  `cylinder_count` key, and its default extract row states 4, so R2 fills it. Changed it like R4 rules for
  `test_existing_rows_keep_every_value`: every column except `cylinder_count` (assumption A6). No assertion weakened:
  the column did not exist in `before`.
- **Step 6, the merge** (stdin script, `cwd=C:/4DApp/repo/labs/vinlab` for the tool, C3): tool printed `skipped in_vref:
  1226`, `collision: 9` (`1E 2GRFE A112A2000 A20NHT B6 FA20 JB K10B LFW`), `status: 0`, `no_my_start: 37`, `span_gap: 0`,
  `map_banks: 0`, `cylinder_heuristic: 0`, `inserted 34 rows; cylinder counts filled 1225; engine_ref now 1308 rows;
  schema rebuilt: yes` (P2, P3). Decode diff over `c6_lib.real_vins()`: decoded 1,131 before and after, 0 lost; changed
  `cyl` 71, `banks` 1, `disp` 11, union 71; induction, air, euro, O₂ 0. **C1:** each of the three VIN sets equals
  `survey.out` S5 (`equal True` ×3), union 71 = 71. Rows with a count: 1,259. Every change is attributed to its row
  (backfilled or inserted) in the RESULT's R5 list.
- **Digest:** `SELECT * FROM engine_ref ORDER BY engine_code`, 1,308 rows × 33 columns →
  `4ee7543717bfa80b95f32f97d584ca9390451c03138f25e3284d0251bfc13a42`, written into `SHIPPED_ROWS_SHA256`.
  `vref.db` sha256 prefix after the merge: `660e81961e887038`. `PRAGMA integrity_check` = `ok`; page_count 86,
  freelist 33 (the rebuild's dropped table; size only, 192,512 → 352,256 bytes).
- **Step 8:** commit `52b834f` (the six paths by name). **Step 9** then showed M13 killed only by an incidental
  `IntegrityError` (the fixture insert hits NOT NULL `has_maf`), not by the missing refusal. T-M13's extract was changed to
  a fill-only code (`5FR` 4), so the mutant merge writes and succeeds: `DID NOT RAISE RuntimeError`. Steps 1 and 2 re-run
  green (`373 passed, 8 skipped`; `55 passed`); commit `324fd5a`.

### Mutants (step 9; copy in `C:/4DApp/recheck/T-VINA-16/mut/<id>_<file>`, copied over, named test, `git restore`)

| id | rule | mutant | named test | result |
|---|---|---|---|---|
| M1 | R1 | `cylinder_count INTEGER NOT NULL DEFAULT 0` | `test_two_count_code_leaves_the_count_null` | 1 failed: `assert 0 is None` |
| M2 | R2 guard | `if names != builder_names:` | `test_null_count_is_backfilled_from_a_single_count_code` | 1 failed: `RuntimeError: engine_ref columns differ` |
| M2b | R2 guard | `if not names >= builder_names - {"cylinder_count"}:` | `test_other_column_difference_refuses` | 1 failed: `DID NOT RAISE RuntimeError` |
| M3 | R2 rebuild | `rebuild = any(notnull … has_maf/has_map)` | `test_db_without_cylinder_count_is_rebuilt` | 1 failed: `no such column: cylinder_count` |
| M4 | R2 one count | `if len(values) >= 1` | `test_two_count_code_leaves_the_count_null` | 1 failed: `assert 1 == 0` |
| M5 | R2 non-NULL kept | drop `IS NULL` from `NULL_COUNT_CODES` and `BACKFILL_COUNT` | `test_stated_count_is_kept` | 1 failed: `assert 1 == 0` |
| M6 | R2 new rows | `"cylinder_count": None` | `test_new_row_carries_the_coalesced_count` | 1 failed: `assert None == 4` |
| M7 | R2 G2 stated count | `if not row["displacement_cc"]:` | `test_cylinder_heuristic_two_bank_hint_with_stated_count_is_inserted` | 1 failed: `assert () == ('ZZ3VEE',)` |
| M8 | R2 G2 coalesced row | `_g2_cylinder_heuristic(group[0], map_rows)` | `test_g2_runs_on_the_coalesced_row` | 1 failed: `assert () == ('ZZ2GTW',)` |
| M9 | R2 report | `backfilled=0,` | `test_null_count_is_backfilled_from_a_single_count_code` | 1 failed: `assert 0 == 1` |
| M10 | R3 | delete the three R3 lines | `test_vref_count_replaces_map_count` | 1 failed: `assert 6 == 4` |
| M11 | R3, 0 keeps the map | `if isinstance(vref_cylinders, int):` | `test_null_or_zero_vref_count_keeps_map_count[0]` | 1 failed: `assert 4 == 6` |
| M12 | digest | `UPDATE engine_ref SET cylinder_count = 8 WHERE engine_code = 'AEB'` on the shipped db | `test_shipped_engine_ref_matches_the_pinned_digest` | 1 failed: `'3cbbf67d78c1…' == '4ee7543717bf…'` |
| M13 | C2 | delete the refusal | `test_counted_db_with_not_null_sensors_refuses` | 1 failed: `DID NOT RAISE RuntimeError` (after `324fd5a`; before it, `IntegrityError`) |
| M14 | C5 | `if row["cylinder_count"] or not row["displacement_cc"]:` | `test_cylinder_heuristic_two_bank_hint_alone_is_skipped[0]` | 1 failed: `assert ('ZZ3VEE',) == ()` |

After each: `git restore` of the file (the db for M12); `git status --porcelain` = the note only.

## Assumptions worked past (redispatch)

- A6. `test_skips_code_already_in_vref` (not named by the plan or R4) now compares every column except
  `cylinder_count`, the same ruling R4 gives `test_existing_rows_keep_every_value`. Its intent (an in-vref code is
  skipped and its row keeps its values) is unchanged; the count fill is R2's rule. Test count unchanged.
- A7. T-M13 uses a fill-only extract (`5FR` 4) so that mutant M13 fails on the missing refusal, not on an incidental
  insert error. Same test name and count.
- A8. `backfilled` is `executemany(...).rowcount` only when `fills` is non-empty, else 0, so an empty `executemany`
  can never report −1 (Cowork measured 0; this makes it independent of the driver).

## VERIFICATION GATE

| step | command (from `### Verification ###`) | expected | actual |
|---|---|---|---|
| 1 | vinlab suite, `--basetemp=…/pt/v` | `373 passed, 8 skipped` | `373 passed, 8 skipped in 7.59s` |
| 2 | the two named files, `--basetemp=…/pt/t` | `55 passed` | `55 passed in 3.74s` |
| 3 | dnalab / wired / ui | `27 passed` / `41 passed` / `30 passed` (P5) | `27 passed in 0.97s` / `41 passed in 3.17s` / `30 passed in 3.20s` |
| 4 | `reach.py` from `audit/scratch/C6` | `{'no_engine_code': 12, 'not_in_vref': 468, 'out_of_window': 72, 'row_applied': 579}` | identical |
| 5 | second merge run | `inserted 0 rows; cylinder counts filled 0; engine_ref now 1308 rows; schema rebuilt: no` | identical |
| 5 | `git status --porcelain labs/vinlab/vinlab/data/vref.db` | no line | no line (sha256 prefix `660e81961e887038` before and after) |
| 5 | `C:/4DApp/.venv-loop/Scripts/ruff.exe check` (5 files) | `All checks passed!` | `All checks passed!` |
| 5 | `git log --oneline 3c2d512..HEAD` | spec and ledger commits, then mine | `324fd5a`, `52b834f`, `96d8a43`, `1bac3f3`, `d681469`, `53a06db` |
| 5 | `git status --porcelain` | the note and the RESULT | the note and the RESULT (pasted in the RESULT) |

Previous decisive failures now absent: `vref outcome` no longer `not_in_vref: 483` (now 468); the merge no longer skips 34
codes as `cylinder_heuristic` (now 0); the decoder no longer gives AEB 6, NG 6, H25A 0 (now 4, 5, 6).

Task-end gate (skill): py_compile clean on the 5 `.py` files; `py -m ruff check` clean; `py -m ruff check --select S`
on the 3 production files: 5 × S608 in `tools/build_vref_db.py` lines 401-481, **pre-existing** (the same 5 on
`git show HEAD:labs/vinlab/tools/build_vref_db.py | py -m ruff check --select S --stdin-filename build_vref_db.py -`
before the edit; not my lines). pyright (1.1.410, `--pythonpath` the venv) on the 5 files: `1 error`, `Import
"mysql.connector" could not be resolved` at `build_vref_db.py:308`, **pre-existing** (line 306 on the base copy
`C:/4DApp/recheck/T-VINA-16/mut/build_vref_db.base.py`, same error). Import sanity: `from wired import diagnose` → `import
ok`. `audit/tools/isolation.py` → `violations: 4` (unchanged). `baseline.sh` and the repo-wide suites: **NOT RUN** (the
task makes them report-only; Cowork runs them at review). **Verdict: CLEAN-WITH-FINDINGS** (the findings are the
pre-existing S608 and pyright lines above).

## CODE REVIEW

- **Scope:** `git diff --stat 96d8a43..HEAD` = the six `### Files to touch ###` paths only. The builder change is the
  two DDL lines (R1). No map, dnalab, wired or ui file is touched (Plan § 5: no value there changes; step 3 confirms).
- **Contracts / consumer:** `engine_ref.cylinder_count` is read by `decoder.py::decode_vin_payload` (R3) into
  `VinDNA.cylinder_count`. `MergeReport.backfilled` is read by `main()` and 7 test lines (anti-orphan grep outside the
  tool: 7 hits, all in `test_vref_tecdoc_merge.py`). `_stated_counts`, `ALL_CODES`, `NULL_COUNT_CODES`,
  `BACKFILL_COUNT` are each read inside `merge()`.
- **Provenance:** no new numeric boundary literal; `> 0` is R3's "positive integer".
- **Boundaries:** no new import in any file.
- **Correctness:** the guard accepts exactly two column sets; the C2 refusal comes before any write; backfill and insert
  share one `BEGIN IMMEDIATE` transaction after the rebuild; the backfill SQL filters `IS NULL` in both the SELECT and the
  UPDATE; R3 sits on the in-window `db_dict` (`{}` when the row is absent or out of window), so a count never applies
  outside the row's window. G2's early return parses the count (C5). A non-integer extract count raises `ValueError` in
  `_stated_counts` and `_int_or_none` (the extract has none: values are blank or 2-12).
- **Tests:** no network; the fixture tests work on `tmp_path` copies (C4); the shipped-db tests are read-only.
- **Findings:** none blocking. Noted: the merged `vref.db` carries 33 free pages (no VACUUM; R2 says run the tool once).

## Revision 02

R4 "Ruled (02, review; revision before acceptance; test files only)". Base `daae97d`; commit `84c5aa0` (the test file
only, `git diff --stat daae97d..HEAD` = `test_vref_tecdoc_merge.py | 29 +++++-`). Tool, decoder, builder and `vref.db`
unchanged: sha256 prefixes `c9980aec5b9b4b4e`, `540b3452756e91e1`, `33d16e0b135f90bf`, `660e81961e887038` after every
mutant restore and at the finish line.

- **Survival before the edit** (copy over, whole merge file, `git restore`): M15 `38 passed`, M16 `38 passed`. Both
  mutants survived the `324fd5a` tests, as the review found.
- **(a)** `test_counted_db_with_not_null_sensors_refuses` is parametrised over `not_null` = `("has_maf",)`,
  `("has_map",)`, `("has_maf", "has_map")` (ids `has_maf`, `has_map`, `both`). Each case rebuilds the `db` fixture's
  `tmp_path` table from `PRE_MERGE_DDL` with the other sensor made nullable, adds `cylinder_count`, copies the 72 rows,
  and asserts the two `PRAGMA table_info` notnull flags before the merge (so a no-op DDL replace cannot pass silently).
  Each case raises `RuntimeError` matching `cylinder_count` and leaves the sha256 unchanged.
- **(b)** `test_conflicting_counts_across_spellings_leave_null`: extract `5FR` 4 (BRANDA) and `5 FR` 6 (BRANDB); `5FR`
  stays NULL and `backfilled` is 0.
- **Green, after the edit:** the 4 new items `4 passed`; merge file 41 items (was 38). Step 2 `58 passed in 3.93s`; step
  1 `376 passed, 8 skipped in 7.79s` (the ruling's counts).

| id | rule | mutant | named test | result |
|---|---|---|---|---|
| M15 | C2, one sensor is enough | `all(notnull …)` in place of `any(notnull …)` (`merge_tecdoc_extract.py:405`) | `test_counted_db_with_not_null_sensors_refuses` | `2 failed, 1 passed`: `[has_maf]` and `[has_map]` `DID NOT RAISE RuntimeError`; `[both]` passes, as derived in readiness (c) |
| M16 | R2, one count per normalised code | `counts[r["engine_code"]].add(…)` in `_stated_counts` (`:350`) | `test_conflicting_counts_across_spellings_leave_null` | `1 failed`: `assert 1 == 0` (`backfilled=1`) |
| M13 (re-run) | C2 refusal deleted (lines 405-407) | the parametrised refusal test | `test_counted_db_with_not_null_sensors_refuses` | `3 failed`, each `DID NOT RAISE RuntimeError` |

Copies in `C:/4DApp/recheck/T-VINA-16/mut/` (`M15_`, `M16_`, `M13r2_merge_tecdoc_extract.py`); after each run `git
restore labs/vinlab/tools/merge_tecdoc_extract.py`, `git status --porcelain` = the note and the RESULT only. Named
mutants now 17 (M1-M16 and M2b).

### Assumptions worked past (revision 02)
- A9. The ruling says "build each variant table" but not how. SQLite cannot drop a NOT NULL constraint in place, so
  each case renames the fixture table, recreates it from `PRE_MERGE_DDL` with one `NOT NULL DEFAULT 0` removed, adds
  `cylinder_count` and copies the rows with `SELECT *, NULL`. The `both` case uses the same path with no removal, so it
  equals the old single test. A notnull-flag assertion checks each variant before the merge.
- A10. I also re-ran M13 on the rewritten test (not asked by the ruling), because its named test changed shape.

### VERIFICATION GATE (revision 02)

| step | expected | actual |
|---|---|---|
| 1 | `376 passed, 8 skipped` | `376 passed, 8 skipped in 7.79s` |
| 2 | `58 passed` | `58 passed in 3.93s` |
| 3 | `27 passed` / `41 passed` / `30 passed` (P5) | `27 passed in 0.99s` / `41 passed in 3.31s` / `30 passed in 3.24s` |
| 4 | `{'no_engine_code': 12, 'not_in_vref': 468, 'out_of_window': 72, 'row_applied': 579}` | identical |
| 5 | `inserted 0 rows; cylinder counts filled 0; engine_ref now 1308 rows; schema rebuilt: no` | identical |
| 5 | no `vref.db` status line | no line (prefix `660e81961e887038`) |
| 5 | ruff (`.venv-loop`, 5 files) `All checks passed!` | `All checks passed!` |
| 5 | `git log --oneline 3c2d512..HEAD` | `84c5aa0`, `daae97d`, `324fd5a`, `52b834f`, `96d8a43`, `1bac3f3`, `d681469`, `53a06db` |
| 5 | `git status --porcelain` | the note and the RESULT only |

Task-end gate on the one touched file: `py_compile` clean; `py -m ruff check` `All checks passed!`; pyright (1.1.410,
`--pythonpath` the venv) `0 errors, 0 warnings, 0 informations`; `py -m ruff check --select S`: 131 × S101 (pytest
`assert`) against 127 at `324fd5a`, so +4, each a new test assert. No production file changed, so the import sanity
line, `isolation.py` and the production S gate were not re-run (unchanged from the build gate above). **Verdict:
CLEAN-WITH-FINDINGS** (the pre-existing findings named in the build gate; revision 02 adds none).

### CODE REVIEW (revision 02)
- **Scope:** one file, `test_vref_tecdoc_merge.py` (+28 −1). The old test's name, comment and assertions are kept; it
  gains the parameter and the variant build. No tool, decoder, builder, `vref.db` or fixture change.
- **Isolation:** each new test fails on exactly its mutant (M15 on the two one-sensor cases, M16 on the conflicting
  spellings) and passes on the real code. Neither mutant failed any of the 38 earlier items.
- **Tests:** no network; every write goes to the `db` fixture's `tmp_path` copy (C4); the shipped digest is unchanged
  (step 2 includes `test_shipped_engine_ref_matches_the_pinned_digest`).
- **Findings:** none.

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| plan (read, baseline, surveys, plan) | 2026-11-05T10:42:56Z | 2026-11-05T10:55:00Z | 12 | ABSENT |
| build (redispatch: readiness, tests, red run, R1-R3, merge, verification, commits, mutants, note, RESULT) | 2026-11-05T11:14:30Z | 2026-11-05T11:29:28Z | 15 (898 s) | ABSENT |
| revision 02 (readiness, survival run, tests, steps 1-5, commit, mutants, note, RESULT) | 2026-11-05T11:55:46Z | 2026-11-05T12:01:03Z | 5 (317 s) | ABSENT |

Plan stop at 2026-11-05T10:55:00Z. `git status --porcelain`: only `?? labs/vinlab/tasks/progress_notes/T-VINA-16.md`.
Finish line at 2026-11-05T11:29:28Z: total 27 min (1,622 s, `date -u -d … +%s` arithmetic) against the 45-90 min
estimate and the 120 min stop rule; the tripwire did not fire. `git status --porcelain`: the note and
`labs/vinlab/tasks/results/RESULT_T-VINA-16.md` only.
Revision 02 finish line at 2026-11-05T12:01:03Z: 317 s (`date -u -d … +%s` arithmetic); task total 32 min (1,939 s)
against the 120 min stop rule; the tripwire did not fire. `git branch --show-current` = `fix/T-VINA-16`;
`git log --oneline daae97d..HEAD` = `84c5aa0`; `git status --porcelain` = the note and the RESULT only.
