> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Feature: Decode happy path | Parent document: BDD_VINLab.md / shipped unit tests

## Feature: Decode happy path

```gherkin
Feature: A well-formed in-scope VIN decodes to a graded VinDNA

  Scenario: A clean petrol VIN with full reference data
    Given a 17-character VIN that passes charset and checksum
      And the WMI, year, and engine code all resolve from reference data
      And the engine row is present in vref.db with no NULL CoC fields
    When the VIN is decoded
    Then a VinDNA is returned
      And confidence = HIGH
      And induction_type, fuel_delivery_type and air_metering_strategy are enum-typed
      And the VinDNA serialises to JSON and reloads unchanged
```
*Maps to:* decoder happy-path fixtures under `tests/fixtures/`.

---


## Graph relations (explicit)

**Feature: Decode happy path** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_decoder.py** VERIFIES **Feature: Decode happy path**
