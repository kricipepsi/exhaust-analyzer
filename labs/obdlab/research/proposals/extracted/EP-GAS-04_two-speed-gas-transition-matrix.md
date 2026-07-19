---
proposal_id: EP-GAS-04
title: Two-speed gas transition matrix as a GASLab capability (Δgas low→2500 RPM)
target_lab: GASLab (per-state frame) → COMLab delta engine
source: various/Vol7.md transition matrix (25 GAS-* cases); chunks/delta-relations/07
type: analytics_module + reference_table
status: PROPOSAL (named consumer = COMLab delta engine, FU-2)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
GASLab produces a per-state 5-gas frame (curb idle + 2500 RPM) so COMLab can compute Δgas
across the speed step, routed by the Vol7 25-case transition matrix: vacuum/unmetered
faults attenuate, speed-dependent wear intensifies.

## Diagnostic rationale
A single 5-gas snapshot cannot separate worn-valve-seals (improves at 2500) from
worn-rings (worsens) — only the **sign of Δgas** resolves them. The chemical complement to
ΔTrim.

## Proposed consumer + code path
GASLab emits the per-state frame; COMLab `delta_engine.py` (FU-2) computes Δgas and routes.
⚠ band conflict: Vol7 = 2500 RPM vs FuelTrimW ΔTrim = 3500–4500 RPM — reconcile before fusing.

## Dependencies / related
[[EP-COM-01_idle-transition-delta-engine]] · [[EP-GAS-05_5gas-sample-validity-gate]] · chunks/delta-relations/07.
