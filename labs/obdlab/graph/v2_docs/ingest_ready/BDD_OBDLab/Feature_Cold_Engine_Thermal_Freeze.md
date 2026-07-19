> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: Cold-engine thermal freeze · Parent document: BDD_OBDLab.md

## Feature: Cold-engine thermal freeze

```gherkin
Feature: A cold engine freezes analytics but still emits a payload

  Scenario: Coolant below 75 °C overrides the bucket and freezes analytics
    Given an engine at 40 °C coolant
    When the translator runs
    Then rpm_state_bucket = COLD_OPEN_LOOP_INVALID
      And engine_warmed = false
      And normalized_obd_lambda = 1.0 (stoichiometric safe default)
      And total_trim_correction_delta = 0.0
      And ve_pct = 0.0 with ve_validity = UNKNOWN
      And the payload is still emitted (no exception)
```

### Entity: Cold-engine test mapping

- **Tests:** `integration/test_pipeline_smoke::test_smoke_cold_engine_none_dna`, `test_semantic_consistency_checker` (thermal gate)

## Graph relations (explicit)

**test_pipeline_smoke.py** VERIFIES **cold-engine thermal freeze** (test_smoke_cold_engine_none_dna)
**test_semantic_consistency_checker.py** VERIFIES **thermal gate** (ECT < 75 → COLD_OPEN_LOOP_INVALID)
**thermal freeze** GATED_BY **ECT < 75** (# wiki: §4.1)
**BDD_OBDLab v2.0** VERIFIES **cold-engine payload defaults** (λ=1.0, trim=0.0, ve=0.0)
