> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: Trim analytics precondition gate · Parent document: BDD_OBDLab.md

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

### Entity: Trim analytics gate test mapping

- **Tests:** `test_analytics_preconditions`

## Graph relations (explicit)

**test_analytics_preconditions.py** VERIFIES **trim analytics gate** (8-gate priority chain)
**AnalyticsPreconditions.evaluate** ENUMERATES **ENGINE_COLD, OPEN_LOOP, O2_FAULT_ACTIVE, CKP_CMP_FAULT_ACTIVE, CODES_RECENTLY_CLEARED, WOT_ACTIVE, DFCO_ACTIVE, VALID** (priority order)
**ECT_WARM_THRESHOLD = 70** VERIFIES **ENGINE_COLD gate** (# wiki: §9)
**WOT_THROTTLE_THRESHOLD = 90** VERIFIES **WOT_ACTIVE gate** (# wiki: §9)
**COMLab** CONSUMES **trim_analytics_gate** (suppress trim findings unless VALID)
**BDD_OBDLab v2.0** VERIFIES **trim analytics gate priority chain**
