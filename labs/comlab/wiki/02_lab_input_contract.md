---
chunk_id: COMWIKI-02
title: Lab Input Contract — every field COMLab consumes
doc: COM_WIKI
version: v2.1
date: 2026-06-21
status: authoritative
summary: 'The signal inventory: every field read from GASLab, OBDLab, DTCLab, DNALab
  and SymptomDNA at Stage A/B, plus the v2 provenance-flag proposal that makes synthetic/imputed
  values observable. v2.1 adds §2a — the COMLab-local consumer bands for the OBD analytic
  fields, so a consumer never reaches into another lab''s research at diagnostic time.'
entities_defined:
- CONCEPT_GAS_INPUT
- CONCEPT_OBD_INPUT
- CONCEPT_OBD_CONSUMER_BANDS
- CONCEPT_DTC_INPUT
- CONCEPT_DNA_INPUT
- CONCEPT_SYMPTOM_INPUT
- CONCEPT_PROVENANCE
related_chunks:
- COMWIKI-01
- COMWIKI-03
- COMWIKI-05
- COMWIKI-07
- COMWIKI-12
sources:
- COMLab_HLD.md §7
- SEMANTIC_CONTRACT.md §4–§5
- OBD_VOCABULARY.md
- DTC_VOCABULARY.md
- GAS_VOCABULARY.md
- REWORK_PLAN_COMLab.md §3.C
node_type: wiki
lab: comlab
module: comlab
subsystem: input-contract
implements:
- labs/comlab/comlab/schemas/ingestion.py
consumers:
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state / total_trim_correction_delta
  / confirmed_dtcs routing'
- 'comlab: labs/comlab/comlab/core/ecu_hardware_checker.py OBD-rail evidence
  (intake_air_temp_c / coolant_temp_c / throttle_pos_pct / total_trim_correction_delta
  / per_bank_trim_delta)'
- 'comlab: labs/comlab/comlab/core/symptom_router.py route_symptom engine_state
  suppression'
drift_guards:
- labs/comlab/tests/unit/test_ingestion_high_idle.py
- labs/comlab/tests/unit/test_fuel_system_gate.py
- labs/comlab/tests/unit/test_fault_atlas_router.py
tags:
- comlab
- input-contract
- wiki
source: labs/comlab/wiki/02_lab_input_contract.md
---

# Lab Input Contract — every field COMLab consumes

This is the signal inventory COMLab reads during Stage A (`lab_pipeline_aggregator.py`) and
Stage B (`fault_atlas_router.py`). It is the surface the fusion stage (`COMWIKI-08`) draws its
evidence from. Every field is owned by an emitter lab and **mirrored locally** in
`schemas/ingestion.py` (`→ CONCEPT_ISOLATION`).

## 1. GASLab — `GasLabPayload` {#CONCEPT_GAS_INPUT}

The tailpipe chemistry; `chemical_state` is the **primary route key** into the fault registry.

| Field | Type | Range | Diagnostic meaning |
|---|---|---|---|
| `chemical_state` | Enum (34 values, v2.1) | — | primary route key into the registry; see GAS_VOCABULARY §3/§21 |
| `lambda_chem` | float | 0.5–2.5 | Brettschneider equivalence ratio; λ<0.97 rich, >1.03 lean. **Ground truth** for perception-vs-truth. |
| `gas_hc` | int ppm | 0–20000 | unburned HC; >120 ppm at idle = misfire/oil trace |
| `gas_co` | float % | 0–15 | CO; >1.5 % = rich |
| `gas_co2` | float % | 0–22 | combustion-efficiency proxy; <13 % = deficit |
| `gas_o2` | float % | 0–22 | free O₂; >4 % = severe lean or air leak |
| `gas_nox` | int ppm | 0–5000 | 5-gas only; >1000 ppm at idle = lean/EGR |
| `lambda_measured` | float \| None | 0.5–2.0 | optional analyser λ; fallback when OBD λ absent (T-FX-7) |
| `sample_validity` | Enum: VALID / BORDERLINE / INVALID / EXTERNAL_O2_SUSPECT | — | Stage-A Gate 1 (`→ GATE_GAS_SAMPLE`) |
| `reading_high` | `GasReading \| None` | — | **optional 2500-RPM frame** (T-GV2-4) — enables Δgas (`COMWIKI-11`) |
| `high_idle_{hc,co,co2,o2,nox,lambda}` | float \| None | — | the high-idle frame's per-gas values |

