# Graph Report - COMLab  (2026-06-01)

## Corpus Check
- 48 files · ~249,117 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1139 nodes · 7495 edges · 30 communities detected
- Extraction: 18% EXTRACTED · 82% INFERRED · 0% AMBIGUOUS · INFERRED: 6127 edges (avg confidence: 0.51)
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
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]

## God Nodes (most connected - your core abstractions)
1. `OrchestratorInboundRequest` - 293 edges
2. `FaultAtlasKG` - 263 edges
3. `VinConfidence` - 245 edges
4. `PowerLossAnalytics` - 233 edges
5. `DTCRoutingTag` - 209 edges
6. `FaultAtlasRouter` - 204 edges
7. `OrchestratorFinalUIOutput` - 203 edges
8. `PerformanceAnalytics` - 201 edges
9. `EngineStateBucket` - 165 edges
10. `O2FailureMode` - 165 edges

## Surprising Connections (you probably didn't know these)
- `Sub-Components: Combustion_Inefficiency_Scaling_Calculator +         Piston_Coun` --uses--> `OrchestratorInboundRequest`  [INFERRED]
  comlab\analytics\power_loss_analytics.py → comlab\schemas\ingestion.py
- `Sub-Component: Pre_vs_Post_Cat_Sensor_Cross_Validator.          Modern cars repo` --uses--> `OrchestratorInboundRequest`  [INFERRED]
  comlab\analytics\power_loss_analytics.py → comlab\schemas\ingestion.py
- `Sub-Component: Catalyst_Conversion_Efficiency_Engine.          Returns Catalyst` --uses--> `OrchestratorInboundRequest`  [INFERRED]
  comlab\analytics\power_loss_analytics.py → comlab\schemas\ingestion.py
- `FaultAtlasKG` --calls--> `kg()`  [INFERRED]
  comlab\core\fault_atlas_kg.py → tests\unit\test_fault_atlas_router.py
