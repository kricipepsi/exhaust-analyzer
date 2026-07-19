---
proposal_id: EP-OBD-IN-02
title: Add Absolute Load Value PID (0x43) as an OBDLab input field
target_lab: OBDLab (input) → COMLab (consumer)
source: proposals/AddObdFields.md §Part 1.2
type: input_field
status: PROPOSAL (consumer proposed, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Ingest **Absolute Load** (PID `0x43`, `absolute_load_pct`). Unlike Calculated Load it
is **not** altitude-corrected — it scales with ambient air density (~−3 %/1000 ft), so
it is a direct read of **volumetric efficiency (VE)**. NA at sea-level WOT ≈ 80–90 %;
boosted engines exceed 100 % under boost.

## Diagnostic rationale
**MAF under-report isolation:** if the model's computed VE ≈ 95 % but Absolute Load
on the stream reads ~70 % (and no P0102), the MAF is electrically intact but dirty and
under-weighing air. Distinguishes a calibration-drifted MAF from an open-circuit MAF.

## Proposed consumer + code path
`comlab/core/fault_atlas_router.py` VE cross-reference, paired with OBDLab's VE engine
([[EP-OBD-10_ve-engine-classifier]]) which supplies the model VE to compare against.

## Dependencies / related
[[EP-OBD-IN-01_calculated-load-pid]] · [[EP-OBD-10_ve-engine-classifier]] ·
[[EP-OBD-11_theoretical-airflow-crosscheck]].

## Open questions
- New payload field `absolute_load_pct` — confirm it is absent today before adding.
- Forced-induction >100 % values must not trip range validation.
