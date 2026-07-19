
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Feature: Phase-2 candidate scoring · Parent document: BDD_DTCLab.md
## Feature: Phase-2 candidate scoring
*Backing tests: `tests/unit/test_rank_candidates.py`, `tests/unit/test_classify_top3.py`.*

```gherkin
Scenario: A confirmed DTC scores its family as DEFINITIVE at full weight
  Given a payload whose confirmed_dtcs map to lean_condition
  When candidates are ranked
  Then lean_condition has raw_confidence 1.0
  And its match_type is DEFINITIVE

Scenario: A pending-only DTC scores its family as INDICATIVE
  Given a payload whose only evidence is a pending DTC mapping to misfire
  When candidates are ranked
  Then misfire has raw_confidence 0.5
  And its match_type is INDICATIVE

Scenario: A DNA-gated family is down-weighted when VIN confidence is PARTIAL
  Given a catalyst_failure candidate at weight 1.0
  And a PARTIAL-confidence DNA view
  When candidates are ranked
  Then catalyst_failure raw_confidence is 0.7   # 1.0 x 0.7 DNA factor

Scenario: classify_top3 clamps, dedups, and caps at three families
  Given candidates spanning five distinct families
  When classify_top3 is called
  Then at most three (family, confidence) pairs are returned
  And every confidence is within [0, 1]
  And the list is sorted by descending confidence then family name
  And the confidences are NOT normalised to sum to 1
```

---


## Graph relations (explicit)

**Feature: Phase-2 candidate scoring** DESCRIBES **DTCLab BDD v1.0**
**test_classify_top3.py** VERIFIES **Feature: Phase-2 candidate scoring**