v2 note: GASLab's `ChemicalSignature` contract is **34-value** (the v2.1 timing-taxonomy split
retired `WRONG_VALVE_TIMING` for three `CAM_TIMING_*` states). COMLab's mirror reconciliation to
34 is `T-GV2-2`/`FU-1` (DEP-1, deferred to S4 — `tasks/PROGRESS.md`). [v2: GASWIKI-06B]

## 2. OBDLab — `OBDLiveDataPayload` {#CONCEPT_OBD_INPUT}

The ECU's correction signal. `total_trim_correction_delta` is the strongest secondary signal
after `chemical_state`.

| Field | Type | Range | Diagnostic meaning |
|---|---|---|---|
| `engine_warmed` | bool | — | Stage-A Gate 2 (`→ GATE_ENGINE_WARMED`) |
| `total_trim_correction_delta` | float % | −200…+200 | shrtft1+longft1; + = ECU adding fuel (lean), − = pulling fuel (rich) |
| `total_trim_correction_delta_b2` | float % | −200…+200 | bank-2 twin; `_b1`/`_b2` asymmetry → `T-COMV2-BANK-FUSE-1` |
| `lambda_perception_delta` | float | — | OBD λ-perception vs reality half; → `T-COMV2-ECU-FUSE-1` |
| `normalized_obd_lambda` | float | 0.7–1.3 | ECU's perceived λ; compare to GAS `lambda_chem` |
| `ve_pct` / `ve_validity` | float % / Enum | 0–100 | volumetric efficiency + trust flag; → `T-COMV2-VE-GATE-1` |
| `rpm_state_bucket` | Enum: STABILIZED_IDLE / REGULATORY_HIGH_IDLE / STRESS_IDLE / COLD_OPEN_LOOP_INVALID | — | which RPM context the trims apply to; the two-point key |
| `trim_analytics_gate` | Enum (9 values) | — | whether trim data is reliable (VALID / ENGINE_COLD / OPEN_LOOP / …) |
| `fuel_system_status` | Enum: CL / OL / OL_DRIVE / OL_FAULT | — | closed/open-loop; → `T-COMV2-FUELSYS-GATE-1` |
| `o2_failure_mode` | Enum (7 values incl. WIDEBAND_OFFSET_CANDIDATE) | — | O₂ behaviour; → `T-COMV2-O2OFFSET-1` |
| `maf_status` / `map_status` | Enum (4 values) | — | sensor health + calibration flag |
| `per_bank_trim_delta` | float \| None | — | per-bank asymmetry (None on single-bank) → `T-COMV2-BANK-FUSE-1` |
| `per_cylinder_misfire_counts` | list[int] | — | misfire localiser → `T-COMV2-MISFIRE-LOC-1` |
| `w_theo` / `sensor_error_delta` | float | — | MAF linearity → `T-COMV2-MAF-LIN-1` |
| `ltft_cell_vector` | list[float] | — | load-cell LTFT classification → `T-COMV2-LTFT-CELL-1` |
| `intake_air_temp_c` / `throttle_pos_pct` / `coolant_temp_c` | float | — | ECU-hardware-lie signature → `T-COMV2-ECU-HW-1` |
| `control_module_voltage_v` | float | — | rail health pre-check → `T-COMV2-VPWR-GATE-1` |
| `freeze_frame_pids` | optional | — | snapshot at fault moment (single, async) |

**Trim thresholds** used in registry rules (literals carry registry/OBD_VOCABULARY citations):
±0–5 % within authority; ±5–15 % compensating; ±15–25 % typical rule threshold; >±25 %
adaptation saturated (`ERR-EF-001`); `< −23 %` unmetered-fuel intrusion (`ERR-RM-005`).

## 2a. OBD analytic-field consumer bands — COMLab-local {#CONCEPT_OBD_CONSUMER_BANDS}

> **Single-lab isolation (why this section exists).** A diagnosis may run on **one lab's
> payload alone** — if no DTC is present, DTCLab is never invoked; a legacy/no-OBD session
> carries no `obd_live_data`. A consumer therefore (a) treats an absent upstream payload/field
> as **inert** (default-`None` → no verdict), and (b) reads its interpretation **thresholds from
> this COMLab wiki**, never from another lab's research tree at diagnostic time. The bands below
> are the COMLab-local truth for the OBD analytic fields; the OBDLab research chunk is recorded
> only as **provenance of record**, not a runtime dependency. (Added 2026-06-21.)

### MAF linearity ladder — `w_theo` + `sensor_error_delta` → `T-COMV2-MAF-LIN-1`

