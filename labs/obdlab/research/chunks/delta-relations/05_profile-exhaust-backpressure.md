---
chunk: delta-relations/05_profile-exhaust-backpressure
topic: delta-relations
sources:
  - FuelTrimW.md — "Profile 4: Exhaust System Backpressure / Restriction"
consumer: PENDING (COMLab delta-calculation script — SWEEP_MANIFEST FU-2)
consumer_status: PENDING
dedup: no equivalent row in fuel-trim/04 (that table is leak/metering-centric); this is a delta-only signature
---

# Delta profile 4 — exhaust system backpressure / restriction

| Measure | Value |
|---|---|
| Low idle total trim | normal, **≈ 0 %** |
| Stress idle total trim | turns negative, **≤ −12 %** (or engine stumbles / cannot hold high RPM) |
| **ΔTrim** | **significant negative, ≤ −10 %** |

**Physical mechanism.** At low idle, exhaust volume is low; a partially clogged
catalytic converter or crushed pipe still vents without excess backpressure → trims
normal. At 3500–4500 RPM, exhaust volume rises sharply; the restriction builds a
high backpressure wave that traps burnt inert gas in the cylinders, cutting
volumetric efficiency. The cylinders draw an incomplete fresh charge → locally rich
→ upstream O₂ sees low oxygen → ECU drives trims **negative** → significant negative
ΔTrim.

Discriminator vs vacuum leak (`02`): both give negative ΔTrim, but opposite trim
*sign behaviour* — vacuum leak starts **high positive** at idle and falls toward 0;
backpressure starts **near 0** and goes **negative** under load. The stress-idle
sign separates them.

Citation: magnitudes, stress ≤ −12 %, ΔTrim ≤ −10 % per FuelTrimW.md Profile 4.
Consumer PENDING per SWEEP_MANIFEST §7 / FU-2.


## Core Entities

- EXHAUST_BACKPRESSURE, DELTA_TRIM
- VACUUM_LEAK
- LOW_IDLE, STRESS_IDLE

## Graph relations (explicit)

**EXHAUST_BACKPRESSURE** PRODUCES_NEGATIVE **DELTA_TRIM**
**EXHAUST_BACKPRESSURE** LOWERS **TOTAL_TRIM** at **STRESS_IDLE**
**EXHAUST_BACKPRESSURE** DISCRIMINATES_FROM **VACUUM_LEAK** by stress-idle trim sign

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
