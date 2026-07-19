# BDD — COMLab

**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-21
**Authored from:** `_skills/doc/BDD.md` (Gherkin Given/When/Then, declarative, one behaviour per scenario)
**Code baseline:** COMLab v2 as-built (`labs/comlab/comlab/`)

These are **executable specifications** for COMLab's observable behaviour at its
two public boundaries: `core/lab_pipeline_aggregator.LabPipelineAggregator.process()`
(the full pipeline) and `core/fault_atlas_router.FaultAtlasRouter.route()` (Stage
B→E). Each scenario is declarative — it states what the fusion spine does for a
given inbound request, never how. Every feature names the test module(s) that
exercise it, so the scenarios stay honest against `pytest`. Numeric values are
illustrative of the documented bands (see LLD / ADRs); they are not new thresholds.

**Scope reminder (ADR-0004):** petrol 1990–2010, Euro 1–5. Post-2010 Euro 6+
technology (SAI, GPF/DPF, LSPI) is out of scope — there are no scenarios for it
because there are no fields for it.

A shared vocabulary used throughout:

- **A request** = one `OrchestratorInboundRequest` (vehicle DNA + gas/OBD/DTC
  payloads + symptom DNA).
- **The verdict** = the `diagnostic_verdict` block of `OrchestratorFinalUIOutput`
  (fault id/name/family, confidence, remediation, siblings).
- **The directive** = the `LabRoutingDirective` from `symptom_router.route_symptom`.
- **A horizon** = `HORIZON_LEGACY` / `HORIZON_ADAPTIVE` / `HORIZON_MODERN`,
  pre-resolved by DNALab.

---

## Feature: Contract validation at the ingestion gate
*Tests: `unit/test_lab_pipeline_aggregator.py`, `unit/test_vocabulary_sae_iso_conformance.py`*

```gherkin
Scenario: A well-formed payload is accepted
  Given an inbound request that conforms to OrchestratorInboundRequest
  When the payload is validated
  Then validation passes and the pipeline proceeds to Stage A

Scenario: A malformed DTC string is rejected
  Given a request whose confirmed_dtcs contains "X1234"
  When the payload is validated
  Then validation fails with ERR-CONTRACT-001

Scenario: An air-metering strategy inconsistent with its sensors is rejected
  Given a request with air_metering_strategy DUAL_MAF_MAP_CROSSCHECK
    But has_map_sensor is false
  When the payload is validated
  Then validation fails with ERR-CONTRACT-002

Scenario: A downstream trim role without a downstream sensor is rejected
  Given a request whose downstream_trim_role is SECONDARY_FUEL_TRIM
    But downstream_o2_present is false
  When the payload is validated
  Then validation fails with ERR-CONTRACT-003
```

---

## Feature: Stage-A fatal gates honour suppression
*Tests: `unit/test_fatal_gate_wiring.py`, `unit/test_lab_pipeline_aggregator.py`*

```gherkin
Scenario: An invalid gas sample aborts the session
  Given a running-engine request whose gas sample_validity is INVALID
  When the fatal gates run
  Then the session aborts with ERR-ABORT-001
    And the output degradation_mode is FATAL_INCOMPLETE

Scenario: A borderline gas sample is allowed through
  Given a request whose gas sample_validity is BORDERLINE
  When the fatal gates run
  Then the gas-sample gate passes

Scenario: A cold engine aborts the session
  Given a request whose obd_live_data.engine_warmed is false
  When the fatal gates run
  Then the session aborts with ERR-ABORT-002

Scenario: An undecodable VIN aborts the session
  Given a request whose vin_confidence is NONE
  When the fatal gates run
  Then the session aborts with ERR-ABORT-004

Scenario: A non-start engine does not abort on missing gas data
  Given a request whose symptom engine_state is will_not_start
    And no valid gas sample is present
  When the fatal gates run
  Then the gas-sample gate is skipped (suppress_gaslab)
    And the session proceeds
```

---

## Feature: Symptom routing suppresses the right lab sections
*Tests: `unit/test_symptom_router.py`*

