# Progress Notes — T-GV2-1

## Plan
1. Reconcile the ChemicalSignature StrEnum count in `gaslab/contracts.py` to 34 members by removing `WRONG_VALVE_TIMING` and inserting the three system-specific states: `CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, and `CAM_TIMING_ADVANCED`.
2. Update the `SIGNATURE_TO_FAMILY` mapping in `gaslab/family_map.py` to map the three new states to the `"cam_timing"` family.
3. Rebind the `wrong_valve_timing_rule` in `gaslab/rule_engine.py` using the 06B gas-direction discriminator (Speed-Density/MAP rich, MAF lean, advanced mild-lean) using the simplified lambda calculations.
4. Replace the old WVT rule and fault record in `gaslab/data/gas_lab_ontology.yaml` with the three new records and their corresponding gas bounds and citations.
5. Update WVT and enum tests in `tests/test_contracts.py`, `tests/test_rule_engine.py`, `tests/test_validators.py`, and `tests/unit/test_rule_engine_reachability.py` to align with the 34-value enum and verify the correctness of the new classification rules.
6. Ensure that all 164 unit tests run and pass cleanly.

## Verification Gate
```
VERIFICATION GATE — T-GV2-1
Phase 1 (syntax):       PASS — python -m compileall gaslab/
Phase 2 (type check):   PASS — pyright gaslab/ (0 errors, 0 warnings)
Phase 3 (lint):         PASS — ruff check gaslab/ tests/
Phase 4 (unit tests):   PASS — pytest tests/ (164 passed, 0 failed)
Phase 5 (provenance):   PASS — every numeric literal in diff has wiki/vocab citation
Phase 6 (diff review):  PASS — 10 files changed, all map to Deliverables
```

## Code Review
```
CODE REVIEW — T-GV2-1
1. Design rule compliance:  PASS — Reconciled to the v2.1 timing-taxonomy revision (34-value enum).
2. Scope compliance:        PASS — Staged paths strictly map to the task deliverables.
3. Contract changes:        PASS — ChemicalSignature updated to 34 values, removing WRONG_VALVE_TIMING and adding 3 timing states.
4. Docstrings:              PASS — Updated docstrings for ChemicalSignature enum to reflect 34-value count.
5. Provenance:              PASS — Every updated/added numeric threshold has a wiki/vocab citation.
6. Immediate Checklist:     PASS — Checked type annotations, docstrings, path operations, and sorting.
7. Test coverage:           PASS — Added tests for enum count and reachability, all green.
```
