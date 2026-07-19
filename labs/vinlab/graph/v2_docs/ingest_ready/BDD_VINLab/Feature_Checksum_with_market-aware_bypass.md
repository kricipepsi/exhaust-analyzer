> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Feature: Checksum with market-aware bypass | Parent document: BDD_VINLab.md / shipped unit tests

## Feature: Checksum with market-aware bypass

```gherkin
Feature: The NHTSA checksum guards North American VINs but bypasses non-NHTSA markets

  Scenario: A North American VIN with a wrong check digit fails
    Given a VIN whose WMI country is the USA and whose position-9 digit is wrong
    When the VIN is decoded
    Then a VINDecodeError is raised (checksum validation failed)

  Scenario: A European VIN without a check digit is accepted
    Given a VIN whose WMI country is in the European set
    When the checksum is validated
    Then validation is bypassed and decoding continues

  Scenario: A known OPSI corrupt-prefix VIN is accepted
    Given a VIN beginning with 3MZ, 3MD, or 3MV
    When the checksum is validated
    Then validation is bypassed (corrupt pos-9 in the source data)
```
*Maps to:* `validate_vin_checksum` (three bypass paths).

---


## Graph relations (explicit)

**Feature: Checksum with market-aware bypass** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_decoder.py** VERIFIES **Feature: Checksum with market-aware bypass**
