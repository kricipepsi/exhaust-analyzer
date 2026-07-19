# Graph Report - dtclab_v2docs  (2026-07-06)

## Corpus Check
- 75 files · ~12,593 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 375 nodes · 300 edges · 75 communities (28 shown, 47 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7b7b2b9b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_16. Test Coverage|16. Test Coverage]]
- [[_COMMUNITY_5. `schemasfreeze_frame.py` — `FreezeFrameRecord`|5. `schemas/freeze_frame.py` — `FreezeFrameRecord`]]
- [[_COMMUNITY_13. `family_map.py` — Routing-tag → canonical-family map  (Phase-2 input)|13. `family_map.py` — Routing-tag → canonical-family map  *(Phase-2 input)*]]
- [[_COMMUNITY_ADR — DTCLab|ADR — DTCLab]]
- [[_COMMUNITY_3. `schemasdna_view.py`|3. `schemas/dna_view.py`]]
- [[_COMMUNITY_4. `schemaspayload.py` — `DTCLabPayload` (9 fields)|4. `schemas/payload.py` — `DTCLabPayload` (9 fields)]]
- [[_COMMUNITY_8. COMLab Integration Points|8. COMLab Integration Points]]
- [[_COMMUNITY_Section 7 — Solution|Section 7 — Solution]]
- [[_COMMUNITY_2. `schemasvocabulary.py` — Enums and Constants|2. `schemas/vocabulary.py` — Enums and Constants]]
- [[_COMMUNITY_9. Non-Functional Requirements|9. Non-Functional Requirements]]
- [[_COMMUNITY_17. Forbidden Patterns (DTCLab-specific)|17. Forbidden Patterns (DTCLab-specific)]]
- [[_COMMUNITY_2. Historical Context Classifier — Exact Boundary Values|2. Historical Context Classifier — Exact Boundary Values]]
- [[_COMMUNITY_14. `ranking.py` — Phase-2 scorer|14. `ranking.py` — Phase-2 scorer]]
- [[_COMMUNITY_10. Known Gaps & Proposals|10. Known Gaps & Proposals]]
- [[_COMMUNITY_3. Mode $06 Margin Tri-State — Exact Boundaries|3. Mode $06 Margin Tri-State — Exact Boundaries]]
- [[_COMMUNITY_Section 8 — Release|Section 8 — Release]]
- [[_COMMUNITY_11. `corerouting_tag_mapper.py` — `RoutingTagMapper`|11. `core/routing_tag_mapper.py` — `RoutingTagMapper`]]
- [[_COMMUNITY_16. Error Types and Codes|16. Error Types and Codes]]
- [[_COMMUNITY_15. `configrouting_tag_map.yaml` — Schema and DNA-Gated Entries|15. `config/routing_tag_map.yaml` — Schema and DNA-Gated Entries]]
- [[_COMMUNITY_6. DNA-Gate Architecture|6. DNA-Gate Architecture]]
- [[_COMMUNITY_15. Phase-2 Scorer Boundaries (`ranking.py`)|15. Phase-2 Scorer Boundaries (`ranking.py`)]]
- [[_COMMUNITY_1. DTC Format Regex — Exact String|1. DTC Format Regex — Exact String]]
- [[_COMMUNITY_Section 2 — Contacts|Section 2 — Contacts]]
- [[_COMMUNITY_10. `coremode06_evaluator.py`|10. `core/mode06_evaluator.py`]]
- [[_COMMUNITY_8. `corefreeze_frame_extractor.py`|8. `core/freeze_frame_extractor.py`]]
- [[_COMMUNITY_12._core_data_fusion_sanitizer.py_—_DataFusionSanitizer|12._core_data_fusion_sanitizer.py_—_DataFusionSanitizer.md]]
- [[_COMMUNITY_7._core_dtc_ingestion_gate.py|7._core_dtc_ingestion_gate.py.md]]
- [[_COMMUNITY_9._core_historical_context_classifier.py|9._core_historical_context_classifier.py.md]]
- [[_COMMUNITY_ADR-0001_Strict_lab_isolation_via_a_locally-mirrored_DNA_view|ADR-0001_Strict_lab_isolation_via_a_locally-mirrored_DNA_view.md]]
- [[_COMMUNITY_ADR-0002_Typed_DTCLabPayload_as_the_single_COMLab_boundary_contract|ADR-0002_Typed_DTCLabPayload_as_the_single_COMLab_boundary_contract.md]]
- [[_COMMUNITY_ADR-0003_DNA_gate_as_a_filter,_not_a_requirement_(three-branch_confidence)|ADR-0003_DNA_gate_as_a_filter,_not_a_requirement_(three-branch_confidence).md]]
- [[_COMMUNITY_ADR-0004_Routing-tag_mapping_lives_in_external_YAML,_not_code|ADR-0004_Routing-tag_mapping_lives_in_external_YAML,_not_code.md]]
- [[_COMMUNITY_ADR-0005_POA_HISTORY_is_injected_by_COMLab,_never_emitted_by_DTCLab|ADR-0005_POA_HISTORY_is_injected_by_COMLab,_never_emitted_by_DTCLab.md]]
- [[_COMMUNITY_ADR-0006_Cross-field_coolant_fluid_signatures_as_a_post-mapping_step_(5b)|ADR-0006_Cross-field_coolant_fluid_signatures_as_a_post-mapping_step_(5b).md]]
- [[_COMMUNITY_ADR-0007_Phase-2_scorer_reuses_§16_weights_—_no_new_literal,_no_normalisation|ADR-0007_Phase-2_scorer_reuses_§16_weights_—_no_new_literal,_no_normalisation.md]]
- [[_COMMUNITY_ADR-0008_Drop_SAI_HISTORY_secondary-air_from_the_routing_surface|ADR-0008_Drop_SAI_HISTORY_secondary-air_from_the_routing_surface.md]]
- [[_COMMUNITY_ADR-0009_Surface_Mode_$06_monitor-aborted_no-start_state_(EP-DTC-NOSTART-1)|ADR-0009_Surface_Mode_$06_monitor-aborted_no-start_state_(EP-DTC-NOSTART-1).md]]
- [[_COMMUNITY_BDD — DTCLab|BDD — DTCLab]]
- [[_COMMUNITY_Feature_Cross-field_coolant_fluid_signatures_(pipeline_step_5b)|Feature_Cross-field_coolant_fluid_signatures_(pipeline_step_5b).md]]
- [[_COMMUNITY_Feature_DTC_ingestion_gate|Feature_DTC_ingestion_gate.md]]
- [[_COMMUNITY_Feature_Freeze-frame_extraction_and_symptom_flags|Feature_Freeze-frame_extraction_and_symptom_flags.md]]
- [[_COMMUNITY_Feature_Historical_fault-context_classification|Feature_Historical_fault-context_classification.md]]
- [[_COMMUNITY_Feature_Lab_isolation_(cross-cutting_invariant)|Feature_Lab_isolation_(cross-cutting_invariant).md]]
- [[_COMMUNITY_Feature_Mode_$06_monitor_evaluation|Feature_Mode_$06_monitor_evaluation.md]]
- [[_COMMUNITY_Feature_Payload_assembly_and_contract_validation|Feature_Payload_assembly_and_contract_validation.md]]
- [[_COMMUNITY_Feature_Phase-2_candidate_scoring|Feature_Phase-2_candidate_scoring.md]]
- [[_COMMUNITY_Feature_Routing-tag_mapping_with_DNA_gates|Feature_Routing-tag_mapping_with_DNA_gates.md]]
- [[_COMMUNITY_DLD — DTCLab|DLD — DTCLab]]
- [[_COMMUNITY_1._Module_Map|1._Module_Map.md]]
- [[_COMMUNITY_6._schemas_mode06_result.py|6._schemas_mode06_result.py.md]]
- [[_COMMUNITY_HLD — DTCLab|HLD — DTCLab]]
- [[_COMMUNITY_1._Responsibility|1._Responsibility.md]]
- [[_COMMUNITY_2._Architecture_Position|2._Architecture_Position.md]]
- [[_COMMUNITY_3._Internal_Pipeline_(Phase_1_—_sanitize)|3._Internal_Pipeline_(Phase_1_—_sanitize).md]]
- [[_COMMUNITY_4._Phase-2_Scorer_(ranking.py)_—_optional_candidate_ranking|4._Phase-2_Scorer_(ranking.py)_—_optional_candidate_ranking.md]]
- [[_COMMUNITY_5._Routing_Tag_Architecture|5._Routing_Tag_Architecture.md]]
- [[_COMMUNITY_7._Mode_$06_Architecture|7._Mode_$06_Architecture.md]]
- [[_COMMUNITY_LLD — DTCLab|LLD — DTCLab]]
- [[_COMMUNITY_10._Config_Path_Resolution|10._Config_Path_Resolution.md]]
- [[_COMMUNITY_11._Error_Contracts|11._Error_Contracts.md]]
- [[_COMMUNITY_12._POA_HISTORY_Injection_—_Exact_Contract_(COMLab_side)|12._POA_HISTORY_Injection_—_Exact_Contract_(COMLab_side).md]]
- [[_COMMUNITY_13._AirMeteringStrategy_and_ResolvedHorizon_Divergence|13._AirMeteringStrategy_and_ResolvedHorizon_Divergence.md]]
- [[_COMMUNITY_14._Cross-Field_Coolant_Fluid_Signatures_(step_5b)|14._Cross-Field_Coolant_Fluid_Signatures_(step_5b).md]]
- [[_COMMUNITY_4._Freeze-Frame_Symptom_Flags_—_Exact_Thresholds|4._Freeze-Frame_Symptom_Flags_—_Exact_Thresholds.md]]
- [[_COMMUNITY_5._DTC_Confidence_Weights_—_Exact_Values|5._DTC_Confidence_Weights_—_Exact_Values.md]]
- [[_COMMUNITY_6._MID_Key_Pattern_—_Exact_Regex|6._MID_Key_Pattern_—_Exact_Regex.md]]
- [[_COMMUNITY_7._DNA-Gate_Dispatch_—_check_high_confidence_gate|7._DNA-Gate_Dispatch_—_check_high_confidence_gate.md]]
- [[_COMMUNITY_8._RoutingTagMapper_—_Output_Ordering|8._RoutingTagMapper_—_Output_Ordering.md]]
- [[_COMMUNITY_9._LRU_Cache_—_Mode_$06_Dictionary|9._LRU_Cache_—_Mode_$06_Dictionary.md]]
- [[_COMMUNITY_PRD — DTCLab|PRD — DTCLab]]
- [[_COMMUNITY_Section_1_—_Summary|Section_1_—_Summary.md]]
- [[_COMMUNITY_Section_3_—_Background|Section_3_—_Background.md]]
- [[_COMMUNITY_Section_4_—_Objective|Section_4_—_Objective.md]]
- [[_COMMUNITY_Section_5_—_Market_Segment|Section_5_—_Market_Segment.md]]
- [[_COMMUNITY_Section_6_—_Value_Proposition|Section_6_—_Value_Proposition.md]]

