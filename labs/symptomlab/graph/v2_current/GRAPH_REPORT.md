# Graph Report - 4DLabV2\labs\symptomlab  (2026-06-06)

## Corpus Check
- 11 files · ~2,040 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 101 nodes · 180 edges · 11 communities (8 shown, 3 thin omitted)
- Extraction: 58% EXTRACTED · 42% INFERRED · 0% AMBIGUOUS · INFERRED: 75 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f7544224`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]

## God Nodes (most connected - your core abstractions)
1. `EnvironmentalConditions` - 22 edges
2. `SymptomDNA` - 21 edges
3. `OccursDuring` - 16 edges
4. `EngineState` - 15 edges
5. `_make_full_payload()` - 11 edges
6. `TestSymptomDNAFromJsonMissingRequired` - 11 edges
7. `SymptomValidationError` - 10 edges
8. `SymptomValidator` - 10 edges
9. `TestSymptomDNAFromJsonRoundTrip` - 9 edges
10. `TestSymptomDNAFromJsonInvalidEnum` - 9 edges

## Surprising Connections (you probably didn't know these)
- `TestSymptomDNAFromJsonRoundTrip` --uses--> `SymptomValidationError`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py
- `TestSymptomDNAFromJsonMissingRequired` --uses--> `SymptomValidationError`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py
- `TestSymptomDNAFromJsonInvalidEnum` --uses--> `SymptomValidationError`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py
- `TestSymptomDNAFromJsonNoPairValidation` --uses--> `SymptomValidationError`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py
- `TestSymptomDNAFromJsonRoundTrip` --uses--> `OccursDuring`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py

## Communities (11 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (15): _get_validator(), SymptomLab — Part B symptom-triage module for the 4DLab DNA system., Return a SymptomValidator for `allowed_path`. Cached per distinct path., Validate a triage selection and package it as a SymptomDNA.      Per SEMANTIC_CO, resolve(), _clear_validator_cache(), Clear the lru_cache after each test to release resources., Calls with the same allowed_path reuse the cached validator instance. (+7 more)

### Community 1 - "Community 1"
Cohesion: 0.18
Nodes (9): EnvironmentalConditions, The 4-field Part B payload, per SEMANTIC_CONTRACT.md §4.2.      No routing field, Serialize to the JSON shape from contract §4.2., SymptomDNA, Sanity tests for SymptomLab models., test_symptom_dna_is_frozen(), test_symptom_dna_to_json_keys(), SymptomDNA with no free_text_notes should round-trip. (+1 more)

### Community 2 - "Community 2"
Cohesion: 0.21
Nodes (9): StrEnum, EngineState, from_json(), OccursDuring, Raised when (tier_1, tier_2) is not one of the 18 allowed combinations,     or e, SymptomValidationError, SymptomValidator, validator() (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.19
Nodes (6): _make_full_payload(), Tests for SymptomDNA.from_json deserialization., from_json must reject payloads with invalid enum strings., TestSymptomDNAFromJsonInvalidEnum, TestSymptomDNAFromJsonMissingRequired, TestSymptomDNAFromJsonRoundTrip

### Community 4 - "Community 4"
Cohesion: 0.13
Nodes (5): Comprehensive tests for SymptomLab validator and models., TestAll18Combinations, TestAllEnumValues, TestFreeTextNotes, TestJSONShape

### Community 5 - "Community 5"
Cohesion: 0.38
Nodes (6): _load_yaml_pairs(), Drift guard: allowed_combinations.yaml must match VehicleDNA.md §"Complete Unive, Every pair in the YAML must be in the VehicleDNA.md reference table., Every pair in the VehicleDNA.md reference table must be in the YAML., test_vehicledna_reference_matches_yaml(), test_yaml_matches_vehicledna_reference()

### Community 7 - "Community 7"
Cohesion: 0.50
Nodes (3): from_json() does NOT validate (tier_1, tier_2) catalog membership.     This is i, from_json() accepts an unknown (tier_1, tier_2) pair without error.         Call, TestSymptomDNAFromJsonNoPairValidation

## Knowledge Gaps
- **1 isolated node(s):** `labs/symptomlab — SymptomLab v2`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SymptomValidator` connect `Community 2` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.320) - this node is a cross-community bridge._
- **Why does `_get_validator()` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.243) - this node is a cross-community bridge._
- **Why does `SymptomDNA` connect `Community 1` to `Community 2`, `Community 3`, `Community 4`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.207) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `EnvironmentalConditions` (e.g. with `SymptomValidator` and `TestSymptomDNAFromJsonRoundTrip`) actually correct?**
  _`EnvironmentalConditions` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `SymptomDNA` (e.g. with `SymptomValidator` and `TestSymptomDNAFromJsonRoundTrip`) actually correct?**
  _`SymptomDNA` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `OccursDuring` (e.g. with `SymptomValidator` and `TestSymptomDNAFromJsonRoundTrip`) actually correct?**
  _`OccursDuring` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `EngineState` (e.g. with `SymptomValidator` and `TestSymptomDNAFromJsonRoundTrip`) actually correct?**
  _`EngineState` has 12 INFERRED edges - model-reasoned connections that need verification._