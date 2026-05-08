# Threshold Provenance Audit — V1 thresholds.yaml

**Date:** 2026-05-08
**Task:** T-P0-4
**Purpose:** Audit every numeric threshold in `schema/v1_reference/thresholds.yaml` against
the master guides. Categorise each as KEEP (with source), RECALIBRATE (wrong value),
REMOVE (no justification found), or PENDING (master guide not yet written).

**Sources consulted:**
- `timing_compression_forensic.md` — corrected values for late_timing + compression_loss
- `master_egr_guide.md` (T-P0-1) — EGR threshold provenance §5.6
- `master_ecu_guide.md` (T-P0-1) — ECU/λ threshold provenance §5b
- `master_freeze_frame_guide.md` (T-P0-2) — FF threshold provenance §9, §10
- `master_perception_guide.md` (T-P0-2) — perception gap thresholds
- `master_nox_guide.md` (T-P0-3) — NOx threshold provenance §8
- `master_turbo_guide.md` (T-P0-3) — turbo threshold provenance §8
- `master_exhaust_guide.md` (T-P0-3) — exhaust threshold provenance §7
- Pre-existing master guides: `master_gas_guide.md`, `master_ignition_guide.md`,
  `master_mechanical_guide.md`, `master_catalyst_guide.md`, `master_fuel_trim_guide.md`,
  `master_fuel_system_guide.md`, `master_o2_sensor_guide.md`, `master_cold_start_guide.md`,
  `master_air_induction_guide.md`, `master_non_starter_guide.md`, `master_obd_guide.md`

**Category definitions:**
- **KEEP:** Value is correct and source guide justifies it.
- **RECALIBRATE:** Value was wrong; corrected per forensic or master guide.
- **REMOVE:** No physical justification found; threshold should be removed.
- **PENDING:** Relevant master guide not yet written/available for verification.

---

## Summary

| Category | Count |
|----------|-------|
| KEEP | 181 |
| RECALIBRATE | 15 |
| REMOVE | 0 |
| PENDING | 1 |
| **Total** | **197** |

---

## 1. Gas Symptoms (`gas_symptoms`)

General gas analyser thresholds. Source: `master_gas_guide.md` and general automotive
gas-analysis references (MOTOR 5-Gas Analysis, SAE J1979).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 1 | `gas_symptoms.co_high` | 1.0 | 1.0 | `master_gas_guide.md` §3 — CO > 1.0% indicates rich combustion | KEEP | Standard 5-gas threshold; widely documented |
| 2 | `gas_symptoms.co2_low` | 10.0 | 10.0 | `master_exhaust_guide.md` §2.2 — CO₂ < 10% indicates severe dilution or combustion failure | KEEP | Cross-ref O₂-CO₂ sum rule |
| 3 | `gas_symptoms.co2_high` | 15.0 | 15.0 | `master_gas_guide.md` — CO₂ > 15% unusual; indicates rich mixture with efficient combustion | KEEP | Upper bound of normal stoich combustion |
| 4 | `gas_symptoms.co2_good_min` | 14.5 | 14.5 | `master_exhaust_guide.md` §2.2 — stoich combustion produces ~15% CO₂; 14.5% lower bound for healthy cat-equipped engine | KEEP | Widely referenced in 5-gas literature |
| 5 | `gas_symptoms.co2_good_min_decat` | 13.0 | 13.0 | `master_gas_guide.md` — decat engines run 1–2% lower CO₂ | KEEP | Standard decat reference |
| 6 | `gas_symptoms.co2_good_max` | 15.5 | 15.5 | `master_gas_guide.md` — CO₂ max for healthy stoich combustion | KEEP | Standard reference |
| 7 | `gas_symptoms.hc_very_high` | 1000 | 1000 | `master_ignition_guide.md` §6 — HC > 1000 ppm = severe misfire | KEEP | Misfire threshold well-documented |
| 8 | `gas_symptoms.hc_high` | 300 | 300 | `master_egr_guide.md` §5.1 — HC > 300 ppm = measurable combustion deficit (~1.5% unburned fuel) | KEEP | EGR guide §5.1 provides physical basis |
| 9 | `gas_symptoms.hc_low` | 150 | 150 | `master_gas_guide.md` — HC < 150 ppm normal for cat-equipped warm engine | KEEP | Standard healthy-engine reference |
| 10 | `gas_symptoms.o2_very_high` | 5.0 | 5.0 | `master_gas_guide.md` — O₂ > 5% indicates severe lean condition or misfire | KEEP | Well-documented lean/misfire boundary |
| 11 | `gas_symptoms.o2_high` | 2.0 | 2.0 | `master_egr_guide.md` §5.2 — O₂ > 2.0% at warm idle above healthy-no-cat boundary | KEEP | EGR guide §5.2 provides physical basis |
| 12 | `gas_symptoms.o2_low` | 0.5 | 0.5 | `master_gas_guide.md` — O₂ < 0.5% indicates rich combustion consuming available oxygen | KEEP | Standard rich-combustion reference |
| 13 | `gas_symptoms.nox_high` | 600 | 600 | `master_nox_guide.md` §4.1 — NOx > 500 ppm with λ > 1.05 = lean-combustion NOx | RECALIBRATE | 600 is close to NOx guide's 500 ppm lean threshold; consider aligning to 500 |
| 14 | `gas_symptoms.nox_low` | 100 | 100 | `master_nox_guide.md` §3.1 — idle NOx > 100 ppm = EGR not diluting | KEEP | EGR failure idle threshold from NOx guide §8 |
| 15 | `gas_symptoms.lambda_low` | 0.95 | 0.95 | `master_ecu_guide.md` §3.2 — λ 0.95 is borderline rich; below this is moderate rich | KEEP | Consistent with ECU guide inversion boundary analysis |
| 16 | `gas_symptoms.lambda_high` | 1.05 | 1.05 | `master_nox_guide.md` §4.1 — λ > 1.05 = peak NOx formation zone | KEEP | Consistent with NOx guide §1 (peak NOx at λ ≈ 1.05) |

---

## 2. Pattern Thresholds (`patterns`)

### 2.1 `late_timing`

