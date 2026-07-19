---
node_type: "prd"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "requirements"
implements: []
consumers:
  - "hld: labs/obdlab/docs/HLD_OBDLab.md"
drift_guards: []
tags: [obdlab, finished, prd]
source: "labs/obdlab/docs/PRD_OBDLab.md"
---
# PRD — OBDLab
**Status:** Approved
**Version:** 2.0
**Date:** 2026-06-10
**Scope:** Petrol-only, v2 — OBD live-PID analytics module (revive-as-emitter rework)

---

## Section 1 — Summary

OBDLab is the **electronic-perception channel** of the 4D petrol diagnostic pipeline (the L5 live-PID layer). It accepts a raw dict of OBD-II PIDs plus a typed vehicle DNA view (`ObdLabDnaView`, 7 fields), runs a 7-step pipeline (PID ingestion → RPM bucketing → semantic consistency → VE computation → O2 normalisation → trim aggregation → analytics gating), and emits a 31-field `OBDLivePayload` that represents the **ECU's perception** of engine state. COMLab compares this perception against GASLab's chemistry ground truth.

The v2 rework (T-OBDV2-0 through T-OBDV2-11, 2026-06-08–10) revived OBDLab as a **pure emitter** after determining the >95% NO_FAULT result that prompted the quarantine review was a PID-less-corpus artefact, not a code defect. OBDLab emits its own channels — trims, normalised lambda, VE, perception deltas, sensor provenance — and does **not** produce fault-family verdicts. That cross-referencing and final root-cause verdict is COMLab's job (see `HLD_OBDLab.md` §1, §7).

Truth-vs-Perception framing unchanged: the ECU is **perception**; GASLab Brettschneider lambda is **ground truth**.

---

## Section 2 — Contacts

| Name | Role | Responsibility |
|------|------|----------------|
| OBDLab Owner | Module Owner | PID ingestion, VE engine, O2 normaliser, trim analytics gate, MAF linearity |
| COMLab Team | Integration Consumer | Reads `OBDLivePayload`; populates `freeze_frame_pids` before calling OBDLab; consumes perception delta, bank asymmetry, VE evidence, O2 failure mode |
| 4DApp Engineering Lead | Architecture | Signal/noise rule; cross-lab JSON contract; emitter-vs-judge division of labor |

---

## Section 3 — Background

**Context.** OBD-II (ISO 15031 / SAE J1979) standardises real-time engine sensor access for all post-1996 petrol vehicles. Fuel trims (`STFT`, `LTFT`), manifold pressure, mass airflow, coolant temperature, intake air temperature, throttle position, and control module voltage together describe how the ECU is managing the engine. These are the ECU's perception signals — they can be correct or wrong, but they are always present.

**Why now.** The OBD standard is stable. The combination of `pydantic` v2 field validators and the `physical_sensor_bounds.json` drift guard means sensor boundaries can be enforced at ingestion and kept in sync with the wiki automatically. The v2 revive-as-emitter rework added 10 fields to the payload (21→31), widened trim bounds to the OBD rail (±127) to preserve sensor-fault signalling, replaced the legacy O2 failure taxonomy with a 4-value consumer-backed classification, and removed Physics Gate 3 (superseded by `FAULT_VE_SENSOR_SKEW` in the VE validity classifier).

**What recently became possible.** The 3-branch VE routing (dual MAF+MAP crosscheck, MAP-only speed-density, MAF-only) plus the DNA-first configuration model allows OBDLab to handle any petrol engine metering strategy without embedded lookup tables. MAF linearity monitoring (`w_theo`, `sensor_error_delta`) adds a two-point non-linearity check across idle and stress RPM bands. The guarded-emitters pattern (HLD §3) allows fields like `lambda_perception_delta` and `sensor_error_delta` to ship now with forward-registered COMLab consumers (HLD §7) without blocking on the Stage 4 COMLab rework.

---

## Section 4 — Objective

**Business benefit.** Provide ECU-perception data at the same abstraction level as GASLab's chemistry, so COMLab can compute a meaningful delta and route fault hypotheses.

**Customer benefit.** Technicians see validated, unit-normalised OBD data (fuel trims, VE, lambda, MAF linearity) in consistent units with known validity flags — no manual unit conversion, no guessing whether a value is in PSI or kPa.

