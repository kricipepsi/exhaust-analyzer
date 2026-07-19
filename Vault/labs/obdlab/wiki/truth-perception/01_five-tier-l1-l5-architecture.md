---
chunk: truth-perception/01_five-tier-l1-l5-architecture
topic: truth-perception
sources:
  - various/Vol1.md — "The Multi-Tier Diagnostic Paradigm" (L1–L5)
consumer: COMLab perception_contradiction — the L3 "Correlation & Discrepancy Matrix" is exactly the λ_obd-vs-λ_chem override stage (PRD §5 truth-vs-perception). This chunk frames where each existing stage sits.
consumer_status: active (method/framing); L5 prognostic scoring fields are PROPOSAL (see truth-perception/02)
provenance: sources/various/Vol1.md — prose READABLE; inline λ/subscript symbols stripped in export, recovered from the intact case tables (truth-perception/03)
dedup: extends o2-logic/05_bias-vs-real-truth-perception (which is the O₂-only view) to the full 5-tier engine framing
---

# The 5-tier diagnostic paradigm (L1–L5)

The engine treats sensor data as *mediated perception*, not objective truth, and
layers diagnosis so physical reality (gas chemistry) arbitrates over ECU perception.

- **L1 — Raw observation.** PID values: MAF, MAP, O₂ voltage, RPM. Susceptible to
  sensor bias, electrical noise, environment.
- **L2 — Calculated variables.** STFT/LTFT, engine load, VE (ECU side) **and** the
  parallel 5-gas → Brettschneider λ_chem (tailpipe side).
- **L3 — Correlation & Discrepancy Matrix.** The truth-vs-perception junction:
  compare λ_obd vs λ_chem; a significant `Δλ` exposes a "liar" scenario where the
  ECU model no longer represents in-cylinder reality. **= COMLab perception_contradiction.**
- **L4 — Strategy & pattern matching.** Temporal Causal Graphs (TCG) map how one
  deviation propagates to others; separates mechanical failure from electronic
  hallucination (e.g. ghost misfire from alternator ripple). **≈ fault_atlas_router.**
- **L5 — Decision fusion & prognosis.** Engine-health score weighting pattern
  confidence against sensor reliability → repair-now vs monitor.

## Why it maps onto the existing engine
L3 is already implemented as the λ_obd/λ_chem override; L4 as fault-atlas routing.
L1/L2 are the OBDLab/GASLab translators. L5 (prognostic scoring) is the part v2 does
not yet have — its proposed fields are in truth-perception/02.


## Core Entities

- L1, L2, L3, L4, L5, lambda_obd, lambda_chem
- COMLab perception_contradiction (L3, active method)

## Graph relations (explicit)

**L3** IS **perception_contradiction** comparing **lambda_obd** with **lambda_chem**
**L4** APPROXIMATES **fault_atlas_router**
**L1** and **L2** ARE OBDLab/GASLab translators
**L5** prognostic scoring NOT_YET_IN v2 (proposal)

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
