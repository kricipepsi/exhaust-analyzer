---
node_type: "dld"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "detailed-design"
implements:
  - "labs/obdlab/obdlab/core/analytics_preconditions.py"
  - "labs/obdlab/obdlab/core/maf_linearity.py"
  - "labs/obdlab/obdlab/core/o2_normalizer.py"
  - "labs/obdlab/obdlab/core/pid_ingestion_validator.py"
  - "labs/obdlab/obdlab/core/semantic_consistency_checker.py"
  - "labs/obdlab/obdlab/core/sensor_signal_translator.py"
  - "labs/obdlab/obdlab/core/state_bucketing.py"
  - "labs/obdlab/obdlab/core/trim_vector_aggregator.py"
  - "labs/obdlab/obdlab/core/ve_engine.py"
  - "labs/obdlab/obdlab/schemas/dna_view.py"
  - "labs/obdlab/obdlab/schemas/payload.py"
  - "labs/obdlab/obdlab/schemas/vocabulary.py"
consumers:
  - "comlab: fault_atlas fusion (perception channel)"
drift_guards:
  - "labs/obdlab/tests/unit/test_analytics_preconditions.py"
  - "labs/obdlab/tests/unit/test_maf_linearity.py"
  - "labs/obdlab/tests/unit/test_o2_normalizer.py"
  - "labs/obdlab/tests/unit/test_pid_ingestion_validator.py"
  - "labs/obdlab/tests/unit/test_semantic_consistency_checker.py"
  - "labs/obdlab/tests/unit/test_sensor_signal_translator.py"
  - "labs/obdlab/tests/unit/test_trim_vector_aggregator.py"
  - "labs/obdlab/tests/unit/test_ve_engine.py"
  - "labs/obdlab/tests/unit/test_dna_view.py"
  - "labs/obdlab/tests/unit/test_payload.py"
  - "labs/obdlab/tests/unit/test_vocabulary.py"
  - "labs/obdlab/tests/integration/test_pipeline_smoke.py"
tags: [obdlab, finished, dld]
source: "labs/obdlab/docs/DLD_OBDLab.md"
---
# DLD — OBDLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_OBDLab v1.0
**HLD Reference:** HLD_OBDLab v2.0
**Version:** 2.0
**Date:** 2026-06-10
**Supersedes:** DLD_OBDLab v1.0 (2026-05-22) — 21-field payload, 8 vocabulary enums incl. `VERoutingMode`, 10-field DNA view with `emissions`/`resolved_horizon`/`cylinder_count`, exceptions on stdlib bases.

> Grounded in the live `obdlab/` package as of 2026-06-10. Field/enum tables are
> the source of truth surface; constants and formulas live in `LLD_OBDLab.md`.

---

## 1. Module Map

```
obdlab/
├── __init__.py                       ← public surface: SensorSignalTranslator, OBDLivePayload, LinearityAccumulator
├── core/
│   ├── sensor_signal_translator.py   ← public entry point (orchestrator) + LinearityAccumulator
│   ├── pid_ingestion_validator.py
│   ├── state_bucketing.py
│   ├── semantic_consistency_checker.py
│   ├── ve_engine.py
│   ├── o2_normalizer.py
│   ├── trim_vector_aggregator.py
│   ├── maf_linearity.py              ← w_theo / sensor_error_delta helpers (T-OBDV2-10)
│   ├── analytics_preconditions.py
│   └── exceptions.py
├── schemas/
│   ├── dna_view.py
│   ├── payload.py
│   └── vocabulary.py
└── config/
    ├── physical_sensor_bounds.json
    └── obd_translation_rules.yaml
```

`core/__init__.py` and `schemas/__init__.py` each export an explicit `__all__`
(added in T-KG-OBD-2-PREP for code-map legibility). There is **no** `config/`
Python package — config is data only.

---

## 2. `schemas/vocabulary.py` — 8 StrEnums

All values are wire-format strings consumed across lab boundaries
(`SEMANTIC_CONTRACT.md §4.4`). Renames are breaking changes. Drift-guarded by
`test_vocabulary.py`.

> Doc-bug note: the live module docstring still reads "7 StrEnums" — stale since
> `FuelSystemStatus` was added (T-OBDV2-6) bringing the count to 8. Logged as a
> docstring follow-up (FU-OBD-DOC-3); not fixed here (architect does not edit code).