**Key Results:**

- **KR1:** OBDLab pipeline processes a warm-idle HIGH-confidence DNA payload in < 50 ms on reference hardware.
- **KR2:** `OBDLivePayload` is structurally valid for all regression fixtures.
- **KR3:** Zero cross-lab Python imports (import-isolation audit in `test_dna_view.py`).
- **KR4:** `physical_sensor_bounds.json` 12-field drift guard passes on every CI run (`test_sensor_bounds.py`).
- **KR5:** `O2FailureMode` taxonomy carries exactly 4 values (NO_FAULT/STUCK_LEAN/STUCK_RICH/WIDEBAND_OFFSET_CANDIDATE); no pruned v1 member survives in code or doc (`test_vocabulary.py`).
- **KR6:** Every payload field has a named consumer (live or forward-registered S4), per signal/noise (HLD §7).

---

## Section 5 — Market Segment

**Advanced workshop technician (OBD-II user):** Professionals who connect an OBD scanner to a petrol vehicle and need the raw PID stream validated, converted to consistent units, and summarised into actionable fuel-trim and VE analytics — without manually computing VE or interpreting raw O2 voltage.

---

## Section 6 — Value Proposition

- **Jobs addressed:** PID validation, unit conversion, VE computation, O2 lambda normalisation, fuel-trim aggregation, trim analytics validity gating, O2 failure mode classification, MAF linearity monitoring, per-cylinder misfire counting.
- **Gains created:** `total_trim_correction_delta` (STFT+LTFT) is computed and validated in one call. `ve_validity` (VEValidity enum) tells COMLab immediately whether VE is trustworthy. `per_bank_trim_delta` exposes bank-to-bank asymmetry. `lambda_perception_delta` quantifies ECU-vs-commanded deviation. `w_theo` and `sensor_error_delta` provide MAF linearity evidence from a two-point (idle + stress) accumulator. Cold-engine state is detected and frozen gracefully.
- **Pains relieved:** Eliminates manual unit conversion (°F, PSI, inHg, lb/min). Bank-2 null contract enforcement prevents silent downstream errors on single-bank engines. OBD-rail trim bounds (±127, per T-W-6) preserve sensor-fault signalling that narrower nominal bounds would discard.
- **Competitive advantage:** 3-branch VE routing handles MAF-only, MAP-only, and dual-sensor strategies. O2 normalisation supports narrowband voltage, wideband linear, and wideband NB-sim sensors in one module. MAF linearity monitoring adds an independent sensor-health channel. The emitter-only stance means OBDLab ships evidence without coupling to COMLab's verdict logic.

---

## Section 7 — Solution

### Key Features (all P0)

- P0: PID ingestion — physical-bounds validation (12 fields per `physical_sensor_bounds.json`, LLD §2) and unit conversion (°F→°C, psi→kPa, inHg→kPa, lb/min→g/s).
- P0: DNA-RPM gate — three-branch confidence (HIGH strict, PARTIAL log, NONE skip).
- P0: Bank-2 null contract — `number_of_banks == 1` enforces `shrtft2 = longft2 = None`.
- P0: Semantic consistency — Physics Gates 1/2/4 + thermal gate + closed-loop gate (Physics Gate 3 removed per FIX-1; superseded by `FAULT_VE_SENSOR_SKEW` in the VE classifier, HLD §3).
- P0: RPM state bucketing — 4 states from `obd_translation_rules.yaml` (STABILIZED_IDLE, REGULATORY_HIGH_IDLE, STRESS_IDLE, COLD_OPEN_LOOP_INVALID); computed before semantics per F-O7 fix (HLD §3 step [2]).
- P0: VE engine — 3-branch routing by `air_metering_strategy` (DUAL_MAF_MAP_CROSSCHECK / MAP_ONLY_SPEED_DENSITY / MAF_ONLY); only dual yields classified validity (HLD §4).
- P0: O2 normaliser — 3-branch normalisation (narrowband 3-zone voltage→lambda, wideband passthrough, wideband NB-sim) producing unified `normalized_obd_lambda` ∈ [0.7, 1.3] (HLD §5).
- P0: O2 failure mode classification — 4-value taxonomy: NO_FAULT, STUCK_LEAN, STUCK_RICH, WIDEBAND_OFFSET_CANDIDATE (HLD §5; pruned SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT per ARCH-2).
- P0: Fuel system status tracking — CL/OL/OL_DRIVE/OL_FAULT, mirrored from DTC_VOCABULARY §8 (T-OBDV2-6).
- P0: Trim vector aggregation — bank1 and bank2 totals + per-bank delta.
- P0: Trim analytics gate — 8-condition priority gate (ENGINE_COLD → OPEN_LOOP → O2_FAULT_ACTIVE → CKP_CMP_FAULT_ACTIVE → CODES_RECENTLY_CLEARED → WOT_ACTIVE → DFCO_ACTIVE → SEMANTIC_ERROR), HLD §6.
- P0: Guarded emitters — `lambda_perception_delta` (wideband + 0x44 commanded), `w_theo` / `sensor_error_delta` (DUAL strategy + two-point accumulator); emitted only when not frozen and guard satisfied (HLD §3).
- P0: `OBDLivePayload` Pydantic output model (31 canonical fields per DLD §4).

