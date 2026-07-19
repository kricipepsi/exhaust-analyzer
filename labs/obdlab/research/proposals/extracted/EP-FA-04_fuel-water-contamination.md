---
proposal_id: EP-FA-04
title: Fault node — fuel water/contamination (random multi-misfire + positive trim)
target_lab: fault-atlas (air-fuel metering / misfire)
source: chunks/fuel-trim/09 case 10
type: fault_node
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## Signature
P0300 random/multi-cylinder misfire + positive trim, with **normal compression and
spark** — points to contaminated fuel (water) rather than a mechanical or ignition cause.

## Proposed consumer + code path
`fault_atlas_router.py` keyed on (P0300 random AND +trim AND no single-cylinder
dominance AND compression/spark normal). Register in `comlab/config/proposals/`.

## Related
[[EP-OBD-IN-07_per-cylinder-misfire-counts]] (random vs localised) ·
[[EP-COM-07_misfire-vs-fuelling-gate]].