- `T-W-ARCH-6: assert explicit ``use_v2_registry`` selects the intended engine.  Ve` --uses--> `FaultAtlasRouter`  [INFERRED]
  tests\unit\test_fault_atlas_router_registry_select.py → comlab\core\fault_atlas_router.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (174): calculate_catalyst_health_index(), estimate_kinetic_loss(), PowerLossAnalytics, Script 4: Power Loss Analytics — the mathematical estimator.  Scale-independent, Sub-Component: Catalyst_Conversion_Efficiency_Engine.          Returns Catalyst, Stage D — returns the populated PerformanceAnalytics block.          Calculates:, Map kinetic_power_loss_pct into severity bands.          lld: §7 — severity regi, Static methods only — this class is pure math, no state.      Reference test cas (+166 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (170): Pure dict-to-Pydantic projection functions per LLD §5.2.  No I/O, no cross-lab i, Project once into all three views.  # lld: §5.2      Returned tuple-shaped model, Derive resolved_horizon from euro_emission_category.      Mapping per COMLab_Hor, Project a full VehicleDNA JSON dict into the requested LabDnaView.  # lld: §5.2, Script 1: Horizon Context Injector — the context gate.  Runs first on every diag, Final output of Stage A horizon resolution.      Source: lld: §6.1., Reads VehicleDNA, returns HorizonContext.      Does NOT parse the VIN. Does NOT, Load eras_sensitivity_masks.yaml once. Cached for process lifetime.          Sou (+162 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (145): CompensatedRichResult, detect(), detect_compensated_rich(), PerceptionContradictionResult, Perception-contradiction detector — Lambda Truth vs Perception.  Pure function c, Compare ECU-perceived lambda against Brettschneider ground truth.      Args:, Detect compensated-rich: ECU masks a fuel leak by pulling trim to the rail., Output of the compensated-rich detector.      Identifies cases where near-stoich (+137 more)

### Community 3 - "Community 3"
Cohesion: 0.2
Nodes (151): FaultAtlasRouter, RegistryRow, DTCLabPayload, FreezeFramePIDs, FreezeFrameRecord, GasLabPayload, OBDLiveDataPayload, OrchestratorInboundRequest (+143 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (32): _horizon_from_euro(), project(), project_all(), _horizon_from_euro(), HorizonContext, _make_vehicle_dna_stub(), _make_vin_dna_stub(), Unit tests for HorizonContextInjector — v1 rewritten interface.  Covers: from_ve (+24 more)

### Community 5 - "Community 5"
Cohesion: 0.1
Nodes (46): _resolve_pid(), kg(), _make_request(), _sanitized(), test_build_differential_siblings_from_kg_node(), test_catalyst_failure_family_routes(), test_catalyst_override_no_trigger_without_flashing(), test_catalyst_override_no_trigger_without_p030x() (+38 more)

### Community 6 - "Community 6"
Cohesion: 0.19
Nodes (44): COMLab Fault Taxonomy, ecu_fault, ERR-E1-M032, ERR-E2-I104, ERR-E3-F501, ERR-EF-001, ERR-EF-002, ERR-LC-001 (+36 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (22): SymptomDNA lab-suppression routing per data_flow_report.md §5.3.  Pure function:, Derive lab routing flags from SymptomDNA environmental conditions.      Routing, route_symptom(), LabRoutingDirective, SymptomDNA routing output. All flags default False.      Produced by symptom_rou, _make_symptom_dna(), SymptomDNA routing table tests — data_flow_report.md §5.3.  Covers every row of, Empty symptom_dna -> all False (neutral), warning logged, no reasons. (+14 more)

### Community 8 - "Community 8"
Cohesion: 0.1
Nodes (31): cylinder_misfire(), egr_flow_codes(), _ff(), fuel_system_rich(), full_confirmed(), malformed_dtc(), no_codes(), p0016_cam_timing_retard() (+23 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (23): catalyst_overwhelmed(), egr_intake_dilution(), exhaust_air_leak(), healthy_baseline(), ignition_misfire_heavy_hc(), incomplete_combustion(), no_obd_legacy(), Mock GasLab payload builders for tests.  These produce dicts that conform to ``c (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (1): TestOperatorEvaluator

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (12): get_tracer(), _initialise_provider_once(), _NoOpSpan, _NoOpTracer, Idempotent, env-gated OpenTelemetry tracer for COMLab.  Mirror of `4DLabWired/_j, Return a tracer for `name`.      Real tracer iff `OTEL_TRACES_EXPORTER` is set A, Reset the singleton guard. Test-only — never call from production code.      Use, No-op span implementing the subset of the OTel Span API used by COMLab.      Eve (+4 more)

### Community 12 - "Community 12"
Cohesion: 0.17
Nodes (16): _all_nodes(), _load_all(), _load_schema(), Unit tests for the 6 populated ``comlab/config/kg/<family>.json`` files.  Covers, Load all 6 family JSON files, returning {family: data}., Flat dict of all {fault_id: node} across all 6 files., test_all_fault_ids_present(), test_all_nodes_validate_against_schema() (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.11
Nodes (17): coil_arc_under_load(), cold_engine(), hpfp_leak_signature(), legacy_missing_trims(), no_obd_channel(), Mock OBD Live Lab payload builders.  Until the real OBD Live Lab ships, tests us, Engine not yet at operating temperature -- triggers FATAL_INCOMPLETE., Warm engine, neutral fuel trims, healthy VE, all gates valid. (+9 more)

### Community 14 - "Community 14"
Cohesion: 0.25
Nodes (13): in_memory_exporter(), _make_sanitized(), _otel_env_set(), _reset_tracer(), router(), _spans_by_name(), test_prune_emits_rule_pruned_events(), test_rank_emits_rule_scored_events() (+5 more)

### Community 15 - "Community 15"
Cohesion: 0.23
Nodes (12): _make_request(), _o2_circuit_dtc(), Real-routing tests for sensor_fault registry rules — T-P6-11.  Verifies that new, ERR-SF-001 fires via O2_SENSOR_BIASED_LOW perception flag.      OBD lambda (0.88, ERR-SF-002 wins over ERR-SF-001 when both routing_tag AND     perception_flag co, P0134 (O2 circuit no activity) + O2_HISTORY routing tag., ERR-SF-002 fires via O2_HISTORY routing tag + P0134 circuit DTC.      GASLab see, ERR-SF-001 fires via O2_SENSOR_BIASED_HIGH perception flag.      OBD lambda (1.1 (+4 more)

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (10): main(), _map_node(), _parse_frontmatter(), Wiki YAML frontmatter -> KG JSON extraction + validation script.  One-shot: pars, Validate a written KG JSON file against _kg_schema.json.      Returns a list of, COMLab repo root (parent of scripts/)., Extract YAML frontmatter between first --- and second --- fences.      Returns N, Map wiki YAML frontmatter -> KGNode dict.      Returns (fault_id, node_dict). Ra (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.24
Nodes (5): _load_schema(), Unit tests for comlab.schemas.kg + comlab/config/kg/_kg_schema.json.  Covers the, test_json_schema_rejects_overlong_mechanical_failure_mode(), test_json_schema_rejects_unknown_fault_family(), test_json_schema_validates_good_file()

### Community 18 - "Community 18"
Cohesion: 0.2
Nodes (5): hpfp_leak_payload(), modern_vin(), Shared pytest configuration + fixtures for ComLab tests.  Exposes the mock paylo, Example Euro 5/6 VIN used in the BP test harness., Full ingestion payload for the GDI HPFP seal leak scenario.      This is the can

### Community 19 - "Community 19"
Cohesion: 0.2
Nodes (9): T-W-ARCH-6: assert explicit ``use_v2_registry`` selects the intended engine.  Ve, Explicit use_v2_registry=True sets the v2 flag., Explicit use_v2_registry=False sets the v1 (legacy) flag., Without an explicit arg the router defaults to REG-V2., Explicit arg wins over any USE_V2_REGISTRY env value., test_default_is_v2(), test_env_var_does_not_override_explicit(), test_use_v2_registry_false_selects_v1_path() (+1 more)

### Community 20 - "Community 20"
Cohesion: 0.33
Nodes (4): test_4cyl_single_misfire_yields_23pct(), test_8cyl_same_chemistry_yields_half_the_loss(), test_analytics_module_imports(), test_partial_combustion_yields_intermediate_loss()

### Community 21 - "Community 21"
Cohesion: 0.33
Nodes (5): Vocabulary drift guard.  Verifies that every enum value in ``comlab/schemas/voca, DTC_REGEX must match the wiki §2.3 canonical form., Every enum value must appear verbatim in its cited wiki section., test_dtc_regex_matches_wiki(), test_wiki_drift_guard()

### Community 22 - "Community 22"
Cohesion: 0.67
Nodes (1): One-shot CLI demo runner for ComLab.  Usage (after phase 5):     python scripts/

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): ComLab — orchestrator layer of the 4DLab diagnostic app.  ComLab is the determin

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): ComLab analytics — scale-independent calculators.

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): ComLab core — the three routing scripts.

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): COMLab Diagnostic Logic

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): COMLab DNA Architecture

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): COMLab Horizon Eras

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): COMLab Lab Input Reference

## Knowledge Gaps
- **104 isolated node(s):** `ComLab — orchestrator layer of the 4DLab diagnostic app.  ComLab is the determin`, `ComLab analytics — scale-independent calculators.`, `ComLab core — the three routing scripts.`, `Idempotent, env-gated OpenTelemetry tracer for COMLab.  Mirror of `4DLabWired/_j`, `No-op span implementing the subset of the OTel Span API used by COMLab.      Eve` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (24 nodes): `TestOperatorEvaluator`, `.test_deviates_from_target_explicit_tolerance()`, `.test_deviates_from_target_scalar()`, `.test_deviates_from_target_within_tolerance()`, `.test_equals_match()`, `.test_equals_mismatch()`, `.test_greater_than_equal_is_false()`, `.test_greater_than_false()`, `.test_greater_than_or_equal_above()`, `.test_greater_than_or_equal_below()`, `.test_greater_than_or_equal_match()`, `.test_greater_than_true()`, `.test_in_range_above()`, `.test_in_range_below()`, `.test_in_range_boundary()`, `.test_in_range_inside()`, `.test_less_than_false()`, `.test_less_than_or_equal_above()`, `.test_less_than_or_equal_below()`, `.test_less_than_or_equal_match()`, `.test_less_than_true()`, `.test_list_runtime_value_returns_false()`, `.test_none_runtime_value_returns_false()`, `.test_unknown_operator_returns_false()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (3 nodes): `main()`, `run_pipeline_demo.py`, `One-shot CLI demo runner for ComLab.  Usage (after phase 5):     python scripts/`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (2 nodes): `__init__.py`, `ComLab — orchestrator layer of the 4DLab diagnostic app.  ComLab is the determin`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (2 nodes): `ComLab analytics — scale-independent calculators.`, `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (2 nodes): `__init__.py`, `ComLab core — the three routing scripts.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `COMLab Diagnostic Logic`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `COMLab DNA Architecture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `COMLab Horizon Eras`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `COMLab Lab Input Reference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FaultAtlasKG` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 5`, `Community 10`, `Community 14`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `DownstreamTrimRole` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `OrchestratorInboundRequest` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 5`, `Community 10`, `Community 14`, `Community 15`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 290 inferred relationships involving `OrchestratorInboundRequest` (e.g. with `PowerLossAnalytics` and `Script 4: Power Loss Analytics — the mathematical estimator.  Scale-independent`) actually correct?**
  _`OrchestratorInboundRequest` has 290 INFERRED edges - model-reasoned connections that need verification._
- **Are the 257 inferred relationships involving `FaultAtlasKG` (e.g. with `KGFile` and `KGNode`) actually correct?**
  _`FaultAtlasKG` has 257 INFERRED edges - model-reasoned connections that need verification._
- **Are the 242 inferred relationships involving `VinConfidence` (e.g. with `Pure dict-to-Pydantic projection functions per LLD §5.2.  No I/O, no cross-lab i` and `Derive resolved_horizon from euro_emission_category.      Mapping per COMLab_Hor`) actually correct?**
  _`VinConfidence` has 242 INFERRED edges - model-reasoned connections that need verification._
- **Are the 229 inferred relationships involving `PowerLossAnalytics` (e.g. with `OrchestratorInboundRequest` and `PerformanceAnalytics`) actually correct?**
  _`PowerLossAnalytics` has 229 INFERRED edges - model-reasoned connections that need verification._