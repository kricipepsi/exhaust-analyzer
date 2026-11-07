# T-VINA-6 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C6_20261017.md` F-C6-5 (HIGH). Ledger: "petrol guard on real data; measure first".
Rehearsal: `C:/4DApp/recheck/T-VINA-6/` (`measure_fuel.py`, `nonpetrol.csv`, `reach.py`, `rows.py`, `apply_fix.py`,
`test_h1_diesel_map_rows.py`, `rehearsal.patch`).

### Verified context ###
1. **Measure:** the T-VINA-13a extractor's indexing on `D:/4DLab/4DLabV2/DBS/1Q2019`: of the map's keys,
   `petrol=1501`, `non_petrol=27` (84 rows, every id `EngineType` `Diesel`), mixed 0, no hit 4353. Observed.
2. **Reach:** 1 of 1,364 real VINs (`JT111GJ9000023441`, Toyota 1KZ-TE); 0 of the 7 v7 corpus VINs. Observed.
3. **H1:** `decoder.py` `decode_vin_payload` raises on `_is_non_petrol(engine_row["fuel_system_type"])` right after
   `_resolve_engine`; `DIESEL` is a keyword. The `FuelDeliveryType(csv_fuel)` calls run after it. Observed.
4. **Independent of the unmerged AUD chain:** none of the row's files is in `git diff --name-only origin/main
   fix/T-AUD-18e` (212 files); base `origin/main` `8b4d343`. Observed.
5. **Rehearsal** (restored): vinlab `376 → 378 passed, 8 skipped`; new test `2 passed`, `2 failed` on the base map;
   wired `85`, ui `49` equal; map numstat `84 84`. Observed.

### Rulings and the tradeoff that lost ###
- **R1 data fix.** Lost: a decoder change (the guard is right; the data was wrong), and a code-family rule for diesel
  codes TecDoc does not key (no source) → T-VINA-6b with the electric brands.
- **R2 one test file.** Lost: editing `audit/scratch/C6` probes (audit evidence, not the lab's tests).
- Code/data row: second-model review at acceptance. Plan NONE, difficulty 2.
- **T-VINA-7 waits** for the operator's merge of the AUD chain: its files (`decoder.py`, `VIN_VOCABULARY.md`) are in it.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `378 passed, 8 skipped` |
| step 2 | SIMULATED | `2 passed`; base map `2 failed` |
| step 3 | SIMULATED | `85 passed`; `49 passed` |
| step 4 | SIMULATED | numstat `84 84`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-6: 84 engine-map rows of 27 TecDoc-diesel keys say DIESEL; H1 rejects them; new test.

### Cold read ###
own pass 2026-11-07: P1-P3 measured (facts 1, 2, 5) · `apply_fix.py` exits on any count other than 84 · traceability:
criteria 1-2 → steps 1-4 · 1c grep: "every" in P3 is the measured TecDoc fact · cold read: not triggered (d2, scripted)
· no finding.

### Correction history ###
- **Revision 02 (2026-11-07).** Second review ds-flash APPROVE WITH CORRECTIONS (`recheck/codex/T-VINA-6_review.md`).
  Upheld (re-derived): no real VIN and no petrol control in the test; the total 84 does not pin the key population →
  R3 (rehearsed: test `5 passed`; base map `3 failed, 2 passed`; vinlab `381 passed, 8 skipped`; ruff clean).
  Not upheld: BMW FE435 share 0.333 (the decoder already attributes 306D3 to that VDS; the row describes a diesel
  either way) and the cylinder/displacement fields of WL, J3, ZD30, 1KZ-TE, JP (that column is unreliable map-wide,
  e.g. KIA D3FA, a 3-cylinder, says 4; the engine code is the evidence). LOW items (ordering assertion, key-set
  fixture) too small. False negatives D4HE and the WL variants (1WL, PWL) → T-VINA-6b.
