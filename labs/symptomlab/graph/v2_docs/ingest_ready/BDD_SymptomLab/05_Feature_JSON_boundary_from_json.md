> **Context:** SymptomLab BDD v2.1 (2026-06-12) · Module: SymptomLab · Feature: JSON boundary (from_json) · Parent document: BDD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## Feature: JSON boundary (from_json)

```gherkin
Feature: from_json validates structure and enums, not the catalog invariant

  Scenario: A well-formed payload deserialises
    Given a JSON payload with the four fields and valid environmental enums
    When SymptomDNA.from_json is called
    Then a SymptomDNA is returned

  Scenario: A missing required field is rejected
    Given a JSON payload without tier_2_subfield_filter
    When SymptomDNA.from_json is called
    Then a SymptomValidationError is raised (missing required field)

  Scenario: A bad environmental enum string is rejected
    Given a JSON payload whose engine_state is fictional
    When SymptomDNA.from_json is called
    Then a SymptomValidationError is raised

  Scenario: from_json does not enforce the catalog pairing
    Given a JSON payload whose (tier_1, tier_2) is not a catalog pair but is structurally valid
    When SymptomDNA.from_json is called
    Then a SymptomDNA is returned (the pairing invariant is resolve()'s job)
```
*Maps to:* `tests/test_symptomdna_from_json.py`.

---
---

## Graph relations (explicit)

**BDD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**BDD_SymptomLab "well-formed payload"** VERIFIES **SymptomDNA.from_json deserialization**
**BDD_SymptomLab "from_json does not enforce catalog"** VERIFIES **from_json scope**
**tests/test_symptomdna_from_json.py** VERIFIES **JSON boundary**
