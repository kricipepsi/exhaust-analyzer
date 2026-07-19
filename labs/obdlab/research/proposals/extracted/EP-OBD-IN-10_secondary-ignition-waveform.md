---
proposal_id: EP-OBD-IN-10
title: Add secondary-ignition waveform feature set (firing/burn line, coil ripples)
target_lab: OBDLab (manual-entry features) → COMLab fault_atlas ignition
source: various/Vol2.md MD6; chunks/pids-protocol/03
type: input_field
status: PROPOSAL (consumer proposed; manual-entry, no live stream)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Manual-entry waveform features: `firing_kv`, `burn_time_ms`, `coil_ripple_count`,
`polarity`. They resolve what the misfire monitor cannot — ignition failure vs lean
mixture vs low compression.

## Diagnostic rationale
High firing line + short burn = high resistance (worn plug / lean / open wire); low
firing + long spark = rich / fouled / low compression; <3 post-spark ripples = shorted
coil. The discriminator behind the misfire-vs-fuelling gate.

## Proposed consumer + code path
COMLab `fault_atlas_router` ignition family reads the features. No live OBD stream supplies
them — so the consumer must be specced before any field ships (signal/noise).

## Dependencies / related
[[EP-COM-07_misfire-vs-fuelling-gate]] · [[EP-ECU-03_coil-driver-failure]] · chunks/pids-protocol/03.
