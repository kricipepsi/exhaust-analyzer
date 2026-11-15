# Result — T-AUD-22g

## Summary
Completed `T-AUD-22g` (Codeaudit Rest Labs Inventory): audited all **202** non-auto candidates under `labs/` (OBDLab 125, DTCLab 76, SymptomLab 1 across 20 files) from `apps/wired/audit_tasks/codeaudit/candidates_rest.csv`, reconciled against `OBDLab_KG_Wiki.md`, `research/chunks/`, `DTC_VOCABULARY.md`, `01_symptom_catalog.md`, `wikiaudit/claims.csv`, and `claims_comlab.csv`, and appended **210** claims (`RK0001`–`RK0210`) in candidates order to `apps/wired/audit_tasks/codeaudit/claims_rest.csv`.

*(Per lane rules in `T-AUD-22g.go.txt`, git branch/log output and `git commit` / `git push` are omitted.)*

## Classification & Audit Figures
- **Scope covered:** 202 `labs/` candidates -> **210** claims (`RK0001`–`RK0210`)
- **Classes:** `ANALYSER_SPEC=45`, `DIAGNOSTIC_THRESHOLD=34`, `INTERNAL_PARAMETER=31`, `NON_DOMAIN=75`, `PHYSICAL_CONSTANT=21`, `TYPICAL_RANGE=4`
- **`same_as`:** `same_as_wiki=5` (`W0066`, `W0079` x2, `W0116`, `W0118`), `same_as_rk=28`
- **Empty `citation`:** `28` claims (`11` unreferenced code defaults/math/clamp parameters + `17` `NON_DOMAIN` guards/sentinels/notes)
- **"Citation not found" in repo (`labs/` or `Vault/`):** `9` claims (`2` citing missing `DTC_WIKI.md`: `RK0092`, `RK0093`; `7` citing unarchived `BP`: `RK0052`–`RK0057`, `RK0059`)
- **`suspect`: `20` claims** (`RK0014`, `RK0030`–`RK0032`, `RK0062`, `RK0082`–`RK0085`, `RK0087`–`RK0088`, `RK0191`–`RK0192`, `RK0194`–`RK0195`, `RK0197`–`RK0198`, `RK0200`–`RK0201`, `RK0204`), listed with reasons in `apps/wired/audit_tasks/progress_notes/T-AUD-22g.md`.

## Verification
1. `C:/4DApp/.venv/Scripts/python.exe apps/wired/audit_tasks/codeaudit/check_code_claims.py --group rest --files 'labs/*'`
   - `classes ANALYSER_SPEC=45 DIAGNOSTIC_THRESHOLD=34 INTERNAL_PARAMETER=31 NON_DOMAIN=75 PHYSICAL_CONSTANT=21 TYPICAL_RANGE=4`
   - `suspect 20 same_as_wiki 5`
   - `CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 210`
2. `C:/4DApp/.venv/Scripts/python.exe apps/wired/audit_tasks/codeaudit/check_code_claims.py --group rest`
   - `CLAIMS FAIL 338 error(s)` (all 338 `uncovered` under `apps/`, unchanged; zero `apps/` candidates covered)
3. `git diff --numstat apps/wired/audit_tasks/codeaudit/claims_rest.csv`
   - `210	0	apps/wired/audit_tasks/codeaudit/claims_rest.csv` (`0` removed lines)

## Files Written
- `apps/wired/audit_tasks/codeaudit/claims_rest.csv`
- `apps/wired/audit_tasks/progress_notes/T-AUD-22g.md`
- `apps/wired/audit_tasks/results/RESULT_T-AUD-22g.md`