`sensor_error_delta` is the two-point non-linearity % deviation vs theoretical airflow `w_theo`
(`ΔSensor_error = |Sensor_2500 − W_theo_2500| − |Sensor_750 − W_theo_750|`).

| Band | `|sensor_error_delta|` | Verdict |
|---|---|---|
| Linear / healthy | `< 3–4 %` | uniform offset; LTFT absorbs it — no flag |
| Calibration drift / dirty | `5–12 %` | dirty-but-connected MAF → `ERR-LC-002` |
| Component fault | `> 12–15 %` | severe non-linearity → `P0101` (range/performance) |

An **open-circuit MAF** reads *no* signal and sets **`P0102`** — it is the contrast this ladder
keeps a dirty-but-connected MAF from being mis-routed into. *Provenance:* `obdlab/research/chunks/pids-protocol/05_maf-linearity-theoretical-airflow.md`.

### Control-module rail bands — `control_module_voltage_v` → `T-COMV2-VPWR-GATE-1`

| Rail | Reading | Interpretation |
|---|---|---|
| Healthy | `~13.5–14.7 V` running | clean reference |
| **Low** | `< 12.0 V` (esp. `< 11.5 V` with unstable trim) | charging/ground fault — flag **before** sensor-fault routing |
| **High** | `> 15.0 V` (system `> 15.5 V`) | over-charging; AC ripple corrupts references |

ΔVPWR (low→high-idle sweep, future two-point): `< −1.0 V` under revs ⇒ alternator/regulator diode
fault; `> +2.5 V` ⇒ over-charging (feeds the alternator-AC-ripple node, `EP-FA-05`, deferred).
*Provenance:* `obdlab/research/chunks/ecu-diagnosis/09_control-module-voltage.md`.

### LTFT load-cell distribution — `ltft_cell_vector` → `T-COMV2-LTFT-CELL-1`

The PCM learns a matrix of LTFT cells indexed by load × RPM. The **distribution** of lean
(`> +5 %`, per §2 authority bands) discriminates cause:

| Distribution (COMLab v1) | Cause family |
|---|---|
| `LOCALISED` — lean in a subset of populated cells | region-specific (idle vacuum leak / mid-range delivery) |
| `GLOBAL` — lean across all populated cells | global cause (MAF / fuel pressure / O₂ bias) |

The finer **idle-only vs part-throttle-only** split needs an OEM cell-index → operating-region
map (the cell index encodes operating context, OEM-specific — GMH example only), which the emitter
does not yet supply; it is **deferred**, not inferred. *Provenance:* `obdlab/research/chunks/fuel-trim/13_ltft-load-cell-matrix.md`.

### Misfire localisation — `per_cylinder_misfire_counts` → `T-COMV2-MISFIRE-LOC-1`

A misfire pumps fresh O₂ past the upstream sensor → a **false-lean** positive trim, so counts are
read **together with** `total_trim_correction_delta`:

| Counts + trim | Locality |
|---|---|
| Positive trim `> +15 %` + **one** cylinder's count escalating | `SINGLE_CYLINDER` — localised (coil / plug / leaking injector); not a fuelling mis-route |
| High positive trim + counts **spread** across cylinders | `GLOBAL` — fuel starvation (weak pump) |

Per-cylinder counts are portable on CAN (≈2008+); pre-CAN MID/TID are per-OEM, so an absent dict
is the legacy-inert case. *Provenance:* `obdlab/research/chunks/fuel-trim/17_per-cylinder-misfire-counts.md`.

### ECU-hardware digital-lie signature — `intake_air_temp_c` + `throttle_pos_pct` + `coolant_temp_c` → `T-COMV2-ECU-HW-1`

A failed/stuck ECU or a chewed sensor harness produces a **physically impossible but internally
coherent** reading — the diagnostic tell is that several independent sensors rail to their floor/ceiling
*together*. Read as an AND-gate (any input absent → inert):

| Channel | Lie value | Note |
|---|---|---|
| `intake_air_temp_c` | `≤ −40 °C` | sensor floor / open-circuit |
| `coolant_temp_c` | `≤ −40 °C` | sensor floor / open-circuit (both temps at floor at once is the coherent lie) |
| `throttle_pos_pct` | `≥ 100 %` | rail (with no corresponding load) |
| `total_trim_correction_delta` | `\|Δ\| ≥ 25 %` | saturated (`ERR-EF-001`, §2 line70) |
| `per_bank_trim_delta` | `None` or `\|Δ\| ≤ ±5 %` | **bank-symmetric** — global, not bank-local (asymmetric is `T-COMV2-BANK-FUSE-1`) |