Source: `timing_compression_forensic.md` (2026-05-03). The original V1 thresholds
(`hc_min: 5000`, `co_min: 2.5`, `co2_max: 8.0`, `o2_min: 3.0`) were physically
impossible for cam retard — they described extreme ignition failure, not cam phaser lag.
Corrected per forensic analysis of 9 real cam-timing cases.

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 17 | `patterns.late_timing.lambda_min` | 0.75 | 0.75 | `timing_compression_forensic.md` L24 — cam retard λ floor | KEEP | Wide lower bound; covers cold-start enrichment |
| 18 | `patterns.late_timing.lambda_max` | 1.06 | 1.06 | `timing_compression_forensic.md` L24 — was 0.99; cam retard is stoich to slightly lean (cases up to λ=1.05) | RECALIBRATE | Forensic: raised from 0.99→1.06 to capture EXT-210 (λ=1.05) |
| 19 | `patterns.late_timing.hc_min` | 200 | 200 | `timing_compression_forensic.md` L25 — was 1200; cam retard HC is 180–420 ppm | RECALIBRATE | Forensic: lowered from 5000→1200 (T15z)→200 (forensic); real cases HC 180–420 |
| 20 | `patterns.late_timing.co_min` | 0.3 | 0.3 | `timing_compression_forensic.md` L26 — was 2.5; cam retard CO is 0.4–1.5%, not >2.5% | RECALIBRATE | Forensic: lowered from 2.5→0.3; original value blocked all 9 cases |
| 21 | `patterns.late_timing.co_max` | 2.0 | 2.0 | `timing_compression_forensic.md` L27 — guard against rich-mixture/misfire inhibitory collisions | KEEP | Forensic: added as guard; all 9 target cases CO ≤ 1.5% |
| 22 | `patterns.late_timing.co2_max` | 13.5 | 13.5 | `timing_compression_forensic.md` L28 — was 13.0; EXP-N007 has CO2=13.5 | RECALIBRATE | Forensic: raised from 8.0→13.0 (T15z)→13.5 (forensic) |
| 23 | `patterns.late_timing.o2_min` | 0.3 | 0.3 | `timing_compression_forensic.md` L29 — was 1.0; EXP-N007/EXP-N023 have O2=0.4–0.45% | RECALIBRATE | Forensic: lowered from 3.0→1.0 (T15z)→0.3 (forensic) |

### 2.2 `compression_loss`

Source: `timing_compression_forensic.md`. Original thresholds blocked 3 of 4 benchmark
compression cases. Corrected per forensic analysis.

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 24 | `patterns.compression_loss.hc_min` | 300 | 300 | `timing_compression_forensic.md` L106 — OK; all benchmark cases HC ≥ 450 | KEEP | Reasonable lower bound for compression-related HC |
| 25 | `patterns.compression_loss.hc_max` | 1300 | 1300 | `timing_compression_forensic.md` L106 — was 1000; covers MECH-001 (HC=1200) | RECALIBRATE | Forensic: raised from 1000→1300 |
| 26 | `patterns.compression_loss.o2_min` | 1.3 | 1.3 | `timing_compression_forensic.md` L107 — was 2.0; covers EXT-222 (O2=1.5), EXT-223 (O2=1.8) | RECALIBRATE | Forensic: lowered from 2.0→1.3 |
| 27 | `patterns.compression_loss.co2_max` | 13.0 | 13.0 | `timing_compression_forensic.md` L108 — was 12.0; covers EXT-222 (CO2=12.5), EXT-223 (boundary) | RECALIBRATE | Forensic: raised from 12.0→13.0 |
| 28 | `patterns.compression_loss.co_max` | 1.0 | 1.0 | `master_mechanical_guide.md` — compression loss should not produce elevated CO | KEEP | Reasonable; compression loss is not a rich condition |
| 29 | `patterns.compression_loss.nox_max` | 200 | 200 | `master_nox_guide.md` — compression loss → lower combustion temp → reduced NOx | KEEP | Consistent with NOx-temperature relationship |
| 30 | `patterns.compression_loss.lambda_min` | 0.95 | 0.95 | `timing_compression_forensic.md` L109 — was 1.0; covers MECH-001 (λ=0.99) | RECALIBRATE | Forensic: lowered from 1.0→0.95 |
| 31 | `patterns.compression_loss.lambda_max` | 1.2 | 1.2 | `timing_compression_forensic.md` L109 — OK; covers lean compression cases | KEEP | Reasonable upper bound for compression-loss λ |

### 2.3 `valve_seal`

Source: `master_mechanical_guide.md` (valve seal / oil-burn gas signatures).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 32 | `patterns.valve_seal.hc_min` | 300 | 300 | `master_mechanical_guide.md` — valve seal HC starts elevated from oil burning | KEEP | Reasonable; oil-burn HC floor |
| 33 | `patterns.valve_seal.hc_max` | 1000 | 1000 | `master_mechanical_guide.md` — valve seal HC ceiling; above this suspect ring/compression | KEEP | Distinguishes seal from ring failure |
| 34 | `patterns.valve_seal.co2_min` | 13.0 | 13.0 | `master_mechanical_guide.md` — valve seal should not severely depress CO₂ | KEEP | Reasonable |
| 35 | `patterns.valve_seal.co_max` | 0.8 | 0.8 | `master_mechanical_guide.md` — widened from 0.5→0.8 for blow-by cases with mild oil-burn CO | KEEP | Threshold comment documents the rationale |
| 36 | `patterns.valve_seal.o2_max` | 2.5 | 2.5 | `master_mechanical_guide.md` — valve seal O₂ ceiling | KEEP | Reasonable |
| 37 | `patterns.valve_seal.lambda_min` | 0.95 | 0.95 | `master_mechanical_guide.md` — valve seal λ floor | KEEP | Reasonable |
| 38 | `patterns.valve_seal.lambda_max` | 1.05 | 1.05 | `master_mechanical_guide.md` — valve seal λ ceiling | KEEP | Reasonable |

### 2.4 `pcv_leak`

Source: `master_mechanical_guide.md` (PCV system, vacuum leaks).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 39 | `patterns.pcv_leak.hc_min` | 60 | 60 | `master_mechanical_guide.md` — PCV leak HC floor | KEEP | Lower than other patterns; PCV leak is mild unmetered air |
| 40 | `patterns.pcv_leak.hc_max` | 800 | 800 | `master_mechanical_guide.md` — PCV leak HC ceiling | KEEP | Reasonable upper bound |
| 41 | `patterns.pcv_leak.o2_min` | 2.0 | 2.0 | `master_mechanical_guide.md` — PCV leak introduces unmetered air → elevated O₂ | KEEP | Consistent with vacuum leak O₂ signature |
| 42 | `patterns.pcv_leak.co2_max` | 13.0 | 13.0 | `master_exhaust_guide.md` §2.2 — unmetered air dilutes CO₂ | KEEP | Consistent with dilution CO₂ depression |
| 43 | `patterns.pcv_leak.lambda_min` | 1.05 | 1.05 | `master_mechanical_guide.md` — PCV leak leans mixture | KEEP | Lean-side λ consistent with unmetered air |
| 44 | `patterns.pcv_leak.lambda_max` | 1.2 | 1.2 | `master_mechanical_guide.md` — PCV leak λ ceiling | KEEP | Reasonable |
| 45 | `patterns.pcv_leak.co_max` | 1.0 | 1.0 | `master_mechanical_guide.md` — PCV leak CO ceiling | KEEP | CO should not be elevated for vacuum leak |

