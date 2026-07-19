---
proposal_id: EP-FA-06
title: Fault node — EGR insufficient flow (commanded-EGR vs observed-trim response)
target_lab: fault-atlas (EGR / auxiliary emissions)
source: chunks/fuel-trim/09 case 15; sources/taxonomy/faultatlas.md (P0401)
type: fault_node
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## Signature
Carbon-blocked EGR (P0401): commanded EGR produces no corresponding STFT response —
the inverse pattern of an EGR-stuck-open (ERR-LC-005) lean event. Diagnosed by comparing
commanded-EGR against the observed trim reaction.

## Proposed consumer + code path
`fault_atlas_router.py` EGR node keyed on (commanded EGR > 0 AND ΔSTFT ≈ 0). Register in
`comlab/config/proposals/`.

## Related
[[EP-COM-06_traditional-fault-signature-matrix]] · [[EP-DTC-02_j2012-fault-taxonomy]].
