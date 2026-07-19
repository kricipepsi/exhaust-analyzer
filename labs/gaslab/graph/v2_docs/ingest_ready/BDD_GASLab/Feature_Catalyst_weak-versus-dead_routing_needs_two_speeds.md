
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: Catalyst weak-versus-dead routing needs two speeds · Parent document: BDD_GASLab.md
## Feature: Catalyst weak-versus-dead routing needs two speeds
*Tests: `unit/test_resolution.py`*

```gherkin
Scenario: A catalyst weak at idle but working at high idle is not lighting off
  Given a catalyst-equipped vehicle with healthy fuel control at both speeds
    And an idle reading showing weak catalyst chemistry
    And a high-idle reading showing a working catalyst
  When the reading is classified with both readings
  Then chemical_state is CATALYST_NOT_LIGHTING_OFF

Scenario: A catalyst degraded at both speeds is overwhelmed
  Given a catalyst-equipped vehicle with healthy fuel control at both speeds
    And both readings show dead-catalyst chemistry
  When the reading is classified with both readings
  Then chemical_state is CATALYST_OVERWHELMED

Scenario: Bad fuel control rejects any catalyst verdict
  Given a catalyst-equipped vehicle whose lambda is outside 0.98 to 1.02 at either speed
  When the reading is classified with both readings
  Then no CATALYST_* signature survives
```

---


## Graph relations (explicit)

**Feature: Catalyst weak-versus-dead routing needs two speeds** DESCRIBES **GASLab BDD v2.1**
**test_resolution.py** VERIFIES **catalyst dual-idle** -- weak-vs-dead, fuel-control gate


