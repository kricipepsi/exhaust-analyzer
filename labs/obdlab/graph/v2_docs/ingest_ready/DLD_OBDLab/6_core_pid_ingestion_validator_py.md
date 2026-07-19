> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 6 core/pid_ingestion_validator.py · Parent document: DLD_OBDLab.md

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

## Graph relations (explicit)

**PIDIngestionValidator.validate_and_convert** ROUTES_TO **7-step validation pipeline**
**PIDIngestionValidator** CONSUMES **physical_sensor_bounds.json** (bounds config)
**PIDIngestionValidator** CONSUMES **ObdLabDnaView** (DNA-RPM gate)
**_validate_bounds** VERIFIES **12 PID fields vs physical_sensor_bounds.json §3.1**
**_check_dna_rpm** VERIFIES **engine_rpm vs rated_rpm × 1.05** (HIGH confidence only)
**_enforce_bank2_contract** VERIFIES **SEMANTIC_CONTRACT §4.4** (bank-2 null for single-bank)
**_validate_and_map_fuel_system_status** CONSUMES **FuelSystemStatus.from_wire**
**_validate_per_cylinder_misfire_counts** VERIFIES **cyl ≥ 1, count ≥ 0**
**_validate_ltft_cell_vector** VERIFIES **cell ≥ 0, value ∈ [-127, 127]**
**test_pid_ingestion_validator.py** VERIFIES **PIDIngestionValidator** (unit tests)
