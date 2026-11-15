# Progress Note — T-AUD-22h

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-22h` (worktree per `T-AUD-22h.go.txt` lane rule) with spec commit `79c1e1b` (`git log --oneline fix/T-AUD-22g..HEAD`), `git status --porcelain` empty, `check_code_claims.py --group rest --files 'apps/*'` fails with `CLAIMS FAIL 209 error(s)` (all `uncovered`, P1=209, P2), `check_code_claims.py --group rest --files 'labs/*'` passes with `CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 210` (P5) and `out_of_scope 129 candidate(s) in 1 file(s)` (P3), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 209 errors from `check_code_claims.py --group rest --files 'apps/*'` are `uncovered` on the 209 in-scope non-auto candidates under `apps/` (`RK0001`–`RK0210` cover `labs/` only).
- **(c) Independently derived decisive expected value:** Direct scan of `candidates_rest.csv` (789 total rows) finds 202 non-auto `labs/` candidates, 129 non-auto out-of-scope candidates in `apps/ui/_sample_app_reference.py` (P3), and 209 non-auto in-scope `apps/` candidates across 6 files (`apps/ui/ui_payload.py` 93, `apps/ui/app.py` 58, `apps/wired/wired/composition.py` 40, `apps/wired/v7/load_corpus.py` 11, `apps/wired/v7/run_suite.py` 6, `apps/wired/wired/registry_guard.py` 1; P1=209, P4=202+209=411).
- **(d) No contradiction or missing decision:** Rulings R1–R8 and `T-AUD-22h.go.txt` lane rules align with `codeaudit/README.md`, `wikiaudit/README.md`, and `check_code_claims.py`; `claims_rest.csv` is UTF-8.
- **(e) Teach-back:** Append classified claim rows (or `NON_DOMAIN` rows) starting at `RK0211` in candidates order to `apps/wired/audit_tasks/codeaudit/claims_rest.csv` covering all 209 in-scope `apps/` P1 candidates, checking each citation against its cited in-repo document and linking `same_as` to GASLab wiki claims (`W0001`–`W1693`) or earlier `RK` claims where identical. Done is verified by `check_code_claims.py --group rest --files 'apps/*'` and `--group rest` printing `CLAIMS OK` with zero errors (`candidates 209` and `candidates 411`), `--files 'labs/*'` still printing P5, and `git diff` showing `0` removed lines.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-22h.go.txt` govern worktree branch naming (`agy/T-AUD-22h` instead of `fix/T-AUD-22h`), omit `git commit`/`git push`, and skip branch/log paste in RESULT.

## Step 1 Disclosure & Claims Summary
- **Appended rows:** `RK0211`–`RK0451` (**241** new claims covering all **209** non-auto in-scope `apps/` candidates in strict `candidates_rest.csv` order; 31 `_OBD_RAW_RANGES` tuples in `apps/wired/wired/composition.py` and 1 `min_value`/`max_value` widget pair in `apps/ui/app.py:746` split into `plausible min`/`plausible max` and `input min`/`input max` rows per R4).
- **Step 2 (`--group rest`) totals:**
  - `candidates 411 covered claims 451` (`202` `labs/*` + `209` `apps/*` in-scope; `210` baseline + `241` new)
  - `classes`: `ANALYSER_SPEC=203` (baseline 45 + new 158), `DIAGNOSTIC_THRESHOLD=36` (34 + 2), `INTERNAL_PARAMETER=46` (31 + 15), `NON_DOMAIN=140` (75 + 65), `PHYSICAL_CONSTANT=22` (21 + 1), `TYPICAL_RANGE=4` (4 + 0)
  - `suspect 38` (baseline 20 + new **18**), `same_as_wiki 5` (baseline 5 + new **0**), `same_as` to earlier `RK`: **80** new rows
  - `out_of_scope`: `129 candidate(s) in 1 file(s)` (`apps/ui/_sample_app_reference.py`)