| Enum | Members |
|------|---------|
| `RpmStateBucket` | `STABILIZED_IDLE`, `REGULATORY_HIGH_IDLE`, `STRESS_IDLE`, `COLD_OPEN_LOOP_INVALID` |
| `O2NormalizationMode` | `NARROWBAND_VOLTAGE_TO_LAMBDA`, `WIDEBAND_PASSTHROUGH`, `WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA`, `O2_CHANNEL_FAULT` |
| `VEValidity` | `VALID`, `FAULT_VE_IDLE_COLLAPSE`, `FAULT_MAF_CONTAMINATION`, `FAULT_VE_SENSOR_SKEW`, `UNKNOWN` |
| `TrimAnalyticsGate` | `VALID`, `ENGINE_COLD`, `OPEN_LOOP`, `O2_FAULT_ACTIVE`, `CKP_CMP_FAULT_ACTIVE`, `CODES_RECENTLY_CLEARED`, `WOT_ACTIVE`, `DFCO_ACTIVE`, `SEMANTIC_ERROR` |
| `NodeMAFStatus` | `REAL_SENSOR_FEED`, `VIRTUAL_EMULATION` |
| `NodeMAPStatus` | `REAL_SENSOR_FEED`, `BACK_CALCULATED` |
| `FuelSystemStatus` | `CL`, `OL`, `OL_DRIVE`, `OL_FAULT` (+ `from_wire()` coercion) |
| `O2FailureMode` | `NO_FAULT`, `STUCK_LEAN`, `STUCK_RICH`, `WIDEBAND_OFFSET_CANDIDATE` |

**Changes from v1.0:**
- `VERoutingMode` **removed** — it duplicated `AirMeteringStrategy` (ARCH-2).
- `O2FailureMode` pruned 7 → 4: `SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`,
  `HEATER_FAULT` removed (no consumer); `WIDEBAND_OFFSET_CANDIDATE` added
  (T-OBDV2-4 / EP-OBD-17).
- `FuelSystemStatus` **added** (T-OBDV2-6), mirrored from DTC_VOCABULARY §8 — no
  cross-lab import. `from_wire()` coerces legacy strings (`Closed_Loop`,
  `Open_Loop_Cold`, `Open_Loop_Fault`, `Open_Loop_Driving`) and short codes.

`HIGH_IDLE_LOAD` is forbidden throughout `obdlab/` (CI scan in
`test_vocabulary.py`); superseded by `REGULATORY_HIGH_IDLE` / `STRESS_IDLE`.

---

## 3. `schemas/dna_view.py`

### Enums (4)

| Enum | Members | Source |
|------|---------|--------|
| `AirMeteringStrategy` | `DUAL_MAF_MAP_CROSSCHECK`, `MAP_ONLY_SPEED_DENSITY`, `MAF_ONLY` | `OBD_VOCABULARY.md §4.2` |
| `O2SensorType` | `NARROWBAND_0_TO_1V`, `WIDEBAND_LINEAR`, `WIDEBAND_NB_SIM` | `OBD_VOCABULARY.md §4.3` |
| `InductionType` | `NATURALLY_ASPIRATED`, `TURBOCHARGED` | `SEMANTIC_CONTRACT.md §8` |
| `VinConfidence` | `HIGH`, `PARTIAL`, `NONE` | `SEMANTIC_CONTRACT.md §8` |

**Removed from v1.0:** `EuroEmissionCategory` and `ResolvedHorizon` enums, and
the `ObdEmissionsView` sub-model — all pruned (PURGE-2) for lack of a live
consumer.

### `ObdLabDnaView` (7 fields)

| Field | Type | Purpose |
|-------|------|---------|
| `engine_displacement_liters` | `float \| None` | VE formula denominator |
| `rated_rpm` | `int \| None` | DNA-RPM gate ceiling (HIGH confidence) |
| `stress_idle_rpm_target` | `int \| None` | `STRESS_IDLE` `APPROXIMATELY` bucketing |
| `air_metering_strategy` | `AirMeteringStrategy` | VE routing branch |
| `upstream_o2_type` | `O2SensorType` | O2 normalisation path |
| `induction_type` | `InductionType` | `FAULT_VE_SENSOR_SKEW` classifier |
| `confidence` | `VinConfidence` | three-branch DNA-RPM gate |

