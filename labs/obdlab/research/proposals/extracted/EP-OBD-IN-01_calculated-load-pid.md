---
proposal_id: EP-OBD-IN-01
title: Add Calculated Engine Load PID (0x04) as an OBDLab input field
target_lab: OBDLab (input) → COMLab (consumer)
source: proposals/AddObdFields.md §Part 1.1; proposals/OBD_ImplProp.md; chunks/ecu-diagnosis/01
type: input_field
status: PROPOSAL (consumer proposed, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Ingest SAE J1979 **Calculated Engine Load** (PID `0x04`, `calculated_engine_load_pct`,
0–100 %). Altitude-corrected (barometric term), so it must reach ~100 % at WOT
regardless of elevation on both NA and forced-induction engines.

## Diagnostic rationale
- **WOT sensor sanity check:** throttle at 100 % but load stalls at 70–80 % ⇒ airflow
  restriction or severely under-reporting MAF.
- **Idle parasitic drag:** warm idle, no accessories should sit 15–25 %; >35 % ⇒ heavy
  internal mechanical resistance, failing alternator, or tight block.

## Proposed consumer + code path
`comlab/core/fault_atlas_router.py` — load-cell categoriser (idle / cruise / WOT cell)
and the airflow-restriction discriminator. Field already present in
`OBDLivePayload.calculated_engine_load_pct` (verified live), so this is mostly
"name the COMLab reader," not a new schema field.

## Dependencies / related
[[EP-OBD-IN-02_absolute-load-pid]] (VE cross-ref) · [[EP-OBD-IN-06_baro-pid]]
(altitude term) · [[EP-OBD-12_ltft-cell-matrix]] (load axis of the cell map) ·
[[EP-COM-01_idle-transition-delta-engine]] (ΔLoad).

## Open questions
- Is the WOT closed-form evaluator (ECU-FU-4) needed, or is reading the PID enough?
- Confirm fault_atlas actually branches on load-cell today vs. just reading the value.
