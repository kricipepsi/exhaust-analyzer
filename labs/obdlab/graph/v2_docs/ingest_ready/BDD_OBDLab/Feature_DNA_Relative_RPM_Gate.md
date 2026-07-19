> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: DNA-relative RPM gate · Parent document: BDD_OBDLab.md

## Feature: DNA-relative RPM gate (three-branch confidence)

```gherkin
Feature: The RPM ceiling tightens with VIN-decode confidence

  Scenario: HIGH confidence enforces the DNA rated-RPM ceiling
    Given confidence = HIGH and rated_rpm = 6500
      And engine_rpm exceeds rated_rpm × 1.05
    When the translator runs
    Then a PIDValidationError is raised

  Scenario: PARTIAL confidence logs and falls back to static bounds
    Given confidence = PARTIAL
    When the translator runs
    Then the DNA-RPM check is downgraded and only the static 0–8000 bound applies

  Scenario: NONE confidence (or no DNA view) uses static bounds only
    Given confidence = NONE
    When the translator runs
    Then no DNA-relative RPM check is applied
```

### Entity: DNA-RPM gate test mapping

- **Tests:** `test_pid_ingestion_validator` (DNA-RPM three-branch)

## Graph relations (explicit)

**test_pid_ingestion_validator.py** VERIFIES **DNA-RPM three-branch gate** (HIGH/PARTIAL/NONE)
**_check_dna_rpm** VERIFIES **engine_rpm > rated_rpm × 1.05** (HIGH confidence only)
**VinConfidence.HIGH** CONSUMES **_DNA_RPM_HEADROOM = 1.05** (# wiki: §3)
**VinConfidence.PARTIAL** CONSUMES **log + fallthrough to static bounds**
**VinConfidence.NONE** CONSUMES **static [0, 8000] only** (no DNA-RPM check)
**BDD_OBDLab v2.0** VERIFIES **DNA-RPM gate three-branch behaviour**