All conditions together → internal-ECU / wiring fault → route to the **`ecu_fault`** family (`ERR-EF-001`,
`06_fault_atlas_families.md §CONCEPT_FAM_ECU`; P06XX). The point is to stop the engine reading the railed
trim as a real lean/rich verdict. *Provenance:* OBD Mode-04 reset behaviour; proposals `EP-COM-04` /
`EP-OBD-IN-08` / `EP-OBD-IN-05` (`13_proposals_register.md` §B).

> The **bank-asymmetry** (`per_bank_trim_delta`, ±5 % bound) and **symptom-prior cap** (`load_state`,
> 65 % trust) bands are already COMLab-local — §2 authority bands + `04_horizon_eras.md §CONCEPT_LEGACY`
> for the former, `10_differential_and_symptom_prior.md §RULE_SYMPTOM_PRIOR` + `config/symptom_prior.yaml`
> for the latter — so they need no mirror here.

## 3. DTCLab — `DTCLabPayload` {#CONCEPT_DTC_INPUT}

Hard fault codes + the freeze-frame / Mode `$06` historical context.

| Field | Type | Diagnostic meaning |
|---|---|---|
| `active_mil` / `mil_flashing` | bool | MIL on / flashing (catalyst-damage-imminent trigger → `RULE_CAT_OVERRIDE`) |
| `confirmed_dtcs` / `pending_dtcs` / `permanent_dtcs` | list[str] | codes matching `^[BCPU][0-3][0-9]{3}$` |
| `routing_tags` | list[DTCRoutingTag] | semantic tags (EGR, EVAP, MISFIRE, POA_HISTORY, …) |
| `historical_fault_context` | Enum: HISTORICAL_IDLE_FAULT / HISTORICAL_LOAD_FAULT / COLD_START_TRANSIT_FAULT / UNKNOWN | when the code was written |
| `mode_06_monitors` | dict | per-monitor PENDING_FAIL / CRITICAL_FAIL; non-start branch → `T-COMV2-NOSTART-1` |
| `freeze_frame` | `FreezeFrameRecord` | PIDs at fault moment (RPM, ECT, load, trims) |

**Freeze frame is a conditional evidence channel** — present only when a DTC is stored, fused at
the verdict stage, **never as a delta input** (it is one asynchronous, uncontrolled-operating-
point snapshot). Its uses: corroborate/contradict the live delta, and catch intermittent/
load-specific faults the no-load delta cannot reproduce. Caveat: generic OBD-II stores **one
priority frame** (may belong to a higher-priority DTC — check Mode `$02` PID `$02`), 1996+ only.
[v2: REWORK_PLAN §8.3; consumer `T-COMV2-NOSTART-1` + fusion intermittent-fault branch] **[PROPOSAL]**

## 4. DNALab — `VehicleDNA` → 3 `LabDnaViews` {#CONCEPT_DNA_INPUT}

The hardware profile that gates pruning. COMLab reads the **resolved** tokens; it never
re-derives the horizon from the VIN. Full pruning mechanics: `COMWIKI-03`.

| Field | Type | Pruning role |
|---|---|---|
| `resolved_horizon` | Enum: HORIZON_LEGACY / ADAPTIVE / MODERN | Pass 1 era prune (`COMWIKI-04`) |
| `cylinder_count` / `number_of_banks` | int | power-loss math; bank-2 trim validity |
| `induction_type` | Enum: NA / TURBO / SUPERCHARGED | turbo-specific rules; delta sign inversion (`COMWIKI-11`) |
| `fuel_delivery_type` | Enum: GDI / PORT_INJECTION / CARBURETOR | gates GDI-only faults (`ERR-RM-005`, `ERR-MF-007`) |
| `air_metering_strategy` | Enum: MAF_ONLY / MAP_ONLY_SPEED_DENSITY / DUAL_MAF_MAP | polymorphic VE; **speed-density nulls ΔTrim** (`COMWIKI-11`) |
| `has_maf_sensor` / `has_map_sensor` | bool | gate MAF/MAP sensor faults |
| `egr_equipped` / `secondary_air_equipped` / `downstream_o2_present` | bool | gate `ERR-LC-005` / `ERR-LC-007` / `ERR-SF-006` + cat-eff calc |
| `upstream_o2_type` | Enum (5 values) | polymorphic λ normalisation |
| `has_catalyst` | bool | catalyst-damage override gate |
| `stress_idle_rpm_target` | int 2800–5000 | distinguishes STABILISED_IDLE from STRESS_IDLE; the elevated delta point |
| `confidence` | Enum: HIGH / PARTIAL / NONE | degradation-mode classification; NONE → Stage-A abort |

