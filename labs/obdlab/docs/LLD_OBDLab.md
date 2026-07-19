---
node_type: "lld"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "detailed-design"
implements:
  - "labs/obdlab/obdlab/core/ve_engine.py"
  - "labs/obdlab/obdlab/core/o2_normalizer.py"
  - "labs/obdlab/obdlab/core/trim_vector_aggregator.py"
consumers:
  - "dld: labs/obdlab/docs/DLD_OBDLab.md"
drift_guards:
  - "labs/obdlab/tests/unit/test_ve_engine.py"
  - "labs/obdlab/tests/unit/test_o2_normalizer.py"
  - "labs/obdlab/tests/unit/test_trim_vector_aggregator.py"
tags: [obdlab, finished, lld]
source: "labs/obdlab/docs/LLD_OBDLab.md"
---
# LLD — OBDLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_OBDLab v1.0
**HLD / DLD Reference:** HLD_OBDLab v2.0 / DLD_OBDLab v2.0
**Version:** 2.0
**Date:** 2026-06-10
**Supersedes:** LLD_OBDLab v1.0 (2026-05-22).

Convention: every numeric literal in `obdlab/` carries a `# wiki: <source>`
comment (code-review gate). The literals below are transcribed from the live
modules; the `# wiki:` source is shown alongside each.

---

## 1. Physical Constants (`core/ve_engine.py`)

```python
MM_AIR:   float = 28.97   # wiki: §10.1 — molar mass dry air, g/mol
R_GAS:    float = 8.314   # wiki: §10.1 — universal gas constant, J/(mol·K)
K_OFFSET: float = 273.15  # wiki: §10.1 — °C → K offset
```

`core/maf_linearity.py` carries its own constants (different formula family):

```python
R:           float = 0.287   # wiki: research/chunks/pids-protocol/05 — specific gas constant air, kJ/(kg·K)
CONSTANT_120: float = 120.0  # wiki: research/chunks/pids-protocol/05 — 4-stroke/60s factor
K_OFFSET:    float = 273.15  # wiki: research/chunks/pids-protocol/05
PERCENT_MULT: float = 100.0  # wiki: research/chunks/pids-protocol/05
```

---

## 2. Physical Sensor Bounds (`config/physical_sensor_bounds.json`)

Source: `OBDLab_KG_Wiki.md §3.1`. **12 fields** (was 10 in v1.0 — `intake_air_temp_c`
and `throttle_pos_pct` added in T-OBDV2-7; `control_module_voltage_v` in
T-OBDV2-8). Adding a field requires a wiki update and a `test_sensor_bounds.py`
update.

| Field | min | max | unit | Note |
|-------|-----|-----|------|------|
| `engine_rpm` | 0 | 8000 | RPM | |
| `coolant_temp_c` | −40.0 | 140.0 | °C | |
| `calculated_engine_load_pct` | 0.0 | 100.0 | % | |
| `mass_airflow_gps` | 0.0 | 655.35 | g/s | |
| `manifold_vacuum_kpa` | 0.0 | 255.0 | kPa | |
| `shrtft1` | −127.0 | 127.0 | % | widened from OBD-nominal [−100, 99.22] (T-W-6) |
| `longft1` | −127.0 | 127.0 | % | widened (T-W-6) |
| `shrtft2` | −127.0 | 127.0 | % | only validated when `number_of_banks == 2` |
| `longft2` | −127.0 | 127.0 | % | only validated when `number_of_banks == 2` |
| `intake_air_temp_c` | −40.0 | 140.0 | °C | |
| `throttle_pos_pct` | 0.0 | 100.0 | % | |
| `control_module_voltage_v` | 0.0 | 18.0 | V | PCM pin supply per ecu-diagnosis/09 |

**Rail-value rationale (T-W-6):** trims were widened to the OBD rail `±127`
because a railed trim is itself a *sensor-fault signal* consumed by COMLab
trim-evidence scoring; rejecting it as out-of-bounds would lose that signal.

