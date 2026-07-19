
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: Two-operating-point delta diagnosis · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
## Feature: Two-operating-point delta diagnosis
*Tests: `unit/test_delta_engine.py`, `e2e/test_delta_router_wiring.py`*

```gherkin
Scenario: A second operating point promotes the delta-matched family
  Given a request carrying a valid second_operating_point frame
  When the delta engine runs with delta evidence enabled
  Then a DeltaSignature is produced
    And Phase 5 ranks the delta-matched fault family above static signatures

Scenario: Without a second frame the path is single-point
  Given a request with no second_operating_point
  When the pipeline runs
  Then degradation_mode is SINGLE_POINT
    And the verdict matches the single-point path

Scenario: A MAP-only architecture abstains from a trim delta
  Given a second frame on a MAP_ONLY_SPEED_DENSITY vehicle
  When the architecture gate runs
  Then the trim-delta profile is not applied

Scenario: A delta frame measured at the wrong RPM bucket abstains
  Given a second frame whose rpm_state_bucket does not match the band under test
  When that band check runs
  Then it abstains rather than differencing across regimes
```

---


## Graph relations (explicit)

**Feature: Two-operating-point delta diagnosis** DESCRIBES **COMLab BDD v1.0**