## 5. SymptomDNA (top-level) {#CONCEPT_SYMPTOM_INPUT}

The only sub-structure COMLab receives at the top level. Drives lab suppression (Stage A) and a
bounded symptom prior (`COMWIKI-10`).

| Field | Values | COMLab consumer |
|---|---|---|
| `tier_1_primary_symptom` / `tier_2_subfield_filter` | picker enums | symptom-prior routing keys (`COMLab-A` proposal mappings) |
| `occurs_during` | always / cold_only / hot_only / intermittent | `cold_start_mode` flag |
| `engine_state` | running / cranking / will_not_start | lab-suppression flags (`COMWIKI-07`) |
| `environmental_conditions.load_state` | (DNA `T-DNA-2`) | symptom-prior context modifier; → `T-COMV2-CTXMOD-1` |

## 6. Provenance flags — make synthetic/imputed values observable {#CONCEPT_PROVENANCE}

**[PROPOSAL — v2, pack C]** Every non-observed input field carries a companion provenance flag
∈ {observed, derived, imputed, synthetic, manual-override, sentinel, out-of-range, saturated}.
The rework's binding-constraint finding (`COMWIKI-12`) is that the corpus is partly synthetic
and contains ambiguous sentinels (±127, 999) that must **never** be collapsed into a numeric
variable during train/eval. Making provenance observable is the precondition for the calibration
and eval discipline.

- *Named consumer:* the eval harness + the Stage-A validity gates + the calibration split
  (minority-stratified, fit only on `observed`-flagged rows).
- *Files:* `schemas/ingestion.py` (+ provenance flags), corpus pipeline.
- *Status:* proposal — ships with its consumer in the same change (Gate-Data, `COMWIKI-12`).

## Graph relations (explicit)

**GasLabPayload / OBDLiveDataPayload / DTCLabPayload / VehicleDNA / SymptomDNA** CONSUMED_BY **COMLab.schemas.ingestion**
**chemical_state** IS **primary route key** INTO **global_fault_registry.json**
**total_trim_correction_delta** IS **strongest secondary signal**
**reading_high / high_idle_\*** ENABLE **TEST_TWO_POINT (COMWIKI-11)**
**CONCEPT_PROVENANCE** ENABLES **GATE_DATA (COMWIKI-12)** · **[PROPOSAL]**
**chemical_state** CONSUMED-BY **comlab/core/fault_atlas_router.py**
**total_trim_correction_delta** CONSUMED-BY **comlab/core/fault_atlas_router.py**
**confirmed_dtcs** CONSUMED-BY **comlab/core/fault_atlas_router.py**
**vin_dna** CONSUMED-BY **comlab/core/ecu_hardware_checker.py**
**engine_state** CONSUMED-BY **comlab/core/lab_pipeline_aggregator.py**

## Core Entities

- **CONCEPT_GAS_INPUT** — Tailpipe chemistry chemical_state as the primary routing key. Consumer: `comlab/schemas/ingestion.py (GasLabPayload)`.
- **CONCEPT_OBD_INPUT** — ECU correction signal (total_trim_correction_delta). Consumer: `comlab/schemas/ingestion.py (OBDLiveDataPayload)`.
- **CONCEPT_OBD_CONSUMER_BANDS** — COMLab-local thresholds for trim and O₂ sensor evaluation. Consumer: `comlab/analytics/delta_engine.py and comlab/core/perception_contradiction.py`.
- **CONCEPT_DTC_INPUT** — Hard fault codes and Mode $06/freeze frame historical context. Consumer: `comlab/schemas/ingestion.py (DTCLabPayload)`.
- **CONCEPT_DNA_INPUT** — Hardware profile (displacement, cylinder count, banks, euro category) that gates pruning. Consumer: `comlab/schemas/ingestion.py (VehicleDNA)`.
- **CONCEPT_SYMPTOM_INPUT** — Top-level symptom DNA driving lab suppression and symptom prior weight. Consumer: `comlab/schemas/ingestion.py (SymptomDNA)`.
- **CONCEPT_PROVENANCE** — Provenance flags making synthetic/imputed/saturated values observable. Consumer: `comlab/schemas/ingestion.py (proposed)`.
