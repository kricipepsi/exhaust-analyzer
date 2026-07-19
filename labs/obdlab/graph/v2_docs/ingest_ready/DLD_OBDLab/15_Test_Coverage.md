> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 15 Test Coverage (current) · Parent document: DLD_OBDLab.md

## 15. Test Coverage (current)

### Entity: Test coverage by area

- **Unit — per module** — `test_payload`, `test_dna_view`, `test_vocabulary`, `test_sensor_bounds`, `test_pid_ingestion_validator`, `test_semantic_consistency_checker`, `test_state*`, `test_ve_engine`, `test_o2_normalizer`, `test_trim_vector_aggregator`, `test_maf_linearity`, `test_analytics_preconditions`, `test_sensor_signal_translator`
- **Unit — emitter channels** — `test_ecu_perception_delta`, `test_bank_asym`
- **Integration** — `test_pipeline_smoke`
- **PID-logset gate** — `test_pid_logset_wiring_gate` (un-quarantine proof)
- **Regression** — `test_obdlab_regression` (JSON fixtures)
- **Generative** — `test_boundary`, `test_combinatorial`, `test_fuzz`, `test_noise`, `test_overlap`

Latest inner loop (T-KG-OBD-2-PREP): ruff + pyright clean, `pytest` 384 passed /
6 skipped.

## Graph relations (explicit)

**test_payload.py** VERIFIES **OBDLivePayload** (schema contract)
**test_dna_view.py** VERIFIES **ObdLabDnaView** (schema contract + import isolation)
**test_vocabulary.py** VERIFIES **vocabulary.py** (8 StrEnums + HIGH_IDLE_LOAD scan)
**test_sensor_bounds.py** VERIFIES **physical_sensor_bounds.json ↔ OBDLab_KG_Wiki.md §3.1** (drift guard)
**test_pid_ingestion_validator.py** VERIFIES **PIDIngestionValidator** (unit)
**test_semantic_consistency_checker.py** VERIFIES **SemanticConsistencyChecker** (unit)
**test_ve_engine.py** VERIFIES **VEEngine** (unit)
**test_o2_normalizer.py** VERIFIES **O2Normalizer** (unit)
**test_trim_vector_aggregator.py** VERIFIES **TrimVectorAggregator** (unit)
**test_maf_linearity.py** VERIFIES **maf_linearity helpers** (unit)
**test_analytics_preconditions.py** VERIFIES **AnalyticsPreconditions** (unit)
**test_sensor_signal_translator.py** VERIFIES **SensorSignalTranslator** (unit + integration)
**test_ecu_perception_delta.py** VERIFIES **lambda_perception_delta** (emitter channel)
**test_bank_asym.py** VERIFIES **per_bank_trim_delta** (emitter channel)
**test_pipeline_smoke.py** VERIFIES **end-to-end pipeline** (integration)
**test_pid_logset_wiring_gate.py** VERIFIES **PID logset** (un-quarantine proof)
**test_obdlab_regression.py** VERIFIES **regression fixtures** (JSON)
