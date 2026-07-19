> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: PID validation and bounds · Parent document: BDD_OBDLab.md

## Feature: PID validation and bounds

```gherkin
Feature: Out-of-range PIDs are rejected before any analytics

  Scenario: Engine RPM above the static ceiling
    Given engine_rpm = 9000 (ceiling is 8000)
    When the translator runs
    Then a PIDValidationError is raised

  Scenario: Alternate-unit input is converted to canonical form
    Given coolant_temp_f is supplied and coolant_temp_c is absent
    When the translator runs
    Then the value is converted with (F − 32) × 5/9 before bounds checking

  Scenario: Canonical key wins over an alternate unit
    Given both coolant_temp_c and coolant_temp_f are present
    When the translator runs
    Then coolant_temp_c is used and coolant_temp_f is dropped
```

### Entity: PID validation test mapping

- **Tests:** `integration/test_pipeline_smoke::test_smoke_bounds_violation`, `test_pid_ingestion_validator`

## Graph relations (explicit)

**test_pipeline_smoke.py** VERIFIES **bounds violation rejection** (test_smoke_bounds_violation)
**test_pid_ingestion_validator.py** VERIFIES **PID validation and bounds** (unit tests)
**_validate_bounds** VERIFIES **12 fields vs physical_sensor_bounds.json** (static ceiling check)
**_apply_unit_conversions** VERIFIES **canonical key precedence** (_c wins over _f)
**BDD_OBDLab v2.0** VERIFIES **PIDValidationError on bounds violation**
