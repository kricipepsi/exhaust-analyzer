---
proposal_id: EP-GAS-02
title: GASLab misfire chemistry resolver (high HC + high O₂ → COMBUSTION_FAIL)
target_lab: GASLab (chemical ontology)
source: proposals/DataFlow.md §4 (chemical causality)
type: analytics_module
status: PROPOSAL (named consumer; resolves contradictory PPM)
date_extracted: 2026-06-07
---

## What it proposes
A GASLab rule that resolves apparently contradictory tailpipe readings: simultaneous high
**HC** (unburned fuel) and high **O₂** (unused air) is the chemical signature of a
**misfire**, not a fuelling-ratio error. Output a synthesized `chemical_state =
COMBUSTION_FAIL` instead of passing raw conflicting PPM to COMLab.

## Diagnostic rationale
No spark/compression ⇒ mixture never ignites ⇒ both raw fuel and fresh air are pumped out
together. A naive calculator would read "rich AND lean" simultaneously; the resolver gives
COMLab a clean, typed perception.

## Proposed consumer + code path
GASLab chemical ontology emits `chemical_state`; consumed by COMLab `fault_atlas_router`
misfire family and the misfire-vs-fuelling gate.

## Related
[[EP-COM-07_misfire-vs-fuelling-gate]] · [[EP-ECU-03_coil-driver-failure]] ·
[[EP-GAS-01_5gas-brettschneider-schema]].
