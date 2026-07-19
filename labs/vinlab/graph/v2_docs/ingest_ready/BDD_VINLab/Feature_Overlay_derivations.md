> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Feature: Overlay derivations | Parent document: BDD_VINLab.md / shipped unit tests

## Feature: Overlay derivations

```gherkin
Feature: Derived fields come from deterministic overlay rules

  Scenario Outline: Air metering is classified once into both labels
    Given has_maf = <maf> and has_map = <map>
    When air metering is classified
    Then primary_load_calculation = <plc> and air_metering_strategy = <strategy>

    Examples:
      | maf  | map  | plc            | strategy                 |
      | true | true | HYBRID_MAF_MAP | DUAL_MAF_MAP_CROSSCHECK  |
      | true | false| MAF_ONLY       | MAF_ONLY                 |
      | false| true | MAP_ONLY       | MAP_ONLY_SPEED_DENSITY   |
      | false| false| MAP_ONLY       | MAP_ONLY_SPEED_DENSITY   |

  Scenario: Stress-idle RPM is targeted by era + induction + fuel
    Given a EURO_1 naturally-aspirated engine
    When the stress-idle RPM is derived
    Then stress_idle_rpm_target = 3000

  Scenario: Cylinder count is inferred only when unresolved
    Given cylinder_count is still 0 after CSV and vref.db
      And a recognised brand + engine code
    When the cylinder heuristic runs
    Then a brand-rule cylinder count is applied
    But it never overwrites a non-zero CSV or vref.db count
```
*Maps to:* `classify_air_metering`, `stress_idle_rpm`, `infer_cylinder`.

---


## Graph relations (explicit)

**Feature: Overlay derivations** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_air_metering.py** VERIFIES **Feature: Overlay derivations**
**labs/vinlab/tests/unit/test_stress_rpm.py** VERIFIES **vinlab.overlay.stress_rpm.stress_idle_rpm**
**labs/vinlab/tests/unit/test_cylinder_heuristic.py** VERIFIES **vinlab.overlay.cylinder_heuristic.infer_cylinder**
