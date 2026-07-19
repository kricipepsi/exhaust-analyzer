---
node_type: wiki
lab: obdlab
module: semantic-vocabulary
subsystem: obd-enums
implements:
  - "labs/obdlab/obdlab/schemas/vocabulary.py"
consumers:
  - "comlab: fault_atlas_router (fuel_system_status routing)"
  - "comlab: T-COMV2-O2OFFSET-1 (O2FailureMode.WIDEBAND_OFFSET_CANDIDATE)"
  - "dtclab: freeze_frame_extractor (FuelSystemStatus open-loop derivation)"
drift_guards:
  - "labs/obdlab/tests/unit/test_vocabulary.py"
tags: [vocabulary, obd, semantic, finished]
source: "labs/semantic/vocabul/OBD_VOCABULARY.md"
---

# OBD Vocabulary Wiki

**Purpose:** the authoritative vocabulary for OBD (On-Board Diagnostics) identifiers used across all 4DLab modules — VINLab, GASLab, OBDLab, DTCLab, COMLab. Every PID name, unit, range, RPM band, and polymorphic switch in the codebase derives from this wiki.

**Status:** v1.2 (2026-06-10). To be updated as the OBDLab BP and COMLab schemas evolve.
**Changelog:** v1.1 (2026-05-23) — added EGR_DILUTION_MISFIRE, INCOMPLETE_OXIDATION to ChemicalSignature enum (§17).
**Changelog:** v1.2 (2026-06-10) — reconciled §12.4 O2FailureMode (7→4) and §5.2 FuelSystemStatus to shipped obdlab code.

**Scope:** petrol vehicles 1990-2020 (Euro 1 through Euro 6/7), manually entered data — no live CAN/OBD streaming.

---

## 1. Standards anchored

This wiki aligns COMLab's vocabulary with three industry standards. Where the standards differ in naming, this wiki's choices and rationale are documented inline.

| Standard | Scope | Used here for |
|---|---|---|
| **ISO 15031-5 (≡ SAE J1979 / J1979DA)** | OBD-II PID definitions, Mode 01 / Mode 02 | Canonical PID identifiers, units, value ranges |
| **ISO 15031-6 (≡ SAE J2012 / J2012DA)** | DTC code structure and definitions | See DTC_VOCABULARY.md |
| **ISO 14229 (UDS)** | Unified Diagnostic Services | Mode 06 monitor structure |

---

## 2. Canonical PID identifiers (the 8-PID minimalist schema)

The OBDLab BP §2 specifies a "High-Density Node Inventory" of exactly 8 core PIDs. This table is the canonical source for every PID name used in 4DLab code, mapped to its SAE J1979 origin.

| 4DLab canonical name | ISO 15031-5 PID | SAE J1979 PID | Description | Unit | Range | Source |
|---|---|---|---|---|---|---|
| `engine_rpm` | `010C` | `010C` | Engine speed | RPM | 0 – 16383.75 | ISO 15031-5 / J1979 |
| `coolant_temp_c` | `0105` | `0105` | Engine coolant temperature | °C | -40 – 215 | ISO 15031-5 / J1979 |
| `calculated_engine_load_pct` | `0104` | `0104` | Calculated engine load | % | 0 – 100 | ISO 15031-5 / J1979 |
| `mass_airflow_gps` | `0110` | `0110` | Mass airflow rate (MAF) | g/s | 0 – 655.35 | ISO 15031-5 / J1979 |
| `manifold_vacuum_kpa` | `010B` | `010B` | Intake manifold absolute pressure (MAP) | kPa | 0 – 255 | ISO 15031-5 / J1979 |
| `shrtft1` | `0106` | `0106` | Short-term fuel trim, Bank 1 | % | -127 – +127 | ISO 15031-5 / J1979 |
| `longft1` | `0107` | `0107` | Long-term fuel trim, Bank 1 | % | -127 – +127 | ISO 15031-5 / J1979 |
| `total_trim_correction_delta` | (derived) | (derived) | STFT + LTFT, virtual node | % | -200 – +200 | OBDLab BP §2 |

**Bank 2 (V engines):** `shrtft2` and `longft2` map to ISO 15031-5 / SAE J1979 PIDs `0108` and `0109` respectively. Same units and ranges.

**Naming convention rationale:** the short forms (`shrtft1`, `longft1`, `manifold_vacuum_kpa`) come from the OrchestratorLabBP and OBDLab BP, which agreed on a common style. They're descriptive enough that no decoder is needed, short enough to be ergonomic in code. The v6 module's even-shorter names (`stft_idle`, `ltft_idle`, `map_idle`) are retired.

---

## 3. Measurement RPM points — both legal and clinical

The cases corpus and the OBDLab BP currently use **2500 RPM** as the second measurement point. This is the standard regulatory test point, but for clinical diagnosis a higher RPM exposes load-dependent faults that 2500 RPM hides. The wiki captures both:

### 3.1 `REGULATORY_HIGH_IDLE` — the legal compliance point

| Field | Value | Source |
|---|---|---|
| Target RPM | **2500** | SAE J1667, BAR Two-Speed Idle |
| Acceptable band | 2200 – 2800 | Virginia 9VAC5-91-440 |
| Stable hold time | 30 s (10 s warm-up, 20 s measurement) | Two-speed idle spec |
| Purpose | Regulatory emissions test snapshot | EPA / BAR / Euro 2 IM |
| Diagnostic value | Baseline — passes most cars with subtle faults | Limited |

This is what the 281-row `cases_petrol_master_v5.csv` corpus captures in its "2500 RPM" gas readings. It will remain the default measurement point because (a) it's what regulatory hardware reports, and (b) the existing test corpus is built on it.

### 3.2 `STRESS_IDLE` — the clinical diagnostic point (NEW)

| Field | Value | Source |
|---|---|---|
| Target RPM | **VIN-dependent, typically 3500 – 4500** | OBDLab BP, user spec 2026-05-16 |
| Per-vehicle target | from VINLab `stress_idle_rpm_target` field | VINLab output |
| Stable hold time | 15 s minimum | Diagnostic best practice |
| Purpose | Force load-dependent fault exposure — coil arcing under cylinder pressure, marginal injectors, GDI fuel rail droop | Clinical |
| Diagnostic value | High — exposes faults invisible at idle/2500 | Critical |

