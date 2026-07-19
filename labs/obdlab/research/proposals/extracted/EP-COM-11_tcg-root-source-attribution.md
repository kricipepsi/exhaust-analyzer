---
proposal_id: EP-COM-11
title: Temporal Causal Graph (TCG) root-source attribution layer
target_lab: COMLab (L4 pattern matching)
source: various/Vol1.md "Causal Attribution Layer" (TCG_Root_Source)
type: analytics_module + schema
status: PROPOSAL (named consumer)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
A `TCG_Root_Source` classification that maps a gas/PID signature to a causal category:
`IN` intake_leak · `EX` exhaust_leak · `FS` sensor_bias · `ME` mechanical_wear · `SY`
software_hang. A Temporal Causal Graph maps how one deviation (e.g. vacuum drop) propagates
to others (rising HC/O₂), separating mechanical failure from electronic hallucination.

## Diagnostic rationale
Gives fault-atlas an explicit root-cause category instead of a flat symptom list — the L4
tier that distinguishes a real misfire from a ghost misfire (alternator ripple).

## Proposed consumer + code path
`comlab/core/fault_atlas_router.py` attaches `tcg_root_source` to each verdict; drives the
target-validation-test recommendation. Complements DTC causal hierarchy.

## Dependencies / related
[[EP-DTC-01_dtc-causal-hierarchy]] · [[EP-COM-05_semantic-coherence-paradigm]] · chunks/truth-perception/03.
