> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Feature: Two-path engine resolution | Parent document: BDD_VINLab.md / shipped unit tests

## Feature: Two-path engine resolution

```gherkin
Feature: Engine resolves from the modern VDS or the legacy position-8 fallback

  Scenario: Modern five-character VDS match
    Given a VIN whose brand + positions 4-8 match a vds_full key
    When the engine is resolved
    Then the full-VDS row is returned

  Scenario: Legacy single-character position-8 fallback
    Given no vds_full match but a brand + position-8 match
    When the engine is resolved
    Then the pos_8_only row is returned

  Scenario: No engine match downgrades confidence to NONE
    Given neither path matches
    When the VIN is decoded
    Then engine_not_in_csv is flagged and confidence = NONE
```
*Maps to:* `_resolve_engine`, confidence grading.

---


## Graph relations (explicit)

**Feature: Two-path engine resolution** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_csv_suite.py** VERIFIES **Feature: Two-path engine resolution**
