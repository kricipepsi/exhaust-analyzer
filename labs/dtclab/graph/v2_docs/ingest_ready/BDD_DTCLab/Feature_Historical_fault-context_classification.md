
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Feature: Historical fault-context classification · Parent document: BDD_DTCLab.md
## Feature: Historical fault-context classification
*Backing tests: `tests/unit/test_historical_context_classifier.py`.*

```gherkin
Scenario: Cold start dominates idle and load context
  Given coolant_temp_c = 50, engine_rpm = 800, calculated_load_pct = 20
  When the historical context is classified
  Then the result is COLD_START_TRANSIT_FAULT
  And idle/load conditions are not evaluated

Scenario: Idle fault requires both low RPM and low load
  Given coolant_temp_c = 90, engine_rpm = 900, calculated_load_pct = 20
  When the historical context is classified
  Then the result is HISTORICAL_IDLE_FAULT

Scenario: The 60 degree boundary is exclusive
  Given coolant_temp_c = 60, engine_rpm = 2500, calculated_load_pct = 50
  When the historical context is classified
  Then the result is HISTORICAL_LOAD_FAULT
  And it is not COLD_START_TRANSIT_FAULT
```

---


## Graph relations (explicit)

**Feature: Historical fault-context classification** DESCRIBES **DTCLab BDD v1.0**
**test_historical_context_classifier.py** VERIFIES **Feature: Historical fault-context classification**
