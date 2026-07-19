---
proposal_id: EP-COM-08
title: Prerequisite-DTC gate (suppress trim routing under active sensor DTCs)
target_lab: COMLab (analytics_preconditions)
source: chunks/fuel-trim/14; sources/fuel-trim/Fuel Trim Diagnostics.txt
type: routing_gate
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Before routing on fuel trims, check DTCLab output for an active **blocking/prerequisite**
code (MAF/MAP/IAT/ECT/TPS/CKP or coil circuit DTC). If present, suppress trim-based
routing — those trims are corrupted by the upstream sensor fault, not a fuelling problem.

## Diagnostic rationale
DTC enable-criteria define a run envelope; a trim DTC that set while a MAF DTC was active
is not independent evidence. Encodes the "blocking codes" logic.

## Proposed consumer + code path
`comlab/core/analytics_preconditions.py` reads `dtc_lab_output`; adds a
`TrimAnalyticsGate` suppression branch.

## Dependencies / related
[[EP-DTC-03_dtc-enable-window-gate]] · [[EP-DTC-01_dtc-causal-hierarchy]].
