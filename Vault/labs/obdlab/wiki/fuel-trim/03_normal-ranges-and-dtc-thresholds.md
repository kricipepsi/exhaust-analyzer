---
chunk: fuel-trim/03_normal-ranges-and-dtc-thresholds
topic: fuel-trim
sources:
  - master_fuel_trim_guide.md §3
  - Research10.md §1 (per-family magnitudes, real-world DTC threshold)
  - Research10.md §2 (±127/±99 sentinel as range limit)
consumer: fault-atlas routing — Air-&-Fuel-Metering family; the threshold ladder selects P0171/P0174 (lean) vs P0172/P0175 (rich) and the investigational/confirmed bands gate symptom severity
consumer_status: active
dedup: canonical range/threshold table; supersedes range mentions in fuel-trim.md, Fuel Trim Diagnostics.txt, Eastern-Manufacturing.md
---

# Normal operating ranges and DTC thresholds

## Healthy ranges (warm, closed loop)

| Condition | STFT normal | LTFT normal | Total trim normal |
|---|---|---|---|
| Idle, warm, closed loop | −5 % … +5 % (bouncing) | −10 % … +10 % | within ±10 % |
| Steady cruise (60–100 km/h) | −5 % … +5 % (bouncing) | −10 % … +10 % | within ±10 % |
| Bank-to-bank match (V-engines) | within ±5 % between banks | within ±5 % between banks | — |

## Severity ladder (total trim)

- within **±10 %** — healthy.
- **±10 % … ±20 %** — investigational.
- **> ±20 %** — confirmed mixture problem.

A tighter service-tip threshold exists: some sources flag **> ±8 %** as warranting
a diagnostic check (Research10 §1). The 4D engine uses ±10 % as the healthy bound
and treats ±8–10 % as borderline rather than clean.

## DTC trigger thresholds

- LTFT ≈ **+25 %** sustained → **P0171** (B1) / **P0174** (B2), Type A.
- LTFT ≈ **−25 %** sustained → **P0172** (B1) / **P0175** (B2), Type A.
- The actual manufacturer code-set point is often **lower**, around **±18 %** total
  (STFT+LTFT) on many vehicles; Toyota documents total trim within ±35 % as still
  "normal" by its own calibration. Implication: by the time a lean/rich DTC sets,
  trims may already be large — absence of a code does **not** mean trims are clean
  (Research10 §1).

## Register limit / sentinel

- **±127 %** is the absolute signed-8-bit register limit; **±99 %** values seen on
  scan tools indicate the ECU is commanding maximum correction. Both are
  **sentinel/range-limit values**, not physically plausible measured trims — treat
  a pegged value as "very large deviation, exact magnitude meaningless" (detail in
  `06_trim-rails-and-sentinels`). Rare in normal closed loop with a healthy sensor
  (Research10 §2).

Citation: SAE J1979 (signed-8-bit trim PIDs, ±127 % limit); P0171/P0172/P0174/P0175
per SAE J2012 / ISO 15031-6.


## Core Entities

- LTFT, TOTAL_TRIM, P0171, P0172, P0174, P0175
- register sentinel +/-127, +/-99
- fault-atlas routing (consumer, active)

## Graph relations (explicit)

**LTFT** at +25% TRIGGERS **P0171** and **P0174**
**LTFT** at -25% TRIGGERS **P0172** and **P0175**
**TOTAL_TRIM** above +/-20% INDICATES confirmed mixture problem
**TOTAL_TRIM** at +/-127% IS register sentinel (not a measured trim)
absence of DTC DOES_NOT_IMPLY clean **TOTAL_TRIM**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