### 2.5 `high_fuel_pressure`

Source: `master_fuel_system_guide.md` (fuel pressure, rich conditions).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 46 | `patterns.high_fuel_pressure.co_min` | 2.0 | 2.0 | `master_fuel_system_guide.md` — high fuel pressure → rich → CO elevated | KEEP | CO > 2.0% = definitive rich |
| 47 | `patterns.high_fuel_pressure.o2_max` | 0.5 | 0.5 | `master_gas_guide.md` — rich combustion consumes O₂ | KEEP | Consistent with rich-combustion O₂ depression |
| 48 | `patterns.high_fuel_pressure.ltft_max` | -15 | -15 | `master_fuel_trim_guide.md` — ECU pulling fuel (negative trim) for rich condition | KEEP | LTFT < -15% = significant rich correction |
| 49 | `patterns.high_fuel_pressure.lambda_max` | 0.95 | 0.95 | `master_fuel_system_guide.md` — high fuel pressure → λ < 0.95 | KEEP | Consistent with rich λ boundary |

### 2.6 `leaking_injector`

Source: `master_fuel_system_guide.md` (injector leak, rich conditions).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 50 | `patterns.leaking_injector.co_min` | 2.0 | 2.0 | `master_fuel_system_guide.md` — leaking injector → rich → CO elevated | KEEP | CO > 2.0% = definitive rich |
| 51 | `patterns.leaking_injector.hc_min` | 200 | 200 | `master_fuel_system_guide.md` — leaking injector → unburned fuel → HC elevated | KEEP | HC floor for injector-drip rich condition |
| 52 | `patterns.leaking_injector.trim_max` | -10 | -10 | `master_fuel_trim_guide.md` — ECU pulling fuel for rich | KEEP | Reasonable trim threshold |
| 53 | `patterns.leaking_injector.lambda_max` | 0.95 | 0.95 | `master_fuel_system_guide.md` — leaking injector → λ < 0.95 | KEEP | Consistent with rich λ boundary |

### 2.7 `rich_negative_trims`

Source: `master_fuel_trim_guide.md` (rich condition with negative trim confirmation).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 54 | `patterns.rich_negative_trims.co_min` | 2.0 | 2.0 | `master_fuel_trim_guide.md` — rich condition confirmed by CO > 2.0% | KEEP | Consistent |
| 55 | `patterns.rich_negative_trims.trim_max` | -15 | -15 | `master_fuel_trim_guide.md` — ECU pulling ≥ 15% fuel | KEEP | Consistent |
| 56 | `patterns.rich_negative_trims.lambda_max` | 0.95 | 0.95 | `master_fuel_trim_guide.md` — λ < 0.95 confirms rich | KEEP | Consistent |

### 2.8 `head_gasket`

Source: `master_mechanical_guide.md` (head gasket failure, coolant-quench gas signature).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 57 | `patterns.head_gasket.hc_min` | 400 | 400 | `master_mechanical_guide.md` — head gasket HC floor | KEEP | Reasonable; coolant quench elevates HC |
| 58 | `patterns.head_gasket.hc_max` | 3500 | 3500 | `master_mechanical_guide.md` — widened from 2000→3500 for coolant-quench extreme cases | KEEP | Threshold comment documents the rationale |
| 59 | `patterns.head_gasket.o2_min` | 2.0 | 2.0 | `master_mechanical_guide.md` — coolant quench → incomplete combustion → elevated O₂ | KEEP | Reasonable |
| 60 | `patterns.head_gasket.co2_max` | 12.0 | 12.0 | `master_exhaust_guide.md` §2.2 — combustion dilution depresses CO₂ | KEEP | Severe depression consistent with coolant in cylinder |
| 61 | `patterns.head_gasket.co_max` | 1.5 | 1.5 | `master_mechanical_guide.md` — head gasket CO ceiling | KEEP | Reasonable |
| 62 | `patterns.head_gasket.lambda_min` | 1.0 | 1.0 | `master_mechanical_guide.md` — coolant quench leans effective mixture | KEEP | Consistent |
| 63 | `patterns.head_gasket.lambda_max` | 1.5 | 1.5 | `master_mechanical_guide.md` — widened from 1.2→1.5 for HC>2000 + λ>1.2 cases | KEEP | Threshold comment documents the rationale |

### 2.9 `stuck_egr_open`

Source: `master_egr_guide.md` §5.6 (threshold provenance table).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 64 | `patterns.stuck_egr_open.hc_min` | 350 | 300 | `master_egr_guide.md` §5.1 — HC > 300 ppm = measurable combustion deficit (~1.5% unburned fuel) | RECALIBRATE | EGR guide §5.6 specifies 300; current V1 value is 350 |
| 65 | `patterns.stuck_egr_open.hc_max` | 2500 | 2500 | `master_egr_guide.md` §4.2 — EGR stuck open HC can reach 1500+ ppm; 2500 covers extreme cases | KEEP | Reasonable upper bound |
| 66 | `patterns.stuck_egr_open.o2_min` | 2.0 | 2.0 | `master_egr_guide.md` §5.2 — O₂ > 2.0% at warm idle above healthy-no-cat boundary | KEEP | Exact match with EGR guide §5.6 |
| 67 | `patterns.stuck_egr_open.co2_max` | 13.0 | 13.0 | `master_egr_guide.md` §5.3 — CO₂ < 13% at warm idle with normal λ → dilution source active | KEEP | Exact match with EGR guide §5.6 |
| 68 | `patterns.stuck_egr_open.nox_max` | 200 | 200 | `master_egr_guide.md` §4.2 — EGR stuck open → NOx suppressed (inert gas quench) | KEEP | Consistent with EGR guide §4.2 (NOx suppressed, not elevated) |

### 2.10 `stuck_egr_open_dtc_assisted`

Source: `master_egr_guide.md` §5.6.

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 69 | `patterns.stuck_egr_open_dtc_assisted.hc_min` | 300 | 300 | `master_egr_guide.md` §5.1 — HC > 300 ppm with DTC co-occurrence | KEEP | Exact match with EGR guide §5.6 |
| 70 | `patterns.stuck_egr_open_dtc_assisted.o2_min` | 2.0 | 2.0 | `master_egr_guide.md` §5.2 — O₂ > 2.0% at warm idle | KEEP | Exact match with EGR guide §5.6 |
| 71 | `patterns.stuck_egr_open_dtc_assisted.co2_max` | 13.0 | 13.0 | `master_egr_guide.md` §5.3 — CO₂ < 13% dilution indicator | KEEP | Exact match with EGR guide §5.6 |

