# BUILD_DATA_SOURCES.md — VinDNA Field-to-Source Contract

**Purpose:** the input contract for T-VL-3 (`tools/build_vref_db.py`) and T-VL-4 (CSV builds). Maps every `VinDNA` field to its build-time source(s) with precedence. No Python; document only.

**Architecture:** approach C (standalone). All data baked at build time. Runtime has zero MySQL and zero network.

**Version:** 1.0 (2026-05-17)
**Superseded by:** `SEMANTIC_CONTRACT.md` §4.1 where field names differ.

---

## Section A — Field-to-source map

Each field maps to one primary source + up to two fallbacks. "Derived" fields are computed at decode time from other fields already populated.

### A.1 Top-level scalar fields

| # | Field | Type | Primary source | Fallback 1 | Fallback 2 | Build script | Notes |
|---|---|---|---|---|---|---|---|
| 1 | `vin` | `str` | Input parameter | — | — | — | Passed by caller; validated in decoder |
| 2 | `make` | `str` | vPIC WMI table | petrol CSV `D1_make` | TecDoc `manufacturers` | `tools/import_vpic.py` → `build_wmi_map.py` | Normalised to canonical brand name per contract §8 |
| 3 | `model` | `str` | petrol CSV `D3_commercial_name` | vPIC VDS pattern | TecDoc `models` | `tools/build_vds_map.py` | |
| 4 | `model_year` | `int` | vPIC year-code table (corrected for `L` via WMI `era_hint`) | petrol CSV `B_first_reg_date` | — | `tools/import_vpic.py` → `build_years_csv.py` | Position-10 → calendar year; `L` disambiguated per VINlookup.md |
| 5 | `engine_displacement_liters` | `float` | petrol CSV `P11_displacement_cc` ÷ 1000 | TecDoc `Capacity_Technical` | vPIC VDS pattern | `tools/build_vds_map.py` + `tools/build_vref_db.py` | TecDoc value parsed from `"1998 ccm"` format |
| 6 | `cylinder_count` | `int` | petrol CSV (derived; no direct column — inferred from displacement + euro class) | TecDoc `NumberOfCylinders` | vPIC VDS pattern | `tools/build_vds_map.py` + `tools/build_vref_db.py` | |
| 7 | `number_of_banks` | `int` | Derived from `engine_configuration` | — | — | `vinlab/overlay/switches.py` | `"ряд"/Inline` → 1, `"V"/"VR"` → 2, `"W"` → 3 or 4, `"оппозитный"/Boxer` → 2 |
| 8 | `engine_configuration` | `str` | TecDoc `EngineConstruction` | YAML | — | `tools/build_vref_db.py` | Values: `I4`, `V6`, `V8`, `VR6`, `W12`, `BOXER_4`, `ROTARY` (translated from Russian) |
| 9 | `induction_type` | `str` | TecDoc `ChargeType` | YAML | — | `tools/build_vref_db.py` | Contract §8 values: `NATURALLY_ASPIRATED`, `TURBOCHARGED`, `SUPERCHARGED` |
| 10 | `fuel_delivery_type` | `str` | TecDoc `FuelMixture` | YAML | vPIC | `tools/build_vref_db.py` | Contract §8 values: `GDI`, `PORT_INJECTION`, `CARBURETOR` |
| 11 | `euro_emission_category` | `str` | petrol CSV `euro_label` | TecDoc `EmissionNorm` | YAML | `tools/build_vref_db.py` | Contract §8 values: `EURO_1` through `EURO_7` |
| 12 | `stress_idle_rpm_target` | `int` | Overlay rules (`vinlab/overlay/stress_rpm.py`) | — | — | — | Derived from engine code + emission tier + induction type at decode time |
| 13 | `confidence` | `str` | Computed internally by decoder | — | — | — | Contract §8 values: `HIGH`, `PARTIAL`, `NONE` |

### A.2 Air metering architecture (nested)

