> **Context:** DNALab BDD_DNALab v2 (2026-06-12) · Module: DNALab · Section: Feature: · Parent document: BDD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Feature: Version guard

```gherkin
Feature: Cross-version payloads are rejected, never silently coerced

  Scenario: A matching version deserialises
    Given a payload whose schema_version equals SCHEMA_VERSION
    When from_json_payload is called
    Then a VehicleDNA is returned

  Scenario: A mismatched version is rejected
    Given a payload whose schema_version is not SCHEMA_VERSION
    When from_json_payload is called
    Then a ValueError is raised (schema_version mismatch)

  Scenario: A missing top-level key is rejected
    Given a payload missing session_id
    When from_json_payload is called
    Then a KeyError is raised
```
*Maps to:* `test_models.py`, `test_assembly.py::TestSchemaVersion`.

---

## Graph relations (explicit)

**VehicleDNA.from_json_payload()** VERIFIES **matching version deserialises** (test_models.py)
**VehicleDNA.from_json_payload()** VERIFIES **mismatched version raises ValueError** (test_assembly.py::TestSchemaVersion)
**VehicleDNA.from_json_payload()** VERIFIES **missing top-level key raises KeyError** (test_models.py)
