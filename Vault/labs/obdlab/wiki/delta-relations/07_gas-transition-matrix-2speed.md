---
chunk: delta-relations/07_gas-transition-matrix-2speed
topic: delta-relations
sources:
  - various/Vol7.md — "Exhaust Gas Profile Transition Matrix (Low Idle to 2500 RPM)" (25-case GAS-* matrix)
consumer: PENDING (COMLab delta-calculation script — SWEEP_MANIFEST FU-2). The Δgas signatures here are read by the same proposed delta engine that consumes ΔTrim; GASLab is the producer of the per-state 5-gas frame.
consumer_status: PENDING
provenance: sources/various/Vol7.md (gate: prose + numeric tables READABLE; the two display equations — Brettschneider λ and vsum — are stripped, captured separately in delta-relations/08 + formula-wiki pending list)
dedup: complements delta-relations/01-05 (ΔTrim profiles from FuelTrimW.md, OBD-side). THIS is the GAS-side (5-gas tailpipe) Δ across the same low→high idle transition. Stress band here = 2500 RPM (⚠ band conflict with FuelTrimW 3500–4500 — reconcile in FU-2 / O2-FU-3).
---

# Two-speed-idle gas transition matrix (low idle → 2500 RPM)

The diagnostic value of a 5-gas reading is the **change** from curb idle to a
stabilised 2500 RPM (unloaded, neutral), not the single-point value. The transition
mechanism (vacuum-dependent dilution vs speed-dependent intensification) is what
separates faults that read identically at idle.

## Two physical rules that drive every row

1. **Vacuum-dependent / unmetered faults attenuate at 2500 RPM.** Manifold vacuum
   drops (≈18–22 inHg → 10–15 inHg) and metered air-fuel volume rises several-fold,
   so a constant-size leak becomes a negligible fraction. → vacuum leaks, ruptured
   FPR diaphragm, exhaust-leak false-lean all **improve**.
2. **Speed-dependent mechanical / system-action faults intensify at 2500 RPM.** →
   worn rings (oil burn), EVAP purge dump, flat-cam breathing limit, no-EGR NOx
   runaway, weak-coil misfire all **worsen**.

## Distinct Δ-signatures (selected rows; full 25 in source)

| Case | Low idle (HC/CO/CO₂/O₂/λ) | 2500 RPM (HC/CO/CO₂/O₂/λ) | Mechanism |
|---|---|---|---|
| GAS-VAC-001 vacuum-line FPR rupture | 380 / 7.50 / 9.0 / 0.20 / 0.742 | 190 / 2.80 / 12.5 / 0.30 / 0.910 | rich attenuates — lower vacuum cuts leak flow + dilution |
| GAS-LEAN-001 intake vacuum leak | 10 / 0.03 / 7.5 / 8.50 / 2.120 | 8 / 0.05 / 14.8 / 0.40 / 1.010 | lean attenuates — leak negligible vs metered air |
| GAS-EAL-001 pre-cat exhaust leak | 425 / 5.63 / 10.0 / 2.30 / 0.906 | 15 / 0.15 / 15.2 / 0.20 / 1.002 | positive exhaust pressure blocks air ingress; false-rich trim corrects |
| GAS-WPR-001 worn piston rings | 15 / 0.10 / 14.8 / 0.30 / 1.014 | 180 / 0.30 / 14.1 / 0.50 / 1.005 | oil burn **intensifies** — blow-by + ring speed |
| GAS-WVS-001 worn valve seals | 120 / 0.30 / 14.2 / 0.50 / 1.003 | 15 / 0.08 / 15.3 / 0.20 / 1.000 | oil induction **clears** — vacuum drop stops guide pull |
| GAS-FC-001 flat camshaft lobe | 30 / 0.08 / 14.0 / 0.40 / 1.020 | 220 / 0.25 / 12.2 / 2.50 / 1.090 | restricted lift = high-speed breathing misfire |
| GAS-ESC-001 EGR stuck closed | 50 / 0.30 / 15.0 / 0.30 / 1.006 (NOx 1500) | 35 / 0.15 / 15.2 / 0.20 / 1.002 (NOx 2800) | no dilution → NOx runaway past 1370 °C |
| GAS-ESO-001 EGR stuck open | 200 / 0.80 / 12.0 / 1.50 / 1.045 | 25 / 0.12 / 15.1 / 0.30 / 1.000 | high intake volume dilutes stuck EGR; stabilises |
| GAS-EVAP-001 saturated EVAP | 180 / 0.80 / 13.0 / 0.50 / 0.976 | 350 / 1.90 / 12.1 / 0.20 / 0.940 | purge opens at 2500 → raw-vapour spike |
| GAS-CNL-001 cold cat (no light-off) | 100 / 0.50 / 14.0 / 0.50 / 1.000 | 12 / 0.08 / 15.4 / 0.10 / 1.000 | thermal light-off — healthy cat recovers |
| GAS-COV-001 cat overload/blow-through | 500 / 2.00 / 12.0 / 1.00 / 0.921 (NOx 800) | 450 / 1.90 / 12.2 / 0.80 / 0.930 (NOx 1100) | residence time too short — gases blow through |

CO/CO₂ in %, HC/NOx in ppm. Healthy baseline (GAS-NORM-001): CO₂ rises 1–2 % into
15.5–16.0 %, HC/CO →near zero, NOx rises modestly with thermal throughput.

## Why this is delta-relations, not gaslab static

A single 5-gas snapshot cannot tell GAS-WVS (improves) from GAS-WPR (worsens) — both
read "elevated HC" at idle. Only the **sign of Δgas across the speed step** resolves
them. The owning lab for the per-state gas frame is **GASLab**; the cross-state Δ math
is **COMLab** (isolation contract — GASLab stays stateless).

## Routing note
Pairs with the OBD-side ΔTrim profiles (delta-relations/01–05). A full case fuses
Δgas (this) + ΔTrim (those) — e.g. vacuum leak = ΔTrim<0 AND Δλ_gas≈0→1.0.


## Core Entities

- DELTA_GAS, GAS-VAC-001, GAS-LEAN-001, GAS-EAL-001, GAS-WPR-001, GAS-WVS-001
- GAS-FC-001, GAS-ESC-001, GAS-ESO-001, GAS-EVAP-001, GAS-CNL-001, GAS-COV-001
- GASLab (producer of per-state 5-gas frame), COMLab delta engine (consumer, PENDING FU-2)

## Graph relations (explicit)

**GASLab** PRODUCES **DELTA_GAS** per-state 5-gas frame
**COMLab delta engine** CONSUMES **DELTA_GAS**
**WORN_RINGS** INTENSIFIES_AT_2500RPM **DELTA_GAS**
**WORN_VALVE_SEALS** ATTENUATES_AT_2500RPM **DELTA_GAS**
**EGR_STUCK_CLOSED** RAISES **NOx** at 2500 RPM
**DELTA_GAS** PAIRS_WITH **DELTA_TRIM** for case fusion

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
