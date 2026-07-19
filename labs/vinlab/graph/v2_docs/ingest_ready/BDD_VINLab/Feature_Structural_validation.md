> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Feature: Structural validation | Parent document: BDD_VINLab.md / shipped unit tests

## Feature: Structural validation

```gherkin
Feature: Malformed input is rejected before any resolution

  Scenario: Input is not 17 characters
    Given an input string of length 15
    When the VIN is decoded
    Then a ChassisNumberError is raised (a VINDecodeError subclass)

  Scenario: Visually ambiguous characters are recovered before validation
    Given a VIN containing the letters I and O
    When the VIN is decoded
    Then I is substituted with 1 and O with 0 before the charset check

  Scenario: An invalid character set is rejected
    Given a cleaned VIN containing a Q
    When the VIN is decoded
    Then a VINDecodeError is raised (invalid characters)
```
*Maps to:* `pre_clean_vin`, length guard, `_VIN_PATTERN` check.

---


## Graph relations (explicit)

**Feature: Structural validation** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_decoder.py** VERIFIES **Feature: Structural validation**