## God Nodes (most connected - your core abstractions)
1. `16. Test Coverage` - 13 edges
2. `5. `schemas/freeze_frame.py` — `FreezeFrameRecord`` - 13 edges
3. `13. `family_map.py` — Routing-tag → canonical-family map  *(Phase-2 input)*` - 12 edges
4. `ADR — DTCLab` - 11 edges
5. `3. `schemas/dna_view.py`` - 10 edges
6. `4. `schemas/payload.py` — `DTCLabPayload` (9 fields)` - 10 edges
7. `8. COMLab Integration Points` - 8 edges
8. `Section 7 — Solution` - 8 edges
9. `2. `schemas/vocabulary.py` — Enums and Constants` - 7 edges
10. `9. Non-Functional Requirements` - 7 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (75 total, 47 thin omitted)

### Community 0 - "16. Test Coverage"
Cohesion: 0.13
Nodes (14): 16. Test Coverage, File: `test_classify_top3.py` / `test_rank_candidates.py`, File: `test_dna_view.py`, File: `test_dtc_ingestion_gate.py`, File: `test_dtclab_pipeline.py`, File: `test_dtclab_regression.py`, File: `test_family_map.py`, File: `test_freeze_frame_extractor.py` (+6 more)

### Community 1 - "5. `schemas/freeze_frame.py` — `FreezeFrameRecord`"
Cohesion: 0.13
Nodes (14): 5. `schemas/freeze_frame.py` — `FreezeFrameRecord`, Field: `calculated_load_pct`, Field: `coolant_temp_c`, Field: `engine_rpm`, Field: `fuel_system_status`, Field: `ignition_advance_deg`, Field: `intake_air_temp_c`, Field: `long_term_ft1` (+6 more)

