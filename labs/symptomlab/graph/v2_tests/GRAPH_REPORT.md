# Graph Report - labs\symptomlab\tests  (2026-06-12)

## Corpus Check
- 9 files · ~2,139 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 134 nodes · 163 edges · 14 communities (11 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.8)
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
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `SymptomValidator` - 17 edges
2. `_make_full_payload()` - 12 edges
3. `TestSymptomDNAFromJsonMissingRequired` - 7 edges
4. `TestRejection` - 7 edges
5. `make_symptom_dna()` - 5 edges
6. `TestSymptomDNAFromJsonInvalidEnum` - 5 edges
7. `TestAll21Combinations` - 5 edges
8. `TestImmutability` - 5 edges
9. `Path` - 4 edges
10. `test_symptom_dna_to_json_keys()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `test_symptom_dna_is_frozen()` --calls--> `make_symptom_dna()`  [INFERRED]
  unit/test_models.py → conftest.py
- `test_symptom_dna_preserves_reworked_visible_exhaust_strings()` --calls--> `make_symptom_dna()`  [INFERRED]
  unit/test_models.py → conftest.py
- `test_symptom_dna_to_json_keys()` --calls--> `make_symptom_dna()`  [INFERRED]
  unit/test_models.py → conftest.py

## Import Cycles
- None detected.

## Communities (14 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (16): Any, _make_full_payload(), Tests for SymptomDNA.from_json deserialization., Assert that missing engine_state key inside environment raises SymptomValidation, Pre-load-state payloads default to idle for deterministic migration., # WHY: Pre-load-state payloads default to idle for deterministic migration., from_json must reject payloads with invalid enum strings., Assert that an invalid occurs_during enum string is rejected by from_json. (+8 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (13): SymptomValidator, Assert that an unrecognized tier_2 for a known tier_1 raises SymptomValidationEr, Assert that invalid occurs_during values are rejected., Assert that invalid engine_state values are rejected., Assert that invalid load_state values are rejected., Assert that legacy combinations no longer present in the revised catalog are rej, Assert that free_text_notes is None when omitted., Assert that free_text_notes is None when explicitly set to None. (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (8): Comprehensive tests for SymptomLab validator and models., Assert that occurs_during enum values are correctly accepted and mapped., Assert that engine_state enum values are correctly accepted and mapped., Assert that load_state enum values are correctly accepted and mapped., Assert that the serialized payload contains exactly the 4 required keys., Assert that the payload has exactly 4 keys with no extra additions., TestAllEnumValues, TestJSONShape

### Community 3 - "Community 3"
Cohesion: 0.21
Nodes (12): make_symptom_dna(), SymptomDNA, SymptomDNA, Sanity tests for SymptomLab models., Assert that the serialized SymptomDNA JSON payload contains the exact 4 contract, Assert that revised visible exhaust strings are preserved in the JSON payload., Assert that SymptomDNA instances are frozen and write-protected., Assert that all contract enum values match the specific domain string representa (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.24
Nodes (9): _clear_validator_cache(), Path, Clear the lru_cache after each test to release resources., Calls with the same allowed_path reuse the cached validator instance., Calls with different allowed_path return different validator instances., resolve() with an explicit allowed_path uses the injected test catalog., test_different_allowed_path_returns_independent_instance(), test_resolve_with_explicit_allowed_path() (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (5): Assert that SymptomDNA dataclass attributes cannot be reassigned., Assert that SymptomDNA instances are hashable., Assert that EnvironmentalConditions dataclass attributes cannot be reassigned., Assert string equality behavior for OccursDuring enum., TestImmutability

### Community 6 - "Community 6"
Cohesion: 0.25
Nodes (5): Path, Assert that catalogs not defining exactly 21 combinations are rejected., Assert that the parsed catalog combinations match the revised 21 authoritative p, Assert that all 21 combinations in the catalog are successfully validated., TestAll21Combinations

### Community 7 - "Community 7"
Cohesion: 0.43
Nodes (6): allowed_pairs(), bad_allowed_path(), good_allowed_path(), Path, SymptomValidator, validator()

### Community 8 - "Community 8"
Cohesion: 0.38
Nodes (6): _load_yaml_pairs(), Drift guard: allowed_combinations.yaml must match VehicleDNA.md §"Complete Unive, Every pair in the YAML must be in the VehicleDNA.md reference table., Every pair in the VehicleDNA.md reference table must be in the YAML., test_vehicledna_reference_matches_yaml(), test_yaml_matches_vehicledna_reference()

### Community 9 - "Community 9"
Cohesion: 0.29
Nodes (4): Assert that a complete valid JSON payload successfully round-trips to SymptomDNA, SymptomDNA with no free_text_notes should round-trip., Assert that free_text_notes is set to None if absent from the payload., TestSymptomDNAFromJsonRoundTrip

### Community 10 - "Community 10"
Cohesion: 0.50
Nodes (3): from_json() does NOT validate (tier_1, tier_2) catalog membership.     This is i, from_json() accepts an unknown (tier_1, tier_2) pair without error.         Call, TestSymptomDNAFromJsonNoPairValidation

## Knowledge Gaps
- **4 isolated node(s):** `SymptomValidator`, `SymptomDNA`, `Any`, `Path`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SymptomValidator` connect `Community 1` to `Community 2`, `Community 6`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `TestImmutability` connect `Community 5` to `Community 2`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `_make_full_payload()` connect `Community 0` to `Community 9`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `make_symptom_dna()` (e.g. with `test_symptom_dna_is_frozen()` and `test_symptom_dna_preserves_reworked_visible_exhaust_strings()`) actually correct?**
  _`make_symptom_dna()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `SymptomLab test suite.  Contains unit tests and fixtures for verifying SymptomLa`, `SymptomValidator`, `SymptomDNA` to the rest of the system?**
  _59 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.10153846153846154 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.11462450592885376 - nodes in this community are weakly interconnected._