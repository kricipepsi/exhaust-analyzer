> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 7 COMLab Integration Points · Parent document: HLD_OBDLab.md

## 7. COMLab Integration Points

OBDLab emits at Stage 2; COMLab consumes at Stage 4. Several fields are
**frozen-contract surface** with a forward-registered consumer task — emitted
now, read when the COMLab fusion task lands. This is the deliberate
emit-S2 / consume-S4 pattern, kept honest by the signal/noise rule.

### Entity: OBDLivePayload field → COMLab consumer mapping

- **normalized_obd_lambda** → COMLab delta vs GASLab `lambda_chem` (ECU vs chemistry) · Status: **live route**
- **total_trim_correction_delta** (+`_b2`) → COMLab delta_Healing trim computation · Status: **live route**
- **per_bank_trim_delta** → `T-COMV2-BANK-FUSE-1` (bank asymmetry) · Status: **S4 forward-reg**
- **lambda_perception_delta** → `T-COMV2-ECU-FUSE-1` (ECU perception fusion) · Status: **S4 forward-reg**
- **ve_pct** / **ve_validity** → `T-COMV2-VE-GATE-1` (VE-as-evidence gate) · Status: **S4 forward-reg**
- **o2_failure_mode** (`WIDEBAND_OFFSET_CANDIDATE`) → `T-COMV2-O2OFFSET-1` · Status: **S4 forward-reg**
- **fuel_system_status** → live `analytics_preconditions` + `semantic_consistency_checker`; `T-COMV2-FUELSYS-GATE-1` · Status: **live + S4**
- **intake_air_temp_c** → live in `ve_engine`; `T-COMV2-ECU-HW-1` · Status: **live + S4**
- **throttle_pos_pct** → `T-COMV2-ECU-HW-1` · Status: **S4 forward-reg**
- **control_module_voltage_v** → `T-COMV2-VPWR-GATE-1` (electrical pre-check) · Status: **S4 forward-reg**
- **per_cylinder_misfire_counts** → `T-COMV2-MISFIRE-LOC-1` · Status: **S4 forward-reg**
- **ltft_cell_vector** → `T-COMV2-LTFT-CELL-1` · Status: **S4 forward-reg**
- **w_theo** / **sensor_error_delta** → `T-COMV2-MAF-LIN-1` · Status: **S4 forward-reg**
- **maf_status** / **map_status** → COMLab evidence weighting · Status: **S4**
- **rpm_state_bucket** / **engine_warmed** → fault-routing + analytics-applicability context · Status: **S4**
- **trim_analytics_gate** → COMLab confidence path (suppress trim findings unless VALID) · Status: **S4**
- **freeze_frame_pids** → ferried through from DTCLab (populated by COMLab pre-call) · Status: **passthrough**

> **Cross-lab note:** DTCLab and COMLab have **not yet been reworked**. The S4
> consumer tasks above are registered intent; when DTCLab/COMLab are rebuilt
> they reconcile up to this frozen OBD contract, not the other way around.
> OBDLab is never blocked on COMLab.

## Graph relations (explicit)

**COMLab** CONSUMES **normalized_obd_lambda** (live delta vs GASLab lambda_chem)
**COMLab** CONSUMES **total_trim_correction_delta** (live delta_Healing trim)
**COMLab** CONSUMES **fuel_system_status** (live analytics_preconditions + semantic_consistency_checker)
**COMLab** CONSUMES **intake_air_temp_c** (live ve_engine)
**COMLab T-COMV2-BANK-FUSE-1** CONSUMES **per_bank_trim_delta** (S4 forward-reg)
**COMLab T-COMV2-ECU-FUSE-1** CONSUMES **lambda_perception_delta** (S4 forward-reg)
**COMLab T-COMV2-VE-GATE-1** CONSUMES **ve_pct** / **ve_validity** (S4 forward-reg)
**COMLab T-COMV2-O2OFFSET-1** CONSUMES **o2_failure_mode.WIDEBAND_OFFSET_CANDIDATE** (S4 forward-reg, proposal EP-OBD-17)
**COMLab T-COMV2-MAF-LIN-1** CONSUMES **w_theo** / **sensor_error_delta** (S4 forward-reg)
**COMLab T-COMV2-MISFIRE-LOC-1** CONSUMES **per_cylinder_misfire_counts** (S4 forward-reg)
**COMLab T-COMV2-LTFT-CELL-1** CONSUMES **ltft_cell_vector** (S4 forward-reg)
**OBDLivePayload** MIRRORS_CONTRACT_IN **COMLab frozen contract surface** (emit-S2 / consume-S4)
