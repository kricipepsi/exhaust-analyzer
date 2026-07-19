---
proposal_id: EP-OBD-12
title: LTFT adaptive cell-matrix mapping (RPM × Load → idle / cruise / WOT cells)
target_lab: OBDLab (KG) → COMLab load-cell analyzer
source: proposals/AddObdFields.md §Part 1.3; chunks/fuel-trim/13
type: analytics_module
status: PROPOSAL (consumer proposed, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Model the PCM's LTFT adaptive memory as a physical cell matrix keyed by **RPM × Calculated
Load (or MAF g/s)**, mapping PIDs to named cells (Idle / Cruise / Power-Enrichment-WOT).

## Diagnostic rationale
Highly positive LTFT strictly in low-load cells (<20 %) that normalise in high-load cells
(>50 %) automatically isolates a vacuum leak downstream of the throttle body. Cell-vector
localisation (idle-only / part-throttle-only / global) is the discriminator a scalar
total-trim cannot provide.

## Proposed consumer + code path
COMLab **load-cell trim analyzer** ([[EP-COM-09_ltft-cell-vector-analyzer]]) reads the
`ltft_cell_vector`. This proposal supplies the OBDLab-side cell map; EP-COM-09 supplies
the COMLab reader. Field + consumer ship together.

## Dependencies / related
[[EP-COM-09_ltft-cell-vector-analyzer]] · [[EP-OBD-IN-01_calculated-load-pid]].
