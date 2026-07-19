> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 13 lambda_perception_delta Guard · Parent document: LLD_OBDLab.md

## 13. `lambda_perception_delta` Guard

```python
if dna_view is not None and dna_view.upstream_o2_type == O2SensorType.WIDEBAND_LINEAR:
    cmd = sanitized.get("commanded_equivalence_ratio")   # PID 0x44
    if cmd is not None:
        if not isinstance(cmd, (int, float)):
            raise PIDValidationError(...)
        lambda_perception_delta = normalized_lambda - cmd
```

Emitter-only; the meaningful comparison (perception vs commanded) is COMLab's
`T-COMV2-ECU-FUSE-1`. **FU-ECU-2:** `commanded_equivalence_ratio` is currently
range-unbounded (numeric check only) — pin the λ bound from wiki PID 0x44 before
hardening.

## Graph relations (explicit)

**lambda_perception_delta** DERIVED_FROM **normalized_obd_lambda − commanded_equivalence_ratio** (PID 0x44)
**lambda_perception_delta** GATED_BY **WIDEBAND_LINEAR + commanded_equivalence_ratio present** (wideband + 0x44 guard)
**COMLab T-COMV2-ECU-FUSE-1** CONSUMES **lambda_perception_delta** (S4 forward-reg, emitter-only)
**FU-ECU-2** DESCRIBES **commanded_equivalence_ratio λ-range bound gap** (numeric check only, pin from wiki PID 0x44)
**test_ecu_perception_delta.py** VERIFIES **lambda_perception_delta** (emitter channel tests)
