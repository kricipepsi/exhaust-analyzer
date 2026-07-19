---
proposal_id: EP-COM-09
title: LTFT cell-vector analyzer (idle-only / part-throttle-only / global localisation)
target_lab: COMLab (analytics)
source: chunks/fuel-trim/13; proposals/AddObdFields.md §1.3
type: analytics_module
status: PROPOSAL (consumer for EP-OBD-12)
date_extracted: 2026-06-07
---

## What it proposes
The COMLab reader for the LTFT cell matrix: classify the trim signature as **idle-only**
(vacuum leak / purge downstream of throttle), **part-throttle/load-only** (fuel-delivery
or MAF), or **global** (wide-range fault) from the `ltft_cell_vector`.

## Diagnostic rationale
Cell-localised LTFT is the discriminator a scalar total-trim cannot give; the OBDLab cell
map ([[EP-OBD-12_ltft-cell-matrix]]) is only signal if a COMLab consumer reads it — this
is that consumer. Field + consumer ship together.

## Proposed consumer + code path
`comlab/analytics/ltft_cell_analyzer.py` → `fault_atlas_router.py` family weighting.

## Dependencies / related
[[EP-OBD-12_ltft-cell-matrix]] · [[EP-OBD-IN-01_calculated-load-pid]].