**Why VIN-dependent:** a Euro 1 carbureted 1.0L can't sustain 4500 RPM without harm; a Euro 6 turbo GDI 2.0L barely starts to stress at 3500. VINLab emits a `stress_idle_rpm_target` per vehicle, derived from engine code + emission tier + induction type. Examples:

```
Euro 1 NA 1.0L  -> stress_idle_rpm_target = 3000  (legacy headroom)
Euro 3 NA 1.6L  -> stress_idle_rpm_target = 3500
Euro 4 NA 2.0L  -> stress_idle_rpm_target = 4000
Euro 5 turbo 1.4L  -> stress_idle_rpm_target = 4000  (boost ramps engage)
Euro 6 GDI 2.0L  -> stress_idle_rpm_target = 4500  (HPFP loaded)
```

### 3.3 Engine state buckets (per OBDLab BP §3)

| Bucket ID | RPM band | Load | Notes |
|---|---|---|---|
| `STABILIZED_IDLE` | 650 – 900 | < 30% | Closed-loop, warm engine |
| `REGULATORY_HIGH_IDLE` | 2200 – 2800 | 15 – 40% | Two-speed idle test (was `HIGH_IDLE_LOAD` in old BP) |
| `STRESS_IDLE` | 3500 – 4500 (VIN-dependent) | 40 – 60% | Clinical load test (NEW). VIN-derived target per OBDLab BP state-bucketing rules; OBDLab BP currently uses `HIGH_IDLE_LOAD` naming and does not yet define this bucket — cross-reference to be added when OBDLab BP §6 is updated. |
| `COLD_OPEN_LOOP_INVALID` | any | any | ECT < 75°C — freeze all trim analytics |

**Recommendation for OBDLab BP:** the BP currently calls the second point `HIGH_IDLE_LOAD` and uses 2200-2600. This wiki proposes renaming it to `REGULATORY_HIGH_IDLE` and adding a new `STRESS_IDLE` bucket. The OBDLab BP needs a §3 revision when this lands.

---

## 4. VIN-driven polymorphic switches (OBDLab BP §4 "Global VIN Guards")

VINLab emits four switches that propagate into OBDLab and Gas Lab. These are the most architecturally important identifiers in the vocabulary.

### 4.1 `euro_emission_category`

```
EURO_1 | EURO_2 | EURO_3 | EURO_4 | EURO_5 | EURO_6 | EURO_7
```

Drives Gas Lab threshold masks (max allowed CO/HC/NO_x per category).

### 4.2 `air_metering_strategy` — solves the "missing MAP sensor" problem

```python
class AirMeteringStrategy(StrEnum):
    DUAL_MAF_MAP_CROSSCHECK = "DUAL_MAF_MAP_CROSSCHECK"  # both sensors present
    MAP_ONLY_SPEED_DENSITY  = "MAP_ONLY_SPEED_DENSITY"   # no MAF — emulate via MAP
    MAF_ONLY                = "MAF_ONLY"                 # no MAP — infer via MAF
```

OBDLab's Volumetric Efficiency calc dynamically routes to the matching formula. Per BP §3.1 (3-Way Polymorphic Math Routing Matrix).

### 4.3 `upstream_o2_sensor_type` — solves the "narrowband vs wideband" problem

```python
class O2SensorType(StrEnum):
    NARROWBAND_0_TO_1V = "NARROWBAND_0_TO_1V"  # voltage swing, switching style
    WIDEBAND_LINEAR    = "WIDEBAND_LINEAR"     # linear lambda or current
    WIDEBAND_NB_SIM    = "WIDEBAND_NB_SIM"     # aftermarket WB controller in NB simulation mode
```

OBDLab normalizes all three to a common virtual node `normalized_obd_lambda`.
WIDEBAND_NB_SIM reads pid_oxygen_sensor_volts and applies the same 3-zone
mapping as narrowband but emits WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA mode so
COMLab TrimAnalyticsGate can apply the correct weight coefficient. Per BP §3.2.

### 4.4 `stress_idle_rpm_target` (NEW per user spec 2026-05-16)

```python
stress_idle_rpm_target: int  # range 2800-5000, VIN-derived
```

OBDLab applies this when entering the STRESS_IDLE bucket.

---

## 5. Derived / virtual nodes

These are not raw PIDs — they're calculated inside OBDLab and exposed to the Orchestrator.

| Node | Formula | Range | Notes |
|---|---|---|---|
| `total_trim_correction_delta` | `shrtft1 + longft1` | -254 – +254 % | Widened per T-W-6 to accommodate ±127% per-trim sentinel doubled |
| `calculated_ve` | Ideal-gas air-loop equation | 0 – 100 % | Volumetric Efficiency, OBDLab BP §1 |
| `normalized_obd_lambda` | Per O2 sensor type | 0.7 – 1.3 | Bridges narrowband + wideband |
| `engine_warmed` | `coolant_temp_c >= 70` | bool | Gates all downstream analytics |

### 5.1 GASLab boundary enums (mirrored in COMLab)

```python
class SampleValidity(StrEnum):
    VALID = "VALID"
    BORDERLINE = "BORDERLINE"
    INVALID = "INVALID"
    EXTERNAL_O2_SUSPECT = "EXTERNAL_O2_SUSPECT"
```

### 5.2 OBDLab analytics enums (mirrored in COMLab)

