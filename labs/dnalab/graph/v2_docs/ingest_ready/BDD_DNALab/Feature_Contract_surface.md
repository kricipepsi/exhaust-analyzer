> **Context:** DNALab BDD_DNALab v2 (2026-06-12) · Module: DNALab · Section: Feature: · Parent document: BDD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

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

## Graph relations (explicit)

**VehicleDNA.to_json_payload()** VERIFIES **exactly five keys** (session_id, timestamp, schema_version, vin_dna, symptom_dna)
**vin_dna** VERIFIES **required key superset** (vin, make, model_year, ... confidence)
**symptom_dna** VERIFIES **exactly four keys** (tier_1_primary_symptom, tier_2_subfield_filter, environmental_conditions, free_text_notes)
**test_assembly.py** VERIFIES **test_contract_top_level_keys, test_vin_dna_keys_superset, test_symptom_dna_keys_exact**
