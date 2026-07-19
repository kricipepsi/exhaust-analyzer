# Graph Report - .  (2026-06-12)

## Corpus Check
- Corpus is ~7,888 words - fits in a single context window. You may not need a graph.

## Summary
- 78 nodes · 169 edges · 7 communities
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]

## God Nodes (most connected - your core abstractions)
1. `SymptomLab` - 43 edges
2. `SymptomDNA` - 18 edges
3. `allowed_combinations.yaml` - 18 edges
4. `from_json` - 13 edges
5. `resolve` - 12 edges
6. `SymptomValidator` - 11 edges
7. `the 18-pair invariant` - 11 edges
8. `environmental axes` - 9 edges
9. `tier vocabulary` - 9 edges
10. `SymptomValidationError` - 7 edges

## Surprising Connections (you probably didn't know these)
- `SymptomDNA` --conceptually_related_to--> `prior, not override`  [EXTRACTED]
  graph/v2_docs/ingest_ready/ADR_SymptomLab/01_ADR-0001_SymptomLab_produces_a_prior_input_never_a_routing_verdict.md → graph/v2_docs/ingest_ready/HLD_SymptomLab/01_1._Responsibility.md
- `SymptomDNA` --conceptually_related_to--> `SEMANTIC_CONTRACT §4.2`  [EXTRACTED]
  graph/v2_docs/ingest_ready/ADR_SymptomLab/01_ADR-0001_SymptomLab_produces_a_prior_input_never_a_routing_verdict.md → graph/v2_docs/ingest_ready/HLD_SymptomLab/01_1._Responsibility.md
- `SymptomValidationError` --references--> `the 18-pair invariant`  [INFERRED]
  graph/v2_docs/ingest_ready/BDD_SymptomLab/02_Feature_Catalog_pair_validation.md → graph/v2_docs/ingest_ready/ADR_SymptomLab/03_ADR-0003_Enforce_exactly_18_catalog_pairs_at_construction.md
- `ADR-0005: SymptomLab is a sibling module with no cross-lab imports` --documents--> `SymptomLab`  [EXTRACTED]
  graph/v2_docs/ingest_ready/ADR_SymptomLab/05_ADR-0005_SymptomLab_is_a_sibling_module_with_no_cross-lab_imports.md → graph/v2_docs/ingest_ready/ADR_SymptomLab/01_ADR-0001_SymptomLab_produces_a_prior_input_never_a_routing_verdict.md
- `ADR_SymptomLab References` --documents--> `SymptomLab`  [EXTRACTED]
  graph/v2_docs/ingest_ready/ADR_SymptomLab/08_References.md → graph/v2_docs/ingest_ready/ADR_SymptomLab/01_ADR-0001_SymptomLab_produces_a_prior_input_never_a_routing_verdict.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **SymptomLab test coverage across five behaviour areas** — code_test_models, code_test_validator, code_test_drift_guard, code_test_symptomdna_from_json, code_test_resolve_isolation [EXTRACTED 0.95]
- **Catalog validation chain (resolve enforces the 18-pair invariant over the YAML catalog)** — concept_resolve, concept_symptomvalidator, concept_allowed_combinations_yaml, concept_18_pair_invariant [INFERRED 0.85]
- **Validation responsibility split between from_json and resolve** — concept_from_json, concept_resolve, concept_symptomvalidator [INFERRED 0.85]
- **SymptomValidator enforces 18-pair catalog to produce SymptomDNA** — concept_symptomvalidator, concept_allowed_combinations_yaml, concept_18_pair_invariant, concept_symptomdna [EXTRACTED 1.00]
- **SymptomDNA to_json/from_json serialization roundtrip** — concept_symptomdna, concept_to_json, concept_from_json [EXTRACTED 1.00]
- **resolve public entry delegates to cached SymptomValidator consumed by DNALab** — concept_resolve, concept_symptomvalidator, concept_dnalab [EXTRACTED 1.00]
- **resolve → SymptomValidator → SymptomDNA validation pipeline** — concept_resolve, concept_symptomvalidator, concept_allowed_combinations_yaml, concept_symptomdna, concept_18_pair_invariant [EXTRACTED 1.00]
- **COMLab consumes SymptomDNA tiers + environmental axes as priors** — concept_comlab, concept_faultatlasrouter, concept_symptomdna, concept_tier_vocabulary, concept_environmental_axes [EXTRACTED 1.00]
- **DNALab assembles SymptomLab Part B via resolve** — concept_dnalab, concept_symptomlab, concept_resolve, concept_symptomdna [EXTRACTED 1.00]

## Communities (7 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.16
Nodes (18): ADR-0002: Tier vocabulary is open (YAML-validated), not a hard-coded enum, ADR-0004: Environmental axes are typed enums; tiers are not, Feature: Environmental-axis validation, BDD Traceability summary, tests/test_models.py, tests/test_validator.py, allowed_combinations.yaml, environmental axes (+10 more)

### Community 1 - "Community 1"
Cohesion: 0.25
Nodes (14): ADR-0006: from_json validates structure only; resolve() owns the catalog invariant, Feature: Resolve happy path, DNALab, operator-symptom channel, resolve, SymptomLab, DLD 5. __init__.py public surface, DLD 1. Module Map (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.22
Nodes (13): ADR-0001: SymptomLab produces a prior input, never a routing verdict, ADR_SymptomLab References, COMLab, EnvironmentalConditions, FaultAtlasRouter, load_state environmental axis, oil_consumption symptom (T-DNA-9, deferred), SEMANTIC_CONTRACT (+5 more)

### Community 3 - "Community 3"
Cohesion: 0.19
Nodes (13): Feature: Catalog pair validation, Feature: The 18-pair invariant, SymptomValidationError, SymptomValidator, validator.py, DLD 7. Error Types, DLD 4. validator.py SymptomValidator, HLD SymptomLab §3 Internal Flow (validate) (+5 more)

### Community 4 - "Community 4"
Cohesion: 0.31
Nodes (9): Feature: JSON boundary (from_json), tests/test_symptomdna_from_json.py, from_json, models.py, to_json, DLD 3. models.py Dataclasses, DLD 8. Test Coverage (current), HLD SymptomLab §9 Known Gaps / Accepted Behaviour (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (7): ADR-0003: Enforce exactly 18 catalog pairs at construction, ADR-0007: Rework the catalog to remove overlap with the environmental axes, tests/test_drift_guard.py, the 18-pair invariant, prior, not override, LLD 1. The 18-Pair Invariant, PRD SymptomLab §6 Value Proposition

### Community 6 - "Community 6"
Cohesion: 0.50
Nodes (4): ADR-0005: SymptomLab is a sibling module with no cross-lab imports, Feature: Isolation (CI-level behaviour), tests/test_resolve_isolation.py, SymptomLab import isolation

## Knowledge Gaps
- **10 isolated node(s):** `legacy 18-pair catalog`, `tests/test_drift_guard.py`, `tests/test_symptomdna_from_json.py`, `tests/test_resolve_isolation.py`, `HLD SymptomLab §2 Architecture Position` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SymptomLab` connect `Community 1` to `Community 5`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `resolve` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **What connects `legacy 18-pair catalog`, `tests/test_drift_guard.py`, `tests/test_symptomdna_from_json.py` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._