---
chunk: ecu-diagnosis/07_comparative-signature-tables
topic: ecu-diagnosis
sources:
  - EcuSignatures.md §"Comparative Diagnostic Framework" (Tables 1–3)
  - EcuSignatures.md §"Analytical Conclusions and Implications"
consumer: PROPOSAL — consumer = COMLab ECU-hardware-fault checker (proposals/OBD_ImplProp.md, ECU-FU-1); register in comlab/config/proposals/. This matrix IS the discriminator table the proposed checker loads — the analogue of fault_atlas_router's discriminator/operator table, for the five proposed ECU-hardware nodes (chunks 02–06). It also drives two companion proposals: (a) a B1-vs-B2 divergence reader of total_trim_correction_delta_b2 (emitted-but-unread today — ECU-FU-2), (b) TPS/IAT input fields (ECU-FU-3). All ship as proposals with their consumers, not deferred.
consumer_status: PROPOSAL
provenance: sources/ecu-diagnosis/EcuSignatures.md
related: [[02_capacitor-leakage-trace-corrosion]], [[03_injector-driver-open-and-short]], [[04_coil-driver-transistor-failure]], [[05_sensor-ground-trace-open]], [[06_5v-regulator-rail-collapse]]
---

# Comparative signature tables + analytical conclusions

The reference matrix for all five modes. Preserved verbatim as the proposed
checker's discriminator input. LI = low idle (700–800), SI = stress idle
(3500–4500).

## Table 1 — physical tailpipe emissions + calculated lambda

| Mode | State | CO₂ % | O₂ % | CO % | HC ppm | NOx ppm | λ_chem |
|---|---|---|---|---|---|---|---|
| 1. Capacitor leak / trace corrosion | LI | 11.5 | 2.5 | 1.8 | 450 | 40 | 1.025 |
| | SI | 10.0 | 1.5 | 3.5 | 600 | 65 | 0.920 |
| 2A. Injector driver open (B1) | LI | 10.5 | 4.5 | 1.5 | 400 | 20 | 1.120 |
| | SI | 11.0 | 4.0 | 2.2 | 350 | 35 | 1.080 |
| 2B. Injector driver shorted (B1) | LI | 8.0 | 1.8 | 7.5 | 1600 | 5 | 0.780 |
| | SI | 8.5 | 1.2 | 6.8 | 1400 | 10 | 0.810 |
| 3. Coil driver shorted / coil melted | LI | 11.0 | 5.2 | 0.2 | 2200 | 10 | 1.010 |
| | SI | 11.5 | 4.8 | 0.15 | 1800 | 25 | 1.005 |
| 4. Vaporized sensor ground trace | LI | 6.5 | 0.3 | 9.5 | 1200 | 10 | 0.720 |
| | SI | 7.2 | 0.2 | 8.8 | 1400 | 15 | 0.740 |
| 5. Collapsed 5 V regulator rail | LI | 8.5 | 6.5 | 0.1 | 850 | 110 | 1.350 |
| | SI | 7.0 | 8.5 | 0.05 | 1100 | 350 | 1.550 |

## Table 2 — live OBD-II PID signatures

Columns: LOAD_PCT % · STFT B1 · STFT B2 · LTFT B1 · LTFT B2 · MAP/MAF · TPS % · ECT/IAT °C.

| Mode | State | LOAD | STFT B1 | STFT B2 | LTFT B1 | LTFT B2 | MAP/MAF | TPS | ECT/IAT |
|---|---|---|---|---|---|---|---|---|---|
| 1. Capacitor leak | LI | 15–35 | ±15 | ±15 | ±5 | ±5 | Fluctuating | 15–18 | Normal (>75) |
| | SI | <10 | 0 | 0 | 0 | 0 | Erratic spikes | 25–30 | Normal (>75) |
| 2A. Injector open | LI | 20–25 | +25 | 0–3 | +25 | 0–3 | Stable | 15–18 | Normal (>75) |
| | SI | 12–15 | +25 | 0–3 | +25 | 0–3 | Scales w/ RPM | 25–30 | Normal (>75) |
| 2B. Injector short | LI | 30–35 | −25 | 0–3 | −25 | 0–3 | Elevated | 18–22 | Normal (>75) |
| | SI | 25–30 | −25 | 0–3 | −25 | 0–3 | Elevated | 30–35 | Normal (>75) |
| 3. Coil driver short | LI | 18–22 | +15…20 | 0–3 | +15…20 | 0–3 | Stable | 15–18 | Normal (>75) |
| | SI | 10–12 | +15 | 0–3 | +15 | 0–3 | Scales w/ RPM | 25–30 | Normal (>75) |
| 4. Ground trace blown | LI | 80–90 | 0 | 0 | 0 | 0 | Pegged high | 100 | −40 (locked) |
| | SI | 100 | 0 | 0 | 0 | 0 | Pegged high | 100 | −40 (locked) |
| 5. Collapsed 5 V rail | LI | 5–8 | +25 | +25 | +25 | +25 | Artificially low | 0 | Normal (>75) |
| | SI | 8–10 | +25 | +25 | +25 | +25 | Artificially low | 15–20 | Normal (>75) |

