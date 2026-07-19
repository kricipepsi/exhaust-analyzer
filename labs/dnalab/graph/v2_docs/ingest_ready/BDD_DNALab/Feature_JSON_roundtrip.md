> **Context:** DNALab BDD_DNALab v2 (2026-06-12) · Module: DNALab · Section: Feature: · Parent document: BDD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

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

## Graph relations (explicit)

**VehicleDNA** VERIFIES **round-trip fidelity** (from_json_payload(to_json_payload(x)) preserves identity)
**test_assembly.py::test_round_trip_json_payload** VERIFIES **JSON round-trip**
**test_vehicledna_roundtrip.py** VERIFIES **dedicated round-trip suite**
