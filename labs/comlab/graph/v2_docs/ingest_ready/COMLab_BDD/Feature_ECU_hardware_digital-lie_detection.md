
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: ECU hardware digital-lie detection · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
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


## Graph relations (explicit)

**Feature: ECU hardware digital-lie detection** DESCRIBES **COMLab BDD v1.0**
