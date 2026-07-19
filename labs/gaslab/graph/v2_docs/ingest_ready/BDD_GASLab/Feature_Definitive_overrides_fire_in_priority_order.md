
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: Definitive overrides fire in priority order · Parent document: BDD_GASLab.md
## Feature: Definitive overrides fire in priority order
*Tests: `unit/test_rule_engine.py`*

```gherkin
Scenario: Combustion gases in the coolant are caught only with the block test
  Given a reading with suppressed CO2 and elevated HC
    And the technician has confirmed a positive block test
  When the reading is classified
  Then chemical_state is COOLANT_LEAK_INTERNAL

Scenario: The same chemistry without the block test does not claim a coolant leak
  Given a reading with suppressed CO2 and elevated HC
    And no block test has been performed
  When the reading is classified
  Then chemical_state is not COOLANT_LEAK_INTERNAL

Scenario: An ignition misfire is confirmed by the oxygen spike
  Given a reading with very high HC, high O2, and suppressed NOx
    And the O2 spike is consistent with at least one dropped cylinder for this cylinder count
  When the reading is classified
  Then chemical_state is IGNITION_MISFIRE

Scenario: A collision pattern with low HC routes to an air leak
  Given a reading where both CO and O2 are elevated
    And the triangle sum is above 16
    And HC is normal
  When the reading is classified
  Then chemical_state is EXHAUST_AIR_LEAK
    And sample_validity is EXTERNAL_O2_SUSPECT

Scenario: A collision pattern with high HC stays a rich misfire
  Given a reading where both CO and O2 are elevated
    And HC is above the normal ceiling
  When the reading is classified
  Then chemical_state is RICH_MISFIRE
```

---


## Graph relations (explicit)

**Feature: Definitive overrides fire in priority order** DESCRIBES **GASLab BDD v2.1**
**test_rule_engine.py** VERIFIES **definitive overrides** -- coolant, masking, collision priority order


