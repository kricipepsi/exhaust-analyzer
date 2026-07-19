---
proposal_id: EP-OBD-IN-04
title: Add Control Module Voltage PID (0x42 / VPWR) as an OBDLab input field
target_lab: OBDLab (input) → COMLab (perception_contradiction)
source: proposals/AddObdFields.md §Part 2.2; proposals/DataFlow.md (delta logic)
type: input_field
status: PROPOSAL (consumer proposed, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Ingest **Control Module Voltage** (PID `0x42`, `control_module_voltage_v`) — supply
voltage at PCM pins. Sensors need a clean DC rail; <12.0 V or >15.0 V (or high AC
ripple) drifts references, shifts stoichiometric points, and triggers false processor
codes (e.g. false P0606 on some Toyotas).

## Diagnostic rationale
Unstable trim delta with `VPWR` <11.5 V ⇒ flag a charging/ground fault **before**
blaming air/fuel sensors. Δ-signature: ΔVPWR < −1.0 V under revs ⇒ alternator/regulator
diode; ΔVPWR > +2.5 V (system >15.5 V) ⇒ over-charging, AC ripple corrupts references.

## Proposed consumer + code path
`comlab/core/perception_contradiction.py` — electrical-health pre-check that suppresses
sensor-fault routing when the rail is out of band. Pairs with the charging-system fault
node [[EP-FA-05_alternator-ac-ripple]].

## Dependencies / related
[[EP-COM-01_idle-transition-delta-engine]] (ΔVPWR) · [[EP-FA-05_alternator-ac-ripple]] ·
[[EP-ECU-01_capacitor-leakage]].
