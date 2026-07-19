> **Context:** SymptomLab BDD v2.1 (2026-06-12) · Module: SymptomLab · Feature: Environmental-axis validation · Parent document: BDD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## Feature: Environmental-axis validation

```gherkin
Feature: Environmental context must use the contract vocabulary

  Scenario Outline: Out-of-vocabulary environmental values are rejected
    Given a valid catalog pair
      And occurs_during = <occ> and engine_state = <eng> and load_state = <load>
    When the selection is resolved
    Then the result is <result>

    Examples:
      | occ        | eng           | load                    | result                   |
      | always     | running       | idle                    | SymptomDNA               |
      | cold_only  | cranking      | transient_acceleration  | SymptomDNA               |
      | never      | running       | idle                    | SymptomValidationError   |
      | always     | flying        | idle                    | SymptomValidationError   |
      | always     | running       | hovering                | SymptomValidationError   |
```
*Maps to:* `tests/test_validator.py`.

---
---

## Graph relations (explicit)

**BDD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**BDD_SymptomLab "out-of-vocabulary environmental values"** VERIFIES **OccursDuring, EngineState, LoadState enum validation**
**tests/test_validator.py** VERIFIES **environmental-axis validation**
