# Graph Report - C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\gaslab\tests  (2026-06-11)

## Corpus Check
- 24 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 494 nodes · 723 edges · 53 communities (20 shown, 33 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.77)
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
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]

## God Nodes (most connected - your core abstractions)
1. `_dna()` - 67 edges
2. `_reading()` - 65 edges
3. `_dna()` - 15 edges
4. `_reading()` - 15 edges
5. `_dna()` - 11 edges
6. `_reading()` - 11 edges
7. `_dna()` - 10 edges
8. `_reading()` - 10 edges
9. `_candidate()` - 9 edges
10. `_cam_map_idle_rich()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `test_boundary_gaslab_run()` --calls--> `build_gaslab_descriptor()`  [INFERRED]
  generative/test_boundary.py → fixtures/descriptor.py
- `test_combinatorial_gaslab_run()` --calls--> `build_gaslab_descriptor()`  [INFERRED]
  generative/test_combinatorial.py → fixtures/descriptor.py
- `test_noise_gaslab_run()` --calls--> `build_gaslab_descriptor()`  [INFERRED]
  generative/test_noise.py → fixtures/descriptor.py
- `test_gaslab_overlap_run()` --calls--> `build_gaslab_descriptor()`  [INFERRED]
  generative/test_overlap.py → fixtures/descriptor.py
- `test_boundary_permutation_no_orphans()` --calls--> `boundary_grid()`  [INFERRED]
  unit/test_validators.py → fixtures/synthetic_grid.py

## Import Cycles
- None detected.

## Communities (53 total, 33 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (57): GasLabDnaView, GasReading, _cam_map_high(), _cam_map_idle(), _dna(), ontology(), overlaps(), Tests for ``gaslab/resolution.py`` — entity resolution layer.  Covers the four s (+49 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (35): GasReading, GasLabDnaView, GasLabDnaView, GasReading, boundary_grid(), iter_edge_probes(), Boundary-permutation grid generator for the 5-gas analyser envelope.  Produces s, Yield ``GasReading`` points spanning the 5-gas analyser envelope.      Ranges an (+27 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (31): LambdaBand, Tests for gaslab.contracts — enums, GasReading, GasLabPayload., 4-gas reading is rejected — NOₓ is required per GAS_VOCABULARY §2., Every gas field validates against analyser envelope — GAS_VOCABULARY §2., Pydantic rejects values outside analyser measurement ranges., A well-formed payload passes validation., lambda_measured is optional — omitting it yields None (OBD-present cars)., lambda_measured within [0.5, 2.0] is accepted.  vocab: GAS_VOCABULARY §2/§6. (+23 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (31): GasLabDnaView, GasReading, MonkeyPatch, CandidateScore, ChemicalSignature, MatchType, _candidate(), _dna() (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (29): Path, _load_raw(), Tests for ``gas_lab_ontology.yaml`` and ``ontology_loader.py``.  Covers the seve, The low-NOₓ + high-HC + high-O₂ override per ``GAS_WIKI §8.4`` is encoded., Every DNA-gated ``ChemicalSignature`` from ``GAS_VOCABULARY §3.1``     declares, ``load_ontology`` raises ``OntologyLoadError`` for a missing file., ``load_ontology`` raises ``OntologyLoadError`` for unparseable YAML., ``load_ontology`` raises ``OntologyLoadError`` when required keys are absent. (+21 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (23): GasLabDnaView, GasReading, _dna(), ontology(), Tests for ranked GASLab candidates., For SPECIFIC candidates, more corroborating channels means higher score., Ordering is stable and follows the exact ranking key., The existing single-verdict API remains unchanged. (+15 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (21): Tests for ``gaslab/rule_engine.py`` — rule engine graph traversal.  Covers the f, Mild-lean rough idle with NOx rising and HC/CO falling keeps CAM_TIMING_ADVANCED, Normalising idle->2500 lean keeps LEAN_MIXTURE and prunes CAM_MAF.      Source:, Persisting lean keeps CAM_MAF and prunes LEAN_MIXTURE.      Source: GAS_WIKI §8., A single lean-family candidate is unchanged by the 6c precedence rule., GDI_HPFP signature with non-GDI DNA → VACUUM_REGULATOR_DIAPHRAGM_RUPTURE.      P, Masking gases with cylinder_count = 4 -> IGNITION_MISFIRE.      Source: docs/GAS, Same gases at cylinder_count in {1, 4, 8, 12} all -> IGNITION_MISFIRE.      Sour (+13 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (23): GasLabDnaView, _dna(), Build a minimal valid ``GasLabDnaView`` with optional overrides., When multiple faults match, the narrowest (most specific) wins.      A reading o, High-idle HC + CO load signature emits WORN_PISTON_RINGS., Valve-seal HC/CO vector + reading_high + fuel_trim = 2.0 -> WORN_VALVE_SEALS., Ring HC/CO vector + fuel_trim = -15.0 -> WORN_PISTON_RINGS., Valve-seal HC/CO but negative trim (-15.0) -> not WORN_VALVE_SEALS (falls throug (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.09
Nodes (22): The same reading classifies as O2_SENSOR_BIASED_* for one sensor type but not an, Assert cylinder_count actively participates in masking decision.      Source: do, Cam-timing signature (HC > 1000, O2 > 2.0, CO present, MAF bounds) classifies to, Build a nominal ``GasReading`` with optional overrides., Idle HC at 600 and high-idle HC at 650 with lambda mismatch stays on POA_SIGNATU, Given a normal-operation gas profile, classify returns NORMAL_OPERATION., A nominal reading is normal for generic bounds but outside when shifted.      Wh, Full classify() returns non-NORMAL_OPERATION when CoC target tightens bounds. (+14 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (16): build_gaslab_descriptor(), GASLab ModuleDescriptor declaration., Build a ModuleDescriptor for the GASLab fork., Generative boundary tests for GASLab., Generate boundary cases from the GASLab descriptor and run them., test_boundary_gaslab_run(), Generative combinatorial tests for GASLab., Generate pairwise cases from the GASLab descriptor and run them. (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (19): Tests for gaslab.validity_gates — triangle gate and dilution screen., Triangle EXTERNAL_O2_SUSPECT + dilution pass → EXTERNAL_O2_SUSPECT., 14 ≤ CO+CO2+O2 ≤ 16 → VALID., 16 < sum ≤ 18 → EXTERNAL_O2_SUSPECT., sum < 14 or > 18 → INVALID., CO+CO2 < 6 % → dilution gate returns False., Triangle INVALID takes priority — dilution not checked., Low triangle sum with non-normal HC remains INVALID at the gate. (+11 more)

### Community 11 - "Community 11"
Cohesion: 0.20
Nodes (16): GasLabDnaView, GasReading, _collect_reachable(), _dna(), dna_variants(), _fault_midpoint_readings(), _probe_grid(), Per-``ChemicalSignature`` reachability probe for the rule engine.  Verifies that (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (16): GasLabDnaView, GasReading, _classify(), _dna(), T-P8-7: Verify EXHAUST_AIR_LEAK collision-rule HC discriminator.  wiki: GAS_WIKI, HC Normal (<=100) + collision pattern + triangle > 16 -> EXHAUST_AIR_LEAK., HC > 100 + collision pattern + triangle > 16 -> RICH_MISFIRE, not EXHAUST_AIR_LE, HC > 100 + collision + triangle <= 16 -> RICH_MISFIRE (unchanged path). (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (15): Tests for gaslab.dna_view — GasLabDnaView slim DNA projection., engine_displacement_liters must be > 0., target_lambda_v112 must be in [0.5, 2.5] per GAS_VOCABULARY §6., cylinder_count must be in [1, 16]., All 13 fields from GAS_WIKI §1.4 table are present and typed., Optional fields default to None when not provided., Assert that GasLabDnaView fields exactly match the 13 fields in wiki §1.4., Mutation must raise — frozen model. (+7 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (13): GasReading, _cam_map_idle_rich(), Rich idle that partially normalises toward 2500 keeps CAM_TIMING_RETARDED_MAP., A flat rich signature idle→2500 rejects CAM_TIMING_RETARDED_MAP.      A sensor/f, RPM-confirmed cam timing prunes a co-surviving low-HC generic misfire.      The, Without an RPM-confirmed timing survivor, low-HC misfire candidates are unchange, Euro-4 rejects a 2500-RPM CAM_MAP HC value that Euro-2 admits., Wiki-conformant CAM_TIMING_RETARDED_MAP rich-idle vector.      λ≈0.755 (∈ [0.75, (+5 more)

### Community 15 - "Community 15"
Cohesion: 0.17
Nodes (11): Tests for gaslab.brettschneider — Brettschneider 5-gas lambda., CO=0.3, CO2=14.8, O2=0.2, HC=20, NOx=20 → λ ∈ [0.99, 1.01]., HC=1500, CO=0.2, CO2=8, O2=4, NOx=10 → λ ∈ [0.98, 1.05].      The masking case f, NOx omitted raises TypeError; NOx=0 with high HC stays valid.      GasReading re, Parametrised sweep across rich → stoich → lean., Custom Hcv value is accepted (methane=4.0 gives different result)., test_5gas_required(), test_custom_hcv() (+3 more)

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (7): GasLabDnaView, _dna(), Tests for ``gaslab/process.py`` — public entry point., GasLabPayload survives model_dump_json → model_validate_json round-trip., End-to-end: process() with a normal reading returns NORMAL_OPERATION., test_payload_round_trip(), test_process_happy_path()

### Community 18 - "Community 18"
Cohesion: 0.50
Nodes (3): Parametrized integration tests over gaslab_cases.csv., Run master-derived integration cases., test_csv_cases()

### Community 20 - "Community 20"
Cohesion: 0.67
Nodes (3): MonkeyPatch, ``classify`` forwards ``engine_state`` to ``apply_differentiators``.      Monkey, test_classify_passes_engine_state_to_apply_differentiators()

## Knowledge Gaps
- **16 isolated node(s):** `GasLabDnaView`, `GasLabDnaView`, `GasReading`, `ChemicalSignature`, `MatchType` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_dna()` connect `Community 7` to `Community 6`, `Community 8`, `Community 14`, `Community 20`, `Community 22`, `Community 23`, `Community 24`, `Community 25`, `Community 26`, `Community 27`, `Community 28`, `Community 29`, `Community 30`, `Community 31`, `Community 32`, `Community 33`, `Community 34`, `Community 35`, `Community 36`, `Community 37`, `Community 38`, `Community 39`, `Community 40`, `Community 41`, `Community 42`, `Community 43`, `Community 44`, `Community 45`, `Community 46`, `Community 47`, `Community 48`, `Community 49`, `Community 50`, `Community 51`, `Community 52`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `_reading()` connect `Community 8` to `Community 6`, `Community 7`, `Community 14`, `Community 20`, `Community 22`, `Community 23`, `Community 24`, `Community 25`, `Community 26`, `Community 27`, `Community 28`, `Community 29`, `Community 30`, `Community 31`, `Community 32`, `Community 33`, `Community 34`, `Community 35`, `Community 36`, `Community 37`, `Community 38`, `Community 39`, `Community 40`, `Community 41`, `Community 42`, `Community 43`, `Community 44`, `Community 45`, `Community 46`, `Community 47`, `Community 48`, `Community 49`, `Community 50`, `Community 51`, `Community 52`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `Pytest configuration for gaslab — shared harness path for generative tests.`, `GASLab ModuleDescriptor declaration.`, `Build a ModuleDescriptor for the GASLab fork.` to the rest of the system?**
  _238 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.06612685560053981 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.10887096774193548 - nodes in this community are weakly interconnected._