- **Citations:**
  - Empty `citation` among new claims: **83** (`64` `NON_DOMAIN` arithmetic/layout/UI-step/empty defaults + `19` domain claims with no inline/spec citation: `9` corpus surrogate defaults/cutoffs in `load_corpus.py`, `7` VIN-17 / fallback-DNA constants in `composition.py`, `1` VIN-17 check in `app.py:329`, `2` `mode06_min_margin_pct` widget bounds in `app.py:746`)
  - `"citation not found"` count: **0** (every cited repo document exists and was verified)
  - Note on `K0231` (`apps/wired/wired/composition.py:527`): inline comment cites `GAS_VOCABULARY §3` for CoC target lambda midpoint, whereas `GAS_VOCABULARY.md §3` defines `ChemicalSignature` and CoC lambda ranges appear in `§11`; classified `NON_DOMAIN` (midpoint divisor `/ 2.0`) per R3 with comment documented in `citation`.
- **New `suspect` claims (18):**
  1. `RK0232` (`K0199`, `apps/wired/wired/composition.py:110`, `stft_idle_pct=-127.0 %`): SAE J1979 trim plausible min is `-100.0 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MIN`), not `-127.0 %`; same defect as `RK0191`.
  2. `RK0233` (`K0199`, `apps/wired/wired/composition.py:110`, `stft_idle_pct=127.0 %`): SAE J1979 trim plausible max is `+99.22 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MAX`), not `127.0 %`; same defect as `RK0192`.
  3. `RK0234` (`K0200`, `apps/wired/wired/composition.py:111`, `ltft_idle_pct=-127.0 %`): SAE J1979 trim plausible min is `-100.0 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MIN`), not `-127.0 %`; same defect as `RK0191`.
  4. `RK0235` (`K0200`, `apps/wired/wired/composition.py:111`, `ltft_idle_pct=127.0 %`): SAE J1979 trim plausible max is `+99.22 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MAX`), not `127.0 %`; same defect as `RK0192`.
  5. `RK0236` (`K0201`, `apps/wired/wired/composition.py:112`, `stft_2500_pct=-127.0 %`): SAE J1979 trim plausible min is `-100.0 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MIN`), not `-127.0 %`; same defect as `RK0191`.
  6. `RK0237` (`K0201`, `apps/wired/wired/composition.py:112`, `stft_2500_pct=127.0 %`): SAE J1979 trim plausible max is `+99.22 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MAX`), not `127.0 %`; same defect as `RK0192`.
  7. `RK0238` (`K0202`, `apps/wired/wired/composition.py:113`, `ltft_2500_pct=-127.0 %`): SAE J1979 trim plausible min is `-100.0 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MIN`), not `-127.0 %`; same defect as `RK0191`.
  8. `RK0239` (`K0202`, `apps/wired/wired/composition.py:113`, `ltft_2500_pct=127.0 %`): SAE J1979 trim plausible max is `+99.22 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MAX`), not `127.0 %`; same defect as `RK0192`.
  9. `RK0260` (`K0213`, `apps/wired/wired/composition.py:124`, `stft_load_pct=-127.0 %`): SAE J1979 trim plausible min is `-100.0 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MIN`), not `-127.0 %`; same defect as `RK0191`.
  10. `RK0261` (`K0213`, `apps/wired/wired/composition.py:124`, `stft_load_pct=127.0 %`): SAE J1979 trim plausible max is `+99.22 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MAX`), not `127.0 %`; same defect as `RK0192`.
  11. `RK0262` (`K0214`, `apps/wired/wired/composition.py:125`, `ltft_load_pct=-127.0 %`): SAE J1979 trim plausible min is `-100.0 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MIN`), not `-127.0 %`; same defect as `RK0191`.
  12. `RK0263` (`K0214`, `apps/wired/wired/composition.py:125`, `ltft_load_pct=127.0 %`): SAE J1979 trim plausible max is `+99.22 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MAX`), not `127.0 %`; same defect as `RK0192`.
  13. `RK0374` (`K0534`, `apps/ui/ui_payload.py:34`, `OBD_TRIM_MIN=-127.0 %`): SAE J1979 trim plausible min is `-100.0 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MIN`), not `-127.0 %`; same defect as `RK0191`.
  14. `RK0375` (`K0535`, `apps/ui/ui_payload.py:35`, `OBD_TRIM_MAX=127.0 %`): SAE J1979 trim plausible max is `+99.22 %` (`OBDLab_KG_Wiki.md §3.1, §4`, `FF_TRIM_MAX`), not `127.0 %`; same defect as `RK0192`.
  15. `RK0410` (`K0574`, `apps/ui/ui_payload.py:77`, `wideband AFR petrol stoichiometric factor=14.7 mass ratio`): own comment notes `GASLab`'s `AFR_STOICH` is `14.71` (`W0083`, `W1193`, `W1264`, `GAS_VOCABULARY.md §6`); `14.7` is commercial wideband petrol scale (cf. `W1102`).
  16. `RK0416` (`K0580`, `apps/ui/ui_payload.py:84`, `ADV_DECEL_CO_MAX=25.0 %`): `25.0 %` exceeds `GAS_VOCABULARY.md §2` 5-gas CO analyser envelope `0-15 % vol` (`W0061`, `W1185`, `GAS_CO_MAX = 15.0`) and stoichiometric air oxygen.
  17. `RK0445` (`K0613`, `apps/ui/ui_payload.py:323`, `obd_upstream_o2_val=0.0 V / lambda / AFR`): generic union tooltip `0.0-20.0` drifts from the 3 per-sensor widgets in `app.py:536-540` (`0.0-1.0 V`, `0.7-1.3 lambda`, `10.0-20.0 AFR`) and `FieldMap §7`, violating `SHIP_UI_CONTRACT_2026-07-07.md` Amendment 2026-07-08 (`tooltip min` drifts vs wideband `0.7 lambda` and `10.0 AFR`).
  18. `RK0446` (`K0614`, `apps/ui/ui_payload.py:324`, `obd_upstream_o2_val=20.0 V / lambda / AFR`): generic union tooltip `0.0-20.0` drifts from the 3 per-sensor widgets in `app.py:536-540` (`0.0-1.0 V`, `0.7-1.3 lambda`, `10.0-20.0 AFR`) and `FieldMap §7`, violating `SHIP_UI_CONTRACT_2026-07-07.md` Amendment 2026-07-08 (`tooltip max` drifts vs narrowband `1.0 V` and wideband `1.3 lambda`).

