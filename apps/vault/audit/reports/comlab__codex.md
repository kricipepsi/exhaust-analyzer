## Plan

Scope: I picked `T-GTA-COM·codex` (first pending Codex row, unblocked). I will audit `_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml`, classify every `implements` / `consumers` / `drift_guards` edge with `file:line` evidence, write only `apps/vault/audit/reports/comlab__codex.md`, and not edit maps, notes, code, graph artifacts, or other agents’ reports.

## Summary

- Lab: `comlab`.
- Map audited: `_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml`.
- Live frontmatter cross-check: 12 framed notes matched map exactly (scripted YAML compare; zero mismatches).
- Total edges classified: 108.
- LIVE: 99.
- MISLABEL: 2.
- ORPHAN: 1.
- PENDING: 6.
- Seeded case: none assigned to `comlab`; method self-check preserved the taxonomy distinction that pending `T-WIRE-1` edges are PENDING, not ORPHAN.
- Unclassified edges: 0.

## Edge classifications

| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| COMLab_PRD.md | consumers: hld: labs/comlab/docs/COMLab_HLD.md | LIVE | labs/comlab/docs/COMLab_HLD.md:1 frontmatter/doc exists | None. |
| COMLab_PRD.md | consumers: wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator integration | PENDING | apps/wired/WIRED_PROGRESS.md:27 T-WIRE-1 pending compose-labs task | Keep pending marker until T-WIRE-1 creates composition.py. |
| COMLab_HLD.md | consumers: lld: labs/comlab/docs/COMLab_LLD.md | LIVE | labs/comlab/docs/COMLab_LLD.md:1 frontmatter/doc exists | None. |
| COMLab_HLD.md | consumers: dld: labs/comlab/docs/COMLab_DLD.md | LIVE | labs/comlab/docs/COMLab_DLD.md:1 frontmatter/doc exists | None. |
| COMLab_HLD.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_router.py family-routing architecture | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:917 5-phase triage; :1643 rank by confidence/family | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/core/lab_pipeline_aggregator.py | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:95 class LabPipelineAggregator; :366 process | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/core/fault_atlas_router.py | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:569 class FaultAtlasRouter; :917 execute_triage_loop | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/core/fault_atlas_kg.py | LIVE | labs/comlab/comlab/core/fault_atlas_kg.py:25 class FaultAtlasKG; :58 resolve | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/core/ecu_hardware_checker.py | LIVE | labs/comlab/comlab/core/ecu_hardware_checker.py:28 class ECUHardwareChecker; :31 check | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/core/horizon_context_injector.py | LIVE | labs/comlab/comlab/core/horizon_context_injector.py:42 class HorizonContextInjector; :70 from_vehicle_dna | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/core/perception_contradiction.py | LIVE | labs/comlab/comlab/core/perception_contradiction.py:127 detect; :249 detect_compensated_rich | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/core/symptom_router.py | LIVE | labs/comlab/comlab/core/symptom_router.py:38 route_symptom | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/analytics/delta_engine.py | LIVE | labs/comlab/comlab/analytics/delta_engine.py:153 class DeltaEngine; :199 compute_delta_signature | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/analytics/power_loss_analytics.py | LIVE | labs/comlab/comlab/analytics/power_loss_analytics.py:28 class PowerLossAnalytics; :191 compute | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/projection.py | LIVE | labs/comlab/comlab/projection.py:42 project; :116 project_all | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/schemas/ingestion.py | LIVE | labs/comlab/comlab/schemas/ingestion.py:138 VehicleDNA; :488 OrchestratorInboundRequest | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/schemas/response.py | LIVE | labs/comlab/comlab/schemas/response.py:132 OrchestratorFinalUIOutput | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/schemas/vocabulary.py | LIVE | labs/comlab/comlab/schemas/vocabulary.py:241 ChemicalSignature | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/schemas/lab_dna_views.py | LIVE | labs/comlab/comlab/schemas/lab_dna_views.py:28/49/66/82 DNA views | None. |
| COMLab_LLD.md | implements: labs/comlab/comlab/schemas/kg.py | LIVE | labs/comlab/comlab/schemas/kg.py:42 KGNode | None. |
| COMLab_LLD.md | consumers: dld: labs/comlab/docs/COMLab_DLD.md | LIVE | labs/comlab/docs/COMLab_DLD.md:1 frontmatter/doc exists | None. |
| COMLab_LLD.md | consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py five-phase pipeline implementation | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:366 process; :373-374 Stage A→D flow | None. |
| COMLab_LLD.md | consumers: wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator import | PENDING | apps/wired/WIRED_PROGRESS.md:27 T-WIRE-1 pending composition.py diagnose/import | Keep pending marker until T-WIRE-1 creates composition.py. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:52 aggregator smoke | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_fault_atlas_router.py | LIVE | labs/comlab/tests/unit/test_fault_atlas_router.py:441 registry load; :477 operator evaluator | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_fault_atlas_kg.py | LIVE | labs/comlab/tests/unit/test_fault_atlas_kg.py:54 resolve; :93 node count | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_ecu_hardware_checker.py | LIVE | labs/comlab/tests/unit/test_ecu_hardware_checker.py:96 schema bounds; :130 checker unit | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_horizon_context_injector.py | LIVE | labs/comlab/tests/unit/test_horizon_context_injector.py:95 from_vehicle_dna | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_perception_contradiction.py | LIVE | labs/comlab/tests/unit/test_perception_contradiction.py:25 detect; :197 select lambda | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_symptom_router.py | LIVE | labs/comlab/tests/unit/test_symptom_router.py:27 routing table | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_delta_engine.py | LIVE | labs/comlab/tests/unit/test_delta_engine.py:148 sentinel; :211 architecture gate | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_power_loss_analytics.py | LIVE | labs/comlab/tests/unit/test_power_loss_analytics.py:14 kinetic loss; :49 compute cat index | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_projection.py | LIVE | labs/comlab/tests/unit/test_projection.py:111 project gas; :183 project_all | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/unit/test_vocabulary.py | LIVE | labs/comlab/tests/unit/test_vocabulary.py:95 enum drift guard | None. |
| COMLab_LLD.md | drift_guards: labs/comlab/tests/e2e/test_diagnostic_engine.py | LIVE | labs/comlab/tests/e2e/test_diagnostic_engine.py:65/79/93 e2e diagnostic cases | None. |
| COMLab_DLD.md | implements: labs/comlab/comlab/core/lab_pipeline_aggregator.py | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:95 class LabPipelineAggregator; :366 process | None. |
| COMLab_DLD.md | implements: labs/comlab/comlab/core/fault_atlas_router.py | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:569 class FaultAtlasRouter; :917 execute_triage_loop | None. |
| COMLab_DLD.md | implements: labs/comlab/comlab/core/fault_atlas_kg.py | LIVE | labs/comlab/comlab/core/fault_atlas_kg.py:25 class FaultAtlasKG; :58 resolve | None. |
| COMLab_DLD.md | implements: labs/comlab/comlab/observability/_tracer.py | LIVE | labs/comlab/comlab/observability/_tracer.py:161 get_tracer | None. |
| COMLab_DLD.md | implements: labs/comlab/comlab/analytics/power_loss_analytics.py | LIVE | labs/comlab/comlab/analytics/power_loss_analytics.py:28 class PowerLossAnalytics; :191 compute | None. |
| COMLab_DLD.md | implements: labs/comlab/comlab/schemas/ingestion.py | LIVE | labs/comlab/comlab/schemas/ingestion.py:138 VehicleDNA; :488 OrchestratorInboundRequest | None. |
| COMLab_DLD.md | implements: labs/comlab/comlab/schemas/response.py | LIVE | labs/comlab/comlab/schemas/response.py:132 OrchestratorFinalUIOutput | None. |
| COMLab_DLD.md | consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py deployment / latency-budget / observability surfaces | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:462-471 router delegation; fault_atlas_router.py:974/976/1038 tracer spans | None. |
| COMLab_DLD.md | consumers: wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator import | PENDING | apps/wired/WIRED_PROGRESS.md:27 T-WIRE-1 pending composition.py diagnose/import | Keep pending marker until T-WIRE-1 creates composition.py. |
| COMLab_DLD.md | drift_guards: labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:52 aggregator smoke | None. |
| COMLab_DLD.md | drift_guards: labs/comlab/tests/unit/test_fatal_gate_wiring.py | LIVE | labs/comlab/tests/unit/test_fatal_gate_wiring.py:96 inert; :153 VIN none fatal | None. |
| COMLab_DLD.md | drift_guards: labs/comlab/tests/e2e/test_pipeline_round_trip.py | LIVE | labs/comlab/tests/e2e/test_pipeline_round_trip.py:59 round-trip; :118 enrichment | None. |
| COMLab_DLD.md | drift_guards: labs/comlab/tests/e2e/test_error_codes.py | LIVE | labs/comlab/tests/e2e/test_error_codes.py:110 contract tests; :257 fatal gates | None. |
| 01_role_boundaries_fusion_spine.md | implements: labs/comlab/comlab/core/fault_atlas_router.py | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:569 class FaultAtlasRouter; :917 execute_triage_loop | None. |
| 01_role_boundaries_fusion_spine.md | implements: labs/comlab/comlab/schemas/ingestion.py | LIVE | labs/comlab/comlab/schemas/ingestion.py:138 VehicleDNA; :488 OrchestratorInboundRequest | None. |
| 01_role_boundaries_fusion_spine.md | consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py .process fusion-spine orchestration | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:366 process; :443 symptom routing; :462 router delegation; :504 output | None. |
| 01_role_boundaries_fusion_spine.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_router.py family-map verdict | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:2093 winner; :2103 KG resolve; :2131-2135 verdict fields | None. |
| 01_role_boundaries_fusion_spine.md | consumers: wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator import | PENDING | apps/wired/WIRED_PROGRESS.md:27 T-WIRE-1 pending composition.py diagnose/import | Keep pending marker until T-WIRE-1 creates composition.py. |
| 01_role_boundaries_fusion_spine.md | drift_guards: labs/comlab/tests/unit/test_fault_atlas_router.py | LIVE | labs/comlab/tests/unit/test_fault_atlas_router.py:441 registry load; :477 operator evaluator | None. |
| 01_role_boundaries_fusion_spine.md | drift_guards: labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:52 aggregator smoke | None. |
| 02_lab_input_contract.md | implements: labs/comlab/comlab/schemas/ingestion.py | LIVE | labs/comlab/comlab/schemas/ingestion.py:138 VehicleDNA; :488 OrchestratorInboundRequest | None. |
| 02_lab_input_contract.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state / total_trim_correction_delta / confirmed_dtcs routing | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:949 chemical_state; :995 confirmed_dtcs; :1238-1243 total_trim fields | None. |
| 02_lab_input_contract.md | consumers: comlab: labs/comlab/comlab/core/ecu_hardware_checker.py vin_dna consumption | MISLABEL | grep no vin_dna/VehicleDNA/RULE_HW_PRUNE matches in ecu_hardware_checker.py; actual check reads OBD rails at ecu_hardware_checker.py:31-69 | Repoint vin_dna consumer to projection.py / horizon_context_injector.py, or relabel this edge to ECU hardware rail evidence. |
| 02_lab_input_contract.md | consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py engine_state ingestion | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:451 route_symptom(request.symptom_dna); symptom_router.py:59-61 reads engine_state/occurs_during | None. |
| 02_lab_input_contract.md | drift_guards: labs/comlab/tests/unit/test_ingestion_high_idle.py | LIVE | labs/comlab/tests/unit/test_ingestion_high_idle.py:11 high-idle schema | None. |
| 02_lab_input_contract.md | drift_guards: labs/comlab/tests/unit/test_fuel_system_gate.py | LIVE | labs/comlab/tests/unit/test_fuel_system_gate.py:72 schema; :131 open-loop demotion | None. |
| 02_lab_input_contract.md | drift_guards: labs/comlab/tests/unit/test_fault_atlas_router.py | LIVE | labs/comlab/tests/unit/test_fault_atlas_router.py:441 registry load; :477 operator evaluator | None. |
| 03_vehicle_dna_pruning.md | implements: labs/comlab/comlab/core/ecu_hardware_checker.py | LIVE | labs/comlab/comlab/core/ecu_hardware_checker.py:28 class ECUHardwareChecker; :31 check | None. |
| 03_vehicle_dna_pruning.md | implements: labs/comlab/comlab/schemas/lab_dna_views.py | LIVE | labs/comlab/comlab/schemas/lab_dna_views.py:28/49/66/82 DNA views | None. |
| 03_vehicle_dna_pruning.md | implements: labs/comlab/comlab/projection.py | LIVE | labs/comlab/comlab/projection.py:42 project; :116 project_all | None. |
| 03_vehicle_dna_pruning.md | consumers: comlab: labs/comlab/comlab/core/ecu_hardware_checker.py RULE_HW_PRUNE (Stage B Pass 2) | ORPHAN | grep no RULE_HW_PRUNE/precondition/DNA-flag reads in ecu_hardware_checker.py; router precondition branch is pass-only at fault_atlas_router.py:901-907 | Do not point RULE_HW_PRUNE at ecu_hardware_checker; implement/repoint a real DNA precondition reader or remove the consumer edge. |
| 03_vehicle_dna_pruning.md | consumers: comlab: labs/comlab/comlab/analytics/delta_engine.py VE polymorph selection | LIVE | labs/comlab/comlab/analytics/delta_engine.py:275-288 architecture gate reads air_metering_strategy; :291-307 returns trim_nulled/trim_inverted | None. |
| 03_vehicle_dna_pruning.md | consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py DNA-confidence degradation | MISLABEL | lab_pipeline_aggregator.py:349-350 reads vin_confidence only for ERR-ABORT-004 NONE; _map_degradation uses symptom directive at :191-196, not DNA confidence/PARTIAL | Relabel to vin_confidence NONE fatal gate/response echo, or implement PARTIAL DNA-confidence degradation before keeping this wording. |
| 03_vehicle_dna_pruning.md | drift_guards: labs/comlab/tests/unit/test_ecu_hardware_checker.py | LIVE | labs/comlab/tests/unit/test_ecu_hardware_checker.py:96 schema bounds; :130 checker unit | None. |
| 03_vehicle_dna_pruning.md | drift_guards: labs/comlab/tests/unit/test_projection.py | LIVE | labs/comlab/tests/unit/test_projection.py:111 project gas; :183 project_all | None. |
| 04_horizon_eras.md | implements: labs/comlab/comlab/core/horizon_context_injector.py | LIVE | labs/comlab/comlab/core/horizon_context_injector.py:42 class HorizonContextInjector; :70 from_vehicle_dna | None. |
| 04_horizon_eras.md | consumers: comlab: labs/comlab/comlab/core/horizon_context_injector.py RULE_HORIZON_PRUNE / era-mask thresholds | LIVE | labs/comlab/comlab/core/horizon_context_injector.py:70 from_vehicle_dna; :77-89 reads resolved_horizon and loads threshold mask | None. |
| 04_horizon_eras.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_router.py per-era RULE_SCORING thresholds | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:847 horizon pruning; :1686 MIN_CONFIDENCE threshold gate | None. |
| 04_horizon_eras.md | drift_guards: labs/comlab/tests/unit/test_horizon_context_injector.py | LIVE | labs/comlab/tests/unit/test_horizon_context_injector.py:95 from_vehicle_dna | None. |
| 05_fault_taxonomy.md | implements: labs/comlab/comlab/core/fault_atlas_router.py | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:569 class FaultAtlasRouter; :917 execute_triage_loop | None. |
| 05_fault_taxonomy.md | implements: labs/comlab/comlab/config/global_fault_registry.json | LIVE | labs/comlab/comlab/config/global_fault_registry.json:1 registry JSON; :7 first rule | None. |
| 05_fault_taxonomy.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_router.py RULE_GAS_ROUTE / taxonomy-table routing | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:883-884 compares row.gas_lab_state to chemical_state; :949 reads chemical_state | None. |
| 05_fault_taxonomy.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_kg.py fault_id enrichment | LIVE | labs/comlab/comlab/core/fault_atlas_kg.py:58 resolve(fault_id); fault_atlas_router.py:2101-2104 resolves winner fault_id | None. |
| 05_fault_taxonomy.md | drift_guards: labs/comlab/tests/unit/test_fault_atlas_router.py | LIVE | labs/comlab/tests/unit/test_fault_atlas_router.py:441 registry load; :477 operator evaluator | None. |
| 05_fault_taxonomy.md | drift_guards: labs/comlab/tests/e2e/test_kg_registry_consistency.py | LIVE | labs/comlab/tests/e2e/test_kg_registry_consistency.py:63 node coverage; :201 signature guard | None. |
| 06_fault_atlas_families.md | implements: labs/comlab/comlab/core/fault_atlas_kg.py | LIVE | labs/comlab/comlab/core/fault_atlas_kg.py:25 class FaultAtlasKG; :58 resolve | None. |
| 06_fault_atlas_families.md | implements: labs/comlab/comlab/config/kg/rich_mixture.json | LIVE | labs/comlab/comlab/config/kg/rich_mixture.json:1 KG family JSON; :5 first node | None. |
| 06_fault_atlas_families.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_kg.py 12-family JSON loading | LIVE | labs/comlab/comlab/core/fault_atlas_kg.py:93-105 iterates kg/*.json; :114-130 loads/validates one family | None. |
| 06_fault_atlas_families.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_router.py family routing | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:982-987 prune candidates; :1675-1682 resolves fault_family for scored rules | None. |
| 06_fault_atlas_families.md | consumers: comlab: labs/comlab/comlab/analytics/delta_engine.py collision-set -> delta motivation | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:1609-1626 consumes delta_signature and kg_node.fault_family via DeltaEngine.apply_rank_score | None. |
| 06_fault_atlas_families.md | drift_guards: labs/comlab/tests/unit/test_fault_atlas_kg.py | LIVE | labs/comlab/tests/unit/test_fault_atlas_kg.py:54 resolve; :93 node count | None. |
| 06_fault_atlas_families.md | drift_guards: labs/comlab/tests/unit/test_kg_schema.py | LIVE | labs/comlab/tests/unit/test_kg_schema.py:49 KGNode schema; :103 JSON schema | None. |
| 06_fault_atlas_families.md | drift_guards: labs/comlab/tests/unit/test_kg_population.py | LIVE | labs/comlab/tests/unit/test_kg_population.py:151 files; :157 node count | None. |
| 07_pipeline_stages.md | implements: labs/comlab/comlab/core/lab_pipeline_aggregator.py | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:95 class LabPipelineAggregator; :366 process | None. |
| 07_pipeline_stages.md | implements: labs/comlab/comlab/core/fault_atlas_router.py | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:569 class FaultAtlasRouter; :917 execute_triage_loop | None. |
| 07_pipeline_stages.md | implements: labs/comlab/comlab/core/fault_atlas_kg.py | LIVE | labs/comlab/comlab/core/fault_atlas_kg.py:25 class FaultAtlasKG; :58 resolve | None. |
| 07_pipeline_stages.md | implements: labs/comlab/comlab/analytics/power_loss_analytics.py | LIVE | labs/comlab/comlab/analytics/power_loss_analytics.py:28 class PowerLossAnalytics; :191 compute | None. |
| 07_pipeline_stages.md | consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py Stage A-D orchestration | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:373-374 Stage A→D docstring; :462-471 delegates B→E router | None. |
| 07_pipeline_stages.md | consumers: comlab: labs/comlab/comlab/analytics/power_loss_analytics.py Stage D severity | LIVE | labs/comlab/comlab/analytics/power_loss_analytics.py:191-200 compute returns PerformanceAnalytics; :233-241 maps severity | None. |
| 07_pipeline_stages.md | consumers: wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator import | PENDING | apps/wired/WIRED_PROGRESS.md:27 T-WIRE-1 pending composition.py diagnose/import | Keep pending marker until T-WIRE-1 creates composition.py. |
| 07_pipeline_stages.md | drift_guards: labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:52 aggregator smoke | None. |
| 07_pipeline_stages.md | drift_guards: labs/comlab/tests/unit/test_fatal_gate_wiring.py | LIVE | labs/comlab/tests/unit/test_fatal_gate_wiring.py:96 inert; :153 VIN none fatal | None. |
| 07_pipeline_stages.md | drift_guards: labs/comlab/tests/unit/test_power_loss_analytics.py | LIVE | labs/comlab/tests/unit/test_power_loss_analytics.py:14 kinetic loss; :49 compute cat index | None. |
| 07_pipeline_stages.md | drift_guards: labs/comlab/tests/e2e/test_diagnostic_engine.py | LIVE | labs/comlab/tests/e2e/test_diagnostic_engine.py:65/79/93 e2e diagnostic cases | None. |
| 10_differential_and_symptom_prior.md | implements: labs/comlab/comlab/core/lab_pipeline_aggregator.py | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:95 class LabPipelineAggregator; :366 process | None. |
| 10_differential_and_symptom_prior.md | implements: labs/comlab/comlab/core/symptom_router.py | LIVE | labs/comlab/comlab/core/symptom_router.py:38 route_symptom | None. |
| 10_differential_and_symptom_prior.md | implements: labs/comlab/comlab/schemas/response.py | LIVE | labs/comlab/comlab/schemas/response.py:132 OrchestratorFinalUIOutput | None. |
| 10_differential_and_symptom_prior.md | consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py CONCEPT_DIFFERENTIAL / RULE_TOPK | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:519-543 resolves KG node and differential siblings; fault_atlas_router.py:1792-1815 builds siblings | None. |
| 10_differential_and_symptom_prior.md | consumers: comlab: labs/comlab/comlab/core/symptom_router.py RULE_SYMPTOM_PRIOR (capped) | LIVE | labs/comlab/comlab/core/fault_atlas_router.py:1073-1103 reads _csv_primary_symptom and applies capped prior; symptom_router.py:38 route_symptom handles routing flags | None. |
| 10_differential_and_symptom_prior.md | consumers: wired (pending T-WIRE-1): apps/wired/wired/composition.py OrchestratorFinalUIOutput rendering | PENDING | apps/wired/WIRED_PROGRESS.md:27 T-WIRE-1 diagnose() returns OrchestratorFinalUIOutput | Keep pending marker until T-WIRE-1 creates composition.py/rendering adapter. |
| 10_differential_and_symptom_prior.md | drift_guards: labs/comlab/tests/unit/test_symptom_router.py | LIVE | labs/comlab/tests/unit/test_symptom_router.py:27 routing table | None. |
| 10_differential_and_symptom_prior.md | drift_guards: labs/comlab/tests/unit/test_symptom_prior.py | LIVE | labs/comlab/tests/unit/test_symptom_prior.py:153 prior lift; :356 table loaded | None. |
| 10_differential_and_symptom_prior.md | drift_guards: labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:52 aggregator smoke | None. |

## Findings

1. `02_lab_input_contract.md` → `ecu_hardware_checker.py vin_dna consumption` is MISLABEL: `ecu_hardware_checker.py` has no `vin_dna` / `VehicleDNA` / `RULE_HW_PRUNE` reads, and `ECUHardwareChecker.check()` only consumes OBD rail evidence (`intake_air_temp_c`, `coolant_temp_c`, `throttle_pos_pct`, `total_trim_correction_delta`, `per_bank_trim_delta`).
2. `03_vehicle_dna_pruning.md` → `ecu_hardware_checker.py RULE_HW_PRUNE (Stage B Pass 2)` is ORPHAN: no hardware-flag precondition pruning is implemented there; the only precondition hook found in `fault_atlas_router.py` is pass-only at lines 901-907.
3. `03_vehicle_dna_pruning.md` → `lab_pipeline_aggregator.py DNA-confidence degradation` is MISLABEL: aggregator reads `vin_confidence` for the `NONE` fatal gate, but `_map_degradation()` derives `GAS_DOMINANT` from the symptom routing directive, not DNA confidence/PARTIAL.

## Verification

- Parsed `vault-map.comlab.yaml` and enumerated 108 edges across 12 framed notes: 40 `implements`, 32 `consumers`, 36 `drift_guards`.
- Compared each framed live note frontmatter under `labs/comlab/docs/` and `labs/comlab/wiki/` against the map: 0 mismatches.
- Confirmed `T-WIRE-1` is a real pending task at `apps/wired/WIRED_PROGRESS.md:27`; all six wired edges classified PENDING, not ORPHAN.
- Confirmed comlab has no seeded validation case in `GRAPH_TRUST_AUDIT.md`; no seeded-case mismatch.
