---
proposal_id: EP-COM-07
title: Misfire-vs-fuelling pre-route gate
target_lab: COMLab (fault_atlas candidate-pruning)
source: chunks/fuel-trim/11; sources/fuel-trim/Fuel Trim Diagnostics.txt
type: routing_gate
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
A pre-routing gate: when a P030x misfire DTC is present **and** single-bank trim is only
mildly positive (≤ +15 %), route the **misfire family first** — because a misfire pumps
fresh O₂ past the sensor and creates a *false-lean* trim that would otherwise mis-route to
a fuel-delivery fault.

## Diagnostic rationale
False-lean from misfire is one of the most common mis-diagnoses; the gate prunes the
lean-fuelling candidate before fault-atlas weighs evidence.

## Proposed consumer + code path
`comlab/core/fault_atlas_router.py` candidate-pruning stage, reading DTCLab misfire codes
and per-cylinder counts ([[EP-OBD-IN-07_per-cylinder-misfire-counts]]).

## Dependencies / related
[[EP-OBD-IN-07_per-cylinder-misfire-counts]] · [[EP-ECU-03_coil-driver-failure]] ·
[[EP-DTC-01_dtc-causal-hierarchy]].