### Technology

- Python ≥ 3.11. Pydantic ≥ 2.5. PyYAML ≥ 6.0. No cross-lab imports.
- Package: `obdlab`, standalone `pyproject.toml`.
- Entry point: `obdlab.SensorSignalTranslator.translate(raw_user_inputs, dna_view, accumulator?) → OBDLivePayload`.
- Optional `LinearityAccumulator` parameter enables two-point MAF linearity monitoring across calls.
- Exceptions under `obdlab.core.exceptions.ObdLabError` hierarchy (no bare `ValueError`/`AssertionError`).

### Payload fields (31 canonical)

| # | Field | Type | Bounds | wiki citation |
|---|-------|------|--------|---------------|
| 1 | `engine_warmed` | `bool` | — | §5 |
| 2 | `rpm_state_bucket` | `RpmStateBucket` | — | §5 / SEMANTIC_CONTRACT §8 |
| 3 | `engine_rpm` | `int` | [0, 8000] | §3.1 |
| 4 | `coolant_temp_c` | `float` | [−40, 140] | §3.1 |
| 5 | `calculated_engine_load_pct` | `float` | [0, 100] | §3.1 |
| 6 | `mass_airflow_gps` | `float\|None` | [0, 655.35] | §3.1 — null when MAP_ONLY |
| 7 | `manifold_vacuum_kpa` | `float\|None` | [0, 255] | §3.1 — null when MAF_ONLY |
| 8 | `shrtft1` | `float` | [−127, 127] | T-W-6 — widened from OBD-nominal |
| 9 | `longft1` | `float` | [−127, 127] | T-W-6 |
| 10 | `shrtft2` | `float\|None` | [−127, 127] | T-W-6 — null when single-bank |
| 11 | `longft2` | `float\|None` | [−127, 127] | T-W-6 — null when single-bank |
| 12 | `total_trim_correction_delta` | `float` | — | §5 / §12 — shrtft1+longft1 |
| 13 | `total_trim_correction_delta_b2` | `float\|None` | — | §5 / §12 — null when single-bank |
| 14 | `per_bank_trim_delta` | `float\|None` | — | §5 / §12.1 — B1−B2 signed delta |
| 15 | `normalized_obd_lambda` | `float` | [0.7, 1.3] | §5 / §11 |
| 16 | `lambda_perception_delta` | `float\|None` | — | §5 — null when not wideband/0x44 |
| 17 | `ve_pct` | `float` | [0.0, 200.0] | §6.4 — 200 ceiling for thermal-shock steam overshoot |
| 18 | `ve_validity` | `VEValidity` | — | §5 / §10 |
| 19 | `trim_analytics_gate` | `TrimAnalyticsGate` | — | §5 / §9 |
| 20 | `maf_status` | `NodeMAFStatus` | — | §5 / §10 |
| 21 | `map_status` | `NodeMAPStatus` | — | §5 / §10 |
| 22 | `o2_failure_mode` | `O2FailureMode` | — | §5 / §6.7 |
| 23 | `fuel_system_status` | `FuelSystemStatus` | — | §5 — CL/OL/OL_DRIVE/OL_FAULT |
| 24 | `freeze_frame_pids` | `dict` | — | §5 — ferried through from DTCLab |
| 25 | `intake_air_temp_c` | `float` | [−40, 140] | §3.1 / §5 |
| 26 | `throttle_pos_pct` | `float` | [0, 100] | §3.1 / §5 |
| 27 | `control_module_voltage_v` | `float` | [0, 18] | §3.1 / §5 — PCM pin supply |
| 28 | `per_cylinder_misfire_counts` | `dict[int,int]\|None` | — | research/chunks/fuel-trim/17 |
| 29 | `ltft_cell_vector` | `dict[int,float]\|None` | — | research/chunks/fuel-trim/13 |
| 30 | `w_theo` | `float\|None` | — | research/chunks/pids-protocol/05 — speed-density theoretical airflow (g/s) |
| 31 | `sensor_error_delta` | `float\|None` | — | research/chunks/pids-protocol/05 — two-point non-linearity delta (%) |

