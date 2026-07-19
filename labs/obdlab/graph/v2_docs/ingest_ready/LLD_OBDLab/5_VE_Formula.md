> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 5 VE Formula · Parent document: LLD_OBDLab.md

## 5. VE Formula (`core/ve_engine.py::_calc_ve_standard`)

Source: `OBDLab_KG_Wiki.md §10.1`. Implementation places R in the numerator and
MM_AIR in the denominator (physically correct unit placement; the wiki prose has
R/MM transposed — code is the truth).

```python
iat_k        = iat_c + K_OFFSET                              # wiki: §10.1
numerator    = maf * R_GAS * iat_k                           # wiki: §10.1 — R in numerator
denominator  = map_kpa * (rpm / 60.0) * (displacement / 2.0) * MM_AIR  # wiki: §10.1 — MM in denominator
return 0.0 if denominator == 0.0 else (numerator / denominator) * 100.0
```

`(displacement / 2.0)` = per-cycle displacement (4-stroke). `ve_pct` payload
bound is `[0.0, 200.0]` (§6.4 — 200 ceiling for thermal-shock steam overshoot).

**Degraded mode:** when `displacement`, `maf`, `map`, or `rpm` is missing (or
`rpm == 0`), `compute_ve` returns `(None, …, VEValidity.UNKNOWN)`; the
orchestrator substitutes the `0.0` sentinel into `ve_pct`. No crash.

### MAP_ONLY emulation / MAF_ONLY back-calculation

```python
# MAP_ONLY — emulate MAF, then run the standard formula:
emulated_maf = map_kpa * (rpm/60) * (disp/2) * MM_AIR / (R_GAS * iat_k) * target_ve
# MAF_ONLY — back-calculate MAP, then run the standard formula:
inferred_map = maf * R_GAS * iat_k / ((rpm/60) * (disp/2) * MM_AIR * target_ve)
```

Both single-sensor branches return `VEValidity.UNKNOWN` — the emulated/inferred
value algebraically cancels, leaving no independent cross-check.

## Graph relations (explicit)

**_calc_ve_standard** CONSUMES **MAF, MAP, RPM, displacement, IAT** (speed-density formula)
**_calc_ve_standard** DERIVED_FROM **VE(%) = (MAF·R·IAT_K) / (MAP·(RPM/60)·(disp/2)·MM_AIR) × 100** (# wiki: §10.1)
**ve_pct** GATED_BY **[0.0, 200.0]** (200 ceiling for thermal-shock steam overshoot, # wiki: §6.4)
**VEEngine._ve_map_only** DERIVED_FROM **emulated_maf from MAP, RPM, disp, IAT, target_ve** (MAP_ONLY branch)
**VEEngine._ve_maf_only** DERIVED_FROM **inferred_map from MAF, RPM, disp, IAT, target_ve** (MAF_ONLY branch)
**VEValidity.UNKNOWN** DESCRIBES **single-sensor branches** (no independent cross-check)
**test_ve_engine.py** VERIFIES **_calc_ve_standard** (unit tests)
