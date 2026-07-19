> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 9 core/ve_engine.py · Parent document: DLD_OBDLab.md

## 9. `core/ve_engine.py` — `VEEngine`

`compute_ve(pids, bucket, dna_view) → (ve_pct|None, NodeMAFStatus, NodeMAPStatus, VEValidity)`.
Branches on `air_metering_strategy` (see HLD §4). `_classify_validity` applies
three fault triggers (thresholds in LLD §7); single-sensor branches return
`UNKNOWN` by construction. `_expected_ve` looks up per-(bucket, strategy)
emulation targets. Constants `MM_AIR`, `R_GAS`, `K_OFFSET` per LLD §1.

## Graph relations (explicit)

**VEEngine.compute_ve** CONSUMES **air_metering_strategy** (VE routing branch)
**VEEngine.compute_ve** CONSUMES **mass_airflow_gps** / **manifold_vacuum_kpa** (sensor inputs)
**VEEngine.compute_ve** CONSUMES **engine_displacement_liters** / **intake_air_temp_c** / **engine_rpm** (formula inputs)
**_classify_validity** ENUMERATES **FAULT_VE_IDLE_COLLAPSE, FAULT_MAF_CONTAMINATION, FAULT_VE_SENSOR_SKEW** (3 fault triggers)
**_expected_ve** ENUMERATES **per-(bucket, strategy) emulation targets** (6 entries)
**VEValidity** ENUMERATES **VALID, FAULT_VE_IDLE_COLLAPSE, FAULT_MAF_CONTAMINATION, FAULT_VE_SENSOR_SKEW, UNKNOWN**
**test_ve_engine.py** VERIFIES **VEEngine** (unit tests)
