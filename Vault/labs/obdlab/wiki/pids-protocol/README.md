---
node_type: "wiki"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "pid-mode06-readiness"
implements:
  - "labs/obdlab/code/core/pid_ingestion_validator.py"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_kg.py — PID/Mode06/readiness fault-atlas keys"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py"
drift_guards:
  - "labs/obdlab/tests/unit/test_pid_ingestion_validator.py"
tags: [obdlab, finished, wiki]
source: "labs/obdlab/research/chunks/pids-protocol/README.md"
---
# chunks/pids-protocol/ — index & disposition ledger


**Date:** 2026-06-07 · **Step:** Phase 2 chunking — pack populated from the
`sources/various/` volume sweep (was empty per SWEEP_MANIFEST §10). Topic = OBD-II
protocol/PID mechanics: Mode 06/Freeze Frame, sensor rationality, ignition waveform,
GDI high-pressure fuel.

## Chunk set

| Chunk | Concept | Consumer | Status |
|---|---|---|---|
| `01_mode06-freezeframe-nostart-method` | Mode $06 MID/TID + Mode $02 FF for no-start/security isolation | DTCLab FF/Mode06 parser → fault_atlas no-start branch | PROPOSAL |
| `02_maf-map-tps-rationality-p0068` | sensor cross-check; inferred BARO; P0068 | OBDLab rationality gate → fault_atlas | PROPOSAL |
| `03_secondary-ignition-waveform-forensics` | firing/burn line + coil ripples; ignition-vs-lean | fault_atlas ignition (manual-entry features) | PROPOSAL |
| `04_gdi-highpressure-fuel-pids` | FRP desired/actual, VCV duty, P0087 | fault_atlas GDI fuel branch | PROPOSAL |
| `05_maf-linearity-theoretical-airflow` | two-point W_theo cross-check; ΔSensor_error 3-4/5-12/12-15 % | OBDLab W_theo → fault_atlas MAF-contamination discriminator (EP-OBD-11) | PROPOSAL |
| `06_readiness-monitors-and-absence-of-dtc-trust` | monitor readiness (Ready/Not-Ready); a missing DTC is trustworthy only if its monitor completed; reset by battery-disconnect/clear; FMEM value-trust note | OBDLab `analytics_preconditions` (demote absence-of-DTC when Not-Ready) → truth-perception `Perception_Reliability_Index` | PROPOSAL |
| `07_fmem-limp-home-substituted-values` | a PID reported under FMEM is a substituted safe default, not a measurement; detect via active circuit DTC for that sensor | OBDLab `analytics_preconditions` (generalised prerequisite-DTC gate — demote candidates reading an FMEM-default PID) → `Perception_Reliability_Index` | PROPOSAL |
| `08_dtc-state-machine-and-confidence-weighting` | DTC lifecycle pending→confirmed→history→erased → per-state confidence weight; a missing-MIL ≠ fixed | DTCLab DTC-state weighting → COMLab `fault_atlas_router` (state-weighted routing) | PROPOSAL |

## Source disposition
`Vol4.md` → 01 (Mode06/FF + 30 era cases; gas-signature cases also feed fuel-trim/
taxonomy). `Vol2.md` MD4→02, MD5→04, MD6→03. All concepts readable; scattered numeric
specs in Vol2 tables were image-stripped — logged in the formula wiki pending list, not
reconstructed. **Advanced Automotive Fault Diagnosis (Denton, 2nd ed.) §5.4.5/5.4.6/5.3
→ 06, 07, 08** (added 2026-06-08; the data-reliability triad — readiness-flag /
absence-of-DTC trust gate (A2), FMEM substituted-value down-trust (A6), and the
DTC-state→confidence model (A1) — see `../../AdvAutomotiveFaultDiagnosis_ANALYSIS.md`).

## Also routes here (from prior passes)
OBD-I↔OBD-II trim conversion formula (DR-FU-1, delta-relations/README) — pending.

## Note
Every chunk is a PROPOSAL: each names a producer + reader, but none of these PID
streams/feature sets is yet an input field. Per signal/noise, fields ship only when the
named consumer is specced and reads them.


## Core Entities

- pids-protocol (8 PROPOSAL chunks)
- Mode06, rationality, w_theo, monitor_readiness, value_is_fmem, dtc_state
- OBDLab analytics_preconditions + COMLab fault_atlas_router

## Graph relations (explicit)

**pids-protocol** PROPOSES input fields gated by named fault_atlas/analytics consumers
**pids-protocol** REGISTERED_IN **comlab/config/proposals/**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