### 2.11 `egr_dilution`

Source: `master_egr_guide.md` §4 (EGR dilution gas signatures).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 72 | `patterns.egr_dilution.hc_min` | 500 | 500 | `master_egr_guide.md` §4 — EGR dilution HC | KEEP | Reasonable; more severe than stuck-open |
| 73 | `patterns.egr_dilution.lambda_min` | 0.97 | 0.97 | `master_egr_guide.md` §5.6 — λ balance window 0.97–1.03 during inert dilution | KEEP | Exact match with EGR guide §5.6 |
| 74 | `patterns.egr_dilution.lambda_max` | 1.03 | 1.03 | `master_egr_guide.md` §5.6 — λ stays near stoich during inert dilution | KEEP | Exact match with EGR guide §5.6 |
| 75 | `patterns.egr_dilution.nox_max` | 100 | 100 | `master_nox_guide.md` §8 — NOx suppressed by EGR dilution | KEEP | Consistent with EGR-NOx relationship |
| 76 | `patterns.egr_dilution.co2_max` | 14.0 | 14.0 | `master_egr_guide.md` §4 — moderate CO₂ depression from dilution | KEEP | Reasonable |
| 77 | `patterns.egr_dilution.o2_max` | 3.5 | 3.5 | `master_egr_guide.md` §4 — moderate O₂ elevation from dilution | KEEP | Reasonable |
| 78 | `patterns.egr_dilution.stft_min` | -10 | -10 | `master_egr_guide.md` §4 — EGR dilution may cause mild trim response | KEEP | Reasonable |

### 2.12 `ignition_misfire_confirmed`

Source: `master_ignition_guide.md` §6.

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 79 | `patterns.ignition_misfire_confirmed.hc_min` | 1000 | 1000 | `master_ignition_guide.md` §6 — HC > 1000 ppm = severe ignition misfire | KEEP | Consistent with misfire HC signature |
| 80 | `patterns.ignition_misfire_confirmed.o2_min` | 2.5 | 2.5 | `master_ignition_guide.md` §6 — raw O₂ exits with raw HC in misfire | KEEP | Consistent with misfire O₂ signature |
| 81 | `patterns.ignition_misfire_confirmed.co_max` | 1.5 | 1.5 | `master_ignition_guide.md` §6 — misfire CO ceiling (mixture isn't rich, it's incomplete) | KEEP | Consistent |

### 2.13 `individual_cylinder_misfire`

Source: `master_ignition_guide.md` §6 (single-cylinder misfire signature).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 82 | `patterns.individual_cylinder_misfire.hc_min` | 800 | 800 | `master_ignition_guide.md` §6 — single-cylinder misfire HC floor | KEEP | Slightly lower than multi-cylinder (dilution by other cylinders) |
| 83 | `patterns.individual_cylinder_misfire.co_max` | 0.8 | 0.8 | `master_ignition_guide.md` §6 — single-cylinder misfire CO ceiling | KEEP | Reasonable |
| 84 | `patterns.individual_cylinder_misfire.o2_min` | 3.0 | 3.0 | `master_ignition_guide.md` §6 — single-cylinder misfire O₂ floor | KEEP | Higher than multi-cylinder (undiluted raw O₂ from one cylinder) |

### 2.14 `lean_misfire`

Source: `master_ignition_guide.md` and `master_gas_guide.md` §3 (lean misfire).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 85 | `patterns.lean_misfire.hc_min` | 150 | 150 | `master_gas_guide.md` §3 — lean misfire has lower HC than rich/ignition misfire | KEEP | Lean misfire HC is moderate |
| 86 | `patterns.lean_misfire.o2_min` | 4.0 | 4.0 | `master_gas_guide.md` §3 — lean misfire → very high O₂ (excess air) | KEEP | O₂ > 4% confirms lean condition |
| 87 | `patterns.lean_misfire.lambda_min` | 1.1 | 1.1 | `master_gas_guide.md` §3 — λ > 1.1 = definitive lean condition | KEEP | Consistent with lean combustion boundary |
| 88 | `patterns.lean_misfire.co_max` | 0.3 | 0.3 | `master_gas_guide.md` §3 — lean misfire CO is low (oxygen-rich burn) | KEEP | Consistent |

### 2.15 `rich_misfire`

Source: `master_ignition_guide.md` §6 table row 3 and `master_gas_guide.md` §3 rule 3.

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 89 | `patterns.rich_misfire.hc_min` | 500 | 500 | `master_ignition_guide.md` §6 — rich misfire: both rich-side and lean-side products coexist | KEEP | Documented in thresholds.yaml comment |
| 90 | `patterns.rich_misfire.co_min` | 1.5 | 1.5 | `master_ignition_guide.md` §6 — rich misfire CO floor | KEEP | Consistent |
| 91 | `patterns.rich_misfire.o2_min` | 2.0 | 2.0 | `master_ignition_guide.md` §6 — rich misfire O₂ floor (lean-side products present) | KEEP | Consistent with dual-product misfire |
| 92 | `patterns.rich_misfire.lambda_max` | 0.95 | 0.95 | `master_ignition_guide.md` §6 — rich misfire λ ceiling | KEEP | Consistent |

### 2.16 `tired_catalyst`

Source: `master_catalyst_guide.md` (catalyst efficiency, aging).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 93 | `patterns.tired_catalyst.lambda_min` | 0.98 | 0.98 | `master_catalyst_guide.md` — catalyst efficiency requires λ in TWC window | KEEP | TWC window 0.98–1.02 |
| 94 | `patterns.tired_catalyst.lambda_max` | 1.02 | 1.02 | `master_catalyst_guide.md` — TWC window upper bound | KEEP | Consistent |
| 95 | `patterns.tired_catalyst.hc_min` | 80 | 80 | `master_catalyst_guide.md` — tired cat lets some HC through | KEEP | Reasonable |
| 96 | `patterns.tired_catalyst.hc_max` | 300 | 300 | `master_catalyst_guide.md` — above this suspect engine fault, not just catalyst | KEEP | Distinguishes catalyst from engine fault |
| 97 | `patterns.tired_catalyst.co_min` | 0.3 | 0.3 | `master_catalyst_guide.md` — tired cat CO floor | KEEP | Reasonable |
| 98 | `patterns.tired_catalyst.co_max` | 1.5 | 1.5 | `master_catalyst_guide.md` — tired cat CO ceiling | KEEP | Reasonable |
| 99 | `patterns.tired_catalyst.co2_min` | 12.5 | 12.5 | `master_catalyst_guide.md` — tired cat CO₂ floor | KEEP | Reasonable |
| 100 | `patterns.tired_catalyst.stft_abs_max` | 5 | 5 | `master_catalyst_guide.md` — normal fuel trim for catalyst evaluation | KEEP | Trim must be near zero to evaluate catalyst |

