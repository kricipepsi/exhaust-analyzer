---
chunk: truth-perception/02_lambda-delta-vector-and-scoring
topic: truth-perception
sources:
  - various/Vol1.md — "Proposed Table Enhancements" (Lambda_Delta_Vector, trust/score columns)
consumer: COMLab perception_contradiction (Δλ vector — quantifies the liar/blind delta) + a proposed L5 prognostic scorer. Field + consumer ship together (v2 forward-progress).
consumer_status: PROPOSAL (Δλ vector refines an active path; the L5 score fields are new)
provenance: sources/various/Vol1.md — numeric Δλ values intact in case tables; prose symbols stripped
dedup: the schema-field proposals here are catalogued in proposals/extracted (EP-COM-03 lambda cross-delta); this chunk is the research basis, not a duplicate ship
---

# Lambda-Delta vector + perception scoring

## The discrepancy vector (L3)

```
Lambda_Delta_Vector = λ_obd − λ_chem      (signed float)

  = 0.00   perfect calibration
  > 0      engine physically LEANER than ECU perceives  → "Rich-Blind" ECU
  < 0      engine physically RICHER  than ECU perceives  → "Lean-Blind" ECU
```

Worked example (ECU-001 / case N-002 family): ECU sets P0171 (perceives lean,
λ_obd≈1.05) but tailpipe is physically rich (λ_chem≈0.84) → Δλ ≈ +0.21, a severe
logic inversion that triggers an L5 ECU-health penalty.

## Proposed scoring fields (L5 — new in v2)

- `Perception_Reliability_Index` (0–100): from O₂ voltage stability + cross-counts.
  A lazy sensor (2 cross-counts / 10 s) scores ~20 → "Low Trust" flag at L3.
- `ECU_Consistency_Score` (0–100): penalises physically-impossible PID combinations
  (e.g. 5 V on a 1 V narrowband).
- `Thermal_State_Confidence` (bool): catalyst above light-off? If false, L3
  discrepancies are treated as expected transient, not faults.

## Consumer / code path
Δλ vector → `comlab/core/perception_contradiction.py` (active override). The three
L5 score fields require a new prognostic scorer (proposal) — named here, not shipped
silently. See proposals/extracted EP-COM-03 / EP-COM-05.


## Core Entities

- Lambda_Delta_Vector, Perception_Reliability_Index, ECU_Consistency_Score, Thermal_State_Confidence
- perception_contradiction (active) + proposed L5 scorer

## Graph relations (explicit)

**Lambda_Delta_Vector** EQUALS **lambda_obd** minus **lambda_chem**
**Lambda_Delta_Vector** above 0 INDICATES Rich-Blind ECU
**Lambda_Delta_Vector** below 0 INDICATES Lean-Blind ECU
**Lambda_Delta_Vector** CONSUMED_BY **perception_contradiction**
**Perception_Reliability_Index**, **ECU_Consistency_Score**, **Thermal_State_Confidence** REQUIRE an L5 scorer

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
