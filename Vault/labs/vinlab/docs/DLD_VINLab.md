---
node_type: "dld"
lab: "vinlab"
module: "vinlab"
subsystem: "detailed-design"
implements:
  - "labs/vinlab/vinlab/__init__.py"
  - "labs/vinlab/vinlab/decoder.py"
  - "labs/vinlab/vinlab/models.py"
  - "labs/vinlab/vinlab/db/tecdoc_query.py"
  - "labs/vinlab/vinlab/overlay/air_metering.py"
  - "labs/vinlab/vinlab/overlay/cylinder_heuristic.py"
  - "labs/vinlab/vinlab/overlay/horizon.py"
  - "labs/vinlab/vinlab/overlay/stress_rpm.py"
  - "labs/vinlab/vinlab/overlay/switches.py"
consumers:
  - "dnalab: labs/dnalab/dnalab/assembly.py decode_vin_payload() -> VehicleDNA Part A"
  - "dnalab: labs/dnalab/dnalab/models.py VinDNA.from_json -> VehicleDNA.vin_dna"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py (VinDNA integration)"
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py (FuelSystemStatus comparison)"
drift_guards:
  - "labs/vinlab/tests/unit/test_decoder.py"
  - "labs/vinlab/tests/unit/test_models.py"
  - "labs/vinlab/tests/unit/test_horizon.py"
  - "labs/vinlab/tests/unit/test_stress_rpm.py"
  - "labs/vinlab/tests/unit/test_switches.py"
  - "labs/vinlab/tests/unit/test_cylinder_heuristic.py"
  - "labs/vinlab/tests/unit/test_air_metering.py"
  - "labs/vinlab/tests/unit/test_contract_conformance.py"
  - "labs/vinlab/tests/unit/test_vindna_from_json.py"
tags: [vinlab, finished, dld]
source: "labs/vinlab/docs/DLD_VINLab.md"
---
# DLD — VINLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_VINLab v2.0
**HLD Reference:** HLD_VINLab v2.1
**Version:** 2.1
**Date:** 2026-06-12

> Grounded in the live `vinlab/` package as of 2026-06-12 (`rated_rpm` emitted, CoC +
> emissions formalized — T-DNA-3/4). Field/enum tables are the source-of-truth surface;
> numeric constants and formulas live in `LLD_VINLab.md`.

---

## 1. Module Map

```
vinlab/
├── __init__.py            ← public surface: decode(), VinDNA, VINDecodeError, ChassisNumberError
├── decoder.py             ← RobustVINDecoder (validation, WMI/year/engine resolvers, assembly)
├── models.py              ← VinDNA + 9 enums + AirMeteringArchitecture + Emissions
├── db/
│   ├── __init__.py        ← "all SQL lives here (H8)"
│   └── tecdoc_query.py    ← lookup_engine_ref(), open_vref_readonly()
├── overlay/
│   ├── __init__.py
│   ├── air_metering.py    ← classify_air_metering() (single deep module, T-FX-2)
│   ├── horizon.py         ← euro_to_horizon(), _year_to_horizon()
│   ├── stress_rpm.py      ← stress_idle_rpm()
│   ├── switches.py        ← derive_upstream_o2_type()
│   └── cylinder_heuristic.py ← infer_cylinder() + per-brand rules (T-VL-7)
└── data/                  ← wmi.csv, years.csv, vds_engine_map.csv, vref.db (baked at build)
```

The public `decode()` wraps a `lru_cache`d `RobustVINDecoder` per `data_dir`. There is
no Python package under `data/` — it is reference data only.

---

## 2. `models.py` — Enums (9 StrEnums)

All values are wire-format strings consumed across the JSON boundary; renames are
breaking changes. Locked to `SEMANTIC_CONTRACT.md §8` (future: import from
`comlab.schemas.vocabulary` when Phase 0b ships — currently a local copy).

