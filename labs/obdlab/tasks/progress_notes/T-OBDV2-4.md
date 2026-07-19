# T-OBDV2-4 — progress note

## Plan

We will add the new wideband-offset diagnostic capability:
- **Enum addition:** Add `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` with standard wiki citation comments.
- **Normalizer logic:** Update `O2Normalizer._wideband_passthrough` to check for persistent offset conditions (warm closed-loop only, WOT/DFCO excluded) and raise `WIDEBAND_OFFSET_CANDIDATE` if `|normalized_obd_lambda − 1.0| > 0.05`.
- **Files to create/modify:**
  - [vocabulary.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/vocabulary.py): Add new StrEnum member.
  - [o2_normalizer.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/o2_normalizer.py): Implement the guard check.
  - [test_vocabulary.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/unit/test_vocabulary.py): Update drift-guard expectations and exempt set.
  - [test_o2_normalizer.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/unit/test_o2_normalizer.py): Add unit tests verifying bounds, preconditions, and emitter discipline.
- **Verification Details:** Run local test suite, ruff, pyright, and verify emitter discipline.

## VERIFICATION GATE

- [x] Confirmed `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` added to [vocabulary.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/vocabulary.py) and registered as a proposal in [entries.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/config/proposals/entries.yaml).
- [x] Confirmed `T-COMV2-O2OFFSET-1` is registered in [PROGRESS.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/tasks/PROGRESS.md) to close the anti-orphan requirement.
- [x] Verified persistent-offset logic in [o2_normalizer.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/o2_normalizer.py) only triggers on `WIDEBAND_LINEAR` under warm closed-loop conditions (`coolant_temp_c >= 70`, `fuel_sys_status == "Closed_Loop"`, not WOT, not DFCO) and when `|λ − 1.0| > 0.05` (with proper `# wiki:` citation comments).
- [x] Emitter discipline verified: Select-String check confirmed no confirmed verdicts (`SENSOR_FAULT`), chemical lambda checks, or gas models exist in `o2_normalizer.py`.
- [x] Local test suite ran clean:
  - Ruff linting checks passed.
  - Pyright static typing checks passed with `0 errors, 0 warnings`.
  - Pytest runs for `obdlab` and `comlab` are completely green.
    - `obdlab`: `380 passed, 6 skipped` (including 8 new wideband-offset tests)
    - `comlab`: `336 passed, 6 skipped`

## CODE REVIEW

- **vocabulary.py:** Added `WIDEBAND_OFFSET_CANDIDATE = "WIDEBAND_OFFSET_CANDIDATE"` with `# wiki: o2-logic/03 §BIASED_OFFSET / o2-logic/08`.
- **o2_normalizer.py:** Declared constants with wiki citations and implemented the conditional check inside `_wideband_passthrough`.
- **test_vocabulary.py & test_o2_normalizer.py:** Integrated the new enum value into drift-guard and added unit test cases covering narrowband base cases, in-band and out-of-band wideband, transient conditions (cold engine, open loop, WOT, DFCO), and emitter discipline.
