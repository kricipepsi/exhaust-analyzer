
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: The payload contract is always honoured · Parent document: BDD_GASLab.md
## Feature: The payload contract is always honoured
*Tests: `unit/test_process.py`, `unit/test_contracts.py`*

```gherkin
Scenario: Every diagnosis emits a complete, in-bounds payload
  Given any valid reading and DNA view
  When the diagnosis completes
  Then GasLabPayload carries chemical_state, the five gases, lambda_chem, and sample_validity
    And every numeric field is within its declared Pydantic range

Scenario: A directly-measured lambda is passed through when supplied
  Given a context carrying lambda_measured
  When the diagnosis completes
  Then the payload's lambda_measured equals the supplied value
  # consumer: COMLab perception-contradiction detector, no-OBD path (T-FX-7)

Scenario: No directly-measured lambda leaves the field null
  Given a context without lambda_measured
  When the diagnosis completes
  Then the payload's lambda_measured is null
```

---


## Graph relations (explicit)

**Feature: The payload contract is always honoured** DESCRIBES **GASLab BDD v2.1**
**test_process.py** VERIFIES **GasLabPayload** -- end-to-end round-trip, idle + dual-RPM
**test_contracts.py** VERIFIES **GasLabPayload** -- 9-field Pydantic ranges, lambda_measured optional


