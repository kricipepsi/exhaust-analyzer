# T-GV2-6c Progress Note

## Plan

1. Read the task spec and only the cited `GAS_WIKI §8.9`, `06b §FAULT_CAM_TIMING_RETARDED_MAF`, `resolution.py`, and `test_rule_engine.py` spans.
2. Add the three contracted tests for lean/timing co-survival precedence before production code.
3. Add a small survivor-level helper in `resolution.py` and wire it after the existing LEAN normalise and CAM_MAF persist predicates.
4. Run the GASLab inner loop, full six-phase verification gate, code review, consumer check, and graphify update.

## TDD

- RED: `python3.14 -m pytest tests/test_rule_engine.py -k "normalising_lean_keeps_lean_mixture_drops_timing or persisting_lean_keeps_timing_drops_lean_mixture or lean_family_no_cosurvival_unchanged" -q --tb=short`
  failed with 3 assertion failures because `_resolve_lean_timing_cosurvival` did not exist yet.
- GREEN: the same targeted run passed after adding the helper:
  `3 passed, 42 deselected`.
- Targeted file run: `python3.14 -m pytest tests/test_rule_engine.py -q --tb=short`
  passed: `45 passed`.

## Verification

- `python3.14 -m py_compile gaslab/resolution.py tests/test_rule_engine.py` - PASS.
- `python3.14 -m ruff check gaslab/resolution.py tests/test_rule_engine.py --fix` - PASS, all checks passed.
- `python3.14 -m pyright gaslab/resolution.py tests/test_rule_engine.py` - PASS, 0 errors / 0 warnings.
- `python3.14 -m pytest tests/test_rule_engine.py -q --tb=short` - PASS, 45 passed.
- Consumer check: COMLab reads `request.gas_lab_output.chemical_state` in `comlab/core/fault_atlas_router.py:552`, uses it for registry matching at `fault_atlas_router.py:487`, and carries `lean_condition` in `comlab/config/kg/lean_condition.json`.
- Graph update: `python -m graphify update .` via `graphify-out/.graphify_python` rebuilt the AST graph: 64,944 nodes / 89,474 edges / 4,939 communities; HTML viz skipped because the graph is above the 5,000-node visualization limit.

VERIFICATION GATE - T-GV2-6c

Phase 1 (syntax):       PASS - `python3.14 -m compileall gaslab/ -q` (exit 0)
Phase 2 (type check):   PASS - `python3.14 -m pyright gaslab/` (0 errors, 0 warnings)
Phase 3 (lint):         PASS - `python3.14 -m ruff check gaslab/ tests/` (All checks passed)
Phase 4 (unit tests):   PASS - `python3.14 -m pytest tests/ -x --tb=short` (185 passed, 0 failed)
Phase 5 (provenance):   PASS - added production numeric literals reuse existing predicates and carry `GAS_WIKI §8.9` / `wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAF` citations; diff provenance scan empty
Phase 6 (diff review):  PASS - scoped GASLab changes are `gaslab/resolution.py` and `tests/test_rule_engine.py`, both mapped to Deliverables

Notes:
- The workspace already had staged changes in the same GASLab files from prior GASLabV2 tasks; this task added only unstaged deltas on top of them.
- `pyright` reported an available version update (`1.1.409 -> 1.1.410`) but no diagnostics.

CODE REVIEW - T-GV2-6c

1. Design rule compliance:  PASS - no schema, enum, cross-lab import, or new threshold set; rule cites `GAS_WIKI §8.9` and `wikiNEW/06b §FAULT_CAM_TIMING_RETARDED_MAF`.
2. Scope compliance:        PASS - production change is limited to explicit LEAN_MIXTURE vs CAM_MAF survivor precedence in `apply_differentiators`; tests cover the three Success criteria.
3. Contract changes:        PASS - no `GasLabPayload`, `GasLabDnaView`, or `ChemicalSignature` mutation.
4. Docstrings:              PASS - new private helper has a source-cited docstring; tests document source sections and behavior.
5. Provenance:              PASS - numeric predicates carry existing wiki citations; no uncited new production numeric literal remains.
6. Immediate Checklist:     PASS - type hints present, no mutable defaults, no bare except, no new imports outside GASLab, sorted imports clean under ruff.
7. Test coverage:           PASS - all three contracted tests are present and green: normalising lean keeps LEAN, persisting lean keeps CAM_MAF, no co-survival unchanged.
