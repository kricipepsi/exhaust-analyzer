> **Context:** OBDLab PRD v2.0 (2026-06-10) · Module: OBDLab · Section 7 Solution · Parent document: PRD_OBDLab.md

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

- **1. engine_warmed** — `bool` · Bounds: — · # wiki: §5
- **2. rpm_state_bucket** — `RpmStateBucket` · Bounds: — · # wiki: §5 / SEMANTIC_CONTRACT §8
- **3. engine_rpm** — `int` · Bounds: [0, 8000] · # wiki: §3.1
- **4. coolant_temp_c** — `float` · Bounds: [−40, 140] · # wiki: §3.1
- **5. calculated_engine_load_pct** — `float` · Bounds: [0, 100] · # wiki: §3.1
- **6. mass_airflow_gps** — `float|None` · Bounds: [0, 655.35] · # wiki: §3.1 — null when MAP_ONLY
- **7. manifold_vacuum_kpa** — `float|None` · Bounds: [0, 255] · # wiki: §3.1 — null when MAF_ONLY
- **8. shrtft1** — `float` · Bounds: [−127, 127] · # wiki: T-W-6 — widened from OBD-nominal
- **9. longft1** — `float` · Bounds: [−127, 127] · # wiki: T-W-6
- **10. shrtft2** — `float|None` · Bounds: [−127, 127] · # wiki: T-W-6 — null when single-bank
- **11. longft2** — `float|None` · Bounds: [−127, 127] · # wiki: T-W-6 — null when single-bank
- **12. total_trim_correction_delta** — `float` · Bounds: — · # wiki: §5 / §12 — shrtft1+longft1
- **13. total_trim_correction_delta_b2** — `float|None` · Bounds: — · # wiki: §5 / §12 — null when single-bank
- **14. per_bank_trim_delta** — `float|None` · Bounds: — · # wiki: §5 / §12.1 — B1−B2 signed delta
- **15. normalized_obd_lambda** — `float` · Bounds: [0.7, 1.3] · # wiki: §5 / §11
- **16. lambda_perception_delta** — `float|None` · Bounds: — · # wiki: §5 — null when not wideband/0x44
- **17. ve_pct** — `float` · Bounds: [0.0, 200.0] · # wiki: §6.4 — 200 ceiling for thermal-shock steam overshoot
- **18. ve_validity** — `VEValidity` · Bounds: — · # wiki: §5 / §10
- **19. trim_analytics_gate** — `TrimAnalyticsGate` · Bounds: — · # wiki: §5 / §9
- **20. maf_status** — `NodeMAFStatus` · Bounds: — · # wiki: §5 / §10
- **21. map_status** — `NodeMAPStatus` · Bounds: — · # wiki: §5 / §10
- **22. o2_failure_mode** — `O2FailureMode` · Bounds: — · # wiki: §5 / §6.7
- **23. fuel_system_status** — `FuelSystemStatus` · Bounds: — · # wiki: §5 — CL/OL/OL_DRIVE/OL_FAULT
- **24. freeze_frame_pids** — `dict` · Bounds: — · # wiki: §5 — ferried through from DTCLab
- **25. intake_air_temp_c** — `float` · Bounds: [−40, 140] · # wiki: §3.1 / §5
- **26. throttle_pos_pct** — `float` · Bounds: [0, 100] · # wiki: §3.1 / §5
- **27. control_module_voltage_v** — `float` · Bounds: [0, 18] · # wiki: §3.1 / §5 — PCM pin supply
- **28. per_cylinder_misfire_counts** — `dict[int,int]|None` · Bounds: — · # wiki: research/chunks/fuel-trim/17
- **29. ltft_cell_vector** — `dict[int,float]|None` · Bounds: — · # wiki: research/chunks/fuel-trim/13
- **30. w_theo** — `float|None` · Bounds: — · # wiki: research/chunks/pids-protocol/05 — speed-density theoretical airflow (g/s)
- **31. sensor_error_delta** — `float|None` · Bounds: — · # wiki: research/chunks/pids-protocol/05 — two-point non-linearity delta (%)

### DNA view fields (7)

- **1. engine_displacement_liters** — `float|None` · # wiki: KG_Wiki §10 — for VE formula
- **2. rated_rpm** — `int|None` · # wiki: KG_Wiki §3.1 — DNA-relative RPM ceiling
- **3. stress_idle_rpm_target** — `int|None` · # wiki: OBD_VOCABULARY §3.2 — per-vehicle stress RPM
- **4. air_metering_strategy** — `AirMeteringStrategy` · # wiki: KG_Wiki §6.2 — VE routing switch
- **5. upstream_o2_type** — `O2SensorType` · # wiki: KG_Wiki §11 — O2 normalisation switch
- **6. induction_type** — `InductionType` · # wiki: KG_Wiki §4 — NA/turbo
- **7. confidence** — `VinConfidence` · # wiki: NewArchProposal §3.3 — three-branch gate

