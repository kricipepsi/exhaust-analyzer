# VIN_VOCABULARY — VINLab (v2)
**Status:** Current (reflects shipped `models.py`)
**Date:** 2026-06-12
**Source of truth:** `SEMANTIC_CONTRACT.md §4.1, §6.x, §8`; enums mirrored locally in
`vinlab/models.py` (future: import from `comlab.schemas.vocabulary` at Phase 0b).

This file is the single reference for every wire-format vocabulary string VINLab emits
on `VinDNA`. All values are strings consumed across the JSON boundary; renaming a member
is a breaking contract change. Drift between this file and `models.py` is a code-review
stop.

---

## 1. Enums (9 StrEnums)

### `Horizon` — architecture era (contract §6.4)
| Member | Wire value | Derived from |
|--------|-----------|--------------|
| `LEGACY` | `HORIZON_LEGACY` | EURO_1, EURO_2 |
| `ADAPTIVE` | `HORIZON_ADAPTIVE` | EURO_3, EURO_4 |
| `MODERN` | `HORIZON_MODERN` | EURO_5, EURO_6, EURO_7 |

### `EuroEmissionCategory` — emission standard (contract §4.1)
`EURO_1`, `EURO_2`, `EURO_3`, `EURO_4`, `EURO_5`, `EURO_6`, `EURO_7` (7 members).
Raw `euro_norm` strings are normalised via `_EURO_MAP` (`euro N` / `euroN` → `EURO_N`);
an unknown value defaults to `EURO_1`.

### `InductionType` — mechanical induction (contract §6.1)
`NATURALLY_ASPIRATED`, `TURBOCHARGED`, `SUPERCHARGED`.

### `AirMeteringStrategy` — OBDLab-canonical metering (contract §6.2)
`DUAL_MAF_MAP_CROSSCHECK`, `MAP_ONLY_SPEED_DENSITY`, `MAF_ONLY`. This is the routing
switch OBDLab's VE engine branches on.

### `PrimaryLoadCalculation` — developer-facing load label (contract §6.2)
`HYBRID_MAF_MAP`, `MAP_ONLY`, `MAF_ONLY`. Paired with `AirMeteringStrategy` (one
classification, two views — ADR-0005).

### `FuelDeliveryType` — fuel delivery method (contract §8)
`GDI`, `PORT_INJECTION`, `CARBURETOR`.

### `UpstreamO2Type` — pre-cat O2 sensor type (contract §6.3)
`NARROWBAND`, `WIDEBAND_AFR`, `WIDEBAND_LAMBDA`, `WIDEBAND_NB_SIM`, `NONE`.
`WIDEBAND_NB_SIM` = an aftermarket wideband controller in narrowband-simulation mode
(physically wideband, emits a 0–1 V simulated NB signal; OBDLab reads
`pid_oxygen_sensor_volts`).

> **Mirror divergence (COMLab-D):** OBDLab's local mirror uses
> `NARROWBAND_0_TO_1V` / `WIDEBAND_LINEAR` / `WIDEBAND_NB_SIM`. The projector reconciles
> VINLab's member names to the OBDLab-canonical set; the realignment is tracked as
> COMLab-D (rework audit). Do not rename either side unilaterally.

### `VinConfidence` — decode confidence (contract §8)
`HIGH` (clean resolve), `PARTIAL` (any downgrade flag), `NONE` (engine not in CSV).
Consumed by OBDLab's three-branch DNA-RPM gate.

### `DownstreamTrimRole` — downstream O2 role (O2_MODEL_STRATEGY.md §3)
`NONE`, `CATALYST_MONITOR_ONLY`, `SECONDARY_FUEL_TRIM`. VINLab is the owning lab;
COMLab mirrors it over the JSON boundary.

---

## 2. Nested object keys

### `air_metering_architecture`
`has_maf_sensor` (bool), `has_map_sensor` (bool),
`primary_load_calculation` (`PrimaryLoadCalculation`).

### `emissions`
`upstream_o2_type` (`UpstreamO2Type`), `downstream_o2_present` (bool),
`downstream_trim_role` (`DownstreamTrimRole`), `has_catalyst` (bool),
`egr_equipped` (bool).

