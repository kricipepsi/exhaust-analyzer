---
proposal_id: EP-GAS-05
title: 5-gas sample-validity gate (vsum + dilution)
target_lab: GASLab (ingestion gate)
source: various/Vol7.md vsum + dilution rule; chunks/delta-relations/08
type: analytics_module
status: PROPOSAL (named consumer)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Reject/flag a 5-gas frame before any Δ or λ computation:
`vsum = HC+CO+CO2+O2+NOx`, VALID 14.0–18.0 %; dilution fail if CO+CO2 ≤ 6.0 %.

## Diagnostic rationale
A diluted sample (probe leak, cracked tailpipe, ambient ingress) produces false-lean λ and
corrupts every downstream delta. At curb idle, pulse reversion dilutes; at 2500 RPM the
positive-pressure barrier purifies — so a frame failing only at idle is itself a sampling
signature.

## Proposed consumer + code path
GASLab marks each frame `gas_sample_valid` + `vsum`; COMLab delta engine skips Δ on invalid
frames. ⚠ the vsum display equation was image-stripped in Vol7 — thresholds survive in
prose; exact weighting PENDING readable export.

## Dependencies / related
[[EP-GAS-04_two-speed-gas-transition-matrix]] · [[EP-GAS-01_5gas-brettschneider-schema]] · chunks/delta-relations/08.
