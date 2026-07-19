---
chunk: ecu-diagnosis/06_5v-regulator-rail-collapse
topic: ecu-diagnosis
sources:
  - EcuSignatures.md §"5. Collapsed/Drifted Internal 5V Regulator Rail"
consumer: PROPOSAL — consumer = COMLab ECU-hardware-fault checker (proposals/OBD_ImplProp.md, ECU-FU-1); register in comlab/config/proposals/. New v2 fault refining ecu_fault.json ERR-EF-006 (5V-ref drift → lean-bias). High-NOx lean chemistry maps to live ChemicalSignature.HIGH_COMBUSTION_TEMP / LEAN_MIXTURE (cross-ref); the proposal adds the internal-VREF verdict (pinned +25 % both banks DESPITE lean tailpipe + flat-low ratiometric voltages). NOTE: ECU internal 5 V regulator — NOT the fuel-pressure regulator (VACUUM_REGULATOR_DIAPHRAGM_RUPTURE). Ships with its consumer, not deferred.
consumer_status: PROPOSAL
provenance: sources/ecu-diagnosis/EcuSignatures.md
related: [[01_method-load-pct-and-idle-bands]], [[07_comparative-signature-tables]]
---

# Failure mode 5 — collapsed / drifted internal 5 V regulator rail

The internal regulator steps 12 V down to a stable 5.0 V reference
($V_{\text{REF}}$) used by the MCU/ADC and routed to ratiometric sensors (MAP,
MAF, TPS, pedal). Thermal/silicon degradation drifts the output down, e.g. to
**4.1 V**. The MCU still scales against an expected 5.0 V baseline, so every
ratiometric reading is suppressed and misinterpreted.

This is the **mirror image of failure mode 4**: there sensors floated high
(false rich over-fuel); here they collapse low (false lean fuel-starve).

## Low idle (700–800 RPM)

- MAP voltage abnormally low → ECU reads **high vacuum / extreme low load** → minimal base pulse width → fuel starvation.
- TPS ≈ 0 V → closed throttle.
- Engine runs **extreme lean**, misfires, near-stall.
- Zirconia upstream **< 0.1 V**; wideband **λ > 1.3**.
- ECU pins STFT/LTFT B1/B2 **+25 %** (both banks) but base fuelling is capped by the corrupted MAP/MAF, so correction is futile.
- Physical: CO₂ 8.5 %, CO 0.1 %, O₂ 6.5 %, HC ≈ 850 ppm, λ_chem ≈ 1.350.
- `calculated_engine_load_pct` artificially low **5–8 %**.

## Stress idle (3500–4500 RPM)

Throttle must open wide to draw air, but suppressed $V_{\text{REF}}$ keeps the
TPS PID at only **15–20 %** and MAP low; `calculated_engine_load_pct` stays
abnormally low **8–10 %**, failing to scale with RPM. Trims pinned **+25 %** both
banks. Ultra-lean + high speed → combustion-temp spike → **NOx ≈ 350 ppm**
(anomalous in neutral). CO₂ 7.0 %, O₂ 8.5 %, HC ≈ 1100, λ_chem ≈ 1.550. Both O₂
sensors locked low **< 0.1 V**.

## Live-path cross-ref (symptom only)

GASLab chemistry → `ChemicalSignature.LEAN_MIXTURE` and, at stress idle,
`HIGH_COMBUSTION_TEMP` (NOx). Live, but exhaust-only.

## Discriminator

**Symmetric +25 % both banks + severely lean tailpipe (high O₂, high NOx) +
flat-low voltage on all 5 V ratiometric sensors + abnormally low LOAD_PCT that
won't scale with RPM.** A first-order reader would swap MAP/TPS; the
truth-vs-perception cross-check (pinned-positive trim that *can't* lean a
genuinely-lean tailpipe) points at the rail. Today nothing fuses that — PENDING.

Citation: EcuSignatures.md failure mode 5, both idle bands; Analytical
Conclusions ¶ on collapsed VREF; Table 1 row 5, Table 2 row 5 (chunk 07).


## Core Entities

- VREF_RAIL_COLLAPSE, LTFT, LOAD_PCT, NOx
- ChemicalSignature.LEAN_MIXTURE, HIGH_COMBUSTION_TEMP, ERR-EF-006
- ECU_HARDWARE_CHECKER (proposed consumer, ECU-FU-1)

## Graph relations (explicit)

**VREF_RAIL_COLLAPSE** PINS **LTFT** to +25% both banks
**VREF_RAIL_COLLAPSE** PRODUCES **LEAN_MIXTURE**
**VREF_RAIL_COLLAPSE** RAISES **NOx** at stress idle (HIGH_COMBUSTION_TEMP)
**VREF_RAIL_COLLAPSE** MIRRORS **SENSOR_GROUND_TRACE_OPEN**
**VREF_RAIL_COLLAPSE** MAPS_TO **ChemicalSignature.LEAN_MIXTURE**
**VREF_RAIL_COLLAPSE** CONSUMED_BY **ECU_HARDWARE_CHECKER**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
