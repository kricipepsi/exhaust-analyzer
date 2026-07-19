
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Feature: Deterministic candidate ranking · Parent document: BDD_GASLab.md
## Feature: Deterministic candidate ranking
*Tests: `unit/test_rank_candidates.py`, `unit/test_rule_engine.py`*

```gherkin
Scenario: The narrowest signature wins over a broader one
  Given two surviving candidates that both match the reading
    And neither is a catch-all
  When the verdict is chosen
  Then the candidate with the narrower total signature width is emitted

Scenario: Catch-all signatures are chosen last
  Given a specific fault and a catch-all fault both match
  When the verdict is chosen
  Then the specific fault is emitted and the catch-all is not

Scenario: No surviving candidate yields normal operation
  Given a reading that matches no fault signature after resolution
  When the verdict is chosen
  Then chemical_state is NORMAL_OPERATION

Scenario: Identical candidates resolve deterministically
  Given two candidates that tie on every ranking key
  When the verdict is chosen
  Then the winner is the one declared first in the ontology
    And the result is identical across process restarts
```

---


## Graph relations (explicit)

**Feature: Deterministic candidate ranking** DESCRIBES **GASLab BDD v2.1**
**test_rank_candidates.py** VERIFIES **candidate ranking** -- specificity, catch-all last, tie stability
**test_rule_engine.py** VERIFIES **deterministic ranking** -- NORMAL_OPERATION fallback


