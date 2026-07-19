> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: O2 normalisation · Parent document: BDD_OBDLab.md

## Feature: O2 normalisation

```gherkin
Feature: O2 sensor input becomes one unified lambda plus a failure mode

  Scenario Outline: Narrowband voltage maps to a 3-zone lambda
    Given upstream_o2_type = NARROWBAND_0_TO_1V and pid_oxygen_sensor_volts = <volts>
    When O2 is normalised
    Then normalized_obd_lambda = <lambda> and o2_failure_mode = NO_FAULT

    Examples:
      | volts | lambda |
      | 0.30  | 1.05   |
      | 0.45  | 1.00   |
      | 0.70  | 0.95   |

  Scenario: Below-range narrowband voltage is a stuck-lean fault
    Given pid_oxygen_sensor_volts = 0.05 (below 0.10)
    When O2 is normalised
    Then mode = O2_CHANNEL_FAULT with lambda clamped to 1.05 and o2_failure_mode = STUCK_LEAN

  Scenario: Above-range narrowband voltage is a stuck-rich fault
    Given pid_oxygen_sensor_volts = 0.95 (above 0.90)
    When O2 is normalised
    Then mode = O2_CHANNEL_FAULT with lambda clamped to 0.95 and o2_failure_mode = STUCK_RICH

  Scenario: Wideband lambda passes straight through
    Given upstream_o2_type = WIDEBAND_LINEAR and pid_wideband_equivalence_ratio = 0.98
    When O2 is normalised
    Then normalized_obd_lambda = 0.98 and mode = WIDEBAND_PASSTHROUGH

  Scenario: Persistent wideband offset under stable conditions flags a candidate
    Given a warm, closed-loop, non-WOT, non-DFCO engine
      And a wideband ratio more than 0.05 away from 1.0
    When O2 is normalised
    Then o2_failure_mode = WIDEBAND_OFFSET_CANDIDATE (proposal EP-OBD-17, emitter-only)
```

### Entity: O2 normalisation test mapping

- **Tests:** `test_o2_normalizer`, `integration/test_pipeline_smoke::test_smoke_stress_idle_wideband`

## Graph relations (explicit)

**test_o2_normalizer.py** VERIFIES **O2 normalisation** (all scenarios + boundary ownership)
**test_pipeline_smoke.py** VERIFIES **wideband stress idle** (test_smoke_stress_idle_wideband)
**O2Normalizer.normalize** VERIFIES **3-zone narrowband mapping** (0.10→1.05 LEAN, 0.41→1.00 STOICH, 0.51→0.95 RICH)
**O2Normalizer.normalize** VERIFIES **STUCK_LEAN** (v < 0.10, λ clamped 1.05)
**O2Normalizer.normalize** VERIFIES **STUCK_RICH** (v > 0.90, λ clamped 0.95)
**O2Normalizer.normalize** VERIFIES **WIDEBAND_PASSTHROUGH** (direct ratio, 0.7–1.3)
**O2Normalizer.normalize** VERIFIES **WIDEBAND_OFFSET_CANDIDATE** (warm+CL+not WOT+not DFCO, |λ−1.0| > 0.05, proposal EP-OBD-17)
**BDD_OBDLab v2.0** VERIFIES **O2FailureMode taxonomy** (4 members)
