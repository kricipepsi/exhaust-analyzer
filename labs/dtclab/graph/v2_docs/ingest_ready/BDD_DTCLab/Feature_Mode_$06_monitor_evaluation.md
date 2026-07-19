
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Feature: Mode $06 monitor evaluation · Parent document: BDD_DTCLab.md
## Feature: Mode $06 monitor evaluation
*Backing tests: `tests/unit/test_mode06_evaluator.py`.*

```gherkin
Scenario Outline: Margin is classified into the tri-state
  Given a Mode $06 margin of <margin>
  When the monitor is evaluated
  Then its state is <state>

  Examples:
    | margin | state                  |
    | -3.0   | CRITICAL_FAIL          |
    | 0.0    | CRITICAL_FAIL          |  # boundary owned by fail side
    | 8.0    | PENDING_FAIL_MARGINAL  |
    | 15.0   | PENDING_FAIL_MARGINAL  |  # inclusive upper
    | 16.0   | PASSED                 |

Scenario: A known MID resolves its target component
  Given the monitor key "MID_21_TID_81"
  When the monitor is evaluated against the hex dictionary
  Then the target_component is "Catalyst OSC Bank 1"

Scenario: An unknown MID resolves to UNKNOWN, not an error
  Given the monitor key "MID_FF_TID_01"
  When the monitor is evaluated
  Then the target_component is "UNKNOWN"

Scenario: A malformed monitor key is rejected
  Given the monitor key "MID_A2"
  When the monitor is evaluated
  Then a ValueError naming the MID_<HEX>_TID_<HEX> form is raised
```

---


## Graph relations (explicit)

**Feature: Mode $06 monitor evaluation** DESCRIBES **DTCLab BDD v1.0**
**test_mode06_evaluator.py** VERIFIES **Feature: Mode $06 monitor evaluation**