## VERIFICATION GATE
- Step 1 (`check_code_claims.py --group rest --files 'apps/*'`): `out_of_scope 129 candidate(s) in 1 file(s)` and `CLAIMS OK group=rest scope=apps/* candidates 209 covered claims 451`.
- Step 2 (`check_code_claims.py --group rest`): `classes ANALYSER_SPEC=203 DIAGNOSTIC_THRESHOLD=36 INTERNAL_PARAMETER=46 NON_DOMAIN=140 PHYSICAL_CONSTANT=22 TYPICAL_RANGE=4`, `suspect 38 same_as_wiki 5`, `out_of_scope 129 candidate(s) in 1 file(s)`, `CLAIMS OK group=rest candidates 411 covered claims 451`.
- Step 3 (`check_code_claims.py --group rest --files 'labs/*'`): `CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 451`.
- Step 4 (`git diff -- apps/wired/audit_tasks/codeaudit/claims_rest.csv` removed lines & `git status --porcelain`): `removed_lines=0`; only `claims_rest.csv` modified, plus new progress note and result files.

## CODE REVIEW
- Confirmed all 241 new claim rows (`RK0211`–`RK0451`) are appended in strict `candidates_rest.csv` order below `RK0210` in clean UTF-8 without modifying `RK0001`–`RK0210` (`removed_lines=0`), all cited repo files exist, `NON_DOMAIN` leaves `value..condition` empty, tuple/widget bounds follow R4, `same_as` points only to earlier `RK` rows on distinct `cand_id`s, and no out-of-scope (`_sample_app_reference.py`) rows were added.