**Bank-2 null contract:** `shrtft2`/`longft2` must be `null` (not `0.0`) when
`number_of_banks == 1`. Emitting `0.0` for an absent bank is a
`SEMANTIC_CONTRACT §4.4` violation.

---

## 3. Unit Conversion Factors (`core/pid_ingestion_validator.py`)

Source: `OBDLab_KG_Wiki.md §3.2`. `{alternate_suffix: (canonical_suffix, fn)}`.

```python
"_f"     → "_c":   (v - 32.0) * 5.0 / 9.0   # °F → °C
"_psi"   → "_kpa": v * 6.895                # psi → kPa
"_inhg"  → "_kpa": v * 3.386                # inHg → kPa
"_lbmin" → "_gps": v * 7.559                # lb/min → g/s
```

Canonical key wins: if both `coolant_temp_c` and `coolant_temp_f` are present,
the `_c` value is kept and `_f` dropped.

---

## 4. DNA-RPM Gate (`core/pid_ingestion_validator.py`)

```python
_DNA_RPM_HEADROOM = 1.05  # wiki: §3 — 5% redline overshoot headroom

# HIGH confidence only, rated_rpm set:
if engine_rpm > rated_rpm * _DNA_RPM_HEADROOM:
    raise PIDValidationError(...)
```

Three-branch confidence: **HIGH** strict (raises), **PARTIAL** logs
`dna_check_downgraded` and falls through to static bounds, **NONE/None** skips
(static `[0, 8000]` only).

---

## 5. VE Formula (`core/ve_engine.py::_calc_ve_standard`)

Source: `OBDLab_KG_Wiki.md §10.1`. Implementation places R in the numerator and
MM_AIR in the denominator (physically correct unit placement; the wiki prose has
R/MM transposed — code is the truth).

```python
iat_k        = iat_c + K_OFFSET                                  # wiki: §10.1
numerator    = maf * R_GAS * iat_k                              # wiki: §10.1 — R in numerator
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

---

## 6. Target VE Constants for Emulation (`core/ve_engine.py::_EXPECTED_VE`)

Source: `OBDLab_KG_Wiki.md BP §1.B / §1.C`. Keyed by `(bucket, strategy)`:

| Bucket | `MAP_ONLY_SPEED_DENSITY` | `MAF_ONLY` |
|--------|--------------------------|------------|
| `STABILIZED_IDLE` | 0.65 | 0.70 |
| `REGULATORY_HIGH_IDLE` | 0.80 | 0.82 |
| `STRESS_IDLE` | 0.80 | 0.82 |

(v1.0 listed only 4 entries; the current table has all 6 — both strategies cover
`REGULATORY_HIGH_IDLE`.)

---

## 7. VE Validity Classification (`core/ve_engine.py::_classify_validity`)

Source: `OBDLab_KG_Wiki.md §6.4`. Thresholds:

```python
_CUTOFF_VE_COLLAPSE       = 50.0  # VE% — idle collapse floor
_CUTOFF_MAP_COLLAPSE      = 45.0  # MAP kPa — must exceed for collapse trigger (BP §2)
_CUTOFF_VE_CONTAMINATION  = 65.0  # VE% — MAF contamination floor
_CUTOFF_TFT_CONTAMINATION = 15.0  # TFT% — contamination requires trim above this
_CUTOFF_VE_SKEW           = 90.0  # VE% — sensor skew ceiling
```

```
FAULT_VE_IDLE_COLLAPSE:  bucket==STABILIZED_IDLE AND ve<50 AND map>45
FAULT_MAF_CONTAMINATION: bucket∈{STRESS_IDLE, REGULATORY_HIGH_IDLE} AND ve<65 AND tft>15
FAULT_VE_SENSOR_SKEW:    bucket==STABILIZED_IDLE AND ve>90 AND induction==NATURALLY_ASPIRATED
otherwise:               VALID
```

`FAULT_VE_SENSOR_SKEW` is the replacement for the removed Physics_Gate_3
(FIX-1 Option B). When `total_trim_correction_delta` is not yet on the dict,
`_classify_validity` recomputes TFT from `shrtft1 + longft1`.

---

## 8. O2 Normaliser Boundaries (`core/o2_normalizer.py`)

Source: `OBDLab_KG_Wiki.md §11.1`.

```python
_ZONE_MIN_VOLTAGE     = 0.10   # min valid narrowband V
_ZONE_LEAN_BOUNDARY   = 0.40   # LEAN upper bound (V)
_ZONE_STOICH_BOUNDARY = 0.50   # STOICH upper bound (V)
_ZONE_MAX_VOLTAGE     = 0.90   # max valid narrowband V

