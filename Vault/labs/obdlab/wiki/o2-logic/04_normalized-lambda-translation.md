---
chunk: o2-logic/04_normalized-lambda-translation
topic: o2-logic
sources:
  - O2logic.md §Scenario-1 step 4 (narrowband step-wise λ)
  - O2logic.md §Scenario-2 (wideband Φ→λ, linear-voltage K_scale)
  - master_o2_sensor_guide.md §3 (Ip ∝ λ−1)
consumer: OBDLab o2_normalizer.py PRODUCES normalized_obd_lambda (range 0.7–1.3); read by COMLab lab_pipeline_aggregator.py (normalized_obd_lambda) and OBDLab family_map.py (lean/rich family selection)
consumer_status: active
related: [[03_failure-modes-taxonomy]], [[05_bias-vs-real-truth-perception]]
---

# Translating O₂ signal → normalized_obd_lambda

OBDLab's `o2_normalizer.py` collapses both sensor families into a single
scalar, `normalized_obd_lambda` (clamped to **0.7–1.3**, OBDLab_KG_Wiki §5),
plus the `o2_failure_mode` and an `O2NormalizationMode`. COMLab's
`lab_pipeline_aggregator.py` and OBDLab's `family_map.py` consume the scalar;
neither reads raw sensor voltage. The translation rule is chosen by sensor type
(`composition.py`, see `01_sensor-types-and-physics`).

## Narrowband — step-wise λ

A narrowband sensor is a switch, not a meter, so it is mapped to a stepped λ
about the 0.45 V stoichiometric threshold:

```
V_upstream > 0.45 V  ⟹  normalized_obd_lambda ≈ 0.97   (rich)
V_upstream < 0.45 V  ⟹  normalized_obd_lambda ≈ 1.03   (lean)
```

Healthy operation oscillates between these steps at the switching frequency in
`01`. The cross-count / switching-frequency check (≥ 8 crossings / 10 s @ 2500
RPM; warm = coolant > 80 °C and closed-loop) is what distinguishes a healthy
oscillation from `SLUGGISH`/`DEAD` (`03_failure-modes-taxonomy`).

## Wideband — linear λ

The reported equivalence ratio Φ converts directly:

```
normalized_obd_lambda = 1 / Φ
```

driven by pump current `Ip ∝ (λ − 1.0)` — positive Ip = lean, negative Ip =
rich (`master_o2_sensor_guide.md §3`). If the platform reports a raw 0–5 V
linear output instead of Φ (e.g. Toyota 3.3 V / Honda 2.5 V stoich baselines),
it maps through the manufacturer scaling constant K_scale:

```
normalized_obd_lambda = Offset_base + K_scale · V_linear
```

K_scale / Offset_base are per-platform constants supplied via DNALab topology,
not invented by OBDLab.

## What does NOT ship here

The wideband **setpoint-offset delta** `Δλ_offset = |λ_obd − 1.0|` and its
`BIASED_OFFSET` assertion (O2logic §Scenario-2 step 4) are a *contradiction*
signal, not a normalization step: they require GASLab `lambda_chem` to confirm
the engine is physically stoichiometric. That cross-lab comparison is the
perception-contradiction path (`05_bias-vs-real-truth-perception`), and
`BIASED_OFFSET` itself has no enum consumer (O2-FU-1). The low-idle/stress-idle
O₂ *deltas* (Δf_O2, ΔV_O2, ΔTI_cat) are deferred to the delta-relations pass
(SWEEP_MANIFEST §7) with consumer PENDING (FU-2) — not chunked here.

Citation: λ-step thresholds and Φ→λ per O2logic.md §Scenario-1/2;
`normalized_obd_lambda` range 0.7–1.3 per labs/obdlab/obdlab/core/o2_normalizer.py
(wiki §5); `Ip ∝ λ−1` per master_o2_sensor_guide.md §3.


## Core Entities

- normalized_obd_lambda, o2_normalizer.py, WIDEBAND_LINEAR, NARROWBAND_0_TO_1V, Ip, K_scale
- COMLab lab_pipeline_aggregator + OBDLab family_map.py (consumer, active)

## Graph relations (explicit)

**o2_normalizer.py** PRODUCES **normalized_obd_lambda** clamped 0.7-1.3
**NARROWBAND_0_TO_1V** MAPS to stepwise lambda about 0.45V
**WIDEBAND_LINEAR** MAPS lambda as 1/Phi via **Ip**
**normalized_obd_lambda** CONSUMED_BY **COMLab lab_pipeline_aggregator** and **family_map.py**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
