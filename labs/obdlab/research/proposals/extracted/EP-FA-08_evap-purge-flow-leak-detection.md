---
proposal_id: EP-FA-08
title: EVAP purge-flow verification + leak-detection logic
target_lab: fault-atlas (EVAP / auxiliary emissions) → COMLab
source: various/Vol2.md Master Document 8 (EVAP System Integrity)
type: fault_node + analytics_module
status: PROPOSAL (named consumer)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
EVAP diagnostics: (1) **purge-flow check** — commanding the purge valve open must produce a
negative trim shift; no shift ⇒ restricted line / stuck-closed valve. (2) **leak decay** —
close vent, open purge, pull vacuum, watch FTP for small (≤0.020") leaks. Saturated-canister
purge dumps raw vapour (HC/CO spike) at 2500 RPM (Vol7 GAS-EVAP-001).

## Diagnostic rationale
Distinguishes a stuck-open purge (rich at idle, normalises at RPM) from a saturated canister
(rich spike AT 2500) from a no-flow purge restriction — three different EVAP faults the trim
sign alone cannot separate.

## Proposed consumer + code path
COMLab fault_atlas EVAP family reads purge-command vs trim-shift + FTP decay; pairs with the
two-speed gas matrix (GAS-EVAP-001). New EVAP PIDs (FTP, purge/vent command) earn place via
this consumer.

## Dependencies / related
[[EP-GAS-04_two-speed-gas-transition-matrix]] · [[EP-COM-06_traditional-fault-signature-matrix]].
