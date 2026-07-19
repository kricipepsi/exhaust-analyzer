
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: Fuel-trim disambiguates an air-rich leak · Parent document: BDD_GASLab.md
## Feature: Fuel-trim disambiguates an air-rich leak
*Tests: `unit/test_rule_engine.py`, `unit/test_resolution.py`*

```gherkin
Scenario: A leak chemistry with strong positive trim is a real air leak
  Given a reading in the EXTERNAL_O2_SUSPECT band matching leak chemistry
    And a short-term fuel trim above 8%
  When the reading is classified
  Then chemical_state is EXHAUST_AIR_LEAK

Scenario: The same chemistry without compensating trim is treated as a bad sample
  Given a reading in the EXTERNAL_O2_SUSPECT band matching leak chemistry
    And a short-term fuel trim at or below 8%
  When the reading is classified
  Then chemical_state is SAMPLE_INVALID
```

---


## Graph relations (explicit)

**Feature: Fuel-trim disambiguates an air-rich leak** DESCRIBES **GASLab BDD v2.1**
**test_rule_engine.py** VERIFIES **fuel_trim disambiguation** -- EXTERNAL_O2_SUSPECT leak routing
**test_resolution.py** VERIFIES **fuel_trim disambiguation** -- leak vs SAMPLE_INVALID


