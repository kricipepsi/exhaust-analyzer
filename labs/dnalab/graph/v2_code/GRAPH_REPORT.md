# Graph Report - labs/dnalab/dnalab  (2026-06-13)

## Corpus Check
- 3 files · ~554 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 26 nodes · 38 edges · 5 communities (3 shown, 2 thin omitted)
- Extraction: 71% EXTRACTED · 29% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ce6b7736`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]

## God Nodes (most connected - your core abstractions)
1. `VehicleDNA` - 10 edges
2. `VinDNA` - 7 edges
3. `SymptomDNA` - 7 edges
4. `Any` - 5 edges
5. `build_vehicle_dna()` - 4 edges
6. `datetime` - 4 edges
7. `Any` - 2 edges
8. `VehicleDNA` - 2 edges
9. `DNALab — the umbrella lab that composes VinDNA + SymptomDNA into VehicleDNA.` - 1 edges
10. `DNALab assembly — build_vehicle_dna() orchestration.` - 1 edges

## Surprising Connections (you probably didn't know these)
- `Any` --uses--> `VehicleDNA`  [INFERRED]
  assembly.py → models.py
- `VehicleDNA` --uses--> `VehicleDNA`  [INFERRED]
  assembly.py → models.py

## Import Cycles
- 1-file cycle: `models.py -> models.py`

## Communities (5 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.31
Nodes (6): Any, Combined Part A (VinDNA) + Part B (SymptomDNA) + session metadata.      The JSON, Serialize to the dict layout from SEMANTIC_CONTRACT.md §4.3.          Top-level, Serialize to a JSON string via to_json_payload().          Forwards **dumps_kwar, Inverse of to_json_payload(). Delegates to each model's from_json.          Rais, VehicleDNA

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (6): build_vehicle_dna(), Any, DNALab assembly — build_vehicle_dna() orchestration., Decode VIN and triage selection, combine into one VehicleDNA.      Args:, # WHY: symptomlab.resolve() requires all five keys; a missing key would, VehicleDNA

### Community 2 - "Community 2"
Cohesion: 0.90
Nodes (4): datetime, Create a VehicleDNA with auto-generated session metadata.          Args:, SymptomDNA, VinDNA

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VehicleDNA` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.599) - this node is a cross-community bridge._
- **Why does `Any` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `VehicleDNA` (e.g. with `Any` and `SymptomDNA`) actually correct?**
  _`VehicleDNA` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `VinDNA` (e.g. with `datetime` and `Any`) actually correct?**
  _`VinDNA` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SymptomDNA` (e.g. with `datetime` and `Any`) actually correct?**
  _`SymptomDNA` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Any` (e.g. with `SymptomDNA` and `VinDNA`) actually correct?**
  _`Any` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DNALab — the umbrella lab that composes VinDNA + SymptomDNA into VehicleDNA.`, `DNALab assembly — build_vehicle_dna() orchestration.`, `Decode VIN and triage selection, combine into one VehicleDNA.      Args:` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._