### Community 2 - "13. `family_map.py` — Routing-tag → canonical-family map  *(Phase-2 input)*"
Cohesion: 0.14
Nodes (13): 13. `family_map.py` — Routing-tag → canonical-family map  *(Phase-2 input)*, Graph relations (explicit), Routing tag: `CATALYST_HISTORY`, Routing tag: `ECU_INTERNAL_HISTORY`, Routing tag: `EGR_HISTORY`, `EVAP_HISTORY`, `THERMAL_HISTORY`, `IDLE_CONTROL_HISTORY`, `BOOST_HISTORY`, `COOLANT_SYSTEM_MALFUNCTION`, `CYLINDER_FLUID_MISFIRE`, Routing tag: `INJECTOR_HISTORY`, Routing tag: `KNOCK_HISTORY`, Routing tag: `LEAN_HISTORY` (+5 more)

### Community 3 - "ADR — DTCLab"
Cohesion: 0.17
Nodes (11): ADR: ADR-0001, ADR: ADR-0002, ADR: ADR-0003, ADR: ADR-0004, ADR: ADR-0005, ADR: ADR-0006, ADR: ADR-0007, ADR: ADR-0008 (+3 more)

### Community 4 - "3. `schemas/dna_view.py`"
Cohesion: 0.17
Nodes (11): 3. `schemas/dna_view.py`, `DtcEmissionsView` (3 fields), `DtcLabDnaView` (8 fields), Enum: `AirMeteringStrategy`, Enum: `EuroEmissionCategory`, Enum: `ResolvedHorizon`, Enum: `VinConfidence`, Enums (+3 more)

