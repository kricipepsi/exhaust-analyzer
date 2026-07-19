
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: Mechanical-wear family resolves to a leaf · Parent document: BDD_GASLab.md
## Feature: Mechanical-wear family resolves to a leaf
*Tests: `unit/test_resolution.py`*

```gherkin
Scenario: HC that drops sharply into high idle points to worn valve seals
  Given an idle reading with moderate HC
    And a high-idle reading where HC drops sharply and CO stays clean
  When the reading is classified with both readings
  Then chemical_state is WORN_VALVE_SEALS

Scenario: HC that climbs under load points to worn piston rings
  Given an idle reading with low HC
    And a high-idle reading where HC rises and CO climbs
    And a strongly negative fuel trim when trim is available
  When the reading is classified with both readings
  Then chemical_state is WORN_PISTON_RINGS

Scenario: A wear pattern with no matching leaf drops the whole family
  Given a co-surviving mechanical-wear family
    And no idle-to-high-idle pattern matches a specific leaf
  When resolution completes
  Then no WORN_* or POA_SIGNATURE candidate remains
```

---


## Graph relations (explicit)

**Feature: Mechanical-wear family resolves to a leaf** DESCRIBES **GASLab BDD v2.1**
**test_resolution.py** VERIFIES **mechanical-wear family** -- leaf routing, idle->2500 HC direction