```python
class VEValidity(StrEnum):
    VALID = "VALID"
    FAULT_VE_IDLE_COLLAPSE = "FAULT_VE_IDLE_COLLAPSE"
    FAULT_MAF_CONTAMINATION = "FAULT_MAF_CONTAMINATION"
    FAULT_VE_SENSOR_SKEW = "FAULT_VE_SENSOR_SKEW"
    UNKNOWN = "UNKNOWN"

class TrimAnalyticsGate(StrEnum):
    VALID = "VALID"
    ENGINE_COLD = "ENGINE_COLD"
    OPEN_LOOP = "OPEN_LOOP"
    O2_FAULT_ACTIVE = "O2_FAULT_ACTIVE"
    CKP_CMP_FAULT_ACTIVE = "CKP_CMP_FAULT_ACTIVE"
    CODES_RECENTLY_CLEARED = "CODES_RECENTLY_CLEARED"
    WOT_ACTIVE = "WOT_ACTIVE"
    DFCO_ACTIVE = "DFCO_ACTIVE"
    SEMANTIC_ERROR = "SEMANTIC_ERROR"

class NodeMAFStatus(StrEnum):
    REAL_SENSOR_FEED = "REAL_SENSOR_FEED"
    VIRTUAL_EMULATION = "VIRTUAL_EMULATION"

class NodeMAPStatus(StrEnum):
    REAL_SENSOR_FEED = "REAL_SENSOR_FEED"
    BACK_CALCULATED = "BACK_CALCULATED"

class O2NormalizationMode(StrEnum):
    """O2 sensor normalization routing mode — emitted by OBDLab, consumed by COMLab TrimAnalyticsGate."""
    NARROWBAND_VOLTAGE_TO_LAMBDA       = "NARROWBAND_VOLTAGE_TO_LAMBDA"       # wiki: OBD_VOCABULARY §12.1 — 3-zone voltage mapping
    WIDEBAND_PASSTHROUGH               = "WIDEBAND_PASSTHROUGH"                # wiki: OBD_VOCABULARY §12.2 — direct lambda/AFR passthrough
    WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA  = "WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA"  # wiki: OBD_VOCABULARY §12.3 — WB sensor in NB-sim mode, 3-zone mapping, mode preserved for COMLab TrimAnalyticsGate branching
```

```python
class FuelSystemStatus(StrEnum):   # mirrored in COMLab; sourced from DTC_VOCABULARY §8
    CL = "CL"              # §8 — closed loop; O₂ feedback active
    OL = "OL"              # §8 — open loop; base map (cold start)
    OL_DRIVE = "OL_DRIVE"  # §8 — open loop driving (WOT, decel)
    OL_FAULT = "OL_FAULT"  # §8 — open loop due to O₂ sensor fault
```



### 5.3 OBDLiveDataPayload — canonical output schema (per T-FX-1)

Replaces the v0.1 stub. Every field has a named consumer in COMLab's fault-atlas router or perception-contradiction detector. Source: `COMLab/comlab/schemas/ingestion.py`.

| Field | Type | Consumer in COMLab |
|---|---|---|
| `engine_warmed` | `bool` | Closed-loop analytics entry gate |
| `total_trim_correction_delta` | `float` (−200..+200 %) | Rich/lean differential diagnosis |
| `normalized_obd_lambda` | `float \| None` (0.7–1.3, Optional for no-OBD fallback per T-FX-7) | Perception-contradiction cross-check vs `lambda_chem` |
| `ve_pct` | `float` (0–100 %) | VE fault verdicts (collapse, contamination, skew) |
| `ve_validity` | `VEValidity` | Gates VE-derived findings |
| `rpm_state_bucket` | `EngineStateBucket` | Evidence weighting per operating regime |
| `trim_analytics_gate` | `TrimAnalyticsGate` | Suppresses trim findings when blocked (cold, open-loop, WOT) |
| `o2_failure_mode` | `O2FailureMode` | Gates trim-based findings when O2 has failed |
| `maf_status` | `NodeMAFStatus` | Provenance flag — real sensor feed vs virtual emulation |
| `map_status` | `NodeMAPStatus` | Provenance flag — real sensor feed vs back-calculated |
| `freeze_frame_pids` | `FreezeFramePIDs?` | Freeze-frame snapshot at DTC set time |

Raw `shrtft1` / `longft1` are **not** emitted — replaced by `total_trim_correction_delta`.
COMLab does not re-aggregate what OBDLab already owns.

### 5.4 DTCLabPayload — canonical output schema (per T-FX-2)

Full 9-field contract replacing the v0.1 stub (`active_mil` + `confirmed_dtcs` only).
Every field is consumed by `fault_atlas_router.py` §4 Stage B or COMLab confidence scoring.
Source: `COMLab/comlab/schemas/ingestion.py`.

| Field | Type | Consumer in COMLab |
|---|---|---|
| `active_mil` | `bool` | DTC status banner |
| `mil_flashing` | `bool` | CRITICAL_IMMEDIATE_STOP override (catalyst damage imminent) |
| `confirmed_dtcs` | `list[str]` | Primary DTC evidence — DTC_REGEX validated |
| `pending_dtcs` | `list[str]` | Weight 0.5 vs confirmed 1.0 — early warning |
| `permanent_dtcs` | `list[str]` | Weight 1.0 — survives scanner clears |
| `routing_tags` | `list[DTCRoutingTag]` | Fault-atlas router primary DTC evidence input |
| `mode_06_monitors` | `dict[MID_TID, Mode06MonitorResult]` | Pre-MIL degradation evidence |
| `historical_fault_context` | `HistoricalFaultContext` | Idle vs load vs cold-start context for differential |
| `freeze_frame` | `FreezeFrameRecord` | 12 mandatory + 7 optional Mode $02 PIDs at fault moment |

---

## 6. Fault families (cross-reference with cases CSV)

Per the `expected_top_fault_family` column in `cases_petrol_master_v5.csv` — these are the **classification labels** COMLab's router emits.

```python
class FaultFamily(StrEnum):
    LEAN_CONDITION    = "lean_condition"
    RICH_MIXTURE      = "rich_mixture"
    MISFIRE           = "misfire"
    SENSOR_FAULT      = "sensor_fault"
    ECU_FAULT         = "ecu_fault"
    CATALYST_FAILURE  = "catalyst_failure"
    EXHAUST_LEAK      = "exhaust_leak"
    IGNITION_FAULT    = "ignition_fault"
    MECHANICAL_WEAR   = "mechanical_wear"
    CAM_TIMING        = "cam_timing"
    NON_STARTER       = "non_starter"
    NO_FAULT          = "no_fault"
```

