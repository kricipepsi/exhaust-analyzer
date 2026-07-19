---
chunk: ecu-diagnosis/08_t15-startup-lambda-logic
topic: ecu-diagnosis
sources:
  - various/Vol2.md — Master Document 12 (ECU Fault Patterns — Lambda and T15 Transitions); MD13 (70% load threshold)
consumer: COMLab analytics_preconditions — a startup/T15 gate: trims and λ during the key-on→closed-loop window are transient and must not be routed as faults until closed loop is achieved.
consumer_status: PROPOSAL (T15 startup gate + 70% load enrichment gate not yet in analytics_preconditions; names consumer)
provenance: sources/various/Vol2.md MD12/MD13 — logic/prose READABLE; the numeric rich/lean fault-limit and load cells were image-stripped (flagged in formula wiki)
dedup: top-up; complements fuel-trim/08 validity-preconditions (ECT/CL/DFCO/WOT) and fuel-trim/15 (KAM/freeze-frame)
---

# T15 startup + high-load enrichment gates

Two ECU operating-mode windows in which trims/λ are deliberately non-stoichiometric and
must not be mistaken for faults.

## T15 (key-on / startup) window (Vol2 MD12)

- T15 init **clears transient KAM** (learned trims reset to zero).
- The PCM must reach closed loop within a bounded time post-start; until then λ is
  managed open-loop off lookup maps.
- A "tightened" rich-fault trigger sits on the edge of the power-enrichment boundary —
  crossing it during a non-load transition indicates a failing feedback loop or a
  leaking injector the PCM can no longer trim. (Exact rich/lean limit values stripped.)

## 70% high-load enrichment window (Vol2 MD13)

- ≥70 % calculated load = transition from cruise (vacuum control) to power demand;
  PCM goes **open-loop**, ignores O₂ feedback to protect the engine, inhibits EVAP
  purge, and pulls timing in the knock window.
- Pressure-delta faults (P0087) and MAF peak-resolution issues surface above 70 % load.

## Logic / consumer
`analytics_preconditions.py` must add `STARTUP_T15_ACTIVE` and `HIGH_LOAD_ENRICH_ACTIVE`
to the TrimAnalyticsGate family so trim/λ routing is suppressed in these windows —
otherwise normal enrichment reads as a rich fault. Numeric limits are PENDING a readable
export (Vol2 MD12/MD13 cells stripped).


## Core Entities

- TrimAnalyticsGate.STARTUP_T15_ACTIVE, TrimAnalyticsGate.HIGH_LOAD_ENRICH_ACTIVE
- analytics_preconditions (proposed consumer), P0087

## Graph relations (explicit)

**TrimAnalyticsGate.STARTUP_T15_ACTIVE** SUPPRESSES trim/lambda routing during key-on window
**TrimAnalyticsGate.HIGH_LOAD_ENRICH_ACTIVE** SUPPRESSES O2 feedback above 70% load
**analytics_preconditions** ADDS **TrimAnalyticsGate.STARTUP_T15_ACTIVE**
**analytics_preconditions** ADDS **TrimAnalyticsGate.HIGH_LOAD_ENRICH_ACTIVE**
**HIGH_LOAD_ENRICH_ACTIVE** SURFACES **P0087**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
