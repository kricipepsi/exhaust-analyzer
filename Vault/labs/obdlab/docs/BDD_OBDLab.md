# BDD — OBDLab (v2)

**Status:** Current (scenarios grounded in the live test suite)
**Reference:** HLD_OBDLab v2.0 / DLD_OBDLab v2.0 / LLD_OBDLab v2.0
**Date:** 2026-06-10

Behaviour specification for OBDLab's single public behaviour: **translate a raw
OBD-II PID dict into a typed `OBDLivePayload`**. Scenarios are declarative
(business/diagnostic focus) and map to existing tests; the mapping column names
the test module that exercises each. These are executable-spec intent, not a
re-derivation of the code — the truth is the test suite.

Ubiquitous language: *translate* = run the pipeline; *frozen* = analytics
suppressed by the cold/thermal gate; *emitter-only* = OBDLab outputs a channel
but never a verdict.

---

## Feature: Pipeline happy path (warm idle)

```gherkin
Feature: Warm-idle translation produces a complete, round-trippable payload

  Scenario: Minimal valid warm-idle input with no DNA view
    Given a warm engine at 800 RPM and 92 °C coolant
      And closed-loop fuel status and a 0.45 V narrowband O2 reading
      And no DNA view is supplied
    When the translator runs
    Then the payload reports engine_warmed = true
      And rpm_state_bucket = STABILIZED_IDLE
      And the payload serialises to JSON and reloads unchanged
```
*Maps to:* `integration/test_pipeline_smoke::test_smoke_minimal_input_none_dna`,
`test_sensor_signal_translator`.

---

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
*Maps to:* `integration/test_pipeline_smoke::test_smoke_cold_engine_none_dna`,
`test_semantic_consistency_checker` (thermal gate).

---

## Feature: PID validation and bounds

```gherkin
Feature: Out-of-range PIDs are rejected before any analytics

  Scenario: Engine RPM above the static ceiling
    Given engine_rpm = 9000 (ceiling is 8000)
    When the translator runs
    Then a PIDValidationError is raised

  Scenario: Alternate-unit input is converted to canonical form
    Given coolant_temp_f is supplied and coolant_temp_c is absent
    When the translator runs
    Then the value is converted with (F − 32) × 5/9 before bounds checking

  Scenario: Canonical key wins over an alternate unit
    Given both coolant_temp_c and coolant_temp_f are present
    When the translator runs
    Then coolant_temp_c is used and coolant_temp_f is dropped
```
*Maps to:* `integration/test_pipeline_smoke::test_smoke_bounds_violation`,
`test_pid_ingestion_validator`.

---

## Feature: DNA-relative RPM gate (three-branch confidence)

```gherkin
Feature: The RPM ceiling tightens with VIN-decode confidence

  Scenario: HIGH confidence enforces the DNA rated-RPM ceiling
    Given confidence = HIGH and rated_rpm = 6500
      And engine_rpm exceeds rated_rpm × 1.05
    When the translator runs
    Then a PIDValidationError is raised

  Scenario: PARTIAL confidence logs and falls back to static bounds
    Given confidence = PARTIAL
    When the translator runs
    Then the DNA-RPM check is downgraded and only the static 0–8000 bound applies

  Scenario: NONE confidence (or no DNA view) uses static bounds only
    Given confidence = NONE
    When the translator runs
    Then no DNA-relative RPM check is applied
```
*Maps to:* `test_pid_ingestion_validator` (DNA-RPM three-branch).

---

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
*Maps to:* `integration/test_pipeline_smoke::test_smoke_2_bank_v_engine`,
`test_trim_vector_aggregator`, `test_bank_asym`.

---

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
*Maps to:* `test_ve_engine`.

---

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
*Maps to:* `test_o2_normalizer`,
`integration/test_pipeline_smoke::test_smoke_stress_idle_wideband`.

---

## Feature: Trim analytics precondition gate

```gherkin
Feature: Trim trustworthiness is classified, never silently suppressed

  Scenario Outline: The first failing precondition wins (priority order)
    Given <condition>
    When the analytics preconditions are evaluated
    Then trim_analytics_gate = <gate>

    Examples:
      | condition                                   | gate                   |
      | coolant_temp_c below 70                     | ENGINE_COLD            |
      | fuel_system_status is not CL                | OPEN_LOOP              |
      | an active DTC in P0130–P0161                | O2_FAULT_ACTIVE        |
      | an active P0335 or P0340                    | CKP_CMP_FAULT_ACTIVE   |
      | fewer than 1 drive cycle since codes cleared| CODES_RECENTLY_CLEARED |
      | throttle at or above 90%                    | WOT_ACTIVE             |
      | decel fuel cut-off active                   | DFCO_ACTIVE            |
      | all preconditions satisfied                 | VALID                  |
```
*Maps to:* `test_analytics_preconditions`.

---

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
*Maps to:* `test_ecu_perception_delta`, `test_maf_linearity`,
`test_sensor_signal_translator`.

---

## Feature: Optional ferried channels validate strictly

```gherkin
Feature: Optional dict channels are validated or passed through as null

  Scenario: Per-cylinder misfire counts must be 1-indexed, non-negative
    Given per_cylinder_misfire_counts with a cylinder index of 0
    When the translator runs
    Then a PIDValidationError is raised

  Scenario: LTFT cell vector values must lie within ±127
    Given ltft_cell_vector with a cell value of 200
    When the translator runs
    Then a PIDValidationError is raised

  Scenario: Absent optional channels are emitted as null
    Given neither per_cylinder_misfire_counts nor ltft_cell_vector is supplied
    When the translator runs
    Then both fields are null in the payload
```
*Maps to:* `test_pid_ingestion_validator`.

---

## Feature: Isolation and vocabulary guards (CI-level behaviour)

```gherkin
Feature: OBDLab stays an isolated, drift-free codebase

  Scenario: No cross-lab Python imports exist
    Given the obdlab package
    When the import-isolation audit runs
    Then there are zero imports from gaslab, dtclab, comlab, dnalab, or vinlab

  Scenario: The forbidden HIGH_IDLE_LOAD token is absent
    Given the obdlab codebase
    When the vocabulary scan runs
    Then HIGH_IDLE_LOAD appears nowhere (superseded by REGULATORY_HIGH_IDLE / STRESS_IDLE)
```
*Maps to:* `test_dna_view` (import isolation), `test_vocabulary` (token scan).

---

## Traceability summary

| Behaviour area | Primary test module(s) |
|----------------|------------------------|
| End-to-end pipeline | `integration/test_pipeline_smoke`, `test_sensor_signal_translator` |
| PID validation / bounds / units | `test_pid_ingestion_validator`, `test_sensor_bounds` |
| Bucketing | `test_state*`, smoke |
| Semantic gates / thermal freeze | `test_semantic_consistency_checker` |
| VE routing + validity | `test_ve_engine` |
| O2 normalisation | `test_o2_normalizer` |
| Trim aggregation / bank asymmetry | `test_trim_vector_aggregator`, `test_bank_asym` |
| Analytics gate | `test_analytics_preconditions` |
| Perception delta / MAF linearity | `test_ecu_perception_delta`, `test_maf_linearity` |
| Schema contracts | `test_payload`, `test_dna_view`, `test_vocabulary` |
| Regression + generative | `test_obdlab_regression`, generative suite |