### Community 5 - "4. `schemas/payload.py` — `DTCLabPayload` (9 fields)"
Cohesion: 0.17
Nodes (11): 4. `schemas/payload.py` — `DTCLabPayload` (9 fields), Field: `active_mil`, Field: `confirmed_dtcs`, Field: `freeze_frame`, Field: `historical_fault_context`, Field: `mil_flashing`, Field: `mode_06_monitors`, Field: `pending_dtcs` (+3 more)

### Community 6 - "8. COMLab Integration Points"
Cohesion: 0.20
Nodes (9): 8. COMLab Integration Points, `DTCLabPayload` field / scorer output: `active_mil` / `mil_flashing`, `DTCLabPayload` field / scorer output: `classify_top3()` → `(family, confidence)`, `DTCLabPayload` field / scorer output: `confirmed_dtcs`, `DTCLabPayload` field / scorer output: `freeze_frame`, `DTCLabPayload` field / scorer output: `historical_fault_context`, `DTCLabPayload` field / scorer output: `mode_06_monitors`, `DTCLabPayload` field / scorer output: `routing_tags` (+1 more)

### Community 7 - "Section 7 — Solution"
Cohesion: 0.20
Nodes (9): Assumption: `DTC_CONFIDENCE_WEIGHTS` values are correct for COMLab aggregation and Phase-2 scoring, Assumption: `dtc_severity_map.yaml` not required, Assumption: `mode_06_hex_dictionary.json` covers needed universal CAN MIDs, Assumption: Phase-2 scorer needs no new numeric literal, Assumptions, Graph relations (explicit), Key Features (all P0), Section 7 — Solution (+1 more)

