---
proposal_id: EP-OBD-11
title: Speed-density theoretical-airflow MAF/MAP sanity cross-check
target_lab: OBDLab (core) → COMLab
source: proposals/AddObdFields.md §Part 1 (W_theo); proposals/DataFlow.md
type: analytics_module
status: PROPOSAL (consumer proposed, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Compute theoretical airflow from speed-density and compare against the reported MAF/MAP:

    W_theo = (η_V · V_disp · P_manifold · RPM) / (120 · R · T_intake)

and the sensor-error delta across two idle points:

    ΔSensor_error = |Sensor_2500 − W_theo_2500| − |Sensor_750 − W_theo_750|

ΔSensor_error ≈ 0 ⇒ sensor scales linearly; large deviation ⇒ calibration drift
(dirty MAF hot-wire) without an open-circuit DTC.

## Diagnostic rationale
Catches the non-linear MAF/MAP fault a single snapshot misses — a sensor accurate at
750 RPM but wrong at 2500 RPM.

## Proposed consumer + code path
OBDLab computes `w_theo` + `sensor_error_delta`; consumed by COMLab
`fault_atlas_router.py` (MAF-contamination vs healthy discriminator) and the delta engine
([[EP-COM-01_idle-transition-delta-engine]]).

## Dependencies / related
[[EP-OBD-10_ve-engine-classifier]] · [[EP-OBD-IN-08_iat-field]] · [[EP-COM-02_dual-frame-stateframe]].
