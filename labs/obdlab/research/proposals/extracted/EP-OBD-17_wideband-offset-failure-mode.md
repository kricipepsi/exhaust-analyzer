---
proposal_id: EP-OBD-17
title: WIDEBAND_OFFSET two-stage O₂ failure-mode expression
target_lab: OBDLab (o2_normalizer.py) → COMLab fusion
source: chunks/o2-logic/README §reconciliation; SWEEP_MANIFEST O2-FU-1; sources/o2-logic/O2logic.md
type: enum_value + fault_node
status: PROPOSAL (accepted v2 addition; placement decided, spec pending)
date_extracted: 2026-06-07
---

## What it proposes
Two-stage wideband-calibration-offset detector (source term `BIASED_OFFSET`):
- **Stage 1 (OBDLab):** `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` — emit when
  sensor = `WIDEBAND_LINEAR` AND persistent `|normalized_obd_lambda − 1.0| > 0.05`.
- **Stage 2 (COMLab):** fusion confirms against GASLab `λ_chem ≈ 1.0` → new
  `SENSOR_FAULT` wideband-calibration node in `fault_atlas_router`.

## Diagnostic rationale
A wideband sensor reading a constant small offset from stoichiometric looks like a real
mixture error to the PCM; only cross-checking against chemical λ exposes it as a sensor
calibration fault. Field + consumer ship together (v2 forward-progress rule).

## Proposed consumer + code path
Producer OBDLab `core/o2_normalizer.py`; consumer COMLab `fault_atlas_router.py`. Spec
must pin threshold, persistence window, the candidate→confirm JSON boundary field, and
the fault-atlas node id (O2-FU-1).

## Dependencies / related
[[EP-COM-03_lambda-cross-delta-engine]] · [[EP-GAS-01_5gas-brettschneider-schema]].
