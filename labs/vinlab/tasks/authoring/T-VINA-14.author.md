# T-VINA-14 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. **Decoder** on `b444481`: `_apply_vref_techmask` sets `banks = 2 if db_dict.get("is_v_engine") else 1` and so
   drops a map BOXER's second bank; `_cylinder_fallback` replaces NATURALLY_ASPIRATED with the heuristic's induction
   whether or not the row states it. Observed (survey § 4).
2. **The map's V/W is wrong on inline engines** that TecDoc marks `is_v_engine 0`: AEB 1,781 cc, NG 2,309 cc, 346KB,
   326S4, 366S1 (8 real VINs). Observed (survey § 4). So R1 trusts only the map's BOXER.
3. **Skipped real VINs** (94): collision 72, G2 (i) 15, G2 (ii) 3, no_my_start 4, G1 0. Observed (survey § 2).
4. **Collisions** (44 codes): 35 coalesce, 9 real conflicts; of the real ones only B6 reaches real VINs (3).
   Observed (survey § 2, § 3).
5. **Merge and reach** on a copy: P3. Observed (survey § 5). The reach counts do not depend on R1/R2 (the window
   check reads only `my_start`/`my_end`).

### Rulings and the tradeoff that lost ###
- R1 BOXER from the map only. Lost: "keep the map's banks unless vref says V" (8 real VINs would get a wrong second
  bank).
- Coalesce collisions in this row. Lost: a brand key in `lookup_engine_ref` (bigger change; 3 real VINs on the
  remaining real conflicts, classified too small for now).
- G2 (i) and the cylinder column moved to T-VINA-16 (15 real VINs, a schema change). Lost: one merge rerun.
- Difficulty 4 (no schema change), plan REQUIRED (decoder behaviour and a binary data file).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base `281 passed, 8 skipped` (Cowork, 2026-11-04, `b444481`) |
| step 2 | DEFERRED | `test_vref_banks_induction.py` does not exist; the merge file alone gives `20 passed` |
| step 3 | RAN | `27 passed`, `41 passed`, `30 passed` |
| step 4 | SIMULATED | `rehearse.py` on a copy prints P3's outcome line; `reach.py` on the base prints P1 |
| step 5 | SIMULATED | the rehearsal ran the tool's `merge` on a copy (inserted 40, 1,274 rows); a second run on the shipped file is the observable |

### Exclusivity ###
No other implementer runs. T-VINA-10 also edits `decoder.py`: it goes after this row.

### Progress hook ###
T-VINA-14: decoder keeps map BOXER banks and stated induction; merge coalesces 35 collisions; +40 rows, reach 568.

### Cold read ###
own pass 2026-11-04: P1-P6 measured · literals 5/5 found once (`csv_config.startswith("BOXER")`, the `banks = 2 if`
line, the three named merge tests, the tool's `engine_ref now` print, reach.py's `vref outcome:`) · 1c: 2 rulings
patched (coalesce exception worded as one reading; porcelain set names the hand-back record) · counts: inserted 40 =
G1 2 + G2 (ii) 5 + coalesced 35 − 2 newly `no_my_start` (35 → 37); cylinder_heuristic 34 = (i) 32 + (iii) 2 ·
traceability: criteria 1-4 → steps 1-5, R4 tests → criterion 1 · JUDGEMENT: 0.
cold read 2026-11-04: skipped, plan-gated (Plan: REQUIRED; the plan review and its second-model review cover it).

### Correction history ###
- **01 (2026-11-04, plan review; Plan: APPROVED with C1-C2).** Plan predictions equal Cowork's rehearsal (40 rows,
  reach 568) and add 3 attributed changes (RFJ euro4, RGX turbo ×2). Second review (codex after the DeepSeek route
  exited 1): APPROVE WITH CORRECTIONS, 2 MEDIUM test gaps, both upheld (C1 tool mutant for G2 (ii); C2 two collision
  PIN tests). Concern: RGX map keys of weak majority, carried to the RESULT and T-VINA-11. Record:
  `corrections/T-VINA-14_plan_correction_20261104.md`.
- **02 (2026-11-04, review; revision before acceptance).** Cowork's re-run equals the RESULT (293/8, 32, reach 568,
  0 existing rows changed, 40 new rows equal Cowork's independent rehearsal db, 0 mismatches). Second review (codex):
  APPROVE WITH CORRECTIONS, F1 MED (guards on the coalesced row untested), F2 LOW (blank-string induction untested).
  Cowork ran the three mutants: each leaves the two files at `32 passed`. Both upheld → R4 (02): three tests, test
  files only. No data effect (shipped rows equal the rehearsal; 0 blank-string inductions in `vref.db`).
