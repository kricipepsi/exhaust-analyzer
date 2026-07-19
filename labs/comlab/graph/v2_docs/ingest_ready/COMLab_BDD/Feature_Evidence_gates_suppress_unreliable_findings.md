
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: Evidence gates suppress unreliable findings · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
## Feature: Evidence gates suppress unreliable findings
*Tests: `unit/test_ve_evidence_gate.py`, `unit/test_fuel_system_gate.py`, `unit/test_ltft_cell_classification.py`*

```gherkin
Scenario: VE evidence is gated to valid cross-checks
  Given an OBD payload whose ve_validity is FAULT_MAF_CONTAMINATION
  When the VE evidence gate runs
  Then full VE evidence weight is withheld from the verdict

Scenario: Trim evidence is suppressed outside closed loop
  Given an OBD payload whose fuel_system_status is OL_FAULT
  When the fuel-system gate runs
  Then trim-based findings are suppressed

Scenario: Trim analytics blocked upstream are not used
  Given an OBD payload whose trim_analytics_gate is not VALID
  When the triage loop runs
  Then trim-derived findings do not contribute to the verdict
```

---


## Graph relations (explicit)

**Feature: Evidence gates suppress unreliable findings** DESCRIBES **COMLab BDD v1.0**
