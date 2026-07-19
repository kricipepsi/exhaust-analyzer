
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: DNA gates suppress impossible faults · Parent document: BDD_GASLab.md
## Feature: DNA gates suppress impossible faults
*Tests: `unit/test_rule_engine.py`, `unit/test_resolution.py`, `unit/test_ontology.py`*

```gherkin
Scenario: A catalyst fault is impossible on a catalyst-free vehicle
  Given a reading whose chemistry matches a catalyst fault
    And a DNA view where has_catalyst is false
  When the reading is classified
  Then no CATALYST_* signature survives resolution

Scenario: A GDI fault is impossible on a port-injected vehicle
  Given a reading whose chemistry matches a GDI fault
    And a DNA view where fuel_delivery_type is not GDI
  When the reading is classified
  Then no GDI_* signature survives resolution

Scenario: An EGR fault is impossible on a vehicle without EGR
  Given a reading whose chemistry matches an EGR fault
    And a DNA view where egr_equipped is false
  When the reading is classified
  Then no EGR_STUCK_* signature survives resolution
```

---


## Graph relations (explicit)

**Feature: DNA gates suppress impossible faults** DESCRIBES **GASLab BDD v2.1**
**test_rule_engine.py** VERIFIES **DNA gates** -- catalyst/GDI/EGR suppression
**test_resolution.py** VERIFIES **DNA gates** -- strict gate enforcement
**test_ontology.py** VERIFIES **DNA gates** -- 6 DNA-gated entries


