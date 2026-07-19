> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 2 Architecture Position · Parent document: HLD_OBDLab.md

## 2. Architecture Position

```
COMLab (Stage 4 — decision engine)
  │  builds ObdLabDnaView from the VIN/DNA record
  │  populates freeze_frame_pids from DTCLab before calling OBDLab
  ▼
obdlab.SensorSignalTranslator.translate(raw_user_inputs, dna_view, accumulator?)
  │
  ├─ [1] PIDIngestionValidator        — unit conversion + bounds + DNA-RPM + bank-2 contract
  ├─ [2] compute_bucket               — RPM state (runs BEFORE semantics — F-O7)
  ├─ [3] SemanticConsistencyChecker   — Physics Gates 1/2/4 + thermal + closed-loop
  ├─ [4] VEEngine.compute_ve          — volumetric efficiency (3-branch)
  ├─ [5] O2Normalizer.normalize       — lambda from O2 (3-branch) + O2 failure mode
  ├─ [6] TrimVectorAggregator.aggregate — STFT+LTFT totals + per-bank delta
  ├─ [7] AnalyticsPreconditions.evaluate — trim analytics gate (8 gates)
  └─ inline: lambda_perception_delta, w_theo, sensor_error_delta (guarded)
  │
  OBDLivePayload (31 canonical fields)
  │
  ▼
COMLab consumes the payload as a frozen contract surface (see §7).
```

Zero cross-lab Python imports. OBDLab owns local mirrors of any cross-lab type
it needs (e.g. `FuelSystemStatus`, mirrored from DTC_VOCABULARY §8). Isolation
is enforced by an import audit in the test suite.

## Graph relations (explicit)

**SensorSignalTranslator.translate** DESCRIBES **OBDLab 7-step pipeline**
**obdlab** GATED_BY **import-isolation audit** (test_dna_view.py)
**FuelSystemStatus** MIRRORS_CONTRACT_IN **DTC_VOCABULARY §8**
**HLD_OBDLab v2.0** SUPERSEDES **HLD_OBDLab v1.0** (2026-05-22)