_LAMBDA_LEAN   = 1.05   # 0.10–0.40 V
_LAMBDA_STOICH = 1.00   # 0.41–0.50 V
_LAMBDA_RICH   = 0.95   # 0.51–0.90 V

_LAMBDA_MIN = 0.7   # wideband passthrough floor (§5)
_LAMBDA_MAX = 1.3   # wideband passthrough ceiling (§5)

_LAMBDA_STOICH_TARGET      = 1.0    # wideband offset reference (o2-logic/03)
_WIDEBAND_OFFSET_THRESHOLD = 0.05   # |ratio−1.0| trigger (o2-logic/03 / 08)
```

**Boundary ownership & fault mapping:**

| Input | Result |
|-------|--------|
| `v == 0.40` | LEAN (λ 1.05) |
| `v == 0.41` | STOICH (λ 1.00) |
| `v == 0.50` | STOICH (λ 1.00) |
| `v == 0.51` | RICH (λ 0.95) |
| `v < 0.10` | `O2_CHANNEL_FAULT`, λ clamped 1.05, **STUCK_LEAN** |
| `v > 0.90` | `O2_CHANNEL_FAULT`, λ clamped 0.95, **STUCK_RICH** |
| wideband `ratio < 0.7` | `O2_CHANNEL_FAULT`, clamp 0.7, NO_FAULT |
| wideband `ratio > 1.3` | `O2_CHANNEL_FAULT`, clamp 1.3, NO_FAULT |
| wideband, warm+CL+not WOT+not DFCO, `\|ratio−1.0\| > 0.05` | `WIDEBAND_PASSTHROUGH`, **WIDEBAND_OFFSET_CANDIDATE** |

`WIDEBAND_NB_SIM` uses the identical voltage map as narrowband but reports
`WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA` so COMLab can apply the WB-sim trim weight.

---

## 9. Semantic Consistency Thresholds (`core/semantic_consistency_checker.py`)

```python
_TRIM_MIN            = -127.0  # Physics_Gate_4 (widened, T-W-6)
_TRIM_MAX            =  127.0  # Physics_Gate_4 (widened, T-W-6)
_CUTOFF_ECT_COLD     =  75     # thermal gate cutoff (°C), §4.1
_CUTOFF_ECT_CLOSED   =  80     # Physics_Gate_2 closed-loop-expected (°C), §4
_CUTOFF_VSS          =  10     # Physics_Gate_1 VSS (km/h)
_CUTOFF_RPM_STALLED  =  400    # Physics_Gate_1 stalled-RPM (RPM)
```

Gate set is **1, 2, 4** (no Gate 3). `gates_passed` collects the three; the
orchestrator's `semantic_gates_passed = (len(gates_passed) == 3)`. A violated
gate **raises** (`SemanticConsistencyError`) and propagates out of `translate`,
so `TrimAnalyticsGate.SEMANTIC_ERROR` is a defensive path rather than a normal
return value.

---

## 10. Analytics Preconditions (`core/analytics_preconditions.py`)

```python
ECT_WARM_THRESHOLD     = 70   # Gate 1 — coolant warm (°C), §9
WOT_THROTTLE_THRESHOLD = 90   # Gate 6 — WOT throttle (%), §9
```

```python
O2_FAULT_DTCS = frozenset({          # 32 codes, §9
    P0130–P0135,   # B1S1
    P0136–P0141,   # B1S2
    P0142–P0149,   # (continuous range to P0161)
    P0150–P0155,   # B2S1
    P0156–P0161,   # B2S2
})
CKP_CMP_FAULT_DTCS = frozenset({"P0335", "P0340"})  # CKP / CMP circuit
```

(The codeset is the literal contiguous range `P0130`…`P0161` = 32 entries.)
Maintained locally; COMLab keeps them in sync with DTCLab routing.

Gate 6 reads `throttle_pos` from the PID dict; Gate 2 reads `fuel_system_status`
(falling back to `fuel_sys_status`), coerced via `FuelSystemStatus.from_wire`.

---

## 11. MAF Linearity (`core/maf_linearity.py`)

Source: `research/chunks/pids-protocol/05`.

```python
W_theo = (eta_v * displacement * map_kpa * rpm) / (120.0 * R(0.287) * (iat_c + 273.15))