```gherkin
Scenario: A no-start engine suppresses gas, live PIDs, and monitors
  Given a symptom DNA with engine_state will_not_start
  When the symptom is routed
  Then suppress_gaslab, suppress_obd_live_pids, and suppress_mode06_ui are set
    And reasons include NON_STARTER_NO_EXHAUST

Scenario: A cranking engine suppresses live PIDs only
  Given a symptom DNA with engine_state cranking
  When the symptom is routed
  Then suppress_obd_live_pids is set
    And gas and monitor sections are not suppressed

Scenario: A cold-only complaint activates the cold-start hypothesis
  Given a symptom DNA with occurs_during cold_only
  When the symptom is routed
  Then cold_start_mode is set
    And reasons include COLD_START_HYPOTHESIS

Scenario: Unread symptom fields route nothing
  Given a symptom DNA carrying only tier_1 and free_text_notes
  When the symptom is routed
  Then no suppression flags are set
```

---

## Feature: Brettschneider chemistry overrules ECU perception
*Tests: `unit/test_perception_contradiction.py`, `integration/test_truth_perception.py`*

```gherkin
Scenario: A biased-lean sensor is surfaced against near-normal chemistry
  Given lambda_chem near 1.00
    And normalized_obd_lambda reading leaner than the era tolerance allows
  When perception contradiction is detected
  Then o2_sensor_bias_verdict is O2_SENSOR_BIASED_LOW
    And lambda_perception_delta carries the signed difference

Scenario: Agreement within tolerance reports no bias
  Given lambda_chem and normalized_obd_lambda within the era tolerance
  When perception contradiction is detected
  Then o2_sensor_bias_verdict is None

Scenario: A no-OBD session falls back to the measured analyser lambda
  Given no normalized_obd_lambda is present
    And the gas payload carries lambda_measured
  When the perception lambda is selected
  Then the measured analyser lambda is used

Scenario: The detector goes inert with no perception lambda at all
  Given neither normalized_obd_lambda nor lambda_measured is present
  When perception contradiction is detected
  Then no bias verdict is produced
```

---

## Feature: Deterministic registry triage with a confidence floor
*Tests: `unit/test_fault_atlas_router.py`, `unit/test_fault_atlas_router_registry_select.py`, `e2e/test_real_routing.py`*

```gherkin
Scenario: A rule not targeting the resolved horizon is pruned
  Given a registry rule whose target_horizons excludes HORIZON_LEGACY
    And a session resolved to HORIZON_LEGACY
  When the triage loop runs
  Then that rule never reaches chemistry matching

Scenario: The same request always produces the same verdict
  Given a fixed inbound request
  When the triage loop runs twice
  Then both runs select the same fault_id with the same confidence_score

Scenario: No rule clearing the confidence floor yields no fault
  Given a session where every candidate scores below 0.70
  When the triage loop runs
  Then the verdict is no_fault with severity OPTIMAL_HEALTH

Scenario: A POA chemistry state injects the POA routing tag
  Given a gas payload whose chemical_state is POA_SIGNATURE
  When the triage loop runs
  Then POA_HISTORY is appended to the working routing tags
```

---

## Feature: Catalyst-damage-imminent safety override
*Tests: `unit/test_fault_atlas_router.py`, `e2e/test_error_codes.py`*

```gherkin
Scenario: A flashing MIL with a misfire code forces a critical stop
  Given dtc_lab_output.mil_flashing is true
    And confirmed_dtcs contains a P030x misfire code
  When the catalyst-damage override is applied
  Then severity_level is forced to CRITICAL_IMMEDIATE_STOP

Scenario: A solid MIL with the same misfire code does not force a stop
  Given dtc_lab_output.mil_flashing is false
    And confirmed_dtcs contains a P030x misfire code
  When the catalyst-damage override is applied
  Then severity_level is left to the analytics ranking
```

---

## Feature: KG enrichment and registry consistency
*Tests: `unit/test_fault_atlas_kg.py`, `unit/test_kg_schema.py`, `e2e/test_kg_registry_consistency.py`*

```gherkin
Scenario: The winning fault is enriched from its KG node
  Given a winning fault_id present in the KG
  When the verdict is enriched
  Then fault_enrichment carries the component_group, impacted_subsystems,
       mechanical_failure_mode, and 1..8 ui_remediation_steps for that fault

Scenario: Every registry fault has a KG node and vice versa
  Given the loaded fault registry and the 13 per-family KG files
  When the consistency check runs
  Then every registry fault_id has exactly one KG node
    And every KG fault_id appears in the registry

Scenario: A duplicate fault_id across KG files fails at boot
  Given two KG files declaring the same fault_id
  When the KG is loaded
  Then loading fails before the process is ready to serve
```

---

## Feature: Differential siblings panel
*Tests: `unit/test_fault_atlas_router.py`*

