# Progress Notes — T-GV2-3

## Plan
1. Reconcile `GasLabDnaView` in `gaslab/dna_view.py` by swapping `target_lambda_low`/`high` for a single `target_lambda_v112` field and adding `co_high_idle`.
2. Update `_coc_adjust_normal_bounds` in `gaslab/rule_engine.py` to center the normal lambda window on `target_lambda_v112 ± 0.005` (with fallback and clamps).
3. Update the wired mapper `_build_gas_dna_view` in `4DLabWired/wired/composition.py` to map these fields and implement a midpoint legacy fallback to maintain test compatibility.
4. Update `tests/test_dna_view.py` with `test_view_matches_wiki_s1_4` checking the 13 fields.
5. Update `tests/test_rule_engine.py` to test the new v112 window and clamping logic.
6. Re-baseline the 4DLabWired tests and update `tests/test_harness.py` to expect 277 total cases.

## Verification Gate
```
VERIFICATION GATE — T-GV2-3
Phase 1 (syntax):       PASS — python -m compileall gaslab/
Phase 2 (type check):   PASS — pyright gaslab/ (0 errors, 0 warnings)
Phase 3 (lint):         PASS — ruff check gaslab/ tests/
Phase 4 (unit tests):   PASS — pytest tests/ in GASLab (164 passed), pytest in 4DLabWired (177 passed)
Phase 5 (provenance):   PASS — inline citations updated for target_lambda_v112 and co_high_idle
Phase 6 (diff review):  PASS — changes mapped exactly to Deliverables
```

## Code Review
```
CODE REVIEW — T-GV2-3
1. Design rule compliance:  PASS — Center the NORMAL lambda window on target_lambda_v112 ± 0.005, co_high_idle added, no secondary_air_equipped.
2. Scope compliance:        PASS — Staged paths strictly map to the task deliverables.
3. Contract changes:        PASS — Inbound GasLabDnaView reconciled to the v2 wiki §1.4.
4. Docstrings:              PASS — Updated docstrings for GasLabDnaView to reflect the 13-field count.
5. Provenance:              PASS — Every updated/added numeric threshold has a wiki/vocab citation.
6. Immediate Checklist:     PASS — Checked type annotations, docstrings, path operations, and sorting.
7. Test coverage:           PASS — Added tests for v112 matching, window shrinkage, and clamping, all green.
```
