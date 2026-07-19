> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 3 schemas/dna_view.py · Parent document: DLD_OBDLab.md

## 3. `schemas/dna_view.py`

### Enums (4)

### Entity: AirMeteringStrategy (3 members)

- **DUAL_MAF_MAP_CROSSCHECK** — Both MAF and MAP sensors present · Source: `OBD_VOCABULARY.md §4.2`
- **MAP_ONLY_SPEED_DENSITY** — MAP only, speed-density strategy · Source: `OBD_VOCABULARY.md §4.2`
- **MAF_ONLY** — MAF only, airflow-based strategy · Source: `OBD_VOCABULARY.md §4.2`

### Entity: O2SensorType (3 members)

- **NARROWBAND_0_TO_1V** — Standard narrowband · Source: `OBD_VOCABULARY.md §4.3`
- **WIDEBAND_LINEAR** — Linear wideband (direct λ) · Source: `OBD_VOCABULARY.md §4.3`
- **WIDEBAND_NB_SIM** — Wideband simulating narrowband · Source: `OBD_VOCABULARY.md §4.3`

### Entity: InductionType (2 members)

- **NATURALLY_ASPIRATED** — **TURBOCHARGED** · Source: `SEMANTIC_CONTRACT.md §8`

### Entity: VinConfidence (3 members)

- **HIGH** — Strict DNA-RPM gate · **PARTIAL** — Log + fallthrough to static · **NONE** — Static bounds only · Source: `SEMANTIC_CONTRACT.md §8`

**Removed from v1.0:** `EuroEmissionCategory` and `ResolvedHorizon` enums, and
the `ObdEmissionsView` sub-model — all pruned (PURGE-2) for lack of a live
consumer.

### `ObdLabDnaView` (7 fields)

### Entity: ObdLabDnaView fields

- **engine_displacement_liters** — `float | None` · Purpose: VE formula denominator
- **rated_rpm** — `int | None` · Purpose: DNA-RPM gate ceiling (HIGH confidence)
- **stress_idle_rpm_target** — `int | None` · Purpose: `STRESS_IDLE` `APPROXIMATELY` bucketing
- **air_metering_strategy** — `AirMeteringStrategy` · Purpose: VE routing branch
- **upstream_o2_type** — `O2SensorType` · Purpose: O2 normalisation path
- **induction_type** — `InductionType` · Purpose: `FAULT_VE_SENSOR_SKEW` classifier
- **confidence** — `VinConfidence` · Purpose: three-branch DNA-RPM gate

`None` at the call boundary is permitted and treated as `confidence == NONE`
(static bounds only, `DUAL_MAF_MAP_CROSSCHECK` + `NARROWBAND_0_TO_1V` defaults).
**Removed from v1.0:** `cylinder_count` (ARCH-2), `emissions` + `resolved_horizon`
(PURGE-2).

## Graph relations (explicit)

**dna_view.py** ENUMERATES **AirMeteringStrategy** (3 members) · **O2SensorType** (3) · **InductionType** (2) · **VinConfidence** (3)
**dna_view.py** DESCRIBES **ObdLabDnaView** (7 fields)
**ObdLabDnaView v2** SUPERSEDES **ObdLabDnaView v1.0** (cylinder_count, emissions, resolved_horizon pruned PURGE-2; EuroEmissionCategory, ResolvedHorizon enums removed)
**VEEngine** CONSUMES **air_metering_strategy** (VE routing branch)
**O2Normalizer** CONSUMES **upstream_o2_type** (O2 normalisation path)
**FAULT_VE_SENSOR_SKEW classifier** CONSUMES **induction_type**
**PIDIngestionValidator** CONSUMES **confidence** (DNA-RPM three-branch gate)
**PIDIngestionValidator** CONSUMES **rated_rpm** (HIGH confidence ceiling)
**PIDIngestionValidator** CONSUMES **engine_displacement_liters** (VE formula denominator)
**compute_bucket** CONSUMES **stress_idle_rpm_target** (APPROXIMATELY bucketing)
