> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Feature: WMI and low-volume manufacturers | Parent document: BDD_VINLab.md / shipped unit tests

## Feature: WMI and low-volume manufacturers

```gherkin
Feature: WMI resolves standard and low-volume manufacturers

  Scenario: A standard manufacturer resolves from positions 1-3
    Given a VIN whose first three characters are a known WMI
    When the WMI is resolved
    Then the brand and country are taken from that WMI record

  Scenario: A low-volume manufacturer uses the extended WMI
    Given a VIN whose third character is 9
    When the WMI is resolved
    Then the 6-character key (positions 1-3 + 12-14) is tried first

  Scenario: An unknown WMI is a decode failure
    Given a VIN whose WMI is not in the registry
    When the WMI is resolved
    Then a VINDecodeError is raised (WMI not found)
```
*Maps to:* `_resolve_wmi`.

---


## Graph relations (explicit)

**Feature: WMI and low-volume manufacturers** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_decoder.py** VERIFIES **Feature: WMI and low-volume manufacturers**
