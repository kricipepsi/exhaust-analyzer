---
chunk: fuel-trim/12_emissions-egr-evap-catalyst-idle-module-cases
topic: fuel-trim
sources:
  - FuelTrimFamilies.md §"Fault Family 3: P04xx" + §"Family 4: P05xx" + §"Family 5: P06xx" (cases 15–20)
consumer: COMLab fault_atlas_router routing into rich_mixture / catalyst_failure / lean_condition / ecu_fault families (ERR-RM-004, ERR-CF-001, ERR-LC-001, ERR-ECU-001). One mechanism is a new-fault PROPOSAL (egr_insufficient_flow). One case (small EVAP leak) has no fuel-trim signal and is logged out-of-scope.
consumer_status: MIXED (active families + 1 proposal)
provenance: sources/fuel-trim/FuelTrimFamilies.md
related: [[09_fault-family-case-matrix]], [[04_trim-pattern-decision-tree]], [[../o2-logic/05_bias-vs-real-truth-perception]]
---

# P04xx / P05xx / P06xx — EGR, EVAP, catalyst, idle control, control modules

## EGR (the "absence of a shift" signal)

- **EGR insufficient flow (row 15, P0401) — PROPOSAL.** When EGR opens correctly it
  displaces intake O₂ → upstream O₂ drops → STFT rises briefly: `EGR open ⟹ (O₂↓ and
  STFT↑)`. A slow/weak valve produces **no such shift**, so P0401 sets while idle
  trims stay 0/0. The diagnostic signal is the *absence* of the expected trim
  perturbation when EGR is commanded — the inverse of `ERR-LC-005 egr_stuck_open`.
  No node captures insufficient flow. Register `egr_insufficient_flow`; consumer =
  fault_atlas EGR routing comparing commanded-EGR vs observed STFT response.

## EVAP

- **Stuck-open purge valve (row 16, ERR-RM-004).** Raw vapour floods intake,
  especially after refuel → upstream O₂ locks 0.9 V (P2196 stuck-rich) → STFT/LTFT
  driven to −25 %. Solenoid resistance normal (24 Ω) ⇒ mechanical, not electrical.
  Maps to `evap_purge_valve_stuck_open`.
- **Small EVAP leak (row 17, P0442).** Set by the vacuum-decay self-test; **no
  driveability symptom and trims stay 0/0**. No fuel-trim consumer — logged here as
  out-of-scope for fuel-trim routing (it is a monitor-only EVAP fault; belongs to a
  dedicated EVAP-monitor path, not the trim engine).

## Catalyst

- **Catalyst efficiency loss (row 18, P0420, ERR-CF-001).** Trims near-normal
  (+2/+4) — the converter, not fuelling, is the fault. Downstream O₂ *mimics*
  upstream switching (lost O₂ storage) instead of a flat ~0.45 V. Maps to
  `catalyst_efficiency_below_threshold`. Cross-ref o2-logic downstream chunk; root
  cause here was oil-poisoning (worn valve seals) — a cross-family link to
  `ERR-RM-001`.

## Idle control

- **IAC body gasket leak (row 19, P0505, maps ERR-LC-001).** Unmetered air past a
  torn IAC gasket → hunting idle (1100–1500 RPM) + lean bias +12/+18 that recovers
  at 2500 RPM — a vacuum-leak signature localised to the idle-control path. Routes
  to `vacuum_leak_post_maf`; optional refine `idle_air_control_leak` for the
  hunting-RPM + IAC-step-at-0 co-signature.

## Control modules

- **False ECM fault from O₂ heater (row 20, P0606, ERR-ECU-001 + sensor_fault).**
  Corroded upstream O₂ heater pins (12.4 Ω → >150 Ω on wiggle) → inductive spike on
  the ground → ECM misreads it as an internal sync fault → P0606 + limp mode,
  closed-loop disabled (trims 0/0). The lesson: P0606 is **not** always an internal
  ECU fault — rule out heater-circuit transients first. Maps to ERR-ECU-001 with a
  sensor_fault (O₂ heater) differential. (Cross-ref ecu-diagnosis: this is the
  external-vs-internal ECU distinction made there.)

Citation: FuelTrimFamilies.md cases 15–20 (trim values, EGR-flow O₂/STFT relation,
purge/heater resistances, P0420 downstream-O₂ behaviour). Node IDs per comlab/config.


## Core Entities

- P0401, P0446, P1450, P0442, P0420, P0505, P0606
- EGR_INSUFFICIENT_FLOW, EVAP_PURGE_STUCK_OPEN, CATALYST_EFFICIENCY_LOSS, IAC_LEAK
- fault_atlas_router (consumer; 1 PROPOSAL)

## Graph relations (explicit)

**EGR_open** LOWERS upstream **O2** and RAISES **STFT** briefly
**P0401** INDICATES **EGR_INSUFFICIENT_FLOW** (absence of expected STFT shift)
**P0446** plus **P1450** INDICATES **EVAP_PURGE_STUCK_OPEN**
**EVAP_PURGE_STUCK_OPEN** DRIVES **LTFT** to -25%
**P0420** INDICATES **CATALYST_EFFICIENCY_LOSS**
**P0505** INDICATES **IAC_LEAK** vacuum-leak variant
**P0606** DOES_NOT_ALWAYS_IMPLY internal ECU fault (rule out O2-heater transient)

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
