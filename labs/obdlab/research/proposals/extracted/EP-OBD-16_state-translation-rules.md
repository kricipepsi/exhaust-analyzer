---
proposal_id: EP-OBD-16
title: State-translation rules (STABILIZED_IDLE / STRESS_IDLE / COLD_OPEN_LOOP_INVALID)
target_lab: OBDLab (config/obd_translation_rules.yaml)
source: proposals/OBD_ImplProp.md §1.B
type: config
status: PROPOSAL (consumer = state bucketer; RpmStateBucket exists)
date_extracted: 2026-06-07
---

## What it proposes
Define the operating-state buckets the state machine uses:
- `STABILIZED_IDLE` — RPM BETWEEN 650–850.
- `STRESS_IDLE` — RPM BETWEEN 3500–4500.
- `COLD_OPEN_LOOP_INVALID` — fallback when coolant < 75 °C.

## Diagnostic rationale
The whole low-idle-vs-stress-idle delta method depends on two well-defined RPM bands.
**⚠ Band reconciliation required:** sources disagree — FuelTrimW.md uses 3500–4500,
O2logic.md uses 2500, fuel-trim chunk 04 uses 2500–3000, shipped `RpmStateBucket` uses
STRESS_IDLE 3000–4500. Pick one canonical pair (or per-signal bands) before delta chunks
ship (O2-FU-3 / FU-2).

## Proposed consumer + code path
OBDLab state bucketer maps to `vocabulary.py::RpmStateBucket`; COMLab delta engine keys on
the buckets ([[EP-COM-01_idle-transition-delta-engine]]).

## Dependencies / related
[[EP-OBD-15_physical-sensor-bounds-config]] · [[EP-COM-01_idle-transition-delta-engine]] ·
[[EP-OBD-IN-03_fuel-system-status-pid]].
