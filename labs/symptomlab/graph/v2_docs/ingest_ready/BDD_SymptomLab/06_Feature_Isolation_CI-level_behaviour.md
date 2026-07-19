> **Context:** SymptomLab BDD v2.1 (2026-06-12) · Module: SymptomLab · Feature: Isolation (CI-level behaviour) · Parent document: BDD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## Feature: Isolation (CI-level behaviour)

```gherkin
Feature: SymptomLab stays an isolated codebase

  Scenario: No cross-lab Python imports exist
    Given the symptomlab package
    When the import-isolation audit runs
    Then there are no imports from gaslab, obdlab, dtclab, comlab, or vinlab

  Scenario: SymptomDNA carries no routing fields
    Given a resolved SymptomDNA
    When its keys are inspected
    Then there is no suppress_modes, prioritize_modes, or target_backend_equation
```
*Maps to:* `tests/test_resolve_isolation.py`.

---
---

## Graph relations (explicit)

**BDD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**BDD_SymptomLab "no cross-lab imports"** VERIFIES **SymptomLab import isolation**
**BDD_SymptomLab "no routing fields"** VERIFIES **SymptomDNA routing-free invariant**
**tests/test_resolve_isolation.py** VERIFIES **import isolation and routing-free invariant**
