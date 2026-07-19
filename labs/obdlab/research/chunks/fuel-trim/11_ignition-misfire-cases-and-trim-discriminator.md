---
chunk: fuel-trim/11_ignition-misfire-cases-and-trim-discriminator
topic: fuel-trim
sources:
  - FuelTrimFamilies.md §"Fault Family 2: P03xx - Ignition System and Misfires" (cases 10–14)
  - Fuel Trim Diagnostics.txt §"STFT range rule of thumb" + §"miss-fire → excess O₂ → false lean"
consumer: COMLab fault_atlas_router misfire/ignition_fault routing (ERR-MF-004/005/006, ERR-IF-003) + the misfire-vs-fuelling pre-route discriminator. Two mechanisms are PROPOSALS (register in comlab/config/proposals/): fuel_water_contamination, alternator_ac_ripple_sensor_corruption.
consumer_status: MIXED (active misfire/ignition families + 2 proposals + 1 discriminator proposal)
provenance: sources/fuel-trim/FuelTrimFamilies.md + Fuel Trim Diagnostics.txt
related: [[09_fault-family-case-matrix]], [[07_trim-vs-gas-chemistry-crosscheck]], [[10_air-fuel-metering-injector-cases]]
---

# P03xx — ignition & misfire, and the misfire-vs-fuelling trim discriminator

## Why misfires move fuel trim (the false-lean mechanism)

A misfiring cylinder pumps **unburned O₂** into the exhaust. The upstream O₂
sensor reads that O₂ as a **lean** mixture, so the PCM **adds fuel** → positive
STFT on the affected bank — even though fuelling is fine. This is the most common
way a non-fuel fault masquerades as a lean fuel fault.

- **Steady misfire** → steady false-lean → high sustained +STFT.
- **Intermittent misfire** → mixed +/− corrections → *lower net* STFT (the O₂
  blasts come and go). A small noisy positive trim does not rule out misfire.

## The STFT rule-of-thumb discriminator (PROPOSAL)

Practitioner range split (Fuel Trim Diagnostics.txt): **ignition/mechanical
misfire ≈ −10 % … +15 %**, **fuelling faults ≈ −10 % … +25 %**. Fuelling faults
push trim *further* and *symmetrically across load*; misfire-induced trim is
single-bank, RPM-noisy, and accompanied by a Pxxxx misfire code. Propose a
`misfire_vs_fuelling` pre-route gate: when a P030x is active AND the positive
trim is single-bank and ≤ +15 %, route to misfire/ignition families **before**
lean-fuel families. Consumer = fault_atlas_router candidate-pruning (it already
carries MISFIRE_HISTORY DTC tags); this adds the trim-magnitude key.

## Cases

- **Water-contaminated fuel (row 10, P0300) — PROPOSAL.** Water pools in the rail,
  intermittently blocks injectors → random multi-cylinder misfire → O₂ drops to
  0.05 V → false lean → STFT +20 %. Oil match-test negative (no dilution/coolant);
  fuel sample shows phase separation. No node covers fuel-borne contamination.
  Register `fuel_water_contamination`; consumer = fault_atlas keyed on (P0300 +
  positive trim + multi-bank random misfire with normal compression/spark).
- **Compression loss (row 11, ERR-MW-005/MF-006).** Single-cylinder mechanical
  misfire → false lean B1 +18 %. Compression test + leak-down (air past intake
  valves) confirms. Maps to `low_compression_mechanical_misfire`.
- **Coil primary open (row 12, ERR-MF-004).** Cylinder not firing → false lean B1
  +14 %; primary OL vs 0.4–2.0 Ω. Swap-and-shift confirms. Maps to
  `ignition_coil_primary_winding_failure`.
- **CKP thermal open (row 13, ERR-IF-003).** Warm stall, 0 RPM on scan; cold signal
  toggles 0.5↔4.5 V, locks at 5 V when heated. Trims oscillate ±15 % pre-stall.
  Maps to `ckp_sensor_intermittent_dropout`.
- **Alternator AC ripple → CMP corruption (row 14, P0340) — PROPOSAL.** Failed
  rectifier diode leaks AC (0.85 V vs <0.5 V limit) → corrupts Hall CMP square wave
  → PCM loses phase sync → defaults to **batch-fire** → minor cross-cylinder
  misfire + small STFT oscillation (±5 %). The CMP sensor itself tests good — the
  root cause is the charging system. No node links charging-system ripple to sensor
  corruption. Register `alternator_ac_ripple_sensor_corruption`; consumer =
  fault_atlas charging_system family + a CMP/CKP-noise route. (Cross-ref ECU pass:
  same AC-ripple mechanism as ecu-diagnosis mode 1, different origin.)

Citation: FuelTrimFamilies.md cases 10–14; Fuel Trim Diagnostics.txt STFT
rule-of-thumb (−10..+15 % ignition/mechanical vs −10..+25 % fuelling) and the
misfire→excess-O₂→false-lean derivation.


## Core Entities

- IGNITION_MISFIRE, MISFIRE_FALSE_LEAN, COMPRESSION_LOSS, COIL_PRIMARY_OPEN, CKP_SENSOR_DROPOUT
- FUEL_WATER_CONTAMINATION, ALTERNATOR_AC_RIPPLE, P0300, P0301, P0340
- misfire_vs_fuelling pre-route gate (PROPOSAL); fault_atlas_router (consumer)

## Graph relations (explicit)

**IGNITION_MISFIRE** PUMPS unburned O2 producing **MISFIRE_FALSE_LEAN**
**MISFIRE_FALSE_LEAN** RAISES single-bank **POSITIVE_TRIM**
**misfire_vs_fuelling** gate ROUTES P030x plus single-bank trim under +15% to misfire family first
**P0300** INDICATES **FUEL_WATER_CONTAMINATION** with random multi-misfire
**P0340** INDICATES **ALTERNATOR_AC_RIPPLE** CMP corruption
**ALTERNATOR_AC_RIPPLE** SHARES_MECHANISM with **ECU_CAPACITOR_LEAK**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