## Time
- First action: `2026-11-15T21:10:11Z` (local wall-clock `22:10:11+01:00`)
- Verification complete: `2026-11-15T21:17:14Z` (local wall-clock `22:17:14+01:00`)
- Duration: `7 min` (`423 s`)

## Correction 1

### Readiness Challenge (Correction 1)
- **(a) Starting state matches task:** Branch `agy/T-AUD-22h` (worktree per `T-AUD-22h.go.txt` lane rule) with commits `79c1e1b`, `5bb8d53`, `5f2726f`, and `4461c46`, `git status --porcelain` empty, all precondition files `checked`, and `check_code_claims.py --group rest` printing `suspect 38 same_as_wiki 5`, `out_of_scope 129 candidate(s) in 1 file(s)`, `CLAIMS OK group=rest candidates 411 covered claims 451`.
- **(b) Test fails for intended reason:** At `5f2726f`, the five P7 rows (`RK0247`, `RK0249`, `RK0384`, `RK0386`, `RK0394`) and additional R9 `ANALYSER_SPEC` lab-bound divergences (`RK0268`, `RK0269`, `RK0399`, `RK0400`, `RK0404`, `RK0405`, `RK0431`, `RK0434`, `RK0435`) have empty `suspect` fields, so `suspect 38 < 43` (P6) and Step 5 would fail (`missing P7`).
- **(c) Independently derived decisive expected value:** Exhaustive comparison of all 158 `ANALYSER_SPEC` rows in `RK0211`–`RK0451` against `RK0001`–`RK0210` yields 14 R9 rows to mark (the 5 P7 rows plus 9 additional rows: `RK0268`, `RK0269`, `RK0399`, `RK0400`, `RK0404`, `RK0405`, `RK0431`, `RK0434`, `RK0435`), raising `suspect` from `38` to `52` (`>= 43`, P6) with `N = 14 >= 5` in Step 5.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R7 and R9 plus `T-AUD-22h.go.txt` lane rules are consistent; `claims_rest.csv` uses UTF-8 with LF (`\n`, 452 lines).
- **(e) Teach-back:** Populate only the `suspect` field of the R9-affected `ANALYSER_SPEC` rows in `RK0211`–`RK0451` (preserving all other fields, row count, and LF line ends) and update `T-AUD-22h.md` and `RESULT_T-AUD-22h.md` under `## Correction 1`. Done is verified by `check_code_claims.py` Steps 1–3 (`CLAIMS OK`, `suspect 52`), Step 4 (`0` removed lines vs `79c1e1b`), and Step 5 (`R9 OK changed 14 missing none` vs `5f2726f`).

### Updated Figures & R9 Suspect Rows
- **Step 2 (`--group rest`) totals after Correction 1:**
  - `candidates 411 covered claims 451` (unchanged)
  - `classes`: `ANALYSER_SPEC=203 DIAGNOSTIC_THRESHOLD=36 INTERNAL_PARAMETER=46 NON_DOMAIN=140 PHYSICAL_CONSTANT=22 TYPICAL_RANGE=4` (unchanged)
  - `suspect 52` (`20` baseline `RK0001`–`RK0210` + `18` run-1 `apps/` + **`14` R9** = **`32` new `apps/` suspects**), `same_as_wiki 5` (unchanged)
  - Empty `citation` among new claims: **83** (unchanged); `"citation not found"` count: **0** (unchanged)
