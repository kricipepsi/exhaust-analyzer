---
proposal_id: EP-OBD-18
title: MAF/MAP/TPS rationality gate + inferred-BARO calibration check (P0068)
target_lab: OBDLab (rationality gate) → COMLab fault_atlas
source: various/Vol2.md Master Document 4; chunks/pids-protocol/02
type: analytics_module
status: PROPOSAL (consumer proposed, not yet wired)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Cross-check the three load sensors (MAF, MAP, TPS) for agreement, and compute an
inferred-BARO at WOT to catch a MAF that is drifted but DTC-silent:
- P0068 when MAF says high airflow while MAP says high vacuum (low load).
- Inferred BARO (from MAF+MAP at hard WOT) vs local actual; a large delta ⇒ MAF
  out of calibration, corrupting the whole fuel strategy.

## Diagnostic rationale
A MAF under-reporting inside the ECU's plausible window sets no code but skews λ — the
"diagnostic blindness" class (Vol1 N-009/N-019). One liar is caught by the other two.

## Proposed consumer + code path
OBDLab emits `rationality` verdict + `inferred_baro_delta`; COMLab `fault_atlas_router`
demotes a "lean fuelling" route in favour of "MAF calibration drift" when the cross-check
fails. Distinct from the speed-density airflow model in [[EP-OBD-11_theoretical-airflow-crosscheck]].

## Dependencies / related
[[EP-OBD-IN-06_baro-pid]] · [[EP-OBD-11_theoretical-airflow-crosscheck]] · chunks/pids-protocol/02.