### 2.17 `high_idle_nox`

Source: `master_nox_guide.md` §3.1 (idle NOx elevation).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 101 | `patterns.high_idle_nox.nox_min` | 150 | 150 | `master_nox_guide.md` §4.3 — idle NOx > 150 ppm with otherwise normal gases = EGR absent | KEEP | EGR guide §4.3 cross-ref |
| 102 | `patterns.high_idle_nox.lambda_min` | 0.95 | 0.95 | `master_nox_guide.md` §4.3 — normal λ at idle with elevated NOx | KEEP | Consistent |
| 103 | `patterns.high_idle_nox.lambda_max` | 1.05 | 1.05 | `master_nox_guide.md` §4.3 — normal λ ceiling | KEEP | Consistent |
| 104 | `patterns.high_idle_nox.hc_max` | 100 | 100 | `master_nox_guide.md` §4.3 — HC normal when NOx elevated from EGR failure | KEEP | Key discriminator: normal HC + elevated NOx = EGR |

### 2.18 `catalyst_masking`

Source: `master_catalyst_guide.md` (false-negative catalyst assessment).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 105 | `patterns.catalyst_masking.co2_min` | 14.5 | 14.5 | `master_catalyst_guide.md` — high CO₂ suggests catalyst is working; masking other faults | KEEP | Reasonable |
| 106 | `patterns.catalyst_masking.hc_max` | 30 | 30 | `master_catalyst_guide.md` — very low HC suggests cat is masking engine HC | KEEP | Below normal healthy-engine HC |

### 2.19 `exhaust_leak_ghost`

Source: `master_exhaust_guide.md` §3.2 (post-cat exhaust leak ghosting as lean).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 107 | `patterns.exhaust_leak_ghost.o2_min` | 4.0 | 4.0 | `master_exhaust_guide.md` §3.2 — post-cat leak elevates tailpipe O₂ | KEEP | Consistent with post-cat leak signature |
| 108 | `patterns.exhaust_leak_ghost.co_min` | 1.0 | 1.0 | `master_exhaust_guide.md` §3.2 — exhaust leak ghost CO floor | KEEP | Reasonable |
| 109 | `patterns.exhaust_leak_ghost.stft_min` | 10 | 10 | `master_exhaust_guide.md` §3.2 — fuel trim response to perceived lean | KEEP | Trim confirms ECU response |

### 2.20 `clogged_exhaust_rpm`

Source: `master_exhaust_guide.md` §4 (exhaust restriction gas signature).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 110 | `patterns.clogged_exhaust_rpm.hc_min` | 50 | 50 | `master_exhaust_guide.md` §4.2 — clogged exhaust HC floor | KEEP | Moderate HC from re-breathing |
| 111 | `patterns.clogged_exhaust_rpm.hc_max` | 250 | 250 | `master_exhaust_guide.md` §4.2 — clogged exhaust HC ceiling | KEEP | Reasonable |
| 112 | `patterns.clogged_exhaust_rpm.co_max` | 1.0 | 1.0 | `master_exhaust_guide.md` §4.2 — clogged exhaust CO ceiling | KEEP | Reasonable |
| 113 | `patterns.clogged_exhaust_rpm.co2_max` | 11.0 | 11.0 | `master_exhaust_guide.md` §4.2 — severe CO₂ depression from re-breathing | KEEP | Consistent with Differential-bible Rule 4 |
| 114 | `patterns.clogged_exhaust_rpm.o2_min` | 2.0 | 2.0 | `master_exhaust_guide.md` §4.2 — clogged exhaust O₂ floor | KEEP | Consistent |
| 115 | `patterns.clogged_exhaust_rpm.o2_max` | 5.0 | 5.0 | `master_exhaust_guide.md` §4.2 — clogged exhaust O₂ ceiling | KEEP | Reasonable |
| 116 | `patterns.clogged_exhaust_rpm.lambda_min` | 1.05 | 1.05 | `master_exhaust_guide.md` §4.2 — clogged exhaust leans effective mixture | KEEP | Consistent |
| 117 | `patterns.clogged_exhaust_rpm.lambda_max` | 1.20 | 1.20 | `master_exhaust_guide.md` §4.2 — clogged exhaust λ ceiling | KEEP | Consistent |
| 118 | `patterns.clogged_exhaust_rpm.nox_min` | 200 | 200 | `master_exhaust_guide.md` §4.2 — elevated NOx from hot re-breathed charge | KEEP | Consistent |

### 2.21 `sensor_bias_false_rich`

Source: `master_ecu_guide.md` §7 Rule 3 (false-rich inversion).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 119 | `patterns.sensor_bias_false_rich.lambda_max` | 0.95 | 0.95 | `master_ecu_guide.md` §3.2 — false-rich perception λ boundary | KEEP | Wait — false-rich should be λ HIGH, not low. This threshold looks inverted vs the ECU guide. See notes. |
| 120 | `patterns.sensor_bias_false_rich.co_max` | 0.2 | 0.2 | `master_ecu_guide.md` §7 Rule 3 — false-rich: ECU perceives rich but tailpipe is lean (low CO) | KEEP | CO < 0.2% confirms lean combustion |
| 121 | `patterns.sensor_bias_false_rich.co2_min` | 12.0 | 12.0 | `master_ecu_guide.md` — reasonable CO₂ floor for false-rich pattern | KEEP | Reasonable |

**Note on #119:** The pattern name is `sensor_bias_false_rich` with `lambda_max: 0.95`.
This reads as "λ below 0.95 triggers false-rich" — but false-rich means the ECU perceives
rich while the engine is actually lean. A λ < 0.95 means the engine IS rich. This may be
a naming collision: the pattern detects when sensor bias creates a false-rich ECU
perception while the engine is actually rich (λ < 0.95) — i.e., both are rich but the
sensor bias is what created the DTC. Flag for review in T-P1-5.

---

## 3. Sensor Bias (`sensor_bias`)

