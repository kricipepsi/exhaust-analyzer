
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: KG enrichment and registry consistency · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
## Feature: KG enrichment and registry consistency
*Tests: `unit/test_fault_atlas_kg.py`, `unit/test_kg_schema.py`, `e2e/test_kg_registry_consistency.py`*

```gherkin
Scenario: The winning fault is enriched from its KG node
  Given a winning fault_id present in the KG
  When the verdict is enriched
  Then fault_enrichment carries the component_group, impacted_subsystems,
       mechanical_failure_mode, and 1..8 ui_remediation_steps for that fault

Scenario: Every registry fault has a KG node and vice versa
  Given the loaded fault registry and the 13 per-family KG files
  When the consistency check runs
  Then every registry fault_id has exactly one KG node
    And every KG fault_id appears in the registry

Scenario: A duplicate fault_id across KG files fails at boot
  Given two KG files declaring the same fault_id
  When the KG is loaded
  Then loading fails before the process is ready to serve
```

---


## Graph relations (explicit)

**Feature: KG enrichment and registry consistency** DESCRIBES **COMLab BDD v1.0**