| # | Field | Type | Primary source | Fallback 1 | Fallback 2 | Build script | Notes |
|---|---|---|---|---|---|---|---|
| 14 | `air_metering_architecture.has_maf_sensor` | `bool` | TecDoc part-level lookup (`prd` + `passanger_car_pds`) | heuristic (`fuel_delivery != CARBURETOR`) | — | `tools/build_vref_db.py` | `has_maf` column in `engine_ref`; assembly group "Приготовление смеси"; implemented T-FX-13 |
| 15 | `air_metering_architecture.has_map_sensor` | `bool` | TecDoc part-level lookup (`prd` + `passanger_car_pds`) | heuristic (turbo/GDI/EGR/carb) | — | `tools/build_vref_db.py` | `has_map` column in `engine_ref`; `prd.id=161` (boost pressure sensor); implemented T-FX-13 |
| 16 | `air_metering_architecture.primary_load_calculation` | `str` | Derived from `has_maf_sensor` + `has_map_sensor` | — | — | `vinlab/overlay/switches.py` | Contract §6.2 mapping; values: `HYBRID_MAF_MAP`, `MAP_ONLY`, `MAF_ONLY` |

### A.3 Emissions (nested)

| # | Field | Type | Primary source | Fallback 1 | Fallback 2 | Build script | Notes |
|---|---|---|---|---|---|---|---|
| 17 | `emissions.upstream_o2_type` | `str` | TecDoc part-level lookup (`prd` + `passanger_car_pds`) | YAML | — | `tools/build_vref_db.py` | Contract §8 values: `NARROWBAND`, `WIDEBAND_AFR`, `WIDEBAND_LAMBDA`, `NONE` |
| 18 | `emissions.downstream_o2_present` | `bool` | TecDoc part-level lookup | YAML | — | `tools/build_vref_db.py` | `true` for Euro 3+ vehicles; `false` for most Euro 1-2 |
| 19 | `emissions.egr_equipped` | `bool` | TecDoc part-level lookup (`prd` + `passanger_car_pds`, assembly group "Рециркуляция ОГ") | YAML | — | `tools/build_vref_db.py` | See TECDOC_VIN_MAPPING.md Subsystem 4 for EGR query |

### A.4 Derived / polymorphic switch fields

| # | Field | Type | Derivation | Compute location | Notes |
|---|---|---|---|---|---|
| 22 | `air_metering_strategy` | `str` | `has_maf_sensor` + `has_map_sensor` → strategy enum | `vinlab/overlay/switches.py` | Contract §6.2 mapping: both=true→`DUAL_MAF_MAP_CROSSCHECK`, MAF-only→`MAF_ONLY`, MAP-only→`MAP_ONLY_SPEED_DENSITY` |
| 23 | `resolved_horizon` | `str` | `euro_emission_category` → `Horizon` enum | `vinlab/overlay/horizon.py` | Contract §6.4: EURO_1-2→HORIZON_LEGACY, EURO_3-4→ADAPTIVE, EURO_5-7→MODERN |
| 24 | `valvetrain_type` | `str` | TecDoc `ValveManagement` + `CylinderConstruction` | `tools/build_vref_db.py` | Inferred from DOHC + hydraulic lifter → `VVT`; SOHC may have VVT; OHV unlikely VVT |

---

## Section B — CSV column coverage

Source file: `C:\Users\muto\claude\4DApp\vehicle-data\petrol_vin\vehicles_petrol_specimens.csv`
Size: 50K+ Slovenian-market petrol VINs with full CoC measurements and registration dates.

### B.1 Columns persisted into `vref.db`

