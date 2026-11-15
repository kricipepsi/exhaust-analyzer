# Progress Note — T-AUD-24a

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-24a` (worktree per `T-AUD-24a.go.txt` lane rule) with spec commits `57c824f` and `7ea524d` above `fix/T-AUD-23b`, `git status --porcelain` empty, `grep -c "127"` prints `5` on `payload.py` and `2` on `ui_payload.py`, all 11 precondition files `checked`, and baseline suites match P2 (`obdlab`: `394 passed, 2 skipped`; `comlab`: `602 passed`; `wired`: `186 passed`; `ui`: `75 passed`).
- **(b) Test fails for intended reason:** Pre-state step 5 prints `55` matching lines for `127`/`254` across P1/P4/P5, and pre-state step 6 prints `R5 FAIL OBDLiveDataPayload` because `OBDLivePayload.shrtft1` and `OBDLiveDataPayload.stft_idle_pct` still carry `ge=-127, le=127` instead of `ge=-100.0, le=99.22`.
- **(c) Independently derived decisive expected value:** SAE J1979 PIDs 06–09 encode `((A - 128) * 100) / 128` for `A` in `0..255`: at `A = 0`, `(0 - 128) * 100 / 128 = -100.0 %`; at `A = 255`, `(255 - 128) * 100 / 128 = 127 * 100 / 128 = 99.21875 %` (rounded `99.22`); two saturated trims sum to `[-200.0, 198.44]`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, P1–P7, and `T-AUD-24a.go.txt` lane rules are consistent; `test_csv_bounce_rate` treats `case_025`/`case_026` (`±127.0`) validation errors as `rejections` rather than `bounces`.
- **(e) Teach-back:** Move all per-trim fuel-trim bounds (`shrtft1`, `longft1`, `shrtft2`, `longft2`, COMLab `*_pct` trims, wired `_OBD_RAW_RANGES`, UI `OBD_TRIM_*`, and `ltft_cell_vector`) to `[-100.0, 99.22]` and `total_trim_correction_delta` to `[-200.0, 198.44]` across code, JSON, docs (including amending `ADR-0006` and updating `OBD_VOCABULARY.md`), and tests, adding one regression test per component that rejects the old `127.0`/`254.0` values. Done is verified when steps 1–4 pass with baseline + new test counts, step 5 prints `0`, and step 6 prints `R5 OK OBDLiveDataPayload`.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-24a.go.txt` govern worktree branch naming (`agy/T-AUD-24a` instead of `fix/T-AUD-24a`), prohibit `git commit`/`git push`/`git switch`/`git checkout`, and omit the git branch/log paste from `RESULT_T-AUD-24a.md`.
- Because `C:\4DApp\.venv` holds editable installs pointing to `C:\4DApp\repo`, pytest invocations in this worktree set `PYTHONPATH` to the worktree's `labs/*` and `apps/*` directories so suites test the worktree's modified code rather than `C:\4DApp\repo`.
- Boundary cases verified before edits: `None` / absent optional trims (`shrtft2`, `longft2`, `stft_*`, `ltft_*`, `ltft_cell_vector`, `SecondOperatingPointFrame` fields), blank string (`""` → `None` in `wired._run_obdlab`), exact limits (`-100.0`, `99.22`, `-200.0`, `198.44`), and just-outside / old-rail values (`-100.1`, `99.3`, `127.0`, `-127.0`, `254.0`).

