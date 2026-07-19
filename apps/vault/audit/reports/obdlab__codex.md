## Plan

I have selected the lab `obdlab` for task row `T-GTA-OBD·codex` from the progress ledger. I will perform a read-only audit of the framed edges in `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml` against the OBDLab codebase (`labs/obdlab/`) and the ComLab consuming code (`labs/comlab/`). I will classify every edge as LIVE, MISLABEL, ORPHAN, or PENDING based on the presence and correctness of code readers. I will write my findings exclusively to `apps/vault/audit/reports/obdlab__codex.md` and touch no other maps, wiki notes, or codebase files, ensuring strict read-only compliance.

## Summary of Classifications

*   **Total Edges:** 62
*   **LIVE:** 56
*   **MISLABEL:** 5
*   **ORPHAN:** 1
*   **PENDING:** 0

*Seeded Case Verification: Seeded validation cases (none for OBDLab) do not apply, but the method successfully verified all 62 edges independently.*

## Audit Table

| Note | Edge | Class | Evidence (file:line) | Proposed Fix |
|---|---|---|---|---|
| **PRD_OBDLab.md** | `consumers: hld: labs/obdlab/docs/HLD_OBDLab.md` | LIVE | `labs/obdlab/docs/HLD_OBDLab.md` exists and contains HLD specifications mapping back to PRD. | None. |
| **HLD_OBDLab.md** | `consumers: lld: labs/obdlab/docs/LLD_OBDLab.md` | LIVE | `labs/obdlab/docs/LLD_OBDLab.md` exists and details low-level code structure. | None. |
| **HLD_OBDLab.md** | `consumers: dld: labs/obdlab/docs/DLD_OBDLab.md` | LIVE | `labs/obdlab/docs/DLD_OBDLab.md` exists and details module data structures. | None. |
| **LLD_OBDLab.md** | `implements: labs/obdlab/code/core/ve_engine.py` | LIVE | `labs/obdlab/obdlab/core/ve_engine.py` - `class VEEngine:56` | None. |
| **LLD_OBDLab.md** | `implements: labs/obdlab/code/core/o2_normalizer.py` | LIVE | `labs/obdlab/obdlab/core/o2_normalizer.py` - `class O2Normalizer:52` | None. |
| **LLD_OBDLab.md** | `implements: labs/obdlab/code/core/trim_vector_aggregator.py` | LIVE | `labs/obdlab/obdlab/core/trim_vector_aggregator.py` - `class TrimVectorAggregator:17` | None. |
| **LLD_OBDLab.md** | `consumers: dld: labs/obdlab/docs/DLD_OBDLab.md` | LIVE | `labs/obdlab/docs/DLD_OBDLab.md` exists. | None. |
| **LLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_ve_engine.py` | LIVE | `labs/obdlab/tests/unit/test_ve_engine.py` - `def _expected_ve:28` | None. |
| **LLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_o2_normalizer.py` | LIVE | `labs/obdlab/tests/unit/test_o2_normalizer.py` - `def _dna_view:23` | None. |
| **LLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_trim_vector_aggregator.py` | LIVE | `labs/obdlab/tests/unit/test_trim_vector_aggregator.py` - `def test_one_bank_aggregation:12` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/core/analytics_preconditions.py` | LIVE | `labs/obdlab/obdlab/core/analytics_preconditions.py` - `class AnalyticsPreconditions:41` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/core/maf_linearity.py` | LIVE | `labs/obdlab/obdlab/core/maf_linearity.py` - `def calculate_w_theo:13` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/core/o2_normalizer.py` | LIVE | `labs/obdlab/obdlab/core/o2_normalizer.py` - `class O2Normalizer:52` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/core/pid_ingestion_validator.py` | LIVE | `labs/obdlab/obdlab/core/pid_ingestion_validator.py` - `class PIDIngestionValidator:29` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/core/semantic_consistency_checker.py` | LIVE | `labs/obdlab/obdlab/core/semantic_consistency_checker.py` - `class SemanticConsistencyChecker:27` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/core/sensor_signal_translator.py` | LIVE | `labs/obdlab/obdlab/core/sensor_signal_translator.py` - `class LinearityAccumulator:49` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/core/state_bucketing.py` | LIVE | `labs/obdlab/obdlab/core/state_bucketing.py` - `def _load_rules:27` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/core/trim_vector_aggregator.py` | LIVE | `labs/obdlab/obdlab/core/trim_vector_aggregator.py` - `class TrimVectorAggregator:17` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/core/ve_engine.py` | LIVE | `labs/obdlab/obdlab/core/ve_engine.py` - `class VEEngine:56` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/schemas/dna_view.py` | LIVE | `labs/obdlab/obdlab/schemas/dna_view.py` - `class AirMeteringStrategy:13` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/schemas/payload.py` | LIVE | `labs/obdlab/obdlab/schemas/payload.py` - `class OBDLivePayload:24` | None. |
| **DLD_OBDLab.md** | `implements: labs/obdlab/code/schemas/vocabulary.py` | LIVE | `labs/obdlab/obdlab/schemas/vocabulary.py` - `class RpmStateBucket:11` | None. |
| **DLD_OBDLab.md** | `consumers: comlab: fault_atlas fusion (perception channel)` | LIVE | `labs/comlab/comlab/core/fault_atlas_router.py:492` (maps OBD live data fields for constraints checks) and `labs/comlab/comlab/core/lab_pipeline_aggregator.py:340` (intakes OBD live payload). | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_analytics_preconditions.py` | LIVE | `labs/obdlab/tests/unit/test_analytics_preconditions.py` - `def _healthy_pids:18` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_maf_linearity.py` | LIVE | `labs/obdlab/tests/unit/test_maf_linearity.py` - `def _dna_view:19` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_o2_normalizer.py` | LIVE | `labs/obdlab/tests/unit/test_o2_normalizer.py` - `def _dna_view:23` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_pid_ingestion_validator.py` | LIVE | `labs/obdlab/tests/unit/test_pid_ingestion_validator.py` - `def _make_dna:21` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_semantic_consistency_checker.py` | LIVE | `labs/obdlab/tests/unit/test_semantic_consistency_checker.py` - `def _make_dna:14` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_sensor_signal_translator.py` | LIVE | `labs/obdlab/tests/unit/test_sensor_signal_translator.py` - `def _dna_high:35` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_trim_vector_aggregator.py` | LIVE | `labs/obdlab/tests/unit/test_trim_vector_aggregator.py` - `def test_one_bank_aggregation:12` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_ve_engine.py` | LIVE | `labs/obdlab/tests/unit/test_ve_engine.py` - `def _expected_ve:28` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_dna_view.py` | LIVE | `labs/obdlab/tests/unit/test_dna_view.py` - `def _find_comlab_vocab:29` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_payload.py` | LIVE | `labs/obdlab/tests/unit/test_payload.py` - `def _canonical_kwargs:19` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/unit/test_vocabulary.py` | LIVE | `labs/obdlab/tests/unit/test_vocabulary.py` - `def test_wiki_drift_guard:35` | None. |
| **DLD_OBDLab.md** | `drift_guards: labs/obdlab/tests/integration/test_pipeline_smoke.py` | LIVE | `labs/obdlab/tests/integration/test_pipeline_smoke.py` - `def translator:27` | None. |
| **o2-logic/README.md** | `implements: labs/obdlab/code/core/o2_normalizer.py` | LIVE | `labs/obdlab/obdlab/core/o2_normalizer.py` - `class O2Normalizer:52` | None. |
| **o2-logic/README.md** | `consumers: comlab: labs/comlab/comlab/core/perception_contradiction.py — O2/lambda bias-vs-truth comparison` | LIVE | `labs/comlab/comlab/core/perception_contradiction.py:127` (`detect` function compares perceived and chemical lambda). | None. |
| **o2-logic/README.md** | `consumers: comlab: labs/comlab/comlab/analytics/power_loss_analytics.py — mixture scoring` | LIVE | `labs/comlab/comlab/analytics/power_loss_analytics.py:189` (`compute` receives/propagates `lambda_perception_delta` & `o2_sensor_bias_verdict`). | None. |
| **o2-logic/README.md** | `drift_guards: labs/obdlab/tests/unit/test_o2_normalizer.py` | LIVE | `labs/obdlab/tests/unit/test_o2_normalizer.py` - `def _dna_view:23` | None. |
| **fuel-trim/README.md** | `implements: labs/obdlab/code/core/trim_vector_aggregator.py` | LIVE | `labs/obdlab/obdlab/core/trim_vector_aggregator.py` - `class TrimVectorAggregator:17` | None. |
| **fuel-trim/README.md** | `consumers: comlab: labs/comlab/comlab/core/perception_contradiction.py — Total Fuel Trim evaluation` | LIVE | `labs/comlab/comlab/core/perception_contradiction.py:251` (`detect_compensated_rich` evaluates total trim delta). | None. |
| **fuel-trim/README.md** | `consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py — OBD payload intake` | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:431` (retrieves and passes `total_trim_correction_delta` to compensated rich check). | None. |
| **fuel-trim/README.md** | `drift_guards: labs/obdlab/tests/unit/test_trim_vector_aggregator.py` | LIVE | `labs/obdlab/tests/unit/test_trim_vector_aggregator.py` - `def test_one_bank_aggregation:12` | None. |
| **delta-relations/README.md** | `implements: labs/obdlab/code/core/ve_engine.py` | LIVE | `labs/obdlab/obdlab/core/ve_engine.py` - `class VEEngine:56` | None. |
| **delta-relations/README.md** | `consumers: comlab: labs/comlab/comlab/analytics/power_loss_analytics.py — lambda-delta-vector scoring` | MISLABEL | `labs/comlab/comlab/analytics/power_loss_analytics.py` only passes lambda_perception_delta through. The actual delta-relations scoring engine is in `labs/comlab/comlab/analytics/delta_engine.py`. | Repoint edge to `"comlab: labs/comlab/comlab/analytics/delta_engine.py:DeltaEngine"`. |
| **delta-relations/README.md** | `consumers: comlab: labs/comlab/comlab/core/perception_contradiction.py` | ORPHAN | `perception_contradiction.py` has no references to volumetric efficiency or the two-speed delta relations calculation. | Repoint edge to `"comlab: labs/comlab/comlab/core/fault_atlas_router.py"` (the caller of DeltaEngine). |
| **delta-relations/README.md** | `drift_guards: labs/obdlab/tests/unit/test_ve_engine.py` | LIVE | `labs/obdlab/tests/unit/test_ve_engine.py` - `def _expected_ve:28` | None. |
| **ecu-diagnosis/README.md** | `implements: labs/obdlab/code/core/semantic_consistency_checker.py` | LIVE | `labs/obdlab/obdlab/core/semantic_consistency_checker.py` - `class SemanticConsistencyChecker:27` | None. |
| **ecu-diagnosis/README.md** | `consumers: comlab: labs/comlab/comlab/core/ecu_hardware_checker.py — ECU driver/rail fault checks` | LIVE | `labs/comlab/comlab/core/ecu_hardware_checker.py:28` (`check` method) and `labs/comlab/comlab/core/fault_atlas_router.py:1312` (calls the checker with OBD data). | None. |
| **ecu-diagnosis/README.md** | `drift_guards: labs/obdlab/tests/unit/test_semantic_consistency_checker.py` | LIVE | `labs/obdlab/tests/unit/test_semantic_consistency_checker.py` - `def _make_dna:14` | None. |
| **pids-protocol/README.md** | `implements: labs/obdlab/code/core/pid_ingestion_validator.py` | LIVE | `labs/obdlab/obdlab/core/pid_ingestion_validator.py` - `class PIDIngestionValidator:29` | None. |
| **pids-protocol/README.md** | `consumers: comlab: labs/comlab/comlab/core/fault_atlas_kg.py — PID/Mode06/readiness fault-atlas keys` | MISLABEL | `fault_atlas_kg.py` is a simple family loader and contains no registry check rules or PID/Mode06 evaluation logic. The actual check is executed by `labs/comlab/comlab/core/fault_atlas_router.py`. | Repoint edge to `"comlab: labs/comlab/comlab/core/fault_atlas_router.py"`. |
| **pids-protocol/README.md** | `consumers: comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py` | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:340` (checks for active OBD live data suppression). | None. |
| **pids-protocol/README.md** | `drift_guards: labs/obdlab/tests/unit/test_pid_ingestion_validator.py` | LIVE | `labs/obdlab/tests/unit/test_pid_ingestion_validator.py` - `def _make_dna:21` | None. |
| **taxonomy/README.md** | `implements: labs/obdlab/code/schemas/dna_view.py` | LIVE | `labs/obdlab/obdlab/schemas/dna_view.py` - `class AirMeteringStrategy:13` | None. |
| **taxonomy/README.md** | `consumers: comlab: labs/comlab/comlab/core/symptom_router.py — era/emission symptom-prior routing` | MISLABEL | `symptom_router.py` does not route based on era or emissions. The era/emission taxonomy routing is handled by `labs/comlab/comlab/core/horizon_context_injector.py` and `labs/comlab/comlab/core/fault_atlas_router.py`. | Repoint edge to `"comlab: labs/comlab/comlab/core/horizon_context_injector.py"` and `"comlab: labs/comlab/comlab/core/fault_atlas_router.py"`. |
| **taxonomy/README.md** | `consumers: comlab: labs/comlab/comlab/core/fault_atlas_kg.py` | MISLABEL | `fault_atlas_kg.py` contains no era/emission taxonomy checks. Rule filtering by target horizons is done in `labs/comlab/comlab/core/fault_atlas_router.py:837`. | Repoint edge to `"comlab: labs/comlab/comlab/core/fault_atlas_router.py"`. |
| **taxonomy/README.md** | `drift_guards: labs/obdlab/tests/unit/test_dna_view.py` | LIVE | `labs/obdlab/tests/unit/test_dna_view.py` - `def _find_comlab_vocab:29` | None. |
| **truth-perception/README.md** | `implements: labs/obdlab/code/core/sensor_signal_translator.py` | LIVE | `labs/obdlab/obdlab/core/sensor_signal_translator.py` - `class LinearityAccumulator:49` | None. |
| **truth-perception/README.md** | `consumers: comlab: labs/comlab/comlab/core/perception_contradiction.py — truth-vs-perception override core` | LIVE | `labs/comlab/comlab/core/perception_contradiction.py:127` (`detect` compares perceived and chemical lambda). | None. |
| **truth-perception/README.md** | `consumers: comlab: labs/comlab/comlab/core/symptom_router.py — symptom prior` | MISLABEL | `symptom_router.py` has no references to symptom priors. Symptom priors are loaded from `symptom_prior.yaml` and applied in `labs/comlab/comlab/core/fault_atlas_router.py`. | Repoint edge to `"comlab: labs/comlab/comlab/core/fault_atlas_router.py"`. |
| **truth-perception/README.md** | `drift_guards: labs/obdlab/tests/unit/test_sensor_signal_translator.py` | LIVE | `labs/obdlab/tests/unit/test_sensor_signal_translator.py` - `def _dna_high:35` | None. |

