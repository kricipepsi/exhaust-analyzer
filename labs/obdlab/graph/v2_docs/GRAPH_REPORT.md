# Graph Report - C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\obdlab\graph\v2_docs\ingest_ready  (2026-06-10)

## Corpus Check
- 68 files · ~15,673 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 480 nodes · 1045 edges · 19 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_DLD OBDLab|DLD OBDLab]]
- [[_COMMUNITY_DLD OBDLab|DLD OBDLab]]
- [[_COMMUNITY_PRD OBDLab|PRD OBDLab]]
- [[_COMMUNITY_BDD OBDLab|BDD OBDLab]]
- [[_COMMUNITY_ADR OBDLab|ADR OBDLab]]
- [[_COMMUNITY_LLD OBDLab|LLD OBDLab]]
- [[_COMMUNITY_DLD OBDLab|DLD OBDLab]]
- [[_COMMUNITY_ADR OBDLab|ADR OBDLab]]
- [[_COMMUNITY_DLD OBDLab|DLD OBDLab]]
- [[_COMMUNITY_ADR OBDLab|ADR OBDLab]]
- [[_COMMUNITY_PRD OBDLab|PRD OBDLab]]
- [[_COMMUNITY_LLD OBDLab|LLD OBDLab]]
- [[_COMMUNITY_ADR OBDLab|ADR OBDLab]]
- [[_COMMUNITY_BDD OBDLab|BDD OBDLab]]
- [[_COMMUNITY_ADR OBDLab|ADR OBDLab]]
- [[_COMMUNITY_PRD OBDLab|PRD OBDLab]]
- [[_COMMUNITY_DLD OBDLab|DLD OBDLab]]
- [[_COMMUNITY_ADR OBDLab|ADR OBDLab]]
- [[_COMMUNITY_ADR OBDLab|ADR OBDLab]]

## God Nodes (most connected - your core abstractions)
1. `15. Test Coverage (current)` - 34 edges
2. `7. COMLab Integration Points` - 23 edges
3. `OBDLivePayload` - 22 edges
4. `BDD_OBDLab v2.0` - 20 edges
5. `3. `schemas/dna_view.py` - 20 edges
6. `OBDLab` - 18 edges
7. `6. `core/pid_ingestion_validator.py` — `PIDIngestionValidator` - 18 edges
8. `3. Internal Pipeline (7 steps + guarded emitters)` - 18 edges
9. `COMLab` - 17 edges
10. `O2Normalizer.normalize` - 17 edges

## Surprising Connections (you probably didn't know these)
- `OBDLab` --DESCRIBES--> `9 jobs addressed`  [EXTRACTED]
  ADR_OBDLab/ADR-0001_Revive_as_Emitter.md → PRD_OBDLab/Section_6_Value_Proposition.md
- `OBDLab` --GATED_BY--> `import-isolation audit`  [EXTRACTED]
  ADR_OBDLab/ADR-0001_Revive_as_Emitter.md → HLD_OBDLab/2_Architecture_Position.md
- `OBDLivePayload` --DESCRIBES--> `key gains`  [EXTRACTED]
  ADR_OBDLab/ADR-0001_Revive_as_Emitter.md → PRD_OBDLab/Section_6_Value_Proposition.md
- `SEMANTIC_CONTRACT §4.4` --VERIFIES--> `bank-2 null contract`  [EXTRACTED]
  ADR_OBDLab/ADR-0009_Bank2_Null_Contract.md → LLD_OBDLab/2_Physical_Sensor_Bounds.md
- `TrimVectorAggregator.aggregate` --ROUTES_TO--> `step [6]`  [EXTRACTED]
  ADR_OBDLab/ADR-0009_Bank2_Null_Contract.md → HLD_OBDLab/3_Internal_Pipeline.md

## Import Cycles
- None detected.

## Communities (19 total, 0 thin omitted)

### Community 0 - "DLD OBDLab"
Cohesion: 0.06
Nodes (60): [0.0, 200.0], 3-branch VE routing, 6 target VE entries, ADR-0008, air_metering_strategy, _calc_ve_standard, _classify_validity, COMLab T-COMV2-VE-GATE-1 (+52 more)