- **R9 rows marked (14 `ANALYSER_SPEC` claims in `RK0211`–`RK0451`):**
  1. `RK0247` (`K0206`, `apps/wired/wired/composition.py:117`, `maf_gps_idle` plausible max `500.0 g/s`): differs from OBDLab `RK0188` (`mass_airflow_gps` plausible max `655.35 g/s`; cf. `RK0080` `0-655.35 g/s`). *(P7)*
  2. `RK0249` (`K0207`, `apps/wired/wired/composition.py:118`, `maf_gps_2500` plausible max `500.0 g/s`): differs from OBDLab `RK0188` (`mass_airflow_gps` plausible max `655.35 g/s`; cf. `RK0080` `0-655.35 g/s`). *(P7)*
  3. `RK0268` (`K0217`, `apps/wired/wired/composition.py:128`, `wideband_lambda_wot` plausible min `0.0 -`): differs from OBDLab `RK0020` (minimum plausible wideband lambda `0.7`; cf. `RK0086` `normalized_obd_lambda` `0.7-1.3`); raw COMLab WOT channel.
  4. `RK0269` (`K0217`, `apps/wired/wired/composition.py:128`, `wideband_lambda_wot` plausible max `3.0 -`): differs from OBDLab `RK0021` (maximum plausible wideband lambda `1.3`; cf. `RK0086` `normalized_obd_lambda` `0.7-1.3`); raw COMLab WOT channel.
  5. `RK0384` (`K0546`, `apps/ui/ui_payload.py:46`, `FF_RPM_MAX` input max `16383 rpm`): SAE J1979 PID `0x0C` freeze-frame encoding range (`0-16383.75 rpm`); differs from OBDLab `RK0182` (`engine_rpm` plausible max `8000 rpm`; cf. `RK0077` `0-8000 rpm`). *(P7)*
  6. `RK0386` (`K0548`, `apps/ui/ui_payload.py:48`, `FF_ECT_MAX` input max `215.0 °C`): SAE J1979 PID `0x05` freeze-frame encoding range (`-40` to `215 °C`); differs from OBDLab `RK0184` (`coolant_temp_c` plausible max `140.0 °C`; cf. `RK0078` `-40-140 °C`). *(P7)*
  7. `RK0394` (`K0558`, `apps/ui/ui_payload.py:58`, `FF_IAT_MAX` input max `215.0 °C`): SAE J1979 PID `0x0F` freeze-frame encoding range (`-40` to `215 °C`); differs from OBDLab `RK0204` (`intake_air_temp_c` plausible max `140.0 °C`; cf. `RK0088` `-40-140 °C`, `OBDLab_KG_Wiki.md §3.1` `80 °C`). *(P7)*
  8. `RK0399` (`K0563`, `apps/ui/ui_payload.py:63`, `FF_O2_V_B1S1_MIN` input min `0.000 V`): SAE J1979 PID `0x14`/`0x15` freeze-frame encoding range (`0.000-1.275 V`); differs from OBDLab `RK0015` (narrowband O2 minimum valid voltage `0.10 V` in `o2_normalizer.py`).
  9. `RK0400` (`K0564`, `apps/ui/ui_payload.py:64`, `FF_O2_V_B1S1_MAX` input max `1.275 V`): SAE J1979 PID `0x14`/`0x15` freeze-frame encoding range (`0.000-1.275 V`); differs from OBDLab `RK0016` (narrowband O2 maximum valid voltage `0.90 V` in `o2_normalizer.py`).
  10. `RK0404` (`K0567`, `apps/ui/ui_payload.py:70`, `UPSTREAM_O2_NARROWBAND_MIN` input min `0.0 V`): differs from OBDLab `RK0015` (narrowband O2 minimum valid voltage `0.10 V` in `o2_normalizer.py`).
  11. `RK0405` (`K0568`, `apps/ui/ui_payload.py:71`, `UPSTREAM_O2_NARROWBAND_MAX` input max `1.0 V`): differs from OBDLab `RK0016` (narrowband O2 maximum valid voltage `0.90 V` in `o2_normalizer.py`).
  12. `RK0431` (`K0595`, `apps/ui/ui_payload.py:100`, `ADV_MAF_GPS_MAX` input max `500.0 g/s`): differs from OBDLab `RK0188` (`mass_airflow_gps` plausible max `655.35 g/s`; cf. `RK0080` `0-655.35 g/s`); same bound as `RK0247`.
  13. `RK0434` (`K0598`, `apps/ui/ui_payload.py:103`, `ADV_LAMBDA_WOT_MIN` input min `0.0 -`): differs from OBDLab `RK0020` (minimum plausible wideband lambda `0.7`; cf. `RK0086` `normalized_obd_lambda` `0.7-1.3`); same bound as `RK0268` (raw COMLab WOT channel).
  14. `RK0435` (`K0599`, `apps/ui/ui_payload.py:104`, `ADV_LAMBDA_WOT_MAX` input max `3.0 -`): differs from OBDLab `RK0021` (maximum plausible wideband lambda `1.3`; cf. `RK0086` `normalized_obd_lambda` `0.7-1.3`); same bound as `RK0269` (raw COMLab WOT channel).