```gherkin
Scenario: Runtime runner-ups and editor-curated siblings are merged
  Given the triage loop produced runner-up faults
    And the winning KG node lists editor-curated differential_siblings
  When the siblings are assembled
  Then both sources are unioned and deduplicated by fault_id
    And the total is capped at 5

Scenario: An editor-curated sibling that did not fire has no score
  Given an editor-curated sibling absent from this session's runner-ups
  When the siblings are assembled
  Then that sibling appears with confidence_score null
```

---

## Feature: Two-operating-point delta diagnosis
*Tests: `unit/test_delta_engine.py`, `e2e/test_delta_router_wiring.py`*

```gherkin
Scenario: A second operating point promotes the delta-matched family
  Given a request carrying a valid second_operating_point frame
  When the delta engine runs with delta evidence enabled
  Then a DeltaSignature is produced
    And Phase 5 ranks the delta-matched fault family above static signatures

Scenario: Without a second frame the path is single-point
  Given a request with no second_operating_point
  When the pipeline runs
  Then degradation_mode is SINGLE_POINT
    And the verdict matches the single-point path

Scenario: A MAP-only architecture abstains from a trim delta
  Given a second frame on a MAP_ONLY_SPEED_DENSITY vehicle
  When the architecture gate runs
  Then the trim-delta profile is not applied

Scenario: A delta frame measured at the wrong RPM bucket abstains
  Given a second frame whose rpm_state_bucket does not match the band under test
  When that band check runs
  Then it abstains rather than differencing across regimes
```

---

## Feature: Evidence gates suppress unreliable findings
*Tests: `unit/test_ve_evidence_gate.py`, `unit/test_fuel_system_gate.py`, `unit/test_ltft_cell_classification.py`*

```gherkin
Scenario: VE evidence is gated to valid cross-checks
  Given an OBD payload whose ve_validity is FAULT_MAF_CONTAMINATION
  When the VE evidence gate runs
  Then full VE evidence weight is withheld from the verdict

Scenario: Trim evidence is suppressed outside closed loop
  Given an OBD payload whose fuel_system_status is OL_FAULT
  When the fuel-system gate runs
  Then trim-based findings are suppressed

Scenario: Trim analytics blocked upstream are not used
  Given an OBD payload whose trim_analytics_gate is not VALID
  When the triage loop runs
  Then trim-derived findings do not contribute to the verdict
```

---

## Feature: ECU hardware digital-lie detection
*Tests: `unit/test_ecu_hardware_checker.py`*

```gherkin
Scenario: Railed sensors with broken bank symmetry flag an ECU hardware fault
  Given intake_air_temp_c railed to its floor
    And throttle_pos_pct railed to 100
    And trims railed beyond 25 percent with bank symmetry broken beyond 5 percent
  When the ECU hardware checker runs
  Then is_ecu_hardware_fault is true with confidence 0.80

Scenario: Plausible sensor values report no ECU hardware fault
  Given intake_air_temp_c and throttle_pos_pct within normal bands
  When the ECU hardware checker runs
  Then is_ecu_hardware_fault is false
```

---

## Feature: Degradation classification and graceful fallback
*Tests: `e2e/test_diagnostic_engine.py`, `e2e/test_pipeline_round_trip.py`, `regression/test_comlab_regression.py`*

```gherkin
Scenario: All four labs reporting cleanly is full fusion
  Given a request with clean gas, OBD, and DTC payloads at HIGH vin_confidence
  When the pipeline runs
  Then execution_meta.degradation_mode is FULL_FUSION
    And processing_confidence_rating is HIGH_ASSURANCE

Scenario: A legacy car without a scanner degrades to gas-dominant
  Given a legacy request with no OBD live data
  When the pipeline runs
  Then degradation_mode is GAS_DOMINANT
    And a verdict is still produced from chemistry

Scenario: The result always carries the routing directive and echo audit
  Given any successfully processed request
  When the final output is assembled
  Then execution_meta.lab_routing_directive is present with its reasons
    And user_input_echo_audit is present (a sentinel when none was supplied)
```

---

## References

- `COMLab_HLD.md` §4 (pipeline stages), `COMLab_LLD.md` §6–§7 (module contracts).
- `docs/adr/` — the decisions these behaviours implement (esp. ADR-0007, ADR-0009,
  ADR-0010, ADR-0011).
- `tests/` — the suites named under each feature are the executable counterpart.
