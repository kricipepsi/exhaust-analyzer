---
proposal_id: EP-COM-13
title: T15 startup + 70% high-load enrichment gates (TrimAnalyticsGate additions)
target_lab: COMLab (analytics_preconditions)
source: various/Vol2.md MD12 (T15) + MD13 (70% load); chunks/ecu-diagnosis/08
type: routing_gate
status: PROPOSAL (named consumer; numeric limits PENDING readable export)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Two new TrimAnalyticsGate states suppressing trim/λ routing during deliberately
non-stoichiometric windows:
- `STARTUP_T15_ACTIVE` — key-on→closed-loop window (KAM reset, open-loop maps).
- `HIGH_LOAD_ENRICH_ACTIVE` — ≥70 % load power-enrichment (open-loop, EVAP inhibited,
  timing retarded).

## Diagnostic rationale
Normal startup/power enrichment otherwise reads as a rich fault. The 70 % load mark is the
cruise→power transition where P0087-type faults surface.

## Proposed consumer + code path
`comlab/core/analytics_preconditions.py` adds the two gate states. ⚠ exact rich/lean
fault-limit + load-cell numbers were image-stripped in Vol2 MD12/13 — PENDING a readable
re-export before the thresholds are pinned.

## Dependencies / related
[[EP-OBD-16_state-translation-rules]] · [[EP-OBD-IN-03_fuel-system-status-pid]] · chunks/ecu-diagnosis/08.
