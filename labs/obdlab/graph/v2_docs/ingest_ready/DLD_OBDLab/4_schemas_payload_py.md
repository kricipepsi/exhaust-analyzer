> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 4 schemas/payload.py — OBDLivePayload (31 fields) · Parent document: DLD_OBDLab.md · Boundary contract: SEMANTIC_CONTRACT §4.4

## 4. `schemas/payload.py` — `OBDLivePayload` (31 fields)

Pydantic `BaseModel`. The JSON contract surface emitted by
`SensorSignalTranslator` and consumed by COMLab's `lab_pipeline_aggregator`
(mirror: `OBDLiveDataPayload`).

### Entity: OBDLivePayload fields (31 canonical)

- **1. engine_warmed** — `bool` · Constraint: — · **Consumed by:** COMLab analytics-applicability context
- **2. rpm_state_bucket** — `RpmStateBucket` · Constraint: — · **Consumed by:** Fault routing context
- **3. engine_rpm** — `int` · Constraint: `[0, 8000]` · **Consumed by:** Context
- **4. coolant_temp_c** — `float` · Constraint: `[-40, 140]` · **Consumed by:** Context
- **5. calculated_engine_load_pct** — `float` · Constraint: `[0, 100]` · **Consumed by:** Context
- **6. mass_airflow_gps** — `float | None` · Constraint: `[0, 655.35]` · **Consumed by:** VE / MAF-linearity
- **7. manifold_vacuum_kpa** — `float | None` · Constraint: `[0, 255]` · **Consumed by:** VE / MAF-linearity
- **8. shrtft1** — `float` · Constraint: `[-127, 127]` · **Consumed by:** Trim analytics
- **9. longft1** — `float` · Constraint: `[-127, 127]` · **Consumed by:** Trim analytics
- **10. shrtft2** — `float | None` · Constraint: `[-127, 127]` · **Consumed by:** Trim analytics bank 2
- **11. longft2** — `float | None` · Constraint: `[-127, 127]` · **Consumed by:** Trim analytics bank 2
- **12. total_trim_correction_delta** — `float` · Constraint: `= shrtft1 + longft1` · **Consumed by:** delta_Healing
- **13. total_trim_correction_delta_b2** — `float | None` · Constraint: `= shrtft2 + longft2` · **Consumed by:** delta_Healing bank 2
- **14. per_bank_trim_delta** — `float | None` · Constraint: `= B1 − B2` · **Consumed by:** `T-COMV2-BANK-FUSE-1` (S4)
- **15. normalized_obd_lambda** — `float` · Constraint: `[0.7, 1.3]` · **Consumed by:** Lambda delta vs GASLab
- **16. lambda_perception_delta** — `float | None` · Constraint: `= λ − commanded_λ` · **Consumed by:** `T-COMV2-ECU-FUSE-1` (S4)
- **17. ve_pct** — `float` · Constraint: `[0.0, 200.0]` · **Consumed by:** `T-COMV2-VE-GATE-1` (S4)
- **18. ve_validity** — `VEValidity` · Constraint: — · **Consumed by:** `T-COMV2-VE-GATE-1` (S4)
- **19. trim_analytics_gate** — `TrimAnalyticsGate` · Constraint: — · **Consumed by:** COMLab confidence path
- **20. maf_status** — `NodeMAFStatus` · Constraint: — · **Consumed by:** COMLab evidence weighting
- **21. map_status** — `NodeMAPStatus` · Constraint: — · **Consumed by:** COMLab evidence weighting
- **22. o2_failure_mode** — `O2FailureMode` · Constraint: — · **Consumed by:** `T-COMV2-O2OFFSET-1` (S4)
- **23. fuel_system_status** — `FuelSystemStatus` · Constraint: — · **Consumed by:** live precond/semantic; `T-COMV2-FUELSYS-GATE-1`
- **24. freeze_frame_pids** — `dict` · Constraint: default `{}` · **Consumed by:** ferried from DTCLab
- **25. intake_air_temp_c** — `float` · Constraint: `[-40, 140]` · **Consumed by:** live in `ve_engine`; `T-COMV2-ECU-HW-1`
- **26. throttle_pos_pct** — `float` · Constraint: `[0, 100]` · **Consumed by:** `T-COMV2-ECU-HW-1` (S4)
- **27. control_module_voltage_v** — `float` · Constraint: `[0, 18]`, default `14.0` · **Consumed by:** `T-COMV2-VPWR-GATE-1` (S4)
- **28. per_cylinder_misfire_counts** — `dict[int, int] | None` · Constraint: cyl ≥ 1, count ≥ 0 · **Consumed by:** `T-COMV2-MISFIRE-LOC-1` (S4)
- **29. ltft_cell_vector** — `dict[int, float] | None` · Constraint: cell ≥ 0, `[-127, 127]` · **Consumed by:** `T-COMV2-LTFT-CELL-1` (S4)
- **30. w_theo** — `float | None` · Constraint: g/s · **Consumed by:** `T-COMV2-MAF-LIN-1` (S4)
- **31. sensor_error_delta** — `float | None` · Constraint: % · **Consumed by:** `T-COMV2-MAF-LIN-1` (S4)

> **Removed from v1.0:** `o2_channel_fault` (the fault signal is now carried by
> `o2_failure_mode` + `O2NormalizationMode.O2_CHANNEL_FAULT`). Fields 14, 16–18,
> 22, 25–31 are post-revive additions (T-OBDV2-* / FIX-*).

## Graph relations (explicit)

**OBDLivePayload v2** SUPERSEDES **OBDLivePayload v1.0** (21→31 fields; o2_channel_fault removed)
**SensorSignalTranslator.translate** DESCRIBES **OBDLivePayload** (emitter surface)
**COMLab lab_pipeline_aggregator** CONSUMES **OBDLivePayload** (JSON contract surface)
**OBDLivePayload** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.4**
**test_payload.py** VERIFIES **OBDLivePayload** (structural validity)
