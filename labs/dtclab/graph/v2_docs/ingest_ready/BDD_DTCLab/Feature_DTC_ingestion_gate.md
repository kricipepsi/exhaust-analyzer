
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Feature: DTC ingestion gate · Parent document: BDD_DTCLab.md
## Feature: DTC ingestion gate
*Backing tests: `tests/unit/test_dtc_ingestion_gate.py`.*

```gherkin
Scenario: A well-formed confirmed DTC list passes through unchanged
  Given a Mode "$03" list ["P0171", "P0300", "U0100"]
  When the ingestion gate validates the list for mode "$03"
  Then the same list is returned unchanged

Scenario: The first malformed code fails fast
  Given a Mode "$03" list ["P0171", "p0300", "P0420"]
  When the ingestion gate validates the list
  Then a DTCFormatError is raised for "p0300"
  And no later code in the list is evaluated

Scenario: An unrecognised OBD mode is rejected before any code is checked
  Given any DTC list
  When the gate is asked to validate it for mode "$05"
  Then a ValueError is raised naming the three valid modes "$03", "$07", "$0A"

Scenario Outline: Canonical regex accepts and rejects exact forms
  Given the code "<code>"
  When it is validated for mode "$03"
  Then it is <verdict>

  Examples:
    | code    | verdict   |
    | P0171   | accepted  |
    | U0100   | accepted  |
    | p0171   | rejected  |  # lowercase system byte
    | P017    | rejected  |  # too short
    | P01711  | rejected  |  # too long
    | X0171   | rejected  |  # invalid system byte
    | P0A71   | accepted  |  # uppercase hex is valid
    | P0a71   | rejected  |  # lowercase hex
```

---


## Graph relations (explicit)

**Feature: DTC ingestion gate** DESCRIBES **DTCLab BDD v1.0**
**test_dtc_ingestion_gate.py** VERIFIES **Feature: DTC ingestion gate**
