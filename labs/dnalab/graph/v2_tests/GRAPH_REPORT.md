# Graph Report - labs/dnalab/tests  (2026-06-13)

## Corpus Check
- 8 files · ~1,239 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 58 nodes · 95 edges · 12 communities (4 shown, 8 thin omitted)
- Extraction: 58% EXTRACTED · 42% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.8)
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
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]

## God Nodes (most connected - your core abstractions)
1. `make_vin_dna()` - 22 edges
2. `make_symptom_dna()` - 21 edges
3. `TestBuildVehicleDNA` - 11 edges
4. `TestVehicleDNASerialization` - 8 edges
5. `TestVehicleDNARoundTrip` - 6 edges
6. `fake_decode_returning()` - 5 edges
7. `fake_resolve_returning()` - 4 edges
8. `sample_dna()` - 4 edges
9. `TestVehicleDNAConstruction` - 4 edges
10. `Any` - 2 edges

## Surprising Connections (you probably didn't know these)
- `make_vin_dna()` --references--> `Any`  [EXTRACTED]
  conftest.py → conftest.py  _Bridges community 1 → community 0_
- `make_vin_dna()` --references--> `VinDNA`  [EXTRACTED]
  conftest.py → conftest.py  _Bridges community 1 → community 5_
- `sample_dna()` --calls--> `make_vin_dna()`  [EXTRACTED]
  conftest.py → conftest.py  _Bridges community 1 → community 2_
- `make_symptom_dna()` --references--> `SymptomDNA`  [EXTRACTED]
  conftest.py → conftest.py  _Bridges community 0 → community 6_
- `sample_dna()` --calls--> `make_symptom_dna()`  [EXTRACTED]
  conftest.py → conftest.py  _Bridges community 0 → community 2_

## Import Cycles
- None detected.

## Communities (12 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.29
Nodes (4): Any, make_symptom_dna(), Explicit round-trip test for VehicleDNA JSON serialization.  Build a VehicleDNA,, TestVehicleDNARoundTrip

### Community 2 - "Community 2"
Cohesion: 0.29
Nodes (3): DNALab test fixtures., sample_dna(), VehicleDNA

## Knowledge Gaps
- **1 isolated node(s):** `VehicleDNA`
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `make_vin_dna()` connect `Community 1` to `Community 0`, `Community 2`, `Community 4`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.307) - this node is a cross-community bridge._
- **Why does `TestBuildVehicleDNA` connect `Community 3` to `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.278) - this node is a cross-community bridge._
- **Why does `make_symptom_dna()` connect `Community 0` to `Community 1`, `Community 2`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `make_vin_dna()` (e.g. with `.test_happy_path_composes_vehicle_dna_from_fakes()` and `.test_invalid_triage_propagates()`) actually correct?**
  _`make_vin_dna()` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `make_symptom_dna()` (e.g. with `.test_happy_path_composes_vehicle_dna_from_fakes()` and `.test_invalid_vin_propagates()`) actually correct?**
  _`make_symptom_dna()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `VehicleDNA`, `DNALab test fixtures.`, `Controlled DNALab test fixtures.` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._