---
proposal_id: EP-OBD-IN-05
title: Add Absolute/Relative Throttle Position PIDs (0x11 / 0x45 — TP / TP_R)
target_lab: OBDLab (input) → COMLab (fault_atlas idle-leak validator)
source: proposals/AddObdFields.md §Part 2.3; proposals/OBD_ImplProp.md (TPS gates)
type: input_field
status: PROPOSAL (consumer proposed; field gap)
date_extracted: 2026-06-07
---

## What it proposes
Ingest **Throttle Position** (absolute `0x11` / relative `0x45`, `throttle_pos_pct`,
`throttle_rel_pct`) — plate angle vs learned closed-idle stop. The ecu-diagnosis pass
flagged TPS as a **payload field gap** (absent from `OBDLivePayload` today).

## Diagnostic rationale
- **Idle air-leak validator (P0505):** TP_R = 0 % (closed) but RPM high (~1500) and load
  high ⇒ unmetered air bypassing the blade (manifold crack, blown IAC gasket, stuck-open
  purge). Δ-signature: ΔTP_R > 15 % from low→high idle ⇒ intake/filter/backpressure
  restriction; ΔTP_R ≈ 0 with surging RPM ⇒ unmetered-air bypass.
- **ECU ground-trace tell:** TPS pinned 100 % at idle is a key signature for
  [[EP-ECU-04_sensor-ground-trace-blown]].

## Proposed consumer + code path
`comlab/core/fault_atlas_router.py` idle-air-leak validator + the ECU-fault checker
([[EP-COM-04_ecu-hardware-fault-checker]]). Add `throttle_pos_pct` (and rel) to
`OBDLivePayload`.

## Dependencies / related
[[EP-ECU-04_sensor-ground-trace-blown]] · [[EP-COM-01_idle-transition-delta-engine]] (ΔTP_R).
