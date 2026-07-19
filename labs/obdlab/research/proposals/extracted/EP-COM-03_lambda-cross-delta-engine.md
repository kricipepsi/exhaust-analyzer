---
proposal_id: EP-COM-03
title: Lambda cross-delta divergence engine (λ_chem vs λ_obd, Δδ)
target_lab: COMLab (perception_contradiction)
source: proposals/wikiResearch.md §cross-delta; proposals/DataFlow.md §1.B
type: analytics_module
status: PROPOSAL (named consumer; extends truth-vs-perception)
date_extracted: 2026-06-07
---

## What it proposes
Compute the digital-vs-physical divergence and its transition:
- δ = λ_obd − λ_chem (the "digital lie" at one speed).
- Δλ_obd, Δλ_gas (vertical deltas across speed).
- Δδ = δ_stress − δ_low (cross-delta — how the lie widens with RPM).

## Diagnostic rationale
Separates **physical faults** (δ ≈ 0 both speeds — engine honest) from **internal ECU
faults** (δ wide / widening). Worked signatures: flash bit-flip ⇒ δ spikes only in the
corrupted RPM cell (Δδ ≥ +0.16); capacitor leak ⇒ Δδ ≈ +0.10 (high-RPM OL crash); ADC
mux ⇒ δ wide and constant (Δδ ≈ +0.03, permanently broken loop).

## Proposed consumer + code path
`comlab/core/perception_contradiction.py` — extends the existing λ_obd-vs-λ_chem override
(PRD §5 truth-vs-perception) with the Δδ term. Feeds the ECU checker discriminator.

## Dependencies / related
[[EP-COM-01_idle-transition-delta-engine]] · [[EP-GAS-01_5gas-brettschneider-schema]] ·
[[EP-ECU-07_eprom-bitflip]] · [[EP-COM-04_ecu-hardware-fault-checker]].
