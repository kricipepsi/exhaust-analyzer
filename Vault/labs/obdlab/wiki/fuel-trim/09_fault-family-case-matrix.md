---
chunk: fuel-trim/09_fault-family-case-matrix
topic: fuel-trim
sources:
  - FuelTrimFamilies.md §"Comprehensive Case Diagnosis & Fuel Trim Reference Matrix" (20 cases, 5 P-code families)
consumer: COMLab fault_atlas_router + global_fault_registry.json — each case is a cross_domain_matrix calibration point (gas_lab_state + obd_live_pids idle/RPM operators + dtc p_code_match). 14 of 20 map to existing registry/KG nodes (active); 6 are new-fault PROPOSALS (see status). The idle-vs-2500RPM column pair is the discriminator fault_atlas already keys on (calc_load_pct/trims/map/coolant/maf).
consumer_status: MIXED — 14 active (validate existing nodes), 6 PROPOSAL (new nodes, register in comlab/config/proposals/)
provenance: sources/fuel-trim/FuelTrimFamilies.md (readable replacement for the "Fuel Trim Diagnostics Across Fault Families" HTML report — gate passed, 0 image placeholders)
related: [[04_trim-pattern-decision-tree]], [[10_air-fuel-metering-injector-cases]], [[11_ignition-misfire-cases-and-trim-discriminator]], [[12_emissions-egr-evap-catalyst-idle-module-cases]]
---

# Fuel-trim fault-family case matrix (20 real-world cases)

The quantified evidence base behind the decision tree (`04`). Each row is a real
diagnosed case with trims at idle and 2500 RPM — the **idle→RPM shift is the
discriminator**. "Node" maps the case to its COMLab fault node, or flags a
**PROPOSAL** where v2 has no node yet (forward-progress per root `CLAUDE.md`).

