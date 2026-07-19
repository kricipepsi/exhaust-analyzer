> **Context:** DNALab BDD_DNALab v2 (2026-06-12) · Module: DNALab · Section: Feature: · Parent document: BDD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Feature: Fail-fast and exception propagation

```gherkin
Feature: Producer errors propagate; incomplete triage fails before the decode

  Scenario: A missing triage key fails before the VIN is decoded
    Given a triage dict with only tier_1
    When build_vehicle_dna is called
    Then a SymptomValidationError is raised
      And vinlab.decode is not reached

  Scenario: An invalid VIN propagates the decode error
    Given an undecodable VIN and a complete triage
    When build_vehicle_dna is called
    Then a VINDecodeError is raised

  Scenario: An invalid triage selection propagates the symptom error
    Given a complete-but-nonsensical triage (unknown symptom, bad environmental values)
    When build_vehicle_dna is called
    Then a SymptomValidationError is raised
```
*Maps to:* `test_assembly.py` (`test_missing_triage_key_...`, `test_invalid_vin_propagates`,
`test_invalid_triage_propagates`).

---

## Graph relations (explicit)

**build_vehicle_dna()** VERIFIES **missing triage key → SymptomValidationError before decode** (test_assembly.py)
**build_vehicle_dna()** VERIFIES **invalid VIN → VINDecodeError propagates** (test_assembly.py)
**build_vehicle_dna()** VERIFIES **invalid triage → SymptomValidationError propagates** (test_assembly.py)
