# Result

## Status
completed

## Summary
Appended 334 classified / `NON_DOMAIN` claim rows (`CK0693`-`CK1026`) to `apps/wired/audit_tasks/codeaudit/claims_comlab.csv`, covering all 303 non-auto candidates in `labs/comlab/comlab/config/global_fault_registry.json`:
- 208 `base_weight` / `bonus_on_dtc_match` lines → `INTERNAL_PARAMETER` (`registry base_weight` / `registry bonus_on_dtc_match`, unit `score`, condition = `fault_id`).
- 40 `obd_live_pids` threshold lines (32 scalar `value` + 8 `IN_RANGE` array items) → `DIAGNOSTIC_THRESHOLD`.
- 35 `ui_diagnostic_string` and 19 `remediation_map` entries → one claim per stated domain value, or `NON_DOMAIN` when only mode/DTC/PID numbers appear (`K0986`, `K0993`, `K0996`), plus `NON_DOMAIN` for `fault_wiki_page` (`K0813`).
- `citation` is empty on all 334 new rows (R6); `same_as` links 7 rows to `W` claims and 20 rows to earlier `CK` claims; 12 new claims are flagged `suspect`. No web access was used.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | 2026-11-15T18:19:20Z | 2026-11-15T18:25:37Z | 6.3 | ABSENT |

## Files changed
- `apps/wired/audit_tasks/codeaudit/claims_comlab.csv`: modified (334 rows appended, `CK0693`-`CK1026`, `0` removed lines).
- `apps/wired/audit_tasks/progress_notes/T-AUD-22d.md`: created.
- `apps/wired/audit_tasks/results/RESULT_T-AUD-22d.md`: created.

## Commands executed
- Baseline First action (`git branch --show-current`, `git log --oneline fix/T-COMA-32..HEAD`, `git status --porcelain`, `check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/global_fault_registry.json'`), Preconditions check, and baseline step 3 check.
- Read-only inspection of `candidates_comlab.csv`, `claims_comlab.csv`, `global_fault_registry.json`, `labs/comlab/registry/rules/*.json`, `OBD_VOCABULARY.md`, `GAS_VOCABULARY.md`, and `labs/gaslab/audit_tasks/wikiaudit/claims.csv`.
- Appended 334 rows to `claims_comlab.csv` via Python stdin.
- Verification steps 1–4.

## Validation evidence
```
# 1.
classes ANALYSER_SPEC=28 DIAGNOSTIC_THRESHOLD=370 INTERNAL_PARAMETER=448 NON_DOMAIN=140 PHYSICAL_CONSTANT=7 TYPICAL_RANGE=32
suspect 46 same_as_wiki 27
CLAIMS OK group=comlab scope=labs/comlab/comlab/config/global_fault_registry.json candidates 303 covered claims 1025
# 2.
knobs 208 internal 208
# 3.
CLAIMS OK group=comlab scope=labs/comlab/registry/rules/* candidates 357 covered claims 1025
# 4.
0
 M apps/wired/audit_tasks/codeaudit/claims_comlab.csv
?? apps/wired/audit_tasks/progress_notes/T-AUD-22d.md
?? apps/wired/audit_tasks/results/RESULT_T-AUD-22d.md
```
The earlier decisive failure (`CLAIMS FAIL 303 error(s)`, all `uncovered`) is absent, and no `ERROR` line is printed.

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | Step 1 prints `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/global_fault_registry.json candidates 303 covered claims 1025` with no `ERROR` line. |
| 2 | MET | Step 2 prints `knobs 208 internal 208`. |
| 3 | MET | Step 3 prints `CLAIMS OK group=comlab scope=labs/comlab/registry/rules/* candidates 357 covered claims 1025`; rows `CK0001`-`CK0692` unchanged. |
| 4 | MET | `apps/wired/audit_tasks/progress_notes/T-AUD-22d.md` discloses step 1 `classes`, `suspect`, and `same_as_wiki` figures and lists all 12 new `suspect` claims with reasons. |
| 5 | MET | Step 4 prints `0` removed lines; `git status --porcelain` shows only `claims_comlab.csv` modified, `T-AUD-22d.md`, and `RESULT_T-AUD-22d.md`. |

## Decisions the task did not specify
- `IN_RANGE` array items (`K0408`/`K0409`, `K0453`/`K0454`, `K0572`/`K0573`, `K0613`/`K0614`) named `<pid> in_range lower edge` and `<pid> in_range upper edge`, matching `T-AUD-22c`.
- Prose test conditions (`at 2500 RPM` in `K0433`/`K0998`, `at 20 C` in `K1012`) kept inside `condition` rather than emitted as separate claims; single DTCs, Mode `$06`, and `PID $0C` treated as non-claims (`K0986`, `K0993`, `K0996` emitted as `NON_DOMAIN`).
- `5 V` ECU sensor reference (`K0938`, `K0942`) classified as `ANALYSER_SPEC` (consistent with `CK0180`); `lambda_chem` `1.0` (`K1024`) classified as `PHYSICAL_CONSTANT` (`same_as W0079`); `60 000-100 000` (`K1023`) retains spaced thousands to match line digits.
- Duplicate `fault_id` scoring knobs (`ERR-CT-003`, `ERR-MF-002`, `ERR-SF-001`) link `same_as` to their first occurrence when `(quantity, fault_id, value)` matches identically.
- `ERR-MW-005` (`map_kpa < 30.0`, `K0587`) cites `CK0469` (`MW-004`, removed in `T-COMA-32`) in `suspect` rather than `same_as` because the fault/gas state differs.

## Pre-existing changes preserved
The worktree was clean at start (`git status --porcelain` empty). No pre-existing files outside `### Files to touch ###` were modified.

## Rollback
`git restore -- apps/wired/audit_tasks/codeaudit/claims_comlab.csv` and delete the untracked `apps/wired/audit_tasks/progress_notes/T-AUD-22d.md` and `apps/wired/audit_tasks/results/RESULT_T-AUD-22d.md`.

## Remaining risks or uncertainties
- None of the 12 `suspect` claims or domain thresholds was web-verified (out of scope per R7); verification rows will settle them against primary sources.
- Duplicate `fault_id` entries (`ERR-CT-003`, `ERR-LC-004`, `ERR-MF-002`, `ERR-SF-001`) exist in `global_fault_registry.json` as source data; left untouched per `### Out of scope ###`.
