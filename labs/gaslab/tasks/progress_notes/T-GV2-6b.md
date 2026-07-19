# T-GV2-6b - Misfire-vs-timing precedence

## Plan

- Add survivor-level precedence after the existing T-GV2-6a cam-timing RPM gates in `GASLab/gaslab/resolution.py`.
- Prune misfire-family candidates only when a cam-timing state remains and idle HC is below `HC_IGNITION_MISFIRE_FLOOR = 1000` from `GAS_VOCABULARY 10.1`.
- Add direct `apply_differentiators` regression tests in `GASLab/tests/test_rule_engine.py` for low-HC prune, high-HC co-fault survival, and no-timing no-change.
- Consumer: COMLab `chemical_state` / fault-atlas precedence from `GAS_WIKI 8.9`; no new field or enum.

## TDD Evidence

- RED: `python3.14 -m pytest tests/test_rule_engine.py::test_timing_confirmed_prunes_low_hc_misfire -q --tb=short`
  failed with current behavior returning `['CAM_TIMING_RETARDED_MAP', 'IGNITION_MISFIRE']`.
- GREEN: the three new contracted tests passed after the survivor-prune helper landed:
  `3 passed in 0.33s`.
- Targeted file run: `python3.14 -m pytest tests/test_rule_engine.py -q --tb=short`
  passed: `42 passed`.

## Verification

- `python3.14 -m py_compile gaslab/resolution.py tests/test_rule_engine.py` - PASS.
- `python3.14 -m ruff check gaslab/resolution.py tests/test_rule_engine.py` - PASS.
- `python3.14 -m pyright gaslab/resolution.py tests/test_rule_engine.py` - PASS, 0 errors / 0 warnings.
- `python3.14 -m pytest tests/test_rule_engine.py -q --tb=short` - PASS, 42 passed.

VERIFICATION GATE - T-GV2-6b

Phase 1 (syntax):       PASS - `python3.14 -m compileall gaslab/ -q` (exit 0)
Phase 2 (type check):   PASS - `python3.14 -m pyright gaslab/` (0 errors, 0 warnings)
Phase 3 (lint):         PASS - `python3.14 -m ruff check gaslab/ tests/` (All checks passed)
Phase 4 (unit tests):   PASS - `python3.14 -m pytest tests/ -x --tb=short` (182 passed, 0 failed)
Phase 5 (provenance):   PASS - task diff has one new production numeric literal (`1000`) and it carries `# vocab: GAS_VOCABULARY 10.1`; test literals are exempt
Phase 6 (diff review):  PASS - 2 task files changed, all map to Deliverables

Notes:
- Pyright reported a tooling update notice (`v1.1.409 -> v1.1.410`), not a code warning.
- The broader package provenance scan still reports three pre-existing continuation-line hits in `gaslab/rule_engine.py`; they are outside this task diff and were not changed per the surgical-scope rule.

CODE REVIEW - T-GV2-6b

1. Design rule compliance:  PASS - no cross-lab import, no contract mutation, and the rule follows `GAS_WIKI 8.9` plus `GAS_VOCABULARY 10.1`.
2. Scope compliance:        PASS - only `resolution.py` survivor precedence and `test_rule_engine.py` regression tests changed.
3. Contract changes:        PASS - no `GasLabPayload`, `GasLabDnaView`, or enum changes.
4. Docstrings:              PASS - the new private helper and tests document the source sections and behavior.
5. Provenance:              PASS - the new HC floor literal is cited; new rule branch cites `GAS_WIKI 8.9`.
6. Immediate Checklist:     PASS - type hints present, no mutable defaults, no bare except, no new imports, and no uncited production numeric literal.
7. Test coverage:           PASS - all three contracted tests are present and green, including high-HC co-fault survival and no-timing no-change.
