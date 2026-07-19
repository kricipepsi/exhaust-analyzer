> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Feature: Model-year resolution and the L collision | Parent document: BDD_VINLab.md / shipped unit tests

## Feature: Model-year resolution and the L collision

```gherkin
Feature: Year resolution handles passthrough characters and the 1990/2020 collision

  Scenario: A passthrough year character yields an unknown year
    Given a VIN whose position-10 character is 0, U, or Z
    When the year is resolved
    Then model_year is None (unknown, not an error)

  Scenario Outline: The L year is disambiguated by the WMI era hint
    Given a VIN with year code L and WMI era_hint = <hint>
    When the year is resolved
    Then model_year = <year>

    Examples:
      | hint    | year |
      | legacy  | 1990 |
      | modern  | 2020 |

  Scenario: A year outside the supported window is out of scope
    Given a resolved model_year of 2023
    When the scope guard runs
    Then a VINDecodeError is raised (year out of supported scope 1990-2020)
```
*Maps to:* `_resolve_year`, H2 guard.

---


## Graph relations (explicit)

**Feature: Model-year resolution and the L collision** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_decoder.py** VERIFIES **Feature: Model-year resolution and the L collision**
