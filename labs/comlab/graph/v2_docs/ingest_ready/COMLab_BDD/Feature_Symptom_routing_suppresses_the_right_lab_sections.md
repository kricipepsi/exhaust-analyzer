
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: Symptom routing suppresses the right lab sections · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
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


## Graph relations (explicit)

**Feature: Symptom routing suppresses the right lab sections** DESCRIBES **COMLab BDD v1.0**
