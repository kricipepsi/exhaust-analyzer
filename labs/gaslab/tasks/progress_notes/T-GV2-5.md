# T-GV2-5 — Catalyst Dual-Idle Weak-vs-Dead Test progress notes

### Plan ###

1. Implement the catalyst dual-idle test logic in the resolution layer (`apply_differentiators` in `resolution.py`), checking for:
   - Fuel control precondition (lambda at both speeds in `[0.98, 1.02]`).
   - Weak catalyst delta (idle matches weak, high idle matches working).
   - Dead catalyst (both speeds match raw engine-out).
2. Filter candidates based on the routing results.
3. Add unit tests in `test_rule_engine.py` covering all cases.
4. Verify using pytest.

---

VERIFICATION GATE — T-GV2-5
Phase 1 (syntax):       PASS — python -m compileall gaslab/
Phase 2 (type check):   PASS — pyright gaslab/ (0 errors, 0 warnings)
Phase 3 (lint):         PASS — ruff check gaslab/ tests/
Phase 4 (unit tests):   PASS — pytest tests/ (171 passed, 0 failed)
Phase 5 (provenance):   PASS — every numeric literal in diff has wiki/vocab citation
Phase 6 (diff review):  PASS — 2 files changed, all map to Deliverables

---

CODE REVIEW — T-GV2-5
1. Design rule compliance:  PASS — honors GAS_WIKI §7.6 / GAS_VOCABULARY
2. Scope compliance:        PASS — only resolution.py and test_rule_engine.py touched
3. Contract changes:        PASS — no contract changes
4. Docstrings:              PASS — internal logic updated, test functions have docstrings
5. Provenance:              PASS — all added numeric literals carry '# wiki: GAS_WIKI §7.6'
6. Immediate Checklist:     PASS — type hints, no magic numbers, standard constructs
7. Test coverage:           PASS — three new test cases added for catalyst dual-idle test