| CSV column | Description | Maps to VinDNA field(s) |
|---|---|---|
| `B_first_reg_date` | First registration date | `model_year` (fallback), WMI `era_hint` source |
| `D1_make` | Manufacturer brand name | `make` (fallback) |
| `D2_factory_designation` | Factory model code | `model` (fallback) |
| `D3_commercial_name` | Commercial model name | `model` (primary) |
| `E_VIN` | 17-character VIN | WMI extraction, VDS extraction, decoder test corpus |
| `E1_id_code` | Vehicle ID / type code | VDS cross-reference |
| `J_cat_code` | Vehicle category code (e.g. M1) | Filter: passenger cars only |
| `J_cat_desc` | Vehicle category description | Filter validation |
| `P11_displacement_cc` | Engine displacement (cc) | `engine_displacement_liters` (primary) |
| `P13_fuel` | Fuel type label | Petrol-only filter gate |
| `P13_fuel_code` | Fuel type code | Petrol-only filter gate |
| `P14_rated_rpm` | Rated engine speed (RPM) | `stress_idle_rpm_target` reference |
| `P15_engine_code` | Engine code string | Join key to YAML / TecDoc |
| `U1_noise_stationary_dBA` | Stationary noise level | Not used in VinDNA (consumed by GASLab) |
| `U2_noise_rpm` | RPM at noise measurement | Not used in VinDNA |
| `U3_noise_driving_dBA` | Driving noise level | Not used in VinDNA |
| `V1_CO` | CO emission (g/km or %) | CoC reference value |
| `V2_HC` | HC emission | CoC reference value |
| `V3_NOx` | NOx emission | CoC reference value |
| `V4_HC_NOx` | Combined HC+NOx | CoC reference value |
| `V7_CO2` | CO2 emission (g/km) | CoC reference value |
| `V9_euro_class_full` | Full Euro class string | `euro_emission_category` (primary) |
| `V10_idle_rpm_low` | Low-idle RPM | CoC reference |
| `V101_CO_low_idle` | CO at low idle | CoC reference |
| `V102_oil_temp_low_idle` | Oil temp at low idle | CoC reference |
| `V11_idle_rpm_high` | High-idle RPM | CoC reference |
| `V111_CO_high_idle` | CO at high idle | CoC reference |
| `V112_lambda` | Lambda at high idle | CoC reference |
| `V113_oil_temp_high_idle` | Oil temp at high idle | CoC reference |
| `euro_label` | Short Euro label (e.g. "Euro 5") | `euro_emission_category` (primary; preferred over V9 for enum mapping) |
| `D42_country` | Country of registration | Filter: Slovenian-market vehicles |
| `D42_country_code` | Country code | Filter validation |

### B.2 Columns explicitly excluded

| Excluded column | Reason |
|---|---|
| `V5_particles_diesel` | Diesel-only — petrol scope excludes this |
| `V6_absorption_coeff_diesel` | Diesel-only |
| `V61_idle_rpm_diesel` | Diesel-only |
| `V62_max_rpm_diesel` | Diesel-only |
| `V63_oil_temp_diesel` | Diesel-only |
| `V8_fuel_consumption` | Not needed for VinDNA; fuel economy is out of scope |

---

## Section C — TecDoc reuse

This section confirms which TecDoc fields are used and links to the existing detailed mapping. Do **not** duplicate the full table/column/sample-value content from `TECDOC_VIN_MAPPING.md` here.

**Reference document:** `docs/TECDOC_VIN_MAPPING.md` (generated 2026-05-16 from live TecDoc 1Q2018 MySQL via MCP server).

**Database:** `tecdoc` @ 127.0.0.1:3306 (MySQL 8.4.9), ~1.6M rows. Accessed read-only via `mcp_server_mysql` MCP server at **build time only** by `tools/build_vref_db.py`.

### C.1 Fields sourced from TecDoc

