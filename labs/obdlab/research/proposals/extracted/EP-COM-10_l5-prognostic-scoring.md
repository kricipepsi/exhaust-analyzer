---
proposal_id: EP-COM-10
title: L5 prognostic scoring layer (perception-trust / ECU-consistency / thermal-confidence)
target_lab: COMLab (L5 decision-fusion)
source: various/Vol1.md "Proposed Table Enhancements" (L3/L5 columns); chunks/truth-perception/02
type: analytics_module + schema
status: PROPOSAL (named consumer; new L5 tier v2 lacks)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
A decision-fusion scorer producing:
- `Perception_Reliability_Index` (0–100) from O₂ stability + cross-counts (lazy sensor
  → low trust → down-weight L3 evidence).
- `ECU_Consistency_Score` (0–100) penalising physically-impossible PID combinations
  (e.g. 5 V on a 1 V narrowband).
- `Thermal_State_Confidence` (bool) — catalyst above light-off; if false, L3 discrepancies
  are treated as expected transient.

## Diagnostic rationale
Turns the binary fault/no-fault into a confidence-weighted verdict (repair-now vs monitor);
the L5 tier v2 does not yet implement.

## Proposed consumer + code path
New `comlab/analytics/prognostic_scorer.py` reading O₂ metrics, PID-plausibility checks,
and cat thermal state; output weights the final fault-atlas verdict.

## Dependencies / related
[[EP-COM-03_lambda-cross-delta-engine]] · [[EP-COM-05_semantic-coherence-paradigm]] · chunks/truth-perception/02.
