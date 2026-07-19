---
chunk: pids-protocol/03_secondary-ignition-waveform-forensics
topic: pids-protocol
sources:
  - various/Vol2.md — Master Document 6 (Secondary Ignition Waveform Analysis)
consumer: COMLab fault_atlas ignition family — discriminates ignition failure from lean mixture, which a misfire monitor alone cannot. Resolves the "false-lean misfire" confound.
consumer_status: PROPOSAL (waveform-derived features have no live reader; names fault_atlas ignition consumer). Likely a manual-entry feature set, not a live PID stream.
provenance: sources/various/Vol2.md — concept/prose READABLE; KV/ms numeric specs partly stripped (flagged in formula wiki)
dedup: new
---

# Secondary ignition waveform forensics

The secondary waveform resolves what the misfire monitor cannot: ignition failure vs
lean mixture vs low compression.

## Features (Vol2 MD6, readable concepts)

- **Firing line** (voltage to bridge the plug gap) **high** + **short burn time** →
  high resistance: worn plug, wide gap, **lean mixture** (less conductive), or open wire.
- **Firing line low** + **long spark line** → rich mixture, fouled plug, or low
  compression.
- **Coil oscillations (ripples) at end of spark line:** ≥3 ripples confirm coil
  energy/health; missing ripples → shorted coil or fouled plug.
- **Reversed polarity spike** common in waste-spark; raises KV requirement.

## Logic
A lean mixture and a worn plug both raise the firing line, but only the burn-time and
ripple count separate them. This is the microscopic resolution the P030x monitor lacks
— the discriminator behind the misfire-vs-fuelling gate (fuel-trim/11, EP-COM-07).

## Consumer / code path
If adopted, fault_atlas ignition family reads manual-entry waveform features
(firing_kv, burn_ms, ripple_count). No live OBD stream supplies these — so this is a
PROPOSAL whose consumer must be specced before any field ships (signal/noise).


## Core Entities

- firing_kv, burn_ms, ripple_count, IGNITION_MISFIRE
- fault_atlas ignition family (PROPOSAL, manual-entry features)

## Graph relations (explicit)

high firing line with short burn INDICATES high resistance or **LEAN_MIXTURE**
low firing line with long spark INDICATES rich, fouled plug, or low compression
three-or-more coil ripples CONFIRM coil health
**firing_kv**, **burn_ms**, **ripple_count** CONSUMED_BY **fault_atlas ignition family**
**secondary-ignition-waveform** DISCRIMINATES ignition from lean (misfire_vs_fuelling)

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
