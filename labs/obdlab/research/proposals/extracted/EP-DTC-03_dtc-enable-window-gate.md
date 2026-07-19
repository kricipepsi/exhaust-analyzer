---
proposal_id: EP-DTC-03
title: DTC enable-criteria / run-condition window gate
target_lab: DTCLab → COMLab analytics_preconditions
source: chunks/fuel-trim/14; chunks/delta-relations/README (Gen III LS1 window)
type: routing_gate
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Encode per-DTC enable windows (e.g. Gen III LS1 P0171/4: ECT 50–115 °C, BARO > 74 kPa,
MAF 5–90 g/s, MAP 26–90 kPa, IAT −20–90 °C, RPM 400–3000, TPS < 90 %, VSS < 137 km/h,
≥ 6 s) and validate a code's freeze-frame against its window before trusting it.

## Diagnostic rationale
A code that set outside its enable window is unreliable evidence; gating on the window
prevents routing on a spurious set (`dtc_set_outside_enable_window`).

## Proposed consumer + code path
COMLab `analytics_preconditions.py` reads DTCLab freeze-frame + the window table.
Numeric windows carry wiki citations.

## Related
[[EP-COM-08_prerequisite-dtc-gate]] · [[EP-CAT-03_false-p0420-cluster]].
