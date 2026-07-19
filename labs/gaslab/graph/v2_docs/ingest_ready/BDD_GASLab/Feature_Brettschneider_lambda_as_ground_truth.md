
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: Brettschneider lambda as ground truth · Parent document: BDD_GASLab.md
## Feature: Brettschneider lambda as ground truth
*Tests: `unit/test_brettschneider.py`*

```gherkin
Scenario: A stoichiometric burn reads near unity
  Given a clean stoichiometric reading
  When lambda is computed from chemistry
  Then lambda_chem is approximately 1.000

Scenario: A misfiring cylinder does not fool lambda
  Given a reading with high HC and high O2 in stoichiometric proportion
  When lambda is computed from chemistry
  Then lambda_chem stays near 1.000
  # misfire-immunity: raw fuel and raw air leave together (GAS_WIKI §4.3)

Scenario: NOx is included when the analyser reports it
  Given a reading with a non-zero NOx channel
  When lambda is computed from chemistry
  Then the NOx correction term is added to the 4-gas lambda

Scenario: A degenerate all-zero sample returns a safe value
  Given a reading whose carbon sum is zero
  When lambda is computed from chemistry
  Then lambda_chem is the 1.0 sentinel
    And validity gating independently flags SAMPLE_INVALID
```

---


## Graph relations (explicit)

**Feature: Brettschneider lambda as ground truth** DESCRIBES **GASLab BDD v2.1**
**test_brettschneider.py** VERIFIES **lambda_chem()** -- stoich, misfire-immunity, NOx correction, safe sentinel


