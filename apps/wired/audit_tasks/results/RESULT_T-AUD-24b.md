# Result — T-AUD-24b

## Status
completed

## Summary
Removed the six dead `gas_co_max_pct` and `gas_hc_max_ppm` keys from `labs/comlab/comlab/config/eras_sensitivity_masks.yaml` (R1), updated its header to describe `lambda_tolerance` as the OBD-vs-chemical lambda agreement tolerance read by `fault_atlas_router.py` `_ecu_fault_verdict` rather than legal emission limits (R2), updated `labs/comlab/wiki/04_horizon_eras.md` §Era sensitivity masks to match (R3), and added `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py` pinning the key removal and P3 `lambda_tolerance` values (R4).

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-15T22:44:04Z` | `2026-11-15T22:47:04Z` | `3.0` | `ABSENT` |

## Files changed
- Modified: `labs/comlab/comlab/config/eras_sensitivity_masks.yaml` (lines `4-8`; deleted old lines `17-18`, `32-33`, `48-49`)
- Modified: `labs/comlab/wiki/04_horizon_eras.md` (lines `88`, `92-94`)
- Created: `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py` (lines `1-34`)
- Created: `apps/wired/audit_tasks/progress_notes/T-AUD-24b.md`
- Created: `apps/wired/audit_tasks/progress_notes/T-AUD-24b.blocker.json`
- Created: `apps/wired/audit_tasks/results/RESULT_T-AUD-24b.md`

## Commands executed
- First action & preconditions (`git branch --show-current`, `git log --oneline fix/T-AUD-24a..HEAD`, `git status --porcelain`, count of `gas_co_max_pct|gas_hc_max_ppm`, precondition file loop).
- Baseline verification (`labs/comlab/tests`, `apps/wired/tests`, and step 3 YAML check).
- `validate_blocker_record.py` on `apps/wired/audit_tasks/progress_notes/T-AUD-24b.blocker.json`.
- Red-gate pytest on `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py`.
- `py_compile`, `py -m ruff check`, `py -m ruff check --select S`, and `py -m pyright` on `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py`.
- Post-edit `### Verification ###` steps 1–3 (plus `t.items()` variant of step 3), `git diff --stat`, and `git status --porcelain`.

## Validation evidence
- **Step 1 (`labs/comlab/tests`):** `608 passed in 11.27s` (P2 `606 passed` + 2 new tests in `test_t_aud_24b_era_masks.py`, `0 failed`)
- **Step 2 (`apps/wired/tests`):** `189 passed in 8.05s` (P2 `189 passed`, `0 failed`)
- **Step 3 (literal `h.items()`):** `ERA FAIL [] {'HORIZON_LEGACY': None, 'HORIZON_ADAPTIVE': None, 'HORIZON_MODERN': None}` (soft spec bug in `T-AUD-24b_fix_era_masks_dead_keys(2).md:112`, recorded in `T-AUD-24b.blocker.json`)
- **Step 3 (`t.items()` on `gas_lab_thresholds`):** `ERA OK [] {'HORIZON_LEGACY': 0.1, 'HORIZON_ADAPTIVE': 0.05, 'HORIZON_MODERN': 0.02}`
- **Lint & types:** `py_compile` OK; `py -m ruff check` `All checks passed!`; `pyright` `0 errors, 0 warnings, 0 informations` on `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py`.

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Steps 1-2: the P2 counts, plus the R4 test in step 1, and `0 failed` | `MET` | `608 passed in 11.27s` (+2), `189 passed in 8.05s` |
| 2 | Step 3 prints `ERA OK` | `NOT MET` (soft spec defect) | Literal `h.items()` prints `ERA FAIL [] {'HORIZON_LEGACY': None, 'HORIZON_ADAPTIVE': None, 'HORIZON_MODERN': None}`; `t.items()` prints `ERA OK [] {'HORIZON_LEGACY': 0.1, 'HORIZON_ADAPTIVE': 0.05, 'HORIZON_MODERN': 0.02}` (see `T-AUD-24b.blocker.json`) |
| 3 | `git diff --stat` touches only the YAML, the wiki page and the new test | `MET` | `git diff --stat` shows only `eras_sensitivity_masks.yaml` and `04_horizon_eras.md` (plus untracked `test_t_aud_24b_era_masks.py`, progress note, blocker JSON, and result) |

## Decisions the task did not specify
- Recorded the `h.items()` vs `t.items()` bug in `### Verification ###` step 3 (`T-AUD-24b_fix_era_masks_dead_keys(2).md:112`) as a soft `UNSATISFIABLE` finding in `T-AUD-24b.blocker.json` (`stopped: false`) rather than moving `lambda_tolerance` out of `gas_lab_thresholds` (which would violate R1).

## Pre-existing changes preserved
- Clean worktree at start; no pre-existing uncommitted modifications.

## Rollback
- Revert modified tracked files with `git restore labs/comlab/comlab/config/eras_sensitivity_masks.yaml labs/comlab/wiki/04_horizon_eras.md` and remove untracked `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py`, `apps/wired/audit_tasks/progress_notes/T-AUD-24b.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-24b.blocker.json`, and `apps/wired/audit_tasks/results/RESULT_T-AUD-24b.md`.

## Remaining risks or uncertainties
- `### Verification ###` step 3 in `apps/wired/audit_tasks/T-AUD-24b_fix_era_masks_dead_keys(2).md:112` needs `h.items()` changed to `t.items()` in the spec so the one-liner reads `lambda_tolerance` from `gas_lab_thresholds`.
