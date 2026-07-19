> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 12 core/maf_linearity.py · Parent document: DLD_OBDLab.md

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

## Graph relations (explicit)

**calculate_w_theo** DERIVED_FROM **eta_v, displacement, map_kpa, rpm, iat_c** (speed-density theoretical airflow)
**calculate_sensor_error_delta** DERIVED_FROM **maf_stress, w_theo_stress, maf_idle, w_theo_idle** (two-point non-linearity delta)
**maf_linearity helpers** CONSUMES **LinearityAccumulator** (idle + stress bands guard)
**maf_linearity helpers** GATED_BY **DUAL_MAF_MAP_CROSSCHECK** (two-point guard)
**COMLab T-COMV2-MAF-LIN-1** CONSUMES **w_theo / sensor_error_delta** (S4 forward-reg, T-OBDV2-10)
**test_maf_linearity.py** VERIFIES **maf_linearity helpers** (unit tests)
