---
proposal_id: EP-ECU-07
title: ECU fault node — EPROM/flash memory cell corruption (localized bit-flip)
target_lab: fault-atlas (new node) → COMLab ECU checker
source: proposals/wikiResearch.md §cross-delta 1 (Flash Corruption)
type: fault_node
status: PROPOSAL (consumer = EP-COM-04; delta-only signature)
date_extracted: 2026-06-07
---

## Signature
Floating-gate charge leakage corrupts a hex value in **one specific speed/load cell** of
the VE map. The engine runs perfectly at idle (δ_low ≈ 0); the instant it enters the
corrupted block (e.g. exactly 3500–4500 RPM light load) the ECU executes the bit-flipped
command and floods rich — physical λ_gas ≈ 0.84 while OBD still claims stoichiometry.
**Δδ ≥ +0.16, localised to the cell** — the sharpest delta-only signature.

## Why delta-only
A single-snapshot diagnosis cannot see this: it only appears as a divergence spike tied
to a specific RPM cell, so it is detectable **only** through the cross-delta engine.

## Proposed consumer + code path
[[EP-COM-03_lambda-cross-delta-engine]] (cell-localised Δδ spike) →
[[EP-COM-04_ecu-hardware-fault-checker]]. Register in `comlab/config/proposals/`.

## Related
[[EP-COM-01_idle-transition-delta-engine]] · [[EP-OBD-12_ltft-cell-matrix]] (cell coords).
