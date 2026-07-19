> **Context:** SymptomLab BDD v2.1 (2026-06-12) · Module: SymptomLab · Feature: Catalog pair validation · Parent document: BDD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## Feature: Catalog pair validation

```gherkin
Feature: Only catalog pairs are accepted, with actionable errors otherwise

  Scenario: An unknown tier_2 lists the valid sub-filters
    Given tier_1 = visible_exhaust_smoke and tier_2 = green_smoke
    When the selection is resolved
    Then a SymptomValidationError is raised
      And the message lists the valid tier_2 values for visible_exhaust_smoke

  Scenario: An unknown tier_1 lists the valid categories
    Given tier_1 = nonexistent_symptom and tier_2 = anything
    When the selection is resolved
    Then a SymptomValidationError is raised
      And the message lists the six valid tier_1 values
```
*Maps to:* `tests/test_validator.py`.

---
---

## Graph relations (explicit)

**BDD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**BDD_SymptomLab "unknown tier_2"** VERIFIES **SymptomValidationError with valid options**
**BDD_SymptomLab "unknown tier_1"** VERIFIES **SymptomValidationError with valid categories**
**tests/test_validator.py** VERIFIES **catalog pair validation**
