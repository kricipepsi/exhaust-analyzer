# Graph Report - C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\obdlab  (2026-06-10)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 111 nodes · 84 edges · 32 communities (12 shown, 20 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0b05ec39`
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
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
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

## God Nodes (most connected - your core abstractions)
1. `VEValidity` - 6 edges
2. `VEEngine.compute_ve` - 5 edges
3. `_calc_ve_standard` - 5 edges
4. `OBDLivePayload` - 5 edges
5. `COMLab` - 5 edges
6. `_DNA_RPM_HEADROOM` - 5 edges
7. `O2Normalizer.normalize` - 4 edges
8. `maf_linearity helpers` - 4 edges
9. `ADR-0001: Revive OBDLab as perception-channel emitter` - 3 edges
10. `ADR-0002: Emit at Stage 2, consume at Stage 4` - 3 edges

## Surprising Connections (you probably didn't know these)
- `VEEngine.compute_ve` --references--> `AirMeteringStrategy`  [EXTRACTED]
  core/ve_engine.py → HLD_OBDLab/4_VE_Routing_Architecture.md
- `VEEngine.compute_ve` --references--> `DUAL_MAF_MAP_CROSSCHECK`  [EXTRACTED]
  core/ve_engine.py → HLD_OBDLab/4_VE_Routing_Architecture.md
- `VEEngine.compute_ve` --references--> `MAF_ONLY`  [EXTRACTED]
  core/ve_engine.py → HLD_OBDLab/4_VE_Routing_Architecture.md
- `VEEngine.compute_ve` --references--> `MAP_ONLY_SPEED_DENSITY`  [EXTRACTED]
  core/ve_engine.py → HLD_OBDLab/4_VE_Routing_Architecture.md
- `VEValidity` --references--> `FAULT_MAF_CONTAMINATION`  [EXTRACTED]
  core/ve_engine.py → DLD_OBDLab/9_core_ve_engine_py.md

## Import Cycles
- None detected.

## Communities (32 total, 20 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (13): KGtopic.md division-of-labor, AnalyticsPreconditions.evaluate, Anti-orphan (S4), COMLab, COMLab fault_atlas_router, Doc-bug O2-FU-2, freeze_frame_pids, normalized_obd_lambda (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (11): _DNA_RPM_HEADROOM, ObdLabError, KR1: pipeline latency < 50 ms, PIDIngestionValidator.validate_and_convert, PIDValidationError, SemanticConsistencyError, SensorSignalTranslator.translate, thermal freeze defaults (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.25
Nodes (8): AirMeteringStrategy, DUAL_MAF_MAP_CROSSCHECK, MAF_ONLY, MAP_ONLY_SPEED_DENSITY, COMLab T-COMV2-VE-GATE-1, VEEngine.compute_ve, ve_pct, ve_validity

### Community 3 - "Community 3"
Cohesion: 0.38
Nodes (7): FAULT_MAF_CONTAMINATION, FAULT_VE_IDLE_COLLAPSE, FAULT_VE_SENSOR_SKEW, UNKNOWN, VALID, _classify_validity, VEValidity

### Community 4 - "Community 4"
Cohesion: 0.33
Nodes (5): COMLab T-COMV2-O2OFFSET-1, O2Normalizer.normalize, O2FailureMode, O2NormalizationMode, O2Normalizer boundaries

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (5): _calc_ve_standard, K_OFFSET, MM_AIR, R_GAS, VEEngine

### Community 6 - "Community 6"
Cohesion: 0.40
Nodes (4): COMLab T-COMV2-ECU-FUSE-1, commanded_equivalence_ratio, FU-ECU-2, lambda_perception_delta

### Community 7 - "Community 7"
Cohesion: 0.40
Nodes (4): COMLab T-COMV2-MAF-LIN-1, calculate_sensor_error_delta, calculate_w_theo, maf_linearity helpers

### Community 8 - "Community 8"
Cohesion: 0.50
Nodes (4): ADR-0001: Revive OBDLab as perception-channel emitter, Revive OBDLab as emitter, T-OBDV2-0, ADR-0007: Prune dead classifier and orphan enums/fields

### Community 9 - "Community 9"
Cohesion: 0.50
Nodes (4): ADR-0002: Emit at Stage 2, consume at Stage 4, emit-S2 / consume-S4 pattern, T-OBDV2-2..11, T-OBDV2-ECU-PERCEPT-1

### Community 10 - "Community 10"
Cohesion: 0.50
Nodes (4): EP-OBD-11, EP-OBD-12, EP-OBD-17, forward-registered proposals

### Community 12 - "Community 12"
Cohesion: 0.67
Nodes (3): COMLab, COMLab frozen contract surface, OBDLivePayload

## Knowledge Gaps
- **68 isolated node(s):** `Revive OBDLab as emitter`, `T-OBDV2-0`, `OBDLab emitter`, `OBDLab`, `COMLab` (+63 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `COMLab` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `ObdLabError` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **What connects `Revive OBDLab as emitter`, `T-OBDV2-0`, `OBDLab emitter` to the rest of the system?**
  _68 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._