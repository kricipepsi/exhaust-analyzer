---
chunk: truth-perception/03_thirty-case-liar-library
topic: truth-perception
sources:
  - various/Vol1.md — "Proposed New Case Studies (1990-2020)" N-001..N-030 + Group tables
consumer: COMLab fault_atlas_router (pattern library) + the generative test corpus (each case = a labelled truth-vs-perception scenario with λ_obd/λ_chem/Δλ ground truth).
consumer_status: PROPOSAL (case library — drives fault-atlas patterns + test fixtures; 14-style mapping to live nodes TBD per case)
provenance: sources/various/Vol1.md — the case Δλ/gas tables are INTACT (numbers survived); only inline prose symbols stripped
dedup: new — distinct from fuel-trim/09 (20 trim cases) and ecu-diagnosis (5 ECU modes); these are λ_obd-vs-λ_chem discrepancy cases
---

# 30-case truth-vs-perception ("liar") library

30 cases spanning 1990–2020, each defined by the gap between ECU perception and
tailpipe truth. Grouped by the discrepancy class the L3 matrix must catch.

## Representative cases (full 30 with values in source tables)

| ID | Yr | Fault | λ_obd | λ_chem | Δλ | Class / tier |
|---|---|---|---|---|---|---|
| N-002 | 2002 | Silicone-poisoned upstream O₂ | 1.05 | 0.84 | 0.21 | L3 Liar |
| N-004 | 2001 | Pre-cat exhaust venturi leak | 1.12 | 0.92 | 0.20 | L3 Inversion (high O₂+high CO together) |
| N-005 | 2003 | Ground ripple ghost-switching | 1.00 | 1.08 | 0.08 | L3 Blindness |
| N-008 | 2011 | Catalyst-masked oil burn | — | — | — | L5 Masking |
| N-015 | 2019 | Wideband ref-current drift | 1.00 | 1.15 | 0.15 | L3 Blindness (loop internally consistent, externally wrong) |
| N-016 | 2014 | Flywheel ghost misfire | 1.00 | 1.00 | 0.00 | L4 Hallucination (P0300, gas perfect) |
| N-019 | 2007 | Double-liar (MAF under + O₂ rich-bias) | 1.00 | 1.15 | 0.15 | L3 Blindness (faults cancel in trim) |
| N-021 | 2004 | Lean-misfire feedback death-spiral | 1.25 | 0.95 | 0.30 | L3 Inversion |
| N-024 | 2012 | E85 in non-flex tank | 1.15 | 1.00 | — | L5 Model-shift (wrong fuel constants) |
| N-030 | 2019 | Heat-exchanger glycol O₂ poison | 1.10 | 0.82 | 0.28 | L3 Liar (cross-system) |

## Three structural insights (the library's point)

1. **Diagnostic blindness** — a sensor failing inside the ECU's "plausible" window
   (e.g. MAF under-reporting 15 %) sets no DTC but shifts λ. Gas truth is the sanity
   check.
2. **Logic inversion** — exhaust leaks / misfires make the ECU add fuel ("I'm lean")
   which drives the real state rich. Caught at L3 via negative correlation between
   trim movement and λ_chem improvement.
3. **Systemic masking** — efficient cats hide engine misbehaviour until catastrophic
   failure; needs a pre-cat inference model (inlet/outlet temp differential).

## Consumer / code path
Each row is a labelled fixture for the COMLab fault-atlas pattern set and the test
corpus. Cases mapping to existing nodes activate those; novel ones (ghost-misfire
hallucination, double-liar cancellation, model-shift) are fault-atlas PROPOSALS.


## Core Entities

- N-002, N-004, N-015, N-016, N-019, N-021, diagnostic_blindness, logic_inversion, systemic_masking
- fault_atlas pattern set + generative test corpus (PROPOSAL)

## Graph relations (explicit)

each liar case DEFINED_BY the gap between **lambda_obd** and **lambda_chem**
**diagnostic_blindness** SETS no DTC but shifts lambda
**logic_inversion** DRIVES real state opposite to ECU perception
**systemic_masking** HIDES engine fault behind an efficient catalyst
**liar-library** CONSUMED_BY **fault_atlas pattern set** and the test corpus

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
