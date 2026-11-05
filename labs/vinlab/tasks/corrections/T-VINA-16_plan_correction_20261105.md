# T-VINA-16 — plan correction 01 (Windows Cowork, 2026-11-05)

Plan: `repo/labs/vinlab/tasks/progress_notes/T-VINA-16.md` § `## Plan`. Verdict: **APPROVED with corrections C1-C5**,
written into `repo/labs/vinlab/tasks/T-VINA-16_engine_ref_cylinder_count(5).md` (§ Routing, R4). The task file is the
spec; this file is the approval record. No hand-back.

## Accepted from the plan
R1 as the two DDL lines; R2 with `_stated_counts`, the NULL-only `BACKFILL_COUNT`, `backfilled` from `rowcount`, the
guard's two column sets, and the order rebuild → backfill → insert in one transaction; R3 inline in
`decode_vin_payload` on the in-window `db_dict`; choices C1-C7; assumptions A1-A4; tests T-D1…T-D4 and T-M1…T-M12;
optional additions **O1, O2 and O3 (all approved)**; mutants M1-M12; the predicted step 4 and step 5 lines.

## Re-derived by Cowork
- Every extract status is one the merge accepts (OK 1,422, FAMILY 34, AMBIGUOUS 41 with a count; AMBIGUOUS 1 blank),
  so "any status" in `_stated_counts` changes no real fill.
- An empty `executemany` reports `rowcount` 0 on this host (Python 3.14.6, SQLite 3.50.4).
- `infer_cylinder('AEB', 1.781, 'Audi')` = 4, I4, NA (`brand_rule`); the shipped AEB row is 1,781 cc, 1995-2006.
  So M11 (count 0 accepted) makes AEB decode 4 against T-D2[0]'s 6: killed.
- Counts: 1,225 + 48 + 1 = 1,274; 1,225 + 34 = 1,259; reach 579 + 468 + 72 + 12 = 1,131.

## Second review (`C:/4DApp/recheck/codex/T-VINA-16_plan_review.md`, DeepSeek ds-flash, embedded): APPROVE WITH CORRECTIONS
- **F1** (HIGH, empty `executemany` gives `rowcount` −1, T-M2 fails): **not upheld.** Measured 0 (above). T-M2's red
  and green runs will show it either way.
- **F2** (MEDIUM, "must be equal: 71 + 1 + 11" counts field changes, not VINs): **upheld.** → **C1.**
- **F3** (MEDIUM, a db with `cylinder_count` and NOT NULL sensors passes the guard and loses its counts on rebuild):
  **upheld** (no such db exists today, but the guard accepts it). → **C2.**
- **F4** (LOW, step 6 runs the tool from `audit/scratch/C6` by a relative path): **upheld.** → **C3.**
- **F5** (LOW, O2's rationale and copy discipline): **upheld.** → **C4.**
- **F6** (LOW, M11's kill not shown): **not upheld.** Re-derived above.
- **Latent** (G2's early return treats the string `"0"` as stated, R3 does not): **upheld.** → **C5.**

## Corrections
- **C1.** Step 6 compares three field sets with `survey.out` S5 (cylinder 71, banks 1, displacement 11) and asserts
  their union is 71 VINs.
- **C2.** `merge()` refuses a db whose columns include `cylinder_count` while `has_maf` or `has_map` is NOT NULL
  (`RuntimeError`, before any write). NEW test `test_counted_db_with_not_null_sensors_refuses`. Mutant: delete the
  refusal; the test fails.
- **C3.** Step 6 runs the tool with `cwd=C:/4DApp/repo/labs/vinlab` (or its absolute path).
- **C4.** O2 (`test_db_without_cylinder_count_is_rebuilt`) works on the `db` fixture's `tmp_path` copy, never the
  tracked `vref.db`. Its comment says the first merge rebuilds the fixture with nullable sensors, so dropping the column
  reaches the 32-name, nullable-sensor branch (the shipped db's case).
- **C5.** G2's early return tests the parsed count (`_int_or_none(row["cylinder_count"])`, positive), not the raw
  string. `test_cylinder_heuristic_two_bank_hint_alone_is_skipped` is parametrised over `""` and `"0"`: both skip.
  Mutant: raw truthiness; the `"0"` case fails.

## Counts after C1-C5
Merge file +2 tests (C2, C5's second case): step 2 **`55 passed`**; step 1 **`373 passed, 8 skipped`**. Step 3, 4 and 5
unchanged.

### Plan-time digest ###
Re-recorded for revision 02 at `324fd5a` (the build commits changed every file; the plan-time values were `ddbd269f1e0599eb`, `eac76884b6d52744`, `efa5c0654cfc3ce4`, `88d5818782b8acff`, `0f1f2a5ace2c0aa6`, `78ee90f39c2d4631`).

| path (from `C:/4DApp/repo`) | sha256 prefix |
|---|---|
| `labs/vinlab/vinlab/decoder.py` | `540b3452756e91e1` |
| `labs/vinlab/tools/merge_tecdoc_extract.py` | `c9980aec5b9b4b4e` |
| `labs/vinlab/tools/build_vref_db.py` | `33d16e0b135f90bf` |
| `labs/vinlab/vinlab/data/vref.db` | `660e81961e887038` |
| `labs/vinlab/tests/unit/test_vref_tecdoc_merge.py` | `e320dabd17096009` |
| `labs/vinlab/tests/unit/test_vref_banks_induction.py` | `34f7b1cbcee73249` |