| Enum | Members | Contract |
|------|---------|----------|
| `Horizon` | `HORIZON_LEGACY`, `HORIZON_ADAPTIVE`, `HORIZON_MODERN` | §6.4 |
| `EuroEmissionCategory` | `EURO_1` … `EURO_7` (7) | §4.1 |
| `InductionType` | `NATURALLY_ASPIRATED`, `TURBOCHARGED`, `SUPERCHARGED` | §6.1 |
| `AirMeteringStrategy` | `DUAL_MAF_MAP_CROSSCHECK`, `MAP_ONLY_SPEED_DENSITY`, `MAF_ONLY` | §6.2 |
| `PrimaryLoadCalculation` | `HYBRID_MAF_MAP`, `MAP_ONLY`, `MAF_ONLY` | §6.2 |
| `FuelDeliveryType` | `GDI`, `PORT_INJECTION`, `CARBURETOR` | §8 |
| `UpstreamO2Type` | `NARROWBAND`, `WIDEBAND_AFR`, `WIDEBAND_LAMBDA`, `WIDEBAND_NB_SIM`, `NONE` | §6.3 |
| `VinConfidence` | `HIGH`, `PARTIAL`, `NONE` | §8 |
| `DownstreamTrimRole` | `NONE`, `CATALYST_MONITOR_ONLY`, `SECONDARY_FUEL_TRIM` | O2_MODEL_STRATEGY.md §3 |

> **Vocabulary divergence note:** `UpstreamO2Type` in VINLab carries five members
> (`NARROWBAND`/`WIDEBAND_AFR`/`WIDEBAND_LAMBDA`/`WIDEBAND_NB_SIM`/`NONE`), whereas
> OBDLab's mirror uses `NARROWBAND_0_TO_1V`/`WIDEBAND_LINEAR`/`WIDEBAND_NB_SIM`. The
> projector reconciles these; the canonical-vocabulary realignment is COMLab-D
> (rework audit). Documented, not yet resolved.

---

## 3. `models.py` — Nested dataclasses

### `AirMeteringArchitecture` (frozen)

| Field | Type | Default |
|-------|------|---------|
| `has_maf_sensor` | `bool` | `False` |
| `has_map_sensor` | `bool` | `False` |
| `primary_load_calculation` | `PrimaryLoadCalculation` | `MAP_ONLY` |

### `Emissions` (frozen)

| Field | Type | Default | Source |
|-------|------|---------|--------|
| `upstream_o2_type` | `UpstreamO2Type` | `NARROWBAND` | §4.1 |
| `downstream_o2_present` | `bool` | `False` | year ≥ 1996 rule |
| `downstream_trim_role` | `DownstreamTrimRole` | `NONE` | O2_MODEL_STRATEGY.md §3 |
| `has_catalyst` | `bool` | `True` | O2_MODEL_STRATEGY.md §9.1 |
| `egr_equipped` | `bool` | `False` | `vref.db has_egr` |

> **Contract reconciliation (T-DNA-4, done):** the `Emissions` block above is the
> formalized shape. `has_catalyst` (gates GASLab catalyst diagnostics + DTCLab
> `CATALYST_HISTORY`) and `egr_equipped` (gates EGR routing + DTCLab `EGR_HISTORY`) are
> kept **nested under `emissions`**; the legacy `secondary_air_equipped` from the
> `VehicleDNA.md` example is dropped (no named consumer). The projector still reads these
> flags at top level — that path fix is the paired COMLab-C change at Stage 4.

---

## 4. `models.py` — `VinDNA` (frozen dataclass)

Schema governed by `SEMANTIC_CONTRACT.md §4.1`. `to_json()` walks via
`dataclasses.asdict()` then coerces enum members to `.value`; `from_json()` is the
inverse (required keys raise `KeyError`, optional CoC fields preserve `None`).

### Core fields (16)

