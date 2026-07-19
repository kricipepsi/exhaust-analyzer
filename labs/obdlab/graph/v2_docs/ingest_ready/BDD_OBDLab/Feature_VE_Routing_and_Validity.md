> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: VE routing and validity · Parent document: BDD_OBDLab.md

## Feature: VE routing and validity

```gherkin
Feature: VE confidence depends on the air-metering hardware

  Scenario: Dual MAF+MAP yields a classified validity
    Given air_metering_strategy = DUAL_MAF_MAP_CROSSCHECK with both sensors present
    When VE is computed
    Then maf_status = REAL_SENSOR_FEED and map_status = REAL_SENSOR_FEED
      And ve_validity is one of {VALID, FAULT_VE_IDLE_COLLAPSE, FAULT_MAF_CONTAMINATION, FAULT_VE_SENSOR_SKEW}

  Scenario: MAP-only emulation cannot be cross-checked
    Given air_metering_strategy = MAP_ONLY_SPEED_DENSITY
    When VE is computed
    Then maf_status = VIRTUAL_EMULATION and ve_validity = UNKNOWN

  Scenario: NA engine over-reading VE at idle flags sensor skew
    Given a naturally-aspirated engine at STABILIZED_IDLE with VE above 90%
    When VE is classified
    Then ve_validity = FAULT_VE_SENSOR_SKEW

  Scenario: Missing displacement degrades VE without crashing
    Given no DNA view (engine_displacement_liters is unknown)
    When VE is computed
    Then ve_pct carries the 0.0 sentinel and ve_validity = UNKNOWN
```

### Entity: VE routing test mapping

- **Tests:** `test_ve_engine`

## Graph relations (explicit)

**test_ve_engine.py** VERIFIES **VE routing and validity** (all scenarios)
**DUAL_MAF_MAP_CROSSCHECK** VERIFIES **VEValidity classified** (VALID or fault mode)
**MAP_ONLY_SPEED_DENSITY** VERIFIES **VEValidity.UNKNOWN** (no cross-check)
**FAULT_VE_SENSOR_SKEW** VERIFIES **NA engine VE > 90% at idle** (supersedes Physics Gate 3)
**degraded mode** VERIFIES **ve_pct=0.0, VEValidity.UNKNOWN** (no crash on missing displacement)
**BDD_OBDLab v2.0** VERIFIES **VE evidence-gating behaviour**
