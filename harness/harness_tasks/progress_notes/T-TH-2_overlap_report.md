# Box Overlap & Coverage-Gap Report

**Module:** GASLab  
**Date:** 2026-06-07  
**Boxes:** 34 | **Dimensions:** gas_hc, gas_co, gas_co2, gas_o2, gas_nox  
**Pairs analyzed:** 561 | **Overlapping:** 331 | **Identical gas signatures:** 21  

## Coverage Gap (Monte Carlo)

**Samples:** 50,000 (seeded, reproducible)  

| Category | Count | Pct |
|---|---|---|
| No box (unclassifiable hole) | 0 | 0.0% |
| Exactly one box (unambiguous) | 0 | 0.0% |
| Two or more boxes (ambiguous) | 50,000 | 100.0% |

**Discrimination ceiling:** 100.0% of the measurement envelope falls into 0 or 2+ boxes — structurally unresolvable on gas chemistry alone.

### Per-box coverage (top 10)

| Box | Monte Carlo hits |
|---|---|
| SAMPLE_INVALID | 50,000 |
| CAM_TIMING_RETARDED_MAP | 50,000 |
| CAM_TIMING_RETARDED_MAF | 50,000 |
| CAM_TIMING_ADVANCED | 50,000 |
| INCOMPLETE_COMBUSTION | 50,000 |
| COOLANT_LEAK_INTERNAL | 50,000 |
| POA_SIGNATURE | 32,210 |
| EGR_DILUTION_MISFIRE | 32,210 |
| EXHAUST_AIR_LEAK | 32,148 |
| INCOMPLETE_OXIDATION | 28,289 |

### Per-box coverage (bottom 10)

| Box | Monte Carlo hits |
|---|---|
| CATALYST_NOT_LIGHTING_OFF | 0 |
| TIMING_OVER_ADVANCED | 0 |
| TIMING_RETARDED | 0 |
| O2_SENSOR_BIASED_LOW | 0 |
| O2_SENSOR_BIASED_HIGH | 0 |
| WORN_ENGINE | 0 |
| FLAT_CAMSHAFT | 0 |
| WORN_VALVE_SEALS | 0 |
| WORN_PISTON_RINGS | 0 |
| EGR_STUCK_CLOSED | 0 |

### Zero-coverage boxes

These boxes received **zero** Monte Carlo hits — their volume in 5-D gas space may be too small to sample at N=50,000:

- NORMAL_OPERATION
- LEAN_MIXTURE
- HIGH_COMBUSTION_TEMP
- CATALYST_NOT_LIGHTING_OFF
- TIMING_OVER_ADVANCED
- TIMING_RETARDED
- O2_SENSOR_BIASED_LOW
- O2_SENSOR_BIASED_HIGH
- WORN_ENGINE
- FLAT_CAMSHAFT
- WORN_VALVE_SEALS
- WORN_PISTON_RINGS
- EGR_STUCK_CLOSED

## Identical Gas Signatures (cannot separate on gas alone)

- **CAM_TIMING_ADVANCED ↔ CAM_TIMING_RETARDED_MAF**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_ADVANCED ↔ CAM_TIMING_RETARDED_MAP**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_ADVANCED ↔ COOLANT_LEAK_INTERNAL**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_ADVANCED ↔ INCOMPLETE_COMBUSTION**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_ADVANCED ↔ SAMPLE_INVALID**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_RETARDED_MAF ↔ CAM_TIMING_RETARDED_MAP**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_RETARDED_MAF ↔ COOLANT_LEAK_INTERNAL**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_RETARDED_MAF ↔ INCOMPLETE_COMBUSTION**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_RETARDED_MAF ↔ SAMPLE_INVALID**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_RETARDED_MAP ↔ COOLANT_LEAK_INTERNAL**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_RETARDED_MAP ↔ INCOMPLETE_COMBUSTION**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **CAM_TIMING_RETARDED_MAP ↔ SAMPLE_INVALID**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **COOLANT_LEAK_INTERNAL ↔ INCOMPLETE_COMBUSTION**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **COOLANT_LEAK_INTERNAL ↔ SAMPLE_INVALID**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **EGR_DILUTION_MISFIRE ↔ POA_SIGNATURE**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **EGR_STUCK_CLOSED ↔ HIGH_COMBUSTION_TEMP**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **EGR_STUCK_CLOSED ↔ TIMING_OVER_ADVANCED**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **FLAT_CAMSHAFT ↔ NORMAL_OPERATION**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **GDI_HPFP_INTERNAL_SEAL_LEAK ↔ VACUUM_REGULATOR_DIAPHRAGM_RUPTURE**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **HIGH_COMBUSTION_TEMP ↔ TIMING_OVER_ADVANCED**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate
- **INCOMPLETE_COMBUSTION ↔ SAMPLE_INVALID**
  — identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate

## Overlapping Box Pairs (non-identical bounds)

