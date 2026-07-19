---
chunk: delta-relations/06_architecture-modifiers
topic: delta-relations
sources:
  - FuelTrimW.md — "Systemic Mechanical and Chemical Interactions" (Speed-Density paradox; Turbocharged Boost Leaks)
consumer: PENDING (COMLab delta-calculation script — SWEEP_MANIFEST FU-2); the script MUST branch on air-metering architecture before applying profiles 02–05
consumer_status: PENDING
dedup: architecture caveat referenced by 02_profile-vacuum-leak; not in fuel-trim/04
---

# Delta architecture modifiers

The delta profiles (`02`–`05`) assume a MAF / closed-loop architecture. Two cases
**invert or null** the expected delta and must gate any delta-script interpretation.

## Speed-Density (MAP-only) vacuum-leak paradox

On a speed-density engine a vacuum leak does **not** produce a positive trim shift.
Leak air raises manifold absolute pressure; the MAP sensor reads the true higher
pressure, the ECU references a higher VE-table cell and adds matching base fuel, and
the idle-air-control valve closes to hold target RPM. Net: total airflow unchanged,
trims stay **near 0 %**, so **ΔTrim ≈ 0** for a real leak. Instead the leak shows as:

- reduced IAC counts (valve/throttle closes to compensate),
- elevated MAP at idle (e.g. ~45 kPa vs a healthy ~30 kPa),
- idle flare/high idle if the leak exceeds IAC authority.

Implication for the delta script: on MAP-only engines, **do not** run profile `02`;
route to IAC-count / MAP-at-idle checks instead.

## Turbocharged boost leak (sign inversion)

Under boost the intake is positive-pressure; a leak **after** the turbo lets
already-metered air escape. The MAF counted it but it never reached the cylinders →
mixture runs **rich** → trims shift **highly negative** (up to ~−20 % STFT) — the
exact opposite of a naturally-aspirated vacuum leak. The delta script must know
forced-induction state before assigning a positive-trim leak verdict.

Citation: Speed-Density paradox (MAP ~45 vs ~30 kPa) and turbo boost-leak −20 % STFT
per FuelTrimW.md ("Systemic Mechanical and Chemical Interactions").
Consumer PENDING per SWEEP_MANIFEST §7 / FU-2.


## Core Entities

- SPEED_DENSITY, MAF_CLOSED_LOOP, FORCED_INDUCTION, TURBO_BOOST_LEAK
- VACUUM_LEAK, DELTA_TRIM, STFT
- COMLab delta-calculation script (consumer, PENDING FU-2)

## Graph relations (explicit)

**SPEED_DENSITY** NULLIFIES **VACUUM_LEAK** delta
**TURBO_BOOST_LEAK** PRODUCES_NEGATIVE **STFT**
**FORCED_INDUCTION** INVERTS **VACUUM_LEAK** trim sign
**COMLab delta-calculation script** GATES_ON **MAF_CLOSED_LOOP** before profiles 02-05

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
