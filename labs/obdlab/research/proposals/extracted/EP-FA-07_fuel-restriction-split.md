---
proposal_id: EP-FA-07
title: Fault refinement — split fuel-delivery restriction (clogged filter vs weak pump)
target_lab: fault-atlas (refines ERR-LC-003)
source: chunks/fuel-trim/09 case 2; chunks/fuel-trim/README
type: fault_refinement
status: PROPOSAL (named consumer, refines existing node)
date_extracted: 2026-06-07
---

## Signature
Both present as current-normal at idle + positive trim spike under load. Discriminator:
a **pressure drop strictly under high-flow demand** that recovers at idle points to a
**restricted filter**; a pump that cannot hold rail pressure even at moderate demand
points to a **weak pump**. Refines the single `ERR-LC-003` into two dispositions.

## Proposed consumer + code path
`fault_atlas_router.py` ERR-LC-003 branch reading fuel-rail-pressure-vs-load and the
stress-idle trim delta. Register the refinement in `comlab/config/proposals/`.

## Related
[[EP-COM-01_idle-transition-delta-engine]] · [[EP-COM-06_traditional-fault-signature-matrix]].