### Community 8 - "2. `schemas/vocabulary.py` — Enums and Constants"
Cohesion: 0.22
Nodes (8): 2. `schemas/vocabulary.py` — Enums and Constants, Enum: `DTCRoutingTag`, Enum: `DTCSeverityClass`, Enum: `DTCState`, Enum: `FuelSystemStatus`, Enum: `HistoricalFaultContext`, Enum: `Mode06MonitorState`, Graph relations (explicit)

### Community 9 - "9. Non-Functional Requirements"
Cohesion: 0.22
Nodes (8): 9. Non-Functional Requirements, Graph relations (explicit), Requirement: Determinism, Requirement: DTC format, Requirement: Import isolation, Requirement: Mode $06 cache, Requirement: POA_HISTORY, Requirement: Scorer purity

### Community 10 - "17. Forbidden Patterns (DTCLab-specific)"
Cohesion: 0.22
Nodes (8): 17. Forbidden Patterns (DTCLab-specific), Graph relations (explicit), Pattern: Adding a `DTCLabPayload` field without a named COMLab consumer, Pattern: Diesel-specific DTC patterns, Pattern: `dtc_severity_map.yaml` loader, Pattern: `from gaslab import ...` / `from obdlab import ...` / `from comlab import ...`, Pattern: `POA_HISTORY` in `routing_tag_map.yaml`, Pattern: `secondary_air_equipped` / `SAI_HISTORY`

### Community 11 - "2. Historical Context Classifier — Exact Boundary Values"
Cohesion: 0.22
Nodes (8): 2. Historical Context Classifier — Exact Boundary Values, Condition: `ECT == 59.9`, Condition: `ECT == 60.0`, Condition: `RPM == 1000`, Condition: `RPM == 2000`, Condition: `RPM == 2001 AND load == 45.1`, Condition: `RPM == 999 AND load == 24.9`, Graph relations (explicit)

### Community 12 - "14. `ranking.py` — Phase-2 scorer"
Cohesion: 0.25
Nodes (7): 14. `ranking.py` — Phase-2 scorer, `CandidateScore` (frozen dataclass), `classify_top3(payload, *, dna_view=None) → list[tuple[str, float]]`, DNA confidence factors (`§14.2`), Graph relations (explicit), `MatchType(StrEnum)`, `rank_candidates(payload, *, dna_view=None) → list[CandidateScore]`

### Community 13 - "10. Known Gaps & Proposals"
Cohesion: 0.25
Nodes (7): 10. Known Gaps & Proposals, Graph relations (explicit), ID: `DTC_CONFIDENCE_WEIGHTS` drift guard, ID: `dtc_severity_map.yaml`, ID: **EP-DTC-NOSTART-1**, ID: Manufacturer-specific MIDs, ID: T-FX-3 enforcement

### Community 14 - "3. Mode $06 Margin Tri-State — Exact Boundaries"
Cohesion: 0.25
Nodes (7): 3. Mode $06 Margin Tri-State — Exact Boundaries, Graph relations (explicit), Value: `margin < 0`, Value: `margin == 0.0`, Value: `margin == 0.001`, Value: `margin == 15.0`, Value: `margin == 15.001`

### Community 15 - "Section 8 — Release"
Cohesion: 0.25
Nodes (7): Explicitly Deferred (v2 backlog), Graph relations (explicit), ID: **EP-DTC-NOSTART-1**, Proposals (labelled — not shipped; consumer nameable), Section 8 — Release, Success Criteria, v2 Scope

### Community 16 - "11. `core/routing_tag_mapper.py` — `RoutingTagMapper`"
Cohesion: 0.29
Nodes (6): 11. `core/routing_tag_mapper.py` — `RoutingTagMapper`, `_check_high_confidence_gate(gate_name) → bool`, Constructor: `__init__(map_path, dna_view)`, `_gate_allows(tag, gate_name) → bool`, Graph relations (explicit), `map(confirmed_dtcs: list[str]) → list[DTCRoutingTag]`