Specific fault nodes (the `expected_top_fault` column) are documented per case in the cases corpus — examples: `Mechanical_Lean_Vacuum_Leak`, `Mechanical_Rich_Leaking_Injector`, `Mechanical_Misfire_Spark_Plug`, `ECU_Logic_Inversion_False_Lean`, `Lazy_O2_Sensor_Aging`.

---

## 7. Architecture horizons

```python
class Horizon(StrEnum):
    LEGACY   = "HORIZON_LEGACY"    # Euro 1-2, 1990-2000
    ADAPTIVE = "HORIZON_ADAPTIVE"  # Euro 3-4, 2000-2010
    MODERN   = "HORIZON_MODERN"    # Euro 5-6, 2010-2020
```

Mapped from `euro_emission_category` by VINLab. COMLab uses the horizon for fault registry pruning.

---

## 8. Confidence ratings

Per OrchestratorLabBP.md §"Output API Response":

```python
class ConfidenceRating(StrEnum):
    HIGH_ASSURANCE      = "HIGH_ASSURANCE"
    DEGRADED_ASSURANCE  = "DEGRADED_ASSURANCE"
    LOW_CERTAINTY       = "LOW_CERTAINTY"
```

Per VINLab output:

```python
class VinConfidence(StrEnum):
    HIGH    = "HIGH"     # all WMI/year/engine_code resolved
    PARTIAL = "PARTIAL"  # year resolved but engine code unknown
    NONE    = "NONE"     # WMI not found in registry
```

---

## 9. Degradation modes (COMLab fallback tree)

Per OrchestratorLabBP.md §"Fallback Error Execution Tree":

```python
class DegradationMode(StrEnum):
    FULL_FUSION       = "FULL_FUSION"        # all four labs reported cleanly
    GAS_DOMINANT      = "GAS_DOMINANT"       # OBD/DTC degraded — legacy car
    FATAL_INCOMPLETE  = "FATAL_INCOMPLETE"   # essential data missing — abort
```

---

## 10. Severity levels (UI-facing)

Per OrchestratorLabBP.md §"Serialize Output":

```python
class SeverityLevel(StrEnum):
    CRITICAL_IMMEDIATE_STOP        = "CRITICAL_IMMEDIATE_STOP"
    WARNING_DEGRADED_PERFORMANCE   = "WARNING_DEGRADED_PERFORMANCE"
    OPTIMAL_HEALTH                 = "OPTIMAL_HEALTH"
```

---

## 11. Domain reference — Fuel trim patterns (from `master_fuel_trim_guide.md`)

The master fuel trim guide defines the diagnostic interpretation rules for STFT/LTFT that the OBD Lab applies. **Naming alias:** the guide uses `STFT` / `LTFT`; the canonical 4DLab fields are `shrtft1` / `longft1`. Both refer to the same SAE J1979 PIDs (`0106` / `0107`).

### 11.1 Normal operating ranges

| State | STFT range | LTFT range | Total (STFT + LTFT) |
|---|---|---|---|
| Healthy idle | -5% to +5% | -10% to +10% | ±10% |
| Healthy cruise | -5% to +5% | -10% to +10% | ±10% |
| ECU-set DTC trigger | n/a | n/a | ≈ ±25% |
| Register saturation | n/a | n/a | ±127% (magnitude meaningless beyond ±25%) |

### 11.2 RPM-dependence decision tree (THE diagnostic discriminator)

**Three-Speed Test:** measure trims at idle, 2500 RPM, and 3000 RPM. The way trims behave across RPM bands is what distinguishes one fault from another, even when the absolute trim numbers look similar.

