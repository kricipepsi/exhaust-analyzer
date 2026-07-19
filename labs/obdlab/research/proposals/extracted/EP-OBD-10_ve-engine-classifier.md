---
proposal_id: EP-OBD-10
title: VE engine math + validity classifier (FAULT_VE_IDLE_COLLAPSE / SENSOR_SKEW)
target_lab: OBDLab (core/ve_engine.py)
source: proposals/OBD_ImplProp.md §2.A; proposals/wikiResearch.md §1 (missing VE math)
type: analytics_module
status: PROPOSAL (consumer proposed; refines existing ve_engine)
date_extracted: 2026-06-07
---

## What it proposes
Implement the volumetric-efficiency engine and a `_classify_validity` step:

    VE = (maf · R_GAS · IAT_K) / (map_kpa · (rpm/60) · (displacement/2) · MM_AIR) · 100

with classifier states:
- `FAULT_VE_IDLE_COLLAPSE` — VE < 50 % at idle with MAP > 45 kPa (blown grounds /
  collapsed 5 V rail: signals flatline or TPS floats 100 %, denominator inflates).
- `FAULT_VE_SENSOR_SKEW` — VE > 90 % at NA idle (capacitor-leak AC ripple spiking
  MAP/MAF inputs).
- plus traditional states `FAULT_MAF_CONTAMINATION`, `FAULT_VACUUM_LEAK`.

## Diagnostic rationale
wikiResearch.md flags the **complete absence of the VE math engine** as the top gap that
blocks VE-based diagnosis (MAF contamination, cam timing). This supplies it.

## Proposed consumer + code path
Producer: OBDLab `core/ve_engine.py` emitting `ve_pct` + `ve_validity`. Consumer:
`comlab/core/fault_atlas_router.py` (VE cross-ref) and Absolute-Load comparison
([[EP-OBD-IN-02_absolute-load-pid]]). Numeric literals carry wiki citations per CLAUDE.md.

## Dependencies / related
[[EP-OBD-11_theoretical-airflow-crosscheck]] · [[EP-OBD-IN-08_iat-field]] ·
[[EP-ECU-05_5v-regulator-collapse]] · [[EP-ECU-01_capacitor-leakage]].
