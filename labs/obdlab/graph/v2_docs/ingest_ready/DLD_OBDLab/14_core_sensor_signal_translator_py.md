> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 14 core/sensor_signal_translator.py · Parent document: DLD_OBDLab.md

## 14. `core/sensor_signal_translator.py` — `SensorSignalTranslator`

Public entry point `translate(raw_user_inputs, dna_view=None, accumulator=None)
→ OBDLivePayload`. Wires steps [1]–[7] (HLD §3), applies the thermal
freeze, computes guarded emitters (`lambda_perception_delta`, `w_theo`,
`sensor_error_delta`), and assembles the 31-field payload. `LinearityAccumulator`
is a small holder for the two idle/stress bands used by MAF linearity.

## Graph relations (explicit)

**SensorSignalTranslator.translate** DESCRIBES **OBDLab public entry point** (7-step orchestrator)
**SensorSignalTranslator.translate** CONSUMES **PIDIngestionValidator, compute_bucket, SemanticConsistencyChecker, VEEngine, O2Normalizer, TrimVectorAggregator, AnalyticsPreconditions** (step [1]–[7])
**SensorSignalTranslator.translate** CONSUMES **ObdLabDnaView** (may be None)
**SensorSignalTranslator.translate** CONSUMES **LinearityAccumulator** (optional, two-point MAF linearity)
**SensorSignalTranslator.translate** DERIVED_FROM **OBDLivePayload** (31-field assembly)
**SensorSignalTranslator.translate** GATED_BY **thermal freeze** (bucket == COLD_OPEN_LOOP_INVALID → analytics frozen)
**test_sensor_signal_translator.py** VERIFIES **SensorSignalTranslator** (unit + integration tests)