ΔSensor_error =
    ( |maf_stress − W_theo_stress| / W_theo_stress
    − |maf_idle   − W_theo_idle|   / W_theo_idle ) * 100.0
```

Both guard against a zero denominator (return `0.0`). Emitted only under
`DUAL_MAF_MAP_CROSSCHECK` once the `LinearityAccumulator` holds **both** the
`STABILIZED_IDLE` and `STRESS_IDLE` bands.

---

## 12. Cold-Engine Payload Defaults (`core/sensor_signal_translator.py`)

When the thermal gate fires (`rpm_bucket == COLD_OPEN_LOOP_INVALID`,
`analytics_frozen = True`):

```python
ve_pct                       = 0.0
maf_status                   = NodeMAFStatus.REAL_SENSOR_FEED
map_status                   = NodeMAPStatus.REAL_SENSOR_FEED
ve_validity                  = VEValidity.UNKNOWN
normalized_obd_lambda        = 1.0
o2_failure_mode              = O2FailureMode.NO_FAULT
total_trim_correction_delta  = 0.0
total_trim_correction_delta_b2 = None
per_bank_trim_delta          = None
```

`AnalyticsPreconditions` still runs and populates `trim_analytics_gate`
(it will return `ENGINE_COLD`). Not configurable in v1.

---

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

---

## 14. `freeze_frame_pids` Forwarding Contract

`OBDLivePayload.freeze_frame_pids` (default `{}`) is populated by **COMLab**
before the OBDLab call, from DTCLab freeze-frame data — OBDLab ferries it
through unchanged. OBDLab never reads DTCLab directly (no cross-lab import).

---

## 15. Error Types

| Error | Raised when |
|-------|-------------|
| `PIDValidationError(ObdLabError)` | bounds violation; DNA-RPM HIGH breach; bank-2 null contract; non-numeric PID; invalid fuel-status / misfire / cell-vector input |
| `SemanticConsistencyError(ObdLabError)` | Physics_Gate_1 / 2 / 4 violation |
| Pydantic `ValidationError` | `OBDLivePayload` field-constraint violation at assembly |

---

## 16. Forbidden Patterns (OBDLab-specific)

| Pattern | Enforcement |
|---------|-------------|
| `from gaslab/dtclab/comlab/dnalab/vinlab import …` | import-isolation audit (test suite) |
| `HIGH_IDLE_LOAD` anywhere in `obdlab/` | `test_vocabulary.py` codebase scan |
| Numeric literal without `# wiki:` comment | code-review gate |
| New `OBDLivePayload` field without a named consumer | signal/noise rule — field does not ship |
| Diesel-specific logic | `PRD_4D_App.md §5` scope exclusion |
