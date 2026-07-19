# V3 Tunable Reweight Feasibility Map

Generated on: 2026-07-01

## Triage Summary
- **Reweightable (R)**: 8
- **Signal-Gated (S)**: 1
- **Risky (K)**: 6
- **Hard/Not Recoverable (H)**: 5
- **Total Tunable**: 20

## Detailed Case Triage
| Case ID | Expected Family (Rule) | Winner Family (Rule) | Original Score (Winner/Expected) | Expected Rank | Lift Delta | Verdict | Regressions / Absent PIDs |
|---|---|---|---|---|---|---|---|
| CASE-020 | lean_condition (LC-002) | sensor_fault (SF-001) | 0.95/0.85 | 5 | 0.050 | **RISKY** | Regresses: ['CASE-023', 'EXT-217'] |
| CASE-022 | sensor_fault (SF-002) | lean_condition (LC-001) | 1.00/0.95 | 5 | N/A | **SIGNAL-GATED** | Absent definitive PIDs: ['o2_voltage'] |
| CSV-025 | sensor_fault (SF-008) | no_fault (NF-001) | 0.93/0.86 | 5 | N/A | **HARD** |  |
| CSV-095 | exhaust_leak (EL-001) | lean_condition (LC-001) | 1.00/0.90 | 4 | 0.051 | **REWEIGHTABLE** |  |
| EXP-N014 | misfire (MF-001) | sensor_fault (SF-001) | 0.95/0.90 | 4 | 0.001 | **REWEIGHTABLE** |  |
| EXP-N020 | sensor_fault (SF-008) | rich_mixture (RM-001) | 0.95/0.86 | 4 | N/A | **HARD** |  |
| EXP-N027 | rich_mixture (RM-001) | misfire (MF-001) | 0.95/0.90 | 5 | 0.050 | **REWEIGHTABLE** |  |
| EXT-207 | catalyst_failure (CF-001) | lean_condition (LC-002) | 0.95/0.90 | 4 | 0.000 | **REWEIGHTABLE** |  |
| EXT-211 | lean_condition (LC-002) | sensor_fault (SF-001) | 0.95/0.85 | 5 | 0.050 | **RISKY** | Regresses: ['CASE-023', 'EXT-217'] |
| EXT-212 | lean_condition (LC-002) | sensor_fault (SF-001) | 0.95/0.85 | 5 | 0.050 | **RISKY** | Regresses: ['CASE-023', 'EXT-217'] |
| PDF-4G-05 | misfire (MF-005) | sensor_fault (SF-002) | 0.95/0.80 | 5 | 0.050 | **RISKY** | Regresses: ['CASE-023', 'ECU-003', 'EXP-N014', 'EXT-217'] |
| TC-046 | sensor_fault (SF-008) | no_fault (NF-001) | 0.93/0.86 | 5 | N/A | **HARD** |  |
| YAML-PDF_4G_01 | catalyst_failure (CF-002) | cam_timing (CT-002) | 0.80/0.75 | 4 | 0.001 | **REWEIGHTABLE** |  |
| era1_016 | exhaust_leak (EL-001) | lean_condition (LC-001) | 1.00/0.90 | 4 | 0.051 | **REWEIGHTABLE** |  |
| era2_011 | lean_condition (LC-002) | cam_timing (CT-008) | 1.00/0.85 | 4 | 0.050 | **RISKY** | Regresses: ['CASE-023', 'EXT-217'] |
| era2_012 | sensor_fault (SF-008) | catalyst_failure (CF-001) | 0.90/0.86 | 5 | N/A | **HARD** |  |
| era2_016 | misfire (MF-005) | no_fault (NF-001) | 0.93/0.80 | 5 | 0.001 | **RISKY** | Regresses: ['ECU-003'] |
| era3_007 | lean_condition (LC-002) | catalyst_failure (CF-001) | 0.95/0.85 | 4 | 0.010 | **REWEIGHTABLE** |  |
| era3_015 | lean_condition (LC-002) | misfire (MF-001) | 0.90/0.85 | 4 | N/A | **HARD** |  |
| era3_019 | exhaust_leak (EL-001) | lean_condition (LC-001) | 1.00/0.90 | 4 | 0.051 | **REWEIGHTABLE** |  |

