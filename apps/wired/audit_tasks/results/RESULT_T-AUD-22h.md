# Result — T-AUD-22h

## Status
PASS

## Summary
Classified all **209** non-auto in-scope numeric literal candidates under `apps/` (`apps/wired/v7/load_corpus.py`, `apps/wired/v7/run_suite.py`, `apps/wired/wired/composition.py`, `apps/wired/wired/registry_guard.py`, `apps/ui/app.py`, `apps/ui/ui_payload.py`), appending **241** claim rows (`RK0211`–`RK0451`) in strict `candidates_rest.csv` order below `RK0210` in [claims_rest.csv](file:///C:/4DApp/.agy/T-AUD-22h/apps/wired/audit_tasks/codeaudit/claims_rest.csv). Thirty-one `_OBD_RAW_RANGES` `(min, max)` tuples in `composition.py` and the literal `(min_value, max_value)` pair in `app.py:746` were split into paired `plausible min`/`plausible max` and `input min`/`input max` rows. Flagged **18** new `suspect` claims (14 fuel-trim `-127.0`/`127.0 %` bounds against SAE J1979 `-100.0..+99.22 %`, `WIDEBAND_AFR_STOICH = 14.7` vs GASLab `14.71`, `ADV_DECEL_CO_MAX = 25.0 %` vs `0-15 %` CO envelope, and `obd_upstream_o2_val` union tooltip `0.0-20.0` vs the 3 per-sensor widgets in `app.py:536-540`), recorded all required disclosures in [T-AUD-22h.md](file:///C:/4DApp/.agy/T-AUD-22h/apps/wired/audit_tasks/progress_notes/T-AUD-22h.md), and passed all checker gates with zero errors and zero removed lines.

## Files changed
- Modified: `apps/wired/audit_tasks/codeaudit/claims_rest.csv` (+241 lines appended: `RK0211`–`RK0451`; 0 lines removed)
- Created: `apps/wired/audit_tasks/progress_notes/T-AUD-22h.md`
- Created: `apps/wired/audit_tasks/results/RESULT_T-AUD-22h.md`

## Commands executed
- Baseline preconditions & checker baseline (`check_code_claims.py --group rest --files 'apps/*'`, `--files 'labs/*'`)
- `C:/4DApp/.venv/Scripts/python.exe` script reading `candidates_rest.csv` and appending `RK0211`–`RK0451` to `claims_rest.csv`
- Verification Steps 1–4:
  1. `C:/4DApp/.venv/Scripts/python.exe -I apps/wired/audit_tasks/codeaudit/check_code_claims.py --group rest --files 'apps/*' | Select-Object -Last 4`
  2. `C:/4DApp/.venv/Scripts/python.exe -I apps/wired/audit_tasks/codeaudit/check_code_claims.py --group rest | Select-Object -Last 4`
  3. `C:/4DApp/.venv/Scripts/python.exe -I apps/wired/audit_tasks/codeaudit/check_code_claims.py --group rest --files 'labs/*' | Select-Object -Last 1`
  4. `git diff -- apps/wired/audit_tasks/codeaudit/claims_rest.csv | Select-String -Pattern '^-[^-]'` count and `git status --porcelain`

## Validation evidence
- **Step 1 (`--files 'apps/*'`):**
  ```text
  classes ANALYSER_SPEC=203 DIAGNOSTIC_THRESHOLD=36 INTERNAL_PARAMETER=46 NON_DOMAIN=140 PHYSICAL_CONSTANT=22 TYPICAL_RANGE=4
  suspect 38 same_as_wiki 5
  out_of_scope 129 candidate(s) in 1 file(s)
  CLAIMS OK group=rest scope=apps/* candidates 209 covered claims 451
  ```
- **Step 2 (`--group rest`):**
  ```text
  classes ANALYSER_SPEC=203 DIAGNOSTIC_THRESHOLD=36 INTERNAL_PARAMETER=46 NON_DOMAIN=140 PHYSICAL_CONSTANT=22 TYPICAL_RANGE=4
  suspect 38 same_as_wiki 5
  out_of_scope 129 candidate(s) in 1 file(s)
  CLAIMS OK group=rest candidates 411 covered claims 451
  ```
- **Step 3 (`--files 'labs/*'`):**
  ```text
  CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 451
  ```
- **Step 4 (`git diff` removed lines & `git status --porcelain`):**
  ```text
  removed_lines=0
   M apps/wired/audit_tasks/codeaudit/claims_rest.csv
  ?? apps/wired/audit_tasks/progress_notes/T-AUD-22h.md
  ```
  (plus `apps/wired/audit_tasks/results/RESULT_T-AUD-22h.md` created after Step 4)

## Criteria
1. **Step 1 `check_code_claims.py --group rest --files 'apps/*'` prints `out_of_scope 129 candidate(s) in 1 file(s)` and `CLAIMS OK group=rest scope=apps/* candidates 209 covered claims N`, no `ERROR`:** MET (`N = 451`, exit 0).
2. **Step 2 `check_code_claims.py --group rest` prints `CLAIMS OK group=rest candidates 411 covered claims N` with `N >= 419`, no `ERROR`:** MET (`N = 451 >= 419`, exit 0).
3. **Step 3 `check_code_claims.py --group rest --files 'labs/*'` preserves all 202 `labs/*` coverage cleanly:** MET (`CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 451`, exit 0; total `claims_rest.csv` count prints `451` after appending `RK0211`–`RK0451`).
4. **Progress note discloses Step 2 `classes`, `suspect`, `same_as_wiki`, empty-`citation` count (`83`), `"citation not found"` count (`0`), and all 18 new `suspect` claims with reasons:** MET in `apps/wired/audit_tasks/progress_notes/T-AUD-22h.md`.
5. **Only `claims_rest.csv` modified, by appended rows only (`removed_lines=0`), plus new progress note and result file:** MET.

## Decisions the task did not specify
- **Tuple/widget bound splitting (`R4`):** Emitted paired `plausible min`/`plausible max` rows for all 31 `_OBD_RAW_RANGES` lines (`K0197`–`K0227`) in `composition.py` and paired `input min`/`input max` rows for `app.py:746` (`K0507`), giving 241 total new rows across 209 candidates.
- **`K0231` (`composition.py:527` `/ 2.0`):** Classified as `NON_DOMAIN` arithmetic divisor (per `R3`) while documenting the stale inline `GAS_VOCABULARY §3` CoC lambda midpoint comment in `citation` and [T-AUD-22h.md](file:///C:/4DApp/.agy/T-AUD-22h/apps/wired/audit_tasks/progress_notes/T-AUD-22h.md).
- **`RK` `same_as` cross-linking:** Linked matching `OBD_*` / `FF_*` / `ADV_*` / `composition.py` / `FIELD_HELP` constants to their canonical earlier `RK` rows (80 links, zero to `W*`, zero self-links).

## Pre-existing changes preserved
- Existing rows `RK0001`–`RK0210` in `claims_rest.csv` preserved byte-for-byte (`removed_lines=0`).
- Worktree files outside the 3 task deliverables remain untouched on branch `agy/T-AUD-22h`.

## Rollback
- Truncate `apps/wired/audit_tasks/codeaudit/claims_rest.csv` back to lines 1–211 (`RK0001`–`RK0210`) or `git checkout -- apps/wired/audit_tasks/codeaudit/claims_rest.csv`, and delete `apps/wired/audit_tasks/progress_notes/T-AUD-22h.md` and `apps/wired/audit_tasks/results/RESULT_T-AUD-22h.md`.

## Remaining risks or uncertainties
- The 18 `suspect` claims document existing codebase/spec discrepancies (`-127.0`/`127.0 %` fuel trims vs SAE J1979 `-100.0..+99.22 %`, `WIDEBAND_AFR_STOICH = 14.7` vs `14.71`, `ADV_DECEL_CO_MAX = 25.0 %` vs `0-15 %` CO envelope, and `obd_upstream_o2_val` `0.0-20.0` union tooltip drift vs per-sensor widgets) for downstream fix tasks.

## Correction 1

### Status
completed

### Summary
Applied ruling R9 (`4461c46`) across `RK0211`–`RK0451` in [claims_rest.csv](file:///C:/4DApp/.agy/T-AUD-22h/apps/wired/audit_tasks/codeaudit/claims_rest.csv), comparing every `ANALYSER_SPEC` row against `RK0001`–`RK0210` lab bounds. Updated only the `suspect` field on **14** rows (the 5 P7 rows `RK0247`, `RK0249`, `RK0384`, `RK0386`, `RK0394`, plus `RK0268`, `RK0269`, `RK0399`, `RK0400`, `RK0404`, `RK0405`, `RK0431`, `RK0434`, `RK0435`), raising total `suspect` claims from `38` to **`52`** (`>= 43`, P6) with `0` removed lines vs `79c1e1b` and `R9 OK changed 14 missing none` vs `5f2726f`. Updated [T-AUD-22h.md](file:///C:/4DApp/.agy/T-AUD-22h/apps/wired/audit_tasks/progress_notes/T-AUD-22h.md) and this result under `## Correction 1`.

### Files changed
- Modified: `apps/wired/audit_tasks/codeaudit/claims_rest.csv` (`suspect` populated on 14 rows in `RK0211`–`RK0451`; LF preserved; `0` removed lines vs `79c1e1b`)
- Modified: `apps/wired/audit_tasks/progress_notes/T-AUD-22h.md` (added `## Correction 1` readiness challenge, 14-row disclosure, `VERIFICATION GATE`, `CODE REVIEW`, and `## Time`)
- Modified: `apps/wired/audit_tasks/results/RESULT_T-AUD-22h.md` (added `## Correction 1`)

### Commands executed
- Read-only inspection of `claims_rest.csv` (`RK0001`–`RK0210` and `RK0211`–`RK0451`), `composition.py`, `ui_payload.py`, `o2_normalizer.py`, `payload.py`, `physical_sensor_bounds.json`, `OBDLab_KG_Wiki.md`, `4DLab_UI_FieldMap.md`, and `check_code_claims.py`
- In-place Python update of the 14 R9 `suspect` fields in `claims_rest.csv` from `5f2726f` preserving exact bytes of all other rows and LF line endings
- Verification Steps 1–5 from `apps/wired/audit_tasks/T-AUD-22h_codeaudit_rest_apps_inventory(3).md`

### Validation evidence
- **Step 1 (`--files 'apps/*'`):**
  ```text
  classes ANALYSER_SPEC=203 DIAGNOSTIC_THRESHOLD=36 INTERNAL_PARAMETER=46 NON_DOMAIN=140 PHYSICAL_CONSTANT=22 TYPICAL_RANGE=4
  suspect 52 same_as_wiki 5
  out_of_scope 129 candidate(s) in 1 file(s)
  CLAIMS OK group=rest scope=apps/* candidates 209 covered claims 451
  ```
- **Step 2 (`--group rest`):**
  ```text
  classes ANALYSER_SPEC=203 DIAGNOSTIC_THRESHOLD=36 INTERNAL_PARAMETER=46 NON_DOMAIN=140 PHYSICAL_CONSTANT=22 TYPICAL_RANGE=4
  suspect 52 same_as_wiki 5
  out_of_scope 129 candidate(s) in 1 file(s)
  CLAIMS OK group=rest candidates 411 covered claims 451
  ```
- **Step 3 (`--files 'labs/*'`):**
  ```text
  CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 451
  ```
- **Step 4 (`git diff 79c1e1b` removed lines & `git status --porcelain`):**
  ```text
  0
   M apps/wired/audit_tasks/codeaudit/claims_rest.csv
   M apps/wired/audit_tasks/progress_notes/T-AUD-22h.md
   M apps/wired/audit_tasks/results/RESULT_T-AUD-22h.md
  ```
- **Step 5 (R9 check against `5f2726f`):**
  ```text
  R9 OK changed 14 missing none
  ```

### Criteria (Correction 1)
1. **Step 1 (`--files 'apps/*'`) prints P3 and `CLAIMS OK group=rest scope=apps/* candidates 209`, no `ERROR`:** MET (`covered claims 451`).
2. **Step 2 (`--group rest`) prints `CLAIMS OK group=rest candidates 411 covered claims N` (`N >= 419`), no `ERROR`:** MET (`N = 451`, `suspect 52`).
3. **Step 3 (`--files 'labs/*'`) prints P5:** MET (`CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 451`).
4. **Note discloses Step 2 figures, empty-citation (`83`), citation-not-found (`0`), and `## Correction 1` lists each R9 row and reason:** MET in `apps/wired/audit_tasks/progress_notes/T-AUD-22h.md`.
5. **Against `79c1e1b`, `claims_rest.csv` changes only by appended rows (Step 4: `0` removed lines):** MET (`0`).
6. **Against `5f2726f`, only `suspect` fields of `RK0211`–`RK0451` change, every P7 row is included (`R9 OK changed N missing none`, `N >= 5`), and `suspect >= 43` (P6):** MET (`changed 14`, `missing none`, `suspect 52 >= 43`).

### Decisions the task did not specify (Correction 1)
- **`RK0387`/`RK0388` (`FF_TRIM_MIN=-100.0 %`, `FF_TRIM_MAX=99.22 %`):** Left unmarked because they match the SAE J1979 nominal range already recorded in `RK0193`/`RK0196` (`-100 - 99.22 %`), while `RK0191`/`RK0192` (`-127.0`/`127.0 %`) are the already-flagged rail sentinels (consistent with P7).
- **`RK0251`/`RK0253` (`calc_airflow_gps_idle`/`calc_airflow_gps_2500` `500.0 g/s`):** Left unmarked as modeled/calculated airflow (`w_theo`), distinct from measured `mass_airflow_gps` (`RK0188`).
- **`RK0274`/`RK0275`/`RK0380`/`RK0381` (`downstream_o2_v`/`OBD_O2_DN_*` `0.0..1.5 V`):** Left unmarked as post-cat B1S2 voltage bypassed by OBDLab (`RK0015`/`RK0016` bound upstream B1S1 `pid_oxygen_sensor_volts` in `o2_normalizer.py`).

### Rollback (Correction 1)
- `git checkout 5f2726f -- apps/wired/audit_tasks/codeaudit/claims_rest.csv apps/wired/audit_tasks/progress_notes/T-AUD-22h.md apps/wired/audit_tasks/results/RESULT_T-AUD-22h.md` (performed by Cowork if reverting Correction 1).
