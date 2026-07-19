---
proposal_id: EP-COM-06
title: Traditional-fault PID signature matrix (10 external fault families × PIDs)
target_lab: COMLab (fault_atlas_router discriminator table)
source: proposals/OBD_ImplProp.md §2-3 (comparative matrix); chunks/fuel-trim/09
type: reference_table + routing
status: PROPOSAL (mostly active families; table formalises discriminators)
date_extracted: 2026-06-07
---

## What it proposes
A high-density discriminator matrix mapping 10 traditional external fault families
(vacuum leak, restricted fuel, stuck-open purge, contaminated MAF, catalyst failure,
exhaust leak, ignition fault, mechanical wear, retarded cam, retarded spark) to their
LOAD_PCT / STFT / LTFT / MAP-MAF / upstream-O₂ / downstream-O₂ signatures at **both** low
idle and stress idle.

## Diagnostic rationale
Gives `fault_atlas_router` a single, explicit, two-state lookup so coherent faults route
deterministically instead of via scattered if/else. 14 of 20 cases already map to live
nodes; the matrix formalises the discriminators between them.

## Proposed consumer + code path
`comlab/core/fault_atlas_router.py` reads the matrix as config; pairs with the delta
engine for the stress-idle column.

## Dependencies / related
[[EP-COM-01_idle-transition-delta-engine]] · [[EP-DTC-02_j2012-fault-taxonomy]] ·
all `EP-FA-*` (the 6 cases without a live node).
