# T-GV2-4 — Dual-RPM Input and Separation Matrix

### Goal ###

Implement dual-RPM tailpipe gas diagnostics in GASLab. Enable `process()` to accept an optional 2500-RPM `GasReading`, and use the idle ↔ 2500 RPM delta in the resolution layer to implement `TEST_RPM_SEPARATION_MATRIX` (GASWIKI-08) and system-specific VVT/cam-timing behavior (GASWIKI-04 / RULE_WVT).

Specifically:
1. Update `GasLabContext` to hold an optional `reading_high: Optional[GasReading] = None`.
2. Update the public `process()` function to pass `context.reading_high` to `classify()`.
3. Update `classify()` in `rule_engine.py` to accept `reading_high` and pass it to `_definitive_match()` and `_resolve_candidates()`.
4. Implement the RPM-differential check in the `wrong_valve_timing_rule` at priority 82 inside `_definitive_match()` to verify the 2500-RPM signatures for `CAM_TIMING_RETARDED_MAF` and `CAM_TIMING_ADVANCED`.
5. Implement the rich timing branch rule in `_definitive_match()` at priority 40 (fallback) for `CAM_TIMING_RETARDED_MAP` (which partially normalises at 2500 RPM).
6. Implement vacuum leak (`LEAN_MIXTURE`) normalisation checks in the resolution layer (`apply_differentiators` in `resolution.py`): if `LEAN_MIXTURE` is a candidate and `reading_high` is provided, it must normalise (`o2 < 1.0%` and lambda in `[0.985, 1.015]`). If it does not, reject `LEAN_MIXTURE` so that sensor biases or mechanical faults are evaluated.
7. Update the wired composition layer `_run_gaslab` in `4DLabWired/wired/composition.py` to construct `reading_high` when `co_high`, `co2_high`, etc. are present in the `gas_inputs` and update the Streamlit app `app.py` to pass high-idle gases in `gas_inputs` when calling `diagnose()`.

### Success criteria ###

- `tests/test_rule_engine.py::test_cam_timing_retarded_maf_persists_at_2500` — verifies `CAM_TIMING_RETARDED_MAF` matches when the 2500-RPM reading matches the persistent lean vector, but falls back/rejects if it doesn't.
- `tests/test_rule_engine.py::test_cam_timing_advanced_nox_rises` — verifies `CAM_TIMING_ADVANCED` matches when the 2500-RPM reading shows high NOx (300–900 ppm), and rejects if it doesn't.
- `tests/test_rule_engine.py::test_cam_timing_retarded_map_partially_normalises` — verifies `CAM_TIMING_RETARDED_MAP` matches when the 2500-RPM reading partially normalises (lower CO, higher lambda), and rejects if it doesn't.
- `tests/test_rule_engine.py::test_lean_mixture_vacuum_leak_normalises` — verifies `LEAN_MIXTURE` is selected if the 2500-RPM reading normalises, but rejected in favor of other faults if it doesn't.
- All existing tests in GASLab and 4DLabWired are passing.

### Files to touch ###

- `GASLab/gaslab/process.py` (MODIFY)
- `GASLab/gaslab/rule_engine.py` (MODIFY)
- `GASLab/gaslab/resolution.py` (MODIFY)
- `4DLabWired/wired/composition.py` (MODIFY)
- `4DLabWired/app.py` (MODIFY)
- `GASLab/tests/test_rule_engine.py` (MODIFY)

### Deliverables ###

1. `GASLab/gaslab/process.py` — Add `reading_high` to `GasLabContext` and pass to `classify`.
2. `GASLab/gaslab/rule_engine.py` — Rebind `wrong_valve_timing_rule` and add priority 40 `CAM_TIMING_RETARDED_MAP` rule.
3. `GASLab/gaslab/resolution.py` — Update `apply_differentiators` to accept `reading_high` and perform the vacuum leak normalisation check.
4. `4DLabWired/wired/composition.py` — Construct `reading_high` from high-idle input fields and include in `GasLabContext`.
5. `4DLabWired/app.py` — Pass high-idle inputs from Streamlit session state in `gas_inputs`.
6. `GASLab/tests/test_rule_engine.py` — Add unit tests covering the four success criteria.