`None` at the call boundary is permitted and treated as `confidence == NONE`
(static bounds only, `DUAL_MAF_MAP_CROSSCHECK` + `NARROWBAND_0_TO_1V` defaults).
**Removed from v1.0:** `cylinder_count` (ARCH-2), `emissions` + `resolved_horizon`
(PURGE-2).

---

## 4. `schemas/payload.py` — `OBDLivePayload` (31 fields)

Pydantic `BaseModel`. The JSON contract surface emitted by
`SensorSignalTranslator` and consumed by COMLab's `lab_pipeline_aggregator`
(mirror: `OBDLiveDataPayload`).

| # | Field | Type | Constraint | Consumer (signal/noise) |
|---|-------|------|-----------|-------------------------|
| 1 | `engine_warmed` | `bool` | | COMLab analytics-applicability context |
| 2 | `rpm_state_bucket` | `RpmStateBucket` | | Fault routing context |
| 3 | `engine_rpm` | `int` | `[0, 8000]` | Context |
| 4 | `coolant_temp_c` | `float` | `[-40, 140]` | Context |
| 5 | `calculated_engine_load_pct` | `float` | `[0, 100]` | Context |
| 6 | `mass_airflow_gps` | `float \| None` | `[0, 655.35]` | VE / MAF-linearity |
| 7 | `manifold_vacuum_kpa` | `float \| None` | `[0, 255]` | VE / MAF-linearity |
| 8 | `shrtft1` | `float` | `[-127, 127]` | Trim analytics |
| 9 | `longft1` | `float` | `[-127, 127]` | Trim analytics |
| 10 | `shrtft2` | `float \| None` | `[-127, 127]` | Trim analytics bank 2 |
| 11 | `longft2` | `float \| None` | `[-127, 127]` | Trim analytics bank 2 |
| 12 | `total_trim_correction_delta` | `float` | `= shrtft1 + longft1` | delta_Healing |
| 13 | `total_trim_correction_delta_b2` | `float \| None` | `= shrtft2 + longft2` | delta_Healing bank 2 |
| 14 | `per_bank_trim_delta` | `float \| None` | `= B1 − B2` | `T-COMV2-BANK-FUSE-1` (S4) |
| 15 | `normalized_obd_lambda` | `float` | `[0.7, 1.3]` | Lambda delta vs GASLab |
| 16 | `lambda_perception_delta` | `float \| None` | `= λ − commanded_λ` | `T-COMV2-ECU-FUSE-1` (S4) |
| 17 | `ve_pct` | `float` | `[0.0, 200.0]` | `T-COMV2-VE-GATE-1` (S4) |
| 18 | `ve_validity` | `VEValidity` | | `T-COMV2-VE-GATE-1` (S4) |
| 19 | `trim_analytics_gate` | `TrimAnalyticsGate` | | COMLab confidence path |
| 20 | `maf_status` | `NodeMAFStatus` | | COMLab evidence weighting |
| 21 | `map_status` | `NodeMAPStatus` | | COMLab evidence weighting |
| 22 | `o2_failure_mode` | `O2FailureMode` | | `T-COMV2-O2OFFSET-1` (S4) |
| 23 | `fuel_system_status` | `FuelSystemStatus` | | live precond/semantic; `T-COMV2-FUELSYS-GATE-1` |
| 24 | `freeze_frame_pids` | `dict` | default `{}` | ferried from DTCLab |
| 25 | `intake_air_temp_c` | `float` | `[-40, 140]` | live in `ve_engine`; `T-COMV2-ECU-HW-1` |
| 26 | `throttle_pos_pct` | `float` | `[0, 100]` | `T-COMV2-ECU-HW-1` (S4) |
| 27 | `control_module_voltage_v` | `float` | `[0, 18]`, default `14.0` | `T-COMV2-VPWR-GATE-1` (S4) |
| 28 | `per_cylinder_misfire_counts` | `dict[int, int] \| None` | cyl ≥ 1, count ≥ 0 | `T-COMV2-MISFIRE-LOC-1` (S4) |
| 29 | `ltft_cell_vector` | `dict[int, float] \| None` | cell ≥ 0, `[-127, 127]` | `T-COMV2-LTFT-CELL-1` (S4) |
| 30 | `w_theo` | `float \| None` | g/s | `T-COMV2-MAF-LIN-1` (S4) |
| 31 | `sensor_error_delta` | `float \| None` | % | `T-COMV2-MAF-LIN-1` (S4) |