| # | Field | Type | Default |
|---|-------|------|---------|
| 1 | `vin` | `str` | `""` |
| 2 | `make` | `str` | `""` |
| 3 | `model_year` | `int \| None` | `None` |
| 4 | `engine_displacement_liters` | `float` | `0.0` |
| 5 | `cylinder_count` | `int` | `0` |
| 6 | `number_of_banks` | `int` | `1` |
| 7 | `induction_type` | `InductionType` | `NATURALLY_ASPIRATED` |
| 8 | `fuel_delivery_type` | `FuelDeliveryType` | `PORT_INJECTION` |
| 9 | `air_metering_architecture` | `AirMeteringArchitecture` | factory |
| 10 | `emissions` | `Emissions` | factory |
| 11 | `euro_emission_category` | `EuroEmissionCategory` | `EURO_1` |
| 12 | `resolved_horizon` | `Horizon` | `MODERN` |
| 13 | `stress_idle_rpm_target` | `int` | `3000` |
| 14 | `rated_rpm` | `int \| None` | `None` (source `P14_rated_rpm`, T-DNA-3) |
| 15 | `confidence` | `VinConfidence` | `NONE` |
| 16 | `air_metering_strategy` | `AirMeteringStrategy` | `MAP_ONLY_SPEED_DENSITY` |

### CoC empirical overlay fields (13, all `| None`)

| Field | Type | Consumer |
|-------|------|----------|
| `target_lambda_v112` | `float \| None` | GASLab lambda target (formalized T-DNA-4; projector path fix = COMLab-C) |
| `target_rpm_u2` | `int \| None` | high-idle RPM reference |
| `idle_rpm_low` | `int \| None` | low-idle RPM reference |
| `co_low_idle` | `float \| None` | GASLab CO low-idle threshold |
| `co_high_idle` | `float \| None` | GASLab CO high-idle threshold |
| `co_type_approval` | `float \| None` | type-approval CO |
| `hc_type_approval` | `float \| None` | type-approval HC |
| `nox_type_approval` | `float \| None` | type-approval NOx |
| `hc_nox_type_approval` | `float \| None` | type-approval HC+NOx |
| `co2_type_approval` | `float \| None` | type-approval CO₂ |
| `noise_stationary_dba` | `float \| None` | stationary noise |
| `noise_rpm` | `int \| None` | noise-test RPM |
| `noise_driving_dba` | `float \| None` | drive-by noise |

> The CoC fields are **top-level** on `VinDNA` (formalized by T-DNA-4). The projector
> still reads them under `emissions{}`, so the remaining fix is the paired **COMLab-C**
> path change at Stage 4 (read CoC at top level, emissions flags at `emissions.*`). That
> is a COMLab change, not a VINLab one.

---

## 5. `decoder.py` — `RobustVINDecoder`

**`__init__(data_dir)`** loads three CSVs into in-memory dicts and records the
`vref.db` path:

```
wmi_index:        {wmi → {brand, country, era_hint}}            (wmi.csv)
year_index:       {year_code → [{calendar_year, era_bucket}]}  (years.csv; L repeats)
vds_full_index:   {BRAND_VDSFULL → row}                         (vds_engine_map.csv)
vds_pos8_index:   {BRAND_POS8 → row}                            (vds_engine_map.csv)
db_path:          data_dir / vref.db
```

**`decode_vin_payload(raw_vin, *, pre_clean=True) → VinDNA`** — the orchestrator
(HLD §3). **`validate_vin_checksum(vin) → bool`** — NHTSA mod-11 with three bypass
paths (LLD §3). **`_resolve_wmi` / `_resolve_year` / `_resolve_engine`** — the three
resolvers (HLD §5–§6).

**Module-level functions:** `pre_clean_vin(raw)` (I→1, O→0), `_normalise_euro(raw)`
(maps `euro N` → `EURO_N`), `_is_non_petrol(*values)` (H1 keyword scan).

---

## 6. Air-metering derivation (`decoder.py` + `overlay/air_metering.py`)

The decoder derives the `(has_maf, has_map)` fact, then the classifier maps it once:

```
has_maf = bool(db.has_maf)  if present  else  fuel_delivery != CARBURETOR
has_map = bool(db.has_map)  if present  else
          (induction ∈ {TURBO, SUPER}) or fuel ∈ {CARBURETOR, GDI} or egr_equipped

classify_air_metering(has_maf, has_map):
    both    → (HYBRID_MAF_MAP, DUAL_MAF_MAP_CROSSCHECK)
    MAF     → (MAF_ONLY,       MAF_ONLY)
    MAP/neither → (MAP_ONLY,   MAP_ONLY_SPEED_DENSITY)
```

`classify_air_metering` returns a frozen `AirMeteringClassification` carrying both the
developer label and the OBDLab-canonical strategy — one classification, two views
(T-FX-2 closed the "two parallel switches" defect).

