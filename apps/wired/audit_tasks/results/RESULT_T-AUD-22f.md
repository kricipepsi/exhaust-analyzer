# Result

## Status
completed

## Summary
Appended 235 classified claim rows (`CK1381`–`CK1615`) to `apps/wired/audit_tasks/codeaudit/claims_comlab.csv` covering all 213 non-auto candidates across the six COMLab config YAML files (`labs/comlab/comlab/config/*.yaml`, including `proposals/*.yaml`), leaving `CK0001`–`CK1380` untouched. Linked 5 claims to GASLab wiki-register claims (`W1110`, `W1115`, `W0617`, `W0615`, `W0011`), linked 6 claims to earlier COMLab `CK` claims (`CK0089`, `CK1589`), and flagged 10 new `suspect` claims (8 era pass/fail thresholds in `eras_sensitivity_masks.yaml` contradicting UK MOT/Euro legal limits and `wiki/04_horizon_eras.md`, plus 2 gas deltas in `proposals/entries.yaml`).

## Files changed
- `apps/wired/audit_tasks/codeaudit/claims_comlab.csv` (MODIFIED: appended 235 rows `CK1381`–`CK1615`; 0 lines removed)
- `apps/wired/audit_tasks/progress_notes/T-AUD-22f.md` (CREATED)
- `apps/wired/audit_tasks/results/RESULT_T-AUD-22f.md` (CREATED)

## Commands executed
1. First action / Preconditions baseline (`git branch --show-current`, `git log --oneline fix/T-AUD-22e..HEAD`, `git status --porcelain`, `check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/*.yaml'`, preconditions file check).
2. Read-only baseline checks on `candidates_comlab.csv`, `claims_comlab.csv`, `labs/gaslab/audit_tasks/wikiaudit/claims.csv`, `check_code_claims.py --group comlab`, and step 2 `era_limits` query.
3. Appended 235 rows (`CK1381`–`CK1615`) to `apps/wired/audit_tasks/codeaudit/claims_comlab.csv` via Python script.
4. Verification steps 1–4 (`check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/*.yaml'`, `era_limits` Python check, `check_code_claims.py --group comlab`, `git diff` removed-line count & `git status --porcelain`).

## Validation evidence
- **Step 1:**
  ```
  classes ANALYSER_SPEC=41 DIAGNOSTIC_THRESHOLD=553 INTERNAL_PARAMETER=475 NON_DOMAIN=270 PHYSICAL_CONSTANT=9 RULE_OF_THUMB=40 TYPICAL_RANGE=226
  suspect 75 same_as_wiki 47
  CLAIMS OK group=comlab scope=labs/comlab/comlab/config/*.yaml candidates 213 covered claims 1614
  ```
  (Prior decisive failure `CLAIMS FAIL 213 error(s)` absent.)
- **Step 2:**
  ```
  era_limits 9 linked 9
  ```
  (Prior baseline `era_limits 9 linked 0` resolved.)
- **Step 3:**
  ```
  CLAIMS OK group=comlab candidates 1427 covered claims 1614
  ```
  (Prior decisive failure `CLAIMS FAIL 213 error(s)` absent.)
- **Step 4:**
  - `git diff -- apps/wired/audit_tasks/codeaudit/claims_comlab.csv` removed lines (`^-[^-]`): `0`
  - `git status --porcelain`: only `claims_comlab.csv` (modified), `progress_notes/T-AUD-22f.md` (untracked), and `results/RESULT_T-AUD-22f.md` (untracked).

## Criteria
| # | Status | Evidence |
|---|---|---|
| 1 | MET | Step 1 printed `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/*.yaml candidates 213 covered claims 1614` with no `ERROR` line. |
| 2 | MET | Step 2 printed `era_limits 9 linked 9`. |
| 3 | MET | Step 3 printed `CLAIMS OK group=comlab candidates 1427 covered claims 1614` with no `ERROR` line; `CK0001`–`CK1380` unchanged. |
| 4 | MET | `apps/wired/audit_tasks/progress_notes/T-AUD-22f.md` discloses step 1 `classes`, `suspect`, and `same_as_wiki` figures and lists all 10 new `suspect` claims (`CK1384`–`CK1386`, `CK1389`–`CK1391`, `CK1395`–`CK1396`, `CK1517`, `CK1545`) with reasons. |
| 5 | MET | Step 4 confirmed `0` removed lines in `claims_comlab.csv` and only the three authorized files touched in `git status --porcelain`. |

## Decisions the task did not specify
- Classified `eras_sensitivity_masks.yaml` `description` lines (`K0384`, `K0391`, `K0400`) as `NON_DOMAIN` with empty `citation` (matching `model_year_range` per R4, descriptive Euro labels per `ADR-0004`, and existing `NON_DOMAIN` rows in `CK0001`–`CK1380`).
- For `K0402` (`HORIZON_MODERN`, `gas_co_max_pct: 0.2`), linked `same_as=W1110` (`≤ 0.20 %` UK MOT raised-idle CO limit) with empty `suspect` per R5 ("link ... when the value agrees, and write `suspect` ... when it does not"), recording in the progress note that UK MOT natural idle is `≤ 0.30 %` (`W1109`) and `wiki/04_horizon_eras.md` §CONCEPT_ERA_MASK lists `0.5 %`.
- Classified dataset row/sample-size counts (`K2005` `7,079`, `K2021`/`K2032` `31,740,965`) and `consumer` path labels (`K2001` `2500 RPM`) as `NON_DOMAIN` per R2; RepairPal/CarMD empirical frequencies/shares (`K2023`–`K2031`) and `0.1V`/`0.9V` O2 bias labels (`K2115`, `K2120`) as `TYPICAL_RANGE`; `K1967` (`gas_signature`) as 4 `DIAGNOSTIC_THRESHOLD` rows linked to `W1115`/`W0617`/`W0615`/`W0011`; and `taxonomy_backbone.yaml` `5V` sensor reference (`K2245`, `K2247`) as `ANALYSER_SPEC` matching `CK0956`/`CK1152`.
- Flagged `CK1517` (`K2095` leaking/stuck-open injector `co: -5%`) and `CK1545` (`K2122` `0.9V` O2 rich bias `co: +410%`) as `suspect` per R6 based on domain physics and `W1564`/`W0485`.

## Pre-existing changes preserved
None (working tree was clean at start).

## Rollback
`git restore -- apps/wired/audit_tasks/codeaudit/claims_comlab.csv` and delete the two untracked files `apps/wired/audit_tasks/progress_notes/T-AUD-22f.md` and `apps/wired/audit_tasks/results/RESULT_T-AUD-22f.md`.

## Remaining risks or uncertainties
None for inventory classification; verification of unlinked claims against primary sources is deferred to the subsequent verification rows.
