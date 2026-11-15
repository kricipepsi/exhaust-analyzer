# Result — T-AUD-24a

## Status
completed

## Summary
Moved all per-trim fuel-trim bounds (`shrtft1`, `longft1`, `shrtft2`, `longft2`, COMLab `*_pct` trims, wired `_OBD_RAW_RANGES`, UI `OBD_TRIM_*`, and OBDLab `ltft_cell_vector`) from `[-127.0, 127.0]` to the SAE J1979 PIDs `06`–`09` range `[-100.0, 99.22]`, and moved `total_trim_correction_delta` (`OBDLiveDataPayload` and `SecondOperatingPointFrame`) from `[-254.0, 254.0]` to `[-200.0, 198.44]`, across code, JSON config, documentation (amending `ADR-0006`), and tests, adding component regression tests pinning the new bounds.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-15T22:19:02Z` | `2026-11-15T22:24:40Z` | `5.6` | `ABSENT` |

## Files changed
- Modified: `labs/obdlab/obdlab/config/physical_sensor_bounds.json` (lines `30-31, 33, 36-37, 39, 42-43, 45, 48-49, 51`)
- Modified: `labs/obdlab/obdlab/schemas/payload.py` (lines `53-54, 57-58, 60-61, 63-64`)
- Modified: `labs/obdlab/obdlab/core/semantic_consistency_checker.py` (lines `18-19`)
- Modified: `labs/obdlab/obdlab/core/pid_ingestion_validator.py` (lines `65, 99, 101`)
- Modified: `labs/comlab/comlab/schemas/ingestion.py` (lines `351-354, 377-378, 380-381, 416-419, 442, 444, 499-501`)
- Modified: `apps/wired/wired/composition.py` (lines `110-113, 124-125`)
- Modified: `apps/ui/ui_payload.py` (lines `34-35`)
- Modified: `labs/obdlab/docs/ADR_OBDLab.md` (lines `221-225`)
- Modified: `labs/obdlab/docs/LLD_OBDLab.md` (lines `66-69, 74, 232-233`)
- Modified: `labs/obdlab/docs/PRD_OBDLab.md` (lines `120-123, 179-182, 187`)
- Modified: `labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md` (lines `36-38, 148, 347`)
- Modified: `labs/obdlab/tests/fixtures/descriptor.py` (lines `31, 39, 101-102, 122-125`)
- Modified: `labs/obdlab/tests/unit/test_payload.py` (lines `113-115, 182-183, 185, 188-189, 191-197`)
- Modified: `labs/obdlab/tests/unit/test_pid_ingestion_validator.py` (lines `52-55`)
- Modified: `labs/obdlab/tests/unit/test_sensor_bounds.py` (lines `22-27`)
- Modified: `labs/obdlab/tests/generative/test_fuzz.py` (lines `42-43, 51-52`)
- Modified: `labs/comlab/tests/unit/test_fault_atlas_router.py` (line `1372`)
- Created: `labs/comlab/tests/unit/test_trim_bounds_j1979.py`
- Created: `apps/wired/tests/test_trim_bounds_j1979.py`
- Created: `apps/ui/tests/test_trim_bounds_j1979.py`
- Created: `apps/wired/audit_tasks/progress_notes/T-AUD-24a.md`
- Created: `apps/wired/audit_tasks/results/RESULT_T-AUD-24a.md`

## Commands executed
- First action & preconditions (`git branch --show-current`, `git log --oneline fix/T-AUD-23b..HEAD`, `git status --porcelain`, `grep -c "127"`, precondition file loop).
- Baseline verification (steps 1–4 + pre-state steps 5–6).
- `py_compile`, `ruff check`, `ruff check --select S`, and `pyright` on touched `.py` files.
- Full verification (`### Verification ###` steps 1–6 and `git status --porcelain`).

## Validation evidence
- **Step 1 (`labs/obdlab/tests`):** `395 passed, 2 skipped in 0.97s` (P2 `394 passed, 2 skipped` + 1 new test)
- **Step 2 (`labs/comlab/tests`):** `606 passed in 11.38s` (P2 `602 passed` + 4 new tests)
- **Step 3 (`apps/wired/tests`):** `189 passed in 8.25s` (P2 `186 passed` + 3 new tests)
- **Step 4 (`apps/ui/tests`):** `76 passed in 5.15s` (P2 `75 passed` + 1 new test)
- **Step 5 (P3 `127`/`254` grep across P1 + `OBD_VOCABULARY.md` + `descriptor.py`):** `0` (pre-state `55`)
- **Step 6 (`-I` Pydantic `OBDLivePayload.shrtft1` & `OBDLiveDataPayload.stft_idle_pct` check):** `R5 OK OBDLiveDataPayload` (pre-state `R5 FAIL OBDLiveDataPayload`)
- **Lint & types:** `py_compile` OK; `py -m ruff check` passed on all 15 touched `.py` files; `py -m ruff check --select S` passed on all 6 production `.py` files; `pyright` reported 0 errors on all edited lines (`composition.py` has 6 pre-existing errors at untouched lines 268 and 666–676).

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Steps 1–4: each suite passes with P2 count plus new tests (R5), no new skip or failure | `MET` | `395 passed, 2 skipped` (+1), `606 passed` (+4), `189 passed` (+3), `76 passed` (+1) |
| 2 | Step 5 prints `0` (P3) | `MET` | Step 5 output: `0` |
| 3 | Step 6 prints `R5 OK`: `OBDLivePayload.shrtft1` and `OBDLiveDataPayload.stft_idle_pct` carry P7 limits | `MET` | Step 6 output: `R5 OK OBDLiveDataPayload` |
| 4 | ADR-0006 carries R4 amendment; progress note lists every changed line by file | `MET` | `labs/obdlab/docs/ADR_OBDLab.md:221-225` and `apps/wired/audit_tasks/progress_notes/T-AUD-24a.md` |
| 5 | `git diff --stat` touches only P1, P4, P5 files and new R5 test files | `MET` | `git status --porcelain` shows only the 17 modified P1/P4/P5 files plus the 3 new R5 test files, progress note, and result |

## Decisions the task did not specify
- Set `PYTHONPATH` to the worktree's `labs/*` and `apps/*` directories when running pytest in `C:\4DApp\.agy\T-AUD-24a` because `C:\4DApp\.venv` holds editable installs pointing to `C:\4DApp\repo`.
- Placed `### Amendment (T-AUD-24a)` in `labs/obdlab/docs/ADR_OBDLab.md` directly below `**Status:** Amended (T-AUD-24a, 2026-11-15)` and above `### Context` so the original Context and Decision text remain intact underneath the amendment per R4.

## Pre-existing changes preserved
- Clean worktree at start; no pre-existing uncommitted modifications. Pre-existing `pyright` issues in `apps/wired/wired/composition.py` lines 268 and 666–676 left untouched.

## Rollback
- Revert all modified tracked files with `git restore <paths>` and delete the untracked test, progress note, and result files (`labs/comlab/tests/unit/test_trim_bounds_j1979.py`, `apps/wired/tests/test_trim_bounds_j1979.py`, `apps/ui/tests/test_trim_bounds_j1979.py`, `apps/wired/audit_tasks/progress_notes/T-AUD-24a.md`, `apps/wired/audit_tasks/results/RESULT_T-AUD-24a.md`).

## Remaining risks or uncertainties
- None in scope; `case_025` and `case_026` in `labs/obdlab/tests/fixtures/obdlab_cases.csv` (`±127.0`) now fall in `rejections` in `test_csv_bounce_rate` without exceeding `FLOOR_STANDALONE`.
