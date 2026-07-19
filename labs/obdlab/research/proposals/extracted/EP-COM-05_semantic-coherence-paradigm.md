---
proposal_id: EP-COM-05
title: Semantic-coherence vs digital-divergence classification paradigm
target_lab: COMLab (perception_contradiction / fault_atlas routing policy)
source: proposals/OBD_ImplProp.md §1 (paradigm); proposals/wikiResearch.md §4
type: architecture
status: PROPOSAL (policy layer over existing routing)
date_extracted: 2026-06-07
---

## What it proposes
A top-level routing policy: classify every case as **Semantically Coherent** (sensors
honestly measure a real physical/chemical shift — OBD agrees with the 5-gas truth) or
**Semantically Incoherent / Digital Lie** (board-level failure corrupts the measurement;
OBD contradicts the tailpipe). Coherent → traditional-fault families; incoherent →
ECU-hardware checker.

## Diagnostic rationale
This is the organising principle behind the whole truth-vs-perception override: it decides
*which* sub-engine should own a case before any family routing, preventing COMLab from
chasing a fuel-delivery fault when the ECU is lying.

## Proposed consumer + code path
`comlab/core/perception_contradiction.py` sets a `coherence` flag read by
`fault_atlas_router.py` to gate between traditional families and
[[EP-COM-04_ecu-hardware-fault-checker]].

## Dependencies / related
[[EP-COM-03_lambda-cross-delta-engine]] · [[EP-GAS-01_5gas-brettschneider-schema]] ·
[[EP-OBD-14_semantic-consistency-gates]].