> **Removed from v1.0:** `o2_channel_fault` (the fault signal is now carried by
> `o2_failure_mode` + `O2NormalizationMode.O2_CHANNEL_FAULT`). Fields 14, 16–18,
> 22, 25–31 are post-revive additions (T-OBDV2-* / FIX-*).

---

## 5. `core/exceptions.py`

```python
class ObdLabError(Exception): ...                       # unified root (FIX-5)
class PIDValidationError(ObdLabError): ...
class SemanticConsistencyError(ObdLabError): ...
```

**Changed from v1.0:** the hierarchy was reparented from stdlib bases
(`ValueError` / `AssertionError`) to a single `ObdLabError` root so COMLab's
fusion error-handling path can catch the whole family with one `except`.

---

## 6. `core/pid_ingestion_validator.py` — `PIDIngestionValidator`

Constructor loads `config["bounds"]` from `physical_sensor_bounds.json`.

`validate_and_convert(raw_user_inputs, dna_view) → dict` runs, in order:

```
1. _apply_unit_conversions   _f→_c, _psi→_kpa, _inhg→_kpa, _lbmin→_gps
                              canonical key wins (alternate dropped if canonical present)
2. _validate_bounds          12 fields; bank-2 fields only when number_of_banks==2;
                              non-numeric → PIDValidationError
3. _check_dna_rpm            HIGH: engine_rpm > rated_rpm×1.05 → error;
                              PARTIAL: log + fallthrough; NONE/None: skip
4. _enforce_bank2_contract   number_of_banks==1 AND (shrtft2 or longft2) not None → error
5. _validate_and_map_fuel_system_status  map to FuelSystemStatus; default CL when absent
6. _validate_per_cylinder_misfire_counts dict[int≥1, int≥0] or None
7. _validate_ltft_cell_vector            dict[int≥0, float∈[-127,127]] or None
```

---

## 7. `core/state_bucketing.py`

`compute_bucket(sanitized_pids, dna_view) → RpmStateBucket`. Rules loaded once
from `obd_translation_rules.yaml`. Priority rules (lower number = higher
priority) evaluated first, then document order, then fallback `STABILIZED_IDLE`.
Operators: `LESS_THAN`, `BETWEEN`, `APPROXIMATELY` (`tolerance_pct`, default 10).
`stress_idle_rpm_target` is resolved from `dna_view` for the `APPROXIMATELY`
`STRESS_IDLE` rule. Called **before** the semantic checker (F-O7).

---

## 8. `core/semantic_consistency_checker.py` — `SemanticConsistencyChecker`

`evaluate(sanitized_pids, dna_view) → dict` returns
`{rpm_state_bucket_override, engine_warmed, trim_analytics_suspect, gates_passed}`.

| Gate | Condition | Effect |
|------|-----------|--------|
| Thermal | `ECT < 75` | override bucket → `COLD_OPEN_LOOP_INVALID`; `engine_warmed=False` |
| Physics_Gate_1 | `VSS > 10 AND RPM < 400` | `SemanticConsistencyError` |
| Physics_Gate_2 | `ECT ≥ 80 AND fuel_status == OL` | `SemanticConsistencyError` |
| Physics_Gate_4 | trim outside `[-127, 127]` | `SemanticConsistencyError` |
| Closed-loop | `ECT ≥ 75 AND fuel_status != CL` | `trim_analytics_suspect=True` (non-blocking) |

`gates_passed` lists the 3 physics gates that passed; the orchestrator derives
`semantic_gates_passed = (len(gates_passed) == 3)`. **Physics_Gate_3 (the NA VE
ceiling) was removed (FIX-1 Option B)** — its intent is now carried by
`VEValidity.FAULT_VE_SENSOR_SKEW` in the VE engine.

---

## 9. `core/ve_engine.py` — `VEEngine`

