---
proposal_id: EP-FA-01
title: Fault node — MAF circuit ground-open failsafe (speed-density limp)
target_lab: fault-atlas (sensor_fault family) → COMLab
source: chunks/fuel-trim/09 case 3; chunks/fuel-trim/README
type: fault_node
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## Signature
P0102 (MAF low) + **negative both-bank trim** ⇒ ECU has dropped to a speed-density
failsafe map that over-fuels (runs rich). Distinct from a dirty-MAF under-report (which
runs lean / positive trim).

## Proposed consumer + code path
`fault_atlas_router.py` sensor_fault, keyed on (P0102 AND both-bank trim < 0). Register
in `comlab/config/proposals/`.

## Related
[[EP-OBD-IN-02_absolute-load-pid]] · [[EP-DTC-01_dtc-causal-hierarchy]].
