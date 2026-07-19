# BDD — SymptomLab (v2)

**Status:** Current (scenarios grounded in the live test suite)
**Reference:** HLD_SymptomLab v2.1 / DLD_SymptomLab v2.1 / LLD_SymptomLab v2.1
**Date:** 2026-06-12

Behaviour specification for SymptomLab's single public behaviour: **validate a two-tier
triage selection and package it as a typed `SymptomDNA`**. Scenarios are declarative;
the truth is the test suite (`tests/`).

Ubiquitous language: *resolve* = run `symptomlab.resolve()`; *catalog* = the 18-pair
`allowed_combinations.yaml`; *environmental axis* = `occurs_during` / `engine_state` /
`load_state`.

---

## Feature: Resolve happy path

```gherkin
Feature: A legal triage selection resolves to a 4-field SymptomDNA

  Scenario: A valid pair with valid environmental context
    Given tier_1 = rough_idle_shudder and tier_2 = surging_hunting_idle
      And occurs_during = cold_only and engine_state = running and load_state = idle
    When the selection is resolved
    Then a SymptomDNA is returned with exactly four fields
      And environmental_conditions.occurs_during = cold_only
      And environmental_conditions.load_state = idle
      And the SymptomDNA serialises to JSON and reloads unchanged
      And the payload contains no routing fields
```
*Maps to:* `tests/test_models.py`, `tests/test_validator.py`.

---

## Feature: Catalog pair validation

```gherkin
Feature: Only catalog pairs are accepted, with actionable errors otherwise

  Scenario: An unknown tier_2 lists the valid sub-filters
    Given tier_1 = visible_exhaust_smoke and tier_2 = green_smoke
    When the selection is resolved
    Then a SymptomValidationError is raised
      And the message lists the valid tier_2 values for visible_exhaust_smoke

  Scenario: An unknown tier_1 lists the valid categories
    Given tier_1 = nonexistent_symptom and tier_2 = anything
    When the selection is resolved
    Then a SymptomValidationError is raised
      And the message lists the six valid tier_1 values
```
*Maps to:* `tests/test_validator.py`.

---

## Feature: Environmental-axis validation

```gherkin
Feature: Environmental context must use the contract vocabulary

  Scenario Outline: Out-of-vocabulary environmental values are rejected
    Given a valid catalog pair
      And occurs_during = <occ> and engine_state = <eng> and load_state = <load>
    When the selection is resolved
    Then the result is <result>

    Examples:
      | occ        | eng           | load                    | result                   |
      | always     | running       | idle                    | SymptomDNA               |
      | cold_only  | cranking      | transient_acceleration  | SymptomDNA               |
      | never      | running       | idle                    | SymptomValidationError   |
      | always     | flying        | idle                    | SymptomValidationError   |
      | always     | running       | hovering                | SymptomValidationError   |
```
*Maps to:* `tests/test_validator.py`.

---

## Feature: The 18-pair invariant

```gherkin
Feature: The catalog must define exactly 18 pairs

  Scenario: A catalog of the wrong size fails at construction
    Given an allowed_combinations.yaml that does not define exactly 18 pairs
    When the SymptomValidator is constructed
    Then a ValueError is raised before any triage is validated

  Scenario: The shipped catalog is the curated 6x3 set
    Given the default allowed_combinations.yaml
    When the SymptomValidator is constructed
    Then it loads exactly 18 (tier_1, tier_2) pairs
```
*Maps to:* `tests/test_drift_guard.py`.

> **Live state:** the shipped `allowed_combinations.yaml` defines exactly **18** pairs,
> with `visible_exhaust_smoke = {black_smoke, blue_oily_smell, white_sweet_smell}`
> (reconciled by T-DNA-8). Both scenarios above pass against the live file.

---

## Feature: JSON boundary (from_json)

```gherkin
Feature: from_json validates structure and enums, not the catalog invariant

  Scenario: A well-formed payload deserialises
    Given a JSON payload with the four fields and valid environmental enums
    When SymptomDNA.from_json is called
    Then a SymptomDNA is returned

  Scenario: A missing required field is rejected
    Given a JSON payload without tier_2_subfield_filter
    When SymptomDNA.from_json is called
    Then a SymptomValidationError is raised (missing required field)

  Scenario: A bad environmental enum string is rejected
    Given a JSON payload whose engine_state is fictional
    When SymptomDNA.from_json is called
    Then a SymptomValidationError is raised

  Scenario: from_json does not enforce the catalog pairing
    Given a JSON payload whose (tier_1, tier_2) is not a catalog pair but is structurally valid
    When SymptomDNA.from_json is called
    Then a SymptomDNA is returned (the pairing invariant is resolve()'s job)
```
*Maps to:* `tests/test_symptomdna_from_json.py`.

---

## Feature: Isolation (CI-level behaviour)

```gherkin
Feature: SymptomLab stays an isolated codebase

  Scenario: No cross-lab Python imports exist
    Given the symptomlab package
    When the import-isolation audit runs
    Then there are no imports from gaslab, obdlab, dtclab, comlab, or vinlab

  Scenario: SymptomDNA carries no routing fields
    Given a resolved SymptomDNA
    When its keys are inspected
    Then there is no suppress_modes, prioritize_modes, or target_backend_equation
```
*Maps to:* `tests/test_resolve_isolation.py`.

---

## Traceability summary

| Behaviour area | Primary test module |
|----------------|---------------------|
| Resolve happy path | `test_models.py`, `test_validator.py` |
| Catalog pair validation | `test_validator.py` |
| Environmental validation | `test_validator.py` |
| 18-pair invariant / drift | `test_drift_guard.py` |
| JSON boundary | `test_symptomdna_from_json.py` |
| Isolation / routing-free | `test_resolve_isolation.py` |
