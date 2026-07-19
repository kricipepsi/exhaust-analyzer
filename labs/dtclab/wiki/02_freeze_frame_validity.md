---
node_type: wiki
lab: dtclab
module: dtclab
subsystem: freeze-frame-validation
implements:
  - "labs/dtclab/dtclab/schemas/freeze_frame.py"
  - "labs/dtclab/dtclab/core/freeze_frame_extractor.py"
consumers:
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py DTCLabPayload freeze_frame integration"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py freeze_frame.calculated_load_pct PID source / FuelSystemStatus.CL gate"
drift_guards:
  - "labs/dtclab/tests/unit/test_freeze_frame_extractor.py"
  - "labs/dtclab/tests/unit/test_payload.py"
tags: [dtclab, wiki, freeze-frame-validation]
source: "labs/dtclab/wiki/02_freeze_frame_validity.md"
---
# 02 — Freeze-frame validity gates & interpretation

Anchors: `DTC_VOCABULARY.md §12` (`FreezeFrameRecord`), `§12.3` (derived symptom
flags). See `00_INDEX.md` for scope.

---

## 2.1 Mandated freeze-frame parameter set (v2 pin)

Denton §5.4.4 enumerates the SAE-mandated set of parameters the PCM stores in the
Mode `$02` freeze frame at the instant a DTC sets. This pins the
`FreezeFrameRecord` mandatory-PID list (`DTC_VOCABULARY.md §12.1`) to an
authoritative source rather than an invented one. Source:
`AdvAutomotiveFaultDiagnosis_ANALYSIS.md` §A3.

Mandated stored set: **calculated/derived load, engine speed, STFT/LTFT, fuel
(rail) pressure, vehicle speed, coolant temperature, intake-manifold pressure,
open/closed-loop fuel-system status, and the triggering DTC.** This is reference
corroboration for the existing 12-field mandatory schema — it adds no new field;
it confirms the set DTCLab already emits to COMLab fusion.

---

## 2.2 Calculated Load Value (CLV) threshold table

CLV (PID `$04`) is the percentage of peak available torque at current RPM. It
reaches 100% at WOT regardless of altitude or temperature. **Not throttle
position.**

| CLV range | Engine condition | Diagnostic implication |
|---|---|---|
| < 30% | Idle or light cruise | Fault is idle-circuit, vacuum leak, EGR, EVAP |
| 30 – 70% | Light to moderate cruise | Sensor drift, sustained fuel-trim codes |
| > 70% | High-stress load | Fuel delivery (pump/filter), ignition breakdown, boost leak |
| > 70% AND RPM < 1500 | High load at low RPM | Flag `ff_load_high_at_low_rpm` — stalling under demand; torque-converter stall, clutch slip |

The 70% threshold derives from Innova Diagnostic Reference / Autodtcs FF docs.

---

## 2.3 ECT gate for freeze-frame validity

| ECT range | Engine state at fault time | DTCLab action |
|---|---|---|
| < 60°C | Warm-up transition | Flag `ff_ect_warmup`; cold-enrichment residuals still present; weight fuel-trim evidence lower |
| 60 – 70°C | Upper warm-up boundary | Enrichment decaying; treat with caution |
| ≥ 70°C | Fully warm | Freeze-frame evidence valid; all candidates eligible |
| ≥ 100°C | Unusually hot | Consider cooling system or heat-related failure |

**Catalyst monitor gate:** P0420 requires ECT ≥ 70°C to be a valid test. A P0420
freeze frame with ECT < 70°C was set before catalyst light-off — demote
catalyst-failure candidates.

ECT 70°C boundary from Nissan OBD service docs / Ford PCED, corroborated by
Denton's warm-up-cycle minimum (≥ 70°C with +22°C rise).

---

## 2.4 Freeze-frame interpretation rules

Four core rules applied when reading freeze-frame fuel-trim data. Resolve the
most common DTC-evidence-vs-physical-fault ambiguities.

### 2.4.1 Open-loop fault rule

> If `fuel_system_status ∈ {OL, OL_FAULT}` and the DTC is P0171 or P0172, the
> fault set **before** the O₂ sensor reached operating temperature. Fuel-trim
> values reflect base fuel map behaviour during cold start, not closed-loop
> feedback. Do not diagnose mixture faults from this freeze frame.

