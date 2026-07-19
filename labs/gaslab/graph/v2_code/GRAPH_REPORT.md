# Graph Report - C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\gaslab\gaslab  (2026-06-11)

## Corpus Check
- 12 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 237 nodes · 407 edges · 12 communities (10 shown, 2 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 94 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

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

## God Nodes (most connected - your core abstractions)
1. `ChemicalSignature` - 47 edges
2. `EngineStateBucket` - 24 edges
3. `GasReading` - 23 edges
4. `GasLabDnaView` - 20 edges
5. `_definitive_match()` - 16 edges
6. `SampleValidity` - 14 edges
7. `rank_candidates()` - 14 edges
8. `MatchType` - 13 edges
9. `apply_differentiators()` - 13 edges
10. `classify()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `GasReading` --uses--> `GasReading`  [INFERRED]
  brettschneider.py → contracts.py
- `find_overlaps()` --calls--> `_is_catch_all()`  [INFERRED]
  resolution.py → audits.py
- `process()` --calls--> `lambda_chem()`  [INFERRED]
  process.py → brettschneider.py
- `apply_differentiators()` --calls--> `lambda_chem()`  [INFERRED]
  resolution.py → brettschneider.py
- `_rpm_route_matches()` --calls--> `lambda_chem()`  [INFERRED]
  resolution.py → brettschneider.py

## Import Cycles
- None detected.

## Communities (12 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (38): EngineStateBucket, GasLabDnaView, GasReading, GasReading, Five raw analyser inputs.  All fields required — no 4-gas fallback.      Source:, Reject readings outside analyser measurement envelope.          Source: ``GAS_VO, _candidate_score(), CandidateScore (+30 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (35): EngineStateBucket, GasLabDnaView, GasReading, SampleValidity, ChemicalSignature, GasLabDnaView, Slim DNA projection consumed by GASLab.  Declared locally so GASLab has no cross, The 13-field DNA slice GASLab consumes.      GASLab does not consume the full `` (+27 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (36): ChemicalSignature, CAM_TIMING_ADVANCED, CAM_TIMING_RETARDED_MAF, CAM_TIMING_RETARDED_MAP, CATALYST_NOT_LIGHTING_OFF, CATALYST_OVERWHELMED, COOLANT_LEAK_INTERNAL, EGR_DILUTION_MISFIRE (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.10
Nodes (31): EngineStateBucket, GasLabDnaView, GasReading, _append_rpm_routes(), apply_differentiators(), _euro_thresholds(), EuroThresholds, find_overlaps() (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (25): CatalystStatus, LIT_AND_WORKING, NOT_EVALUABLE, NOT_LIT, OVERWHELMED, GasBehavior, COLLISION, INVERSE_CORRELATION (+17 more)

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (16): BaseModel, GasReading, EngineStateBucket, COLD_OPEN_LOOP_INVALID, REGULATORY_HIGH_IDLE, STABILIZED_IDLE, STRESS_IDLE, GasLabPayload (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.17
Nodes (15): GasReading, SampleValidity, Triangle-gate verdict.  Source: ``GAS_VOCABULARY §5``., SampleValidity, BORDERLINE, EXTERNAL_O2_SUSPECT, INVALID, VALID (+7 more)

### Community 7 - "Community 7"
Cohesion: 0.19
Nodes (12): Path, find_uncovered_overlaps(), _has_resolution(), _is_catch_all(), parse_vocabulary_thresholds(), Validation audit helpers for GASLab.  Pure functions used by the T-P5-1 validati, Parse per-gas threshold tables from ``GAS_VOCABULARY.md §10``.      Returns a di, Return True if two fault signatures overlap in all six dimensions. (+4 more)

### Community 8 - "Community 8"
Cohesion: 0.24
Nodes (8): Any, Path, load_ontology(), OntologyLoadError, Ontology loader — reads ``gas_lab_ontology.yaml`` into a typed dict.  Pure funct, Raised when ``gas_lab_ontology.yaml`` cannot be parsed or is malformed., Load and return the GASLab declarative ontology.      Args:         path: Path t, RuntimeError

### Community 9 - "Community 9"
Cohesion: 0.40
Nodes (4): GasReading, lambda_chem(), Brettschneider 5-gas lambda — chemistry-only, pure function.  Source: ``GAS_VOCA, Brettschneider 5-gas lambda from tailpipe chemistry.      The carbon-balance den

## Knowledge Gaps
- **65 isolated node(s):** `Path`, `Any`, `NORMAL_OPERATION`, `RICH_MIXTURE`, `LEAN_MIXTURE` (+60 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ChemicalSignature` connect `Community 2` to `Community 0`, `Community 1`, `Community 4`?**
  _High betweenness centrality (0.291) - this node is a cross-community bridge._
- **Why does `EngineStateBucket` connect `Community 5` to `Community 0`, `Community 1`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Why does `GasReading` connect `Community 0` to `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 9`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `ChemicalSignature` (e.g. with `EngineStateBucket` and `GasLabDnaView`) actually correct?**
  _`ChemicalSignature` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `EngineStateBucket` (e.g. with `GasReading` and `EngineStateBucket`) actually correct?**
  _`EngineStateBucket` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `GasReading` (e.g. with `GasReading` and `GasReading`) actually correct?**
  _`GasReading` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `GasLabDnaView` (e.g. with `GasReading` and `EngineStateBucket`) actually correct?**
  _`GasLabDnaView` has 17 INFERRED edges - model-reasoned connections that need verification._