### DNA view fields (7)

| # | Field | Type | wiki citation |
|---|-------|------|---------------|
| 1 | `engine_displacement_liters` | `float\|None` | KG_Wiki §10 — for VE formula |
| 2 | `rated_rpm` | `int\|None` | KG_Wiki §3.1 — DNA-relative RPM ceiling |
| 3 | `stress_idle_rpm_target` | `int\|None` | OBD_VOCABULARY §3.2 — per-vehicle stress RPM |
| 4 | `air_metering_strategy` | `AirMeteringStrategy` | KG_Wiki §6.2 — VE routing switch |
| 5 | `upstream_o2_type` | `O2SensorType` | KG_Wiki §11 — O2 normalisation switch |
| 6 | `induction_type` | `InductionType` | KG_Wiki §4 — NA/turbo |
| 7 | `confidence` | `VinConfidence` | NewArchProposal §3.3 — three-branch gate |

### Vocabulary — 8 StrEnums (DLD §2)

| Enum | Members |
|------|---------|
| `RpmStateBucket` | STABILIZED_IDLE, REGULATORY_HIGH_IDLE, STRESS_IDLE, COLD_OPEN_LOOP_INVALID |
| `O2NormalizationMode` | NARROWBAND_VOLTAGE_TO_LAMBDA, WIDEBAND_PASSTHROUGH, WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA, O2_CHANNEL_FAULT |
| `VEValidity` | VALID, FAULT_VE_IDLE_COLLAPSE, FAULT_MAF_CONTAMINATION, FAULT_VE_SENSOR_SKEW, UNKNOWN |
| `TrimAnalyticsGate` | VALID, ENGINE_COLD, OPEN_LOOP, O2_FAULT_ACTIVE, CKP_CMP_FAULT_ACTIVE, CODES_RECENTLY_CLEARED, WOT_ACTIVE, DFCO_ACTIVE, SEMANTIC_ERROR |
| `NodeMAFStatus` | REAL_SENSOR_FEED, VIRTUAL_EMULATION |
| `NodeMAPStatus` | REAL_SENSOR_FEED, BACK_CALCULATED |
| `FuelSystemStatus` | CL, OL, OL_DRIVE, OL_FAULT (mirrored from DTC_VOCABULARY §8) |
| `O2FailureMode` | NO_FAULT, STUCK_LEAN, STUCK_RICH, WIDEBAND_OFFSET_CANDIDATE |

### Physical sensor bounds — 12 fields (LLD §2)

| Field | min | max | unit | Note |
|-------|-----|-----|------|------|
| `engine_rpm` | 0 | 8000 | RPM | wiki: §3.1 |
| `coolant_temp_c` | −40.0 | 140.0 | °C | wiki: §3.1 |
| `calculated_engine_load_pct` | 0.0 | 100.0 | % | wiki: §3.1 |
| `mass_airflow_gps` | 0.0 | 655.35 | g/s | wiki: §3.1 |
| `manifold_vacuum_kpa` | 0.0 | 255.0 | kPa | wiki: §3.1 |
| `shrtft1` | −127.0 | 127.0 | % | widened from OBD-nominal (T-W-6) |
| `longft1` | −127.0 | 127.0 | % | widened (T-W-6) |
| `shrtft2` | −127.0 | 127.0 | % | only validated when `number_of_banks == 2` |
| `longft2` | −127.0 | 127.0 | % | only validated when `number_of_banks == 2` |
| `intake_air_temp_c` | −40.0 | 140.0 | °C | wiki: §3.1 |
| `throttle_pos_pct` | 0.0 | 100.0 | % | wiki: §3.1 |
| `control_module_voltage_v` | 0.0 | 18.0 | V | wiki: §3.1 / ecu-diagnosis/09 |

