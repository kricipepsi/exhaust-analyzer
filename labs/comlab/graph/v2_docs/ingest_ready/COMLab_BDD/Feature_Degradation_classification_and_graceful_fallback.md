
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: Degradation classification and graceful fallback · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
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


## Graph relations (explicit)

**Feature: Degradation classification and graceful fallback** DESCRIBES **COMLab BDD v1.0**
