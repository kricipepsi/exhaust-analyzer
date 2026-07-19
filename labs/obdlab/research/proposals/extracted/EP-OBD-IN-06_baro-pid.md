---
proposal_id: EP-OBD-IN-06
title: Add Barometric Pressure PID (0x33 / BARO) as an OBDLab input field
target_lab: OBDLab (input) → COMLab (ambient-pressure calibration)
source: proposals/AddObdFields.md §Part 2.4
type: input_field
status: PROPOSAL (consumer proposed, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Ingest **Barometric Pressure** (PID `0x33`, `baro_kpa`) — atmospheric pressure from a
dedicated sensor or MAP at KOEO. Sea-level reference 101.3 kPa; drops with altitude.

## Diagnostic rationale
The engine must scale max-theoretical-airflow equations by local BARO; a MAP that
under-reports ambient BARO forces a lean-biased altitude-compensation map. Static-test
Δ-signature: ΔBARO must be 0 during a stationary low→high idle sweep — a calculated
drop ⇒ collapsed intake hose / restricted airbox pulling vacuum on the ductwork.

## Proposed consumer + code path
`comlab/core/fault_atlas_router.py` ambient-pressure calibration of the airflow model;
feeds the speed-density theoretical-airflow cross-check.

## Dependencies / related
[[EP-OBD-IN-01_calculated-load-pid]] · [[EP-OBD-11_theoretical-airflow-crosscheck]] ·
[[EP-COM-01_idle-transition-delta-engine]] (ΔBARO).