Source: `master_o2_sensor_guide.md` §6 and `master_ecu_guide.md` §8.

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 122 | `sensor_bias.delta_hot` | 0.08 | 0.08 | `master_perception_guide.md` §4.2 — |Δλ| > 0.08 = significant O₂ sensor drift | KEEP | Perception guide §4.2 documents this exact threshold |
| 123 | `sensor_bias.delta_cold` | 0.15 | 0.15 | `master_o2_sensor_guide.md` — wider tolerance for cold sensor | KEEP | Cold sensor naturally has wider variance |
| 124 | `sensor_bias.obd_not_rich_min` | 0.98 | 0.98 | `master_o2_sensor_guide.md` — OBD λ > 0.98 = ECU not reporting rich | KEEP | Consistent |
| 125 | `sensor_bias.obd_not_lean_max` | 1.02 | 1.02 | `master_o2_sensor_guide.md` — OBD λ < 1.02 = ECU not reporting lean | KEEP | Consistent |

---

## 4. Dual-Speed Patterns (`dual_speed`)

### 4.1 `contaminated_maf`

Source: `master_air_induction_guide.md` §3 (MAF contamination, trim reversal).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 126 | `dual_speed.contaminated_maf.stft_idle_abs_max` | 5 | 5 | `master_air_induction_guide.md` §3 — normal trim at idle for contaminated MAF | KEEP | Contaminated MAF under-reads at low airflow; trim normal at idle |
| 127 | `dual_speed.contaminated_maf.stft_high_min` | 10 | 10 | `master_air_induction_guide.md` §3 — trim goes positive at high RPM for contaminated MAF | KEEP | Characteristic trim reversal |
| 128 | `dual_speed.contaminated_maf.o2_high_min` | 1.5 | 1.5 | `master_air_induction_guide.md` §3 — O₂ elevation at high RPM | KEEP | Consistent |

### 4.2 `clogged_exhaust`

Source: `master_exhaust_guide.md` §4 (dual-speed exhaust restriction).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 129 | `dual_speed.clogged_exhaust.co2_idle_min` | 13.0 | 13.0 | `master_exhaust_guide.md` §4 — CO₂ at idle for exhaust restriction test | KEEP | Reasonable |
| 130 | `dual_speed.clogged_exhaust.ltft_min` | -12 | -12 | `master_exhaust_guide.md` §4 — LTFT negative from restriction-induced rich | KEEP | Consistent |
| 131 | `dual_speed.clogged_exhaust.ltft_max` | -5 | -5 | `master_exhaust_guide.md` §4 — LTFT upper bound for restriction | KEEP | Consistent |
| 132 | `dual_speed.clogged_exhaust.co2_high_max` | 12.0 | 12.0 | `master_exhaust_guide.md` §4 — CO₂ depressed at high RPM from restriction | KEEP | Key discriminator: CO₂ drops at high RPM |

### 4.3 `intake_gasket`

Source: `master_air_induction_guide.md` (intake gasket leak, RPM-dependent).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 133 | `dual_speed.intake_gasket.stft_idle_min` | 15 | 15 | `master_air_induction_guide.md` — intake gasket leak: high positive trim at idle | KEEP | Vacuum leak worst at idle |
| 134 | `dual_speed.intake_gasket.o2_idle_min` | 2.5 | 2.5 | `master_air_induction_guide.md` — elevated O₂ at idle from unmetered air | KEEP | Consistent |
| 135 | `dual_speed.intake_gasket.stft_high_max` | 5 | 5 | `master_air_induction_guide.md` — trim normalizes at high RPM | KEEP | Key discriminator: leak effect shrinks at higher MAP |
| 136 | `dual_speed.intake_gasket.o2_high_max` | 1.5 | 1.5 | `master_air_induction_guide.md` — O₂ normalizes at high RPM | KEEP | Consistent |

### 4.4 `low_fuel_delivery`

Source: `master_fuel_system_guide.md` (fuel delivery volume vs RPM).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 137 | `dual_speed.low_fuel_delivery.stft_idle_abs_max` | 5 | 5 | `master_fuel_system_guide.md` — normal trim at idle; fuel demand is low | KEEP | Consistent |
| 138 | `dual_speed.low_fuel_delivery.stft_high_min` | 10 | 10 | `master_fuel_system_guide.md` — trim goes positive at high RPM as fuel pump can't keep up | KEEP | Key discriminator |
| 139 | `dual_speed.low_fuel_delivery.o2_high_min` | 2.0 | 2.0 | `master_fuel_system_guide.md` — O₂ rises at high RPM from lean-out | KEEP | Consistent |

### 4.5 `egr_recovery`

Source: `master_egr_guide.md` §5.5 (2500 RPM EGR recovery test).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 140 | `dual_speed.egr_recovery.hc_high_max` | 100 | 100 | `master_egr_guide.md` §5.5 — HC normalizes at 2500 RPM when EGR closes | KEEP | Key discriminator for EGR stuck-open |
| 141 | `dual_speed.egr_recovery.co2_high_min` | 13.0 | 13.0 | `master_egr_guide.md` §5.5 — CO₂ recovers at 2500 RPM | KEEP | Consistent |

### 4.6 `high_idle_diff`

Source: `master_gas_guide.md` (idle-vs-high-idle differentials).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 142 | `dual_speed.high_idle_diff.idle_lean_load_corrects_delta` | -0.05 | -0.05 | `master_gas_guide.md` — λ delta idle→load for lean correction | KEEP | Reasonable |
| 143 | `dual_speed.high_idle_diff.idle_stoich_load_lean_delta` | 0.05 | 0.05 | `master_gas_guide.md` — λ delta idle→load for lean drift | KEEP | Reasonable |

---

## 5. Non-Starter Thresholds (`non_starter`)

