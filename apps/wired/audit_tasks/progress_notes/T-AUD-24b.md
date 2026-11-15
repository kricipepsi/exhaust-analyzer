# Progress Note — T-AUD-24b

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-24b` (worktree per `T-AUD-24b.go.txt` lane rule) with spec commit `fd6a818` above `fix/T-AUD-24a`, `git status --porcelain` empty, `eras_sensitivity_masks.yaml` has `6` `gas_co_max_pct`/`gas_hc_max_ppm` lines (17-18, 32-33, 48-49), all 3 precondition files `checked`, and baseline suites match P2 (`labs/comlab/tests`: `606 passed in 11.32s`; `apps/wired/tests`: `189 passed in 8.29s`).
- **(b) Test fails for intended reason:** Pre-state `### Verification ###` step 3 prints `ERA FAIL ['HORIZON_LEGACY', 'HORIZON_ADAPTIVE', 'HORIZON_MODERN'] {'HORIZON_LEGACY': None, 'HORIZON_ADAPTIVE': None, 'HORIZON_MODERN': None}` because all three horizons still contain `gas_co_max_pct` and `gas_hc_max_ppm` (and because step 3's `lt` comprehension iterates `h.items()` rather than `t.items()`, see soft finding in `T-AUD-24b.blocker.json`).
- **(c) Independently derived decisive expected value:** Under `horizons.<HORIZON>.gas_lab_thresholds`, deleting the 6 `gas_co_max_pct`/`gas_hc_max_ppm` keys leaves only `lambda_tolerance` with P3 values `HORIZON_LEGACY: 0.10`, `HORIZON_ADAPTIVE: 0.05`, `HORIZON_MODERN: 0.02`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R4 are unambiguous; `### Verification ###` step 3 has a soft spec bug (`h.items()` instead of `t.items()` in `lt`, recorded in `T-AUD-24b.blocker.json` with `stopped: false`) that does not affect R1–R4 implementation or require rework.
- **(e) Teach-back:** Remove the 6 unused `gas_co_max_pct` and `gas_hc_max_ppm` lines from `labs/comlab/comlab/config/eras_sensitivity_masks.yaml` and `labs/comlab/wiki/04_horizon_eras.md`, update both header/prose descriptions to explain `lambda_tolerance` as the OBD-vs-chemical lambda agreement tolerance read by `fault_atlas_router.py` `_ecu_fault_verdict`, and add `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py` pinning the absence of those keys and the P3 `lambda_tolerance` values. Done is verified when `labs/comlab/tests` (`606` + new tests) and `apps/wired/tests` (`189`) pass with `0 failed` and the YAML check confirms `bad == []` and the P3 `lambda_tolerance` mapping.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-24b.go.txt` govern worktree branch naming (`agy/T-AUD-24b` instead of `fix/T-AUD-24b`), prohibit `git commit`/`git push`/`git switch`/`git checkout`, and omit the git branch/log paste from `RESULT_T-AUD-24b.md`.
- `### Verification ###` step 3 (`apps/wired/audit_tasks/T-AUD-24b_fix_era_masks_dead_keys(2).md:112`) writes `lt={k:v.get('lambda_tolerance') for k,v in h.items()}`, which reads `horizons.<HORIZON>` instead of `gas_lab_thresholds` (`t.items()`), so `lt` always evaluates to `None` even when R1 is implemented verbatim. Recorded as a soft `UNSATISFIABLE` finding in `T-AUD-24b.blocker.json` (`stopped: false`); proceeding with R1–R4 verbatim and running both the literal step 3 command and the `t.items()` variant.

## Changed lines by file
- `labs/comlab/comlab/config/eras_sensitivity_masks.yaml`: lines `4-8` (R2 header replacement), deleted old lines `17-18`, `32-33`, `48-49` (R1 dead `gas_co_max_pct`/`gas_hc_max_ppm` keys)
- `labs/comlab/wiki/04_horizon_eras.md`: lines `88`, `92-94` (R3 prose and YAML summary update)
- Created `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py`: lines `1-34` (R4 unit tests)
- Created `apps/wired/audit_tasks/progress_notes/T-AUD-24b.blocker.json`: lines `1-36` (soft `UNSATISFIABLE` record for step 3 `h.items()`)

## VERIFICATION GATE
- Step 1 (`labs/comlab/tests`): `608 passed in 11.27s` (P2 baseline `606 passed` + 2 new tests in `test_t_aud_24b_era_masks.py`, `0 failed`)
- Step 2 (`apps/wired/tests`): `189 passed in 8.05s` (P2 baseline `189 passed`, `0 failed`)
- Step 3 (literal `h.items()`): `ERA FAIL [] {'HORIZON_LEGACY': None, 'HORIZON_ADAPTIVE': None, 'HORIZON_MODERN': None}` (soft spec defect recorded in `T-AUD-24b.blocker.json`)
- Step 3 (`t.items()` on `gas_lab_thresholds`): `ERA OK [] {'HORIZON_LEGACY': 0.1, 'HORIZON_ADAPTIVE': 0.05, 'HORIZON_MODERN': 0.02}`
- `py_compile`: passed on `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py`
- `py -m ruff check`: `All checks passed!` on `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py` (`ruff check --select S`: 3 `S101` pytest `assert` notices only)
- `pyright`: `0 errors, 0 warnings, 0 informations` on `labs/comlab/tests/unit/test_t_aud_24b_era_masks.py`

## CODE REVIEW
- **Scope (PASS):** Every changed line traces directly to R1–R4 in `eras_sensitivity_masks.yaml`, `04_horizon_eras.md`, and `test_t_aud_24b_era_masks.py`; no unrelated edits, no `Vault/` edits, no commits or writes outside the worktree.
- **Contracts & Provenance (PASS):** `eras_sensitivity_masks.yaml` header documents `lambda_tolerance` as the OBD-vs-chemical lambda agreement tolerance read by `fault_atlas_router.py` `_ecu_fault_verdict`, and explicitly states these are not legal emission limits (`T-AUD-24b`).
- **Boundaries & Tests (PASS):** No cross-lab imports added; `test_t_aud_24b_era_masks.py` failed on the unedited YAML (Red gate) and passes after R1.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-15T22:44:04Z` | `2026-11-15T22:47:04Z` | `3.0` | `ABSENT` |
