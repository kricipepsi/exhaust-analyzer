> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Feature: Offline + isolation guarantees (CI-level behaviour) | Parent document: BDD_VINLab.md / shipped unit tests

## Feature: Offline + isolation guarantees (CI-level behaviour)

```gherkin
Feature: VINLab stays offline and isolated

  Scenario: Decoding makes no network or MySQL call
    Given the vinlab package and baked vinlab/data/
    When a VIN is decoded
    Then only local CSV reads and a read-only vref.db query occur

  Scenario: No cross-lab Python imports exist
    Given the vinlab package
    When the import-isolation audit runs
    Then there are no imports from gaslab, obdlab, dtclab, comlab, or symptomlab

  Scenario: All SQL is confined to the db layer
    Given the vinlab package
    When the SQL-isolation audit runs
    Then SQL strings appear only in db/tecdoc_query.py
```
*Maps to:* offline-runtime constraint, DNA-family boundary, H8.

---


## Graph relations (explicit)

**Feature: Offline + isolation guarantees (CI-level behaviour)** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_standalone.py** VERIFIES **Feature: Offline + isolation guarantees (CI-level behaviour)**
