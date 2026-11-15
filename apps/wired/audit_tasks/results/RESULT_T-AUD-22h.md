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
