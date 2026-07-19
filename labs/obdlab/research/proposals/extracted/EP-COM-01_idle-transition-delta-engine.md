---
proposal_id: EP-COM-01
title: Idle-transition delta engine (low-idle vs stress-idle Δ across PIDs)
target_lab: COMLab (analytics/idle_transition_evaluator.py / delta_engine.py)
source: proposals/DataFlow.md §2-3; proposals/AddObdFields.md §Delta logic; chunks/delta-relations/*
type: analytics_module
status: PROPOSAL (named consumer; whole delta-relations folder PENDING on this)
date_extracted: 2026-06-07
---

## What it proposes
A centralised COMLab delta module computing the transition deltas between low idle
(~750 RPM) and stress idle (~2500–4500 RPM) — the single consumer that unblocks the
staged `chunks/delta-relations/`:
- ΔLoad_calc, ΔSensor_error (airflow), ΔFUELSYS, ΔVPWR, ΔTP_R, ΔBARO, ΔMisfire_cyl,
  ΔTrim, Δλ_chem, Δairflow_efficiency.

## Diagnostic rationale
Static single-point snapshots cannot separate faults with identical idle values (vacuum
leak vs weak pump vs dirty MAF vs lazy O₂). The delta sign/magnitude across two load
states resolves them with near-mathematical certainty (DataFlow §3 decision table).

## Proposed consumer + code path
`comlab/analytics/delta_engine.py` invoked inside the `perception_contradiction` stage;
results read by `fault_atlas_router.py`. Labs stay stateless — they never compute deltas
(isolation contract). Requires the dual-frame payload [[EP-COM-02_dual-frame-stateframe]].

## Dependencies / related
[[EP-COM-02_dual-frame-stateframe]] · [[EP-OBD-16_state-translation-rules]] (band reconcile)
· [[EP-COM-03_lambda-cross-delta-engine]] · every `EP-OBD-IN-*` delta input.

## Open questions
Canonical stress-idle band must be fixed first (FU-2 / O2-FU-3 band conflict).
