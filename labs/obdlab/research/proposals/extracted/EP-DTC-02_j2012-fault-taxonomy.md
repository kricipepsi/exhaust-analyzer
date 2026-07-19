---
proposal_id: EP-DTC-02
title: SAE J2012 / ISO 15031-6 eight-family fault taxonomy backbone
target_lab: DTCLab + fault-atlas
source: sources/taxonomy/faultatlas.md; sources/taxonomy/faultlist.md
type: reference_taxonomy
status: PROPOSAL (backbone for fault-atlas routing)
date_extracted: 2026-06-07
---

## What it proposes
Adopt the 8 standard Powertrain P-code families as the routing backbone (1990–2010
petrol): Air&Fuel Metering (P01xx/P02xx), Ignition&Misfire (P03xx), Auxiliary Emissions
(P04xx), Speed&Idle (P05xx), Computer&Output (P06xx) — each with subfault categories and
canonical DTCs, structured as Family → Subfault → Target-DTCs.

## Diagnostic rationale
Gives fault-atlas a standards-aligned hierarchy so every case and proposal node has a
defined home; the P06xx family is exactly where the internal-ECU proposals attach.

## Proposed consumer + code path
`comlab/config/kg/*` family registry + `fault_atlas_router.py`. Many `EP-FA-*` and
`EP-ECU-*` nodes register under these families.

## Related
[[EP-COM-06_traditional-fault-signature-matrix]] · [[EP-DTC-01_dtc-causal-hierarchy]] ·
all `EP-ECU-*` (P06xx) and `EP-FA-*`.
