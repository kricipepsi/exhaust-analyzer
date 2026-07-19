# Graph Report - temp_dnalab_v1  (2026-06-06)

## Corpus Check
- 12 files · ~2,987 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 98 nodes · 126 edges · 12 communities (9 shown, 3 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.65)
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
- [[_COMMUNITY_Community 10|Community 10]]

## God Nodes (most connected - your core abstractions)
1. `TestBuildVehicleDNA` - 12 edges
2. `_make_vin_dna()` - 11 edges
3. `_make_symptom_dna()` - 11 edges
4. `VehicleDNA` - 9 edges
5. `TestVehicleDNASerialization` - 9 edges
6. `ADR 0004 — Enum-Typed Fields` - 9 edges
7. `build_vehicle_dna()` - 7 edges
8. `TestVehicleDNARoundTrip` - 7 edges
9. `ADR 0001 — Naming Contract: VinDNA / SymptomDNA / VehicleDNA` - 7 edges
10. `ADR 0002 — DNALab Is the Only Lab That Imports Other Labs` - 7 edges

## Surprising Connections (you probably didn't know these)
- `sample_dna()` --calls--> `build_vehicle_dna()`  [INFERRED]
  tests/conftest.py → dnalab/assembly.py
- `TestBuildVehicleDNA` --uses--> `VehicleDNA`  [INFERRED]
  tests/test_assembly.py → dnalab/models.py
- `TestVehicleDNAConstruction` --uses--> `VehicleDNA`  [INFERRED]
  tests/test_models.py → dnalab/models.py
- `TestVehicleDNASerialization` --uses--> `VehicleDNA`  [INFERRED]
  tests/test_models.py → dnalab/models.py
- `TestVehicleDNARoundTrip` --uses--> `VehicleDNA`  [INFERRED]
  tests/test_vehicledna_roundtrip.py → dnalab/models.py

## Communities (12 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.29
Nodes (5): _make_symptom_dna(), _make_vin_dna(), Round-trip and contract tests for VehicleDNA., TestVehicleDNAConstruction, TestVehicleDNASerialization

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (4): build_vehicle_dna(), DNALab assembly — build_vehicle_dna() orchestration., Decode VIN and triage selection, combine into one VehicleDNA.      Args:, TestBuildVehicleDNA

### Community 2 - "Community 2"
Cohesion: 0.17
Nodes (6): VehicleDNA — the combined Part A + Part B payload.  Schema governed by SEMANTIC_, Combined Part A (VinDNA) + Part B (SymptomDNA) + session metadata.      The JSON, Serialize to the dict layout from SEMANTIC_CONTRACT.md §4.3.          Top-level, VehicleDNA, Integration and contract tests for build_vehicle_dna., TestSchemaVersion

### Community 3 - "Community 3"
Cohesion: 0.20
Nodes (9): ADR 0004 — Enum-Typed Fields, Consequences, Context, Date, Decision, Future cut-over to comlab.schemas.vocabulary, Sources, Status (+1 more)

### Community 4 - "Community 4"
Cohesion: 0.42
Nodes (4): _make_symptom_dna(), _make_vin_dna(), Explicit round-trip test for VehicleDNA JSON serialization.  Build a VehicleDNA,, TestVehicleDNARoundTrip

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (7): ADR 0001 — Naming Contract: VinDNA / SymptomDNA / VehicleDNA, Consequences, Context, Date, Decision, Sources, Status

### Community 6 - "Community 6"
Cohesion: 0.25
Nodes (7): ADR 0002 — DNALab Is the Only Lab That Imports Other Labs, Consequences, Context, Date, Decision, Sources, Status

### Community 7 - "Community 7"
Cohesion: 0.25
Nodes (7): ADR 0003 — String-Typed Enum Fields, Consequences, Context, Date, Decision, Sources, Status

## Knowledge Gaps
- **26 isolated node(s):** `Status`, `Date`, `Context`, `Decision`, `Consequences` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VehicleDNA` connect `Community 2` to `Community 0`, `Community 1`, `Community 4`?**
  _High betweenness centrality (0.270) - this node is a cross-community bridge._
- **Why does `TestBuildVehicleDNA` connect `Community 1` to `Community 2`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Why does `build_vehicle_dna()` connect `Community 1` to `Community 8`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `VehicleDNA` (e.g. with `TestBuildVehicleDNA` and `TestSchemaVersion`) actually correct?**
  _`VehicleDNA` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DNALab assembly — build_vehicle_dna() orchestration.`, `Decode VIN and triage selection, combine into one VehicleDNA.      Args:`, `VehicleDNA — the combined Part A + Part B payload.  Schema governed by SEMANTIC_` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._