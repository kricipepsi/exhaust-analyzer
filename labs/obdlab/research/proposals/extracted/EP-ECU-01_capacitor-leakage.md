---
proposal_id: EP-ECU-01
title: ECU fault node — liquid-electrolyte capacitor leakage / board corrosion
target_lab: fault-atlas (new node) → COMLab ECU checker
source: chunks/ecu-diagnosis/02; proposals/OBD_ImplProp.md FAULT 7; proposals/wikiResearch.md §2
type: fault_node
status: PROPOSAL (consumer = EP-COM-04; refines ecu_fault.json)
date_extracted: 2026-06-07
---

## Signature
Conductive electrolyte on the PCB creates high-impedance shorts on sensor reference lines.
AC ripple (worse at high RPM as alternator output rises) introduces clock jitter →
ECU drops to open-loop fault. **Symmetric ±15 % STFT** at idle, `fuel_sys_status` = CL at
idle but **OL_FAULT at stress idle**, calc-load collapses (≥15 % → <10 %). Δδ ≈ +0.10.

## Why it ships as a proposal
v1 cannot detect this; refines existing `ecu_fault.json` (sharpens, not duplicates). The
named consumer is the ECU-hardware-fault checker — field + consumer ship together.

## Proposed consumer + code path
[[EP-COM-04_ecu-hardware-fault-checker]] discriminator (symmetric-trim + OL_FAULT-on-rev).
Register node in `comlab/config/proposals/`.

## Related
[[EP-FA-05_alternator-ac-ripple]] (distinguish charging-side ripple) ·
[[EP-OBD-IN-03_fuel-system-status-pid]] · [[EP-OBD-IN-04_control-module-voltage-pid]].
