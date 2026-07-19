---
chunk: delta-relations/04_profile-maf-underreport
topic: delta-relations
sources:
  - FuelTrimW.md — "Profile 3: Mass Airflow (MAF) Sensor Under-Reporting"
consumer: PENDING (COMLab delta-calculation script — SWEEP_MANIFEST FU-2)
consumer_status: PENDING
dedup: quantified delta version of the "MAF under-reading (contaminated)" row in fuel-trim/04_trim-pattern-decision-tree
---

# Delta profile 3 — MAF sensor under-reporting

| Measure | Value |
|---|---|
| Low idle total trim | normal/slightly positive, **≈ 0 % … +8 %** |
| Stress idle total trim | shifts highly positive, **+15 % … +30 %** |
| **ΔTrim** | **major positive, ≥ +10 %** |

**Thermodynamic mechanism.** Contamination (oil from aftermarket filters, dust
bypass) insulates the MAF hot-wire, so it transfers heat poorly to the air stream.
At low idle, airflow velocity is low → error minimal/absorbed by idle adaptation.
At 3500–4500 RPM the actual air mass rises sharply; the insulated wire fails to
register the high-velocity cooling and **under-reports air mass**. The ECU commands
too little fuel → upstream O₂ detects lean → large positive trim → major positive
ΔTrim.

Discriminator vs fuel starvation (`03`): same positive-ΔTrim direction; separate by
the low-idle band (MAF under-report tolerates up to +8 % at idle) and by checking
MAF g/s against expected airflow for the RPM (implausibly low g/s under load points
to MAF).

Citation: magnitudes and ΔTrim ≥ +10 % per FuelTrimW.md Profile 3.
Consumer PENDING per SWEEP_MANIFEST §7 / FU-2.


## Core Entities

- MAF_UNDERREPORT, DELTA_TRIM, LTFT
- FUEL_STARVATION
- LOW_IDLE, STRESS_IDLE

## Graph relations (explicit)

**MAF_UNDERREPORT** PRODUCES_POSITIVE **DELTA_TRIM**
**MAF_UNDERREPORT** RAISES **LTFT** at **STRESS_IDLE**
**MAF_UNDERREPORT** DISCRIMINATES_FROM **FUEL_STARVATION** by MAF g/s plausibility

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
