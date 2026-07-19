
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Feature: Routing-tag mapping with DNA gates · Parent document: BDD_DTCLab.md
## Feature: Routing-tag mapping with DNA gates
*Backing tests: `tests/unit/test_routing_tag_mapper.py`, `tests/integration/test_dtclab_pipeline.py`.*

```gherkin
Scenario: Ungated DTCs always map to their tag
  Given confirmed DTCs ["P0171", "P0300"]
  When the DTCs are mapped to routing tags
  Then the tags include LEAN_HISTORY and MISFIRE_HISTORY

Scenario: A catalyst code on a catalyst-equipped vehicle (HIGH confidence) emits
  Given a HIGH-confidence DNA view with has_catalyst = True
  And confirmed DTCs ["P0420"]
  When the DTCs are mapped
  Then the tags include CATALYST_HISTORY

Scenario: A catalyst code on a non-catalyst vehicle (HIGH confidence) is suppressed
  Given a HIGH-confidence DNA view with has_catalyst = False
  And confirmed DTCs ["P0420"]
  When the DTCs are mapped
  Then the tags do not include CATALYST_HISTORY

Scenario: A low-confidence VIN never suppresses a real DTC
  Given a NONE-confidence DNA view (or dna_view = None)
  And confirmed DTCs ["P0420"]
  When the DTCs are mapped
  Then the tags include CATALYST_HISTORY

Scenario: POA_HISTORY is never emitted by the mapper
  Given any set of confirmed DTCs
  When the DTCs are mapped
  Then POA_HISTORY is never in the result
  # POA_HISTORY is injected by COMLab on GASLab POA_SIGNATURE (T-FX-3)
```

---


## Graph relations (explicit)

**Feature: Routing-tag mapping with DNA gates** DESCRIBES **DTCLab BDD v1.0**
**test_routing_tag_mapper.py** VERIFIES **Feature: Routing-tag mapping with DNA gates**
