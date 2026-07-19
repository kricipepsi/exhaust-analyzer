---
chunk: ecu-diagnosis/03_injector-driver-open-and-short
topic: ecu-diagnosis
sources:
  - EcuSignatures.md §"2. Low-Side Fuel Injector Driver Failures" (Mode A open, Mode B shorted)
consumer: PROPOSAL — consumer = COMLab ECU-hardware-fault checker (proposals/OBD_ImplProp.md, ECU-FU-1); register in comlab/config/proposals/. New v2 fault refining ecu_fault.json ERR-EF-007 (rich-bias / injector-driver) to localise an internal low-side-driver fault vs external injector/wiring. Mode B's railed-negative-trim OVERLAPS live detect_compensated_rich() (cross-ref) but that attributes it to a fuel leak, not a driver — so the proposal adds the driver-specific verdict. Ships with its consumer, not deferred.
consumer_status: PROPOSAL
provenance: sources/ecu-diagnosis/EcuSignatures.md
related: [[01_method-load-pct-and-idle-bands]], [[07_comparative-signature-tables]]
---

# Failure mode 2 — low-side fuel injector driver failures

The low-side MOSFET/driver IC pulses each injector's ground. Thermal fatigue
gives two opposite electrical modes; both are **single-bank (Bank 1)** here.

## Mode A — open-circuit driver (one cylinder dead on B1)

Dead cylinder pumps pure air (≈ 20.9 % O₂) into the B1 manifold.

| Band | STFT/LTFT B1 | B2 | λ_chem | Key gases | LOAD_PCT |
|---|---|---|---|---|---|
| Low idle | pinned **+25 %** | 0…+3 % | ≈ 1.120 | O₂ 4.5 %, CO 1.5 %, HC 400 | 20–25 % |
| Stress idle | pinned **+25 %** | 0…+3 % | ≈ 1.080 | tailpipe CO 2.2 %, HC 350 | 12–15 % |

Zirconia upstream B1 pegs lean **< 0.1 V**; wideband B1 reads **λ > 1.2**.
Downstream pegs lean from O₂ bypass. Max enrichment is applied globally to B1, so
the *surviving* B1 cylinders run rich (the deceptive CO alongside high O₂).

## Mode B — shorted-to-ground driver (stuck-active on B1)

Drain–source fuse → continuous ground → injector sprays constantly → flooded
cylinder, rich misfire.

| Band | STFT/LTFT B1 | B2 | λ_chem | Key gases | LOAD_PCT |
|---|---|---|---|---|---|
| Low idle | pinned **−25 %** | balanced | ≈ 0.780 | CO 7.5 %, HC 1600, CO₂ 8.0 % | 30–35 % |
| Stress idle | pinned **−25 %** | balanced | ≈ 0.810 | CO 6.8 %, HC 1400 | 25–30 % |

Zirconia upstream B1 pegs rich **> 0.9 V**; wideband **λ < 0.8**. Deceptive
tailpipe O₂ ≈ 1.8 % (misfire pumps some O₂). Catalyst risk: fuel-flooded.

### Live-path overlap (does NOT make this active)

Mode B's **railed-negative trim + rich** matches the AND-gate in
`detect_compensated_rich()` (lambda_chem ∈ [0.95,1.05], trim < −15 %, rich DTC).
But Mode B's λ_chem (0.78–0.81) is **outside** that stoich window, so the live
detector would not even fire — and if it did, it would report "compensated rich
/ fuel leak," not "injector driver short." Correct verdict requires the proposed
ECU checker.

## Discriminator

**Single-bank** pinned trim at the rail (+25 % open / −25 % short), B2 balanced,
held across both idle bands. LOAD_PCT stays plausible (Mode A) or elevated from
lost vacuum (Mode B). Bank asymmetry is the signal — and again, unread today.

Citation: EcuSignatures.md failure mode 2 Mode A / Mode B, both idle bands;
Table 1 rows 2A/2B, Table 2 rows 2A/2B (chunk 07).


## Core Entities

- INJECTOR_DRIVER_OPEN, INJECTOR_DRIVER_SHORT, STFT, LTFT
- ERR-EF-007, detect_compensated_rich
- ECU_HARDWARE_CHECKER (proposed consumer, ECU-FU-1)

## Graph relations (explicit)

**INJECTOR_DRIVER_OPEN** PINS **LTFT** B1 to +25%
**INJECTOR_DRIVER_SHORT** PINS **LTFT** B1 to -25%
**INJECTOR_DRIVER_SHORT** OVERLAPS **detect_compensated_rich** but lambda_chem falls outside its stoich window
**INJECTOR_DRIVER_SHORT** REFINES **ERR-EF-007**
**INJECTOR_DRIVER_OPEN** CONSUMED_BY **ECU_HARDWARE_CHECKER**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
