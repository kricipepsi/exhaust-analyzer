---
proposal_id: EP-OBD-IN-08
title: Add Intake Air Temperature (IAT) as an OBDLab input field
target_lab: OBDLab (input) → OBDLab VE engine + COMLab ECU checker
source: proposals/OBD_ImplProp.md (VE formula T_intake); chunks/ecu-diagnosis/05 (field gap)
type: input_field
status: PROPOSAL (consumer proposed; field gap)
date_extracted: 2026-06-07
---

## What it proposes
Ingest **Intake Air Temperature** (`intake_air_temp_c`). The ecu-diagnosis pass logged
IAT as **absent** from `OBDLivePayload`. It is required by the speed-density VE/airflow
math (T_intake term) and is a signature input for ECU ground-trace (IAT floats to
−40 °C alongside ECT).

## Diagnostic rationale
- VE / theoretical-airflow calculation needs intake charge temperature for air density.
- Mode-4 ECU ground-trace tell: IAT = −40 °C + TPS = 100 % + ECT = −40 °C simultaneously
  is a digital-lie signature no single bad sensor produces.

## Proposed consumer + code path
OBDLab `core/ve_engine.py` (density term) and the COMLab ECU-hardware-fault checker
([[EP-COM-04_ecu-hardware-fault-checker]]). Per signal/noise: IAT earns a field only
because these two consumers name it.

## Dependencies / related
[[EP-OBD-11_theoretical-airflow-crosscheck]] · [[EP-ECU-04_sensor-ground-trace-blown]].
