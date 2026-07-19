---
chunk: delta-relations/03_profile-fuel-starvation
topic: delta-relations
sources:
  - FuelTrimW.md — "Profile 2: Fuel Supply Starvation"
consumer: PENDING (COMLab delta-calculation script — SWEEP_MANIFEST FU-2)
consumer_status: PENDING
dedup: quantified delta version of the "fuel delivery" row in fuel-trim/04_trim-pattern-decision-tree
---

# Delta profile 2 — fuel supply starvation

| Measure | Value |
|---|---|
| Low idle total trim | normal/slightly positive, **≈ 0 % … +5 %** |
| Stress idle total trim | escalates, **+15 % … +25 %** |
| **ΔTrim** | **large positive, ≥ +10 %** |

**Pneumatic mechanism.** At low idle the fuel volume needed for stoichiometry is
minimal, so even a weak pump, partially clogged filter, or leaking pressure-
regulator diaphragm can hold target rail pressure → trims normal. At 3500–4500 RPM
the engine demands far more fuel per second; the supply restriction drops actual
rail pressure → lean → ECU maximises positive trim → large positive ΔTrim.

Discriminator vs MAF under-report (`04`): both worsen under load (positive ΔTrim);
they are separated by the low-idle starting value (starvation starts near 0 %; MAF
under-report can start slightly higher and climbs further) and by corroborating
PIDs (fuel rail pressure vs MAF g/s plausibility).

Citation: magnitudes and ΔTrim ≥ +10 % per FuelTrimW.md Profile 2.
Consumer PENDING per SWEEP_MANIFEST §7 / FU-2.


## Core Entities

- FUEL_STARVATION, DELTA_TRIM, LTFT
- MAF_UNDERREPORT
- LOW_IDLE, STRESS_IDLE

## Graph relations (explicit)

**FUEL_STARVATION** PRODUCES_POSITIVE **DELTA_TRIM**
**FUEL_STARVATION** RAISES **LTFT** at **STRESS_IDLE**
**FUEL_STARVATION** DISCRIMINATES_FROM **MAF_UNDERREPORT** by low-idle band and fuel-rail-pressure PID

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
