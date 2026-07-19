> **Context:** SymptomLab BDD v2.1 (2026-06-12) · Module: SymptomLab · Feature: Resolve happy path · Parent document: BDD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## Feature: Resolve happy path

```gherkin
Feature: A legal triage selection resolves to a 4-field SymptomDNA

  Scenario: A valid pair with valid environmental context
    Given tier_1 = rough_idle_shudder and tier_2 = surging_hunting_idle
      And occurs_during = cold_only and engine_state = running and load_state = idle
    When the selection is resolved
    Then a SymptomDNA is returned with exactly four fields
      And environmental_conditions.occurs_during = cold_only
      And environmental_conditions.load_state = idle
      And the SymptomDNA serialises to JSON and reloads unchanged
      And the payload contains no routing fields
```
*Maps to:* `tests/test_models.py`, `tests/test_validator.py`.

---
---

## Graph relations (explicit)

**BDD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**BDD_SymptomLab "legal triage selection"** VERIFIES **symptomlab.resolve**
**tests/test_models.py** VERIFIES **SymptomDNA 4-field structure**
**tests/test_validator.py** VERIFIES **resolve happy path**
