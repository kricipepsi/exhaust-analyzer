# OBDLab Module Wiki

**Module:** `obd_live_lab` | **Version:** 5.0 (2026-05-18) | **Scope:** Petrol OBD-II, 1990–2020

**Purpose:** single-source operational reference for the OBDLab module — validation rules, computation logic, enum declarations, alias normalization, and diagnostic knowledge graph for KG ingestion.

**Anchored to:**
- `COMLab/docs/wiki/OBD_VOCABULARY.md` — canonical cross-lab OBD vocabulary (PIDs, RPM bands, fault families, decision tree). **Do not duplicate here.**
- `COMLab/docs/wiki/SEMANTIC_CONTRACT.md §4.4` — `OBDLivePayload` JSON schema (canonical output contract)
- `COMLab/docs/wiki/DTC_VOCABULARY.md` — DTC taxonomy, routing tags, Mode 06 structure
- `OBDLab/bp/OBDlab.md` — module implementation blueprint

> **Measurement convention used throughout this wiki:**
> - **Stabilised Idle (SI):** 650–900 RPM, warm, closed-loop, no accessory load.
> - **Stress Idle (StI):** VIN-derived RPM (~4000 RPM typical), steady no-load in-bay rev — emitted by VINLab as `stress_idle_rpm_target`. **Replaces "2500 RPM"** as the second measurement point used in earlier drafts. See `OBD_VOCABULARY.md §3.2`.

---

## 1. Standards anchored

| Standard | Scope | Used here for |
|---|---|---|
| **SAE J1979 / J1979DA** | OBD-II PID definitions, Mode 01/02 | PID canonical names, units, ranges |
| **SAE J2012 / J2012DA** | DTC structure and definitions | See `DTC_VOCABULARY.md` |
| **ISO 15031-5 / 15031-6** | International OBD-II equivalents | EU vehicle compatibility |
| **ISO 14229 (UDS)** | Unified Diagnostic Services — Mode 06 | Monitor preconditions, MID/TID structure |

---

## 2. Module architecture

### 2.1 Processing sequence

```
[User UI / Form Input]
        │
        ▼
[1] pid_ingestion_validator.py        ← boundary checking + unit normalisation (§3)
        │
        ▼
[2] semantic_consistency_checker.py   ← physics contradiction detection (§4)
        │
        ▼
[3] sensor_signal_translator.py       ← lambda normalise, VE compute, trim vector (§10–12)
        │
        ▼
[OBDLivePayload JSON]  →  COMLab (SEMANTIC_CONTRACT §4.4)
```

**Rule:** OBDLab produces only JSON. No Python objects cross the lab boundary. `SEMANTIC_CONTRACT §4.4` is the authoritative output schema.

### 2.2 Directory structure

```
obd_live_lab/
├── core/
│   ├── pid_ingestion_validator.py
│   │   ├── Manual_Input_Data_Typing_Gate        — validates entries against §3 bounds
│   │   └── Unit_Normalizer_Converter            — psi→kPa, °F→°C, in Hg→kPa
│   ├── semantic_consistency_checker.py
│   │   ├── Sensor_Contradiction_Evaluator       — §4 Physics Gates 1–4
│   │   └── Loop_Status_Sanity_Gate              — §4.2 thermal + closed-loop check
│   └── sensor_signal_translator.py
│       ├── Wideband_Lambda_Normalizer           — §11 O₂ normalisation
│       └── Trim_Vector_Aggregator               — §12 TFT computation
└── config/
    ├── physical_sensor_bounds.json              — §3 boundary constraints
    └── obd_translation_rules.yaml              — translation lookups per Horizon
```

### 2.3 Python class API (key signatures)

```python
class PIDIngestionValidator:
    def __init__(self, config_path: str):
        # loads physical_sensor_bounds.json

    def validate_and_convert(self, raw_user_inputs: dict) -> dict:
        # raises ValueError on bounds violation
        # returns unit-normalised dict

class SemanticConsistencyChecker:
    @staticmethod
    def assert_sensor_logic(sanitized_pids: dict) -> bool:
        # raises SemanticConsistencyError on Physics Gate violation
        # returns True if all gates pass

class SensorSignalTranslator:
    @staticmethod
    def translate_signals(sanitized_pids: dict) -> dict:
        # computes total_trim_correction_delta, calculated_ve, normalized_obd_lambda
        # returns enriched dict → serialised to OBDLivePayload
```

---

## 3. Input validation — physical sensor bounds

### 3.1 Boundary rules (`config/physical_sensor_bounds.json`)

Values outside these bounds raise `ValueError` and block all downstream processing.

| Field | Min | Max | Unit | Note |
|---|---|---|---|---|
| `engine_rpm` | 0 | 8000 | RPM | |
| `coolant_temp_c` | −40 | 140 | °C | |
| `calculated_engine_load_pct` | 0 | 100 | % | |
| `mass_airflow_gps` | 0 | 655.35 | g/s | |
| `manifold_vacuum_kpa` | 0 | 255 | kPa | Absolute pressure, not gauge |
| `shrtft1` | −100.0 | +99.22 | % | Bank 1 |
| `longft1` | −100.0 | +99.22 | % | Bank 1 |
| `shrtft2` | −100.0 | +99.22 | % | Only validated when `number_of_banks == 2` |
| `longft2` | −100.0 | +99.22 | % | Only validated when `number_of_banks == 2` |
| `intake_air_temp_c` | −40 | 80 | °C | |
| `throttle_pos_pct` | 0 | 100 | % | |
| `control_module_voltage_v` | 0 | 18 | V | |


**Contract rule:** `shrtft2` and `longft2` must be `null` (not `0.0`) when `number_of_banks == 1`. Emitting `0.0` for absent bank fields is a `SEMANTIC_CONTRACT` violation.

### 3.2 Unit normalisation

| User input unit | Normalised to | Conversion factor |
|---|---|---|
| °F | °C | `(F − 32) × 5/9` |
| psi | kPa | `× 6.895` |
| in Hg | kPa | `× 3.386` |
| lb/min | g/s | `× 7.559` |

---

## 4. Semantic consistency rules (Physics Gates)

Enforced by `semantic_consistency_checker.py`. Run after §3 validation, before §10–12 computation.

| Rule ID | Trigger condition | Error raised | Rationale |
|---|---|---|---|
| `Physics_Gate_1` | `VSS > 10 km/h AND engine_rpm < 400` | `SemanticConsistencyError: vehicle moving, engine stalled` | Vehicle cannot roll at speed with a stalled engine |
| `Physics_Gate_2` | `coolant_temp_c ≥ 80 AND fuel_sys_status == "Open_Loop_Cold"` | `SemanticConsistencyError: closed loop should be active at engine temperature` | ECU must enter closed loop by ~70 °C |
| `Physics_Gate_3` | `calculated_ve > 90% AND induction_type == "NATURALLY_ASPIRATED" AND rpm_state_bucket == "STABILIZED_IDLE"` | `SemanticConsistencyError: VE exceeds physical limit for NA engine at idle` | NA engines cannot exceed 90% VE at idle |
| `Physics_Gate_4` | `shrtft1 < −100 OR shrtft1 > 99.22` (or same for `longft1`) | `ValueError: input breaks safety limits` | Redundant check — also caught in §3 |

### 4.1 Thermal gate

```
gate_thermal_stabilization:
  source:    coolant_temp_c
  condition: coolant_temp_c < 75
  action:    FREEZE — set rpm_state_bucket = COLD_OPEN_LOOP_INVALID
             block ALL downstream trim, lambda, VE analytics
             propagate: engine_warmed = false
```

### 4.2 Closed-loop sanity gate

```
gate_closed_loop:
  source:    fuel_sys_status
  condition: fuel_sys_status != "Closed_Loop" AND coolant_temp_c >= 75
  action:    flag open_loop_invalid
             mark trim analytics as suspect — do NOT block payload emission
             propagate lower confidence to COMLab
```

---

## 5. OBDLivePayload — canonical output schema

The JSON shape OBDLab emits to COMLab. Defined authoritatively in `SEMANTIC_CONTRACT.md §4.4`. Reproduced here for module-internal reference only.