Sets `ff_open_loop_at_fault`; downstream candidates that depend on closed-loop
trim evidence are demoted.

### 2.4.2 False-lean rule (misfire masking)

> An active misfire (P0300 – P0312) sends unburned O₂-rich exhaust past the
> upstream sensor, causing it to read lean and driving STFT positive. This can
> produce P0171 as a secondary code from a primary misfire, not a true lean
> condition.

Resolution: when both `P030x` AND a `LEAN_HISTORY`-tagged DTC are present in the
same freeze frame, prefer the misfire interpretation. The lean code is a
downstream artefact. If STFT is strongly positive AND misfire counters on Mode
`$06` MID `$A1`–`$A9` are incrementing on a specific cylinder, the lean code is
misfire-masked.

### 2.4.3 Low-load lean rule

> `calculated_load_pct < 30%` at idle with `short_term_ft1 > +15%` → the lean
> condition is at low load.

Discriminates **vacuum leaks** (constant unmetered air volume, more dilutive at
low flow) from **fuel-delivery faults** (worsen under high load).

- Idle-load lean → vacuum leaks, EGR passages, IAC/ETC, post-MAF intake gaskets.
- High-load lean → fuel pump volume, fuel-filter restriction, fuel-pressure
  regulator.

### 2.4.4 Neutral-trim misfire rule

> If STFT and LTFT are both near 0% AND a misfire DTC (P030x) is present, the
> fault is **not** a mixture imbalance.

ECU is not compensating with fuel because combustion is failing at the ignition
or mechanical stage, not the fuelling stage. Investigate coil output, plug
condition, compression, or injector timing on the affected cylinder.

## Graph relations (explicit)

**FreezeFrameRecord** ENUMERATES **calculated_load_pct**, **engine_rpm**, **coolant_temp_c**, **short_term_ft1**, **long_term_ft1**, **manifold_pressure_kpa**, **vehicle_speed_kmh**, **ignition_advance_deg**, **intake_air_temp_c**, **maf_gps**, **throttle_pos_pct**, **fuel_system_status**
**FreezeFrameRecord** CONSUMED_BY **dtclab/schemas/freeze_frame.py**
**calculated_load_pct** > 70 AND **engine_rpm** < 1500 TRIGGERES **ff_load_high_at_low_rpm**
**coolant_temp_c** < 60°C TRIGGERES **ff_ect_warmup**
**fuel_system_status** ∈ {OL, OL_FAULT, OL_DRIVE} TRIGGERES **ff_open_loop_at_fault**
**intake_air_temp_c** − **coolant_temp_c** > 30°C AND **engine_rpm** == 0 TRIGGERES **ff_iat_ect_biased**
**ignition_advance_deg** < -10° TRIGGERES **ff_timing_retard_severe**
**open-loop fault rule** SETS **ff_open_loop_at_fault**
**false-lean rule** RESOLVES **P030x** AND **P0171**
**low-load lean rule** DISCRIMINATES **vacuum leaks** FROM **fuel-delivery faults**
**neutral-trim misfire rule** IDENTIFIES **ignition_fault** OR **mechanical_wear**

## Core Entities

- **FreezeFrameRecord** — Struct of Mode $02 PID values captured at code trigger. Consumer: `dtclab/schemas/freeze_frame.py`.
- **ff_load_high_at_low_rpm** — Symptom flag indicating torque overload or potential stall context. Consumer: `dtclab/core/freeze_frame_extractor.py`.
- **ff_ect_warmup** — Symptom flag indicating engine was not fully warmed up at fault time. Consumer: `dtclab/core/freeze_frame_extractor.py`.
- **ff_open_loop_at_fault** — Symptom flag indicating open loop status during fault trigger. Consumer: `dtclab/core/freeze_frame_extractor.py`.
- **ff_iat_ect_biased** — Symptom flag indicating temperature sensor correlation error at key-on. Consumer: `dtclab/core/freeze_frame_extractor.py`.
- **ff_timing_retard_severe** — Symptom flag indicating excessive timing retard. Consumer: `dtclab/core/freeze_frame_extractor.py`.

