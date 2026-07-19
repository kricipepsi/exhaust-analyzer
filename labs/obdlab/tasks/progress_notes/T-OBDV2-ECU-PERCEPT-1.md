# T-OBDV2-ECU-PERCEPT-1 — progress note

## Plan

We will implement the OBD perception-delta channel for `ecu_fault`.
- **Files to create/modify:**
  - [payload.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/payload.py): add `lambda_perception_delta: float | None` field.
  - [sensor_signal_translator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/sensor_signal_translator.py): ingest PID 0x44 (`commanded_equivalence_ratio`), validate it, compute the perception delta, and emit it.
  - [test_ecu_perception_delta.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/unit/test_ecu_perception_delta.py): new unit tests covering the computability branches and emitter-discipline assertions.
- **Computability gate (Q4):** Emitted as a value only when `dna_view.upstream_o2_type == WIDEBAND_LINEAR` and `commanded_equivalence_ratio` is present. Otherwise, `None`.
- **Emitter-only stance:** Assert that OBDLab does not emit `ecu_fault` or other fault verdicts.
- **Forward-registered S4 Consumer:** COMLab `T-COMV2-ECU-FUSE-1` consumes `lambda_perception_delta` + bank-symmetry (`total_trim_correction_delta` vs `_b2`) + GASLab `λ_chem`.

## VERIFICATION GATE

- [x] Computability branches verified (3 unit test cases in `test_ecu_perception_delta.py` pass).
- [x] Emitter-only discipline verified (unit test asserts that no fault classification fields are present on the payload, and `Select-String` search contains zero references to `ecu_fault`, `fault_family`, or `FaultFamily` in `sensor_signal_translator.py`).
- [x] Run command: `python -m pytest tests/unit/test_ecu_perception_delta.py`
  Result: `5 passed in 0.27s`
- [x] Run command: `python -m pytest`
  Result: `370 passed, 6 skipped in 0.79s`

## CODE REVIEW

- **Validation:** Non-numeric validation is added for `commanded_equivalence_ratio` which raises `PIDValidationError` as expected by client specifications.
- **Static Typing & Formatting:** Pyright check shows `0 errors, 0 warnings`. Ruff linting is fully clean and auto-formatted.
- **Consumer Alignment:** COMLab `T-COMV2-ECU-FUSE-1` forward-registered row verified to consume `lambda_perception_delta`.
