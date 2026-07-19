---
chunk: delta-relations/02_profile-vacuum-leak
topic: delta-relations
sources:
  - FuelTrimW.md — "Profile 1: Intake Manifold Vacuum Leak / Unmetered Air"
consumer: PENDING (COMLab delta-calculation script — SWEEP_MANIFEST FU-2)
consumer_status: PENDING
dedup: quantified delta version of the "vacuum leak" row in fuel-trim/04_trim-pattern-decision-tree
---

# Delta profile 1 — intake manifold vacuum leak / unmetered air

| Measure | Value |
|---|---|
| Low idle total trim | highly positive, **+15 % … +25 %** |
| Stress idle total trim | normalises, **≈ 0 % … +5 %** |
| **ΔTrim** | **large negative, ≤ −10 %** |

**Aerodynamic mechanism.** At low idle the throttle plate is nearly closed,
creating high manifold vacuum (typically **18–22 in-Hg**). That pressure
differential pulls unmetered air through cracks in intake gaskets, vacuum lines,
or injector O-rings **downstream of the MAF**. Because total idle airflow is very
low, the leak is a large fraction of the charge → lean → high positive trim. At
3500–4500 RPM the throttle opens, manifold vacuum drops, metered airflow rises,
and the (roughly constant absolute) leak becomes a negligible fraction → trims
normalise → strongly negative ΔTrim.

Architecture caveat: this positive-trim signature is the **MAF/MAP closed-loop**
behaviour; on a pure speed-density (MAP) system a vacuum leak does **not** shift
trim — see `06_architecture-modifiers` (Speed-Density paradox).

Citation: magnitudes, ΔTrim ≤ −10 %, 18–22 in-Hg per FuelTrimW.md Profile 1.
Consumer PENDING per SWEEP_MANIFEST §7 / FU-2.


## Core Entities

- VACUUM_LEAK, DELTA_TRIM, LTFT
- MAF_CLOSED_LOOP, SPEED_DENSITY
- LOW_IDLE, STRESS_IDLE

## Graph relations (explicit)

**VACUUM_LEAK** RAISES **LTFT** at **LOW_IDLE**
**VACUUM_LEAK** PRODUCES_NEGATIVE **DELTA_TRIM**
**VACUUM_LEAK** REQUIRES **MAF_CLOSED_LOOP**
**SPEED_DENSITY** NULLIFIES **VACUUM_LEAK** delta
**VACUUM_LEAK** DISCRIMINATES_FROM **EXHAUST_BACKPRESSURE** by stress-idle sign

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
