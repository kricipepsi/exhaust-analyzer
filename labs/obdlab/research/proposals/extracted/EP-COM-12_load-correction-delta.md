---
proposal_id: EP-COM-12
title: Load-correction delta (MAF-reported load vs gas-calculated load)
target_lab: COMLab (analytics)
source: various/Vol1.md "Load_Correction_Delta" enhancement
type: analytics_module
status: PROPOSAL (named consumer)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Compare the MAF-reported engine load against a load inferred from exhaust-gas volume/
temperature. If MAF says "low load" but gas chemistry/heat says "high load," flag a MAF
scaling error.

## Diagnostic rationale
A second, independent cross-check on MAF calibration using the gas channel (truth side) —
catches under-reporting that the OBD side alone cannot (diagnostic blindness).

## Proposed consumer + code path
`comlab/analytics/` computes `load_correction_delta` from MAF load vs GASLab-derived load;
fault_atlas routes a MAF-scaling fault when it diverges.

## Dependencies / related
[[EP-OBD-18_maf-map-tps-rationality]] · [[EP-OBD-IN-02_absolute-load-pid]] · [[EP-GAS-01_5gas-brettschneider-schema]].
