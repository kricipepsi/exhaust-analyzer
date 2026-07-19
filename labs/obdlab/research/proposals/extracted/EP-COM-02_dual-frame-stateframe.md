---
proposal_id: EP-COM-02
title: Dual-frame StateFrame / multi-frame OrchestratorInboundRequest (low + high idle)
target_lab: COMLab schemas + wired/composition.py
source: proposals/DataFlow.md §2 (StateFrame); proposals/OBD_ImplProp.md §5
type: schema + architecture
status: PROPOSAL (named consumer = delta engine)
date_extracted: 2026-06-07
---

## What it proposes
Restructure the inbound payload to carry two operating-state frames:

    class StateFrame: gas: GasLabPayload; obd: OBDLivePayload; dtc: DTCLabPayload
    class OrchestratorInboundRequest:
        vehicle_dna: VehicleDNA
        low_idle: StateFrame
        high_idle: StateFrame

`composition.py::diagnose()` runs DNALab→GAS/OBD/DTC **twice** (one per engine state) and
assembles the dual-state request.

## Diagnostic rationale
Deltas are only computable if both states are captured in one typed payload. Keeps labs
stateless: they translate each frame independently; COMLab owns the cross-frame math.

## Proposed consumer + code path
COMLab delta engine ([[EP-COM-01_idle-transition-delta-engine]]) reads `low_idle` /
`high_idle`. Composition is the sole legal assembly point (no cross-lab imports).

## Dependencies / related
[[EP-COM-01_idle-transition-delta-engine]] · [[EP-ARCH-01_downstream-fusion-isolation]].
