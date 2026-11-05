# T-VINA-16 — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **The decoder reads cylinders from the map only** on `3c2d512`: `_engine_attrs_from_csv` sets `cylinder_count`
   from `csv_cyl`; `_cylinder_fallback` runs `_infer_cylinder` only when that is 0. No vref column exists (S1).
   Observed.
2. **`engine_ref` has no cylinder column** and the builder holds no cylinder source (`grep -n cylind
   tools/build_vref_db.py`: no line). The extract states `cylinder_count` per brand row. Observed.
3. **Backfill population** (S2): 1,225 of 1,274 rows take a single extract count; 48 have no extract code; 1 has only
   blank counts. One filled row differs in displacement by more than 50 cc (`M96_03`), with the same 6 cylinders.
   Observed.
4. **G2** (S3): on the tip, the 34 `cylinder_heuristic` codes all state a count. With G2 False for a stated count, all
   34 insert and no other reason moves. Observed.
5. **Effect** (S5, reach rehearsal): 71 cylinder, 1 bank, 11 displacement, 15 reach changes; 0 induction, euro, O₂,
   air. The spot checks (AEB 4, NG 5, BMW M52 `206S4` 6, TU1 `HFX` 4, `X10XE` 3, H25A V6) match the engines.
   Observed; per-VIN attribution is the RESULT's (R5).
6. The survey had two key bugs (raw against normalised code). Both were fixed before these figures; `survey.out` is the
   fixed run. Observed.

### Rulings and the tradeoff that lost ###
- Backfill all existing rows from the extract. Lost: new rows only (the 71 wrong counts sit mostly on existing rows:
  AEB, NG, `206S4`, `HFX`).
- Backfill when the code states one count over all brands, regardless of other fields. Lost: only codes that coalesce
  (would drop codes whose brands differ only in fields the count does not depend on).
- A stated count beats the map's count. Lost: the map wins and the vref count only fills a blank (keeps AEB at 6).
- Banks stay T-VINA-14 R1. Lost: derive banks from the count (I6 against V6 needs configuration, which TecDoc does not
  state).
- Difficulty 5 (schema change, binary data, 71 decodes); plan REQUIRED; opus xhigh.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base `354 passed, 8 skipped` (Cowork, 2026-11-05, `3c2d512`, baseline.sh) |
| step 2 | RAN | base `36 passed` (merge file alone `27 passed`) |
| step 3 | RAN | `27 passed`, `41 passed`, `30 passed` |
| step 4 | SIMULATED | `reach_rehearsal.py` on the rehearsal db prints P3's line; `reach.py` on the base prints P1 |
| step 5 | SIMULATED | the survey's rehearsal db has 1,308 rows and 1,259 counts; a second run on the shipped file is the observable |

### Exclusivity ###
No other implementer runs. T-VINA-20 edits `tools/build_vref_db.py` after this row. The Linux main-merge review holds
`fix/T-MERGE-1` frozen; this row branches from it and does not push to it.

### Progress hook ###
T-VINA-16: engine_ref cylinder_count (1,259 stated), decoder prefers it; +34 rows, reach 579; table digest pinned.

### Cold read ###
own pass 2026-11-05: P1-P5 measured · literals found once (`csv_cyl`, `if cylinder_count == 0:`, the G2 (i) line,
`SELECT *`, the tool's `engine_ref now` print, reach.py's `vref outcome:`) · counts: 1,259 = 1,225 + 34; reach 579 +
468 + 72 + 12 = 1,131; 468 = 483 − 15 · traceability: criteria 1-4 → steps 1-5, R4 tests → criterion 1.
cold read: skipped, plan-gated (Plan: REQUIRED; the plan review and its second-model review cover it).

### Correction history ###
- **01 (2026-11-05, plan review; Plan: APPROVED with O1-O3 and C1-C5).** The plan's counts equal Cowork's survey
  (1,225 / 34 / 1,308 / 1,259; reach 579; decode 71/1/11). Second review (DeepSeek ds-flash): APPROVE WITH CORRECTIONS.
  F1 HIGH (empty `executemany` rowcount −1) not upheld: measured 0. F6 (M11 kill) not upheld: AEB heuristic = 4.
  Upheld: F2 (VIN set arithmetic), F3 (counted db with NOT NULL sensors loses counts → refuse), F4 (step-6 cwd), F5
  (O2 on a copy), latent `"0"` truthiness in G2. Record: `corrections/T-VINA-16_plan_correction_20261105.md`.
