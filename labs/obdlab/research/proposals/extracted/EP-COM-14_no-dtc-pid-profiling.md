---
proposal_id: EP-COM-14
title: No-DTC live-PID profiling mode (two-state baseline diagnosis)
target_lab: COMLab (diagnosis mode)
source: various/Vol3.md (PID logic without DTCs)
type: analytics_module
status: PROPOSAL (named consumer)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
A diagnosis mode that isolates faults from live-PID drift **without any DTC** — by
profiling a healthy baseline at curb idle (~800 RPM) and stress idle (~4000 RPM) and
flagging "skewed" sensors that read within plausible electrical range but wrong physical
range.

## Diagnostic rationale
PCMs mask mechanical/sensory drift until a DTC threshold trips; a no-DTC profiling mode
catches impending failure earlier (pre-MIL). This is the operating premise behind the
whole two-speed delta method.

## Proposed consumer + code path
COMLab orchestration runs the dual-frame request even when DTC set is empty; fault_atlas
routes on the delta vector. Reuses the dual-frame payload + delta engine.

## Dependencies / related
[[EP-COM-01_idle-transition-delta-engine]] · [[EP-COM-02_dual-frame-stateframe]].
