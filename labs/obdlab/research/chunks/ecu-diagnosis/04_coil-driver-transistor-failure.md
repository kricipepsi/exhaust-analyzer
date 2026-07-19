---
chunk: ecu-diagnosis/04_coil-driver-transistor-failure
topic: ecu-diagnosis
sources:
  - EcuSignatures.md §"3. High-Power Ignition Coil Driver Transistor Failures"
consumer: PROPOSAL — consumer = COMLab ECU-hardware-fault checker (proposals/OBD_ImplProp.md, ECU-FU-1); register in comlab/config/proposals/. New v2 fault. GASLab chemistry maps to live ChemicalSignature.IGNITION_MISFIRE / CATALYST_OVERWHELMED (cross-ref), but those classify the *exhaust symptom*, not "internal coil-driver transistor short" — the proposal adds the ECU-localising verdict on top of those signals. Ships with its consumer, not deferred.
consumer_status: PROPOSAL
provenance: sources/ecu-diagnosis/EcuSignatures.md
related: [[01_method-load-pct-and-idle-bands]], [[07_comparative-signature-tables]]
---

# Failure mode 3 — ignition coil driver transistor failure

Darlington/IGBT coil drivers switch up to 15 A. High secondary resistance (worn
plugs/wires) overstresses the junction → thermal short → continuous 100 % duty
ground → coil primary saturates, melts, fails open → **permanent single-cylinder
ignition misfire on B1**.

## The deceptive-lambda trap (this mode's whole point)

The dead cylinder pumps raw fuel **and** unburned air in stoichiometric
proportion, so calculated **λ_chem stays ≈ 1.01** — looks healthy — while **raw
HC is enormous (≈ 2200 ppm)** and CO is very low (≈ 0.2 %). Lambda alone hides a
catastrophic misfire; HC + O₂ expose it.

## Low idle (700–800 RPM)

- λ_chem ≈ 1.010; O₂ 5.2 %; HC ≈ 2200 ppm; CO ≈ 0.2 %.
- Zirconia upstream B1 pegs lean **< 0.1 V**; wideband reads deceptive lean λ ≈ 1.10.
- ECU drives STFT/LTFT B1 **+15…+20 %**; B2 normal → surviving B1 cylinders go rich (CO rises to 1.2 %).
- `calculated_engine_load_pct` normal **18–22 %**.

## Stress idle (3500–4500 RPM)

Raw HC + O₂ ignite in the catalyst → substrate **> 900 °C (1650 °F)**;
post-cat tailpipe HC drops to 1800 ppm, CO 0.15 %, λ_chem ≈ 1.005.

- Downstream zirconia may rise to ~0.45 V or fluctuate as OSC is exceeded.
- B1 trims stay **+15 %**; B2 near stoich.
- `calculated_engine_load_pct` tracks RPM **10–12 %**.

## Live-path cross-ref (symptom only)

GASLab chemistry → `ChemicalSignature.IGNITION_MISFIRE` (unburned fuel + O₂
spike) and, at stress idle, `CATALYST_OVERWHELMED` (raw fuel hitting cat). These
are live but describe the *exhaust*, not the ECU driver. Localising to the coil
driver (vs a bad plug/coil/wire) is the proposed checker's job.

## Discriminator

Single-bank positive trim + classic IGNITION_MISFIRE chemistry (high HC, high O₂,
near-stoich λ). What flags it as *internal driver* rather than external ignition
is forensic (the 100 %-duty thermal-runaway history) — no PID uniquely separates
them, which is exactly why this stays PENDING.

Citation: EcuSignatures.md failure mode 3, both idle bands; Table 1 row 3, Table
2 row 3, Table 3 row 3 (chunk 07).


## Core Entities

- COIL_DRIVER_SHORT, HC, LTFT
- ChemicalSignature.IGNITION_MISFIRE, CATALYST_OVERWHELMED
- ECU_HARDWARE_CHECKER (proposed consumer, ECU-FU-1)

## Graph relations (explicit)

**COIL_DRIVER_SHORT** CAUSES **IGNITION_MISFIRE**
**COIL_DRIVER_SHORT** RAISES **HC** at near-stoich lambda
**IGNITION_MISFIRE** at stress idle PRODUCES **CATALYST_OVERWHELMED**
**COIL_DRIVER_SHORT** MAPS_TO **ChemicalSignature.IGNITION_MISFIRE**
**COIL_DRIVER_SHORT** CONSUMED_BY **ECU_HARDWARE_CHECKER**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
