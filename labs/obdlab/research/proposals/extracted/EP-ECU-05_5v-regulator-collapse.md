---
proposal_id: EP-ECU-05
title: ECU fault node — internal 5 V regulator rail collapse
target_lab: fault-atlas (new node) → COMLab ECU checker
source: chunks/ecu-diagnosis/06; proposals/OBD_ImplProp.md FAULT 2
type: fault_node
status: PROPOSAL (consumer = EP-COM-04; refines ERR-EF-006)
date_extracted: 2026-06-07
---

## Signature
The internal 5 V reference sags (e.g. to 4.1 V). All ratiometric sensors (TPS, MAP) read
suppressed: TPS ≈ 0 %, calc-load ≤ 8–10 %, but **both-bank trims pinned ≥ +40 %** and a
**NOx spike** — the ECU commands maximum enrichment while the engine actually runs lean.
Global (both-bank) lean distinguishes it from the single-bank injector-driver fault.

## Proposed consumer + code path
[[EP-COM-04_ecu-hardware-fault-checker]] (symptom → LEAN_MIXTURE / HIGH_COMBUSTION_TEMP).
Cross-refs VE collapse ([[EP-OBD-10_ve-engine-classifier]] FAULT_VE_IDLE_COLLAPSE).
Register in `comlab/config/proposals/`.

## Related
[[EP-OBD-10_ve-engine-classifier]] · [[EP-OBD-13_bank-asymmetry-audit]] (symmetric ⇒ here).
