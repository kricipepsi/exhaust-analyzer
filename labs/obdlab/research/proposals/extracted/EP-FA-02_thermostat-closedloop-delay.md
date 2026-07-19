---
proposal_id: EP-FA-02
title: Fault node — thermostat stuck open → delayed closed-loop entry
target_lab: fault-atlas + analytics_preconditions
source: chunks/fuel-trim/09 case 6; sources/taxonomy/faultatlas.md (P0128)
type: fault_node
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## Signature
Coolant never reaches regulating temp (P0128); the engine lingers in open-loop cold
enrichment, giving persistent `ENGINE_COLD` precondition failures and skewed early trims.

## Proposed consumer + code path
`analytics_preconditions.py` ENGINE_COLD-persistence detector + `fault_atlas_router.py`
thermal-management node. Register in `comlab/config/proposals/`.

## Related
[[EP-OBD-IN-03_fuel-system-status-pid]] · [[EP-COM-08_prerequisite-dtc-gate]].
