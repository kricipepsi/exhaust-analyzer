
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Feature: Cross-field coolant/fluid signatures (pipeline step 5b) · Parent document: BDD_DTCLab.md
## Feature: Cross-field coolant/fluid signatures (pipeline step 5b)
*Backing tests: `tests/integration/test_dtclab_pipeline.py`, `tests/regression/test_dtclab_regression.py`.*

```gherkin
Scenario: Thermostat code while in open-loop-fault flags coolant malfunction
  Given confirmed DTCs include "P0128"
  And the freeze frame fuel_system_status is OL_FAULT
  When the full pipeline runs
  Then routing_tags include COOLANT_SYSTEM_MALFUNCTION

Scenario: A misfire code while in closed loop flags a fluid-quench misfire
  Given confirmed DTCs include "P0301"
  And the freeze frame fuel_system_status is CL
  When the full pipeline runs
  Then routing_tags include CYLINDER_FLUID_MISFIRE

Scenario: The same misfire code in open loop does NOT flag fluid quench
  Given confirmed DTCs include "P0301"
  And the freeze frame fuel_system_status is OL
  When the full pipeline runs
  Then routing_tags do not include CYLINDER_FLUID_MISFIRE
```

---


## Graph relations (explicit)

**Feature: Cross-field coolant/fluid signatures (pipeline step 5b)** DESCRIBES **DTCLab BDD v1.0**
**test_dtclab_pipeline.py** VERIFIES **Feature: Cross-field coolant/fluid signatures (pipeline step 5b)**
