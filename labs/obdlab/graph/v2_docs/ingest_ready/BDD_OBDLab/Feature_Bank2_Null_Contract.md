> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: Bank-2 null contract · Parent document: BDD_OBDLab.md

## Feature: Bank-2 null contract

```gherkin
Feature: Absent banks are null, present banks are aggregated

  Scenario: Single-bank engine must leave bank-2 trims null
    Given number_of_banks = 1
      And a non-null shrtft2 is supplied
    When the translator runs
    Then a PIDValidationError is raised (SEMANTIC_CONTRACT violation)

  Scenario: Two-bank V-engine aggregates both banks
    Given number_of_banks = 2 with bank-1 trims (−3, −5) and bank-2 trims (−8, −12)
    When the translator runs
    Then total_trim_correction_delta = −8.0
      And total_trim_correction_delta_b2 = −20.0
      And per_bank_trim_delta = 12.0 (B1 − B2)

  Scenario: Two-bank engine missing a bank-2 value is rejected
    Given number_of_banks = 2 and longft2 is null
    When the translator runs
    Then a PIDValidationError is raised
```

### Entity: Bank-2 contract test mapping

- **Tests:** `integration/test_pipeline_smoke::test_smoke_2_bank_v_engine`, `test_trim_vector_aggregator`, `test_bank_asym`

## Graph relations (explicit)

**test_pipeline_smoke.py** VERIFIES **2-bank V-engine aggregation** (test_smoke_2_bank_v_engine)
**test_trim_vector_aggregator.py** VERIFIES **TrimVectorAggregator** (bank-2 contract)
**test_bank_asym.py** VERIFIES **per_bank_trim_delta** (bank asymmetry channel)
**_enforce_bank2_contract** VERIFIES **number_of_banks==1 → shrtft2/longft2 must be None** (SEMANTIC_CONTRACT §4.4)
**TrimVectorAggregator.aggregate** VERIFIES **bank1 + bank2 aggregation** (per_bank_trim_delta = B1 − B2)
**BDD_OBDLab v2.0** VERIFIES **bank-2 null contract behaviour**
