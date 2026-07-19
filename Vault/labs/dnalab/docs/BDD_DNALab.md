# BDD — DNALab (v2)

**Status:** Current (scenarios grounded in the live test suite)
**Reference:** HLD_DNALab v2.1 / DLD_DNALab v2.1 / LLD_DNALab v2.1
**Date:** 2026-06-12

Behaviour specification for DNALab's single public behaviour: **compose a VIN + triage
into a versioned, round-trippable `VehicleDNA`**. Scenarios are declarative; the truth is
`tests/` (`test_assembly.py`, `test_models.py`, `test_vehicledna_roundtrip.py`).

Ubiquitous language: *compose* = run `build_vehicle_dna()`; *envelope* = the five-key
`VehicleDNA`; *round-trip* = `from_json_payload(to_json_payload(x))`.

---

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

## Feature: Contract surface

```gherkin
Feature: The payload has exactly the five contract keys

  Scenario: Top-level keys are the §4.3 set
    Given a composed VehicleDNA
    When to_json_payload is inspected
    Then the keys are exactly {session_id, timestamp, schema_version, vin_dna, symptom_dna}

  Scenario: VinDNA carries the required key superset
    Given a composed VehicleDNA
    When the vin_dna payload is inspected
    Then it contains all required VinDNA keys (vin, make, model_year, ... confidence)

  Scenario: SymptomDNA carries exactly four keys
    Given a composed VehicleDNA
    When the symptom_dna payload is inspected
    Then the keys are exactly {tier_1_primary_symptom, tier_2_subfield_filter,
         environmental_conditions, free_text_notes}
```
*Maps to:* `test_assembly.py` (`test_contract_top_level_keys`, `test_vin_dna_keys_superset`,
`test_symptom_dna_keys_exact`).

---

## Feature: JSON round-trip

```gherkin
Feature: A VehicleDNA survives serialization unchanged

  Scenario: Round-trip preserves identity and both parts
    Given a composed VehicleDNA
    When it is serialised with to_json_payload and reloaded with from_json_payload
    Then session_id, timestamp, and schema_version are preserved
      And vin_dna.vin and symptom_dna.tier_1_primary_symptom are preserved
```
*Maps to:* `test_assembly.py::test_round_trip_json_payload`,
`test_vehicledna_roundtrip.py`.

---

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

## Feature: Isolation (CI-level behaviour)

```gherkin
Feature: DNALab imports only its two in-family producers

  Scenario: Only in-family imports exist
    Given the dnalab package
    When the import audit runs
    Then it imports vinlab and symptomlab and imports no comlab, gaslab, obdlab, or dtclab
```
*Maps to:* import-direction audit (`docs/adr/0002-dnalab-only-importer.md`).

---

## Traceability summary

| Behaviour area | Primary test module |
|----------------|---------------------|
| Composition happy path | `test_assembly.py` |
| Contract keys | `test_assembly.py` |
| Round-trip | `test_vehicledna_roundtrip.py`, `test_assembly.py` |
| Version guard | `test_models.py`, `test_assembly.py` |
| Fail-fast / propagation | `test_assembly.py` |
| Fixtures | `conftest.py` |