**Rail-value rationale (T-W-6):** trim bounds were widened from OBD-nominal [−100, 99.22] to the OBD rail ±127 because a railed trim is itself a *sensor-fault signal* consumed by COMLab trim-evidence scoring; rejecting it as out-of-bounds would discard that signal.

### Physical constants (LLD §1)

| Constant | Value | Unit | wiki citation |
|----------|-------|------|---------------|
| MM_AIR | 28.97 | g/mol | §10.1 — molar mass dry air |
| R_GAS | 8.314 | J/(mol·K) | §10.1 — universal gas constant |
| K_OFFSET | 273.15 | — | §10.1 — °C → K offset |
| R (MAF linearity) | 0.287 | kJ/(kg·K) | research/chunks/pids-protocol/05 — specific gas constant air |
| CONSTANT_120 | 120.0 | — | research/chunks/pids-protocol/05 — 4-stroke/60s factor |

### Assumptions

| Assumption | Validation |
|-----------|-----------|
| `physical_sensor_bounds.json` is the single source of truth for PID bounds (12 fields) | `test_sensor_bounds.py` drift guard vs `OBDLab_KG_Wiki.md §3.1` |
| `HIGH_IDLE_LOAD` enum value is permanently retired (superseded by `REGULATORY_HIGH_IDLE`/`STRESS_IDLE`) | `test_vocabulary.py` codebase scan asserts zero occurrences |
| `O2_CHANNEL_FAULT` is a formal 4th member of `O2NormalizationMode` (sentinel for out-of-range O2 input) | Guarded by `test_vocabulary.py` enum-vs-wiki drift check |
| `O2FailureMode` carries exactly 4 values (NO_FAULT/STUCK_LEAN/STUCK_RICH/WIDEBAND_OFFSET_CANDIDATE); no pruned v1 member (SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT) survives | `test_vocabulary.py` codebase scan |
| Cold engine defaults (`lambda=1.0`, `trim_delta=0.0`) are COMLab-acceptable | COMLab must treat `analytics_frozen=True` as a signal to skip trim analysis |
| OBD-rail trim bounds (±127) capture sensor-fault signalling that narrower nominal bounds would discard | COMLab trim-evidence scoring consumes railed-trim signal |
| `WIDEBAND_OFFSET_CANDIDATE` is a proposal flag, never a verdict | COMLab `T-COMV2-O2OFFSET-1` (Stage 4) is the named consumer |

---

## Section 8 — Release

### v2 Scope

All P0 features above. The v2 rework (T-OBDV2-0 through T-OBDV2-11) revived OBDLab as a pure emitter, expanded the payload from 21 to 31 fields, replaced the legacy O2 failure taxonomy with a 4-value consumer-backed classification, added FuelSystemStatus tracking, widened trim bounds to the OBD rail, removed Physics Gate 3, added MAF linearity monitoring, and established the guarded-emitters pattern for forward-registered COMLab consumers (HLD §7).

### Explicitly Deferred (v3 / COMLab Stage 4)

- `dna_view=None` fallback displacement for VE (currently returns `VEValidity.UNKNOWN`, `ve_pct=0.0`).
- Descriptive names for regression fixtures (currently `case_01`–`case_06`).
- Brittle relative-path assumption in `test_dna_view.py` (`../COMLab/docs/wiki/`).
- PID 0x44 `commanded_equivalence_ratio` λ-range bound (currently numeric check only; FU-ECU-2).

### Success Criteria

1. KR1–KR6 all pass in CI.
2. All regression fixtures produce structurally valid `OBDLivePayload` (31 fields).
3. `HIGH_IDLE_LOAD` scan finds zero occurrences in `obdlab/`.
4. `O2FailureMode` scan finds zero occurrences of SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT in `obdlab/`.
5. No cross-lab Python imports (import-isolation audit).
6. `physical_sensor_bounds.json` 12-field drift guard passes.
7. Every payload field has a named consumer (live or forward-registered S4) per HLD §7.
