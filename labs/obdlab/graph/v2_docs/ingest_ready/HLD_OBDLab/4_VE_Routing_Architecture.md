> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 4 VE Routing Architecture · Parent document: HLD_OBDLab.md

## 4. VE Routing Architecture

`VEEngine.compute_ve` routes on `ObdLabDnaView.air_metering_strategy`. Three
branches cover the three real petrol sensor configurations:

### Entity: AirMeteringStrategy routing table

- **DUAL_MAF_MAP_CROSSCHECK** — Sensor config: Both present · VE branch: `_ve_dual` · MAF node: `REAL_SENSOR_FEED` · MAP node: `REAL_SENSOR_FEED` · Validity: classified (§6.4)
- **MAP_ONLY_SPEED_DENSITY** — Sensor config: MAP only · VE branch: `_ve_map_only` · MAF node: `VIRTUAL_EMULATION` · MAP node: `REAL_SENSOR_FEED` · Validity: `UNKNOWN` (no independent cross-check)
- **MAF_ONLY** — Sensor config: MAF only · VE branch: `_ve_maf_only` · MAF node: `REAL_SENSOR_FEED` · MAP node: `BACK_CALCULATED` · Validity: `UNKNOWN` (no independent cross-check)

Only `DUAL_MAF_MAP_CROSSCHECK` yields a cross-checkable VE and therefore a
non-`UNKNOWN` `ve_validity`. In the single-sensor branches the emulated/inferred
value algebraically cancels, so the validity is deliberately `UNKNOWN` — VE is
evidence only under the dual gate (T-OBDV2-2, Q5).

VE formula (speed-density / ideal gas), as implemented in `_calc_ve_standard`:

```
VE(%) = [MAF(g/s) × R(8.314) × (IAT_C + 273.15)]
        / [MAP(kPa) × (RPM/60) × (Disp_L/2) × MM_AIR(28.97)] × 100
```

`ve_pct` is bounded `[0.0, 200.0]` (the 200 ceiling accommodates thermal-shock
steam overshoot). When analytics are frozen or inputs are missing, `ve_pct`
carries the `0.0` sentinel and `ve_validity == UNKNOWN` suppresses all
VE-based router decisions downstream.

## Graph relations (explicit)

**VEEngine.compute_ve** ENUMERATES **AirMeteringStrategy** (3 branches: DUAL_MAF_MAP_CROSSCHECK, MAP_ONLY_SPEED_DENSITY, MAF_ONLY)
**ve_validity** ENUMERATES **VEValidity** (VALID, FAULT_VE_IDLE_COLLAPSE, FAULT_MAF_CONTAMINATION, FAULT_VE_SENSOR_SKEW, UNKNOWN)
**COMLab T-COMV2-VE-GATE-1** CONSUMES **ve_pct** / **ve_validity** (S4 forward-reg)
**ve_pct** DERIVED_FROM **MAF, MAP, RPM, displacement, IAT** (speed-density formula)
**VEEngine** MIRRORS_CONTRACT_IN **HLD §4 / DLD §9 / LLD §5–7**
