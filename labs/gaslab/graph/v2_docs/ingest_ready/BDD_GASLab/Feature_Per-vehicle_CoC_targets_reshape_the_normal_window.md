
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: Per-vehicle CoC targets reshape the normal window · Parent document: BDD_GASLab.md
## Feature: Per-vehicle CoC targets reshape the normal window
*Tests: `unit/test_rule_engine.py`, `unit/test_dna_view.py`*

```gherkin
Scenario: A certified lambda target tightens the normal band
  Given a DNA view carrying target_lambda_v112
  When NORMAL_OPERATION bounds are evaluated
  Then the lambda window is centred on v112 plus or minus 0.005
    And it is clamped within 0.85 and 1.15

Scenario: A per-vehicle idle CO ceiling overrides the Euro default
  Given a DNA view carrying co_low_idle
  When NORMAL_OPERATION bounds are evaluated
  Then the CO ceiling uses the per-vehicle value rather than the Euro-scaled default

Scenario: A wideband upstream sensor recalibrates the O2-bias signatures
  Given a DNA view whose upstream_o2_type contains "wideband"
  When O2_SENSOR_BIASED_LOW or _HIGH bounds are evaluated
  Then their CO and lambda windows use the wideband calibration
```

---


## Graph relations (explicit)

**Feature: Per-vehicle CoC targets reshape the normal window** DESCRIBES **GASLab BDD v2.1**
**test_rule_engine.py** VERIFIES **CoC targets** -- target_lambda_v112 window, CO ceiling override
**test_dna_view.py** VERIFIES **DNA view** -- 13-field validation, optional field handling