### Community 1 - "DLD OBDLab"
Cohesion: 0.09
Nodes (44): 3-zone narrowband mapping, COMLab T-COMV2-O2OFFSET-1, Feature: O2 normalisation, 10. `core/o2_normalizer.py` — `O2Normalizer, 2. `schemas/vocabulary.py` — 8 StrEnums, 2. Architecture Position, 5. O2 Normalisation Architecture, 8. O2 Normaliser Boundaries (`core/o2_normalizer.py`) (+36 more)

### Community 2 - "PRD OBDLab"
Cohesion: 0.09
Nodes (43): 12 sensor bounds, 13 P0 features, 31 payload fields, 4 deferred items, 5 physical constants, 7 assumptions, 7 DNA view fields, 7 success criteria (+35 more)

### Community 3 - "BDD OBDLab"
Cohesion: 0.09
Nodes (40): 4 unit conversion factors, absent optional channels → null, Anti-orphan (S4), _apply_unit_conversions, BDD_OBDLab v2.0, bounds violation rejection, canonical key precedence, COMLab T-COMV2-ECU-FUSE-1 (+32 more)

### Community 4 - "ADR OBDLab"
Cohesion: 0.12
Nodes (30): 2-bank V-engine aggregation, ADR-0009, bank1 − bank2, bank1 + bank2 aggregation, bank-2 null contract behaviour, Bank-2 trims null, never 0.0, on single-bank engines, COMLab fault_atlas_router, COMLab T-COMV2-BANK-FUSE-1 (+22 more)

### Community 5 - "LLD OBDLab"
Cohesion: 0.15
Nodes (29): AnalyticsPreconditions, AnalyticsPreconditions.evaluate, CKP_CMP_FAULT_DTCS, cold-engine defaults, Feature: Trim analytics precondition gate, 13. `core/analytics_preconditions.py` — `AnalyticsPreconditions, 6. Trim Analytics Gate — 8-Gate Priority Chain, 10. Analytics Preconditions (`core/analytics_preconditions.py`) (+21 more)

### Community 6 - "DLD OBDLab"
Cohesion: 0.13
Nodes (29): cold-engine payload defaults, cold-engine thermal freeze, COMLab lab_pipeline_aggregator, Feature: Cold-engine thermal freeze, Feature: Pipeline happy path (warm idle), 14. `core/sensor_signal_translator.py` — `SensorSignalTranslator, 15. Test Coverage (current), 4. `schemas/payload.py` — `OBDLivePayload` (31 fields) (+21 more)

### Community 7 - "ADR OBDLab"
Cohesion: 0.11
Nodes (28): [-127, 127], 12 PID bounds, ADR-0006, bank-2 null contract, COMLab trim-evidence scoring, ADR-0006: Widen fuel-trim bounds to the OBD rail `±127` and treat rails as signal, 8. `core/semantic_consistency_checker.py` — `SemanticConsistencyChecker, 2. Physical Sensor Bounds (`config/physical_sensor_bounds.json`) (+20 more)

### Community 8 - "DLD OBDLab"
Cohesion: 0.11
Nodes (26): 12 fields vs physical_sensor_bounds.json, 12 PID fields vs physical_sensor_bounds.json §3.1, 7-step validation pipeline, before SemanticConsistencyChecker, cell ≥ 0, value ∈ [-127, 127], compute_bucket, cyl ≥ 1, count ≥ 0, 6. `core/pid_ingestion_validator.py` — `PIDIngestionValidator (+18 more)

### Community 9 - "ADR OBDLab"
Cohesion: 0.13
Nodes (24): 9 jobs addressed, ADR-0007, AirMeteringStrategy, competitive advantage, confidence, dna_view.py, ADR-0007: Prune the dead standalone classifier and orphan enums/fields, 3. `schemas/dna_view.py (+16 more)

### Community 10 - "PRD OBDLab"
Cohesion: 0.15
Nodes (22): 4DApp Engineering Lead, ADR-0001, advanced workshop technician, COMLab, COMLab Team, ADR-0001: Revive OBDLab as a perception-channel emitter, not a fault classifier, 14. `freeze_frame_pids` Forwarding Contract, Section 1 — Summary (+14 more)

