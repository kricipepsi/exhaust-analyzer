> **Context:** SymptomLab BDD v2.1 (2026-06-12) · Module: SymptomLab · Feature: The 18-pair invariant · Parent document: BDD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## Feature: The 18-pair invariant

```gherkin
Feature: The catalog must define exactly 18 pairs

  Scenario: A catalog of the wrong size fails at construction
    Given an allowed_combinations.yaml that does not define exactly 18 pairs
    When the SymptomValidator is constructed
    Then a ValueError is raised before any triage is validated

  Scenario: The shipped catalog is the curated 6x3 set
    Given the default allowed_combinations.yaml
    When the SymptomValidator is constructed
    Then it loads exactly 18 (tier_1, tier_2) pairs
```
*Maps to:* `tests/test_drift_guard.py`.

> **Live state:** the shipped `allowed_combinations.yaml` defines exactly **18** pairs,
> with `visible_exhaust_smoke = {black_smoke, blue_oily_smell, white_sweet_smell}`
> (reconciled by T-DNA-8). Both scenarios above pass against the live file.

---
---

## Graph relations (explicit)

**BDD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**BDD_SymptomLab "wrong-size catalog"** VERIFIES **SymptomValidator construction invariant**
**tests/test_drift_guard.py** VERIFIES **18-pair invariant**