> **Contract reconciliation (T-DNA-4, done):** the emissions block is formalized as
> `{upstream_o2_type, downstream_o2_present, downstream_trim_role, has_catalyst,
> egr_equipped}`. `has_catalyst` (default `True`) and `egr_equipped` (default `False`) are
> kept **nested under `emissions`** — `has_catalyst` gates GASLab catalyst diagnostics and
> DTCLab `CATALYST_HISTORY`; `egr_equipped` gates EGR fault routing / DTCLab `EGR_HISTORY`.
> The legacy `secondary_air_equipped` is dropped (no named consumer).

---

## 3. `VinDNA` top-level keys (JSON contract surface)

Core (16): `vin`, `make`, `model_year`, `engine_displacement_liters`, `cylinder_count`,
`number_of_banks`, `induction_type`, `fuel_delivery_type`, `air_metering_architecture`,
`emissions`, `euro_emission_category`, `resolved_horizon`, `stress_idle_rpm_target`,
`rated_rpm`, `confidence`, `air_metering_strategy`.

> `rated_rpm` (`int | None`) is emitted by `VinDNA` since T-DNA-3 — source
> `DBS/docs/vehicles_petrol_specimens.csv` `P14_rated_rpm`. Consumer: COMLab `projection.py`
> → `ObdLabDnaView.rated_rpm` → the OBDLab RPM ceiling.

CoC overlay (13): `target_lambda_v112`, `target_rpm_u2`, `idle_rpm_low`, `co_low_idle`,
`co_high_idle`, `co_type_approval`, `hc_type_approval`, `nox_type_approval`,
`hc_nox_type_approval`, `co2_type_approval`, `noise_stationary_dba`, `noise_rpm`,
`noise_driving_dba`.

---

## 4. Confidence flag vocabulary (internal — not on `VinDNA`)

These strings are collected during decode and collapse into the `confidence` grade;
they are **not** serialised:

| Flag | Meaning | Grade effect |
|------|---------|--------------|
| `era_hint_unrecognised` | L-year era hint did not match ERA_1/ERA_3 | PARTIAL |
| `engine_not_in_csv` | no `vds_full`/`pos_8_only` match | NONE |
| `no_engine_code` | engine row present but blank engine_code | PARTIAL |
| `engine_not_in_vref` | engine_code not in `vref.db` | PARTIAL |
| `coc_null_<field>` | a core CoC field is NULL (first of 9 checked) | PARTIAL |

The 9 CoC fields that drive the downgrade: `target_lambda_v112`, `target_rpm_u2`,
`idle_rpm_low`, `co_low_idle`, `co_high_idle`, `co_type_approval`, `hc_type_approval`,
`nox_type_approval`, `co2_type_approval`. The `hc_nox` and three noise fields do **not**
affect confidence (documented gap, HLD §9).

---

## 5. Out-of-scope keyword vocabulary (H1 petrol guard)

`_NON_PETROL_KEYWORDS`: `DIESEL`, `LPG`, `CNG`, `E85`, `HYBRID`, `ELECTRIC`, `EV`,
`FLEX_FUEL`, `FLEXFUEL`, `METHANOL`, `ETHANOL`, `BIOFUEL`. Any match in CSV
`fuel_system_type` or `vref.db` `fuel_delivery_type` raises `VINDecodeError`.

---

## 6. Forbidden / retired tokens

| Token | Status |
|-------|--------|
| bare `str` vocabulary fields | retired — replaced by StrEnums (ADR-0004 / T-FX-5) |
| duplicate air-metering switch logic | retired — single classifier (ADR-0005 / T-FX-2) |
| SQL outside `db/tecdoc_query.py` | forbidden — H8 SQL-isolation |
| cross-lab import (except `dnalab → vinlab`) | forbidden — DNA-family boundary |
| `rated_rpm` on `VinDNA` | **emitted** since T-DNA-3 (source `P14_rated_rpm`) |
| `model` on `VinDNA` | **kept-empty** (no field) — T-DNA-5: DBS shows no within-engine-code variance, so no diagnostic signal; DTCLab mirror relaxed via COMLab-D |
| `fuel_type` / `altitude_band` on `VinDNA` | proposal-only (COMLab-E) — not in the live schema; `fuel_type` → future `GasLabDnaView` (E5/E10), `altitude_band` stays session/context (lambda is altitude-invariant) |