```jsonc
{
  "engine_warmed": true,                    // bool: coolant_temp_c >= 70
  "rpm_state_bucket": "STRESS_IDLE",        // RpmStateBucket enum — see §6.1
  "engine_rpm": 4500,                       // int: raw RPM
  "coolant_temp_c": 92,                     // float: °C
  "calculated_engine_load_pct": 55,         // float: 0–100 %
  "mass_airflow_gps": 12.5,                 // float: g/s (null if MAP_ONLY routing)
  "manifold_vacuum_kpa": 68,                // float: kPa (null if MAF_ONLY routing)
  "shrtft1": -10.0,                         // float: % Bank 1 STFT
  "longft1": -25.0,                         // float: % Bank 1 LTFT
  "shrtft2": null,                          // float | null: Bank 2 STFT (null if banks == 1)
  "longft2": null,                          // float | null: Bank 2 LTFT (null if banks == 1)
  "total_trim_correction_delta": -35.0,     // float: shrtft1 + longft1
  "normalized_obd_lambda": 0.85,            // float: 0.7–1.3 unified lambda
  "freeze_frame_pids": { }                  // see DTC_VOCABULARY §17
}
```

**Fields NOT emitted** (internal computation only):

| Internal field | Why not emitted | Exposed as |
|---|---|---|
| `calculated_ve` | Internal cross-check only | `ve_state_isValid` (bool) |
| `ve_routing_mode` | Internal VERoutingMode enum | Not exposed |
| `o2_normalization_mode` | Internal O2NormalizationMode enum | Not exposed |
| `trim_analytics_gate` | Internal gate state | Not exposed; affects COMLab confidence path |

---

## 6. OBDLab enum declarations

### 6.1 RpmStateBucket — see `SEMANTIC_CONTRACT.md §8`

```python
class RpmStateBucket(StrEnum):
    STABILIZED_IDLE         = "STABILIZED_IDLE"         # 650–900 RPM, load < 30%
    REGULATORY_HIGH_IDLE    = "REGULATORY_HIGH_IDLE"    # 2200–2800 RPM — regulatory 2-speed idle test
    STRESS_IDLE             = "STRESS_IDLE"             # VIN-derived 3000–4500 RPM, no-load clinical test
    COLD_OPEN_LOOP_INVALID  = "COLD_OPEN_LOOP_INVALID"  # ECT < 75 °C — freeze all analytics
```

**History:** `REGULATORY_HIGH_IDLE` was `HIGH_IDLE_LOAD` in OBDLab BP early drafts. `STRESS_IDLE` is the new clinical measurement point superseding the old "2500 RPM" second measurement. See `OBD_VOCABULARY.md §3`.

### 6.2 VERoutingMode — OBDLab-internal

```python
class VERoutingMode(StrEnum):
    DUAL_MAF_MAP_CROSSCHECK  = "DUAL_MAF_MAP_CROSSCHECK"  # both sensors: standard formula
    MAP_ONLY_SPEED_DENSITY   = "MAP_ONLY_SPEED_DENSITY"   # no MAF — emulate from MAP + RPM + Disp
    MAF_ONLY                 = "MAF_ONLY"                 # no MAP — back-calculate MAP from MAF
```

Maps 1-to-1 to `AirMeteringStrategy` (`OBD_VOCABULARY.md §4.2`). `VERoutingMode` is the OBDLab-internal execution view; `AirMeteringStrategy` is the cross-lab vocabulary term. They always agree.

### 6.3 O2NormalizationMode — OBDLab-internal

```python
class O2NormalizationMode(StrEnum):
    NARROWBAND_VOLTAGE_TO_LAMBDA       = "NARROWBAND_VOLTAGE_TO_LAMBDA"       # 0.1–0.9 V → lambda mapping
    WIDEBAND_PASSTHROUGH               = "WIDEBAND_PASSTHROUGH"                # direct lambda/AFR value
    WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA  = "WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA"  # WB sensor, NB sim output → 3-zone mapping
```

Driven by `VinDNA.upstream_o2_type`. See §11.

### 6.4 VEValidity — OBDLab-internal

```python
class VEValidity(StrEnum):
    VALID                    = "VALID"
    FAULT_VE_IDLE_COLLAPSE   = "FAULT_VE_IDLE_COLLAPSE"   # VE < 50% at STABILIZED_IDLE
    FAULT_MAF_CONTAMINATION  = "FAULT_MAF_CONTAMINATION"  # VE < 65% at STRESS_IDLE + positive TFT
    FAULT_VE_SENSOR_SKEW     = "FAULT_VE_SENSOR_SKEW"     # VE > 85% at idle on NA engine
    UNKNOWN                  = "UNKNOWN"                  # insufficient inputs to compute
```

### 6.5 TrimAnalyticsGate — OBDLab-internal

```python
class TrimAnalyticsGate(StrEnum):
    VALID                   = "VALID"
    ENGINE_COLD             = "ENGINE_COLD"             # coolant_temp_c < 70
    OPEN_LOOP               = "OPEN_LOOP"               # fuel_sys_status != Closed_Loop
    O2_FAULT_ACTIVE         = "O2_FAULT_ACTIVE"         # active P0130–P0161
    CKP_CMP_FAULT_ACTIVE    = "CKP_CMP_FAULT_ACTIVE"    # active P0335 / P0340
    CODES_RECENTLY_CLEARED  = "CODES_RECENTLY_CLEARED"  # < 1 drive cycle since codes_cleared
    WOT_ACTIVE              = "WOT_ACTIVE"              # throttle at wide-open
    DFCO_ACTIVE             = "DFCO_ACTIVE"             # decel fuel cut-off
    SEMANTIC_ERROR          = "SEMANTIC_ERROR"          # Physics Gate violation (§4)
```

### 6.6 NodeSensorStatus — OBDLab-internal

```python
class NodeMAFStatus(StrEnum):
    REAL_SENSOR_FEED   = "REAL_SENSOR_FEED"    # MAF sensor physically present and reading
    VIRTUAL_EMULATION  = "VIRTUAL_EMULATION"   # MAP_ONLY route — MAF value is computed

class NodeMAPStatus(StrEnum):
    REAL_SENSOR_FEED   = "REAL_SENSOR_FEED"    # MAP sensor physically present and reading
    BACK_CALCULATED    = "BACK_CALCULATED"     # MAF_ONLY route — MAP value is inferred
```

### 6.7 O2FailureMode — OBDLab-internal

```python
class O2FailureMode(StrEnum):
    STUCK_LEAN          = "STUCK_LEAN"          # pinned < 0.2 V (narrowband)
    STUCK_RICH          = "STUCK_RICH"          # pinned > 0.85 V (narrowband)
    SLUGGISH            = "SLUGGISH"            # rise/fall time > 100 ms
    DEAD                = "DEAD"                # no voltage activity
    WRONG_CENTERLINE    = "WRONG_CENTERLINE"    # bias drift from 0.45 V stoich centre
    HEATER_FAULT        = "HEATER_FAULT"        # heater resistance outside 4–14 Ω
```

---

## 7. Alias normalization table

Maps names used across source documents to their canonical JSON field in `OBDLivePayload`, with the authoritative reference for each.

