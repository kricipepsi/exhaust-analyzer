## Plan

Scope: I picked `T-GTA-OBD·agy` (first pending Antigravity/Agy row, unblocked). I audited `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml`, cross-checked the live frontmatter in `labs/obdlab/docs/` and `labs/obdlab/research/chunks/` after the required live remap (`labs/obdlab/code/` → `labs/obdlab/obdlab/`), classified every `implements` / `consumers` / `drift_guards` edge with file:line evidence, and wrote only this report.

## Summary

- Lab: `obdlab`.
- Map audited: `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml`.
- Live frontmatter cross-check: 11 framed notes matched the map exactly after live-remapping `implements` paths; zero mismatches.
- Total edges classified: 62.
- LIVE: 58.
- MISLABEL: 4.
- ORPHAN: 0.
- PENDING: 0.
- Seeded case: none assigned to `obdlab`; method self-check preserved the taxonomy distinction that a LIVE-but-unwired reader is not ORPHAN.
- Unclassified edges: 0.

## Findings

- `delta-relations/README.md` consumer `comlab: labs/comlab/comlab/analytics/power_loss_analytics.py — lambda-delta-vector scoring` is MISLABEL: the cross-operating-point delta calculator and scoring logic is implemented in `comlab/analytics/delta_engine.py` (which differences low-idle and second operating point frames), not `power_loss_analytics.py`.
- `delta-relations/README.md` consumer `comlab: labs/comlab/comlab/core/perception_contradiction.py` is MISLABEL: `perception_contradiction.py` only computes the single-point perception contradiction delta and does not consume cross-state delta relations; the real consumer of the cross-operating-point delta is `comlab/analytics/delta_engine.py`.
- `taxonomy/README.md` consumer `comlab: labs/comlab/comlab/core/symptom_router.py — era/emission symptom-prior routing` is MISLABEL: `symptom_router.py` does not perform era/emission standard DNA routing (it only routes based on `engine_state` and `occurs_during`). The real era/horizon mask loading and era-bounded checks occur in `comlab/core/horizon_context_injector.py` and `comlab/core/fault_atlas_router.py`.
- `truth-perception/README.md` consumer `comlab: labs/comlab/comlab/core/symptom_router.py — symptom prior` is MISLABEL: `symptom_router.py` does not read truth-vs-perception or sensor-bias values; the truth-vs-perception override and perception contradiction checks are handled in `comlab/core/fault_atlas_router.py` and `comlab/core/lab_pipeline_aggregator.py`.

## Edge classifications

| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| PRD_OBDLab.md | consumers: hld: labs/obdlab/docs/HLD_OBDLab.md | LIVE | labs/obdlab/docs/HLD_OBDLab.md:1 frontmatter/doc exists | None. |
| HLD_OBDLab.md | consumers: lld: labs/obdlab/docs/LLD_OBDLab.md | LIVE | labs/obdlab/docs/LLD_OBDLab.md:1 frontmatter/doc exists | None. |
| HLD_OBDLab.md | consumers: dld: labs/obdlab/docs/DLD_OBDLab.md | LIVE | labs/obdlab/docs/DLD_OBDLab.md:1 frontmatter/doc exists | None. |
| LLD_OBDLab.md | implements: labs/obdlab/code/core/ve_engine.py → labs/obdlab/obdlab/core/ve_engine.py | LIVE | labs/obdlab/obdlab/core/ve_engine.py:16 class VEEngine; :32 function calculate_volumetric_efficiency | None. |
| LLD_OBDLab.md | implements: labs/obdlab/code/core/o2_normalizer.py → labs/obdlab/obdlab/core/o2_normalizer.py | LIVE | labs/obdlab/obdlab/core/o2_normalizer.py:11 function normalize_o2_voltage | None. |
| LLD_OBDLab.md | implements: labs/obdlab/code/core/trim_vector_aggregator.py → labs/obdlab/obdlab/core/trim_vector_aggregator.py | LIVE | labs/obdlab/obdlab/core/trim_vector_aggregator.py:12 function aggregate_trims | None. |
| LLD_OBDLab.md | consumers: dld: labs/obdlab/docs/DLD_OBDLab.md | LIVE | labs/obdlab/docs/DLD_OBDLab.md:1 frontmatter/doc exists | None. |
| LLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_ve_engine.py | LIVE | labs/obdlab/tests/unit/test_ve_engine.py:11 function test_ve_calculation | None. |
| LLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_o2_normalizer.py | LIVE | labs/obdlab/tests/unit/test_o2_normalizer.py:12 function test_voltage_out_of_bounds | None. |
| LLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_trim_vector_aggregator.py | LIVE | labs/obdlab/tests/unit/test_trim_vector_aggregator.py:12 function test_trim_aggregation_symmetric | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/core/analytics_preconditions.py → labs/obdlab/obdlab/core/analytics_preconditions.py | LIVE | labs/obdlab/obdlab/core/analytics_preconditions.py:15 function check_preconditions | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/core/maf_linearity.py → labs/obdlab/obdlab/core/maf_linearity.py | LIVE | labs/obdlab/obdlab/core/maf_linearity.py:14 function check_maf_linearity | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/core/o2_normalizer.py → labs/obdlab/obdlab/core/o2_normalizer.py | LIVE | labs/obdlab/obdlab/core/o2_normalizer.py:11 function normalize_o2_voltage | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/core/pid_ingestion_validator.py → labs/obdlab/obdlab/core/pid_ingestion_validator.py | LIVE | labs/obdlab/obdlab/core/pid_ingestion_validator.py:15 class PIDIngestionValidator | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/core/semantic_consistency_checker.py → labs/obdlab/obdlab/core/semantic_consistency_checker.py | LIVE | labs/obdlab/obdlab/core/semantic_consistency_checker.py:15 class SemanticConsistencyChecker | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/core/sensor_signal_translator.py → labs/obdlab/obdlab/core/sensor_signal_translator.py | LIVE | labs/obdlab/obdlab/core/sensor_signal_translator.py:11 function translate_signals | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/core/state_bucketing.py → labs/obdlab/obdlab/core/state_bucketing.py | LIVE | labs/obdlab/obdlab/core/state_bucketing.py:12 function bucket_operating_state | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/core/trim_vector_aggregator.py → labs/obdlab/obdlab/core/trim_vector_aggregator.py | LIVE | labs/obdlab/obdlab/core/trim_vector_aggregator.py:12 function aggregate_trims | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/core/ve_engine.py → labs/obdlab/obdlab/core/ve_engine.py | LIVE | labs/obdlab/obdlab/core/ve_engine.py:16 class VEEngine | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/schemas/dna_view.py → labs/obdlab/obdlab/schemas/dna_view.py | LIVE | labs/obdlab/obdlab/schemas/dna_view.py:11 class OBDDnaView | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/schemas/payload.py → labs/obdlab/obdlab/schemas/payload.py | LIVE | labs/obdlab/obdlab/schemas/payload.py:12 class OBDLiveDataPayload | None. |
| DLD_OBDLab.md | implements: labs/obdlab/code/schemas/vocabulary.py → labs/obdlab/obdlab/schemas/vocabulary.py | LIVE | labs/obdlab/obdlab/schemas/vocabulary.py:11 class O2FailureMode | None. |
| DLD_OBDLab.md | consumers: comlab: fault_atlas fusion (perception channel) | LIVE | labs/comlab/comlab/schemas/ingestion.py:497 obd_live_data: OBDLiveDataPayload; fault_atlas_router.py:1238-1245 reads normalized_obd_lambda/total_trim_correction_delta | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_analytics_preconditions.py | LIVE | labs/obdlab/tests/unit/test_analytics_preconditions.py:11 function test_preconditions_valid | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_maf_linearity.py | LIVE | labs/obdlab/tests/unit/test_maf_linearity.py:11 function test_maf_linear | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_o2_normalizer.py | LIVE | labs/obdlab/tests/unit/test_o2_normalizer.py:12 function test_voltage_out_of_bounds | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_pid_ingestion_validator.py | LIVE | labs/obdlab/tests/unit/test_pid_ingestion_validator.py:12 function test_validator_valid_payload | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_semantic_consistency_checker.py | LIVE | labs/obdlab/tests/unit/test_semantic_consistency_checker.py:12 function test_consistency_check_passed | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_sensor_signal_translator.py | LIVE | labs/obdlab/tests/unit/test_sensor_signal_translator.py:12 function test_translation_valid | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_trim_vector_aggregator.py | LIVE | labs/obdlab/tests/unit/test_trim_vector_aggregator.py:12 function test_trim_aggregation_symmetric | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_ve_engine.py | LIVE | labs/obdlab/tests/unit/test_ve_engine.py:11 function test_ve_calculation | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_dna_view.py | LIVE | labs/obdlab/tests/unit/test_dna_view.py:12 function test_dna_view_defaults | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_payload.py | LIVE | labs/obdlab/tests/unit/test_payload.py:12 function test_payload_validation | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/unit/test_vocabulary.py | LIVE | labs/obdlab/tests/unit/test_vocabulary.py:11 function test_vocabulary_enums | None. |
| DLD_OBDLab.md | drift_guards: labs/obdlab/tests/integration/test_pipeline_smoke.py | LIVE | labs/obdlab/tests/integration/test_pipeline_smoke.py:12 function test_pipeline_happy_path | None. |
| o2-logic/README.md | implements: labs/obdlab/code/core/o2_normalizer.py → labs/obdlab/obdlab/core/o2_normalizer.py | LIVE | labs/obdlab/obdlab/core/o2_normalizer.py:11 function normalize_o2_voltage | None. |
| o2-logic/README.md | consumers: comlab: labs/comlab/comlab/core/perception_contradiction.py — O2/lambda bias-vs-truth comparison | LIVE | labs/comlab/comlab/core/perception_contradiction.py:101-124 selects lambda_measured when OBD lambda absent; :127-180 compares perceived vs true lambda | None. |
| o2-logic/README.md | consumers: comlab: labs/comlab/comlab/analytics/power_loss_analytics.py — mixture scoring | LIVE | labs/comlab/comlab/analytics/power_loss_analytics.py:111-137 derive_pre_cat_lambda checks narrowband voltage vs wideband lambda | None. |
| o2-logic/README.md | drift_guards: labs/obdlab/tests/unit/test_o2_normalizer.py | LIVE | labs/obdlab/tests/unit/test_o2_normalizer.py:12 function test_voltage_out_of_bounds | None. |
| fuel-trim/README.md | implements: labs/obdlab/code/core/trim_vector_aggregator.py → labs/obdlab/obdlab/core/trim_vector_aggregator.py | LIVE | labs/obdlab/obdlab/core/trim_vector_aggregator.py:12 function aggregate_trims | None. |
| fuel-trim/README.md | consumers: comlab: labs/comlab/comlab/core/perception_contradiction.py — Total Fuel Trim evaluation | LIVE | labs/comlab/comlab/core/perception_contradiction.py:251-288 evaluates total_trim_correction_delta against -15% railed limit | None. |
| fuel-trim/README.md | consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py — OBD payload intake | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:430-432 extracts total_trim_correction_delta from obd_live_data | None. |
| fuel-trim/README.md | drift_guards: labs/obdlab/tests/unit/test_trim_vector_aggregator.py | LIVE | labs/obdlab/tests/unit/test_trim_vector_aggregator.py:12 function test_trim_aggregation_symmetric | None. |
| delta-relations/README.md | implements: labs/obdlab/code/core/ve_engine.py → labs/obdlab/obdlab/core/ve_engine.py | LIVE | labs/obdlab/obdlab/core/ve_engine.py:16 class VEEngine; :32 function calculate_volumetric_efficiency | None. |
| delta-relations/README.md | consumers: comlab: labs/comlab/comlab/analytics/power_loss_analytics.py — lambda-delta-vector scoring | MISLABEL | `power_loss_analytics.py` only computes static kinetics/catalyst indexes; the cross-operating-point delta engine calculations live in `comlab/analytics/delta_engine.py` | Relabel consumer path to `comlab/analytics/delta_engine.py`. |
| delta-relations/README.md | consumers: comlab: labs/comlab/comlab/core/perception_contradiction.py | MISLABEL | `perception_contradiction.py` handles single-point contradiction check; the cross-operating-point delta engine calculations live in `comlab/analytics/delta_engine.py` | Relabel consumer path to `comlab/analytics/delta_engine.py` or remove if redundant with the delta engine. |
| delta-relations/README.md | drift_guards: labs/obdlab/tests/unit/test_ve_engine.py | LIVE | labs/obdlab/tests/unit/test_ve_engine.py:11 function test_ve_calculation | None. |
| ecu-diagnosis/README.md | implements: labs/obdlab/code/core/semantic_consistency_checker.py → labs/obdlab/obdlab/core/semantic_consistency_checker.py | LIVE | labs/obdlab/obdlab/core/semantic_consistency_checker.py:15 class SemanticConsistencyChecker | None. |
| ecu-diagnosis/README.md | consumers: comlab: labs/comlab/comlab/core/ecu_hardware_checker.py — ECU driver/rail fault checks | LIVE | labs/comlab/comlab/core/ecu_hardware_checker.py:28 class ECUHardwareChecker; :31 function check; :58-70 performs multi-rail correlation | None. |
| ecu-diagnosis/README.md | drift_guards: labs/obdlab/tests/unit/test_semantic_consistency_checker.py | LIVE | labs/obdlab/tests/unit/test_semantic_consistency_checker.py:12 function test_consistency_check_passed | None. |
| pids-protocol/README.md | implements: labs/obdlab/code/core/pid_ingestion_validator.py → labs/obdlab/obdlab/core/pid_ingestion_validator.py | LIVE | labs/obdlab/obdlab/core/pid_ingestion_validator.py:15 class PIDIngestionValidator | None. |
| pids-protocol/README.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_kg.py — PID/Mode06/readiness fault-atlas keys | LIVE | `fault_atlas_kg.py` loads and parses the JSON files (e.g. `misfire.json`, `ecu_fault.json`) containing PID/Mode06/readiness codes and remediation instructions | None. |
| pids-protocol/README.md | consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py | LIVE | labs/comlab/comlab/core/lab_pipeline_aggregator.py:340 checks if `directive.suppress_obd_live_pids` is true and does validation checks | None. |
| pids-protocol/README.md | drift_guards: labs/obdlab/tests/unit/test_pid_ingestion_validator.py | LIVE | labs/obdlab/tests/unit/test_pid_ingestion_validator.py:12 function test_validator_valid_payload | None. |
| taxonomy/README.md | implements: labs/obdlab/code/schemas/dna_view.py → labs/obdlab/obdlab/schemas/dna_view.py | LIVE | labs/obdlab/obdlab/schemas/dna_view.py:11 class OBDDnaView | None. |
| taxonomy/README.md | consumers: comlab: labs/comlab/comlab/core/symptom_router.py — era/emission symptom-prior routing | MISLABEL | `symptom_router.py` does not perform era/emission standard DNA routing (routes only on `engine_state` and `occurs_during`); real era/horizon checks are in `comlab/core/horizon_context_injector.py` and `comlab/core/fault_atlas_router.py` | Relabel consumer path to `comlab/core/horizon_context_injector.py` and `comlab/core/fault_atlas_router.py`. |
| taxonomy/README.md | consumers: comlab: labs/comlab/comlab/core/fault_atlas_kg.py | LIVE | `fault_atlas_kg.py` loads and validates JSON maps representing the 16 emission-era fault categories | None. |
| taxonomy/README.md | drift_guards: labs/obdlab/tests/unit/test_dna_view.py | LIVE | labs/obdlab/tests/unit/test_dna_view.py:12 function test_dna_view_defaults | None. |
| truth-perception/README.md | implements: labs/obdlab/code/core/sensor_signal_translator.py → labs/obdlab/obdlab/core/sensor_signal_translator.py | LIVE | labs/obdlab/obdlab/core/sensor_signal_translator.py:11 function translate_signals | None. |
| truth-perception/README.md | consumers: comlab: labs/comlab/comlab/core/perception_contradiction.py — truth-vs-perception override core | LIVE | `perception_contradiction.py` defines the core truth-vs-perception comparison and verdict rules | None. |
| truth-perception/README.md | consumers: comlab: labs/comlab/comlab/core/symptom_router.py — symptom prior | MISLABEL | `symptom_router.py` does not consume truth-vs-perception or sensor-bias values; the overrides are evaluated in `comlab/core/fault_atlas_router.py` and `comlab/core/lab_pipeline_aggregator.py` | Relabel consumer path to `comlab/core/fault_atlas_router.py`. |
| truth-perception/README.md | drift_guards: labs/obdlab/tests/unit/test_sensor_signal_translator.py | LIVE | labs/obdlab/tests/unit/test_sensor_signal_translator.py:12 function test_translation_valid | None. |