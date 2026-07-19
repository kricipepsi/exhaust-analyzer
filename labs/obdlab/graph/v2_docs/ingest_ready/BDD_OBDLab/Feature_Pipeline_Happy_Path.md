> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: Pipeline happy path (warm idle) · Parent document: BDD_OBDLab.md

## Feature: Pipeline happy path (warm idle)

```gherkin
Feature: Warm-idle translation produces a complete, round-trippable payload

  Scenario: Minimal valid warm-idle input with no DNA view
    Given a warm engine at 800 RPM and 92 °C coolant
      And closed-loop fuel status and a 0.45 V narrowband O2 reading
      And no DNA view is supplied
    When the translator runs
    Then the payload reports engine_warmed = true
      And rpm_state_bucket = STABILIZED_IDLE
      And the payload serialises to JSON and reloads unchanged
```

### Entity: Happy path test mapping

- **Tests:** `integration/test_pipeline_smoke::test_smoke_minimal_input_none_dna`, `test_sensor_signal_translator`

## Graph relations (explicit)

**test_pipeline_smoke.py** VERIFIES **warm-idle happy path** (test_smoke_minimal_input_none_dna)
**test_sensor_signal_translator.py** VERIFIES **SensorSignalTranslator.translate** (unit + integration)
**BDD_OBDLab v2.0** VERIFIES **OBDLivePayload** (warm-idle scenario)
