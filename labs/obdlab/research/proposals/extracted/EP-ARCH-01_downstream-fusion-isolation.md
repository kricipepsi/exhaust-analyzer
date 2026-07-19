---
proposal_id: EP-ARCH-01
title: Downstream centralized fusion model + lab isolation contract
target_lab: architecture (COMLab as central broker)
source: proposals/DataFlow.md §How the architecture resolves this
type: architecture
status: PROPOSAL (formalises the contract the other proposals assume)
date_extracted: 2026-06-07
---

## What it proposes
Formalise the four-phase pipeline: (1) DNALab identity/topology → (2) parallel stateless
translation (GAS/OBD/DTC output typed "perceptions") → (3) `OrchestratorInboundRequest`
assembly in composition.py → (4) COMLab centralized reasoning (Stage A gates → perception
contradiction → fault-atlas routing → family verdict → output). Labs **never** talk to
each other; all cross-reference is deferred to COMLab.

## Diagnostic rationale
Lets the 20 studied cases cross-reference (misfire false-lean suppression, purge-valve +
rich-gas override) without tight coupling or cyclic dependencies — the structural basis
for every COMLab fusion proposal here.

## Proposed consumer + code path
Composition layer + COMLab pipeline stages. No cross-lab Python imports; COMLab mirrors
the types it needs locally (CLAUDE.md constraint).

## Related
[[EP-COM-02_dual-frame-stateframe]] · [[EP-ARCH-02_per-lab-knowledge-graph]] ·
[[EP-COM-05_semantic-coherence-paradigm]].
