
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: Deterministic registry triage with a confidence floor · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
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


## Graph relations (explicit)

**Feature: Deterministic registry triage with a confidence floor** DESCRIBES **COMLab BDD v1.0**