## Changed lines by file
- `apps/ui/ui_payload.py`: lines `34-35`
- `apps/wired/wired/composition.py`: lines `110-113, 124-125`
- `labs/comlab/comlab/schemas/ingestion.py`: lines `351-354, 377-378, 380-381, 416-419, 442, 444, 499-501`
- `labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md`: lines `36-38, 148, 347`
- `labs/comlab/tests/unit/test_fault_atlas_router.py`: line `1372`
- `labs/obdlab/docs/ADR_OBDLab.md`: lines `221-225`
- `labs/obdlab/docs/LLD_OBDLab.md`: lines `66-69, 74, 232-233`
- `labs/obdlab/docs/PRD_OBDLab.md`: lines `120-123, 179-182, 187`
- `labs/obdlab/obdlab/config/physical_sensor_bounds.json`: lines `30-31, 33, 36-37, 39, 42-43, 45, 48-49, 51`
- `labs/obdlab/obdlab/core/pid_ingestion_validator.py`: lines `65, 99, 101`
- `labs/obdlab/obdlab/core/semantic_consistency_checker.py`: lines `18-19`
- `labs/obdlab/obdlab/schemas/payload.py`: lines `53-54, 57-58, 60-61, 63-64`
- `labs/obdlab/tests/fixtures/descriptor.py`: lines `31, 39, 101-102, 122-125`
- `labs/obdlab/tests/generative/test_fuzz.py`: lines `42-43, 51-52`
- `labs/obdlab/tests/unit/test_payload.py`: lines `113-115, 182-183, 185, 188-189, 191-197`
- `labs/obdlab/tests/unit/test_pid_ingestion_validator.py`: lines `52-55`
- `labs/obdlab/tests/unit/test_sensor_bounds.py`: lines `22-27`
- Created `labs/comlab/tests/unit/test_trim_bounds_j1979.py`: lines `1-67`
- Created `apps/wired/tests/test_trim_bounds_j1979.py`: lines `1-42`
- Created `apps/ui/tests/test_trim_bounds_j1979.py`: lines `1-11`

## VERIFICATION GATE
- Step 1 (`labs/obdlab/tests`): `395 passed, 2 skipped in 0.97s` (P2 baseline `394 passed, 2 skipped` + 1 new test `test_shrtft1_rejects_old_127_rail`)
- Step 2 (`labs/comlab/tests`): `606 passed in 11.38s` (P2 baseline `602 passed` + 4 new tests in `test_trim_bounds_j1979.py`)
- Step 3 (`apps/wired/tests`): `189 passed in 8.25s` (P2 baseline `186 passed` + 3 new tests in `test_trim_bounds_j1979.py`)
- Step 4 (`apps/ui/tests`): `76 passed in 5.15s` (P2 baseline `75 passed` + 1 new test in `test_trim_bounds_j1979.py`)
- Step 5 (P3 grep for `127`/`254` in P1 + `OBD_VOCABULARY.md` + `descriptor.py`): `0`
- Step 6 (`-I` Pydantic `OBDLivePayload.shrtft1` & `OBDLiveDataPayload.stft_idle_pct` bounds): `R5 OK OBDLiveDataPayload`
- `py_compile`: passed on all 15 touched `.py` files
- `py -m ruff check`: `All checks passed!` on all 15 touched `.py` files; `ruff check --select S`: `All checks passed!` on all 6 touched production `.py` files
- `pyright`: `0` errors on `payload.py`, `semantic_consistency_checker.py`, `pid_ingestion_validator.py`, `ingestion.py`, `ui_payload.py`, `labs/comlab/tests/unit/test_trim_bounds_j1979.py`, and `apps/ui/tests/test_trim_bounds_j1979.py` (`composition.py` has 6 pre-existing errors at untouched lines 268 and 666–676)

## CODE REVIEW
- **Scope (PASS):** Every changed line traces directly to R1–R5 in P1, P4, P5, and the 3 new R5 test files; no unrelated edits, no code-audit/wiki register edits, no commits or writes outside the worktree.
- **Contracts & Provenance (PASS):** All boundary literals carry SAE J1979 PIDs `06`–`09` / wiki §3.1 / `T-AUD-24a` citations; `ADR-0006` carries `**Status:** Amended (T-AUD-24a, 2026-11-15)` and `### Amendment (T-AUD-24a)` citing `fault_atlas_router.py:103`, `ecu_hardware_checker.py:14`, `perception_contradiction.py:54`, and `CK0181`, `RK0191`, `RK0192`, with the original Context and Decision preserved underneath.
- **Boundaries & Tests (PASS):** No cross-lab imports added; every component has a new regression test that fails on the old `127.0`/`254.0` values and passes on `[-100.0, 99.22]` / `[-200.0, 198.44]`.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-15T22:19:02Z` | `2026-11-15T22:24:40Z` | `5.6` | `ABSENT` |
