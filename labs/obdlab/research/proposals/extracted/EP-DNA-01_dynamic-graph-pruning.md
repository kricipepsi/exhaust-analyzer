---
proposal_id: EP-DNA-01
title: Dynamic per-lab graph pruning by VehicleDNA (speed-density vs MAF subgraph)
target_lab: DNALab → OBDLab/GASLab/DTCLab graph selection
source: proposals/DataFlow.md §3 (dynamic graph pruning)
type: architecture
status: PROPOSAL (named consumer; runtime path selection)
date_extracted: 2026-06-07
---

## What it proposes
Let each lab prune/select its evaluation subgraph at runtime from the resolved
`VehicleDNA`, instead of hardcoding per-config logic:
- Speed-density engine → activate MAP+IAT → air-density → injection-PW path.
- MAF engine → bypass manifold-pressure equations, map MAF directly to air mass.

## Diagnostic rationale
Replaces thousands of lines of conditional code with a graph-template load + traversal;
keeps labs flexible across heterogeneous 1990–2010 platforms.

## Proposed consumer + code path
DNALab resolves topology; each lab's local KG loads the matching template. Pairs with the
slim DNA views ([[EP-DNA-02_slim-dna-views]]).

## Related
[[EP-DNA-02_slim-dna-views]] · [[EP-OBD-10_ve-engine-classifier]] · [[EP-ARCH-02_per-lab-knowledge-graph]].
