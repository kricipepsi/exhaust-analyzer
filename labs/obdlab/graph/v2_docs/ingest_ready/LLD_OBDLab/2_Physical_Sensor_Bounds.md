> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 2 Physical Sensor Bounds · Parent document: LLD_OBDLab.md · Boundary contract: OBDLab_KG_Wiki.md §3.1

## 2. Physical Sensor Bounds (`config/physical_sensor_bounds.json`)

Source: `OBDLab_KG_Wiki.md §3.1`. **12 fields** (was 10 in v1.0 — `intake_air_temp_c`
and `throttle_pos_pct` added in T-OBDV2-7; `control_module_voltage_v` in
T-OBDV2-8). Adding a field requires a wiki update and a `test_sensor_bounds.py`
update.

### Entity: Physical sensor bounds (12 fields)

- **engine_rpm** — min: 0, max: 8000 RPM · Note: —
- **coolant_temp_c** — min: −40.0, max: 140.0 °C · Note: —
- **calculated_engine_load_pct** — min: 0.0, max: 100.0 % · Note: —
- **mass_airflow_gps** — min: 0.0, max: 655.35 g/s · Note: —
- **manifold_vacuum_kpa** — min: 0.0, max: 255.0 kPa · Note: —
- **shrtft1** — min: −127.0, max: 127.0 % · Note: widened from OBD-nominal [−100, 99.22] (T-W-6)
- **longft1** — min: −127.0, max: 127.0 % · Note: widened (T-W-6)
- **shrtft2** — min: −127.0, max: 127.0 % · Note: only validated when `number_of_banks == 2`
- **longft2** — min: −127.0, max: 127.0 % · Note: only validated when `number_of_banks == 2`
- **intake_air_temp_c** — min: −40.0, max: 140.0 °C · Note: —
- **throttle_pos_pct** — min: 0.0, max: 100.0 % · Note: —
- **control_module_voltage_v** — min: 0.0, max: 18.0 V · Note: PCM pin supply per ecu-diagnosis/09

**Rail-value rationale (T-W-6):** trims were widened to the OBD rail `±127`
because a railed trim is itself a *sensor-fault signal* consumed by COMLab
trim-evidence scoring; rejecting it as out-of-bounds would lose that signal.

**Bank-2 null contract:** `shrtft2`/`longft2` must be `null` (not `0.0`) when
`number_of_banks == 1`. Emitting `0.0` for an absent bank is a
`SEMANTIC_CONTRACT §4.4` violation.

## Graph relations (explicit)

**physical_sensor_bounds.json** DESCRIBES **12 PID bounds** (was 10 in v1.0, T-OBDV2-7/8)
**PIDIngestionValidator._validate_bounds** CONSUMES **physical_sensor_bounds.json** (bounds check)
**test_sensor_bounds.py** VERIFIES **physical_sensor_bounds.json ↔ OBDLab_KG_Wiki.md §3.1** (0 drift)
**T-W-6** DESCRIBES **trim bounds widened to ±127** (OBD rail for sensor-fault signal)
**SEMANTIC_CONTRACT §4.4** VERIFIES **bank-2 null contract** (null, never 0.0, for single-bank)
