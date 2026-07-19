---
proposal_id: EP-FA-05
title: Fault node — alternator AC ripple corrupting sensor references
target_lab: fault-atlas (charging system) → COMLab
source: chunks/fuel-trim/09 case 14
type: fault_node
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## Signature
A failed alternator rectifier diode injects AC ripple onto the supply, corrupting CMP/CKP
and sensor reference signals → erratic trims, intermittent misfire-like noise, false
processor codes. The charging-side analogue of capacitor-leak ripple (distinguish via
VPWR / external charging test, not internal-ECU symmetry).

## Proposed consumer + code path
`fault_atlas_router.py` charging_system + CMP/CKP-noise route, reading
[[EP-OBD-IN-04_control-module-voltage-pid]] (ΔVPWR). Register in `comlab/config/proposals/`.

## Related
[[EP-ECU-01_capacitor-leakage]] (internal vs charging-side disambiguation) ·
[[EP-COM-01_idle-transition-delta-engine]].
