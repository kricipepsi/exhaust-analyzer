> **Context:** DNALab BDD_DNALab v2 (2026-06-12) · Module: DNALab · Section: Feature: · Parent document: BDD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Feature: Composition happy path

```gherkin
Feature: A VIN and a complete triage compose into a VehicleDNA

  Scenario: Valid VIN and valid triage
    Given a decodable VIN and a triage with tier_1, tier_2, occurs_during, engine_state, load_state
    When build_vehicle_dna is called
    Then a VehicleDNA is returned
      And its vin_dna.vin equals the input VIN
      And its symptom_dna.tier_1_primary_symptom equals the triage tier_1
      And its symptom_dna.environmental_conditions.load_state equals the triage load_state
      And session_id starts with DNA_TX_
      And timestamp matches ISO-8601 UTC (YYYY-MM-DDTHH:MM:SSZ)
      And schema_version = 1.2
```
*Maps to:* `test_assembly.py::TestBuildVehicleDNA` (happy path, session-id, timestamp).

---

## Graph relations (explicit)

**build_vehicle_dna()** VERIFIES **valid VIN + valid triage → VehicleDNA** (test_assembly.py::TestBuildVehicleDNA)
**VehicleDNA** VERIFIES **vin_dna.vin == input VIN** (test_assembly.py)
**VehicleDNA** VERIFIES **symptom_dna.tier_1_primary_symptom == triage tier_1** (test_assembly.py)
**VehicleDNA** VERIFIES **symptom_dna.environmental_conditions.load_state == triage load_state** (test_assembly.py)
**session_id** VERIFIES **prefix DNA_TX_** (test_assembly.py)
**timestamp** VERIFIES **ISO-8601 UTC format** (test_assembly.py)
**schema_version** VERIFIES **== "1.2"** (test_assembly.py)
