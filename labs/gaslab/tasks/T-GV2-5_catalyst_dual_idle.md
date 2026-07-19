# T-GV2-5 — Catalyst Dual-Idle Weak-vs-Dead Test

### Goal ###

Implement the dual-idle catalyst efficiency test (`TEST_DUAL_IDLE_CATALYST` from `GASWIKI-07` / §7.6) in the GASLab resolution layer. Leverage the idle ↔ 2500 RPM delta comparison when `reading_high` is provided to separate a weak/degraded catalyst (which lights off at 2500 RPM) from a dead/poisoned catalyst (which has no delta and shows engine-out pollution at both speeds), provided that engine fuel control is healthy.

Specifically:
1. Update the resolution layer (`apply_differentiators` in `GASLab/gaslab/resolution.py`):
   - When the vehicle DNA indicates `has_catalyst` is True and `reading_high` is provided:
     - Check the fuel control precondition: both the idle Brettschneider lambda (`lambda_chem(reading)`) and high-idle Brettschneider lambda (`lambda_chem(reading_high)`) must be within `[0.98, 1.02]`. If fuel control is invalid (lambda at either speed is outside this window), reject/remove both `CATALYST_NOT_LIGHTING_OFF` and `CATALYST_OVERWHELMED` candidates from the survivors (since a catalyst cannot be diagnosed with bad feed gas).
     - If fuel control is valid (lambdas within `[0.98, 1.02]`):
       - Define the working catalyst signature at 2500 RPM: `14.5 <= co2 <= 16.0`, `o2 < 0.5`, `co < 0.2`, `hc < 35`.
       - Define the weak catalyst signature at idle: `13.5 <= co2 <= 14.5`, `0.3 <= o2 <= 0.7`, `0.5 <= co <= 0.9`, `75 <= hc <= 125`.
       - Define the dead catalyst signature (raw engine-out): `co2 < 13.5`, `hc > 100`, `co > 0.5`, `o2 > 0.5`.
       - Implement the routing logic:
         - If we have a weak catalyst delta (idle is weak cat AND high is working cat):
           - Retain `CATALYST_NOT_LIGHTING_OFF` if it is a candidate.
           - Filter out/reject `CATALYST_OVERWHELMED` if it is a candidate.
         - If we have a dead catalyst (idle is dead cat AND high is dead cat):
           - Route to `CATALYST_OVERWHELMED`: if `CATALYST_NOT_LIGHTING_OFF` is a candidate, replace it with `CATALYST_OVERWHELMED` (or add `CATALYST_OVERWHELMED` if not present, and filter out `CATALYST_NOT_LIGHTING_OFF`).
           - Retain `CATALYST_OVERWHELMED` if it is a candidate.
         - Otherwise, if a high-idle reading is provided but doesn't match either pattern:
           - Filter out `CATALYST_NOT_LIGHTING_OFF` (since a weak catalyst must work at high RPM).
           - Filter out `CATALYST_OVERWHELMED` (since a dead catalyst must show raw engine-out values).
2. Write unit tests in `GASLab/tests/test_rule_engine.py` verifying:
   - Valid fuel control is a precondition: both catalyst verdicts are suppressed if lambda at either speed is outside `[0.98, 1.02]`.
   - Clear idle-vs-2500 delta (idle matches weak, high matches working) resolves to `CATALYST_NOT_LIGHTING_OFF`.
   - Raw engine-out readings at both speeds (idle matches dead, high matches dead) resolves to `CATALYST_OVERWHELMED`.
   - When high-idle is provided but does not match the working cat signature, `CATALYST_NOT_LIGHTING_OFF` is rejected.
   - When high-idle is provided but does not match the dead/raw signature, `CATALYST_OVERWHELMED` is rejected.

### Success criteria ###

- `tests/test_rule_engine.py::test_catalyst_precondition_lambda_out_of_bounds` — verifies both catalyst signatures are rejected if lambda at either speed is out of bounds.
- `tests/test_rule_engine.py::test_weak_catalyst_delta_routes_to_not_lighting_off` — verifies `CATALYST_NOT_LIGHTING_OFF` matches when the 2500-RPM reading working cat matches and low-idle is weak cat.
- `tests/test_rule_engine.py::test_dead_catalyst_raw_both_speeds_routes_to_overwhelmed` — verifies `CATALYST_OVERWHELMED` matches when both speeds show raw engine-out readings.
- All unit tests in GASLab (including 168+ existing ones) pass successfully.

### Files to touch ###

- `GASLab/gaslab/resolution.py` (MODIFY)
- `GASLab/tests/test_rule_engine.py` (MODIFY)

### Deliverables ###

1. `GASLab/gaslab/resolution.py` — Add catalyst dual-idle logic (Rule 7.6) within `apply_differentiators`.
2. `GASLab/tests/test_rule_engine.py` — Add unit tests covering the success criteria.