**Live-field availability of these columns:** LOAD → `calculated_engine_load_pct`
✓ · STFT/LTFT B1 → `shrtft1`/`longft1` ✓ · STFT/LTFT B2 → `shrtft2`/`longft2`
(nullable) ✓ · MAP → `manifold_vacuum_kpa` ✓ · MAF → `mass_airflow_gps` ✓ · ECT
→ `coolant_temp_c` ✓ · **TPS → none** ✗ · **IAT → none** ✗.

## Table 3 — O₂ sensor configuration behaviour (condensed)

| Mode | A: NB up + NB down | B: WB up (UEGO) + NB down | C: single NB up |
|---|---|---|---|
| 1. Capacitor leak | in-phase erratic 0.15–0.85 V (LI) → rich peg >0.85 V (SI) | WB λ 0.98–1.05 fluctuating (LI) → pegs rich <0.90 (SI) | high-amplitude swings 0.1–0.9 V, no stable trim baseline |
| 2A. Injector open | up B1 lean <0.1 V; down lean <0.1 V (O₂ bypass) | WB B1 λ>1.15; down NB lean <0.1 V | up lean <0.1 V → global STFT +25 % |
| 2B. Injector short | up B1 rich >0.9 V; down rich >0.85 V | WB B1 λ<0.80; down NB rich >0.85 V | — |
| 3. Coil driver short | up B1 erratic lean spikes <0.2 V; down <0.15 V | WB B1 λ≈1.05–1.10; down NB <0.15 V | up oscillates lean-biased → positive trims |
| 4. Ground trace | up & down peg high >0.9 V, unresponsive | WB λ<0.75; down NB >0.9 V | up pegs high >0.9 V, open-loop default |
| 5. Collapsed 5 V rail | up & down peg lean <0.1 V | WB λ>1.4; down NB <0.1 V | up lean <0.1 V, max positive trim |

## Analytical conclusions (the discriminator logic)

1. **Truth-vs-perception beats fault codes.** Collapsed VREF makes MAP/TPS read
   low, tempting a sensor swap — but the 5-gas analyser shows global lean + high
   NOx while trims are pinned **+25 %**. Lean tailpipe + pinned-positive trim +
   flat-low ratiometric voltages ⇒ the **reference rail / ECU power stage**, not
   a sensor. (This is the `perception_contradiction` axis, generalised beyond λ.)

2. **Symmetric vs asymmetric across banks.** External sensor/harness faults are
   typically **bank-specific** (e.g. B1 O₂ short → asymmetric). Internal faults
   that touch a shared plane (vaporized reference ground; collapsed VREF) hit
   **both banks symmetrically** (frozen or pinned B1≈B2 + locked extreme ECT/TPS).
   ⇒ B1-vs-B2 symmetry is a primary discriminator — **but no live code reads
   `total_trim_correction_delta_b2` for divergence today** (the proposed checker
   must add it).

3. **Deceptive lambda.** Single-cylinder coil/injector faults pump raw fuel +
   raw O₂ in stoich proportion, so λ_chem ≈ 1.01 looks normal while HC ≈ 2200 ppm
   screams misfire. **Never clear a fault on lambda alone — read HC and O₂.**
   At SI these mix in the catalyst → >900 °C substrate temp (melt risk).

Citation: EcuSignatures.md Tables 1–3 and Analytical Conclusions section.


## Core Entities

- ECU_CAPACITOR_LEAK, INJECTOR_DRIVER_OPEN, INJECTOR_DRIVER_SHORT, COIL_DRIVER_SHORT, SENSOR_GROUND_TRACE_OPEN, VREF_RAIL_COLLAPSE
- total_trim_correction_delta_b2, perception_contradiction
- ECU_HARDWARE_CHECKER (proposed consumer, ECU-FU-1)

## Graph relations (explicit)

**ECU_HARDWARE_CHECKER** LOADS comparative signature matrix (Tables 1-3)
**bank_symmetry** DISCRIMINATES internal from external faults
**total_trim_correction_delta_b2** READ_BY **ECU_HARDWARE_CHECKER**
**deceptive_lambda** REQUIRES **HC** and **O2** to expose misfire
**ECU_HARDWARE_CHECKER** ROUTES **ECU_CAPACITOR_LEAK**, **INJECTOR_DRIVER_OPEN**, **INJECTOR_DRIVER_SHORT**, **COIL_DRIVER_SHORT**, **SENSOR_GROUND_TRACE_OPEN**, **VREF_RAIL_COLLAPSE**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
