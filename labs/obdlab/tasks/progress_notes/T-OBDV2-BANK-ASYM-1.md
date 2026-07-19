# T-OBDV2-BANK-ASYM-1 — progress note

## Plan

We will implement the OBD per-bank trim-delta channel for bank asymmetry.
- **Files to create/modify:**
  - [payload.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/schemas/payload.py): add `per_bank_trim_delta: float | None = None`.
  - [trim_vector_aggregator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/trim_vector_aggregator.py): compute signed `per_bank_trim_delta` as `bank1 - bank2` under the bank-2 presence gate; return `None` when single-bank.
  - [sensor_signal_translator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/core/sensor_signal_translator.py): pass the computed delta to `OBDLivePayload`.
  - [test_bank_asym.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/unit/test_bank_asym.py): new unit tests covering single-bank (`None`), V-engine (signed float) branches, and emitter-discipline assertions.
- **Applicability gate (Q6):** Emitted as a value only when `total_trim_correction_delta_b2` is not `None`. Otherwise, `None`.
- **Emitter-only stance:** Assert that OBDLab does not emit `bank_asym` or asymmetry fault verdicts.
- **Forward-registered S4 Consumer:** COMLab `T-COMV2-BANK-FUSE-1` consumes `per_bank_trim_delta` to apply the ±5% bound (Q2) and pre-2001 caveat (Q6) at Stage 4.


## VERIFICATION GATE

- [x] Computability branches verified (3 unit test cases in `test_bank_asym.py` pass).
- [x] Emitter-only discipline verified (unit test asserts that no fault classification fields are present on the payload, and `Select-String` search contains zero references to `bank_asym`, `asymmetry_verdict`, or `fault_family` in `trim_vector_aggregator.py`).
- [x] Run command: `python -m pytest tests/unit/test_bank_asym.py`
  Result: `3 passed`
- [x] Run command: `python -m pytest`
  Result: `373 passed, 6 skipped`

## CODE REVIEW

- **Validation & Computation:** `TrimVectorAggregator.aggregate()` returns a 3-tuple including the B1 - B2 `per_bank_trim_delta` value, which is correctly gated by bank-2 presence and set to `None` for single-bank setups.
- **Static Typing & Formatting:** Pyright check shows `0 errors, 0 warnings`. Ruff linting is fully clean and auto-formatted.
- **Consumer Alignment:** COMLab `T-COMV2-BANK-FUSE-1` forward-registered dependency status updated to reflect that `T-OBDV2-BANK-ASYM-1` is `done`.
