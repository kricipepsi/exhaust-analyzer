
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: RPM-differential separation of the cam-timing family · Parent document: BDD_GASLab.md
## Feature: RPM-differential separation of the cam-timing family
*Tests: `unit/test_resolution.py`, `unit/test_t_p8_7_hc_discriminator.py`, `unit/test_rule_engine_reachability.py`*

```gherkin
Scenario: A retarded-cam MAF lean persists at high idle
  Given a lean idle reading matching the cam-MAF pattern
    And a high-idle reading where the lean condition persists
  When the reading is classified with both readings
  Then chemical_state is CAM_TIMING_RETARDED_MAF

Scenario: A vacuum lean that normalises at high idle is not cam timing
  Given a lean idle reading
    And a high-idle reading where lambda normalises toward 1.0 and O2 falls below 1%
  When the reading is classified with both readings
  Then chemical_state is LEAN_MIXTURE
    And CAM_TIMING_RETARDED_MAF does not survive

Scenario: An advanced cam shows rising NOx and falling HC into high idle
  Given a rough idle reading with a mild-lean lambda offset
    And a high-idle reading where NOx rises while HC and CO fall
  When the reading is classified with both readings
  Then chemical_state is CAM_TIMING_ADVANCED

Scenario: A retarded-cam MAP rich condition partially normalises at high idle
  Given a rich idle reading matching the Speed-Density over-fuel pattern
    And a high-idle reading where lambda rises toward 1.0 and CO falls
  When the reading is classified with both readings
  Then chemical_state is CAM_TIMING_RETARDED_MAP

Scenario: An over-advanced ignition shows a clean idle with a NOx-only spike
  Given a clean idle reading
    And a high-idle reading whose only abnormality is a very high NOx spike
  When the reading is classified with both readings
  Then TIMING_OVER_ADVANCED is among the survivors

Scenario: A confirmed cam timing prunes generic low-HC misfire noise
  Given a confirmed cam-timing survivor
    And a co-surviving generic misfire candidate whose HC is below the misfire floor
  When resolution completes
  Then the generic misfire candidate is dropped as overlap noise
```

---


## Graph relations (explicit)

**Feature: RPM-differential separation of the cam-timing family** DESCRIBES **GASLab BDD v2.1**
**test_resolution.py** VERIFIES **RPM-differential separation** -- cam timing, lean-vs-cam, over-advance
**test_t_p8_7_hc_discriminator.py** VERIFIES **HC discriminator** -- timing/misfire family
**test_rule_engine_reachability.py** VERIFIES **34-signature reachability** -- all states reachable