| # | DTC | STFT/LTFT idle | @2500 RPM | Root cause | Node / disposition |
|---|---|---|---|---|---|
| 1 | P0171+P0174 | +15 / +25 | 0 / +5 | Intake gasket vacuum leak (post-MAF) | ERR-LC-001 vacuum_leak_post_maf |
| 2 | P0171+P0174 | +2 / +5 | +25 / +25 | Restricted fuel filter (low delivery under load) | ERR-LC-003 fuel_pump_low_pressure (signature match; **PROPOSAL** to split a fuel_delivery_restriction discriminator) |
| 3 | P0102+P0172 | −22 / −18 | −20 / −15 | MAF circuit **ground open** → speed-density failsafe → rich | **PROPOSAL** maf_circuit_ground_open_failsafe (distinct from SF-003 under-read) |
| 4 | P0106+P0172 | −14 / −12 | −10 / −8 | MAP sensor over-reporting pressure | ERR-SF-004 map_sensor_calibration_drift |
| 5 | P0118+P0172 | 0 / 0 (failsafe) | 0 / 0 | Open ECT thermistor → false −40 °C → cold enrichment | ERR-SF-005 coolant_temp_sensor_stuck_cold / ERR-RM-006 |
| 6 | P0128 | +14 ALPHA (+14%) | +14% | Thermostat stuck open → closed-loop never reached | **PROPOSAL** thermostat_stuck_open_closedloop_delay |
| 7 | P0201+P0301 | +15 (B1) | +5 (B1) | Injector open circuit (cyl dead → false lean B1) | ERR-MF-005 dead_injector_cylinder_misfire |
| 8 | P0201+P0301 | +10 (B1) | +8 (B1) | GDI injector coil high-resistance (won't open at rail pressure) | ERR-MF-005 (refine: gdi_injector_high_resistance) |
| 9 | P0205+P0305 | +18 (cold) | 0 (warm) | Temperature-intermittent injector coil | **PROPOSAL** injector_thermal_intermittent |
| 10 | P0300 | +20 | +15 | Water-contaminated fuel → intermittent multi-misfire | **PROPOSAL** fuel_water_contamination |
| 11 | P0301 | +18 (B1) | +15 (B1) | Cylinder compression loss (intake valve leak) | ERR-MW-005 / ERR-MF-006 low_compression_mechanical_misfire |
| 12 | P0351+P0301 | +14 (B1) | +8 (B1) | Ignition coil primary open | ERR-MF-004 ignition_coil_primary_winding_failure |
| 13 | P0335 | ±15 osc | 0 (stalled) | CKP sensor thermal open | ERR-IF-003 ckp_sensor_intermittent_dropout |
| 14 | P0340 | ±5 osc | ±3 osc | Alternator rectifier diode → AC ripple corrupts CMP → batch-fire | **PROPOSAL** alternator_ac_ripple_sensor_corruption |
| 15 | P0401 | 0 / 0 | 0 / 0 | EGR insufficient flow (absence of expected lean shift) | **PROPOSAL** egr_insufficient_flow (LC-005 is the opposite, egr_stuck_open) |
| 16 | P0446+P1450 | −20 / −25 | −15 / −20 | Canister purge valve stuck open → rich | ERR-RM-004 evap_purge_valve_stuck_open |
| 17 | P0442 | 0 / 0 | 0 / 0 | Small EVAP leak — **no fuel-trim signal** (monitor-only) | ERR (none) — note: no trim consumer; out of fuel-trim scope |
| 18 | P0420 | +2 / +4 | +1 / +3 | Catalyst efficiency loss (oil-poisoned) | ERR-CF-001 catalyst_efficiency_below_threshold |
| 19 | P0505 | +12 / +18 | +3 / +5 | IAC body gasket vacuum leak (hunting idle) | ERR-LC-001 vacuum_leak_post_maf (idle-control variant) |
| 20 | P0606 | 0 / 0 (limp) | 0 / 0 | O₂ heater corrosion → inductive spike → false ECM fault | ERR-ECU-001 + sensor_fault (O₂ heater) |

## How the matrix is consumed

`fault_atlas_router` discriminates candidates using exactly these axes:
`shrtft1/longft1` (+b2), `calc_load_pct`, `map_kpa`, `coolant_temp_c`,
`mass_airflow_gps`, and DTC `p_code_match`. Each row above is a calibration point
for an existing node's `cross_domain_matrix` in `global_fault_registry.json`, or a
new node to register. The decisive feature for most is the **idle→RPM direction**:

- **Drops toward 0 at RPM** (rows 1, 19): unmetered-air / vacuum-leak family.
- **Worsens at RPM** (row 2): fuel-delivery restriction.
- **Flat across RPM** (rows 3, 4, 16): sensor-bias / fuel-pressure (RPM-independent).
- **Single-bank only** (rows 7, 8, 11, 12): cylinder/injector/coil-specific.
- **0/0 despite a driveability fault** (rows 5, 6, 15, 20): open-loop / failsafe —
  trims are frozen, so *trim silence + symptom* is itself the signal (cross-ref `06`, `08`).

Citation: FuelTrimFamilies.md case matrix (cases 1–20), idle and 2500-RPM
STFT/LTFT columns and root-cause column. Node IDs per
`comlab/config/global_fault_registry.json` + `comlab/config/kg/*.json`.


## Core Entities

- P0171, P0174, P0172, P0102, P0128, P0301, P0335, P0340, P0401, P0420, P0606
- VACUUM_LEAK, FUEL_STARVATION, THERMOSTAT_STUCK_OPEN, CKP_SENSOR_DROPOUT, CATALYST_EFFICIENCY_LOSS
- fault_atlas_router + global_fault_registry.json (consumer; 14 active / 6 PROPOSAL)

## Graph relations (explicit)

**P0171** plus **P0174** INDICATES **VACUUM_LEAK**
**P0102** plus **P0172** INDICATES **MAF_UNDERREPORT** ground-open failsafe
**P0128** INDICATES **THERMOSTAT_STUCK_OPEN**
**P0335** INDICATES **CKP_SENSOR_DROPOUT**
**P0420** INDICATES **CATALYST_EFFICIENCY_LOSS**
**fault_atlas_router** DISCRIMINATES cases by idle-to-2500RPM trim shift
**fault-family-case-matrix** CALIBRATES **global_fault_registry.json**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