- **Non-marked boundary decisions:**
  - `RK0387`/`RK0388` (`FF_TRIM_MIN=-100.0 %`, `FF_TRIM_MAX=99.22 %`): match the SAE J1979 nominal range recorded in `RK0193`/`RK0196` (`-100 - 99.22 %`), whereas `RK0191`/`RK0192` (`-127.0`/`127.0 %`) are the already-flagged rail sentinels.
  - `RK0251`/`RK0253` (`calc_airflow_gps_idle`/`calc_airflow_gps_2500` `500.0 g/s`): modeled/calculated airflow (`w_theo`), distinct from measured `mass_airflow_gps` (`RK0188`, `655.35 g/s`).
  - `RK0274`/`RK0275`/`RK0380`/`RK0381` (`downstream_o2_v`/`OBD_O2_DN_*` `0.0..1.5 V`): post-cat B1S2 reading bypassed by OBDLab (`o2_normalizer.py` `RK0015`/`RK0016` bound upstream B1S1 `pid_oxygen_sensor_volts`).

### VERIFICATION GATE (Correction 1)
- Step 1 (`check_code_claims.py --group rest --files 'apps/*'`): `classes ANALYSER_SPEC=203 DIAGNOSTIC_THRESHOLD=36 INTERNAL_PARAMETER=46 NON_DOMAIN=140 PHYSICAL_CONSTANT=22 TYPICAL_RANGE=4`, `suspect 52 same_as_wiki 5`, `out_of_scope 129 candidate(s) in 1 file(s)`, `CLAIMS OK group=rest scope=apps/* candidates 209 covered claims 451`.
- Step 2 (`check_code_claims.py --group rest`): `classes ANALYSER_SPEC=203 DIAGNOSTIC_THRESHOLD=36 INTERNAL_PARAMETER=46 NON_DOMAIN=140 PHYSICAL_CONSTANT=22 TYPICAL_RANGE=4`, `suspect 52 same_as_wiki 5`, `out_of_scope 129 candidate(s) in 1 file(s)`, `CLAIMS OK group=rest candidates 411 covered claims 451`.
- Step 3 (`check_code_claims.py --group rest --files 'labs/*'`): `CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 451`.
- Step 4 (`git diff 79c1e1b -- apps/wired/audit_tasks/codeaudit/claims_rest.csv` removed lines & `git status --porcelain`): `0` removed lines; status lists only `claims_rest.csv`, `T-AUD-22h.md`, and `RESULT_T-AUD-22h.md`.
- Step 5 (R9 check against `5f2726f`): `R9 OK changed 14 missing none`.

### CODE REVIEW (Correction 1)
- Verified only `suspect` fields on the 14 R9 rows in `RK0211`–`RK0451` changed vs `5f2726f` (`RK0001`–`RK0210` and all non-`suspect` fields untouched byte-for-byte), all 5 P7 rows (`RK0247`, `RK0249`, `RK0384`, `RK0386`, `RK0394`) are present, UTF-8 encoding and LF (`\n`) line endings are preserved (0 CRLF), and `removed_lines=0` vs `79c1e1b`.

## Time (Correction 1)
phase | start | end | minutes | context at end
correction-1 | 2026-11-15T21:23:11Z | 2026-11-15T21:27:09Z | 4 | ABSENT
