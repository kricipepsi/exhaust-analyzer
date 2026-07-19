---
chunk: fuel-trim/16_three-speed-trim-test
topic: fuel-trim
sources:
  - various/Vol2.md — Master Document 3 (Fuel Trim Logic); various/Vol3.md — PID-without-DTC profiling
consumer: COMLab delta engine + fault_atlas — the idle / 2500 RPM / cruise trim sweep that separates vacuum leak (idle-only) from fuel-delivery restriction (worsens with load) from MAF "double-whammy" (rich idle/lean load).
consumer_status: active (maps to existing fault_atlas families) + PENDING for the load-axis delta (FU-2)
provenance: sources/various/Vol2.md MD3 + Vol3.md — logic/prose READABLE; the total-trim display equation in Vol3 was stripped (it is the standard total=STFT+LTFT, in fuel-trim/01)
dedup: complements fuel-trim/04 (idle-vs-2500 static pattern) and delta-relations/01-05 (ΔTrim). THIS adds the third (cruise/load) point + the MAF double-whammy signature.
---

# Three-speed fuel-trim test

Monitoring total trim (STFT+LTFT) at **three** operating points resolves faults that
look identical at any single point.

```
points:  idle (~800 RPM)  |  2500 RPM (no load)  |  cruise / under load

vacuum leak        : +trim at idle only      -> improves with RPM (leak negligible vs metered air)
fuel delivery limit: normal idle             -> +trim worsens under load (pump/filter can't keep volume)
MAF contamination  : "double whammy"         -> rich at idle / lean under load (mis-weighs air at different flows)
systemic rich      : -trim at all points     -> excess pressure / EVAP / GDI seal leak
bank imbalance     : split B1 vs B2 (>~10%)  -> injector or valve-timing localised to one bank
```

## Logic
The classic single-point trap: a +trim at idle could be a vacuum leak or a weak pump.
The **direction of change across the speed/load sweep** is the discriminator — a vacuum
leak attenuates, a fuel-delivery limit intensifies. The MAF "double-whammy" (positive at
idle, negative — or vice versa — under load) is uniquely a contaminated-sensor signature.

## Consumer / code path
The idle-vs-2500 static split is active in fault_atlas (fuel-trim/04). The cruise/load
third point + its delta require the COMLab delta engine (FU-2). `total_trim = STFT+LTFT`
per fuel-trim/01. Numeric DTC thresholds (±18/±25) per fuel-trim/03.


## Core Entities

- TOTAL_TRIM, VACUUM_LEAK, FUEL_STARVATION, MAF_UNDERREPORT
- COMLab delta engine + fault_atlas (consumer; load-axis PENDING FU-2)

## Graph relations (explicit)

**VACUUM_LEAK** RAISES trim at idle only and improves with RPM
**FUEL_STARVATION** WORSENS trim under load
**MAF_UNDERREPORT** PRODUCES double-whammy rich-idle lean-load
**three-speed-trim-test** DISCRIMINATES by direction of change across the sweep
load-axis delta CONSUMED_BY **COMLab delta engine** (PENDING FU-2)

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
