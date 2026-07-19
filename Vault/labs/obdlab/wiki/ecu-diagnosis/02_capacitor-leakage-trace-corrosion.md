---
chunk: ecu-diagnosis/02_capacitor-leakage-trace-corrosion
topic: ecu-diagnosis
sources:
  - EcuSignatures.md §"1. Liquid Electrolyte Capacitor Leakage and Board-Level Trace Corrosion"
consumer: PROPOSAL — consumer = COMLab ECU-hardware-fault checker (proposals/OBD_ImplProp.md, specced in ECU-FU-1); register node in comlab/config/proposals/. New v2 fault: the engine cannot detect ECU capacitor-leak / trace-corrosion today (cross-ref existing ecu_fault.json ERR-ECU-001 processor/5V — refine, don't duplicate). Ships with its consumer per the v2 forward-progress rule, not deferred. Live ingredient fields all exist (calculated_engine_load_pct, shrtft1/longft1 + b2, normalized_obd_lambda).
consumer_status: PROPOSAL
provenance: sources/ecu-diagnosis/EcuSignatures.md
related: [[01_method-load-pct-and-idle-bands]], [[07_comparative-signature-tables]]
---

# Failure mode 1 — capacitor leakage / board-level trace corrosion

Liquid-electrolyte aluminium caps on the internal 5 V / 12 V rails degrade over
decades; leaked conductive electrolyte dissolves PCB copper traces, creating
high-impedance paths and AC ripple on the DC reference lines. Signature is
**rhythmic instability**, not a fixed offset.

## Low idle (700–800 RPM)

AC ripple superimposes on the reference lines and corrupts ratiometric MAP/MAF
readings, so the ECU cannot stabilise $\dot{m}_{\text{actual}}$.

- `calculated_engine_load_pct` fluctuates erratically **15–35 %**.
- STFT B1 and B2 oscillate symmetrically **±15 %** (chasing the shifting sensors).
- Zirconia upstream oscillates erratically **0.15 V–0.85 V**; downstream mimics it.
- Physical: CO ≈ 1.8 %, HC ≈ 450 ppm, λ_chem ≈ 1.025 (oscillating).

## Stress idle (3500–4500 RPM)

Higher alternator speed intensifies ripple → clock jitter, serial-data
corruption, ADC misreads. ECU often drops to **open-loop fault mode (OL_FAULT)**.

- STFT B1/B2 and LTFT B1/B2 **freeze at 0 %** (maps to live `TrimAnalyticsGate.OPEN_LOOP`, which suppresses trim findings).
- `calculated_engine_load_pct` drops **< 10 %** or locks at a fail-safe default.
- Mixture drifts rich on base open-loop maps: CO ≈ 3.5 %, HC ≈ 600 ppm, λ_chem ≈ 0.920.
- Both zirconia sensors peg high **> 0.85 V** (rich, unmetered by OBD).

## Discriminator

Symmetric ±15 % STFT oscillation across **both** banks + erratic LOAD_PCT at low
idle, collapsing to frozen 0 % trims + open loop at stress idle. The symmetry
(B1≈B2) is the tell vs a single-bank sensor fault — but **no live path reads
B1-vs-B2 divergence** (`total_trim_correction_delta_b2` has no consumer); that
discriminator is part of what the proposed checker must add.

Citation: EcuSignatures.md failure mode 1, low-idle and stress-idle subsections;
Table 1 row 1 / Table 2 row 1 (see chunk 07).


## Core Entities

- ECU_CAPACITOR_LEAK, STFT, LTFT, LOAD_PCT
- TrimAnalyticsGate.OPEN_LOOP, ERR-ECU-001
- ECU_HARDWARE_CHECKER (proposed consumer, ECU-FU-1)

## Graph relations (explicit)

**ECU_CAPACITOR_LEAK** OSCILLATES **STFT** symmetrically both banks
**ECU_CAPACITOR_LEAK** TRIGGERS **TrimAnalyticsGate.OPEN_LOOP** at stress idle
**TrimAnalyticsGate.OPEN_LOOP** SUPPRESSES trim findings
**ECU_CAPACITOR_LEAK** REFINES **ERR-ECU-001**
**ECU_CAPACITOR_LEAK** CONSUMED_BY **ECU_HARDWARE_CHECKER**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