## Cluster Citations & Discriminators
| Case ID | Expected vs Winner | Research Cluster | Diagnostic Discriminator |
|---|---|---|---|
| CASE-020 | lean_condition vs sensor_fault | Cluster 4 — Exhaust leak vs true lean vs biased O2 sensor | Two-point fuel trim delta (idle → 2500 RPM no-load) with air-metering architecture pre-gate, and upstream vs. downstream O₂ / wideband vs. narrowband cross-check |
| CASE-022 | sensor_fault vs lean_condition | Cluster 4 — Exhaust leak vs true lean vs biased O2 sensor | Two-point fuel trim delta (idle → 2500 RPM no-load) with air-metering architecture pre-gate, and upstream vs. downstream O₂ / wideband vs. narrowband cross-check |
| CSV-025 | sensor_fault vs no_fault | Cluster 6 — Sensor fault under-detection | Mode $06 O2 sensor dynamic response rate tests (rich-to-lean/lean-to-rich transition times) and MAF plausibility comparison (measured MAF vs calculated airflow) |
| CSV-095 | exhaust_leak vs lean_condition | Cluster 4 — Exhaust leak vs true lean vs biased O2 sensor | Two-point fuel trim delta (idle → 2500 RPM no-load) and CO₂ tailpipe dilution signature |
| EXP-N014 | misfire vs sensor_fault | Cluster 6 — Sensor fault under-detection | OBD-II Mode $06 misfire counters vs Mode $06 O2 sensor response times |
| EXP-N020 | sensor_fault vs rich_mixture | Cluster 6 — Sensor fault under-detection | Upstream vs downstream O2 sensor voltage cross-check, and Mode $06 O2 sensor response rate tests |
| EXP-N027 | rich_mixture vs misfire | Cluster 1 — Mechanical vs misfire | Tailpipe oxygen (elevated to ~5% for misfire, near 0% for rich) and carbon monoxide (high for rich, low/moderate for misfire) concentrations |
| EXT-207 | catalyst_failure vs lean_condition | Cluster 2 — Rich mixture vs catalyst failure | Fuel trim monitoring (STFT/LTFT near zero for catalyst failure, highly positive for lean condition) and Mode $06 catalyst monitor index ratio |
| EXT-211 | lean_condition vs sensor_fault | Cluster 4 — Exhaust leak vs true lean vs biased O2 sensor | Two-point fuel trim delta (idle → 2500 RPM no-load) with air-metering architecture pre-gate, and upstream vs. downstream O₂ / wideband vs. narrowband cross-check |
| EXT-212 | lean_condition vs sensor_fault | Cluster 4 — Exhaust leak vs true lean vs biased O2 sensor | Two-point fuel trim delta (idle → 2500 RPM no-load) with air-metering architecture pre-gate, and upstream vs. downstream O₂ / wideband vs. narrowband cross-check |
| PDF-4G-05 | misfire vs sensor_fault | Cluster 6 — Sensor fault under-detection | OBD-II Mode $06 misfire counters vs Mode $06 O2 sensor response times |
| TC-046 | sensor_fault vs no_fault | Cluster 6 — Sensor fault under-detection | Mode $06 O2 sensor dynamic response rate tests (rich-to-lean/lean-to-rich transition times) and MAF plausibility comparison (measured MAF vs calculated airflow) |
| YAML-PDF_4G_01 | catalyst_failure vs cam_timing | Cluster 2 — Rich mixture vs catalyst failure | Mode $06 catalyst monitor switch ratio vs cam-to-crank correlation / VVT angle commands |
| era1_016 | exhaust_leak vs lean_condition | Cluster 4 — Exhaust leak vs true lean vs biased O2 sensor | Two-point fuel trim delta (idle → 2500 RPM no-load) and CO₂ tailpipe dilution signature |
| era2_011 | lean_condition vs cam_timing | Cluster 7 — Cam timing / VVT fault | Volumetric efficiency / MAF-at-RPM signature and cam-to-crank correlation (DTC P0016-class) |
| era2_012 | sensor_fault vs catalyst_failure | Cluster 6 — Sensor fault under-detection | Mode $06 O2 sensor response rate tests vs Mode $06 catalyst monitor index ratio |
| era2_016 | misfire vs no_fault | Cluster 9 — Confirming 'no fault' reliably | Mode $06 misfire counters (to detect ECU blindness) and OBD readiness monitors |
| era3_007 | lean_condition vs catalyst_failure | Cluster 2 — Rich mixture vs catalyst failure | Fuel trim monitoring (STFT/LTFT near zero for catalyst failure, highly positive for lean condition) and Mode $06 catalyst monitor index ratio |
| era3_015 | lean_condition vs misfire | Cluster 5 — Lean-condition root cause | Mode $06 misfire counters vs fuel trim pattern across operating points (unmetered air leak trims recover at 2500 RPM, misfires do not) |
| era3_019 | exhaust_leak vs lean_condition | Cluster 4 — Exhaust leak vs true lean vs biased O2 sensor | Two-point fuel trim delta (idle → 2500 RPM no-load) and CO₂ tailpipe dilution signature |