### Vocabulary — 8 StrEnums (DLD §2)

- **RpmStateBucket:** STABILIZED_IDLE, REGULATORY_HIGH_IDLE, STRESS_IDLE, COLD_OPEN_LOOP_INVALID
- **O2NormalizationMode:** NARROWBAND_VOLTAGE_TO_LAMBDA, WIDEBAND_PASSTHROUGH, WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA, O2_CHANNEL_FAULT
- **VEValidity:** VALID, FAULT_VE_IDLE_COLLAPSE, FAULT_MAF_CONTAMINATION, FAULT_VE_SENSOR_SKEW, UNKNOWN
- **TrimAnalyticsGate:** VALID, ENGINE_COLD, OPEN_LOOP, O2_FAULT_ACTIVE, CKP_CMP_FAULT_ACTIVE, CODES_RECENTLY_CLEARED, WOT_ACTIVE, DFCO_ACTIVE, SEMANTIC_ERROR
- **NodeMAFStatus:** REAL_SENSOR_FEED, VIRTUAL_EMULATION
- **NodeMAPStatus:** REAL_SENSOR_FEED, BACK_CALCULATED
- **FuelSystemStatus:** CL, OL, OL_DRIVE, OL_FAULT (mirrored from DTC_VOCABULARY §8)
- **O2FailureMode:** NO_FAULT, STUCK_LEAN, STUCK_RICH, WIDEBAND_OFFSET_CANDIDATE

### Physical sensor bounds — 12 fields (LLD §2)

- **engine_rpm:** [0, 8000] RPM · **coolant_temp_c:** [−40.0, 140.0] °C · **calculated_engine_load_pct:** [0.0, 100.0] % · **mass_airflow_gps:** [0.0, 655.35] g/s · **manifold_vacuum_kpa:** [0.0, 255.0] kPa · **shrtft1:** [−127.0, 127.0] % (widened T-W-6) · **longft1:** [−127.0, 127.0] % (widened T-W-6) · **shrtft2:** [−127.0, 127.0] % (bank-2 only) · **longft2:** [−127.0, 127.0] % (bank-2 only) · **intake_air_temp_c:** [−40.0, 140.0] °C · **throttle_pos_pct:** [0.0, 100.0] % · **control_module_voltage_v:** [0.0, 18.0] V

**Rail-value rationale (T-W-6):** trim bounds widened from [−100, 99.22] to ±127 to preserve sensor-fault signal.

### Physical constants (LLD §1)

- **MM_AIR:** 28.97 g/mol · **R_GAS:** 8.314 J/(mol·K) · **K_OFFSET:** 273.15 — · **R (MAF linearity):** 0.287 kJ/(kg·K) · **CONSTANT_120:** 120.0 —

### Assumptions

- `physical_sensor_bounds.json` single source of truth for PID bounds (12 fields) → `test_sensor_bounds.py` drift guard
- `HIGH_IDLE_LOAD` permanently retired → `test_vocabulary.py` scan
- `O2_CHANNEL_FAULT` formal 4th member of `O2NormalizationMode` → `test_vocabulary.py` drift check
- `O2FailureMode` = 4 values exactly; no pruned v1 member survives → `test_vocabulary.py` scan
- Cold engine defaults (λ=1.0, trim_delta=0.0) COMLab-acceptable → COMLab must treat `analytics_frozen=True` as signal
- OBD-rail trim bounds (±127) capture sensor-fault signalling → COMLab trim-evidence scoring
- `WIDEBAND_OFFSET_CANDIDATE` is proposal flag, never verdict → COMLab `T-COMV2-O2OFFSET-1` (Stage 4)

## Graph relations (explicit)

**PRD §7** ENUMERATES **13 P0 features** (PID ingestion → OBDLivePayload)
**PRD §7** ENUMERATES **31 payload fields** (with bounds, types, wiki citations)
**PRD §7** ENUMERATES **7 DNA view fields** (with wiki citations)
**PRD §7** ENUMERATES **8 StrEnums** (vocabulary, DLD §2)
**PRD §7** ENUMERATES **12 sensor bounds** (LLD §2, T-W-6 rail rationale)
**PRD §7** ENUMERATES **5 physical constants** (LLD §1)
**PRD §7** ENUMERATES **7 assumptions** (with validations)
**test_sensor_bounds.py** VERIFIES **physical_sensor_bounds.json ↔ KG_Wiki.md §3.1** (assumption 1)
**test_vocabulary.py** VERIFIES **HIGH_IDLE_LOAD absent + O2FailureMode=4 values** (assumptions 2, 4)
**test_vocabulary.py** VERIFIES **O2_CHANNEL_FAULT as 4th O2NormalizationMode member** (assumption 3)
**COMLab T-COMV2-O2OFFSET-1** CONSUMES **WIDEBAND_OFFSET_CANDIDATE** (assumption 7, S4 forward-reg)
