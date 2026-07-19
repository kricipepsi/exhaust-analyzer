
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: Brettschneider chemistry overrules ECU perception · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
## Feature: Brettschneider chemistry overrules ECU perception
*Tests: `unit/test_perception_contradiction.py`, `integration/test_truth_perception.py`*

```gherkin
Scenario: A biased-lean sensor is surfaced against near-normal chemistry
  Given lambda_chem near 1.00
    And normalized_obd_lambda reading leaner than the era tolerance allows
  When perception contradiction is detected
  Then o2_sensor_bias_verdict is O2_SENSOR_BIASED_LOW
    And lambda_perception_delta carries the signed difference

Scenario: Agreement within tolerance reports no bias
  Given lambda_chem and normalized_obd_lambda within the era tolerance
  When perception contradiction is detected
  Then o2_sensor_bias_verdict is None

Scenario: A no-OBD session falls back to the measured analyser lambda
  Given no normalized_obd_lambda is present
    And the gas payload carries lambda_measured
  When the perception lambda is selected
  Then the measured analyser lambda is used

Scenario: The detector goes inert with no perception lambda at all
  Given neither normalized_obd_lambda nor lambda_measured is present
  When perception contradiction is detected
  Then no bias verdict is produced
```

---


## Graph relations (explicit)

**Feature: Brettschneider chemistry overrules ECU perception** DESCRIBES **COMLab BDD v1.0**