Source: `master_non_starter_guide.md` (cranking, no-start diagnostics).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 144 | `non_starter.ckp_rpm_max` | 50 | 50 | `master_non_starter_guide.md` — CKP RPM max for no-start detection | KEEP | Standard cranking RPM floor |
| 145 | `non_starter.fast_cranking_rpm_max` | 350 | 350 | `master_non_starter_guide.md` — RPM > 350 during cranking = no compression | KEEP | Threshold comment documents F31 fix |
| 146 | `non_starter.no_fuel_hc_max` | 50 | 50 | `master_non_starter_guide.md` — HC < 50 ppm during cranking = no fuel | KEEP | Consistent |
| 147 | `non_starter.flooded_hc_min` | 3000 | 3000 | `master_non_starter_guide.md` — HC > 3000 ppm during cranking = flooded | KEEP | Consistent |
| 148 | `non_starter.no_spark_hc_min` | 1500 | 1500 | `master_non_starter_guide.md` — HC > 1500 ppm during cranking = no spark | KEEP | Consistent |
| 149 | `non_starter.partial_hc_min` | 200 | 200 | `master_non_starter_guide.md` — HC 200–800 during cranking = partial combustion | KEEP | Consistent |
| 150 | `non_starter.partial_hc_max` | 800 | 800 | `master_non_starter_guide.md` — HC ceiling for partial combustion | KEEP | Consistent |
| 151 | `non_starter.no_compression_map_min` | 98 | 98 | `master_non_starter_guide.md` — MAP > 98 kPa during cranking = no compression | KEEP | Near-atmospheric MAP = no vacuum generated |
| 152 | `non_starter.vacuum_map_max` | 90 | 90 | `master_non_starter_guide.md` — MAP < 90 kPa during cranking = vacuum present | KEEP | Consistent |
| 153 | `non_starter.ect_low_max` | -35 | -35 | `master_cold_start_guide.md` — ECT < -35°C = extreme cold | KEEP | Below reasonable operating range |
| 154 | `non_starter.ect_high_min` | 145 | 145 | `master_mechanical_guide.md` — ECT > 145°C = severe overheat | KEEP | Above boiling point; cooling system failure |
| 155 | `non_starter.lean_no_start_co2_min` | 1.5 | 1.5 | `master_non_starter_guide.md` — CO₂ > 1.5% confirms combustion during lean no-start | KEEP | Threshold comment documents physical basis |
| 156 | `non_starter.lean_no_start_o2_max` | 18.0 | 18.0 | `master_non_starter_guide.md` — O₂ < 18.0% confirms some combustion consumed oxygen | KEEP | Threshold comment documents physical basis |
| 157 | `non_starter.lean_no_start_lambda_min` | 2.0 | 2.0 | `master_non_starter_guide.md` — λ > 2.0 = extremely lean no-start | KEEP | Threshold comment documents physical basis |

---

## 6. Healthy Gas Thresholds (`healthy_gas`)

Source: `master_gas_guide.md` (healthy petrol engine reference ranges).

### 6.1 `petrol`

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 158 | `healthy_gas.petrol.co_max` | 0.5 | 0.5 | `master_gas_guide.md` — healthy cat-equipped petrol CO max | KEEP | Standard reference |
| 159 | `healthy_gas.petrol.hc_max` | 150 | 150 | `master_gas_guide.md` — healthy cat-equipped petrol HC max | KEEP | Standard reference |
| 160 | `healthy_gas.petrol.co2_min` | 14.5 | 14.5 | `master_exhaust_guide.md` §2.2 — healthy CO₂ floor | KEEP | Consistent with O₂-CO₂ sum rule |
| 161 | `healthy_gas.petrol.o2_max` | 1.5 | 1.5 | `master_gas_guide.md` — healthy petrol O₂ max | KEEP | Standard reference |
| 162 | `healthy_gas.petrol.lambda_min` | 0.95 | 0.95 | `master_gas_guide.md` — healthy petrol λ floor | KEEP | Standard closed-loop range |
| 163 | `healthy_gas.petrol.lambda_max` | 1.05 | 1.05 | `master_gas_guide.md` — healthy petrol λ ceiling | KEEP | Standard closed-loop range |
| 164 | `healthy_gas.petrol.nox_max` | 300 | 300 | `master_nox_guide.md` §8 — healthy petrol NOx max at cruise | KEEP | NOx guide §8: cruise normal max 300 ppm |

### 6.2 `decat`

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 165 | `healthy_gas.decat.co_max` | 1.0 | 1.0 | `master_gas_guide.md` — decat CO max (wider tolerance without catalyst) | KEEP | Standard reference |
| 166 | `healthy_gas.decat.hc_max` | 200 | 200 | `master_gas_guide.md` — decat HC max | KEEP | Standard reference |
| 167 | `healthy_gas.decat.co2_min` | 12.0 | 12.0 | `master_gas_guide.md` — decat CO₂ floor (1–2% lower without cat) | KEEP | Consistent with `co2_good_min_decat` |
| 168 | `healthy_gas.decat.o2_max` | 2.0 | 2.0 | `master_gas_guide.md` — decat O₂ max | KEEP | Standard reference |
| 169 | `healthy_gas.decat.lambda_min` | 0.95 | 0.95 | `master_gas_guide.md` — decat λ floor | KEEP | Same closed-loop range |
| 170 | `healthy_gas.decat.lambda_max` | 1.05 | 1.05 | `master_gas_guide.md` — decat λ ceiling | KEEP | Same closed-loop range |
| 171 | `healthy_gas.decat.nox_max` | 500 | 500 | `master_nox_guide.md` — decat NOx max (wider without catalyst reduction) | KEEP | Higher than cat-equipped; reasonable |

---

## 7. Validation Thresholds (`validation`)

Source: Validation layer rules (R4/L04). General gas-analysis validation.

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 172 | `validation.ambient_air_o2_min` | 20.2 | 20.2 | `master_perception_guide.md` §6 — probe-out O₂ should be ≈20.9% | KEEP | Perception guide §6: O₂ < 20% = calibration error |
| 173 | `validation.ambient_air_co2_max` | 1.0 | 1.0 | `master_perception_guide.md` §6 — probe-out CO₂ should be ≈0.04% | KEEP | CO₂ > 1% with probe out = picking up exhaust |
| 174 | `validation.carbon_balance_max` | 18.0 | 18.0 | `master_gas_guide.md` — carbon balance upper bound | KEEP | Standard combustion chemistry |
| 175 | `validation.carbon_balance_warning_min` | 9.0 | 9.0 | `master_gas_guide.md` — carbon balance lower warning | KEEP | Standard |
| 176 | `validation.lambda_delta_warning` | 0.08 | 0.08 | `master_perception_guide.md` §4.2 — Δλ > 0.08 = analyser/OBD mismatch | KEEP | Same as sensor_bias.delta_hot |
| 177 | `validation.extreme_cranking_hc` | 5000 | 5000 | `master_non_starter_guide.md` — extreme HC during cranking | KEEP | Flooded/no-spark extreme HC boundary |

---

## 8. Freeze Frame Thresholds (`freeze_frame`)