### Community 17 - "16. Error Types and Codes"
Cohesion: 0.29
Nodes (6): 16. Error Types and Codes, Error: `DTCFormatError(ValueError)`, Error: `FreezeFrameIncompleteError(ValueError)`, Error: Pydantic `ValidationError`, Error: `ValueError`, Graph relations (explicit)

### Community 18 - "15. `config/routing_tag_map.yaml` — Schema and DNA-Gated Entries"
Cohesion: 0.33
Nodes (5): 15. `config/routing_tag_map.yaml` — Schema and DNA-Gated Entries, Graph relations (explicit), Patterns: `^P040[0-9]$`, Patterns: `^P0420$`, Patterns: `^P0430$`

### Community 19 - "6. DNA-Gate Architecture"
Cohesion: 0.33
Nodes (5): 6. DNA-Gate Architecture, Gate name: `egr_equipped`, Gate name: `has_catalyst`, Gate name: unknown gate, Graph relations (explicit)

### Community 20 - "15. Phase-2 Scorer Boundaries (`ranking.py`)"
Cohesion: 0.33
Nodes (5): 15. Phase-2 Scorer Boundaries (`ranking.py`), Confidence assembly, DNA confidence factor (`§14.2`), Graph relations (explicit), MatchType ← weight mapping

### Community 21 - "1. DTC Format Regex — Exact String"
Cohesion: 0.33
Nodes (5): 1. DTC Format Regex — Exact String, Graph relations (explicit), Position: 1, Position: 2, Position: 3–5

### Community 22 - "Section 2 — Contacts"
Cohesion: 0.33
Nodes (5): Graph relations (explicit), Name: 4DApp Engineering Lead, Name: COMLab Team, Name: DTCLab Owner, Section 2 — Contacts

### Community 23 - "10. `core/mode06_evaluator.py`"
Cohesion: 0.40
Nodes (4): 10. `core/mode06_evaluator.py`, `classify_margin(margin_pct: float) → Mode06MonitorState`, `evaluate_monitor(mid_key, margin_pct, dictionary_path) → Mode06MonitorResult`, Graph relations (explicit)

### Community 24 - "8. `core/freeze_frame_extractor.py`"
Cohesion: 0.40
Nodes (4): 8. `core/freeze_frame_extractor.py`, `evaluate_coolant_dtc_context(dtc_code, fuel_status) → str | None`  *(step 5b)*, `extract_freeze_frame(raw: dict, codes_cleared: bool = False) → FreezeFrameRecord`, Graph relations (explicit)

### Community 25 - "12._core_data_fusion_sanitizer.py_—_DataFusionSanitizer.md"
Cohesion: 0.50
Nodes (3): 12. `core/data_fusion_sanitizer.py` — `DataFusionSanitizer`, Graph relations (explicit), `sanitize(raw_dtcs, raw_freeze_frame, raw_mode06, *, codes_cleared=False, active_mil=False, mil_flashing=False) → DTCLabPayload`

### Community 26 - "7._core_dtc_ingestion_gate.py.md"
Cohesion: 0.50
Nodes (3): 7. `core/dtc_ingestion_gate.py`, Graph relations (explicit), `validate_dtc_list(codes: list[str], mode: str) → list[str]`

### Community 27 - "9._core_historical_context_classifier.py.md"
Cohesion: 0.50
Nodes (3): 9. `core/historical_context_classifier.py`, `classify_historical_context(coolant_temp_c, engine_rpm, calculated_load_pct) → HistoricalFaultContext`, Graph relations (explicit)

## Knowledge Gaps
- **267 isolated node(s):** `ADR: ADR-0001`, `ADR: ADR-0002`, `ADR: ADR-0003`, `ADR: ADR-0004`, `ADR: ADR-0005` (+262 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **47 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `ADR: ADR-0001`, `ADR: ADR-0002`, `ADR: ADR-0003` to the rest of the system?**
  _267 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `16. Test Coverage` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `5. `schemas/freeze_frame.py` — `FreezeFrameRecord`` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `13. `family_map.py` — Routing-tag → canonical-family map  *(Phase-2 input)*` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._