| Trim pattern across RPM | Most likely fault |
|---|---|
| LTFT high+ at idle, drops toward normal at 2500-3000 | **Vacuum leak** (constant volume — diluted at high air mass flow) |
| Moderate+ at idle, **worsens** at higher RPM | **Fuel delivery** (pump/filter/regulator — can't keep up) |
| + at idle, − under load | **MAF under-reading** (contaminated sensor) |
| − on **one bank**, persists across RPM | **Leaking injector** on that bank |
| − at idle, normalizes at cruise | **Stuck-open EVAP purge** |
| High+ at idle, normalizes at cruise | **Stuck-open EGR** |

### 11.3 Truth-vs-Perception cross-check

Compare ECU-reported lambda direction against Gas Lab's chemistry-derived lambda:

| Gas Lab λ | ECU trim direction | Verdict |
|---|---|---|
| λ < 1 (chemically rich) | LTFT negative (cutting fuel) | Agreement — real rich condition |
| λ < 1 | LTFT positive (adding fuel) | **Contradiction** — suspect O₂ sensor bias or silicone poisoning |
| λ > 1 (chemically lean) | LTFT positive (adding fuel) | Agreement — real lean condition |
| λ > 1 | LTFT negative (cutting fuel) | **Contradiction** — suspect O₂ sensor bias |

### 11.4 Preconditions for valid trim reading

All of the following must hold; otherwise mark `fuel_trim_invalid`:

- ECT ≥ 70°C (engine warmed)
- Fuel system status = closed-loop (CL)
- No active P0130–P0161 (O₂ sensor faults)
- No active P0335 / P0340 (crank/cam sensor faults)
- ≥ 1 drive cycle since `codes_cleared`
- Not in WOT (Wide Open Throttle) or DFCO (Decel Fuel Cut-Off)

---

## 12. Domain reference — O₂ sensor behavior (from `master_o2_sensor_guide.md`)

### 12.1 Narrowband (NARROWBAND_0_TO_1V) sensor numerical thresholds

| Metric | Healthy range | Failure signature |
|---|---|---|
| Stoichiometric center | ~0.45 V (450 mV) | Drift = bias |
| Rich peak | 0.80 – 0.90 V | Stuck rich if pinned > 0.85 V |
| Lean peak | 0.10 – 0.20 V | Stuck lean if pinned < 0.20 V |
| Cross-counts @ 2500 RPM | ≥ 8 per 10 s | < 8 = sluggish |
| Switching frequency (MPI) | 2 – 5 Hz | < 0.5 Hz = slow/dying |
| Switching frequency (TBI) | 2 – 3 Hz | < 0.5 Hz = slow/dying |
| Rise time | < 100 ms | > 100 ms = sluggish |
| Heater resistance | 4 – 14 Ω | open or shorted = fault |

### 12.2 Wideband (WIDEBAND_LINEAR) thresholds

| Metric | Healthy range |
|---|---|
| Pumping current Ip | -2 to +2 mA |
| Heater resistance | 2.5 – 10 Ω |
| Lambda direct read | 0.70 – 1.30 (linear) |

### 12.3 Sensor position canonical names

```
B1S1  = Bank 1 upstream (pre-cat, the primary feedback sensor)
B1S2  = Bank 1 downstream (post-cat, catalyst monitor)
B2S1  = Bank 2 upstream
B2S2  = Bank 2 downstream
```

### 12.4 Failure mode taxonomy

```python
class O2FailureMode(StrEnum):
    NO_FAULT            = "NO_FAULT"            # wiki: §6.7 — healthy baseline, no fault detected
    STUCK_LEAN          = "STUCK_LEAN"          # wiki: §6.7 — pinned < 0.2 V (narrowband)
    STUCK_RICH          = "STUCK_RICH"          # wiki: §6.7 — pinned > 0.85 V (narrowband)
    WIDEBAND_OFFSET_CANDIDATE = "WIDEBAND_OFFSET_CANDIDATE"  # wiki: o2-logic/03 §BIASED_OFFSET / o2-logic/08
```

### 12.5 Catalyst masking signals (cross-check rules)

- If `|obd_lambda − gas_lab_lambda| ≥ 0.08` → surface `perception_contradiction`
- Pre-cat ↔ post-cat switching ratio: if rear cross-count ≥ 0.5 × front → **suspect catalyst**, not the rear sensor (catalyst not storing oxygen, so rear sensor sees front signal)

---

## 13. Domain reference — Catalyst diagnostics (from `master_catalyst_guide.md`)

### 13.1 Operating envelope

| Parameter | Range |
|---|---|
| Lambda window for conversion | 0.97 – 1.03 |
| Light-off temperature | ~250 – 300 °C |
| Misfire damage threshold | > 1 % of combustion events |

### 13.2 Catalyst monitor enable conditions

Same gating envelope as fuel trim plus:

- ECT ≥ 70 °C
- Steady 2000 – 3000 RPM
- Closed loop
- No active P0300–P0312 (misfires — would damage cat)
- No active P0171/P0172/P0174/P0175 (mixture imbalance — confounds reading)
- ≥ 1 drive cycle since `codes_cleared`

### 13.3 Physical inspection thresholds

| Test | Pass | Fail |
|---|---|---|
| Idle backpressure | < 1.5 psi | ≥ 1.5 psi |
| 2500 RPM backpressure | < 3.0 psi | ≥ 3.0 psi |
| Snap-throttle peak | ≤ 5 psi | > 5 psi |
| IR delta (outlet − inlet) | ≥ 20 °C | < 20 °C = not converting |

### 13.4 Reference emissions table

| Gas | Pre-cat (engine-out) | Post-cat (with healthy cat) | Without cat |
|---|---|---|---|
| CO | ~0.65 % | < 0.10 % | 1.0 – 2.0 % |
| HC | ~250 ppm | < 35 ppm | 200 – 400 ppm |
| O₂ | low | low (< 0.5 %) | low |
| λ | varies | 0.995 – 1.005 | varies |
| CO₂ | 13 – 14 % | 14.5 – 16 % | 12 – 14 % |
| NO_x | high | < 100 ppm | high |

---

## 14. Domain reference — Historical fault context (from `DTClab.md`)

When the ECU stored a freeze frame, COMLab classifies the operating context to bias the differential diagnosis. The DTC Lab emits these states.

```python
class HistoricalFaultContext(StrEnum):
    HISTORICAL_IDLE_FAULT       = "HISTORICAL_IDLE_FAULT"
    HISTORICAL_LOAD_FAULT       = "HISTORICAL_LOAD_FAULT"
    COLD_START_TRANSIT_FAULT    = "COLD_START_TRANSIT_FAULT"
    UNKNOWN                     = "UNKNOWN"
```

Triggers:

| Context | Condition |
|---|---|
| `HISTORICAL_IDLE_FAULT` | `ff_engine_speed < 1000` AND `ff_calculated_load < 25.0` |
| `HISTORICAL_LOAD_FAULT` | `ff_engine_speed > 2000` AND `ff_calculated_load > 45.0` |
| `COLD_START_TRANSIT_FAULT` | `ff_coolant_temp < 60` °C |

---

## 15. Domain reference — Ideal stoichiometric values (from `Gas Lab Wiki DTC Code Matching`)

Reference values for a healthy stoichiometric engine at steady state. Used by Gas Lab; cross-referenced here for completeness.

| Gas | Healthy value |
|---|---|
| CO | < 0.5 % |
| HC | < 35 ppm |
| O₂ | 0.0 – 0.5 % |
| CO₂ | 14.5 – 16 % |
| NO_x | < 100 ppm |
| λ | 0.995 – 1.005 |

**PCM trim limit:** ECU saturates STFT/LTFT at approximately −15% to −25% before setting P0172/P0175.

**Misfire signature math:** O₂ rise ≈ 21% atmospheric ÷ N cylinders. Example: one dead cylinder on a 4-cylinder engine produces O₂ ≈ 5.25 %.

---

## 16. Domain reference — extended PIDs and baselines (from `OBD Live PID Diagnostic Profiles.md`, `OBDadd1.md`)

### 16.1 Additional PIDs beyond the 8-PID minimalist schema

The 8-PID core covers mainline diagnostics. These additional PIDs add resolution for ignition timing, idle control, and intake correction — they're optional inputs that COMLab routes through when available.

| 4DLab canonical name | ISO 15031-5 PID | SAE J1979 PID | Description | Unit | Source |
|---|---|---|---|---|---|
| `absolute_engine_load_pct` | `0143` | `0143` | Absolute load (mass air per intake stroke vs. peak torque %) | % | ISO 15031-5 / J1979 |
| `iac_step` / `iac_counts` | (mfg-specific) | (mfg-specific) | Idle air control bypass step/counts | step | manufacturer-specific |
| `timing_advance_deg_btdc` | `010E` | `010E` | Spark advance before TDC | ° | ISO 15031-5 / J1979 |
| `knock_retard_deg` | (mfg-specific) | (mfg-specific) | PCM-commanded knock retard | ° | manufacturer-specific |
| `intake_air_temp_c` | `010F` | `010F` | Intake air temperature | °C | ISO 15031-5 / J1979 |
| `fuel_rail_pressure_kpa` | `0123` | `0123` | GDI/MPI rail pressure | kPa | ISO 15031-5 / J1979 |
| `o2_sensor_voltage_b1s1` | `0114` | `0114` | Bank 1 Sensor 1 narrowband voltage | V | ISO 15031-5 / J1979 |
| `fuel_system_status` | `0103` | `0103` | Closed-loop / open-loop / fault | enum | ISO 15031-5 / J1979 |

### 16.2 Quantitative MAF baselines

Per `OBD Live PID Diagnostic Profiles.md`:

| State | MAF reading (per liter displacement) |
|---|---|
| Curb idle (~800 RPM) | ~1 g/s per liter |
| Stress idle (~4000 RPM, no load) | 3 – 5 g/s per liter, ~4× idle MAF |
| WOT acceleration | up to 8 – 10 g/s per liter |

**Double Whammy MAF skew:** MAF that **over-reads at low velocities** and **under-reads at high velocities** is the signature of a contaminated hot-wire sensor. Trims look fine at idle but go significantly positive at 4000 RPM.

### 16.3 Timing advance baselines

| State | Spark advance |
|---|---|
| Curb idle | 5 – 15° BTDC |
| 4000 RPM (no load) | 25 – 40° BTDC |
| WOT (premium fuel) | 30 – 35° BTDC |
| **Knock retard active** | baseline minus 5 – 15° |

Rule: if `timing_advance_deg_btdc` at 4000 RPM is **significantly below baseline** AND `knock_retard_deg` > 0, PCM is reacting to detonation — investigate fuel octane, carbon buildup, or cooling.

### 16.4 Sample validity gate (chemistry)

Per `OBDadd1.md` — Validity Step-0:

> If `CO + CO₂ + O₂` (volume %) is not between **14 % and 18 %**, mark `SAMPLE_INVALID` and abort downstream evaluation. Air ingress at the probe or analyzer fault.

This rule lives at the Gas Lab boundary but COMLab respects it — a `SAMPLE_INVALID` payload triggers `FATAL_INCOMPLETE` degradation.

---

## 17. Domain reference — Chemical signature enum (30 values, from `OBDadd1.md`)

These are the canonical fault-signature labels the Gas Lab emits in its `chemical_state` field. COMLab consumes them as opaque tokens and routes via the fault registry. Listed here so the vocabulary module can declare them as a sealed enum.

```python
class ChemicalSignature(StrEnum):
    NORMAL_OPERATION                   = "NORMAL_OPERATION"
    RICH_MIXTURE                       = "RICH_MIXTURE"
    LEAN_MIXTURE                       = "LEAN_MIXTURE"
    IGNITION_MISFIRE                   = "IGNITION_MISFIRE"
    LEAN_MISFIRE                       = "LEAN_MISFIRE"
    RICH_MISFIRE                       = "RICH_MISFIRE"
    EXHAUST_AIR_LEAK                   = "EXHAUST_AIR_LEAK"
    HIGH_COMBUSTION_TEMP               = "HIGH_COMBUSTION_TEMP"
    CATALYST_NOT_LIGHTING_OFF          = "CATALYST_NOT_LIGHTING_OFF"
    CATALYST_OVERWHELMED               = "CATALYST_OVERWHELMED"
    SAMPLE_INVALID                     = "SAMPLE_INVALID"
    TIMING_OVER_ADVANCED               = "TIMING_OVER_ADVANCED"
    TIMING_RETARDED                    = "TIMING_RETARDED"
    O2_SENSOR_BIASED_LOW               = "O2_SENSOR_BIASED_LOW"
    O2_SENSOR_BIASED_HIGH              = "O2_SENSOR_BIASED_HIGH"
    WORN_ENGINE                        = "WORN_ENGINE"
    FLAT_CAMSHAFT                      = "FLAT_CAMSHAFT"
    GDI_INTAKE_VALVE_CARBON            = "GDI_INTAKE_VALVE_CARBON"
    VACUUM_REGULATOR_DIAPHRAGM_RUPTURE = "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE"
    GDI_HPFP_INTERNAL_SEAL_LEAK        = "GDI_HPFP_INTERNAL_SEAL_LEAK"
    WORN_VALVE_SEALS                   = "WORN_VALVE_SEALS"
    WORN_PISTON_RINGS                  = "WORN_PISTON_RINGS"
    POA_SIGNATURE                      = "POA_SIGNATURE"
    WRONG_VALVE_TIMING                 = "WRONG_VALVE_TIMING"
    EGR_STUCK_CLOSED                   = "EGR_STUCK_CLOSED"
    EGR_STUCK_OPEN                     = "EGR_STUCK_OPEN"
    VVT_FAILURE                        = "VVT_FAILURE"
    EVAP_CANISTER_SATURATED            = "EVAP_CANISTER_SATURATED"
    EGR_DILUTION_MISFIRE               = "EGR_DILUTION_MISFIRE"
    INCOMPLETE_OXIDATION               = "INCOMPLETE_OXIDATION"
```

Note: `WRONG_VALVE_TIMING` and `POA_SIGNATURE` use underscores here (the source uses dashes / spaces — normalized for code).

---

## 18. Domain reference — Trim Delta rules (from `OBDadd1.md`)

### 18.1 Opposing-Values Delta rule

> If **STFT and LTFT have opposite signs**, the fault is currently **healing or recently repaired**. The PCM is reversing a learned correction because the underlying condition went away.

Example: LTFT +12% (learned compensation for past lean condition) but STFT -4% (currently slightly rich) → vacuum leak was repaired but adaptive memory hasn't reset yet.

### 18.2 Matching-Values Delta rule

> If **STFT and LTFT have the same sign and similar magnitude**, the fault is **active and severe**. Both immediate and adaptive corrections are agreeing on the direction.

Example: STFT +18%, LTFT +22% → real lean condition right now.

### 18.3 Cross-bank asymmetry rule

For V engines with two banks, compare `B1_STFT/B1_LTFT` against `B2_STFT/B2_LTFT`:

| Pattern | Interpretation |
|---|---|
| One bank's trims drift, other is normal | **Single-bank fault**: intake gasket on that bank, clogged injectors that bank, exhaust pre-cat leak that side |
| Both banks drift in same direction | **Common-mode fault**: fuel pump/regulator, MAF contamination, intake leak post-MAF, EVAP/EGR |
| Banks drift in opposite directions | **Sensor fault** on at least one bank, OR exhaust crossover/swap |

### 18.4 Ghost Misfire rule

> If misfire counters increment but `total_trim_correction_delta` and wideband lambda look normal, suspect **alternator AC ripple** corrupting the ignition primary signal. Check charging system ripple before chasing coils.

---

## 19. Domain reference — Mode 06 universal MID inventory (from `OBDadd1.md`)

Ten universal Mode 06 MIDs (Monitor IDs) covered across most petrol vehicles 2008+. The DTCLab `mode_06_hex_dictionary.json` is seeded from this table.

| MID range | Monitor | TID examples |
|---|---|---|
| `$A1` – `$A6+` | Misfire per cylinder (one MID per cylinder) | `$0B` = accumulator count |
| `$21` / `$22` | Catalyst Bank 1 / Bank 2 efficiency (OSC) | `$81` = OSC test, `$80` = light-off |
| `$01` / `$02` | O₂ sensor response time, B1S1 / B1S2 | `$01` rich→lean, `$07` lean→rich, `$08` switch period |
| `$05` / `$06` | O₂ heater performance, B1 / B2 | `$01` heater current |
| `$31` – `$3A` | EVAP leak testing (size-graded: gross → small → very small) | `$83` = 0.040", `$84` = 0.020" |
| `$3B` / `$3C` | EGR flow / cooler bypass | `$80` flow rate |
| `$3D` | VVT phaser accuracy (degree error) | `$84` phase delta |
| `$13` | Fuel system monitor (rail pressure, injector volume) | `$80` rail pressure target |
| `$71` | Secondary Air Injection | `$80` flow test |
| `$81` / `$82` | Fuel rail pressure sensor (modern GDI) | `$83` HPFP duty cycle |
| `$E1` | Thermostat / cooling | `$80` warm-up time vs spec |

Some sources use CID (Component ID) numbering — `CID $A2-$A9` for misfire, `CID $0C` for catalyst — interchangeable with the MID numbering above on most ECUs.

---

## 20. Domain reference — Mode 06 margin math (from `OBDadd1.md`)

Mode 06 reports raw values bounded by a min and/or max limit. Margin is the safety distance from limit, expressed as percentage. Three formulas depending on which bounds are present:

| Limit type | Formula | Notes |
|---|---|---|
| Max-only | `Margin% = (1 − Current/Max) × 100` | Lower is healthier (e.g., misfire count vs cap) |
| Min-only | `Margin% = ((Current − Min) / Current) × 100` | Higher is healthier (e.g., O2 switching speed) |
| Window | based on window range, normalized to 0-100% | Use for fuel rail pressure, OSC tests |

### 20.1 Three-tier color classification

| Margin | Color | Status enum |
|---|---|---|
| ≤ 0 % | RED | `CRITICAL_FAIL` |
| 1 – 15 % | YELLOW | `PENDING_FAIL_MARGINAL` |
| 16 – 100 % | GREEN | `PASSED` |

(Aligned with §11 Mode 06 status tri-state in `DTC_VOCABULARY.md`.)

---

## 21. Domain reference — Diagnostic decision tree (from `OBDadd1.md`)

The orchestrator should walk this decision tree before consulting the fault registry. Each step prunes the candidate set.

```
Step 0  Sample validity (CO+CO2+O2 in 14-18%)
   ├─ FAIL  -> emit SAMPLE_INVALID, abort
   └─ PASS  -> Step 1

Step 1  Trim + lambda branch
   ├─ STFT/LTFT positive AND lambda > 1.02   -> LEAN branch (Step 2A)
   ├─ STFT/LTFT negative AND lambda < 0.98   -> RICH branch (Step 2B)
   ├─ Trims neutral AND lambda neutral       -> Misfire branch (Step 2C)
   └─ Trim direction vs lambda contradicts   -> Sensor bias / Perception fault

Step 2A LEAN branch
   ├─ Trims drop toward normal at 4000 RPM   -> vacuum leak
   ├─ Trims worsen at 4000 RPM               -> fuel delivery (pump/filter/regulator)
   ├─ Single-bank asymmetry                  -> bank-specific intake/injector
   └─ Both banks, MAF reads low for RPM      -> MAF under-read (contaminated)

Step 2B RICH branch
   ├─ Bank-asymmetric negative                -> leaking injector on that bank
   ├─ LTFT pegged at -25% AND chemistry rich  -> unmetered fuel intrusion (HPFP / regulator)
   ├─ Stuck-rich post-cat O2                  -> evaporative HC source / canister
   └─ Stable rich AND timing retarded         -> fuel pressure too high

Step 2C Misfire branch
   ├─ Single-cylinder misfire scaling with RPM -> coil or plug wire
   ├─ Multi-cylinder same bank               -> bank-shared ignition or fuel
   ├─ Random under load only                  -> coil insulation under cylinder pressure
   └─ Counters rise but trims neutral         -> ghost misfire (alternator ripple)

Step 3  Special cases
   ├─ HC normal-high, CO low, lambda ~1      -> POA (oil burning)
   ├─ Lambda normal, CO/HC both elevated     -> catalyst overwhelmed
   ├─ Cold-start spike only                   -> thermostat / coolant
   └─ Mode $06 fail + no DTC                  -> early warning, surface to UI
```

---

## 22. What the 4DLab vocabulary explicitly does NOT define

Listed for clarity — these belong to upstream modules and are NOT in the COMLab vocabulary:

- Gas Lab `chemical_state` strings (`IGNITION_MISFIRE`, `UNMETERED_FUEL_INTRUSION`, etc.) — owned by GASLab module, consumed by COMLab as opaque labels.
- Specific fault node IDs (`Mechanical_Lean_Vacuum_Leak`, etc.) — owned by the cases corpus + fault registry, consumed by COMLab.
- Manufacturer-specific Mode 06 hex IDs — owned by DTCLab's `mode_06_hex_dictionary.json`.

---

## 23. Domain reference — ECT operational thresholds (NEW per registry overheating family)

SAE J1979 PID `0105` defines the coolant temperature range (-40 to 215°C) but not diagnostic thresholds. The operational bands below derive from automotive diagnostic best practice (Brady/Hall, SAE J1667 warm-up diagnostics, and the SAE J1979 coolant-temperature PID rationale). Each threshold is a boundary where the ECU or engine physics change behaviour.

### 23.1 ECT diagnostic bands

| Band | ECT range | ECU / engine behaviour | Diagnostic meaning |
|---|---|---|---|
| `COLD_OPEN_LOOP` | < 70°C | Open-loop enrichment active; closed-loop fuel control disabled | Trim analytics frozen — engine not evaluable |
| `WARMUP_TRANSITION` | 70 – 88°C | Closed-loop enabled; thermostat still closed | Normal warm-up behaviour — valid but not at equilibrium |
| `NORMAL_OPERATING` | 88 – 95°C | Thermostat open; steady-state coolant temp | Normal operating range — all diagnostics valid |
| `FAN_RANGE` | 95 – 105°C | Radiator fan cycles; ECU maintains temp within band | Normal under load or hot ambient — fan-on is expected |
| `ELEVATED_TEMP` | 105 – 110°C | Fan running continuously; no DTC yet | Thermostat sticking, fan degradation, or coolant loss — still below dash warning |
| `OVERHEATING_THRESHOLD` | ≥ 108°C | Sustained at idle is diagnostic for cooling-system fault; ECU may limit timing | Cooling system fault probable — fan failure, stuck-closed thermostat, or coolant loss |
| `SEVERE_OVERHEAT` | ≥ 115°C | ECU forces OL_FAULT enrichment to cool catalyst; dash warning light triggers | Active overheating — stop-and-inspect urgency |
| `CRITICAL_OVERHEAT` | ≥ 120°C | Head-gasket damage risk; coolant boiling risk at ambient pressure | Critical — engine damage imminent per SAE J1979 coolant-range safety margin |

### 23.2 Idle RPM in overheating context

The ECU may raise the target idle RPM when overheating is detected, to increase water-pump speed and fan airflow for convective cooling. This is distinct from the normal STABILIZED_IDLE band in §3.3.

| RPM band | Range | Meaning |
|---|---|---|
| `NORMAL_HOT_IDLE` | 650 – 900 RPM | Normal warm-engine idle (STABILIZED_IDLE bucket per §3.3) |
| `ECU_COOLING_IDLE` | 1000 – 1200 RPM | ECU-elevated idle target during detected overheat — drives water pump and fan faster |
| `IDLE_NOT_ELEVATED` | < 1000 RPM | No ECU cooling response — fan failure scenario where ECU has not detected the overheat, or overheat is below ECU intervention threshold |

The diagnostic discriminator: ECT ≥ 108°C with RPM ≥ 1000 RPM suggests the ECU has detected the overheat and commanded a cooling response. ECT ≥ 105°C with RPM < 1000 RPM suggests the ECU has NOT detected the overheat (fan failure, gradual coolant loss below the sensor threshold, or thermostat sticking without the ECU flagging the temperature as abnormal).

### 23.3 Combined ECT + RPM diagnostic matrix

| ECT | RPM | Interpretation |
|---|---|---|
| ≥ 108°C | ≥ 1000 RPM | ECU-detected overheat — thermostat stuck closed, coolant loss, or fan failure with ECT sensor capturing the temperature |
| ≥ 105°C | < 1000 RPM | Undetected overheat — fan failure where ECT sensor location misses the hot spot, or gradual coolant loss below sensor detection threshold |
| 95 – 105°C | any | Normal hot-running — fan cycling; not diagnostic for a fault |
| < 88°C | any | Engine not at operating temperature — cooling-system diagnostics deferred |

---
## 12. Standards references (sources)

- SAE J1979 OBD-II PID list — [GitHub OBDb/SAEJ1979](https://github.com/OBDb/SAEJ1979), [Wikipedia OBD-II PIDs](https://en.wikipedia.org/wiki/OBD-II_PIDs), [CSS Electronics PID table](https://www.csselectronics.com/pages/obd2-pid-table-on-board-diagnostics-j1979)
- BAR Two-Speed Idle Test (2500 RPM specification) — [smog-tech-training.com](https://www.smog-tech-training.com/Two-Speed-Smog-Inspection.html), [Bureau of Automotive Repair cutpoints](https://www.bar.ca.gov/industry/tsi-cutpoints-table)
- Virginia 9VAC5-91-440 two-speed idle spec (2200-2800 band) — [law.lis.virginia.gov](https://law.lis.virginia.gov/admincode/title9/agency5/chapter91/section440/)
- Snap throttle test (PicoAuto methodology) — [picoauto.com](https://www.picoauto.com/library/automotive-guided-tests/intake-manifold-pressure-during-snap-test-gasoline/)
- Ignition coil under-load testing rationale — [Standard Motor Products](https://www.standardbrand.com/en/products/ignition/ignition-coils/ignition-coil-breakdown-and-testing), [aa1car.com ignition coils](https://www.aa1car.com/library/ignition_coils.htm)