| # | Box A | Box B | Intersection region (per dim) |
|---|---|---|---|
| 1 | CAM_TIMING_ADVANCED | CATALYST_NOT_LIGHTING_OFF | hc: [75, 125]<br>co: [0.5, 0.9]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.7]<br>nox: [0.0, 5000.0] |
| 2 | CAM_TIMING_ADVANCED | CATALYST_OVERWHELMED | hc: [200, 20000.0]<br>co: [1.0, 15.0]<br>co2: [0.0, 12]<br>o2: [0.0, 2.0]<br>nox: [500, 5000.0] |
| 3 | CAM_TIMING_ADVANCED | EGR_DILUTION_MISFIRE | hc: [500, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 14.5]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 4 | CAM_TIMING_ADVANCED | EGR_STUCK_CLOSED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 5 | CAM_TIMING_ADVANCED | EGR_STUCK_OPEN | hc: [100, 20000.0]<br>co: [0.5, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 2.0]<br>nox: [0.0, 5000.0] |
| 6 | CAM_TIMING_ADVANCED | EVAP_CANISTER_SATURATED | hc: [100, 500]<br>co: [0.5, 3.0]<br>co2: [0.0, 13]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 7 | CAM_TIMING_ADVANCED | EXHAUST_AIR_LEAK | hc: [0.0, 20000.0]<br>co: [0.45, 15.0]<br>co2: [0.0, 16]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 8 | CAM_TIMING_ADVANCED | FLAT_CAMSHAFT | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 9 | CAM_TIMING_ADVANCED | GDI_HPFP_INTERNAL_SEAL_LEAK | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 10 | CAM_TIMING_ADVANCED | GDI_INTAKE_VALVE_CARBON | hc: [100, 20000.0]<br>co: [0.0, 0.45]<br>co2: [0.0, 16]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 11 | CAM_TIMING_ADVANCED | HIGH_COMBUSTION_TEMP | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 12 | CAM_TIMING_ADVANCED | IGNITION_MISFIRE | hc: [1000, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 16]<br>o2: [3.0, 22.0]<br>nox: [0.0, 50] |
| 13 | CAM_TIMING_ADVANCED | INCOMPLETE_OXIDATION | hc: [200, 20000.0]<br>co: [0.5, 15.0]<br>co2: [0.0, 13]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 14 | CAM_TIMING_ADVANCED | LEAN_MISFIRE | hc: [200, 600]<br>co: [0.0, 0.2]<br>co2: [0.0, 12]<br>o2: [4.0, 22.0]<br>nox: [0.0, 5000.0] |
| 15 | CAM_TIMING_ADVANCED | LEAN_MIXTURE | hc: [0.0, 200]<br>co: [0.0, 0.1]<br>co2: [0.0, 14]<br>o2: [2.5, 22.0]<br>nox: [0.0, 500] |
| 16 | CAM_TIMING_ADVANCED | NORMAL_OPERATION | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 17 | CAM_TIMING_ADVANCED | O2_SENSOR_BIASED_HIGH | hc: [0.0, 100]<br>co: [0.0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 2.0]<br>nox: [0.0, 500] |
| 18 | CAM_TIMING_ADVANCED | O2_SENSOR_BIASED_LOW | hc: [0.0, 100]<br>co: [0.5, 3.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 500] |
| 19 | CAM_TIMING_ADVANCED | POA_SIGNATURE | hc: [500, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 14.5]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 20 | CAM_TIMING_ADVANCED | RICH_MISFIRE | hc: [200, 20000.0]<br>co: [0.45, 15.0]<br>co2: [5, 15]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 21 | CAM_TIMING_ADVANCED | RICH_MIXTURE | hc: [0.0, 500]<br>co: [1.5, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.5]<br>nox: [0.0, 500] |
| 22 | CAM_TIMING_ADVANCED | TIMING_OVER_ADVANCED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 23 | CAM_TIMING_ADVANCED | TIMING_RETARDED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 50] |
| 24 | CAM_TIMING_ADVANCED | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 25 | CAM_TIMING_ADVANCED | VVT_FAILURE | hc: [0.0, 500]<br>co: [0.0, 15.0]<br>co2: [0.0, 22.0]<br>o2: [0.0, 22.0]<br>nox: [500, 5000.0] |
| 26 | CAM_TIMING_ADVANCED | WORN_ENGINE | hc: [35, 300]<br>co: [0.1, 1.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 100] |
| 27 | CAM_TIMING_ADVANCED | WORN_PISTON_RINGS | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [14.5, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 28 | CAM_TIMING_ADVANCED | WORN_VALVE_SEALS | hc: [75, 250]<br>co: [0.0, 0.5]<br>co2: [11, 14.5]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 29 | CAM_TIMING_RETARDED_MAF | CATALYST_NOT_LIGHTING_OFF | hc: [75, 125]<br>co: [0.5, 0.9]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.7]<br>nox: [0.0, 5000.0] |
| 30 | CAM_TIMING_RETARDED_MAF | CATALYST_OVERWHELMED | hc: [200, 20000.0]<br>co: [1.0, 15.0]<br>co2: [0.0, 12]<br>o2: [0.0, 2.0]<br>nox: [500, 5000.0] |
| 31 | CAM_TIMING_RETARDED_MAF | EGR_DILUTION_MISFIRE | hc: [500, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 14.5]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 32 | CAM_TIMING_RETARDED_MAF | EGR_STUCK_CLOSED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 33 | CAM_TIMING_RETARDED_MAF | EGR_STUCK_OPEN | hc: [100, 20000.0]<br>co: [0.5, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 2.0]<br>nox: [0.0, 5000.0] |
| 34 | CAM_TIMING_RETARDED_MAF | EVAP_CANISTER_SATURATED | hc: [100, 500]<br>co: [0.5, 3.0]<br>co2: [0.0, 13]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 35 | CAM_TIMING_RETARDED_MAF | EXHAUST_AIR_LEAK | hc: [0.0, 20000.0]<br>co: [0.45, 15.0]<br>co2: [0.0, 16]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 36 | CAM_TIMING_RETARDED_MAF | FLAT_CAMSHAFT | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 37 | CAM_TIMING_RETARDED_MAF | GDI_HPFP_INTERNAL_SEAL_LEAK | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 38 | CAM_TIMING_RETARDED_MAF | GDI_INTAKE_VALVE_CARBON | hc: [100, 20000.0]<br>co: [0.0, 0.45]<br>co2: [0.0, 16]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 39 | CAM_TIMING_RETARDED_MAF | HIGH_COMBUSTION_TEMP | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 40 | CAM_TIMING_RETARDED_MAF | IGNITION_MISFIRE | hc: [1000, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 16]<br>o2: [3.0, 22.0]<br>nox: [0.0, 50] |
| 41 | CAM_TIMING_RETARDED_MAF | INCOMPLETE_OXIDATION | hc: [200, 20000.0]<br>co: [0.5, 15.0]<br>co2: [0.0, 13]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 42 | CAM_TIMING_RETARDED_MAF | LEAN_MISFIRE | hc: [200, 600]<br>co: [0.0, 0.2]<br>co2: [0.0, 12]<br>o2: [4.0, 22.0]<br>nox: [0.0, 5000.0] |
| 43 | CAM_TIMING_RETARDED_MAF | LEAN_MIXTURE | hc: [0.0, 200]<br>co: [0.0, 0.1]<br>co2: [0.0, 14]<br>o2: [2.5, 22.0]<br>nox: [0.0, 500] |
| 44 | CAM_TIMING_RETARDED_MAF | NORMAL_OPERATION | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 45 | CAM_TIMING_RETARDED_MAF | O2_SENSOR_BIASED_HIGH | hc: [0.0, 100]<br>co: [0.0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 2.0]<br>nox: [0.0, 500] |
| 46 | CAM_TIMING_RETARDED_MAF | O2_SENSOR_BIASED_LOW | hc: [0.0, 100]<br>co: [0.5, 3.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 500] |
| 47 | CAM_TIMING_RETARDED_MAF | POA_SIGNATURE | hc: [500, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 14.5]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 48 | CAM_TIMING_RETARDED_MAF | RICH_MISFIRE | hc: [200, 20000.0]<br>co: [0.45, 15.0]<br>co2: [5, 15]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 49 | CAM_TIMING_RETARDED_MAF | RICH_MIXTURE | hc: [0.0, 500]<br>co: [1.5, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.5]<br>nox: [0.0, 500] |
| 50 | CAM_TIMING_RETARDED_MAF | TIMING_OVER_ADVANCED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 51 | CAM_TIMING_RETARDED_MAF | TIMING_RETARDED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 50] |
| 52 | CAM_TIMING_RETARDED_MAF | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 53 | CAM_TIMING_RETARDED_MAF | VVT_FAILURE | hc: [0.0, 500]<br>co: [0.0, 15.0]<br>co2: [0.0, 22.0]<br>o2: [0.0, 22.0]<br>nox: [500, 5000.0] |
| 54 | CAM_TIMING_RETARDED_MAF | WORN_ENGINE | hc: [35, 300]<br>co: [0.1, 1.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 100] |
| 55 | CAM_TIMING_RETARDED_MAF | WORN_PISTON_RINGS | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [14.5, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 56 | CAM_TIMING_RETARDED_MAF | WORN_VALVE_SEALS | hc: [75, 250]<br>co: [0.0, 0.5]<br>co2: [11, 14.5]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 57 | CAM_TIMING_RETARDED_MAP | CATALYST_NOT_LIGHTING_OFF | hc: [75, 125]<br>co: [0.5, 0.9]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.7]<br>nox: [0.0, 5000.0] |
| 58 | CAM_TIMING_RETARDED_MAP | CATALYST_OVERWHELMED | hc: [200, 20000.0]<br>co: [1.0, 15.0]<br>co2: [0.0, 12]<br>o2: [0.0, 2.0]<br>nox: [500, 5000.0] |
| 59 | CAM_TIMING_RETARDED_MAP | EGR_DILUTION_MISFIRE | hc: [500, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 14.5]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 60 | CAM_TIMING_RETARDED_MAP | EGR_STUCK_CLOSED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 61 | CAM_TIMING_RETARDED_MAP | EGR_STUCK_OPEN | hc: [100, 20000.0]<br>co: [0.5, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 2.0]<br>nox: [0.0, 5000.0] |
| 62 | CAM_TIMING_RETARDED_MAP | EVAP_CANISTER_SATURATED | hc: [100, 500]<br>co: [0.5, 3.0]<br>co2: [0.0, 13]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 63 | CAM_TIMING_RETARDED_MAP | EXHAUST_AIR_LEAK | hc: [0.0, 20000.0]<br>co: [0.45, 15.0]<br>co2: [0.0, 16]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 64 | CAM_TIMING_RETARDED_MAP | FLAT_CAMSHAFT | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 65 | CAM_TIMING_RETARDED_MAP | GDI_HPFP_INTERNAL_SEAL_LEAK | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 66 | CAM_TIMING_RETARDED_MAP | GDI_INTAKE_VALVE_CARBON | hc: [100, 20000.0]<br>co: [0.0, 0.45]<br>co2: [0.0, 16]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 67 | CAM_TIMING_RETARDED_MAP | HIGH_COMBUSTION_TEMP | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 68 | CAM_TIMING_RETARDED_MAP | IGNITION_MISFIRE | hc: [1000, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 16]<br>o2: [3.0, 22.0]<br>nox: [0.0, 50] |
| 69 | CAM_TIMING_RETARDED_MAP | INCOMPLETE_OXIDATION | hc: [200, 20000.0]<br>co: [0.5, 15.0]<br>co2: [0.0, 13]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 70 | CAM_TIMING_RETARDED_MAP | LEAN_MISFIRE | hc: [200, 600]<br>co: [0.0, 0.2]<br>co2: [0.0, 12]<br>o2: [4.0, 22.0]<br>nox: [0.0, 5000.0] |
| 71 | CAM_TIMING_RETARDED_MAP | LEAN_MIXTURE | hc: [0.0, 200]<br>co: [0.0, 0.1]<br>co2: [0.0, 14]<br>o2: [2.5, 22.0]<br>nox: [0.0, 500] |
| 72 | CAM_TIMING_RETARDED_MAP | NORMAL_OPERATION | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 73 | CAM_TIMING_RETARDED_MAP | O2_SENSOR_BIASED_HIGH | hc: [0.0, 100]<br>co: [0.0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 2.0]<br>nox: [0.0, 500] |
| 74 | CAM_TIMING_RETARDED_MAP | O2_SENSOR_BIASED_LOW | hc: [0.0, 100]<br>co: [0.5, 3.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 500] |
| 75 | CAM_TIMING_RETARDED_MAP | POA_SIGNATURE | hc: [500, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 14.5]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 76 | CAM_TIMING_RETARDED_MAP | RICH_MISFIRE | hc: [200, 20000.0]<br>co: [0.45, 15.0]<br>co2: [5, 15]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 77 | CAM_TIMING_RETARDED_MAP | RICH_MIXTURE | hc: [0.0, 500]<br>co: [1.5, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.5]<br>nox: [0.0, 500] |
| 78 | CAM_TIMING_RETARDED_MAP | TIMING_OVER_ADVANCED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 79 | CAM_TIMING_RETARDED_MAP | TIMING_RETARDED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 50] |
| 80 | CAM_TIMING_RETARDED_MAP | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 81 | CAM_TIMING_RETARDED_MAP | VVT_FAILURE | hc: [0.0, 500]<br>co: [0.0, 15.0]<br>co2: [0.0, 22.0]<br>o2: [0.0, 22.0]<br>nox: [500, 5000.0] |
| 82 | CAM_TIMING_RETARDED_MAP | WORN_ENGINE | hc: [35, 300]<br>co: [0.1, 1.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 100] |
| 83 | CAM_TIMING_RETARDED_MAP | WORN_PISTON_RINGS | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [14.5, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 84 | CAM_TIMING_RETARDED_MAP | WORN_VALVE_SEALS | hc: [75, 250]<br>co: [0.0, 0.5]<br>co2: [11, 14.5]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 85 | CATALYST_NOT_LIGHTING_OFF | COOLANT_LEAK_INTERNAL | hc: [75, 125]<br>co: [0.5, 0.9]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.7]<br>nox: [0, 5000] |
| 86 | CATALYST_NOT_LIGHTING_OFF | EGR_STUCK_CLOSED | hc: [75, 100]<br>co: [0.5, 0.5]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.5]<br>nox: [1000, 5000] |
| 87 | CATALYST_NOT_LIGHTING_OFF | EGR_STUCK_OPEN | hc: [100, 125]<br>co: [0.5, 0.9]<br>co2: [13.5, 14]<br>o2: [0.3, 0.7]<br>nox: [0, 5000] |
| 88 | CATALYST_NOT_LIGHTING_OFF | FLAT_CAMSHAFT | hc: [75, 100]<br>co: [0.5, 0.5]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.5]<br>nox: [0, 100] |
| 89 | CATALYST_NOT_LIGHTING_OFF | HIGH_COMBUSTION_TEMP | hc: [75, 100]<br>co: [0.5, 0.5]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.5]<br>nox: [1000, 5000] |
| 90 | CATALYST_NOT_LIGHTING_OFF | INCOMPLETE_COMBUSTION | hc: [75, 125]<br>co: [0.5, 0.9]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.7]<br>nox: [0, 5000] |
| 91 | CATALYST_NOT_LIGHTING_OFF | NORMAL_OPERATION | hc: [75, 100]<br>co: [0.5, 0.5]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.5]<br>nox: [0, 100] |
| 92 | CATALYST_NOT_LIGHTING_OFF | O2_SENSOR_BIASED_LOW | hc: [75, 100]<br>co: [0.5, 0.9]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.3]<br>nox: [0, 500] |
| 93 | CATALYST_NOT_LIGHTING_OFF | SAMPLE_INVALID | hc: [75, 125]<br>co: [0.5, 0.9]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.7]<br>nox: [0, 5000] |
| 94 | CATALYST_NOT_LIGHTING_OFF | TIMING_OVER_ADVANCED | hc: [75, 100]<br>co: [0.5, 0.5]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.5]<br>nox: [1000, 5000] |
| 95 | CATALYST_NOT_LIGHTING_OFF | TIMING_RETARDED | hc: [75, 100]<br>co: [0.5, 0.5]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.5]<br>nox: [0, 50] |
| 96 | CATALYST_NOT_LIGHTING_OFF | VVT_FAILURE | hc: [75, 125]<br>co: [0.5, 0.9]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.7]<br>nox: [500, 5000] |
| 97 | CATALYST_NOT_LIGHTING_OFF | WORN_ENGINE | hc: [75, 125]<br>co: [0.5, 0.9]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.3]<br>nox: [0, 100] |
| 98 | CATALYST_NOT_LIGHTING_OFF | WORN_PISTON_RINGS | hc: [75, 100]<br>co: [0.5, 0.5]<br>co2: [14.5, 14.5]<br>o2: [0.3, 0.5]<br>nox: [0, 100] |
| 99 | CATALYST_NOT_LIGHTING_OFF | WORN_VALVE_SEALS | hc: [75, 125]<br>co: [0.5, 0.5]<br>co2: [13.5, 14.5]<br>o2: [0.3, 0.5]<br>nox: [0, 5000] |
| 100 | CATALYST_OVERWHELMED | COOLANT_LEAK_INTERNAL | hc: [200, 20000]<br>co: [1.0, 15]<br>co2: [0, 12]<br>o2: [0, 2.0]<br>nox: [500, 5000] |
| 101 | CATALYST_OVERWHELMED | EGR_DILUTION_MISFIRE | hc: [500, 20000]<br>co: [1.0, 15]<br>co2: [0, 12]<br>o2: [0, 2.0]<br>nox: [500, 5000] |
| 102 | CATALYST_OVERWHELMED | EGR_STUCK_OPEN | hc: [200, 20000]<br>co: [1.0, 15]<br>co2: [0, 12]<br>o2: [0, 2.0]<br>nox: [500, 5000] |
| 103 | CATALYST_OVERWHELMED | EVAP_CANISTER_SATURATED | hc: [200, 500]<br>co: [1.0, 3.0]<br>co2: [0, 12]<br>o2: [0, 0.5]<br>nox: [500, 5000] |
| 104 | CATALYST_OVERWHELMED | EXHAUST_AIR_LEAK | hc: [200, 20000]<br>co: [1.0, 15]<br>co2: [0, 12]<br>o2: [2.0, 2.0]<br>nox: [500, 5000] |
| 105 | CATALYST_OVERWHELMED | GDI_HPFP_INTERNAL_SEAL_LEAK | hc: [300, 20000]<br>co: [3.0, 15]<br>co2: [0, 12]<br>o2: [0, 0.3]<br>nox: [500, 5000] |
| 106 | CATALYST_OVERWHELMED | INCOMPLETE_COMBUSTION | hc: [200, 20000]<br>co: [1.0, 15]<br>co2: [0, 12]<br>o2: [0, 2.0]<br>nox: [500, 5000] |
| 107 | CATALYST_OVERWHELMED | INCOMPLETE_OXIDATION | hc: [200, 20000]<br>co: [1.0, 15]<br>co2: [0, 12]<br>o2: [0, 2.0]<br>nox: [500, 5000] |
| 108 | CATALYST_OVERWHELMED | POA_SIGNATURE | hc: [500, 20000]<br>co: [1.0, 15]<br>co2: [0, 12]<br>o2: [0, 2.0]<br>nox: [500, 5000] |
| 109 | CATALYST_OVERWHELMED | RICH_MISFIRE | hc: [200, 20000]<br>co: [1.0, 15]<br>co2: [5, 12]<br>o2: [2.0, 2.0]<br>nox: [500, 5000] |
| 110 | CATALYST_OVERWHELMED | RICH_MIXTURE | hc: [200, 500]<br>co: [1.5, 15]<br>co2: [0, 12]<br>o2: [0, 0.5]<br>nox: [500, 500] |
| 111 | CATALYST_OVERWHELMED | SAMPLE_INVALID | hc: [200, 20000]<br>co: [1.0, 15]<br>co2: [0, 12]<br>o2: [0, 2.0]<br>nox: [500, 5000] |
| 112 | CATALYST_OVERWHELMED | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 20000]<br>co: [3.0, 15]<br>co2: [0, 12]<br>o2: [0, 0.3]<br>nox: [500, 5000] |
| 113 | CATALYST_OVERWHELMED | VVT_FAILURE | hc: [200, 500]<br>co: [1.0, 15]<br>co2: [0, 12]<br>o2: [0, 2.0]<br>nox: [500, 5000] |
| 114 | COOLANT_LEAK_INTERNAL | EGR_DILUTION_MISFIRE | hc: [500, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 14.5]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 115 | COOLANT_LEAK_INTERNAL | EGR_STUCK_CLOSED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 116 | COOLANT_LEAK_INTERNAL | EGR_STUCK_OPEN | hc: [100, 20000.0]<br>co: [0.5, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 2.0]<br>nox: [0.0, 5000.0] |
| 117 | COOLANT_LEAK_INTERNAL | EVAP_CANISTER_SATURATED | hc: [100, 500]<br>co: [0.5, 3.0]<br>co2: [0.0, 13]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 118 | COOLANT_LEAK_INTERNAL | EXHAUST_AIR_LEAK | hc: [0.0, 20000.0]<br>co: [0.45, 15.0]<br>co2: [0.0, 16]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 119 | COOLANT_LEAK_INTERNAL | FLAT_CAMSHAFT | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 120 | COOLANT_LEAK_INTERNAL | GDI_HPFP_INTERNAL_SEAL_LEAK | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 121 | COOLANT_LEAK_INTERNAL | GDI_INTAKE_VALVE_CARBON | hc: [100, 20000.0]<br>co: [0.0, 0.45]<br>co2: [0.0, 16]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 122 | COOLANT_LEAK_INTERNAL | HIGH_COMBUSTION_TEMP | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 123 | COOLANT_LEAK_INTERNAL | IGNITION_MISFIRE | hc: [1000, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 16]<br>o2: [3.0, 22.0]<br>nox: [0.0, 50] |
| 124 | COOLANT_LEAK_INTERNAL | INCOMPLETE_OXIDATION | hc: [200, 20000.0]<br>co: [0.5, 15.0]<br>co2: [0.0, 13]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 125 | COOLANT_LEAK_INTERNAL | LEAN_MISFIRE | hc: [200, 600]<br>co: [0.0, 0.2]<br>co2: [0.0, 12]<br>o2: [4.0, 22.0]<br>nox: [0.0, 5000.0] |
| 126 | COOLANT_LEAK_INTERNAL | LEAN_MIXTURE | hc: [0.0, 200]<br>co: [0.0, 0.1]<br>co2: [0.0, 14]<br>o2: [2.5, 22.0]<br>nox: [0.0, 500] |
| 127 | COOLANT_LEAK_INTERNAL | NORMAL_OPERATION | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 128 | COOLANT_LEAK_INTERNAL | O2_SENSOR_BIASED_HIGH | hc: [0.0, 100]<br>co: [0.0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 2.0]<br>nox: [0.0, 500] |
| 129 | COOLANT_LEAK_INTERNAL | O2_SENSOR_BIASED_LOW | hc: [0.0, 100]<br>co: [0.5, 3.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 500] |
| 130 | COOLANT_LEAK_INTERNAL | POA_SIGNATURE | hc: [500, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 14.5]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 131 | COOLANT_LEAK_INTERNAL | RICH_MISFIRE | hc: [200, 20000.0]<br>co: [0.45, 15.0]<br>co2: [5, 15]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 132 | COOLANT_LEAK_INTERNAL | RICH_MIXTURE | hc: [0.0, 500]<br>co: [1.5, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.5]<br>nox: [0.0, 500] |
| 133 | COOLANT_LEAK_INTERNAL | TIMING_OVER_ADVANCED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 134 | COOLANT_LEAK_INTERNAL | TIMING_RETARDED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 50] |
| 135 | COOLANT_LEAK_INTERNAL | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 136 | COOLANT_LEAK_INTERNAL | VVT_FAILURE | hc: [0.0, 500]<br>co: [0.0, 15.0]<br>co2: [0.0, 22.0]<br>o2: [0.0, 22.0]<br>nox: [500, 5000.0] |
| 137 | COOLANT_LEAK_INTERNAL | WORN_ENGINE | hc: [35, 300]<br>co: [0.1, 1.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 100] |
| 138 | COOLANT_LEAK_INTERNAL | WORN_PISTON_RINGS | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [14.5, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 139 | COOLANT_LEAK_INTERNAL | WORN_VALVE_SEALS | hc: [75, 250]<br>co: [0.0, 0.5]<br>co2: [11, 14.5]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 140 | EGR_DILUTION_MISFIRE | EGR_STUCK_OPEN | hc: [500, 20000]<br>co: [0.5, 15]<br>co2: [0, 14]<br>o2: [0, 2.0]<br>nox: [0, 5000] |
| 141 | EGR_DILUTION_MISFIRE | EVAP_CANISTER_SATURATED | hc: [500, 500]<br>co: [0.5, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.5]<br>nox: [0, 5000] |
| 142 | EGR_DILUTION_MISFIRE | EXHAUST_AIR_LEAK | hc: [500, 20000]<br>co: [0.45, 15]<br>co2: [0, 14.5]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 143 | EGR_DILUTION_MISFIRE | GDI_HPFP_INTERNAL_SEAL_LEAK | hc: [500, 20000]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 144 | EGR_DILUTION_MISFIRE | GDI_INTAKE_VALVE_CARBON | hc: [500, 20000]<br>co: [0, 0.45]<br>co2: [0, 14.5]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 145 | EGR_DILUTION_MISFIRE | IGNITION_MISFIRE | hc: [1000, 20000]<br>co: [0, 15]<br>co2: [0, 14.5]<br>o2: [3.0, 22]<br>nox: [0, 50] |
| 146 | EGR_DILUTION_MISFIRE | INCOMPLETE_COMBUSTION | hc: [500, 20000]<br>co: [0, 15]<br>co2: [0, 14.5]<br>o2: [0, 22]<br>nox: [0, 5000] |
| 147 | EGR_DILUTION_MISFIRE | INCOMPLETE_OXIDATION | hc: [500, 20000]<br>co: [0.5, 15]<br>co2: [0, 13]<br>o2: [0, 22]<br>nox: [0, 5000] |
| 148 | EGR_DILUTION_MISFIRE | LEAN_MISFIRE | hc: [500, 600]<br>co: [0, 0.2]<br>co2: [0, 12]<br>o2: [4.0, 22]<br>nox: [0, 5000] |
| 149 | EGR_DILUTION_MISFIRE | RICH_MISFIRE | hc: [500, 20000]<br>co: [0.45, 15]<br>co2: [5, 14.5]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 150 | EGR_DILUTION_MISFIRE | RICH_MIXTURE | hc: [500, 500]<br>co: [1.5, 15]<br>co2: [0, 14]<br>o2: [0, 0.5]<br>nox: [0, 500] |
| 151 | EGR_DILUTION_MISFIRE | SAMPLE_INVALID | hc: [500, 20000]<br>co: [0, 15]<br>co2: [0, 14.5]<br>o2: [0, 22]<br>nox: [0, 5000] |
| 152 | EGR_DILUTION_MISFIRE | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [500, 20000]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 153 | EGR_DILUTION_MISFIRE | VVT_FAILURE | hc: [500, 500]<br>co: [0, 15]<br>co2: [0, 14.5]<br>o2: [0, 22]<br>nox: [500, 5000] |
| 154 | EGR_STUCK_CLOSED | EGR_STUCK_OPEN | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 14]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 155 | EGR_STUCK_CLOSED | EVAP_CANISTER_SATURATED | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 13]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 156 | EGR_STUCK_CLOSED | INCOMPLETE_COMBUSTION | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 157 | EGR_STUCK_CLOSED | SAMPLE_INVALID | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 158 | EGR_STUCK_CLOSED | VVT_FAILURE | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 159 | EGR_STUCK_CLOSED | WORN_VALVE_SEALS | hc: [75, 100]<br>co: [0, 0.5]<br>co2: [13, 14.5]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 160 | EGR_STUCK_OPEN | EVAP_CANISTER_SATURATED | hc: [100, 500]<br>co: [0.5, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.5]<br>nox: [0, 5000] |
| 161 | EGR_STUCK_OPEN | EXHAUST_AIR_LEAK | hc: [100, 20000]<br>co: [0.5, 15]<br>co2: [0, 14]<br>o2: [2.0, 2.0]<br>nox: [0, 5000] |
| 162 | EGR_STUCK_OPEN | FLAT_CAMSHAFT | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 14]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 163 | EGR_STUCK_OPEN | GDI_HPFP_INTERNAL_SEAL_LEAK | hc: [300, 20000]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 164 | EGR_STUCK_OPEN | HIGH_COMBUSTION_TEMP | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 14]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 165 | EGR_STUCK_OPEN | INCOMPLETE_COMBUSTION | hc: [100, 20000]<br>co: [0.5, 15]<br>co2: [0, 14]<br>o2: [0, 2.0]<br>nox: [0, 5000] |
| 166 | EGR_STUCK_OPEN | INCOMPLETE_OXIDATION | hc: [200, 20000]<br>co: [0.5, 15]<br>co2: [0, 13]<br>o2: [0, 2.0]<br>nox: [0, 5000] |
| 167 | EGR_STUCK_OPEN | NORMAL_OPERATION | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 14]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 168 | EGR_STUCK_OPEN | O2_SENSOR_BIASED_LOW | hc: [100, 100]<br>co: [0.5, 3.0]<br>co2: [13, 14]<br>o2: [0, 0.3]<br>nox: [0, 500] |
| 169 | EGR_STUCK_OPEN | POA_SIGNATURE | hc: [500, 20000]<br>co: [0.5, 15]<br>co2: [0, 14]<br>o2: [0, 2.0]<br>nox: [0, 5000] |
| 170 | EGR_STUCK_OPEN | RICH_MISFIRE | hc: [200, 20000]<br>co: [0.5, 15]<br>co2: [5, 14]<br>o2: [2.0, 2.0]<br>nox: [0, 5000] |
| 171 | EGR_STUCK_OPEN | RICH_MIXTURE | hc: [100, 500]<br>co: [1.5, 15]<br>co2: [0, 14]<br>o2: [0, 0.5]<br>nox: [0, 500] |
| 172 | EGR_STUCK_OPEN | SAMPLE_INVALID | hc: [100, 20000]<br>co: [0.5, 15]<br>co2: [0, 14]<br>o2: [0, 2.0]<br>nox: [0, 5000] |
| 173 | EGR_STUCK_OPEN | TIMING_OVER_ADVANCED | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 14]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 174 | EGR_STUCK_OPEN | TIMING_RETARDED | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 14]<br>o2: [0, 0.5]<br>nox: [0, 50] |
| 175 | EGR_STUCK_OPEN | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 20000]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 176 | EGR_STUCK_OPEN | VVT_FAILURE | hc: [100, 500]<br>co: [0.5, 15]<br>co2: [0, 14]<br>o2: [0, 2.0]<br>nox: [500, 5000] |
| 177 | EGR_STUCK_OPEN | WORN_ENGINE | hc: [100, 300]<br>co: [0.5, 1.0]<br>co2: [13, 14]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 178 | EGR_STUCK_OPEN | WORN_VALVE_SEALS | hc: [100, 250]<br>co: [0.5, 0.5]<br>co2: [11, 14]<br>o2: [0, 0.5]<br>nox: [0, 5000] |
| 179 | EVAP_CANISTER_SATURATED | FLAT_CAMSHAFT | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 13]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 180 | EVAP_CANISTER_SATURATED | GDI_HPFP_INTERNAL_SEAL_LEAK | hc: [300, 500]<br>co: [3.0, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 181 | EVAP_CANISTER_SATURATED | HIGH_COMBUSTION_TEMP | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 13]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 182 | EVAP_CANISTER_SATURATED | INCOMPLETE_COMBUSTION | hc: [100, 500]<br>co: [0.5, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.5]<br>nox: [0, 5000] |
| 183 | EVAP_CANISTER_SATURATED | INCOMPLETE_OXIDATION | hc: [200, 500]<br>co: [0.5, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.5]<br>nox: [0, 5000] |
| 184 | EVAP_CANISTER_SATURATED | NORMAL_OPERATION | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 13]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 185 | EVAP_CANISTER_SATURATED | O2_SENSOR_BIASED_LOW | hc: [100, 100]<br>co: [0.5, 3.0]<br>co2: [13, 13]<br>o2: [0, 0.3]<br>nox: [0, 500] |
| 186 | EVAP_CANISTER_SATURATED | POA_SIGNATURE | hc: [500, 500]<br>co: [0.5, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.5]<br>nox: [0, 5000] |
| 187 | EVAP_CANISTER_SATURATED | RICH_MIXTURE | hc: [100, 500]<br>co: [1.5, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.5]<br>nox: [0, 500] |
| 188 | EVAP_CANISTER_SATURATED | SAMPLE_INVALID | hc: [100, 500]<br>co: [0.5, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.5]<br>nox: [0, 5000] |
| 189 | EVAP_CANISTER_SATURATED | TIMING_OVER_ADVANCED | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 13]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 190 | EVAP_CANISTER_SATURATED | TIMING_RETARDED | hc: [100, 100]<br>co: [0.5, 0.5]<br>co2: [13, 13]<br>o2: [0, 0.5]<br>nox: [0, 50] |
| 191 | EVAP_CANISTER_SATURATED | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 500]<br>co: [3.0, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 192 | EVAP_CANISTER_SATURATED | VVT_FAILURE | hc: [100, 500]<br>co: [0.5, 3.0]<br>co2: [0, 13]<br>o2: [0, 0.5]<br>nox: [500, 5000] |
| 193 | EVAP_CANISTER_SATURATED | WORN_ENGINE | hc: [100, 300]<br>co: [0.5, 1.0]<br>co2: [13, 13]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 194 | EVAP_CANISTER_SATURATED | WORN_VALVE_SEALS | hc: [100, 250]<br>co: [0.5, 0.5]<br>co2: [11, 13]<br>o2: [0, 0.5]<br>nox: [0, 5000] |
| 195 | EXHAUST_AIR_LEAK | GDI_INTAKE_VALVE_CARBON | hc: [100, 20000]<br>co: [0.45, 0.45]<br>co2: [0, 16]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 196 | EXHAUST_AIR_LEAK | IGNITION_MISFIRE | hc: [1000, 20000]<br>co: [0.45, 15]<br>co2: [0, 16]<br>o2: [3.0, 22]<br>nox: [0, 50] |
| 197 | EXHAUST_AIR_LEAK | INCOMPLETE_COMBUSTION | hc: [0, 20000]<br>co: [0.45, 15]<br>co2: [0, 16]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 198 | EXHAUST_AIR_LEAK | INCOMPLETE_OXIDATION | hc: [200, 20000]<br>co: [0.5, 15]<br>co2: [0, 13]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 199 | EXHAUST_AIR_LEAK | POA_SIGNATURE | hc: [500, 20000]<br>co: [0.45, 15]<br>co2: [0, 14.5]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 200 | EXHAUST_AIR_LEAK | RICH_MISFIRE | hc: [200, 20000]<br>co: [0.45, 15]<br>co2: [5, 15]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 201 | EXHAUST_AIR_LEAK | SAMPLE_INVALID | hc: [0, 20000]<br>co: [0.45, 15]<br>co2: [0, 16]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 202 | EXHAUST_AIR_LEAK | VVT_FAILURE | hc: [0, 500]<br>co: [0.45, 15]<br>co2: [0, 16]<br>o2: [2.0, 22]<br>nox: [500, 5000] |
| 203 | FLAT_CAMSHAFT | INCOMPLETE_COMBUSTION | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 204 | FLAT_CAMSHAFT | O2_SENSOR_BIASED_HIGH | hc: [0, 100]<br>co: [0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 0.5]<br>nox: [0, 100] |
| 205 | FLAT_CAMSHAFT | O2_SENSOR_BIASED_LOW | hc: [0, 100]<br>co: [0.5, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 206 | FLAT_CAMSHAFT | SAMPLE_INVALID | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 207 | FLAT_CAMSHAFT | TIMING_RETARDED | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [0, 50] |
| 208 | FLAT_CAMSHAFT | WORN_ENGINE | hc: [35, 100]<br>co: [0.1, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 209 | FLAT_CAMSHAFT | WORN_PISTON_RINGS | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [14.5, 16]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 210 | FLAT_CAMSHAFT | WORN_VALVE_SEALS | hc: [75, 100]<br>co: [0, 0.5]<br>co2: [13, 14.5]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 211 | GDI_HPFP_INTERNAL_SEAL_LEAK | INCOMPLETE_COMBUSTION | hc: [300, 20000]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 212 | GDI_HPFP_INTERNAL_SEAL_LEAK | INCOMPLETE_OXIDATION | hc: [300, 20000]<br>co: [3.0, 15]<br>co2: [0, 13]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 213 | GDI_HPFP_INTERNAL_SEAL_LEAK | POA_SIGNATURE | hc: [500, 20000]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 214 | GDI_HPFP_INTERNAL_SEAL_LEAK | RICH_MIXTURE | hc: [300, 500]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 500] |
| 215 | GDI_HPFP_INTERNAL_SEAL_LEAK | SAMPLE_INVALID | hc: [300, 20000]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 216 | GDI_HPFP_INTERNAL_SEAL_LEAK | VVT_FAILURE | hc: [300, 500]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [500, 5000] |
| 217 | GDI_INTAKE_VALVE_CARBON | IGNITION_MISFIRE | hc: [1000, 20000]<br>co: [0, 0.45]<br>co2: [0, 16]<br>o2: [3.0, 22]<br>nox: [0, 50] |
| 218 | GDI_INTAKE_VALVE_CARBON | INCOMPLETE_COMBUSTION | hc: [100, 20000]<br>co: [0, 0.45]<br>co2: [0, 16]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 219 | GDI_INTAKE_VALVE_CARBON | LEAN_MISFIRE | hc: [200, 600]<br>co: [0, 0.2]<br>co2: [0, 12]<br>o2: [4.0, 22]<br>nox: [0, 5000] |
| 220 | GDI_INTAKE_VALVE_CARBON | LEAN_MIXTURE | hc: [100, 200]<br>co: [0, 0.1]<br>co2: [0, 14]<br>o2: [2.5, 22]<br>nox: [0, 500] |
| 221 | GDI_INTAKE_VALVE_CARBON | O2_SENSOR_BIASED_HIGH | hc: [100, 100]<br>co: [0, 0.2]<br>co2: [13, 16]<br>o2: [2.0, 2.0]<br>nox: [0, 500] |
| 222 | GDI_INTAKE_VALVE_CARBON | POA_SIGNATURE | hc: [500, 20000]<br>co: [0, 0.45]<br>co2: [0, 14.5]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 223 | GDI_INTAKE_VALVE_CARBON | RICH_MISFIRE | hc: [200, 20000]<br>co: [0.45, 0.45]<br>co2: [5, 15]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 224 | GDI_INTAKE_VALVE_CARBON | SAMPLE_INVALID | hc: [100, 20000]<br>co: [0, 0.45]<br>co2: [0, 16]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 225 | GDI_INTAKE_VALVE_CARBON | VVT_FAILURE | hc: [100, 500]<br>co: [0, 0.45]<br>co2: [0, 16]<br>o2: [2.0, 22]<br>nox: [500, 5000] |
| 226 | HIGH_COMBUSTION_TEMP | INCOMPLETE_COMBUSTION | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 227 | HIGH_COMBUSTION_TEMP | SAMPLE_INVALID | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 228 | HIGH_COMBUSTION_TEMP | VVT_FAILURE | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 229 | HIGH_COMBUSTION_TEMP | WORN_VALVE_SEALS | hc: [75, 100]<br>co: [0, 0.5]<br>co2: [13, 14.5]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 230 | IGNITION_MISFIRE | INCOMPLETE_COMBUSTION | hc: [1000, 20000]<br>co: [0, 15]<br>co2: [0, 16]<br>o2: [3.0, 22]<br>nox: [0, 50] |
| 231 | IGNITION_MISFIRE | INCOMPLETE_OXIDATION | hc: [1000, 20000]<br>co: [0.5, 15]<br>co2: [0, 13]<br>o2: [3.0, 22]<br>nox: [0, 50] |
| 232 | IGNITION_MISFIRE | POA_SIGNATURE | hc: [1000, 20000]<br>co: [0, 15]<br>co2: [0, 14.5]<br>o2: [3.0, 22]<br>nox: [0, 50] |
| 233 | IGNITION_MISFIRE | RICH_MISFIRE | hc: [1000, 20000]<br>co: [0.45, 15]<br>co2: [5, 15]<br>o2: [3.0, 22]<br>nox: [0, 50] |
| 234 | IGNITION_MISFIRE | SAMPLE_INVALID | hc: [1000, 20000]<br>co: [0, 15]<br>co2: [0, 16]<br>o2: [3.0, 22]<br>nox: [0, 50] |
| 235 | INCOMPLETE_COMBUSTION | INCOMPLETE_OXIDATION | hc: [200, 20000.0]<br>co: [0.5, 15.0]<br>co2: [0.0, 13]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 236 | INCOMPLETE_COMBUSTION | LEAN_MISFIRE | hc: [200, 600]<br>co: [0.0, 0.2]<br>co2: [0.0, 12]<br>o2: [4.0, 22.0]<br>nox: [0.0, 5000.0] |
| 237 | INCOMPLETE_COMBUSTION | LEAN_MIXTURE | hc: [0.0, 200]<br>co: [0.0, 0.1]<br>co2: [0.0, 14]<br>o2: [2.5, 22.0]<br>nox: [0.0, 500] |
| 238 | INCOMPLETE_COMBUSTION | NORMAL_OPERATION | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 239 | INCOMPLETE_COMBUSTION | O2_SENSOR_BIASED_HIGH | hc: [0.0, 100]<br>co: [0.0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 2.0]<br>nox: [0.0, 500] |
| 240 | INCOMPLETE_COMBUSTION | O2_SENSOR_BIASED_LOW | hc: [0.0, 100]<br>co: [0.5, 3.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 500] |
| 241 | INCOMPLETE_COMBUSTION | POA_SIGNATURE | hc: [500, 20000.0]<br>co: [0.0, 15.0]<br>co2: [0.0, 14.5]<br>o2: [0.0, 22.0]<br>nox: [0.0, 5000.0] |
| 242 | INCOMPLETE_COMBUSTION | RICH_MISFIRE | hc: [200, 20000.0]<br>co: [0.45, 15.0]<br>co2: [5, 15]<br>o2: [2.0, 22.0]<br>nox: [0.0, 5000.0] |
| 243 | INCOMPLETE_COMBUSTION | RICH_MIXTURE | hc: [0.0, 500]<br>co: [1.5, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.5]<br>nox: [0.0, 500] |
| 244 | INCOMPLETE_COMBUSTION | TIMING_OVER_ADVANCED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 245 | INCOMPLETE_COMBUSTION | TIMING_RETARDED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 50] |
| 246 | INCOMPLETE_COMBUSTION | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 247 | INCOMPLETE_COMBUSTION | VVT_FAILURE | hc: [0.0, 500]<br>co: [0.0, 15.0]<br>co2: [0.0, 22.0]<br>o2: [0.0, 22.0]<br>nox: [500, 5000.0] |
| 248 | INCOMPLETE_COMBUSTION | WORN_ENGINE | hc: [35, 300]<br>co: [0.1, 1.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 100] |
| 249 | INCOMPLETE_COMBUSTION | WORN_PISTON_RINGS | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [14.5, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 250 | INCOMPLETE_COMBUSTION | WORN_VALVE_SEALS | hc: [75, 250]<br>co: [0.0, 0.5]<br>co2: [11, 14.5]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 251 | INCOMPLETE_OXIDATION | POA_SIGNATURE | hc: [500, 20000]<br>co: [0.5, 15]<br>co2: [0, 13]<br>o2: [0, 22]<br>nox: [0, 5000] |
| 252 | INCOMPLETE_OXIDATION | RICH_MISFIRE | hc: [200, 20000]<br>co: [0.5, 15]<br>co2: [5, 13]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 253 | INCOMPLETE_OXIDATION | RICH_MIXTURE | hc: [200, 500]<br>co: [1.5, 15]<br>co2: [0, 13]<br>o2: [0, 0.5]<br>nox: [0, 500] |
| 254 | INCOMPLETE_OXIDATION | SAMPLE_INVALID | hc: [200, 20000]<br>co: [0.5, 15]<br>co2: [0, 13]<br>o2: [0, 22]<br>nox: [0, 5000] |
| 255 | INCOMPLETE_OXIDATION | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 20000]<br>co: [3.0, 15]<br>co2: [0, 13]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 256 | INCOMPLETE_OXIDATION | VVT_FAILURE | hc: [200, 500]<br>co: [0.5, 15]<br>co2: [0, 13]<br>o2: [0, 22]<br>nox: [500, 5000] |
| 257 | INCOMPLETE_OXIDATION | WORN_ENGINE | hc: [200, 300]<br>co: [0.5, 1.0]<br>co2: [13, 13]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 258 | INCOMPLETE_OXIDATION | WORN_VALVE_SEALS | hc: [200, 250]<br>co: [0.5, 0.5]<br>co2: [11, 13]<br>o2: [0, 0.5]<br>nox: [0, 5000] |
| 259 | LEAN_MISFIRE | LEAN_MIXTURE | hc: [200, 200]<br>co: [0, 0.1]<br>co2: [0, 12]<br>o2: [4.0, 22]<br>nox: [0, 500] |
| 260 | LEAN_MISFIRE | POA_SIGNATURE | hc: [500, 600]<br>co: [0, 0.2]<br>co2: [0, 12]<br>o2: [4.0, 22]<br>nox: [0, 5000] |
| 261 | LEAN_MISFIRE | SAMPLE_INVALID | hc: [200, 600]<br>co: [0, 0.2]<br>co2: [0, 12]<br>o2: [4.0, 22]<br>nox: [0, 5000] |
| 262 | LEAN_MISFIRE | VVT_FAILURE | hc: [200, 500]<br>co: [0, 0.2]<br>co2: [0, 12]<br>o2: [4.0, 22]<br>nox: [500, 5000] |
| 263 | LEAN_MIXTURE | SAMPLE_INVALID | hc: [0, 200]<br>co: [0, 0.1]<br>co2: [0, 14]<br>o2: [2.5, 22]<br>nox: [0, 500] |
| 264 | LEAN_MIXTURE | VVT_FAILURE | hc: [0, 200]<br>co: [0, 0.1]<br>co2: [0, 14]<br>o2: [2.5, 22]<br>nox: [500, 500] |
| 265 | NORMAL_OPERATION | O2_SENSOR_BIASED_HIGH | hc: [0, 100]<br>co: [0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 0.5]<br>nox: [0, 100] |
| 266 | NORMAL_OPERATION | O2_SENSOR_BIASED_LOW | hc: [0, 100]<br>co: [0.5, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 267 | NORMAL_OPERATION | SAMPLE_INVALID | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 268 | NORMAL_OPERATION | TIMING_RETARDED | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [0, 50] |
| 269 | NORMAL_OPERATION | WORN_ENGINE | hc: [35, 100]<br>co: [0.1, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 270 | NORMAL_OPERATION | WORN_PISTON_RINGS | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [14.5, 16]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 271 | NORMAL_OPERATION | WORN_VALVE_SEALS | hc: [75, 100]<br>co: [0, 0.5]<br>co2: [13, 14.5]<br>o2: [0, 0.5]<br>nox: [0, 100] |
| 272 | O2_SENSOR_BIASED_HIGH | SAMPLE_INVALID | hc: [0, 100]<br>co: [0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 2.0]<br>nox: [0, 500] |
| 273 | O2_SENSOR_BIASED_HIGH | TIMING_RETARDED | hc: [0, 100]<br>co: [0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 0.5]<br>nox: [0, 50] |
| 274 | O2_SENSOR_BIASED_HIGH | VVT_FAILURE | hc: [0, 100]<br>co: [0, 0.2]<br>co2: [13, 16]<br>o2: [0.5, 2.0]<br>nox: [500, 500] |
| 275 | O2_SENSOR_BIASED_HIGH | WORN_PISTON_RINGS | hc: [0, 100]<br>co: [0, 0.2]<br>co2: [14.5, 16]<br>o2: [0.5, 0.5]<br>nox: [0, 100] |
| 276 | O2_SENSOR_BIASED_HIGH | WORN_VALVE_SEALS | hc: [75, 100]<br>co: [0, 0.2]<br>co2: [13, 14.5]<br>o2: [0.5, 0.5]<br>nox: [0, 500] |
| 277 | O2_SENSOR_BIASED_LOW | RICH_MIXTURE | hc: [0, 100]<br>co: [1.5, 3.0]<br>co2: [13, 14]<br>o2: [0, 0.3]<br>nox: [0, 500] |
| 278 | O2_SENSOR_BIASED_LOW | SAMPLE_INVALID | hc: [0, 100]<br>co: [0.5, 3.0]<br>co2: [13, 16]<br>o2: [0, 0.3]<br>nox: [0, 500] |
| 279 | O2_SENSOR_BIASED_LOW | TIMING_RETARDED | hc: [0, 100]<br>co: [0.5, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.3]<br>nox: [0, 50] |
| 280 | O2_SENSOR_BIASED_LOW | VVT_FAILURE | hc: [0, 100]<br>co: [0.5, 3.0]<br>co2: [13, 16]<br>o2: [0, 0.3]<br>nox: [500, 500] |
| 281 | O2_SENSOR_BIASED_LOW | WORN_ENGINE | hc: [35, 100]<br>co: [0.5, 1.0]<br>co2: [13, 16]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 282 | O2_SENSOR_BIASED_LOW | WORN_PISTON_RINGS | hc: [0, 100]<br>co: [0.5, 0.5]<br>co2: [14.5, 16]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 283 | O2_SENSOR_BIASED_LOW | WORN_VALVE_SEALS | hc: [75, 100]<br>co: [0.5, 0.5]<br>co2: [13, 14.5]<br>o2: [0, 0.3]<br>nox: [0, 500] |
| 284 | POA_SIGNATURE | RICH_MISFIRE | hc: [500, 20000]<br>co: [0.45, 15]<br>co2: [5, 14.5]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 285 | POA_SIGNATURE | RICH_MIXTURE | hc: [500, 500]<br>co: [1.5, 15]<br>co2: [0, 14]<br>o2: [0, 0.5]<br>nox: [0, 500] |
| 286 | POA_SIGNATURE | SAMPLE_INVALID | hc: [500, 20000]<br>co: [0, 15]<br>co2: [0, 14.5]<br>o2: [0, 22]<br>nox: [0, 5000] |
| 287 | POA_SIGNATURE | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [500, 20000]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 5000] |
| 288 | POA_SIGNATURE | VVT_FAILURE | hc: [500, 500]<br>co: [0, 15]<br>co2: [0, 14.5]<br>o2: [0, 22]<br>nox: [500, 5000] |
| 289 | RICH_MISFIRE | SAMPLE_INVALID | hc: [200, 20000]<br>co: [0.45, 15]<br>co2: [5, 15]<br>o2: [2.0, 22]<br>nox: [0, 5000] |
| 290 | RICH_MISFIRE | VVT_FAILURE | hc: [200, 500]<br>co: [0.45, 15]<br>co2: [5, 15]<br>o2: [2.0, 22]<br>nox: [500, 5000] |
| 291 | RICH_MIXTURE | SAMPLE_INVALID | hc: [0, 500]<br>co: [1.5, 15]<br>co2: [0, 14]<br>o2: [0, 0.5]<br>nox: [0, 500] |
| 292 | RICH_MIXTURE | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 500]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [0, 500] |
| 293 | RICH_MIXTURE | VVT_FAILURE | hc: [0, 500]<br>co: [1.5, 15]<br>co2: [0, 14]<br>o2: [0, 0.5]<br>nox: [500, 500] |
| 294 | SAMPLE_INVALID | TIMING_OVER_ADVANCED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [1000, 5000.0] |
| 295 | SAMPLE_INVALID | TIMING_RETARDED | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [13, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 50] |
| 296 | SAMPLE_INVALID | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | hc: [300, 20000.0]<br>co: [3.0, 15.0]<br>co2: [0.0, 14]<br>o2: [0.0, 0.3]<br>nox: [0.0, 5000.0] |
| 297 | SAMPLE_INVALID | VVT_FAILURE | hc: [0.0, 500]<br>co: [0.0, 15.0]<br>co2: [0.0, 22.0]<br>o2: [0.0, 22.0]<br>nox: [500, 5000.0] |
| 298 | SAMPLE_INVALID | WORN_ENGINE | hc: [35, 300]<br>co: [0.1, 1.0]<br>co2: [13, 16]<br>o2: [0.0, 0.3]<br>nox: [0.0, 100] |
| 299 | SAMPLE_INVALID | WORN_PISTON_RINGS | hc: [0.0, 100]<br>co: [0.0, 0.5]<br>co2: [14.5, 16]<br>o2: [0.0, 0.5]<br>nox: [0.0, 100] |
| 300 | SAMPLE_INVALID | WORN_VALVE_SEALS | hc: [75, 250]<br>co: [0.0, 0.5]<br>co2: [11, 14.5]<br>o2: [0.0, 0.5]<br>nox: [0.0, 5000.0] |
| 301 | TIMING_OVER_ADVANCED | VVT_FAILURE | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 302 | TIMING_OVER_ADVANCED | WORN_VALVE_SEALS | hc: [75, 100]<br>co: [0, 0.5]<br>co2: [13, 14.5]<br>o2: [0, 0.5]<br>nox: [1000, 5000] |
| 303 | TIMING_RETARDED | WORN_ENGINE | hc: [35, 100]<br>co: [0.1, 0.5]<br>co2: [13, 16]<br>o2: [0, 0.3]<br>nox: [0, 50] |
| 304 | TIMING_RETARDED | WORN_PISTON_RINGS | hc: [0, 100]<br>co: [0, 0.5]<br>co2: [14.5, 16]<br>o2: [0, 0.5]<br>nox: [0, 50] |
| 305 | TIMING_RETARDED | WORN_VALVE_SEALS | hc: [75, 100]<br>co: [0, 0.5]<br>co2: [13, 14.5]<br>o2: [0, 0.5]<br>nox: [0, 50] |
| 306 | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | VVT_FAILURE | hc: [300, 500]<br>co: [3.0, 15]<br>co2: [0, 14]<br>o2: [0, 0.3]<br>nox: [500, 5000] |
| 307 | VVT_FAILURE | WORN_VALVE_SEALS | hc: [75, 250]<br>co: [0, 0.5]<br>co2: [11, 14.5]<br>o2: [0, 0.5]<br>nox: [500, 5000] |
| 308 | WORN_ENGINE | WORN_PISTON_RINGS | hc: [35, 100]<br>co: [0.1, 0.5]<br>co2: [14.5, 16]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 309 | WORN_ENGINE | WORN_VALVE_SEALS | hc: [75, 250]<br>co: [0.1, 0.5]<br>co2: [13, 14.5]<br>o2: [0, 0.3]<br>nox: [0, 100] |
| 310 | WORN_PISTON_RINGS | WORN_VALVE_SEALS | hc: [75, 100]<br>co: [0, 0.5]<br>co2: [14.5, 14.5]<br>o2: [0, 0.5]<br>nox: [0, 100] |

**Disjoint pairs:** 230/561 (41%)

---

*Report generated by T-TH-2 box-overlap & coverage-gap analyzer.*

