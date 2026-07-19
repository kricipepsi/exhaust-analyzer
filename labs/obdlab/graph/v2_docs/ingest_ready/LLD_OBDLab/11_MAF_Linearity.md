> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 11 MAF Linearity · Parent document: LLD_OBDLab.md

## 11. MAF Linearity (`core/maf_linearity.py`)

Source: `research/chunks/pids-protocol/05`.

```python
W_theo = (eta_v * displacement * map_kpa * rpm) / (120.0 * R(0.287) * (iat_c + 273.15))

ΔSensor_error =
    ( |maf_stress − W_theo_stress| / W_theo_stress
    − |maf_idle   − W_theo_idle|   / W_theo_idle ) * 100.0
```

Both guard against a zero denominator (return `0.0`). Emitted only under
`DUAL_MAF_MAP_CROSSCHECK` once the `LinearityAccumulator` holds **both** the
`STABILIZED_IDLE` and `STRESS_IDLE` bands.

## Graph relations (explicit)

**calculate_w_theo** DERIVED_FROM **W_theo = (η_V · disp · map · rpm) / (120 · R · T_K)** (# wiki: research/chunks/pids-protocol/05)
**calculate_sensor_error_delta** DERIVED_FROM **Δ = (|maf_stress − W_stress|/W_stress − |maf_idle − W_idle|/W_idle) × 100** (# wiki: research/chunks/pids-protocol/05)
**calculate_w_theo** GATED_BY **zero denominator guard** (return 0.0)
**calculate_sensor_error_delta** GATED_BY **zero denominator guard** (return 0.0)
**maf_linearity helpers** GATED_BY **DUAL_MAF_MAP_CROSSCHECK + LinearityAccumulator** (both bands: STABILIZED_IDLE + STRESS_IDLE)
**COMLab T-COMV2-MAF-LIN-1** CONSUMES **w_theo / sensor_error_delta** (S4 forward-reg)
**test_maf_linearity.py** VERIFIES **maf_linearity helpers** (unit tests)
