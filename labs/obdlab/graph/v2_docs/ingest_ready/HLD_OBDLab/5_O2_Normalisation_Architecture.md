> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 5 O2 Normalisation Architecture · Parent document: HLD_OBDLab.md

## 5. O2 Normalisation Architecture

Three sensor types map to two code paths, producing one unified
`normalized_obd_lambda` in `[0.7, 1.3]` plus an `O2FailureMode`:

```
NARROWBAND_0_TO_1V   ─┐
WIDEBAND_NB_SIM      ─┤→ 3-zone voltage→lambda (reads pid_oxygen_sensor_volts)
                       │    0.10–0.40 V → λ 1.05 (LEAN)
                       │    0.41–0.50 V → λ 1.00 (STOICH)
                       │    0.51–0.90 V → λ 0.95 (RICH)
                       │    < 0.10 V → O2_CHANNEL_FAULT, clamp λ 1.05, STUCK_LEAN
                       │    > 0.90 V → O2_CHANNEL_FAULT, clamp λ 0.95, STUCK_RICH

WIDEBAND_LINEAR      ──→ direct passthrough (reads pid_wideband_equivalence_ratio)
                           0.7 ≤ λ ≤ 1.3 → WIDEBAND_PASSTHROUGH
                           out-of-range → O2_CHANNEL_FAULT, clamp to nearest bound
                           warm + closed-loop + not WOT + not DFCO + |λ−1.0| > 0.05
                              → WIDEBAND_OFFSET_CANDIDATE (proposal EP-OBD-17)
```

### Entity: O2FailureMode taxonomy (4 members)

- **NO_FAULT** — Normal operation, no fault detected
- **STUCK_LEAN** — Narrowband voltage < 0.10 V, λ clamped to 1.05 · **Consumed by:** COMLab `fault_atlas_router` O2 channel
- **STUCK_RICH** — Narrowband voltage > 0.90 V, λ clamped to 0.95 · **Consumed by:** COMLab `fault_atlas_router` O2 channel
- **WIDEBAND_OFFSET_CANDIDATE** — Wideband, warm+CL+not WOT+not DFCO, |λ−1.0| > 0.05 · **Consumed by:** COMLab `T-COMV2-O2OFFSET-1` (S4 forward-reg, proposal EP-OBD-17)

The legacy members `SLUGGISH`/`DEAD`/`WRONG_CENTERLINE`/`HEATER_FAULT` were
pruned (ARCH-2) — they had no consumer.

The wideband branch only flags `WIDEBAND_OFFSET_CANDIDATE`; it never asserts a
verdict. COMLab `T-COMV2-O2OFFSET-1` (Stage 4) is the named consumer.

## Graph relations (explicit)

**O2Normalizer.normalize** ENUMERATES **O2NormalizationMode** (NARROWBAND_VOLTAGE_TO_LAMBDA, WIDEBAND_PASSTHROUGH, WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA, O2_CHANNEL_FAULT)
**O2Normalizer.normalize** ENUMERATES **O2FailureMode** (NO_FAULT, STUCK_LEAN, STUCK_RICH, WIDEBAND_OFFSET_CANDIDATE)
**COMLab T-COMV2-O2OFFSET-1** CONSUMES **o2_failure_mode.WIDEBAND_OFFSET_CANDIDATE** (S4 forward-reg, proposal EP-OBD-17)
**O2FailureMode v2** SUPERSEDES **O2FailureMode v1** (SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT pruned per ARCH-2)
**normalized_obd_lambda** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.4**
