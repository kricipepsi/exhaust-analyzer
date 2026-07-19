# Progress Notes — T-GV2-4

## Plan
1. Update `GasLabContext` in [process.py](file:///C:/Users/muto/claude/4DApp/4DLab/GASLab/gaslab/process.py) to hold `reading_high: GasReading | None = None`.
2. Update `classify()` in [rule_engine.py](file:///C:/Users/muto/claude/4DApp/4DLab/GASLab/gaslab/rule_engine.py) to accept `reading_high` and forward it to `_definitive_match()` and `_resolve_candidates()`.
3. Update `wrong_valve_timing_rule` in `rule_engine.py` (priority 82) to check `reading_high` against the high-RPM signature for `CAM_TIMING_RETARDED_MAF` and `CAM_TIMING_ADVANCED` if it is present.
4. Implement priority 40 rich timing fallback rule for `CAM_TIMING_RETARDED_MAP` (which partially normalises at 2500 RPM) inside `_definitive_match()` in `rule_engine.py`.
5. Update `apply_differentiators` in [resolution.py](file:///C:/Users/muto/claude/4DApp/4DLab/GASLab/gaslab/resolution.py) to filter out `CAM_TIMING_RETARDED_MAF`, `CAM_TIMING_ADVANCED`, and `CAM_TIMING_RETARDED_MAP` when `reading_high` is provided but fails to match their respective high-idle signatures.
6. Implement `LEAN_MIXTURE` normalisation checks in `apply_differentiators()`: if `reading_high` does not normalise (O2 < 1.0% and lambda in `[0.985, 1.015]`), reject `LEAN_MIXTURE`.
7. Update `rank_candidates()` and `classify_top3()` in [ranking.py](file:///C:/Users/muto/claude/4DApp/4DLab/GASLab/gaslab/ranking.py) to accept and forward `reading_high`.
8. Update the composition layer `_run_gaslab` and `_build_gas_lab_result` in [composition.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/apps/wired/wired/composition.py) to parse high-idle inputs into `reading_high: GasReading` and feed them into `GasLabContext` and `gas_classify_top3`.
9. Update streamlit frontend [app.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/apps/wired/app.py) to merge high-idle gases into `gas_inputs` if they are populated.
10. Add and refine unit tests in [test_rule_engine.py](file:///C:/Users/muto/claude/4DApp/4DLab/GASLab/tests/test_rule_engine.py) to cover retarded timing, advanced timing, MAP timing, and lean mixture normalisation.

## Verification Gate
```
VERIFICATION GATE — T-GV2-4
Phase 1 (syntax):       PASS — python -m compileall gaslab/ 4DLabWired/
Phase 2 (type check):   PASS — pyright gaslab/ (0 errors, 0 warnings)
Phase 3 (lint):         PASS — ruff check gaslab/ 4DLabWired/ tests/
Phase 4 (unit tests):   PASS — pytest tests/ in GASLab (168 passed), pytest in 4DLabWired (177 passed)
Phase 5 (provenance):   PASS — inline citations updated for wrong_valve_timing_rule and RPM-differential check
Phase 6 (diff review):  PASS — changes mapped exactly to Deliverables
```

## Code Review
```
CODE REVIEW — T-GV2-4
1. Design rule compliance:  PASS — Dual-RPM tailpipe checks implemented, resolution layer correctly filters timing candidates, LEAN_MIXTURE normalisation check verified.
2. Scope compliance:        PASS — Staged paths strictly map to the task deliverables.
3. Contract changes:        PASS — GasLabContext updated with reading_high; composition and UI layers pass high-idle readings.
4. Docstrings:              PASS — Updated docstrings for modified functions.
5. Provenance:              PASS — Every updated/added RPM-differential threshold has a wiki/vocab citation.
6. Immediate Checklist:     PASS — Checked type annotations, docstrings, path operations, and sorting.
7. Test coverage:           PASS — Added comprehensive unit tests covering the four dual-RPM criteria, all green.
```
