> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: Guarded perception channels (emitter-only) · Parent document: BDD_OBDLab.md

## Feature: Guarded perception channels (emitter-only)

```gherkin
Feature: Cross-lab fusion channels are emitted only when their inputs justify them

  Scenario: Lambda perception delta requires wideband and a commanded ratio
    Given upstream_o2_type = WIDEBAND_LINEAR and commanded_equivalence_ratio (PID 0x44) present
    When the translator runs
    Then lambda_perception_delta = normalized_obd_lambda − commanded ratio
      And the field is emitted for COMLab T-COMV2-ECU-FUSE-1, not judged here

  Scenario: Non-wideband configurations omit the perception delta
    Given upstream_o2_type = NARROWBAND_0_TO_1V
    When the translator runs
    Then lambda_perception_delta is null

  Scenario: MAF linearity needs both idle and stress bands
    Given DUAL_MAF_MAP_CROSSCHECK and a LinearityAccumulator
      And the stabilized-idle band then the stress-idle band are both observed
    When the translator runs on the stress sample
    Then w_theo and sensor_error_delta are emitted (for COMLab T-COMV2-MAF-LIN-1)
    But with only one band observed they remain null
```

### Entity: Guarded emitters test mapping

- **Tests:** `test_ecu_perception_delta`, `test_maf_linearity`, `test_sensor_signal_translator`

## Graph relations (explicit)

**test_ecu_perception_delta.py** VERIFIES **lambda_perception_delta** (emitter channel)
**test_maf_linearity.py** VERIFIES **w_theo / sensor_error_delta** (two-point MAF linearity)
**test_sensor_signal_translator.py** VERIFIES **guarded emitters** (integration)
**lambda_perception_delta** GATED_BY **WIDEBAND_LINEAR + commanded_equivalence_ratio** (PID 0x44)
**w_theo / sensor_error_delta** GATED_BY **DUAL_MAF_MAP_CROSSCHECK + LinearityAccumulator** (both idle + stress bands)
**COMLab T-COMV2-ECU-FUSE-1** CONSUMES **lambda_perception_delta** (S4 forward-reg)
**COMLab T-COMV2-MAF-LIN-1** CONSUMES **w_theo / sensor_error_delta** (S4 forward-reg)
**BDD_OBDLab v2.0** VERIFIES **guarded emitters pattern** (emitted only when guard satisfied)