---

## 7. `overlay/cylinder_heuristic.py` — `infer_cylinder`

Returns a frozen `CylinderHint(count, config, induction, source)`; `count == 0` means
unresolved. Fires only when `cylinder_count == 0` after CSV + `vref.db`. Brand dispatch
table (`_BRAND_DISPATCH`) routes to per-manufacturer rules:

| Brand(s) | Rule sketch |
|----------|-------------|
| BMW | `[NBMS]XX` family digit → cyl; turbo families {N54,N55,B58,S55,S63}; displacement tiebreak |
| Hyundai/Kia | `G[n]` → second char is cylinder digit |
| Honda | J-series ≥ 3.0 L → V6; D/B/F/K/R/J/L → I4 |
| Toyota | family-prefix sets (I4/V6/V8) |
| Volvo | `B[n]` digit = cyl; `T` suffix → turbo |
| Mercedes | `MXXX` code → table lookup |
| VW/Audi/Skoda/Seat | displacement bands + brand-aware induction |
| Nissan | family-prefix sets (I4/V6/turbo-I4) |
| Mitsubishi | leading digit = cyl |
| Mazda | `[BFKP]n` → I4 |
| Subaru | `EJ/FA/FB/EE` → BOXER_4; `EZ` → BOXER_6 |
| Renault/Dacia | family table (I4/I3) |
| PSA (Peugeot/Citroen) | `XU/ES/EW` → I4 |
| unknown brand | displacement-only fallback |

Displacement fallback bands (`_displacement_fallback`): ≤1.2 → I3, ≤2.5 → I4, ≤3.5 →
V6, ≤5.0 → V8, >5.0 → V12. Config vocabulary `_CONFIG_VOCAB` (I3/I4/I5/I6/V6/V8/V10/V12/
BOXER_4/BOXER_6/ROTARY/W12) is aux data — `config` is **not** stored on `VinDNA`; it
feeds only `number_of_banks` (V/W/Boxer → 2) and the induction default.

---

## 8. `db/tecdoc_query.py` — SQL isolation (H8)

```python
lookup_engine_ref(db_path, engine_code) → dict | None
    # SELECT * FROM engine_ref WHERE engine_code = ?  (read-only URI: file:...?mode=ro)
open_vref_readonly(db_path) → sqlite3.Connection
```

All SQL strings in the codebase live here. `vref.db` is opened read-only via the SQLite
URI `mode=ro`; rows are returned as plain dicts keyed by column.

---

## 9. Confidence grading (`decoder.py`)

```
conf_flags collected during decode:
    year:    era_hint_unrecognised
    engine:  engine_not_in_csv | no_engine_code | engine_not_in_vref
    coc:     coc_null_<field>   (first NULL among 9 core CoC fields)

if "engine_not_in_csv" in conf_flags → VinConfidence.NONE
elif conf_flags                       → VinConfidence.PARTIAL
else                                  → VinConfidence.HIGH
```

`confidence` drives OBDLab's three-branch DNA-RPM gate (HIGH strict / PARTIAL
log-fallthrough / NONE static bounds).

---

## 10. Error Types

| Error | Base | Raised when |
|-------|------|-------------|
| `VINDecodeError` | `ValueError` | invalid charset; checksum fail; WMI not found; year char not found; year out of scope (H2); fuel out of scope (H1) |
| `ChassisNumberError` | `VINDecodeError` | `len(vin) != 17` — likely a pre-VIN chassis/frame number |

Catching `VINDecodeError` also catches `ChassisNumberError`; callers route the latter
to a legacy-identifier pipeline.

---

## 11. Test Coverage (current)

| Area | Location |
|------|----------|
| Decoder + resolvers | `tests/` (fixtures under `tests/fixtures/`) |
| Tooling / build data | `tools/`, `temp/` dry-run outputs |
| Graph artefacts | `graph/v1_baseline` vs `graph/v2_current` (off-runtime; no code reads them) |

> Tests skip when `vref.db` is absent. `graph/` is a frozen, verified artefact — not in
> the inner loop or verification gate (do **not** re-run graphify).
