# T-GV2-7 Progress Note

## Plan

1. Read the authored task spec, cited `CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR` wiki section, and the target code in `gaslab/resolution.py`.
2. Add the leaf routing logic in `apply_differentiators` after the lean co-survival block, only when `reading_high` is not None.
3. Map `POA_SIGNATURE` and co-surviving `WORN_*` candidates to specific wear leaves (`WORN_VALVE_SEALS`, `WORN_PISTON_RINGS`, `WORN_ENGINE`, or stay on `POA_SIGNATURE`) based on idle->2500 RPM HC change direction, high-idle CO, and chemistry lambda.
4. Implement targeted test cases in `tests/test_rule_engine.py` covering:
   - valve seals (sharp HC drop, low CO, stoich λ)
   - piston rings (rising HC, high CO, rich λ)
   - worn engine (flat moderate HC, flat/slight CO rise, stoich-leaning λ)
   - severe persistent POA mismatch (extreme persistent HC, λ mismatch)
   - idle-only fallback (no `reading_high`, behavior unchanged)
5. Run the inner verification loop, full verification gate, and code review.

## TDD

- RED: Initial tests failed with `EVAP_CANISTER_SATURATED` or `WORN_VALVE_SEALS` because of incorrect lambda calculations or unmatched target ranges.
- GREEN: After adjusting test gas reading values to calculate to appropriate Brettschneider lambda boundaries, all targeted test cases passed: `5 passed`.
- Targeted module run: `python3.14 -m pytest tests/test_rule_engine.py -q --tb=short` passed: `54 passed`.

## Verification

- `python3.14 -m py_compile gaslab\resolution.py tests\test_rule_engine.py` - PASS.
- `..\.venv-wired\Scripts\ruff.exe check gaslab/ tests/` - PASS, all checks passed.
- `..\.venv-wired\Scripts\pyright.exe gaslab/` - PASS, 0 errors / 0 warnings.
- `python3.14 -m pytest tests/ -x --tb=short` - PASS, 194 passed.
- Provenance audit: PASS, empty output. Every new numeric literal carries a `# wiki:` comment pointing to `docs/GASLab/wikiNEW/06a_fault_atlas_oil_mechanical.md §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR`.
- Consumer check: PASS, mechanical-wear family candidates (`WORN_VALVE_SEALS`, `WORN_PISTON_RINGS`, `WORN_ENGINE`, `POA_SIGNATURE`) route to COMLab `chemical_state` / fault-atlas routing (GASWIKI-06A). No new field or enum is added.

VERIFICATION GATE - T-GV2-7

Phase 1 (syntax):       PASS - python3.14 -m compileall gaslab/ -q (exit 0)
Phase 2 (type check):   PASS - pyright gaslab/ (0 errors, 0 warnings)
Phase 3 (lint):         PASS - ruff check gaslab/ tests/ (All checks passed)
Phase 4 (unit tests):   PASS - pytest tests/ -x --tb=short (194 passed, 0 failed)
Phase 5 (provenance):   PASS - every numeric literal in diff has wiki/vocab citation
Phase 6 (diff review):  PASS - 2 files changed, all map to Deliverables

Notes:
- `pyright` reported an available version update (`1.1.409 -> 1.1.410`) but no diagnostics.

CODE REVIEW - T-GV2-7

1. Design rule compliance:  PASS - no new schema field or enum; matches petrol-only 5-gas, no cross-lab imports.
2. Scope compliance:        PASS - limited strictly to the leaf router inside apply_differentiators and test cases.
3. Contract changes:        PASS - no contract changes.
4. Docstrings:              PASS - tests and logic documented clearly with wiki references.
5. Provenance:              PASS - every numeric literal in the diff carries a wiki citation to 06a §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR.
6. Immediate Checklist:     PASS - type hints present, no mutable defaults, no bare except, pathlib unaffected, sorted imports clean.
7. Test coverage:           PASS - added 5 tests covering all wear leaves and fallback.