| OBDLab BP / wiki alias | Canonical JSON field | Authority | SAE J1979 PID |
|---|---|---|---|
| `pid_engine_speed` | `engine_rpm` | OBD_VOCAB §2 | `010C` |
| `pid_engine_coolant_temp` / ECT | `coolant_temp_c` | OBD_VOCAB §2 | `0105` |
| `pid_engine_load` / Calculated Load | `calculated_engine_load_pct` | OBD_VOCAB §2 | `0104` |
| `pid_mass_airflow` / MAF | `mass_airflow_gps` | OBD_VOCAB §2 | `0110` |
| `pid_manifold_absolute_pressure` / MAP | `manifold_vacuum_kpa` | OBD_VOCAB §2 | `010B` |
| `pid_short_term_fuel_trim` / STFT | `shrtft1` (Bank 1) | OBD_VOCAB §2 | `0106` |
| `pid_long_term_fuel_trim` / LTFT | `longft1` (Bank 1) | OBD_VOCAB §2 | `0107` |
| STFT Bank 2 | `shrtft2` | OBD_VOCAB §2 | `0108` |
| LTFT Bank 2 | `longft2` | OBD_VOCAB §2 | `0109` |
| `calculated_total_fuel_trim` / TFT | `total_trim_correction_delta` | OBD_VOCAB §2 | (derived) |
| `resolved_obd_lambda` / `normalized_obd_lambda` | `normalized_obd_lambda` | OBD_VOCAB §5 | (derived) |
| `calculated_ve` | (internal only — not emitted) | OBD_VOCAB §5 | (derived) |
| `current_engine_state_bucket` (old BP name) | `rpm_state_bucket` | SEMANTIC_CONTRACT §8 | — |
| `HIGH_IDLE_LOAD` (superseded) | `REGULATORY_HIGH_IDLE` in `RpmStateBucket` | OBD_VOCAB §3.1 | — |
| stress idle / ~4000 RPM second measurement | `STRESS_IDLE` in `RpmStateBucket` | OBD_VOCAB §3.2 | — |
| `air_metering_strategy` (OBDLab BP) | `air_metering_strategy` (in VinDNA) | OBD_VOCAB §4.2 | — |
| `upstream_o2_sensor_type` (OBDLab BP) | `upstream_o2_type` (in VinDNA) | SEMANTIC_CONTRACT §6.3 | — |
| `has_turbocharged_induction` (OBDLab BP) | `induction_type == "TURBOCHARGED"` (in VinDNA) | SEMANTIC_CONTRACT §8 | — |
| stress idle RPM target | `stress_idle_rpm_target` (in VinDNA) | OBD_VOCAB §4.4 | — |