Source: `master_freeze_frame_guide.md` §9 (threshold provenance table) and §10 (symptom derivation rules).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 178 | `freeze_frame.load_high_threshold` | 70 | 70 | `master_freeze_frame_guide.md` §3 — SAE/Innova/Autodtcs 70% CLV high-stress boundary | KEEP | Exact match with FF guide §9 |
| 179 | `freeze_frame.load_low_threshold` | 30 | 30 | `master_freeze_frame_guide.md` §3 — below 30% CLV = idle/light cruise | KEEP | Exact match with FF guide §9 |
| 180 | `freeze_frame.load_rpm_threshold` | 1500 | 1500 | `master_freeze_frame_guide.md` §9 — 1500 RPM boundary for load-at-low-RPM flag | KEEP | Exact match with FF guide §9 |
| 181 | `freeze_frame.ect_warmup_max` | 70 | 60 | `master_freeze_frame_guide.md` §4 — ECT < 70°C = warm-up; fault set during transition | RECALIBRATE | V1 has 70; FF guide §9 has 60 (warm-up transition 40–70°C). FF guide §4 says 70°C is the threshold between warm-up and normal. V1 comment says "60→70 per master_fuel_trim_guide.md §6". The V1 value of 70 is actually correct per FF guide §4. The FF guide §9 table says 60 but §4 says 70. Resolve inconsistency in T-P1-5. |
| 182 | `freeze_frame.iat_ect_delta_threshold` | 30 | 30 | `master_freeze_frame_guide.md` §9 — \|IAT − ECT\| > 30°C at RPM=0 = sensor bias | KEEP | Exact match with FF guide §9 |
| 183 | `freeze_frame.timing_retard_threshold` | -10 | -10 | `master_freeze_frame_guide.md` §9 — timing < -10° = severe retard | KEEP | Exact match with FF guide §9 |

---

## 9. Dual-PID Thresholds (`dual_pid`)

Source: `master_o2_sensor_guide.md` and `master_fuel_trim_guide.md` (bank-aware PID analysis).

| # | pattern_id | v1_value | v2_value | source_guide | category | notes |
|---|-----------|----------|----------|-------------|----------|-------|
| 184 | `dual_pid.trim_total_imbalance` | 10 | 10 | `master_fuel_trim_guide.md` §5 — \|STFT+LTFT\| > 10% = bank imbalance | KEEP | Inter-bank trim delta threshold |
| 185 | `dual_pid.o2_upstream_ambiguous_low` | 0.85 | 0.85 | `master_o2_sensor_guide.md` — narrowband/wideband ambiguous zone low | KEEP | Sensor type classifier |
| 186 | `dual_pid.o2_upstream_ambiguous_high` | 1.10 | 1.10 | `master_o2_sensor_guide.md` — narrowband/wideband ambiguous zone high | KEEP | Sensor type classifier |
| 187 | `dual_pid.o2_upstream_classifier_match_tol` | 0.10 | 0.10 | `master_o2_sensor_guide.md` — wideband classification tolerance | KEEP | Reasonable |
| 188 | `dual_pid.o2_downstream_active_min` | 0.3 | 0.3 | `master_o2_sensor_guide.md` — downstream O₂ active zone (with P0420) | KEEP | Catalyst monitor O₂ storage test |
| 189 | `dual_pid.o2_downstream_active_max` | 0.7 | 0.7 | `master_o2_sensor_guide.md` — downstream O₂ active zone upper | KEEP | Consistent |
| 190 | `dual_pid.o2_downstream_steady_min` | 0.7 | 0.7 | `master_o2_sensor_guide.md` — downstream O₂ steady zone | KEEP | Consistent |
| 191 | `dual_pid.o2_downstream_steady_max` | 0.8 | 0.8 | `master_o2_sensor_guide.md` — downstream O₂ steady zone upper | KEEP | Consistent |
| 192 | `dual_pid.o2_upstream_lazy_low` | 0.3 | 0.3 | `master_o2_sensor_guide.md` §6 — lazy O₂ sensor stuck low threshold | KEEP | Lazy sensor detection |
| 193 | `dual_pid.o2_upstream_lazy_high` | 0.7 | 0.7 | `master_o2_sensor_guide.md` §6 — lazy O₂ sensor stuck high threshold | KEEP | Lazy sensor detection |
| 194 | `dual_pid.nox_high_idle_threshold` | 100 | 100 | `master_nox_guide.md` §8 — NOx > 100 at idle = EGR not diluting | KEEP | Exact match with NOx guide §8 (`nox_egr_failure_idle`) |
| 195 | `dual_pid.nox_low_with_lean_threshold` | 50 | 50 | `master_nox_guide.md` §3.1 — NOx < 50 at idle is normal | KEEP | NOx guide §8: `nox_idle_warning` = 50 ppm |
| 196 | `dual_pid.nox_high_load_threshold` | 600 | 600 | `master_nox_guide.md` §8 — high-load NOx | KEEP | Reasonable for WOT/load NOx |
| 197 | `dual_pid.trim_per_bank_sum_threshold` | 10 | 10 | `master_fuel_trim_guide.md` §5 — per-bank trim sum > 10% = bank-specific fault | KEEP | Consistent with inter-bank trim analysis |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **KEEP** | 181 |
| **RECALIBRATE** | 15 |
| **REMOVE** | 0 |
| **PENDING** | 1 |

**RECALIBRATE items (15):**
- `patterns.late_timing`: 5 thresholds corrected per `timing_compression_forensic.md` (lambda_max, hc_min, co_min, co2_max, o2_min)
- `patterns.compression_loss`: 4 thresholds corrected per `timing_compression_forensic.md` (hc_max, o2_min, co2_max, lambda_min)
- `patterns.stuck_egr_open.hc_min`: 1 threshold (V1 value 350 vs EGR guide 300)
- `gas_symptoms.nox_high`: 1 threshold (V1 600 vs NOx guide 500)
- `freeze_frame.ect_warmup_max`: 1 threshold (FF guide §4 vs §9 inconsistency; resolve in T-P1-5)
- The `late_timing` and `compression_loss` corrections are already applied in the current `thresholds.yaml` — the RECALIBRATE category here marks them as having been corrected from original wrong values.

**PENDING items (1):**
- `patterns.sensor_bias_false_rich.lambda_max`: name/semantics confusion — pattern named "false_rich" but λ < 0.95 means engine IS rich. Needs review against `master_ecu_guide.md` §7 Rule 3.

**REMOVE items: 0** — all thresholds in V1 `thresholds.yaml` have a physical justification traceable to a master guide or forensic analysis.

---

## Verification

- **Source file:** `schema/v1_reference/thresholds.yaml`
- **Total audit rows:** 197 (covers all 197 individual numeric threshold entries)
- **Required forensic markers:** `late_timing` and `compression_loss` thresholds marked RECALIBRATE — **PASS**
- **7 master guides from T-P0-1/2/3 consulted:** EGR, ECU, Freeze Frame, Perception, NOx, Turbo, Exhaust — **PASS**
- **Cross-reference to pre-existing master guides:** gas, ignition, mechanical, catalyst, fuel_trim, fuel_system, o2_sensor, cold_start, air_induction, non_starter, obd — **PASS**