| VinDNA field | TecDoc source table | TecDoc column/attribute | TECDOC_VIN_MAPPING section |
|---|---|---|---|
| `engine_displacement_liters` | `passanger_car_attributes` | `Capacity_Technical.displayvalue` | Subsystem 1 |
| `cylinder_count` | `passanger_car_attributes` | `NumberOfCylinders.displayvalue` | Subsystem 1 |
| `engine_configuration` | `engine_attributes` | `EngineConstruction.displayvalue` | Subsystem 1 |
| `number_of_banks` | (derived from `EngineConstruction`) | — | Subsystem 1 |
| `induction_type` | `engine_attributes` | `ChargeType.displayvalue` | Subsystem 2 |
| `fuel_delivery_type` | `passanger_car_attributes` / `engine_attributes` | `FuelMixture.displayvalue` | Subsystem 2 |
| `has_maf_sensor` | `prd` + `passanger_car_pds` (part-level) | Assembly group "Приготовление смеси" | Subsystem 2 |
| `has_map_sensor` | `prd` + `passanger_car_pds` (part-level) | `prd.id=161` (boost pressure sensor) | Subsystem 2 |
| `valvetrain_type` | `engine_attributes` | `ValveManagement.displayvalue` + `CylinderConstruction.displayvalue` | Subsystem 3 |
| `fuel_type` (petrol gate) | `passanger_car_attributes` / `engine_attributes` | `FuelType.displayvalue` / `EngineType.displayvalue` | Subsystem 3 |
| `upstream_o2_type` | `prd` + `passanger_car_pds` (part-level) | Assembly group "Приготовление смеси", lambda sensor products | Subsystem 4 |
| `egr_equipped` | `prd` + `passanger_car_pds` (part-level) | Assembly group "Рециркуляция ОГ" | Subsystem 4 |

| `euro_emission_category` | `engine_attributes` | `EmissionNorm.displayvalue` | Subsystem 4 |

### C.2 Key linkage tables

From `TECDOC_VIN_MAPPING.md` "Key Linkage Tables":

- **Vehicle → Engine:** `passanger_cars.id ← passanger_car_engines.id → engines.id`
- **Vehicle → Parts:** `passanger_cars.id ← passanger_car_pds.passangercarid → prd.id`
- **Engine attributes:** `passanger_car_engines.engineid → engine_attributes.engineid`

### C.3 Russian-to-English translation map

Build script `tools/build_vref_db.py` must translate these TecDoc Russian display values:

| TecDoc Russian | English / enum value |
|---|---|
| `"ряд"` | `I` (Inline) |
| `"V"` | `V` |
| `"оппозитный двигатель"` | `BOXER` |
| `"всасывающее устройство"` | `NATURALLY_ASPIRATED` |
| `"турбо/нагнетатель"` | `TURBOCHARGED` (inclusive) |
| `"турбонагнетатель"` | `TURBOCHARGED` |
| `"компрессор"` | `SUPERCHARGED` |
| `"Впрыскивание во впускной коллектор"` | `PORT_INJECTION` |
| `"Непосредственный впрыск"` | `GDI` |
| `"Карбюратор"` | `CARBURETOR` |
| `"бензин"` | `petrol` (fuel type gate) |
| `"Бензиновый двигатель"` | `petrol` (engine type gate) |
| `"Euro N"` (EmissionNorm) | `EURO_N` |

---

## Section D — vPIC extraction

