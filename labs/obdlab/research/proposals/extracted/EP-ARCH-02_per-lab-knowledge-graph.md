---
proposal_id: EP-ARCH-02
title: Per-lab local knowledge graph + ontology (semantic translation layer)
target_lab: architecture (GAS/OBD/DTC each)
source: proposals/DataFlow.md §"why labs need an ontology"
type: architecture
status: PROPOSAL (design principle for the translators)
date_extracted: 2026-06-07
---

## What it proposes
Each translation lab carries its **own local KG + ontology** to turn syntactic raw values
into semantic perceptions: a raw 0.1 V O₂ float becomes `o2_failure_mode = SLUGGISH` only
after consulting sensor type, spatial location, and downstream dependency. The graph
resolves the spatial/physical relationships; the ontology defines interpretation rules.

## Diagnostic rationale
Explains why labs cannot be flat if/else tables and yet still emit simple typed output:
the complexity lives in the local graph, the boundary stays a clean typed JSON payload.

## Proposed consumer + code path
Each lab's `core` + local `config/kg`; output consumed by COMLab. No cross-lab imports.

## Related
[[EP-ARCH-01_downstream-fusion-isolation]] · [[EP-DNA-01_dynamic-graph-pruning]] ·
[[EP-GAS-02_misfire-chemistry-resolver]].