**Disambiguation:** `manifold_vacuum_kpa` is **absolute pressure in kPa**, not negative gauge pressure. Low kPa = high vacuum. Normal warm idle: 25–35 kPa (≈18–22" Hg at sea level).

---

## 8. Engine state bucketing

### 8.1 Bucket definitions

See `OBD_VOCABULARY.md §3.3` for the authoritative table.

| `rpm_state_bucket` | RPM band | Load | Analytics |
|---|---|---|---|
| `STABILIZED_IDLE` | 650–900 | < 30% | Full — primary diagnosis state |
| `REGULATORY_HIGH_IDLE` | 2200–2800 | 15–40% | Regulatory baseline (cases corpus) |
| `STRESS_IDLE` | VIN-derived 3000–4500 | 40–60% | Clinical load test — exposes load-dependent faults |
| `COLD_OPEN_LOOP_INVALID` | any | any | All analytics frozen (§4.1) |

### 8.2 YAML bucketing rules (`obd_translation_rules.yaml`)

```yaml
state_bucketing_rules:
  - bucket_id: "STABILIZED_IDLE"
    conditions:
      - node: "engine_rpm"
        operator: "BETWEEN"
        value: [650, 900]
      - node: "calculated_engine_load_pct"
        operator: "LESS_THAN"
        value: 30.0

  - bucket_id: "STRESS_IDLE"
    conditions:
      - node: "engine_rpm"
        operator: "APPROXIMATELY"
        value: "stress_idle_rpm_target"    # per-vehicle value from VinDNA
        tolerance_pct: 10
      - node: "calculated_engine_load_pct"
        operator: "BETWEEN"
        value: [10.0, 60.0]
    notes: "Supersedes former HIGH_IDLE_LOAD at 2200-2600 RPM"

  - bucket_id: "COLD_OPEN_LOOP_INVALID"
    conditions:
      - node: "coolant_temp_c"
        operator: "LESS_THAN"
        value: 75.0
    priority: 1    # evaluated first regardless of RPM
```

### 8.3 `STRESS_IDLE` RPM per VIN

`stress_idle_rpm_target` is emitted by VINLab and consumed by OBDLab. OBDLab uses it to define the `STRESS_IDLE` bucket window and to prompt the technician for the correct RPM to hold. See `OBD_VOCABULARY.md §3.2` for the per-Euro-tier example table.

---

## 9. Analytics preconditions

Before running any fuel-trim, lambda, or catalyst analytics, ALL gates must return `VALID`. Failed gates flag a `TrimAnalyticsGate` enum value; OBDLab still emits the payload but `ve_state_isValid = false`.

| Gate | Condition for VALID | Gate enum on fail |
|---|---|---|
| Engine warm | `coolant_temp_c ≥ 70` | `ENGINE_COLD` |
| Closed loop | `fuel_sys_status == "Closed_Loop"` | `OPEN_LOOP` |
| No O₂ fault | No active P0130–P0161 | `O2_FAULT_ACTIVE` |
| No CKP/CMP fault | No active P0335 / P0340 | `CKP_CMP_FAULT_ACTIVE` |
| Codes not recently cleared | ≥ 1 drive cycle since `codes_cleared` | `CODES_RECENTLY_CLEARED` |
| Not WOT | Throttle not at wide-open | `WOT_ACTIVE` |
| Not DFCO | Decel fuel cut not active | `DFCO_ACTIVE` |
| Semantic gates pass | §4 Physics Gates 1–4 all pass | `SEMANTIC_ERROR` |

---

## 10. VE computation

### 10.1 Formula (Speed-Density Ideal Gas)

```
VE (%) = [MAF(g/s) × 28.97 × (IAT(°C) + 273.15)]
         ──────────────────────────────────────────── × 100
         [MAP(kPa) × (RPM/60) × (Displacement(L)/2) × 8.314]
```

**Inputs:** `mass_airflow_gps`, `intake_air_temp_c`, `manifold_vacuum_kpa`, `engine_rpm`, `engine_displacement_liters` (from VinDNA).

`calculated_ve` is an **internal sensor cross-check** — it is not emitted. `ve_state_isValid` (bool) carries the result.

### 10.2 Polymorphic routing (by VERoutingMode)

```
  VinDNA: air_metering_strategy
                │
    ┌───────────┼──────────────────────────┐
    ▼                   ▼                  ▼
DUAL_MAF_MAP       MAP_ONLY           MAF_ONLY
CROSSCHECK         SPEED_DENSITY
    │                   │                  │
Standard VE        Emulate MAF        Back-calc MAP
formula (§10.1)    from MAP+RPM+Disp  from MAF+RPM+Disp

MAF status:   REAL_SENSOR_FEED   VIRTUAL_EMULATION   REAL_SENSOR_FEED
MAP status:   REAL_SENSOR_FEED   REAL_SENSOR_FEED    BACK_CALCULATED
```

**MAP_ONLY emulation:**
```
Emulated_MAF = (MAP × RPM × Displacement) / (2 × R × IAT_K) × (target_VE / 100)
```

**MAF_ONLY back-calculation:**
```
Inferred_MAP = (MAF × R × IAT_K) / (RPM × Displacement / 2)
```

### 10.3 VE validation triggers

| State | Target VE | Low trigger | High trigger |
|---|---|---|---|
| `STABILIZED_IDLE` | 60–75% | `< 50%` → `FAULT_VE_IDLE_COLLAPSE` (structural exhaust restriction) | `> 85%` on NA engine → `FAULT_VE_SENSOR_SKEW` (calibration error) |
| `STRESS_IDLE` | 75–85% | `< 65%` AND TFT `> +15%` → `FAULT_MAF_CONTAMINATION` | `> 95%` → forced induction suspected |

### 10.4 Sub-module YAML config

```yaml
version: "3.1"
sub_module_id: "obd_ve_calc_engine"
dependencies:
  inputs:
    - "obd_live_lab:mass_airflow_gps"
    - "obd_live_lab:manifold_vacuum_kpa"
    - "obd_live_lab:engine_rpm"
    - "obd_live_lab:intake_air_temp_c"
  context:
    - "vin_dna:engine_displacement_liters"
    - "vin_dna:induction_type"
execution_loop:
  formula: "((MAF * 28.97 * (IAT + 273.15)) / (MAP * (RPM / 60) * (Displacement / 2) * 8.314)) * 100"
```

---

## 11. O₂ Normalisation

  §11.1 Narrowband → lambda (NARROWBAND_VOLTAGE_TO_LAMBDA)
  §11.2 Wideband passthrough (WIDEBAND_PASSTHROUGH)
  §11.3 Wideband-NB-sim → lambda (WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA)

OBDLab outputs a single `normalized_obd_lambda` regardless of upstream sensor technology. Routing driven by `VinDNA.upstream_o2_type`.

### 11.1 Narrowband → lambda (NARROWBAND_VOLTAGE_TO_LAMBDA)

```
Input: pid_o2_sensor_voltage_b1s1 (0.1 – 0.9 V)

  Voltage 0.10 – 0.40 V  →  LEAN_STATE        →  normalized_obd_lambda ≈ 1.05
  Voltage 0.41 – 0.49 V  →  STOICH_APPROACH   →  normalized_obd_lambda = 1.00
  Voltage 0.50 V          →  STOICHIOMETRIC    →  normalized_obd_lambda = 1.00
  Voltage 0.51 – 0.59 V  →  STOICH_RICH_SIDE  →  normalized_obd_lambda = 1.00
  Voltage 0.60 – 0.90 V  →  RICH_STATE        →  normalized_obd_lambda ≈ 0.95

Output: normalized_obd_lambda
```

Narrowband numerical thresholds for pattern matching (see `OBD_VOCABULARY.md §12.1` for full table):

| Metric | Healthy range | Failure signature |
|---|---|---|
| Stoichiometric centre | ~0.45 V | Drift = `WRONG_CENTERLINE` bias |
| Cross-counts at StI | ≥ 8 per 10 s | < 8 = `SLUGGISH` |
| Switching frequency (MPI) | 2–5 Hz | < 0.5 Hz = `SLUGGISH` / `DEAD` |
| Rise time | < 100 ms | > 100 ms = `SLUGGISH` |

### 11.2 Wideband passthrough (WIDEBAND_PASSTHROUGH)

```
Input: pid_wideband_equivalence_ratio (direct lambda/AFR value from ECU)

  Transformation: PASS_THROUGH_DIRECT_VALUE
  — wideband PIDs stream linear lambda directly; no conversion needed

Output: normalized_obd_lambda = pid_wideband_equivalence_ratio
```

### 11.3 Wideband-in-NB-simulation (WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA)

```
Input: pid_oxygen_sensor_volts (0–1 V simulated NB signal from aftermarket WB controller)

  Transformation: 3-ZONE_VOLTAGE_TO_LAMBDA (same mapping as §11.1)
  — Physically a wideband sensor; ECU sees 0–1 V simulated NB signal
  — Mode differs from NARROWBAND_VOLTAGE_TO_LAMBDA so COMLab
    TrimAnalyticsGate can apply WB-sim trim weight coefficient

Output: (lambda, O2NormalizationMode.WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA)
```

### 11.4 Sensor bias detection rule

| Narrowband reads | Wideband reads | Conclusion | `ChemicalSignature` |
|---|---|---|---|
| Lean (< 0.4 V) | Rich (λ < 0.95) | Narrowband biased LOW — ECU adds fuel on false-lean signal | `O2_SENSOR_BIASED_LOW` |
| Rich (> 0.6 V) | Lean (λ > 1.05) | Narrowband biased HIGH — ECU pulls fuel on false-rich signal | `O2_SENSOR_BIASED_HIGH` |
| Normal switching | `|obd_lambda − gas_lambda| ≥ 0.08` | `perception_contradiction` — suspect catalyst or probe | — |

---

## 12. Trim vector computation

### 12.1 Total Fuel Trim (TFT)

```
total_trim_correction_delta    = shrtft1 + longft1    (Bank 1)
total_trim_correction_delta_b2 = shrtft2 + longft2    (Bank 2 — V engines only)
```

**Sentinels:**
- `±10%` total: healthy operating range
- `±25%`: ECU DTC trigger threshold (P0171 / P0172 / P0174 / P0175)
- `±127%`: register saturation — any magnitude beyond ±25% is diagnostically floor/ceiling; the exact number is meaningless

### 12.2 STFT/LTFT delta rules

See `OBD_VOCABULARY.md §18` for the full canonical rules. Summary:

| STFT sign | LTFT sign | Condition |
|---|---|---|
| Opposite to LTFT | Retained from past | **Fault recently repaired / healing.** ECU reversing a learned correction. |
| Same as LTFT | Similar magnitude | **Fault active and severe.** Both immediate and adaptive corrections agree on direction. |

### 12.3 Bank comparison (V engines)

See `OBD_VOCABULARY.md §18.3`. Summary:

| Pattern | Interpretation |
|---|---|
| One bank drifts, other normal | Single-bank fault (intake gasket, injector, pre-cat exhaust leak that side) |
| Both banks drift same direction | Common-mode fault (fuel pump, MAF contamination, EVAP/EGR) |
| Banks drift opposite directions | Sensor fault on ≥ 1 bank, or exhaust crossover/swap |

---

## Domain reference — Fuel trim diagnostics (from `master_fuel_trim_guide.md`)

**Cross-reference:** `OBD_VOCABULARY.md §11` covers normal ranges, RPM-dependence decision tree, truth-vs-perception cross-check, and full precondition list. This section adds OBDLab-specific supplementary techniques.

### Trim-pattern RPM-dependence decision tree

```
Measure TFT at STABILIZED_IDLE (SI) and STRESS_IDLE (StI).
RPM-dependence is the primary fault discriminator.

  SI trim POSITIVE (> +10%)
    │
    ├─ Drops toward normal at StI         → VACUUM LEAK
    │                                        (constant-volume unmetered air; diluted
    │                                        at StI by high airflow mass)
    │
    ├─ Worsens at StI (> +25%)            → FUEL DELIVERY fault
    │                                        (pump / filter / regulator can't keep up)
    │
    └─ Positive at SI, NEGATIVE at StI    → MAF UNDER-READING
                                             (contaminated hot-wire: over-reads at low
                                             velocity, under-reads at high velocity)

  SI trim NEGATIVE (< −10%)
    │
    ├─ One bank only, persists across RPM → LEAKING INJECTOR (that bank)
    │
    ├─ Coincides with EVAP purge duty     → EVAP CANISTER SATURATED / stuck-open purge
    │
    ├─ Worsens with RPM, high vacuum      → HIGH FUEL PRESSURE (regulator)
    │
    └─ High MAP at idle, clears at StI   → EGR STUCK OPEN
                                             (dilutes charge at idle; EGR authority
                                             drops with higher airflow at StI)

  Both trims near zero
    │
    └─ MAF reads high for RPM             → MAF OVER-READING
```

### Supplementary trim techniques

**EVAP canister pinch test:** Pinch the purge line at idle. If trims shift positive (lean) immediately, purge was contributing a rich offset — saturated canister confirmed.

**Propane enrichment snap test (vacuum leak confirmation):** With trims high positive at idle, introduce propane around the intake. Trims momentarily drop and settle → unmetered air location confirmed.

**Snap throttle O₂ test:** Rapid throttle snap → narrowband O₂ voltage should dive lean then snap rich. Delayed response (> 100 ms) = `SLUGGISH` sensor.

---

## Domain reference — O₂ sensor diagnostics (from `master_o2_sensor_guide.md`)

**Cross-reference:** `OBD_VOCABULARY.md §12` covers numerical thresholds, wideband specs, and failure taxonomy. This section adds OBDLab-specific context.

### Sensor position canonical names

```
B1S1  =  Bank 1, upstream (pre-cat — primary feedback sensor)
B1S2  =  Bank 1, downstream (post-cat — catalyst monitor)
B2S1  =  Bank 2, upstream
B2S2  =  Bank 2, downstream
```

### Pre-cat ↔ post-cat switching ratio (catalyst masking)

If rear (B1S2) cross-count rate ≥ 0.5 × front (B1S1) → suspect **catalyst failure** before the rear sensor. A healthy catalyst stores oxygen and suppresses rear switching. Vigorous rear switching = catalyst has lost OSC (oxygen storage capacity).

### DTC families by sensor position

| DTC range | Position | Fault type |
|---|---|---|
| P0130–P0137 | B1S1 | Circuit / signal range |
| P0138–P0145 | B1S2 | Circuit / signal range |
| P0150–P0167 | B2S1 / B2S2 | Circuit / signal range |
| P0030 / P0036 / P0050 / P0056 | All | Heater control circuit |
| P2A00–P2A03 | B1S1–B2S2 | Wideband-specific AFR sensor fault |

---

## Domain reference — Catalyst diagnostics (from `master_catalyst_guide.md`)

### TWC operating envelope

| Parameter | Value |
|---|---|
| Lambda window for conversion | 0.97 – 1.03 |
| Light-off temperature | ~250 – 300 °C |
| Misfire damage threshold | > 1 % of combustion events |

### Catalyst monitor enable conditions

- ECT ≥ 70 °C — steady 2000–3000 RPM — closed loop
- No active P0300–P0312 (misfires would damage the catalyst)
- No active P0171 / P0172 / P0174 / P0175 (mixture imbalance confounds reading)
- ≥ 1 drive cycle since `codes_cleared`

> **Freeze-frame flag:** If freeze-frame ECT for P0420 < 70 °C → flag `dtc_set_outside_enable_window` and demote catalyst-failure candidate.

### P0420 diagnosis sequence

```
Step 1  Confirm ECT ≥ 70 °C at DTC set time (freeze-frame ECT)
Step 2  Check for active misfire or trim DTC — resolve primary fault first
Step 3  Live downstream O₂: flat/slow = catalyst working; active switching = catalyst dead
Step 4  Switching ratio: rear cross-count ≥ 0.5 × front → replace catalyst
Step 5  Check for exhaust air leak upstream of rear O₂ sensor (false lean signal)
Step 6  Check for silicone or coolant contamination of rear O₂ sensor
Step 7  Check for aftermarket catalyst (genuine conversion but insufficient OSC for OBD monitor)
```

### False P0420 cluster

P0420 can set without genuine catalyst failure when: exhaust air leak upstream of B1S2 / silicone sensor contamination / aftermarket catalyst with low OSC / engine running rich (low O₂ throughput masks a dead catalyst — `Catalyst_Masking_Rich` pattern).

### Physical inspection thresholds

| Test | Pass | Fail |
|---|---|---|
| Idle backpressure | < 1.5 psi | ≥ 1.5 psi |
| 2500 RPM backpressure | < 3.0 psi | ≥ 3.0 psi |
| Snap-throttle peak backpressure | ≤ 5 psi | > 5 psi |
| IR delta (outlet − inlet) | ≥ 20 °C | < 20 °C = not converting |

---

## Domain reference — DTC classification (from `master_obd_guide.md`)

**Cross-reference:** `DTC_VOCABULARY.md` covers the full taxonomy, canonical regex, routing tags, freeze-frame fields, and Mode 06 structure. This section covers OBDLab-specific DTC handling rules only.

### OBDLab DTC portability rules

- `P0xxx`, `P2xxx`, `P34xx–P39xx` → portable across vehicles; fully decoded
- `P1xxx`, `P30xx–P33xx` → manufacturer-specific → flag `dtc_manufacturer_specific`, demote until make known

### DTC type / MIL behaviour

| Type | MIL behaviour | Key codes |
|---|---|---|
| **A — Emissions-critical** | MIL on immediately on first detection. Flashing MIL = catalyst damage imminent. | P0300–P0312, P0171/P0172/P0174/P0175 |
| **B — Emissions-related** | MIL on second consecutive failing drive cycle | P0420/P0430, EVAP family |

**Rule:** Flashing MIL during active misfire P030x → force `severity_level = CRITICAL_IMMEDIATE_STOP` regardless of confidence score.

### DTC source weighting

| Source | Weight in fault inference |
|---|---|
| Mode $03 (confirmed stored) | Full weight |
| Mode $07 (pending) | Half weight — surface as "pending" hint |
| Mode $0A (permanent) | Full weight — cannot be cleared by scan tool |
| After `codes_cleared` | Demote trim-derived faults for ≥ 1 drive cycle |

### Freeze-frame rules

- ECU stores freeze-frame for the **first Type A DTC** of the session.
- `ff_coolant_temp < 70` → fault set during warm-up → flag `dtc_set_during_warmup`.
- `ff_fuel_status == "Open_Loop"` for a fuel-trim DTC → flag as suspect.

### Sanity rails

- P0420 with no trim DTC and no misfire DTC = the **only** configuration where catalyst replacement is plausible.
- No DTCs ≠ healthy. Never use DTC absence as positive evidence.
- Codes cleared + no DTCs: trims reset; cannot be interpreted for ≥ 1 drive cycle.

---

## Domain reference — 28 live fault profiles (from `OBD Live PID Diagnostic Profiles.md`)

Each profile maps one `ChemicalSignature` enum value (`OBD_VOCABULARY.md §17`) to expected PID behaviour at SI (Stabilised Idle, 650–900 RPM) and StI (Stress Idle, VIN-derived ~4000 RPM).

**Sign convention:** Positive STFT/LTFT = ECU adding fuel (engine running lean). Negative = ECU removing fuel (engine running rich). λ > 1.0 = lean; λ < 1.0 = rich.

---

### Profile 1 — `NORMAL_OPERATION`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| STFT | −5 to +5% | −5 to +5% | Well-adapted |
| LTFT | −10 to +10% | Same | Stable long-term map |
| Wideband λ | 0.97–1.03 | 0.97–1.03 | Stoichiometric |
| O₂ (narrowband) | 0.1–0.9 V switching, 2–5 Hz | Active switching | Healthy oscillation |
| Downstream O₂ | Flat (0.4–0.6 V) | Flat | Catalyst buffering |
| MAP | 25–35 kPa | 40–60 kPa | Normal vacuum / load |

*Without DTC: All parameters nominal.*

---

### Profile 2 — `RICH_MIXTURE`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| STFT | Negative (−10 to −25%) | Negative | ECU pulls fuel |
| LTFT | Negative drift | Negative | Long-term correction |
| Wideband λ | < 0.95 | < 0.95 | Actual rich |
| O₂ (narrowband) | Stuck high (0.7–0.9 V) | High | Excess fuel, low O₂ |
| Downstream O₂ | High (0.6–0.8 V) | High | Catalyst overwhelmed |
| MAP | Normal | Normal | No air metering issue |

*Without DTC: Negative trims + rich wideband + high O₂ voltage. Check injectors, fuel pressure, EVAP.*

---

### Profile 3 — `LEAN_MIXTURE`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| STFT | Positive (> +10%) | Positive, may increase | Lean compensation |
| LTFT | Positive drift | Same | Long-term lean adaption |
| O₂ (narrowband) | Low (0.1–0.3 V), slow switching | Low | Excess O₂ |
| Wideband λ | > 1.05 | > 1.05 | Lean confirmed |
| Downstream O₂ | Low (0.1–0.3 V) | Low | Lean exhaust |
| MAP | May be slightly higher (less vacuum) if vacuum leak | Depends on leak size | — |

*Without DTC: Positive trims + lean wideband + low O₂ voltage. P0171 / P0174 probable.*

---

### Profile 4 — `IGNITION_MISFIRE`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| Misfire counters | High on one cylinder | Counts increase with RPM | Worsens under load |
| O₂ (narrowband) | Fluctuates lean (0.1–0.3 V avg) | Very lean (0.1 V) | Unburned O₂ from dead cylinder |
| Wideband λ | Lean spikes (> 1.10) but averages near stoich | Lean | Excess O₂ |
| STFT | Positive (ECU compensates) | Very positive (> +25%) | ECU trying to enrich |
| MAP | Slight pulsation (rough idle) | May drop | Misfire causes vacuum pulsation |

*Without DTC: Cylinder-specific misfire + lean O₂ + positive trims. Misfire should follow swapped coil.*

---

### Profile 5 — `LEAN_MISFIRE`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| Misfire counters | Random or multiple cylinders | Many, may be continuous | Lean mixture prevents ignition |
| O₂ (narrowband) | Very low (0.05–0.2 V) | Stuck lean | Massive excess air |
| Wideband λ | > 1.15 | > 1.15 | Extremely lean |
| STFT | Max positive (> +25%) | Pegged positive | ECU out of compensation range |
| LTFT | Large positive | Same | Cannot compensate |

*Without DTC: Multiple misfires + extremely lean wideband + pegged positive trims. P0171 + P0300.*

---

### Profile 6 — `RICH_MISFIRE`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| Misfire counters | Moderate | Worse | Rich mixture → incomplete burn |
| O₂ (narrowband) | Stuck high (0.7–0.9 V) with lean spikes | Stuck high | Excess fuel + some O₂ from misfire |
| Wideband λ | Rich (< 0.92) but unstable | Very rich | Fuel excess |
| STFT | Negative (−10 to −20%) | Negative | ECU pulls fuel |
| Downstream O₂ | High | High | Catalyst overloaded |
| Timing advance | Retarded | Retarded | Rich burn is slow |

*Without DTC: Negative trims + rich wideband + misfire counts + high O₂ voltage.*

---

### Profile 7 — `EXHAUST_AIR_LEAK`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| STFT / LTFT | Near zero (±5%) | Near zero | Leak is downstream of O₂ sensor — ECU sees no error |
| O₂ (narrowband) | Normal switching (0.1–0.9 V) | Normal | Upstream sensor unaffected |
| Wideband λ | Shows lean (λ > 1.05) | Lean | Brettschneider equation sees extra O₂ |
| Downstream O₂ | Reads lean (0.1–0.3 V) | Lean | Air dilutes downstream sample |
| MAF | Normal | Normal | No intake leak |

*Without DTC: Wideband lean + fuel trims near zero + downstream lean + normal upstream switching = exhaust air leak (post-O₂ sensor).*

---

### Profile 8 — `HIGH_COMBUSTION_TEMP` / `EGR_STUCK_CLOSED`

| PID | SI | StI / light load | Reasoning |
|---|---|---|---|
| STFT / LTFT | Normal | Normal | No mixture issue |
| Wideband λ | 0.99–1.01 | 0.99–1.01 | Stoichiometric |
| Knock retard | 0° | 3–8° retard | ECU detecting knock under load |
| EGR duty cycle | Commanded > 0% | No MAP change | EGR valve not opening |
| NOx (external) | < 100 ppm | > 1000 ppm | High combustion temperature |

*Without DTC: Normal mixture + high NOx under load + knock retard active + EGR commanded but no MAP delta.*

---

### Profile 9 — `CATALYST_NOT_LIGHTING_OFF`

| PID | SI (cold cat) | After warm-up (still fails) | Reasoning |
|---|---|---|---|
| Downstream O₂ | Mirrors upstream (swings 0.1–0.9 V) | Still mirrors after 2+ min | No oxygen storage → dead catalyst |
| Upstream O₂ | Normal switching | Normal | Engine running fine |
| STFT / LTFT | Normal | Normal | No mixture fault |
| Misfire counters | 0 | 0 | No misfire |
| ECT | Warm (85 °C) | Warm | Engine fully hot |

*Without DTC: Downstream O₂ switching like upstream (should be flat) + engine gases normal = failed catalyst. P0420 pending.*

---

### Profile 10 — `CATALYST_OVERWHELMED`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| Upstream O₂ | Abnormal (rich or lean per primary fault) | Same | Primary fault drives signal |
| Downstream O₂ | Follows upstream (no smoothing) | Follows upstream | Catalyst cannot compensate |
| STFT | Abnormal | Abnormal | Primary fuel trim problem present |
| Misfire counters | Present if misfire | Worse | Raw emissions exceed cat capacity |

*Without DTC: Downstream O₂ mirrors upstream + engine has clear mixture or misfire fault. Resolve primary fault first, then reassess catalyst.*

---

### Profile 11 — `SAMPLE_INVALID`

| PID | SI | Reasoning |
|---|---|---|
| Wideband λ | > 1.30 | Probe sampling ambient air |
| O₂ (narrowband) | Stuck lean (0.0–0.1 V) | Sensor sees atmospheric O₂ |
| STFT / LTFT | Normal | Fuel control unaffected |
| Gas analyser | CO₂ ~0.04%, O₂ ~20.9% | Ambient air sample confirmed |

*Without DTC: Wideband reads extremely lean but fuel trims normal → probe not in exhaust stream. CO + CO₂ + O₂ outside 14–18%.*

---

### Profile 12 — `TIMING_OVER_ADVANCED`

| PID | SI | StI / load | Reasoning |
|---|---|---|---|
| Timing advance | Normal (5–15°) | Much higher than spec (e.g., 50° vs 30°) | Over-advanced |
| Knock retard | 0° | Active retard (5–10°) | ECU detecting knock |
| STFT / LTFT | Normal | Normal | Mixture unaffected |
| Wideband λ | Normal | Normal | Stoichiometric |

*Without DTC: Timing advanced beyond spec + knock retard active + no mixture issues. Check base timing or knock sensor circuit.*

---

### Profile 13 — `TIMING_RETARDED`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| Timing advance | Lower than normal (0–5° vs 10°) | Lower than spec (15° vs 35°) | Retarded |
| Knock retard | 0° | 0° | Not pinging |
| ECT | Normal | Normal or slightly elevated | Late burn heats exhaust |
| STFT | Slightly positive | Slightly positive | Inefficient combustion |

*Without DTC: Timing fixed low, engine sluggish, no knock retard. Check cam timing, crank sensor, timing chain stretch.*

---

### Profile 14 — `O2_SENSOR_BIASED_LOW`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| O₂ (narrowband) | Stays low (0.1–0.3 V) despite actual rich mixture | Same | Falsely reports lean |
| Wideband λ (separate) | Shows rich (λ < 0.95) | Rich | Truth is rich |
| STFT | Positive (ECU adds fuel believing lean) | Positive, large | Opposite of expected |
| LTFT | Positive drift | Positive | Long-term wrong adaption |
| TFT | Combined > +15% | > +15% | Cross-check mismatch |

*Without DTC: Wideband rich but narrowband reads lean + positive trims = upstream O₂ biased low.*

---

### Profile 15 — `O2_SENSOR_BIASED_HIGH`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| O₂ (narrowband) | Stays high (0.7–0.9 V) despite actual lean mixture | High | Falsely reports rich |
| Wideband λ | Shows lean (λ > 1.05) | Lean | Truth is lean |
| STFT | Negative (ECU removes fuel) | Negative | Opposite of expected |
| LTFT | Negative drift | Negative | Long-term wrong adaption |
| TFT | < −10% | < −10% | Cross-check mismatch |

*Without DTC: Wideband lean but narrowband reads rich + negative trims = upstream O₂ biased high.*

---

### Profile 16 — `WORN_ENGINE`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| Misfire counters | Occasional random | More frequent | Loss of compression |
| MAP | Slightly lower vacuum (35 kPa vs 30) | Lower than normal | Vacuum loss |
| STFT | Slightly positive | Slightly positive | Inefficient combustion |
| O₂ sensors | Normal switching but may be slow | Normal | No persistent mixture bias |

*Without DTC: Low manifold vacuum + random misfire counts + normal fuel trims + low compression test.*

---

### Profile 17 — `FLAT_CAMSHAFT`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| Misfire counters | Persistent on one cylinder | Same cylinder — not load-dependent | That cylinder not filling |
| MAP | Normal vacuum, slight pulsation | Normal | Not a vacuum leak |
| MAF | Normal for RPM | Normal | Air measured correctly |
| O₂ sensors | Lean spikes from dead cylinder | Lean spikes | Unburned air |

*Without DTC: Single cylinder misfire that does not respond to ignition or injector swap → cam lobe suspect. Compression test confirms.*

---

### Profile 18 — `GDI_INTAKE_VALVE_CARBON`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| STFT | Positive (5–15%) at idle | Near 0% at stress idle | Carbon disrupts idle mixture; clears at higher airflow |
| Misfire counters | Random at idle | Disappears at elevated RPM | Flow restriction at low valve lift |
| MAP | Normal or slightly high | Normal | Carbon reduces effective flow |
| Wideband λ | Slightly lean (1.05) at idle | Normal (1.00) | Corrects at RPM |

*Without DTC: Idle misfire / lean trims that clear at stress idle in GDI engine. True lean (Profile 3) persists across the full RPM range.*

---

### Profile 19 — `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| STFT | Very negative (−20 to −30%) | Very negative | ECU pulls fuel aggressively |
| LTFT | Negative, pegged | Negative | Cannot compensate |
| Wideband λ | Very rich (λ < 0.85) | Very rich | Unmetered fuel via vacuum hose |
| O₂ (narrowband) | Stuck high (0.8–0.9 V) | Stuck high | No oxygen |
| MAP | Normal | Normal | Not a vacuum leak |

*Without DTC: Extreme negative trims + rich wideband + normal MAP. Pull FPR vacuum hose — wet = ruptured diaphragm.*

---

### Profile 20 — `GDI_HPFP_INTERNAL_SEAL_LEAK`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| STFT | Very negative (−20 to −30%) | Very negative | Same pattern as FPR rupture |
| Wideband λ | Very rich (λ < 0.85) | Very rich | Unmetered fuel via PCV system |
| LTFT | Pegged negative | Pegged negative | ECU cannot compensate |
| Oil level (physical) | Overfull, smells of fuel | — | Physical check — not a PID |

*Without DTC: Same rich pattern as Profile 19 but no fuel at FPR vacuum hose. Check oil dipstick — fuel odour + overfull on GDI engine.*

---

### Profile 21 — `WORN_VALVE_SEALS`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| Misfire counters | Occasional at idle | Clears at stress idle | Oil ingestion stops at higher RPM |
| STFT / LTFT | Slightly positive (3–8%) at idle | Near 0% at stress idle | Minor mixture effect |
| O₂ sensors | Normal switching, slight oscillation | Normal | No persistent bias |
| MAP | Normal | Normal | Vacuum draws oil at idle |

*Without DTC: Blue smoke on start-up or idle; HC high at idle; clears at stress idle with no fuel trim change.*

---

### Profile 22 — `WORN_PISTON_RINGS`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| STFT | Near 0% at idle | Negative (−12% or more) at StI | PCV blow-by vapour causes rich condition at higher RPM |
| LTFT | Slowly drifts negative | Negative | Long-term adaption to blow-by |
| Wideband λ | Normal at idle | Rich (λ < 0.98) at StI | Oil vapour + blow-by |
| Misfire counters | Few at idle | More at StI | Oil disrupts combustion |

*Without DTC: Negative fuel trims at stress idle only + oil consumption + possible blue smoke on acceleration. Compression low.*

---

### Profile 23 — `POA_SIGNATURE`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| STFT / LTFT | Positive at idle (O₂ poisoned → false lean) | Negative at StI (actual rich from oil) | Erratic trims across RPM bands |
| O₂ (narrowband) | Slow switching, biased lean despite rich mixture | Still biased | Sensor contaminated by oil |
| Wideband λ | Shows lean (false) at idle; rich at StI | Inconsistent | Sensor poisoning effect |
| Misfire counters | High HC contribution | High | Oil causing incomplete combustion |
| Downstream O₂ | Slow, cat efficiency poor | Poor switching | Catalyst coated with oil-ash |

*Without DTC: Oil consumption + erratic fuel trims + O₂ stuck lean + high HC. Replace O₂ and catalyst after fixing the oil ingestion source.*

---

### Profile 24 — `WRONG_VALVE_TIMING`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| MAP | Lower vacuum (45 kPa vs 30) | Lower throughout | Poor volumetric efficiency |
| Misfire counters | Random or multiple cylinders | Worse | Valves opening at wrong time |
| Wideband λ | Normal or slightly lean | Normal | Not a mixture issue |
| STFT | Slightly positive | Positive | ECU compensates for incomplete burn |
| Cam/Crank correlation PID | Camshaft position offset > 5° | Same | Mechanical misalignment |

*Without DTC: Poor vacuum + misfire counts + normal fuel trims + cam/crank correlation error → check timing marks.*

---

### Profile 25 — `EGR_STUCK_CLOSED`

| PID | SI | StI / light load | Reasoning |
|---|---|---|---|
| MAP | Normal idle vacuum | Under load: MAP lower (no EGR gas dilution) | No exhaust gas displacing charge |
| EGR duty cycle | Commanded > 0% | No MAP change | EGR valve not opening |
| STFT / LTFT | Normal | Normal | No mixture effect |
| Knock retard | 0° | May show retard under load | No EGR cooling → higher combustion temp |

*Without DTC: High NOx (external meter) + EGR commanded but no MAP change + possible knock retard under load.*

---

### Profile 26 — `EGR_STUCK_OPEN`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| MAP | Higher than normal (50 kPa vs 30–35) | Returns to normal at StI | EGR dilutes charge at idle |
| STFT | Positive (ECU adds fuel to maintain combustion) | Normal at high RPM | EGR authority disappears with high airflow |
| Misfire counters | High at idle | Clears at stress idle | Rough idle from EGR dilution |
| Wideband λ | Slightly lean (1.05) at idle | Normal | EGR displaces intake air |

*Without DTC: Rough idle + high MAP + misfire counts that clear with RPM. Command EGR off — if idle improves, EGR stuck open.*

---

### Profile 27 — `VVT_FAILURE`

| PID | SI | StI | Reasoning |
|---|---|---|---|
| Cam position desired vs actual | Desired retard, actual stuck advanced (or vice versa) | Same error | Phaser mechanically stuck |
| MAP | Lower vacuum (reduced VE) | Lower | Wrong valve timing |
| STFT | May be positive | Positive | Inefficient combustion |
| Misfire counters | Possible random | Possible | Poor valve timing |

*Without DTC: VVT angle error on scan tool + driveability complaint. Check oil pressure and solenoid function.*

---

### Profile 28 — `EVAP_CANISTER_SATURATED`

| PID | Condition: mid-load cruise | Reasoning |
|---|---|---|
| STFT | Negative spikes when purge valve opens | Purge vapour is fuel-rich |
| LTFT | Drifts negative over time | Long-term learned compensation |
| Wideband λ | Momentary rich spikes (λ < 0.98) during purge | Loaded canister releasing fuel vapour |
| EVAP purge duty cycle | Rises at cruise | Confirmed purge active |

*Without DTC: Negative trims coincident with EVAP purge duty cycle rise at cruise. Check canister for fuel saturation.*

---

## Domain reference — Advanced powertrain clusters (from `OBDadd1.md`)

**Cross-reference:** `OBD_VOCABULARY.md §18` — trim delta rules. `OBD_VOCABULARY.md §21` — full diagnostic decision tree. This section supplements with powertrain cluster classification and 5-gas/OBD correlation.

### 5-gas / OBD correlation table

| Gas | Rich condition | Lean condition | Misfire condition |
|---|---|---|---|
| CO | High | Low | High (partial combustion) |
| HC | High (fuel wash) | Normal–high (lean misfire) | High (unburned fuel) |
| O₂ | Low (fuel consumes it) | High (excess air) | High (unburned air from dead cylinder) |
| CO₂ | Low–medium | Low (diluted) | Low (incomplete combustion) |
| NOx | Low (rich quenches) | High (high temp + excess O₂) | Low (misfire quenches) |
| λ | < 1.0 | > 1.0 | ~1.0 average (cylinder-by-cylinder varies) |

**Key rule:** High HC with low CO = misfire, not rich. High HC with high CO = rich mixture.

### Powertrain cluster classification (fault family routing)

| Cluster | TFT | λ | Gas O₂ | Gas CO | Primary `FaultFamily` |
|---|---|---|---|---|---|
| **Rich** | Negative | < 1.0 | Low | High | `rich_mixture` |
| **Lean** | Positive | > 1.0 | High | Low | `lean_condition` |
| **Misfire** | Near 0% or erratic | ~1.0 (average) | High (dead cylinder O₂) | High (partial burn) | `misfire` |
| **Perception** | Opposes λ direction | Contradicts TFT | Consistent with gas analyser | Contradicts OBD | `sensor_fault` |

### Ghost Misfire rule (from `OBD_VOCABULARY.md §18.4`)

If misfire counters increment but `total_trim_correction_delta` and wideband lambda are normal → check alternator AC ripple corrupting ignition primary signal before chasing coils or plugs.

---

## Domain reference — Ignition timing system (from `RefDocs/ignition-timing/`)

### Timing advance rationale

Flame front burn rate is approximately constant. More crank-angle time is needed for combustion as RPM increases → timing must advance with RPM.

| State | Typical spark advance |
|---|---|
| Curb idle (~800 RPM) | 5–15° BTDC |
| Stress idle (~4000 RPM, no load) | 25–40° BTDC |
| WOT (premium fuel) | 30–35° BTDC |
| **Knock retard active** | Baseline minus 5–15° |

**Over-advance effects:** Detonation, piston crown damage, knock sensor activation, PCM retard. Signature: `knock_retard_deg > 0` at load with timing above spec.

**Under-advance (retard) effects:** Low power, excessive exhaust heat, exhaust valve / bore wear, high idle HC. Signature: timing fixed low, no knock retard, sluggish engine.

### Cam vs ignition timing distinction

| Term | What it describes | How to read |
|---|---|---|
| Ignition timing | When the spark fires (BTDC) | Scan tool `timing_advance_deg_btdc` PID (`010E`) |
| Cam timing | When valves open/close (crank degrees) | Cam/crank correlation PID or timing light at cam mark |

A stretched timing chain affects **cam timing**, not ignition timing directly. ECU may retard spark in response to poor VE or knock if the cam is significantly retarded.

### Spark burn line analysis (oscilloscope)

| Burn line characteristic | Diagnosis |
|---|---|
| < 0.75 ms | Lean mixture, low compression, or high plug lead resistance |
| > 2 ms | Rich mixture, fouled plug, or plug/lead short circuit |
| "Hash" on burn line | Lean misfire or ignition noise |
| < 2 coil oscillations after firing line | Weak coil — likely to fail under cylinder pressure |
| ≥ 3 coil oscillations | Healthy coil |

### Spark plug condition diagnostics

| Plug condition | Likely cause |
|---|---|
| Wet / oily | Oil ingestion (valve seals or rings) |
| Black sooty (dry) | Rich mixture or incomplete combustion |
| Whitish-brown / chalky | Lean mixture |
| Detonation pitting / melted electrode | Pre-ignition / detonation damage |
| Normal grey/tan | Healthy |

---

## Domain reference — Vacuum / MAP diagnostics (from `RefDocs/vacuum-systems/`)

### MAP kPa reference (sea-level, closed throttle, warm idle)

| kPa reading | Vacuum equivalent | Condition |
|---|---|---|
| 25–35 kPa | ~18–22" Hg | Healthy engine at warm idle |
| 35–50 kPa | ~10–17" Hg | Marginal — timing or restriction issue |
| > 50 kPa | < 10" Hg | Significant restriction or major vacuum leak |
| ~100 kPa | ~0" Hg | Engine off (atmospheric) or severe restriction |

**Altitude correction:** −1" Hg per 1000 ft above sea level.

### Vacuum gauge patterns

| Reading | Condition |
|---|---|
| 18–22" Hg steady | Healthy engine |
| < 15" Hg steady | Worn engine, exhaust restriction, or retarded timing |
| Low + rhythmic fluctuation | Burnt or leaking valves |
| Gradual drop at held elevated RPM | Exhaust restriction (collapsed pipe, clogged catalyst) |

### Snap throttle test

```
Step 1  Warm idle
Step 2  Snap throttle to ~25% and release
Step 3  Healthy:             MAP plunges to ~0" Hg → rebounds 5"+ above idle on release
        Exhaust restriction: MAP same or lower at steady elevated RPM — cannot evacuate cylinders
        Vacuum leak:         Low idle MAP; improves only slightly on snap
```

### IAC count as vacuum leak indicator

| IAC count | Interpretation |
|---|---|
| 20–30 | Normal — IAC controlling idle correctly |
| < 10 (near 0) | Major vacuum leak — IAC closing to compensate for excess unmetered air |
| > 50 | IAC open wide — engine needs more air than spec |

### EGR strategy divergence (critical for OBDLab VIN DNA routing)

| `air_metering_strategy` | EGR effect on MAP | Trim response |
|---|---|---|
| `MAP_ONLY_SPEED_DENSITY` | EGR raises MAP → ECU reads lower load → LTFT **positive** (lean compensation) | Positive trims at idle may be EGR, not vacuum leak |
| `DUAL_MAF_MAP_CROSSCHECK` | EGR dilutes charge → MAF drops → ECU reads less air → LTFT **negative** (rich compensation) | Negative trims at idle may be EGR stuck open |

**Rule:** Always cross-reference `VinDNA.air_metering_strategy` before assigning trim direction to an EGR fault. The same EGR fault produces opposite trim signs depending on the air metering strategy.

---

## Domain reference — Misfire diagnostics (from `RefDocs/misfires/`)

### Three root causes

```
Misfire (incomplete combustion)
    │
    ├─ Loss of spark
    │   └─ Coil, plug wire, spark plug, CKP/CMP sensor, ignition module
    │
    ├─ Air/fuel mixture out of range
    │   └─ Vacuum leak, fuel delivery, injector, MAF, VVT, EGR, EVAP
    │
    └─ Loss of compression
        └─ Worn rings, burnt/leaking valve, flat cam lobe, jumped timing, head gasket
```

### Misfire type classification

| Type | Characteristics | Likely cause |
|---|---|---|
| **Steady single-cylinder** | Specific cylinder always misfires | Coil, plug, injector, or mechanical (single cylinder) |
| **Intermittent single-cylinder** | Same cylinder, comes and goes | Weak coil (arcs under cylinder pressure), hairline plug crack |
| **Random multi-cylinder (P0300)** | No cylinder pattern | Vacuum leak post-MAF, EGR, coil power supply, fuel pressure |
| **Load-dependent** | Only at stress idle, clears at idle | Coil insulation breakdown, GDI HPFP, fuel delivery |
| **Idle-only** | Clears at stress idle | Valve seals, GDI carbon, EGR stuck open |

### DTC pairing rules

| DTC combination | Interpretation |
|---|---|
| P030x + P020x (same cylinder) | Bad injector |
| P030x + P035x (same cylinder) | Bad coil |
| P030x + P0401 | Carbon under EGR valve — clean or replace EGR |
| P030x + P0171 / P0174 (lean) | Lean misfire — find air leak or fuel delivery fault |
| P0300 + no companion DTC | Common-mode fault — vacuum leak, fuel pressure, alternator ripple |

### Adjacent cylinder misfire rule

Two adjacent cylinders misfiring simultaneously with no individual injector or coil DTC → suspect **head gasket breach between those cylinders.** Confirm with cooling system pressure test.

### OBD-II misfire monitor operation

Tracked via CKP tooth-period analysis. Runs continuously once:
- ECT > 60 °C, RPM 600–6000, no fuel cut active

Mode 06 MID `$A1–$A6+`: per-cylinder misfire accumulators. TID `$0B` = cumulative misfire count. See `OBD_VOCABULARY.md §19`.

---

## Document index — source files incorporated

| Section(s) | Source document | Location |
|---|---|---|
| §2–12 (module core) | OBDlab.md (blueprint) | `OBDLab/bp/OBDlab.md` |
| Fault profiles §1–28 | OBD Live PID Diagnostic Profiles.md | `OBDLab/wiki/` |
| Advanced clusters | OBDadd1.md | `OBDLab/wiki/` |
| Fuel trim (cross-ref) | master_fuel_trim_guide.md | `OBDLab/wiki/` |
| O₂ sensors (cross-ref) | master_o2_sensor_guide.md | `OBDLab/wiki/` |
| Catalyst (cross-ref) | master_catalyst_guide.md | `OBDLab/wiki/` |
| DTC (cross-ref) | master_obd_guide.md | `OBDLab/wiki/` |
| Ignition timing | ignition-timing.md, ignition-diagnostics.md, analyzing-ignition-misfires.md | `OBDLab/RefDocs/ignition-timing/` |
| Vacuum / MAP | vacuum.md, Diagnostic Dilemmas.md, map-sensor-troubleshooting.md | `OBDLab/RefDocs/vacuum-systems/` |
| Misfire extended | misfire-diagnosis.md | `OBDLab/RefDocs/misfires/` |

---

*Document version: 5.0 — Reformatted 2026-05-18 to COMLab vocabulary wiki standard*
*Changes from v4.1: Added StrEnum declarations (§6), alias normalization table (§7), Physics Gate table (§4), explicit OBDLivePayload schema (§5), domain reference provenance headers. Content cross-referenced to OBD_VOCABULARY.md §11–21 rather than duplicated. 28 fault profiles retained in full.*
*Stress Idle correction: second measurement point is VIN-derived stress idle RPM (~4000 RPM typical), not 2500 RPM.*
