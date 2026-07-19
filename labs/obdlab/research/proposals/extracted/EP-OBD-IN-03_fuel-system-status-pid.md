---
proposal_id: EP-OBD-IN-03
title: Add Fuel System Status PID (0x03 / FUELSYS) as an OBDLab input field
target_lab: OBDLab (input) → COMLab (Stage A gate)
source: proposals/AddObdFields.md §Part 2.1; proposals/OBD_ImplProp.md §Gate 2
type: input_field
status: PROPOSAL (consumer proposed; partial enum exists)
date_extracted: 2026-06-07
---

## What it proposes
Ingest **Fuel System Status** (PID `0x03`): OL / CL / OL_Drive / OL_Fault. Fuel-trim
values are **meaningless in Open Loop** (PCM ignoring O₂ feedback, running lookup
tables), so trims must be gated on loop state.

## Diagnostic rationale
ECT high (>80 °C) but `FUELSYS` stuck `OL` with trims flatlined at 0 % ⇒ an active fault
blocking closed-loop transition (dead/unheated O₂ sensor). Also the Δ-signature: CL at
idle dropping to OL_Fault at 2500 RPM ⇒ heat/RPM-dependent O₂ heater or harness fault.

## Proposed consumer + code path
COMLab **Stage A gate** / `analytics_preconditions` — abort or down-weight trim routing
when not in closed loop. Maps onto existing `TrimAnalyticsGate.OPEN_LOOP`. Add the raw
`fuel_system_status` field that feeds the gate.

## Dependencies / related
[[EP-COM-01_idle-transition-delta-engine]] (ΔFUELSYS) · [[EP-OBD-16_state-translation-rules]]
(COLD_OPEN_LOOP_INVALID) · [[EP-ECU-01_capacitor-leakage]] (OL_FAULT at stress idle).
