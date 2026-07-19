> **Context:** SymptomLab BDD v2.1 (2026-06-12) · Module: SymptomLab · Traceability summary · Parent document: BDD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## Traceability summary

| Behaviour area | Primary test module |
|----------------|---------------------|
| Resolve happy path | `test_models.py`, `test_validator.py` |
| Catalog pair validation | `test_validator.py` |
| Environmental validation | `test_validator.py` |
| 18-pair invariant / drift | `test_drift_guard.py` |
| JSON boundary | `test_symptomdna_from_json.py` |
| Isolation / routing-free | `test_resolve_isolation.py` |
---

## Graph relations (explicit)

**BDD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**BDD_SymptomLab traceability matrix** VERIFIES **test coverage across 5 behaviour areas**
