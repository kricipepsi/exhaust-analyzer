# T-OBDV2-FIX-3 — De-state orchestrator MAF linearity

## Plan
We will de-state the two-point MAF/MAP linearity check in `SensorSignalTranslator` by:
1. Removing the mutable instance state `self._last_stabilized_idle` and `self._last_stress_idle` from `SensorSignalTranslator.__init__`.
2. Defining a new `LinearityAccumulator` helper class in `obdlab.core.sensor_signal_translator`:
   ```python
   class LinearityAccumulator:
       def __init__(self) -> None:
           self.stabilized_idle: tuple[float, float] | None = None
           self.stress_idle: tuple[float, float] | None = None
   ```
3. Modifying `SensorSignalTranslator.translate` to accept an optional `accumulator: LinearityAccumulator | None = None` argument.
4. Implementing the two-point MAF linearity check using the provided `accumulator` object. The translator itself remains stateless: multiple sequential calls or different instances using different accumulators will not leak state.
5. Updating `tests/unit/test_maf_linearity.py` to use `LinearityAccumulator` when checking the two-point guard.
6. Adding a new unit test to explicitly verify that two separate `SensorSignalTranslator` calls with different accumulators (or in different orders) are order-independent and do not leak state.

## VERIFICATION GATE
- [x] `ruff check obdlab/ && pyright obdlab/` clean
- [x] `pytest -x -q` green
- [x] No `_last_stabilized_idle` or `_last_stress_idle` present in `SensorSignalTranslator.__init__` (verified via `grep`)
- [x] Verification suite passes and all 381 tests run clean

## CODE REVIEW
- [x] Checked for thread-safety and state isolation (translator class carries no mutable state; state resides entirely in the caller-owned `LinearityAccumulator`).
- [x] Verified that `w_theo` and `sensor_error_delta` are only emitted when both bands are captured in the provided `accumulator`.
- [x] Confirmed order-independence (reversed call order yields correct delta).
