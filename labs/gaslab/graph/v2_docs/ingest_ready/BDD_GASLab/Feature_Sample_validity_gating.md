
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: Sample validity gating · Parent document: BDD_GASLab.md
## Feature: Sample validity gating
*Tests: `unit/test_validity_gates.py`, `unit/test_rule_engine.py`*

```gherkin
Scenario: A clean idle sample is accepted
  Given a reading whose CO + CO2 + O2 sums to between 14 and 16
    And CO + CO2 is above the 6% dilution floor
  When the reading is classified
  Then sample_validity is VALID
    And classification proceeds to fault matching

Scenario: A diluted or contaminated sample halts the diagnosis
  Given a reading whose CO + CO2 + O2 is below 14 or above 18
  When the reading is classified
  Then chemical_state is SAMPLE_INVALID
    And sample_validity is INVALID

Scenario: An air-rich sample is flagged but not rejected
  Given a reading whose CO + CO2 + O2 sums to between 16 and 18
  When the reading is classified
  Then sample_validity is EXTERNAL_O2_SUSPECT
    And the diagnosis continues with that warning

Scenario: A sample that passes the triangle but fails dilution is rejected
  Given a reading inside the triangle band
    But CO + CO2 is at or below 6%
  When the reading is classified
  Then sample_validity is INVALID
```

---


## Graph relations (explicit)

**Feature: Sample validity gating** DESCRIBES **GASLab BDD v2.1**
**test_validity_gates.py** VERIFIES **SampleValidity gating** -- triangle + dilution gate scenarios
**test_rule_engine.py** VERIFIES **SampleValidity gating** -- SAMPLE_INVALID halt path


