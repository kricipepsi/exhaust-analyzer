---
proposal_id: EP-FA-03
title: Fault node — thermally intermittent injector (cold-only single-bank lean)
target_lab: fault-atlas (air-fuel metering)
source: chunks/fuel-trim/09 case 9
type: fault_node
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## Signature
Single-bank **+STFT only when cold** that normalises once warm — an injector whose flow is
restricted at low temperature. Distinct from a steady-state lean fault.

## Proposed consumer + code path
`fault_atlas_router.py` keyed on (cold-state single-bank +STFT AND warm-state normal),
which needs the dual-frame / thermal-state context. Register in `comlab/config/proposals/`.

## Related
[[EP-COM-02_dual-frame-stateframe]] · [[EP-OBD-13_bank-asymmetry-audit]].