`compute_ve(pids, bucket, dna_view) → (ve_pct|None, NodeMAFStatus, NodeMAPStatus, VEValidity)`.
Branches on `air_metering_strategy` (see HLD §4). `_classify_validity` applies
three fault triggers (thresholds in LLD §7); single-sensor branches return
`UNKNOWN` by construction. `_expected_ve` looks up per-(bucket, strategy)
emulation targets. Constants `MM_AIR`, `R_GAS`, `K_OFFSET` per LLD §1.

---

## 10. `core/o2_normalizer.py` — `O2Normalizer`

`normalize(pids, dna_view) → (lambda, O2NormalizationMode, O2FailureMode)`.
Branches on `upstream_o2_type` (see HLD §5). The wideband branch additionally
flags `WIDEBAND_OFFSET_CANDIDATE` when warm + closed-loop + not WOT + not DFCO
and `|ratio − 1.0| > 0.05`. Reuses `ECT_WARM_THRESHOLD` and
`WOT_THROTTLE_THRESHOLD` imported from `analytics_preconditions` (single source).

---

## 11. `core/trim_vector_aggregator.py` — `TrimVectorAggregator`

`aggregate(sanitized_pids) → (bank1_tft, bank2_tft|None, per_bank_trim_delta|None)`.

```
bank1 = shrtft1 + longft1                    (always; None → PIDValidationError)
if number_of_banks != 2: return (bank1, None, None)
shrtft2/longft2 None when banks==2 → PIDValidationError
bank2 = shrtft2 + longft2
per_bank_trim_delta = bank1 − bank2
```

Bank-2 contract and `per_bank_trim_delta` are the bank-asymmetry channel
(T-OBDV2-BANK-ASYM-1).

---

## 12. `core/maf_linearity.py`

Pure helpers (no class):
- `calculate_w_theo(eta_v, displacement, map_kpa, rpm, iat_c) → float` —
  theoretical airflow `(η·V·P·RPM)/(120·R·T_K)`.
- `calculate_sensor_error_delta(maf_stress, w_theo_stress, maf_idle, w_theo_idle) → float`
  — two-point non-linearity delta in %.

Driven from the orchestrator under the `DUAL_MAF_MAP_CROSSCHECK` two-point guard
via `LinearityAccumulator` (captures idle + stress bands across calls). Both
emit only once both bands are present (T-OBDV2-10 / FIX-3 — accumulator threads
prior band explicitly, no instance state).

---

## 13. `core/analytics_preconditions.py` — `AnalyticsPreconditions`

`evaluate(sanitized_pids, semantic_gates_passed) → TrimAnalyticsGate`. 8 gates,
priority order (HLD §6). Constants: `O2_FAULT_DTCS` (32 codes, P0130–P0161),
`CKP_CMP_FAULT_DTCS` ({P0335, P0340}), `ECT_WARM_THRESHOLD = 70`,
`WOT_THROTTLE_THRESHOLD = 90`. DTC checks are opaque set intersection — no regex.

---

## 14. `core/sensor_signal_translator.py` — `SensorSignalTranslator`

Public entry point `translate(raw_user_inputs, dna_view=None, accumulator=None)
→ OBDLivePayload`. Wires steps [1]–[7] (HLD §3), applies the thermal
freeze, computes guarded emitters (`lambda_perception_delta`, `w_theo`,
`sensor_error_delta`), and assembles the 31-field payload. `LinearityAccumulator`
is a small holder for the two idle/stress bands used by MAF linearity.

---

## 15. Test Coverage (current)

| Area | Files |
|------|-------|
| Unit — per module | `test_payload`, `test_dna_view`, `test_vocabulary`, `test_sensor_bounds`, `test_pid_ingestion_validator`, `test_semantic_consistency_checker`, `test_state`*, `test_ve_engine`, `test_o2_normalizer`, `test_trim_vector_aggregator`, `test_maf_linearity`, `test_analytics_preconditions`, `test_sensor_signal_translator` |
| Unit — emitter channels | `test_ecu_perception_delta`, `test_bank_asym` |
| Integration | `test_pipeline_smoke` |
| PID-logset gate | `test_pid_logset_wiring_gate` (un-quarantine proof) |
| Regression | `test_obdlab_regression` (JSON fixtures) |
| Generative | `test_boundary`, `test_combinatorial`, `test_fuzz`, `test_noise`, `test_overlap` |

Latest inner loop (T-KG-OBD-2-PREP): ruff + pyright clean, `pytest` 384 passed /
6 skipped.
