---
chunk: pids-protocol/05_maf-linearity-theoretical-airflow
topic: pids-protocol
sources:
  - research/MAFLinearity.md — two-point non-linearity delta + threshold ladder (Gemini research, LaTeX readable)
  - proposals/AddObdFields.md §Part 1 — speed-density theoretical airflow W_theo
  - proposals/extracted/EP-OBD-11_theoretical-airflow-crosscheck.md
consumer: OBDLab speed-density W_theo cross-check emitting `w_theo` + `sensor_error_delta`; COMLab `fault_atlas_router` MAF-contamination-vs-healthy discriminator (EP-OBD-11). Catches a dirty/drifted MAF that reads correctly at idle but under-reports under load, with no open-circuit DTC.
consumer_status: PROPOSAL (EP-OBD-11 — consumer named, not yet wired)
provenance: MAFLinearity.md readable (LaTeX survives — $W_{theo}$, $\Delta Sensor\_error$, % thresholds intact); W_theo form from AddObdFields §Part 1.
dedup: quantified *detection method* for the under-report *profile* in delta-relations/04; pairs with the static crosscheck in pids-protocol/02 (MAF/MAP/TPS rationality) but is a distinct two-point linearity test.
---

# MAF linearity — two-point theoretical-airflow cross-check

A contaminated hot-wire MAF reads plausibly at idle but **under-reports as airflow rises** — an
insulating dust/oil layer blocks the high-velocity cooling the sensor depends on. A single snapshot
misses it; a **two-point** comparison against speed-density theoretical airflow exposes it without
an open-circuit DTC.

## Theoretical airflow (speed-density)

    W_theo = (η_V · V_disp · P_manifold · RPM) / (120 · R · T_intake)

(η_V volumetric efficiency, V_disp displacement, P_manifold MAP, R gas constant, T_intake = IAT in K.)
Requires `intake_air_temp_c` (see ecu-diagnosis / IAT field) and MAP.

## The non-linearity delta

    ΔSensor_error = |Sensor_2500 − W_theo_2500| − |Sensor_750 − W_theo_750|

A clean sensor's error curve runs **parallel** to theoretical → `ΔSensor_error ≈ 0`. Contamination
makes the 2500 RPM error **dwarf** the 750 RPM error, driving the delta upward.

## Threshold ladder (% deviation between the two points)

| Zone | ΔSensor_error | Behaviour |
|---|---|---|
| **Linear / healthy** | **< 3–4 %** | error curve parallel; LTFT absorbs the uniform offset, no flag |
| **Calibration drift / dirty** | **5–12 %** | the magnitude separating health from drift; idle-vs-load fuel-trim *split* (trims at 750 ≠ trims at 2500) |
| **Component fault** | **> 12–15 %** | non-linearity severe (lean surge under accel); ECU can no longer compensate → typically sets **P0101** (MAF range/performance) |

## Discriminator value

Separates a **calibration-drifted (dirty) MAF** — electrically intact, DTC-silent — from an
open-circuit MAF (which sets P0102). It is the quantified detector behind the under-report ΔTrim
profile (`delta-relations/04`): that profile *describes* the trim signature; this *measures* the
sensor non-linearity that causes it.

Citation: threshold ladder (3–4 % / 5–12 % / 12–15 %) and the dirty-hot-wire physics per
`research/MAFLinearity.md`; `W_theo` per AddObdFields §Part 1; P0101 per SAE J2012 / ISO 15031-6.
Consumer PROPOSAL — EP-OBD-11 (`fault_atlas` MAF-contamination discriminator); ships field +
consumer together per signal/noise.


## Core Entities

- w_theo, sensor_error_delta, MAF_UNDERREPORT, P0101, P0102, intake_air_temp_c
- fault_atlas MAF-contamination discriminator (PROPOSAL, EP-OBD-11)

## Graph relations (explicit)

**w_theo** COMPUTED_FROM VE, displacement, MAP, RPM, and **intake_air_temp_c**
**sensor_error_delta** of 5-12% INDICATES **MAF_UNDERREPORT** (dirty, DTC-silent)
**sensor_error_delta** above 12-15% SETS **P0101**
**w_theo** and **sensor_error_delta** EMITTED_BY OBDLab and CONSUMED_BY **fault_atlas MAF-contamination discriminator**
**maf-linearity** MEASURES the cause behind **delta-relations/04** MAF_UNDERREPORT profile

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
