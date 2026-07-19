> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 3 Internal Pipeline (7 steps + guarded emitters) · Parent document: HLD_OBDLab.md

## 3. Internal Pipeline (7 steps + guarded emitters)

```
raw_user_inputs + ObdLabDnaView (may be None) + LinearityAccumulator (optional)
       │
  [1]  PIDIngestionValidator.validate_and_convert
       │  Unit conversions: _f→_c, _psi→_kpa, _inhg→_kpa, _lbmin→_gps
       │  Bounds check:     12 fields vs physical_sensor_bounds.json §3.1
       │  DNA-RPM gate:     HIGH strict / PARTIAL log-fallthrough / NONE static
       │  Bank-2 contract:  number_of_banks==1 → shrtft2/longft2 must be None
       │  Maps fuel_system_status, validates per_cylinder_misfire_counts & ltft_cell_vector
       │
  [2]  compute_bucket  (state_bucketing.py, rules from obd_translation_rules.yaml)
       │  COLD_OPEN_LOOP_INVALID (priority 1, ECT<75) | STABILIZED_IDLE |
       │  REGULATORY_HIGH_IDLE | STRESS_IDLE   (default → STABILIZED_IDLE)
       │  Computed early so Physics gates can read rpm_state_bucket (F-O7 fix).
       │
  [3]  SemanticConsistencyChecker.evaluate
       │  Thermal gate:    ECT < 75 → override bucket to COLD_OPEN_LOOP_INVALID, engine_warmed=False
       │  Physics_Gate_1:  VSS > 10 AND RPM < 400 → SemanticConsistencyError
       │  Physics_Gate_2:  ECT ≥ 80 AND fuel_status == OL → SemanticConsistencyError
       │  Physics_Gate_4:  trim outside [-127, 127] → SemanticConsistencyError
       │  Closed-loop gate: ECT ≥ 75 AND fuel_status != CL → trim_analytics_suspect (non-blocking)
       │  (Physics_Gate_3 was REMOVED — FIX-1 Option B; superseded by FAULT_VE_SENSOR_SKEW)
       │
  thermal override → analytics_frozen = (bucket == COLD_OPEN_LOOP_INVALID)
       │
  [4]  VEEngine.compute_ve            (frozen → ve_pct=0.0, ve_validity=UNKNOWN)
  [5]  O2Normalizer.normalize         (frozen → normalized_obd_lambda=1.0, NO_FAULT)
  [6]  TrimVectorAggregator.aggregate (frozen → totals 0.0, bank-2/delta None)
       │
  [7]  AnalyticsPreconditions.evaluate  (ALWAYS runs, even when frozen)
       │  8 gates in priority order → TrimAnalyticsGate
       │
  guarded emitters (only when not frozen + guard satisfied):
       │  lambda_perception_delta — WIDEBAND_LINEAR + commanded_equivalence_ratio (PID 0x44)
       │  w_theo / sensor_error_delta — DUAL strategy + two-point accumulator (idle + stress bands)
       │
  ASSEMBLE OBDLivePayload (31 fields)
```

The thermal gate at step [3] freezes steps [4]–[6] (analytics frozen) but step
[7] still runs to populate `trim_analytics_gate`.

## Graph relations (explicit)

**PIDIngestionValidator.validate_and_convert** ROUTES_TO **step [1]** — unit conversion + bounds + DNA-RPM
**compute_bucket** ROUTES_TO **step [2]** — RPM state computed BEFORE semantics (F-O7)
**SemanticConsistencyChecker.evaluate** ROUTES_TO **step [3]** — Physics Gates 1/2/4 + thermal + closed-loop
**VEEngine.compute_ve** ROUTES_TO **step [4]** — VE computation (3-branch)
**O2Normalizer.normalize** ROUTES_TO **step [5]** — lambda normalisation + O2FailureMode
**TrimVectorAggregator.aggregate** ROUTES_TO **step [6]** — STFT+LTFT totals + per-bank delta
**AnalyticsPreconditions.evaluate** ROUTES_TO **step [7]** — trim analytics gate (8 gates)
**Physics_Gate_3** SUPERSEDES **FAULT_VE_SENSOR_SKEW** (FIX-1 Option B)
**COMLab** CONSUMES **OBDLivePayload** (31 fields, frozen contract)
