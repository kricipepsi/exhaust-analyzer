---
proposal_id: EP-ECU-06
title: ECU fault node — analog-to-digital converter (ADC) multiplexer / channel failure
target_lab: fault-atlas (new node) → COMLab ECU checker
source: chunks/ecu-diagnosis (Tables); proposals/OBD_ImplProp.md FAULT 6 / §2.C Gate B; wikiResearch.md §2-ADC
type: fault_node
status: PROPOSAL (consumer = EP-COM-04)
date_extracted: 2026-06-07
---

## Signature
The O₂ input channel/mux shorts or goes high-impedance. The micro reads a static flatline
0.0–0.15 V (interprets extreme lean), applies maximum positive trims, floods the engine.
OBD reports λ ≈ 1.00 / lean while physical λ_gas ≈ 0.85–0.88 (CO ≥ 3.5 %). The divergence
δ stays **wide and constant across both speeds** (Δδ ≈ +0.03) — the loop is permanently
broken inside the hardware, not modulated by RPM.

## Proposed consumer + code path
[[EP-COM-04_ecu-hardware-fault-checker]] Gate B (OBD-O₂ flatline + railed trim + rich
5-gas λ). Register in `comlab/config/proposals/`.

## Related
[[EP-COM-03_lambda-cross-delta-engine]] (constant-wide δ tell) ·
[[EP-OBD-14_semantic-consistency-gates]] · [[EP-GAS-01_5gas-brettschneider-schema]].