**Source package:** [cardog-ai/corgi](https://github.com/cardog-ai/corgi) — TypeScript library that bundles NHTSA vPIC data into a compressed SQLite database (`vpic.lite.db.gz`, ~8MB compressed, ~40MB uncompressed). Downloaded once at build time from `https://corgi.cardog.io/vpic.lite.db.gz`.

**Build script:** `tools/import_vpic.py` — downloads, decompresses, and extracts needed tables into `vinlab/data/{wmi.csv, years.csv}` and feeds `tools/build_vds_map.py`.

### D.1 Inferred schema

The corgi project does not publish a standalone SQL schema file; its TypeScript source (`lib/db.ts`, `lib/decode.ts`, `lib/pattern.ts`) defines the query interface. Based on the corgi README API response shape, the SQLite database contains at minimum these logical tables/views:

| Logical table | Key columns | What VINLab extracts |
|---|---|---|
| **WMI table** | `wmi` (3-char), `manufacturer`, `make`, `country`, `region` | `make` (primary source) |
| **Year-code table** | `year_code` (1-char), `calendar_year` (int) | `model_year` (primary source) |
| **VDS-pattern table** | `wmi_pattern`, `vds_pattern`, `cylinders`, `displacement_liters`, `fuel_type` | `cylinder_count`, `engine_displacement_liters`, `fuel_delivery_type` (fallback) |
| **Manufacturer table** | `id`, `name`, `country` | Brand normalisation cross-reference |

**Extraction approach (`tools/import_vpic.py`):**

1. Download `vpic.lite.db.gz` from `https://corgi.cardog.io/vpic.lite.db.gz`.
2. Decompress to a temp SQLite file.
3. Attach and query with `sqlite3`:
   - `SELECT DISTINCT wmi, make, manufacturer, country FROM wmi_table` → `wmi.csv`
   - `SELECT DISTINCT year_code, calendar_year FROM year_table WHERE calendar_year BETWEEN 1980 AND 2030` → `years.csv`
4. Delete the temp SQLite file after extraction.

### D.2 Fields VINLab will NOT use from vPIC

| vPIC field | Reason excluded |
|---|---|
| `body_class` | Not needed for diagnostic engine |
| `drive_type` | Out of scope for petrol diagnostics |
| `gvwr` | Commercial vehicle attribute; petrol passenger cars only |
| `plant_city` / `plant_country` | Assembly plant not needed for diagnosis |
| `trim` | Cosmetic; no diagnostic relevance |
| `engine_model` (free-text) | Unreliable free-text field; use TecDoc + CSV for engine attributes |
| `doors` | Not diagnostic-relevant |

### D.3 vPIC limitations

- **Weak on European-market VINs:** NHTSA database is US-centric. Many European-manufacturer VINs (especially pre-2000) return `confidence: NONE` or partial results. This is why vPIC is fallback #2 for engine attributes and fallback #1 only for WMI (which has the broadest coverage).
- **Schema stability:** The corgi SQLite schema is an implementation detail of corgi — it may change between releases. `tools/import_vpic.py` must validate column existence at build time and fail with a clear message if the schema has changed. Pinning a specific corgi release version in `requirements.txt` is recommended.
- **The `L` year-code ambiguity:** vPIC's year-code table lists both 1990 and 2020 for position-10 character `L`. VINLab resolves this via the WMI `era_hint` column (built from `B_first_reg_date` in petrol CSV), not from vPIC.

---

## Section E — Manual YAML residue

**Source file:** `tools/vref_manual_overrides.yaml` (seeded from `C:\Users\muto\claude\4DApp\v2\4D-Diagnostic-Engine-v2\tools\vref_manual_overrides.yaml`).

**Role:** last-resort gap filler. Fields populated from YAML only when TecDoc and CSV both have no entry for the resolved `engine_code`.

### E.1 Fields where YAML is the only possible source

These are the tech-mask flags that TecDoc's `prd` part-level linkage may not cover. The v2 seed has 52 engine codes across 16 brands with these flags populated.

| Field | Coverage in YAML seed | Risk if absent |
|---|---|---|
| `has_maf_sensor` | Inferred from `o2_type` + induction era; not explicit in seed | Low — induction_type + era strongly predicts MAF presence |
| `has_map_sensor` | Inferred from `has_turbo`; not explicit in seed | Low — turbo vehicles virtually always have MAP |
| `fuel_delivery_type` | Inferred from `has_gdi` flag | Medium — pre-2000 European GDI vehicles are rare but exist |
| `egr_equipped` | Explicit `has_egr` in seed | Low — almost all petrol vehicles 1990-2020 have EGR |

| `upstream_o2_type` | Explicit `o2_type` (WB/NB) in seed | Low — inferrable from euro_norm |
| `euro_emission_category` | Explicit `euro_norm` in seed | Low — inferrable from model_year |

### E.2 Known YAML-only engine codes

The v2 seed covers 52 engine codes. Expected additions after build: rare Japanese-market engines (Mitsubishi GDI-era, Mazda rotary) and low-volume European manufacturers (Saab, Lancia, Rover) that may not appear in the Slovenian CSV.

### E.3 YAML structure (per entry)

```yaml
engines:
  - engine_code: EA111_1.2_TSI
    brand: VOLKSWAGEN
    displacement_cc: 1197
    euro_norm: euro5
    my_start: 2009
    my_end: 2015
    has_vvt: true
    has_gdi: true
    has_turbo: true
    is_v_engine: false
    has_egr: true

    o2_type: WB
    target_rpm_u2: 2500
    target_lambda_v112: 1.000
```

---

## Section F — Conflict resolution policy

When two build-time sources disagree on the same field for the same vehicle, the following precedence table resolves the conflict. This matches the decisions recorded in `CLAUDE_CODE_PROMPT.md` (user decisions, 2026-05-17).

### F.1 Per-field-group precedence

| Field group | Winner | Reason |
|---|---|---|
| **Basic attributes** (`make`, `model`, `model_year`, `euro_emission_category`) | 1. petrol CSV > 2. TecDoc > 3. vPIC | CSV is ground-truth (government CoC data); TecDoc is curated; vPIC is broad but US-centric |
| **Engine measurements** (`engine_displacement_liters`, `cylinder_count`) | 1. petrol CSV (`P11_displacement_cc`) > 2. TecDoc (`Capacity_Technical`) > 3. vPIC | CSV has exact cc values from CoC; TecDoc may round |
| **Tech-mask flags** (`has_maf_sensor`, `has_map_sensor`, `egr_equipped`, `upstream_o2_type`) | 1. TecDoc part-level lookup > 2. YAML | TecDoc part catalogue is specific to vehicle; YAML is per engine-code family |
| **Induction + fuel delivery** (`induction_type`, `fuel_delivery_type`) | 1. TecDoc > 2. YAML > 3. vPIC | TecDoc `ChargeType` and `FuelMixture` are vehicle-specific; YAML is engine-family; vPIC fuel field is unreliable |
| **Engine configuration** (`engine_configuration`, `number_of_banks`) | 1. TecDoc > 2. YAML | TecDoc `EngineConstruction` is vehicle-specific |
| **Derived fields** (`air_metering_strategy`, `primary_load_calculation`, `resolved_horizon`) | Computed from upstream fields at decode time — no source conflict possible | |
| **WMI → make** | 1. vPIC > 2. petrol CSV-derived > 3. TecDoc | vPIC has the broadest WMI coverage; CSV adds European brands vPIC misses |
| **Year code → calendar year** | 1. vPIC year-code table (corrected for `L` via WMI `era_hint`) > 2. petrol CSV `B_first_reg_date` | vPIC is canonical for position-10 mapping; CSV reg date is noisy (import lag) |

### F.2 Conflict resolution at build time

Build scripts (`tools/build_vref_db.py`, `tools/build_vds_map.py`) implement precedence as follows:

1. **Query all sources** for each VIN/engine_code combination.
2. **Populate the primary source field** if a value exists.
3. **Populate fallback 1** only if primary is NULL or marked as `UNKNOWN`.
4. **Populate fallback 2** only if both primary and fallback 1 are NULL/UNKNOWN.
5. **Log every conflict** to `build_conflicts.log` with the VIN, field, competing values, and which source won. This log is not shipped; it's a build-time audit trail.
6. **If all three sources are NULL**, set `confidence` to `NONE` for that decode and log a gap.

### F.3 No-conflict fields

The following fields have a single definitive source and cannot experience cross-source conflict:

- `vin` — caller input
- `stress_idle_rpm_target` — overlay rules only (derived post-decode)
- `confidence` — decoder internal computation
- `primary_load_calculation` — derived from MAF/MAP booleans
- `air_metering_strategy` — derived from MAF/MAP booleans
- `resolved_horizon` — derived from `euro_emission_category`

