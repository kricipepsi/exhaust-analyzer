## Plan
Scope: `T-GTA-COM·agy` audits the `comlab` lab vault-map `vault-map.comlab.yaml` located at `/agent_workspace/_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml`. I will classify every framed `consumers`, `drift_guards`, and `implements` edge as LIVE, MISLABEL, ORPHAN, or PENDING, recording the exact `file:line` evidence for each. I will write the report `reports/comlab__agy.md` inside `apps/vault/audit/` and touch nothing else.

## Summary Counts
- **LIVE**: 98
- **MISLABEL**: 3
- **ORPHAN**: 1
- **PENDING**: 6
- **Total Edges**: 108

## Seeded Validation
No seeded validation cases exist for `comlab` in `GRAPH_TRUST_AUDIT.md` (the three seeded cases are for `dtclab` and `dnalab`).

## Audit Table
| Note | Edge Type | Edge | Class | Evidence (file:line) | Proposed Fix |
| --- | --- | --- | --- | --- | --- |
| 01_role_boundaries_fusion_spine.md | implements | labs/comlab/comlab/core/fault_atlas_router.py | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:1` | None |
| 01_role_boundaries_fusion_spine.md | implements | labs/comlab/comlab/schemas/ingestion.py | LIVE | `labs/comlab/comlab/schemas/ingestion.py:1` | None |
| 01_role_boundaries_fusion_spine.md | drift_guards | labs/comlab/tests/unit/test_fault_atlas_router.py | LIVE | `labs/comlab/tests/unit/test_fault_atlas_router.py:1` | None |
| 01_role_boundaries_fusion_spine.md | drift_guards | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | `labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:1` | None |
| 01_role_boundaries_fusion_spine.md | consumers | comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py .process fusion-spine orchestration | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:366` | None |
| 01_role_boundaries_fusion_spine.md | consumers | comlab: labs/comlab/comlab/core/fault_atlas_router.py family-map verdict | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:2133` | None |
| 01_role_boundaries_fusion_spine.md | consumers | wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator import | PENDING | T-WIRE-1 in progress ledger | None |
| 02_lab_input_contract.md | implements | labs/comlab/comlab/schemas/ingestion.py | LIVE | `labs/comlab/comlab/schemas/ingestion.py:1` | None |
| 02_lab_input_contract.md | drift_guards | labs/comlab/tests/unit/test_ingestion_high_idle.py | LIVE | `labs/comlab/tests/unit/test_ingestion_high_idle.py:1` | None |
| 02_lab_input_contract.md | drift_guards | labs/comlab/tests/unit/test_fuel_system_gate.py | LIVE | `labs/comlab/tests/unit/test_fuel_system_gate.py:1` | None |
| 02_lab_input_contract.md | drift_guards | labs/comlab/tests/unit/test_fault_atlas_router.py | LIVE | `labs/comlab/tests/unit/test_fault_atlas_router.py:1` | None |
| 02_lab_input_contract.md | consumers | comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state / total_trim_correction_delta / confirmed_dtcs routing | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:949,1242,995` | None |
| 02_lab_input_contract.md | consumers | comlab: labs/comlab/comlab/core/ecu_hardware_checker.py vin_dna consumption | MISLABEL | `labs/comlab/comlab/core/ecu_hardware_checker.py:1` | Repoint to `labs/comlab/comlab/core/horizon_context_injector.py:75` where `vin_dna` is actually consumed |
| 02_lab_input_contract.md | consumers | comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py engine_state ingestion | MISLABEL | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:1` | Relabel consumer file to `labs/comlab/comlab/core/symptom_router.py:60` |
| 03_vehicle_dna_pruning.md | implements | labs/comlab/comlab/core/ecu_hardware_checker.py | LIVE | `labs/comlab/comlab/core/ecu_hardware_checker.py:1` | None |
| 03_vehicle_dna_pruning.md | implements | labs/comlab/comlab/schemas/lab_dna_views.py | LIVE | `labs/comlab/comlab/schemas/lab_dna_views.py:1` | None |
| 03_vehicle_dna_pruning.md | implements | labs/comlab/comlab/projection.py | LIVE | `labs/comlab/comlab/projection.py:1` | None |
| 03_vehicle_dna_pruning.md | drift_guards | labs/comlab/tests/unit/test_ecu_hardware_checker.py | LIVE | `labs/comlab/tests/unit/test_ecu_hardware_checker.py:1` | None |
| 03_vehicle_dna_pruning.md | drift_guards | labs/comlab/tests/unit/test_projection.py | LIVE | `labs/comlab/tests/unit/test_projection.py:1` | None |
| 03_vehicle_dna_pruning.md | consumers | comlab: labs/comlab/comlab/core/ecu_hardware_checker.py RULE_HW_PRUNE (Stage B Pass 2) | ORPHAN | `labs/comlab/comlab/core/ecu_hardware_checker.py:1` | Candidate pruning is stubbed with `pass` in `labs/comlab/comlab/core/fault_atlas_router.py:904` |
| 03_vehicle_dna_pruning.md | consumers | comlab: labs/comlab/comlab/analytics/delta_engine.py VE polymorph selection | LIVE | `labs/comlab/comlab/analytics/delta_engine.py:288` | None |
| 03_vehicle_dna_pruning.md | consumers | comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py DNA-confidence degradation | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:350` | None |
| 04_horizon_eras.md | implements | labs/comlab/comlab/core/horizon_context_injector.py | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:1` | None |
| 04_horizon_eras.md | drift_guards | labs/comlab/tests/unit/test_horizon_context_injector.py | LIVE | `labs/comlab/tests/unit/test_horizon_context_injector.py:1` | None |
| 04_horizon_eras.md | consumers | comlab: labs/comlab/comlab/core/horizon_context_injector.py RULE_HORIZON_PRUNE / era-mask thresholds | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:75` | None |
| 04_horizon_eras.md | consumers | comlab: labs/comlab/comlab/core/fault_atlas_router.py per-era RULE_SCORING thresholds | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:1241` | None |
| 05_fault_taxonomy.md | implements | labs/comlab/comlab/core/fault_atlas_router.py | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:1` | None |
| 05_fault_taxonomy.md | implements | labs/comlab/comlab/config/global_fault_registry.json | LIVE | `labs/comlab/comlab/config/global_fault_registry.json:1` | None |
| 05_fault_taxonomy.md | drift_guards | labs/comlab/tests/unit/test_fault_atlas_router.py | LIVE | `labs/comlab/tests/unit/test_fault_atlas_router.py:1` | None |
| 05_fault_taxonomy.md | drift_guards | labs/comlab/tests/e2e/test_kg_registry_consistency.py | LIVE | `labs/comlab/tests/e2e/test_kg_registry_consistency.py:1` | None |
| 05_fault_taxonomy.md | consumers | comlab: labs/comlab/comlab/core/fault_atlas_router.py RULE_GAS_ROUTE / taxonomy-table routing | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:726,884` | None |
| 05_fault_taxonomy.md | consumers | comlab: labs/comlab/comlab/core/fault_atlas_kg.py fault_id enrichment | LIVE | `labs/comlab/comlab/core/fault_atlas_kg.py:58` | None |
| 06_fault_atlas_families.md | implements | labs/comlab/comlab/core/fault_atlas_kg.py | LIVE | `labs/comlab/comlab/core/fault_atlas_kg.py:1` | None |
| 06_fault_atlas_families.md | implements | labs/comlab/comlab/config/kg/rich_mixture.json | LIVE | `labs/comlab/comlab/config/kg/rich_mixture.json:1` | None |
| 06_fault_atlas_families.md | drift_guards | labs/comlab/tests/unit/test_fault_atlas_kg.py | LIVE | `labs/comlab/tests/unit/test_fault_atlas_kg.py:1` | None |
| 06_fault_atlas_families.md | drift_guards | labs/comlab/tests/unit/test_kg_schema.py | LIVE | `labs/comlab/tests/unit/test_kg_schema.py:1` | None |
| 06_fault_atlas_families.md | drift_guards | labs/comlab/tests/unit/test_kg_population.py | LIVE | `labs/comlab/tests/unit/test_kg_population.py:1` | None |
| 06_fault_atlas_families.md | consumers | comlab: labs/comlab/comlab/core/fault_atlas_kg.py 12-family JSON loading | LIVE | `labs/comlab/comlab/core/fault_atlas_kg.py:94` | None |
| 06_fault_atlas_families.md | consumers | comlab: labs/comlab/comlab/core/fault_atlas_router.py family routing | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:1079` | None |
| 06_fault_atlas_families.md | consumers | comlab: labs/comlab/comlab/analytics/delta_engine.py collision-set -> delta motivation | LIVE | `labs/comlab/comlab/analytics/delta_engine.py:573` | None |
| 07_pipeline_stages.md | implements | labs/comlab/comlab/core/lab_pipeline_aggregator.py | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:1` | None |
| 07_pipeline_stages.md | implements | labs/comlab/comlab/core/fault_atlas_router.py | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:1` | None |
| 07_pipeline_stages.md | implements | labs/comlab/comlab/core/fault_atlas_kg.py | LIVE | `labs/comlab/comlab/core/fault_atlas_kg.py:1` | None |
| 07_pipeline_stages.md | implements | labs/comlab/comlab/analytics/power_loss_analytics.py | LIVE | `labs/comlab/comlab/analytics/power_loss_analytics.py:1` | None |
| 07_pipeline_stages.md | drift_guards | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | `labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:1` | None |
| 07_pipeline_stages.md | drift_guards | labs/comlab/tests/unit/test_fatal_gate_wiring.py | LIVE | `labs/comlab/tests/unit/test_fatal_gate_wiring.py:1` | None |
| 07_pipeline_stages.md | drift_guards | labs/comlab/tests/unit/test_power_loss_analytics.py | LIVE | `labs/comlab/tests/unit/test_power_loss_analytics.py:1` | None |
| 07_pipeline_stages.md | drift_guards | labs/comlab/tests/e2e/test_diagnostic_engine.py | LIVE | `labs/comlab/tests/e2e/test_diagnostic_engine.py:1` | None |
| 07_pipeline_stages.md | consumers | comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py Stage A-D orchestration | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:373` | None |
| 07_pipeline_stages.md | consumers | comlab: labs/comlab/comlab/analytics/power_loss_analytics.py Stage D severity | LIVE | `labs/comlab/comlab/analytics/power_loss_analytics.py:244` | None |
| 07_pipeline_stages.md | consumers | wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator import | PENDING | T-WIRE-1 in progress ledger | None |
| 10_differential_and_symptom_prior.md | implements | labs/comlab/comlab/core/lab_pipeline_aggregator.py | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:1` | None |
| 10_differential_and_symptom_prior.md | implements | labs/comlab/comlab/core/symptom_router.py | LIVE | `labs/comlab/comlab/core/symptom_router.py:1` | None |
| 10_differential_and_symptom_prior.md | implements | labs/comlab/comlab/schemas/response.py | LIVE | `labs/comlab/comlab/schemas/response.py:1` | None |
| 10_differential_and_symptom_prior.md | drift_guards | labs/comlab/tests/unit/test_symptom_router.py | LIVE | `labs/comlab/tests/unit/test_symptom_router.py:1` | None |
| 10_differential_and_symptom_prior.md | drift_guards | labs/comlab/tests/unit/test_symptom_prior.py | LIVE | `labs/comlab/tests/unit/test_symptom_prior.py:1` | None |
| 10_differential_and_symptom_prior.md | drift_guards | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | `labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:1` | None |
| 10_differential_and_symptom_prior.md | consumers | comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py CONCEPT_DIFFERENTIAL / RULE_TOPK | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:522` | None |
| 10_differential_and_symptom_prior.md | consumers | comlab: labs/comlab/comlab/core/symptom_router.py RULE_SYMPTOM_PRIOR (capped) | MISLABEL | `labs/comlab/comlab/core/symptom_router.py:1` | Relabel consumer file to `labs/comlab/comlab/core/fault_atlas_router.py:1078-1100` |
| 10_differential_and_symptom_prior.md | consumers | wired (pending T-WIRE-1): apps/wired/wired/composition.py OrchestratorFinalUIOutput rendering | PENDING | T-WIRE-1 in progress ledger | None |
| COMLab_DLD.md | implements | labs/comlab/comlab/core/lab_pipeline_aggregator.py | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:1` | None |
| COMLab_DLD.md | implements | labs/comlab/comlab/core/fault_atlas_router.py | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:1` | None |
| COMLab_DLD.md | implements | labs/comlab/comlab/core/fault_atlas_kg.py | LIVE | `labs/comlab/comlab/core/fault_atlas_kg.py:1` | None |
| COMLab_DLD.md | implements | labs/comlab/comlab/observability/_tracer.py | LIVE | `labs/comlab/comlab/observability/_tracer.py:1` | None |
| COMLab_DLD.md | implements | labs/comlab/comlab/analytics/power_loss_analytics.py | LIVE | `labs/comlab/comlab/analytics/power_loss_analytics.py:1` | None |
| COMLab_DLD.md | implements | labs/comlab/comlab/schemas/ingestion.py | LIVE | `labs/comlab/comlab/schemas/ingestion.py:1` | None |
| COMLab_DLD.md | implements | labs/comlab/comlab/schemas/response.py | LIVE | `labs/comlab/comlab/schemas/response.py:1` | None |
| COMLab_DLD.md | drift_guards | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | `labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:1` | None |
| COMLab_DLD.md | drift_guards | labs/comlab/tests/unit/test_fatal_gate_wiring.py | LIVE | `labs/comlab/tests/unit/test_fatal_gate_wiring.py:1` | None |
| COMLab_DLD.md | drift_guards | labs/comlab/tests/e2e/test_pipeline_round_trip.py | LIVE | `labs/comlab/tests/e2e/test_pipeline_round_trip.py:1` | None |
| COMLab_DLD.md | drift_guards | labs/comlab/tests/e2e/test_error_codes.py | LIVE | `labs/comlab/tests/e2e/test_error_codes.py:1` | None |
| COMLab_DLD.md | consumers | comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py deployment / latency-budget / observability surfaces | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:547` | None |
| COMLab_DLD.md | consumers | wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator import | PENDING | T-WIRE-1 in progress ledger | None |
| COMLab_HLD.md | consumers | lld: labs/comlab/docs/COMLab_LLD.md | LIVE | `labs/comlab/docs/COMLab_LLD.md:1` | None |
| COMLab_HLD.md | consumers | dld: labs/comlab/docs/COMLab_DLD.md | LIVE | `labs/comlab/docs/COMLab_DLD.md:1` | None |
| COMLab_HLD.md | consumers | comlab: labs/comlab/comlab/core/fault_atlas_router.py family-routing architecture | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:1079` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/core/lab_pipeline_aggregator.py | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/core/fault_atlas_router.py | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/core/fault_atlas_kg.py | LIVE | `labs/comlab/comlab/core/fault_atlas_kg.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/core/ecu_hardware_checker.py | LIVE | `labs/comlab/comlab/core/ecu_hardware_checker.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/core/horizon_context_injector.py | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/core/perception_contradiction.py | LIVE | `labs/comlab/comlab/core/perception_contradiction.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/core/symptom_router.py | LIVE | `labs/comlab/comlab/core/symptom_router.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/analytics/delta_engine.py | LIVE | `labs/comlab/comlab/analytics/delta_engine.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/analytics/power_loss_analytics.py | LIVE | `labs/comlab/comlab/analytics/power_loss_analytics.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/projection.py | LIVE | `labs/comlab/comlab/projection.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/schemas/ingestion.py | LIVE | `labs/comlab/comlab/schemas/ingestion.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/schemas/response.py | LIVE | `labs/comlab/comlab/schemas/response.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/schemas/vocabulary.py | LIVE | `labs/comlab/comlab/schemas/vocabulary.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/schemas/lab_dna_views.py | LIVE | `labs/comlab/comlab/schemas/lab_dna_views.py:1` | None |
| COMLab_LLD.md | implements | labs/comlab/comlab/schemas/kg.py | LIVE | `labs/comlab/comlab/schemas/kg.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_lab_pipeline_aggregator.py | LIVE | `labs/comlab/tests/unit/test_lab_pipeline_aggregator.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_fault_atlas_router.py | LIVE | `labs/comlab/tests/unit/test_fault_atlas_router.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_fault_atlas_kg.py | LIVE | `labs/comlab/tests/unit/test_fault_atlas_kg.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_ecu_hardware_checker.py | LIVE | `labs/comlab/tests/unit/test_ecu_hardware_checker.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_horizon_context_injector.py | LIVE | `labs/comlab/tests/unit/test_horizon_context_injector.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_perception_contradiction.py | LIVE | `labs/comlab/tests/unit/test_perception_contradiction.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_symptom_router.py | LIVE | `labs/comlab/tests/unit/test_symptom_router.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_delta_engine.py | LIVE | `labs/comlab/tests/unit/test_delta_engine.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_power_loss_analytics.py | LIVE | `labs/comlab/tests/unit/test_power_loss_analytics.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_projection.py | LIVE | `labs/comlab/tests/unit/test_projection.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/unit/test_vocabulary.py | LIVE | `labs/comlab/tests/unit/test_vocabulary.py:1` | None |
| COMLab_LLD.md | drift_guards | labs/comlab/tests/e2e/test_diagnostic_engine.py | LIVE | `labs/comlab/tests/e2e/test_diagnostic_engine.py:1` | None |
| COMLab_LLD.md | consumers | dld: labs/comlab/docs/COMLab_DLD.md | LIVE | `labs/comlab/docs/COMLab_DLD.md:1` | None |
| COMLab_LLD.md | consumers | comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py five-phase pipeline implementation | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:373` | None |
| COMLab_LLD.md | consumers | wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator import | PENDING | T-WIRE-1 in progress ledger | None |
| COMLab_PRD.md | consumers | hld: labs/comlab/docs/COMLab_HLD.md | LIVE | `labs/comlab/docs/COMLab_HLD.md:1` | None |
| COMLab_PRD.md | consumers | wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator integration | PENDING | T-WIRE-1 in progress ledger | None |