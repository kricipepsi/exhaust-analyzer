# Graph Report - labs\symptomlab\symptomlab  (2026-06-12)

## Corpus Check
- 3 files · ~958 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 40 nodes · 86 edges · 6 communities
- Extraction: 58% EXTRACTED · 42% INFERRED · 0% AMBIGUOUS · INFERRED: 36 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f734acab`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]

## God Nodes (most connected - your core abstractions)
1. `SymptomValidator` - 13 edges
2. `EnvironmentalConditions` - 11 edges
3. `SymptomDNA` - 11 edges
4. `LoadState` - 10 edges
5. `SymptomValidationError` - 8 edges
6. `OccursDuring` - 7 edges
7. `EngineState` - 7 edges
8. `Path` - 7 edges
9. `SymptomDNA` - 7 edges
10. `Path` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Path` --uses--> `EnvironmentalConditions`  [INFERRED]
  __init__.py → models.py
- `Path` --uses--> `LoadState`  [INFERRED]
  __init__.py → models.py
- `Path` --uses--> `SymptomDNA`  [INFERRED]
  __init__.py → models.py
- `Path` --uses--> `SymptomValidator`  [INFERRED]
  __init__.py → validator.py
- `SymptomValidator` --uses--> `EnvironmentalConditions`  [INFERRED]
  __init__.py → models.py

## Import Cycles
- None detected.

## Communities (6 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.28
Nodes (8): _get_validator(), Path, SymptomDNA, SymptomLab — Part B symptom-triage module for the 4DLab DNA system., Return a SymptomValidator for `allowed_path`. Cached per distinct path., Validate a triage selection and package it as a SymptomDNA.      Per SEMANTIC_CO, resolve(), SymptomValidator

### Community 1 - "Community 1"
Cohesion: 0.42
Nodes (7): EngineState, LoadState, OccursDuring, # WHY: Pre-load_state payloads deserialize deterministically as, StrEnum, SymptomDNA, Validate a symptom selection against the catalog of 21 combinations.          Ar

### Community 2 - "Community 2"
Cohesion: 0.40
Nodes (3): The 4-field Part B payload, per SEMANTIC_CONTRACT.md §4.2.      No routing field, Serialize to the JSON shape from contract §4.2., SymptomDNA

### Community 3 - "Community 3"
Cohesion: 0.40
Nodes (5): Raised when (tier_1, tier_2) is not one of the 18 allowed combinations,     or e, SymptomValidationError, Path, Load and parse the allowed combinations catalog from allowed_path.          Args, ValueError

### Community 4 - "Community 4"
Cohesion: 0.50
Nodes (3): Any, EnvironmentalConditions, Deserialize from the dict shape in SEMANTIC_CONTRACT.md §4.2.          Raises Sy

### Community 5 - "Community 5"
Cohesion: 0.40
Nodes (4): Validator for symptom selection against allowed combinations catalog., # WHY: allowed_combinations.yaml must define exactly 21 pairs (7 tier_1 × 3 tier, # WHY: reject any (tier_1, tier_2) pair not explicitly allowed in the catalog, SymptomValidator

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SymptomValidator` connect `Community 5` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.342) - this node is a cross-community bridge._
- **Why does `SymptomDNA` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.216) - this node is a cross-community bridge._
- **Why does `EnvironmentalConditions` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `SymptomValidator` (e.g. with `Path` and `SymptomDNA`) actually correct?**
  _`SymptomValidator` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `EnvironmentalConditions` (e.g. with `Path` and `SymptomDNA`) actually correct?**
  _`EnvironmentalConditions` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `SymptomDNA` (e.g. with `Path` and `SymptomDNA`) actually correct?**
  _`SymptomDNA` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `LoadState` (e.g. with `Path` and `SymptomDNA`) actually correct?**
  _`LoadState` has 7 INFERRED edges - model-reasoned connections that need verification._