# T-VINA-13b — plan correction 01 (Windows Cowork, 2026-11-04)

Plan: `repo/labs/vinlab/tasks/progress_notes/T-VINA-13b.md` § `## Plan`. Verdict: **APPROVED with corrections C1-C6**,
written into `repo/labs/vinlab/tasks/T-VINA-13b_vref_tecdoc_merge(5).md` (§ Rulings that bind, Files to touch). The task
file is the spec; this file is the approval record. Hand-back B8 (3 soft findings, all upheld, COWORK).

## Accepted from the plan
The merge with the builder DDL; the window `[start, end + 1]` with an open end at 2019; AMBIGUOUS rows in; guards G1
and G2; CoC NULL; the importlib load of `build_vref_db` with a placeholder `DBS_ROOT`; the 16 tests and mutants.

## Re-derived by Cowork
- B8 settling commands re-run: `NOT_V_ENGINE` holds `BOXER`; `decoder.py:364` gives one bank for `0`;
  `infer_cylinder('AZQ', 1.198, 'SKODA')` = `I3 TURBOCHARGED`; `my_start`/`my_end` have `notnull = 0`.
- **CoC:** the plan says the petrol CSV is absent. It is on `D:/4DLab/4DLabV2/DBS/docs/vehicles_petrol_specimens.csv`.
  Cowork ran `_enrich_from_csv` with `DBS_ROOT=D:/4DLab/4DLabV2/DBS` over the 1,307 extract codes: **0** gain a CoC
  value. The plan's outcome (CoC NULL) stands; its reason is corrected.
- **Positional readers (F4):** every `SELECT * FROM engine_ref` in the repo (`tecdoc_query.py:69,83`,
  `test_build.py:57`, `test_csv_suite.py:155`) uses `sqlite3.Row` by name.
- **Span gaps (F3):** of the multi-brand codes with identical fields, **0** have brand year spans with a gap of more
  than one year.
- **Blank `is_v_engine` (F5):** 15 extract rows; **0** of their codes have a map configuration starting `V`, `W` or
  `BOXER`.

## Second review (`C:/4DApp/recheck/codex/T-VINA-13b_plan_review.md`, ds-pro, embedded): APPROVE WITH CORRECTIONS
- **F1** (the builder's migration guard still adds `NOT NULL DEFAULT 0`, MEDIUM): **upheld** → **C1**: the guard
  (`build_vref_db.py:993-998`) adds both columns as plain `INTEGER`. Files to touch names it.
- **F2** (32 VINs MAF_ONLY → HYBRID_MAF_MAP, HIGH): **not upheld.** The decoder's unchanged heuristic derives
  `has_map` from TecDoc-stated turbo or supercharged induction or GDI, as it would from the same facts without a row.
  → **C2** clarifies R4: a change that the unchanged decoder derives only from a TecDoc-stated field counts as "from a
  stated TecDoc value". The RESULT lists those VINs with the stated field.
- **F3** (the union window over disjoint brand spans, MEDIUM): **upheld as a fail-closed guard, 0 today** → **C3**:
  skip a code whose brand year spans have a gap of more than one year; one test.
- **F4** (column reorder against positional readers, MEDIUM): **not upheld** (re-derived above).
- **F5** (blank `is_v_engine` with a V/W map, MEDIUM): **upheld as a fail-closed guard, 0 today** → **C4**: G1 also
  skips a code whose extract `is_v_engine` is blank and any map configuration starts `V`, `W` or `BOXER`. G2 (iii)
  drops the "map configuration is blank" qualifier. Round 2 reports the new G2 count and the real-VIN effect.
- **F6** (mutant M9 can survive test 9, LOW): **upheld** → **C5**: test 9's fixture window gives a bucket other than
  `ERA_MODERN`, and the test asserts that exact bucket.
- **C6 (Cowork):** the plan's CoC reason is corrected in the RESULT (the CSV is on `D:`; 0 codes match).

## Follow-ups registered (not this row's)
T-VINA-14: the decoder takes banks from a BOXER fact and keeps a vref-stated induction; then a rerun inserts the
guarded codes. T-VINA-15: the 13 existing vref rows with `has_maf = 0` and `has_map = 0` decode with neither sensor.

## Next
Add `## Plan round 2` to the note: C1-C6, the new G1/G2 counts, the inserted count and the `reach.py` prediction.
Then build without a second stop. One return at most.
