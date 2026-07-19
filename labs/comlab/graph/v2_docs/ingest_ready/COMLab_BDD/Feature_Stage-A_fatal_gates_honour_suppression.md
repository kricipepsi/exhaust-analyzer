
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: Stage-A fatal gates honour suppression · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
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


## Graph relations (explicit)

**Feature: Stage-A fatal gates honour suppression** DESCRIBES **COMLab BDD v1.0**