### Community 11 - "LLD OBDLab"
Cohesion: 0.18
Nodes (21): calculate_sensor_error_delta, calculate_w_theo, 12. `core/maf_linearity.py, 11. MAF Linearity (`core/maf_linearity.py`), 1. Physical Constants (`core/ve_engine.py`), DUAL_MAF_MAP_CROSSCHECK + LinearityAccumulator, eta_v, displacement, map_kpa, rpm, iat_c, maf_linearity helpers (+13 more)

### Community 12 - "ADR OBDLab"
Cohesion: 0.26
Nodes (17): ADR-0005, bounds violation, DNA-RPM HIGH breach, bank-2 null contract, non-numeric PID, invalid fuel-status/misfire/cell-vector, COMLab except ObdLabError, ADR-0005: Unify the exception hierarchy under `ObdLabError, 5. `core/exceptions.py, 15. Error Types, ObdLabError, ObdLabError hierarchy (+9 more)

### Community 13 - "BDD OBDLab"
Cohesion: 0.26
Nodes (15): 5% redline overshoot headroom, _check_dna_rpm, DNA-RPM gate three-branch behaviour, _DNA_RPM_HEADROOM = 1.05, DNA-RPM three-branch gate, Feature: DNA-relative RPM gate (three-branch confidence), 4. DNA-RPM Gate (`core/pid_ingestion_validator.py`), engine_rpm > rated_rpm × 1.05 (+7 more)

### Community 14 - "ADR OBDLab"
Cohesion: 0.23
Nodes (14): ADR-0004, _CUTOFF_ECT_COLD=75, _CUTOFF_ECT_CLOSED=80, _CUTOFF_VSS=10, _CUTOFF_RPM_STALLED=400, defensive path, ADR-0004: Remove Physics Gate 3; fold its intent into `FAULT_VE_SENSOR_SKEW, 9. Semantic Consistency Thresholds (`core/semantic_consistency_checker.py`), gates 1, 2, 4 only, gates_passed == 3 (+6 more)

### Community 15 - "PRD OBDLab"
Cohesion: 0.27
Nodes (11): 0 cross-lab imports, 12-field drift guard, Section 4 — Objective, KR1, KR2, KR3, KR4, KR5 (+3 more)

### Community 16 - "DLD OBDLab"
Cohesion: 0.27
Nodes (11): 10 modules, 2 data files, 3 schema modules, config/, core/, DLD_OBDLab v1.0, DLD_OBDLab v2.0, 1. Module Map (+3 more)

### Community 17 - "ADR OBDLab"
Cohesion: 0.33
Nodes (9): ADR-0002, Anti-orphan grep (Stage 4), COMLab frozen contract surface, ADR-0002: Emit at Stage 2, consume at Stage 4 — forward-registered consumers & proposals, emit-S2 / consume-S4 pattern, forward-registered fields have live reader, forward-registered proposals, Proposals: EP-OBD-11, EP-OBD-12, EP-OBD-17 (+1 more)

### Community 18 - "ADR OBDLab"
Cohesion: 0.43
Nodes (7): 9 architecture decisions, ADR-0001..0009, ADR_OBDLab, ADR_OBDLab v1.0, ADR_OBDLab v2.0, Graph relations (explicit), HLD_OBDLab / DLD_OBDLab / LLD_OBDLab

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OBDLivePayload` connect `DLD OBDLab` to `ADR OBDLab`, `ADR OBDLab`, `ADR OBDLab`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Why does `BDD_OBDLab v2.0` connect `BDD OBDLab` to `DLD OBDLab`, `DLD OBDLab`, `ADR OBDLab`, `DLD OBDLab`, `BDD OBDLab`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Why does `SEMANTIC_CONTRACT §4.4` connect `ADR OBDLab` to `ADR OBDLab`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `DLD OBDLab` be split into smaller, more focused modules?**
  _Cohesion score 0.06440677966101695 - nodes in this community are weakly interconnected._
- **Should `DLD OBDLab` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Should `PRD OBDLab` be split into smaller, more focused modules?**
  _Cohesion score 0.08748615725359911 - nodes in this community are weakly interconnected._
- **Should `BDD OBDLab` be split into smaller, more focused modules?**
  _Cohesion score 0.09102564102564102 - nodes in this community are weakly interconnected._

## Build Notes

- Extraction path: deterministic parser over prepared `## Graph relations (explicit)` sections.
- LLM backend note: `graphify extract --backend claude-cli` was attempted, but local Claude CLI reported `loggedIn: false`; no API-key backend was configured in the shell.
- Directed graph: yes. Edges preserve source -> target from explicit relation lines.
