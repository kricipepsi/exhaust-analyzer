---
chunk: ecu-diagnosis/01_method-load-pct-and-idle-bands
topic: ecu-diagnosis
sources:
  - EcuSignatures.md §intro (forensic OBD-PID vs 5-gas method; LOAD_PCT formula; the two idle bands)
consumer: SPLIT. (a) Truth-vs-perception method → ACTIVE: comlab/core/perception_contradiction.py detect() compares normalized_obd_lambda (perception) vs GASLab lambda_chem (truth). (b) Idle bands → ACTIVE: obdlab RpmStateBucket {STABILIZED_IDLE 650–900, STRESS_IDLE 3000–4500}. (c) LOAD_PCT *field* → ACTIVE: OBDLivePayload.calculated_engine_load_pct read by sensor_signal_translator/state_bucketing. (d) The J1979 LOAD_PCT *closed-form WOT formula* → PENDING (no live evaluator; field arrives as an input PID, not computed from this equation).
consumer_status: MIXED (method/bands/field ACTIVE; WOT formula PENDING)
provenance: sources/ecu-diagnosis/EcuSignatures.md (text spine; identical content to the ECU Hardware Fault OBD PID Signatures HTML + PDF renders — extract from the .md only)
related: [[02_capacitor-leakage-trace-corrosion]], [[07_comparative-signature-tables]], [[../o2-logic/05_bias-vs-real-truth-perception]]
---

# Forensic method, LOAD_PCT, and the two idle bands

This document's diagnostic spine is a single principle, and it is the one the
engine already implements: **internal ECU hardware faults are isolated by the
divergence between what the ECU reports over OBD (perception) and what a 5-gas
analyser measures in the exhaust (ground truth).** When an internal component
decays it corrupts the closed-loop control loop and the OBD datastream lies; the
exhaust chemistry does not.

The live consumer of that principle is `perception_contradiction.detect()`
(λ_obd vs λ_chem). **Caveat — see chunk 07 and each failure-mode chunk:** that
detector's Lambda Truth guard *suppresses* a sensor-bias verdict when
`lambda_chem < 0.90 or > 1.10`. Most ECU-hardware faults here produce deeply
abnormal chemistry (λ 0.72–1.55), so they fall *outside* the sensor-bias path by
design — detecting them as ECU-hardware faults needs the proposed checker
(`proposals/OBD_ImplProp.md`), not the existing bias detector.

## Stoichiometric target

Under closed loop with ECT > 75 °C the ECU targets stoichiometry, physical
lambda `λ = 1.000`. Internal hardware failures corrupt this feedback loop.

## J1979 Calculated Load (LOAD_PCT)

The field is live (`OBDLivePayload.calculated_engine_load_pct`, 0–100 %). The
**closed-form WOT definition** below is provenance only — no live code evaluates
it (the field is ingested as a PID):

$$\text{LOAD\_PCT} = \frac{\dot{m}_{\text{actual}}}{\dot{m}_{\text{max\_WOT}}(RPM)\cdot\frac{BARO}{29.92}\cdot\sqrt{\frac{298}{AAT+273}}}\times 100\%$$

where $\dot{m}_{\text{actual}}$ = actual mass airflow, $\dot{m}_{\text{max\_WOT}}(RPM)$ =
peak WOT mass airflow at STP vs engine speed, $BARO$ = barometric pressure,
$AAT$ = ambient air temperature (°C). Internal failures distort either the
variables or the sensor inputs, producing distinct LOAD_PCT signatures at the
two idle bands. *(`AAT` has no live OBDLivePayload field — see chunk 05 / the
PID-gap follow-up.)*

## The two idle bands

| Doc term | RPM | Maps to live `RpmStateBucket` |
|---|---|---|
| Low idle | 700–800 | `STABILIZED_IDLE` (650–900) |
| Stress idle | 3500–4500 | `STRESS_IDLE` (3000–4500) |

Every failure mode is characterised as a **pair** of signatures across these two
bands. ⚠ Band reconciliation (SWEEP_MANIFEST O2-FU-3): this doc uses 3500–4500
for stress idle, matching `FuelTrimW.md` and the live `STRESS_IDLE` bucket, but
`O2logic.md` uses 2500 RPM. Keep ECU deltas on the 3500–4500 band.

Citation: EcuSignatures.md introductory section (stoichiometry, LOAD_PCT formula,
700–800 / 3500–4500 RPM bands). LOAD_PCT field range OBDLab_KG_Wiki §3.1.


## Core Entities

- LOAD_PCT, normalized_obd_lambda, lambda_chem
- perception_contradiction.detect (live consumer)
- RpmStateBucket.STABILIZED_IDLE, RpmStateBucket.STRESS_IDLE
- LOW_IDLE, STRESS_IDLE

## Graph relations (explicit)

**perception_contradiction.detect** COMPARES **normalized_obd_lambda** with **lambda_chem**
**ECU_HARDWARE_FAULT** ISOLATED_BY **perception_contradiction** divergence
**perception_contradiction.detect** SUPPRESSES sensor-bias when **lambda_chem** outside 0.90-1.10
**LOAD_PCT** MAPS_TO **calculated_engine_load_pct**
**LOW_IDLE** MAPS_TO **RpmStateBucket.STABILIZED_IDLE**
**STRESS_IDLE** MAPS_TO **RpmStateBucket.STRESS_IDLE**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
