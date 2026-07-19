> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Feature: Petrol-only scope guard (H1) | Parent document: BDD_VINLab.md / shipped unit tests

## Feature: Petrol-only scope guard (H1)

```gherkin
Feature: Non-petrol vehicles are out of scope

  Scenario: A diesel fuel keyword in the CSV row is rejected
    Given an engine row whose fuel_system_type contains DIESEL
    When the VIN is decoded
    Then a VINDecodeError is raised (fuel type out of scope)

  Scenario: A non-petrol fuel keyword in the vref.db row is rejected
    Given a vref.db row whose fuel_delivery_type contains LPG, CNG, E85, HYBRID, or ELECTRIC
    When the VIN is decoded
    Then a VINDecodeError is raised (fuel type out of scope)
```
*Maps to:* `_is_non_petrol` (CSV + vref.db checks).

---


## Graph relations (explicit)

**Feature: Petrol-only scope guard (H1)** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_decoder.py** VERIFIES **Feature: Petrol-only scope guard (H1)**
