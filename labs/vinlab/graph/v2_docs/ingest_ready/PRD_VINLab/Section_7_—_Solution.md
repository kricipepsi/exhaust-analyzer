> **Context:** VINLab PRD v2.1 (2026-06-12) | Module: VINLab | Section: Section 7 — Solution | Parent document: PRD_VINLab.md / SEMANTIC_CONTRACT section 4.1

## Section 7 — Solution

### Key Features (all P0)

- P0: **Structural validation** — `pre_clean_vin` (I→1, O→0 per SAE J853), 17-char
  length guard (`ChassisNumberError`), charset pattern `[A-HJ-NPR-Z0-9]{17}`, and
  NHTSA modulo-11 checksum with three documented bypass paths.
- P0: **WMI resolution** — standard positions 1–3, plus the SAE J853 low-volume rule
  (`vin[2] == '9'` → try the 6-char extended WMI `vin[0:3]+vin[11:14]` first).
- P0: **Year resolution** — `vin[9]` lookup, passthrough characters (`0`, `U`, `Z`) →
  `model_year = None`, and `L`-year disambiguation (1990 vs 2020) via WMI `era_hint`.
- P0: **Scope guards** — H1 petrol-only (keyword scan of CSV `fuel_system_type` and
  `vref.db` `fuel_delivery_type`), H2 model year ∈ [1990, 2020].
- P0: **Two-path engine resolution** — Path A `vds_full` (`vin[3:8]`), Path B
  `pos_8_only` (`vin[7]`) fallback, keyed by brand.
- P0: **vref.db tech-mask + CoC overlay** — `lookup_engine_ref()` (read-only SQLite)
  fetches induction, fuel delivery, MAF/MAP presence, euro norm, O2 type, EGR, and the
  13 CoC/type-approval/noise measurements.
- P0: **Overlay rules** — air-metering classification, euro→horizon mapping,
  stress-idle-RPM targeting, upstream-O2 derivation, cylinder-count fallback.
- P0: **Confidence grading** — `NONE` (engine not in CSV), `PARTIAL` (any downgrade
  flag), `HIGH` (clean resolve).
- P0: **`VinDNA` output dataclass** (frozen) with `to_json()` / `from_json()`.

### Technology

- Python 3.14. Standard library only at runtime (`csv`, `re`, `sqlite3`, `pathlib`) plus
  PyYAML for tooling; no network, no MySQL. Package `vinlab`, standalone
  `pyproject.toml`.
- Entry point: `vinlab.decode(vin, *, data_dir=None) → VinDNA`. The decoder is
  `lru_cache`d per `data_dir`, loading `wmi.csv`, `years.csv`, `vds_engine_map.csv`
  into memory once and opening `vref.db` read-only.
- Exceptions: `VINDecodeError(ValueError)` and `ChassisNumberError(VINDecodeError)`.
- No cross-lab imports — COMLab mirrors `VinDNA` locally.

### `VinDNA` fields (16 core + 13 CoC overlay)

### #: 1
- **Field**: `vin`
- **Type**: `str`
- **Source**: caller (cleaned)
- **contract cite**: §4.1

### #: 2
- **Field**: `make`
- **Type**: `str`
- **Source**: `wmi.csv` brand
- **contract cite**: §4.1

### #: 3
- **Field**: `model_year`
- **Type**: `int \
- **Source**: None`
- **contract cite**: `vin[9]` + `years.csv`

### #: 4
- **Field**: `engine_displacement_liters`
- **Type**: `float`
- **Source**: `vref.db displacement_cc` / CSV
- **contract cite**: §4.1

### #: 5
- **Field**: `cylinder_count`
- **Type**: `int`
- **Source**: CSV / `vref.db` / heuristic fallback
- **contract cite**: §4.1

### #: 6
- **Field**: `number_of_banks`
- **Type**: `int`
- **Source**: `is_v_engine` / config prefix
- **contract cite**: §4.1

### #: 7
- **Field**: `induction_type`
- **Type**: `InductionType`
- **Source**: `vref.db` / heuristic
- **contract cite**: §4.1, §6.1

### #: 8
- **Field**: `fuel_delivery_type`
- **Type**: `FuelDeliveryType`
- **Source**: `vref.db` / CSV
- **contract cite**: §4.1

### #: 9
- **Field**: `air_metering_architecture`
- **Type**: `AirMeteringArchitecture`
- **Source**: classifier
- **contract cite**: §4.1, §6.2

### #: 10
- **Field**: `emissions`
- **Type**: `Emissions`
- **Source**: `vref.db` + year rule
- **contract cite**: §4.1

### #: 11
- **Field**: `euro_emission_category`
- **Type**: `EuroEmissionCategory`
- **Source**: `vref.db euro_norm`
- **contract cite**: §4.1, §6.4

### #: 12
- **Field**: `resolved_horizon`
- **Type**: `Horizon`
- **Source**: `euro_to_horizon()`
- **contract cite**: §4.1, §6.4

### #: 13
- **Field**: `stress_idle_rpm_target`
- **Type**: `int`
- **Source**: `stress_idle_rpm()`
- **contract cite**: §4.1, §6.5

### #: 14
- **Field**: `rated_rpm`
- **Type**: `int \
- **Source**: None`
- **contract cite**: `vehicles_petrol_specimens.csv` `P14_rated_rpm` (T-DNA-3)

### #: 15
- **Field**: `confidence`
- **Type**: `VinConfidence`
- **Source**: decode flags
- **contract cite**: §4.1

### #: 16
- **Field**: `air_metering_strategy`
- **Type**: `AirMeteringStrategy`
- **Source**: classifier
- **contract cite**: §6.2

### #: 17–29
- **Field**: CoC overlay (13 fields)
- **Type**: `float\
- **Source**: int \
- **contract cite**: None`

The 13 CoC overlay fields are `target_lambda_v112`, `target_rpm_u2`, `idle_rpm_low`,
`co_low_idle`, `co_high_idle`, `co_type_approval`, `hc_type_approval`,
`nox_type_approval`, `hc_nox_type_approval`, `co2_type_approval`,
`noise_stationary_dba`, `noise_rpm`, `noise_driving_dba`.

### Assumptions

### Assumption: `vref.db` (small SQLite) is the runtime reference; `mysql_data/` (~484 MB) is build-time only
- **Validation**: tests skip when `vref.db` absent; `mysql_data/` flagged for Track-2 removal

### Assumption: European / Japanese / Korean / Indian VINs may legitimately lack a NHTSA check digit
- **Validation**: data-driven bypass via `wmi.csv` `country`

### Assumption: The cylinder-count heuristic is a last resort
- **Validation**: gated on `cylinder_count == 0`; never overwrites CSV/DB data

### Assumption: `VinDNA` shape is contract-owned (`SEMANTIC_CONTRACT.md §4.1`)
- **Validation**: enum-typed fields; `from_json` raises `KeyError` on missing required keys

---

## Graph relations (explicit)

**Section 7 — Solution** DESCRIBES **VINLab PRD v2.1 (2026-06-12)**
**vinlab.decoder.RobustVINDecoder.decode_vin_payload** CONSUMES **vinlab.models.VinDNA**
**labs/vinlab/tests/unit/test_vindna_from_json.py** VERIFIES **vinlab.models.VinDNA.from_json**
