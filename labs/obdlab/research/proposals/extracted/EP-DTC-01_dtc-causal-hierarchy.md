---
proposal_id: EP-DTC-01
title: DTCLab causal hierarchy / companion-code sub-graph
target_lab: DTCLab (ontology) → COMLab
source: proposals/DataFlow.md §2 (causal hierarchies)
type: analytics_module
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
DTCLab builds a directed causal sub-graph instead of passing a flat code list, e.g.:

    P0351 (coil circuit) --causes--> P0301 (cyl-1 misfire) --causes--> P0171 (lean from excess O2)

and tags each: P0351 = electrical root (primary), P0301 = combustion consequence, P0171 =
feedback symptom. Output flags the root trigger explicitly.

## Diagnostic rationale
A flat array forces COMLab to chase a false lean-fuelling problem; the prioritised
sub-graph hands COMLab the root cause and suppresses the downstream symptoms.

## Proposed consumer + code path
DTCLab emits a typed prioritised DTC payload; COMLab `fault_atlas_router` consumes
root-vs-symptom tags. Mirrors types locally (no cross-lab import).

## Related
[[EP-COM-07_misfire-vs-fuelling-gate]] · [[EP-DTC-02_j2012-fault-taxonomy]] ·
[[EP-COM-08_prerequisite-dtc-gate]].
