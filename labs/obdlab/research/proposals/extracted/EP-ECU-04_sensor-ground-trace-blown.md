---
proposal_id: EP-ECU-04
title: ECU fault node — vaporized internal sensor ground trace
target_lab: fault-atlas (new node) → COMLab ECU checker
source: chunks/ecu-diagnosis/05; proposals/OBD_ImplProp.md FAULT 1 / §2.C Gate A
type: fault_node
status: PROPOSAL (consumer = EP-COM-04; needs TPS/IAT fields)
date_extracted: 2026-06-07
---

## Signature
A blown PCB ground trace floats every ratiometric sensor reference simultaneously:
**ECT = −40 °C AND TPS = 100 % AND LOAD = 100 %** at physical idle, locked open-loop,
across both speeds — while the physical tailpipe is flooded rich (CO ≈ 9.5 %). No single
bad sensor produces this multi-signal float.

## Input-field dependency (signal/noise)
Requires TPS and IAT payload fields that do not exist today. They earn fields **only**
because this checker names them as consumers (ECU-FU-3) — not added speculatively.

## Proposed consumer + code path
[[EP-COM-04_ecu-hardware-fault-checker]] Gate A (ECT == −40 AND TPS == 100). Register in
`comlab/config/proposals/`.

## Related
[[EP-OBD-IN-05_throttle-position-pids]] · [[EP-OBD-IN-08_iat-field]] ·
[[EP-OBD-14_semantic-consistency-gates]].
