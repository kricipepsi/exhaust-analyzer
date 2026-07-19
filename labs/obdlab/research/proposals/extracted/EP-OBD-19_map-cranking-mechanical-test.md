---
proposal_id: EP-OBD-19
title: MAP cranking mechanical test (electronic vacuum / relative compression)
target_lab: OBDLab (mechanical-health module)
source: various/Vol2.md Master Document 9 (Mechanical Health and Cranking Protocols)
type: analytics_module
status: PROPOSAL (consumer proposed; manual-entry test)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Assess internal mechanical integrity electronically by monitoring MAP during a
clear-flood cranking test (fuel disabled, WOT crank): a healthy engine pulls a rhythmic
vacuum; a leaking intake valve spikes manifold pressure every ~180° of crank rotation.
Pairs with starter-current relative-compression (even peaks across cylinders).

## Diagnostic rationale
Detects valvetrain/sealing faults (low compression, leaking valves) without mechanical
disassembly — a "bouncing" cranking-vacuum signature localises the cylinder.

## Proposed consumer + code path
OBDLab emits `cranking_vacuum_stability` / `relative_compression_evenness`; COMLab
fault_atlas mechanical-wear family reads them. Manual-entry (cranking PIDs), not live stream.

## Dependencies / related
[[EP-FA-07_fuel-restriction-split]] (mechanical vs fuel) · [[EP-COM-06_traditional-fault-signature-matrix]].
