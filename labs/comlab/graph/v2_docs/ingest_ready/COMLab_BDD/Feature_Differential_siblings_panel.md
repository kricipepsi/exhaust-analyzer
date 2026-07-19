
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: Differential siblings panel · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
## Feature: Differential siblings panel
*Tests: `unit/test_fault_atlas_router.py`*

```gherkin
Scenario: Runtime runner-ups and editor-curated siblings are merged
  Given the triage loop produced runner-up faults
    And the winning KG node lists editor-curated differential_siblings
  When the siblings are assembled
  Then both sources are unioned and deduplicated by fault_id
    And the total is capped at 5

Scenario: An editor-curated sibling that did not fire has no score
  Given an editor-curated sibling absent from this session's runner-ups
  When the siblings are assembled
  Then that sibling appears with confidence_score null
```

---


## Graph relations (explicit)

**Feature: Differential siblings panel** DESCRIBES **COMLab BDD v1.0**
