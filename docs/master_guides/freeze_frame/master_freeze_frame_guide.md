# Master Freeze Frame Guide — 4D Petrol Diagnostic Engine

**Purpose.** A single, self-contained reference for OBD-II freeze frame data (SAE J1979 Mode $02) — what parameters are stored and why, the physical meaning of calculated load, coolant temperature, RPM, vehicle speed, fuel system status, and fuel trim values in context, and the physical justification for every threshold in the 4D engine's `freeze_frame.py` module and the `freeze_frame:` section of `schema/thresholds.yaml`. The 4D engine's L4 layer is built on the rules below; all freeze-frame-derived symptoms (`ff_open_loop_at_fault`, `ff_load_high_at_low_rpm`, `ff_ect_warmup`, `ff_iat_ect_biased`, `ff_timing_retard_severe`, `ff_codes_cleared_invalidated`) cite §-numbers from this guide.

---

## 1. What freeze frame data is

When a DTC meets its confirmation criteria (typically the second consecutive drive cycle where the monitor fails), the ECU captures a snapshot of operating conditions and stores it alongside the DTC. This snapshot is **freeze frame** — Mode $02 in SAE J1979.

A DTC tells you *what* failed. Freeze frame tells you *under what conditions* it failed. The difference is often the difference between chasing a fault blind and knowing exactly what to reproduce. Freeze frame data is the single most underused diagnostic parameter available to a technician with an OBD-II scanner.

**Single-frame priority rule (SAE J1979 §5.3):** The ECU stores freeze frame for the *first* emissions-critical DTC of the session. A later DTC overwrites the frame only if no earlier emissions DTC is present. In practice: if P0171 set first and then P0420 set on the same drive, the freeze frame belongs to P0171. If both are present and the freeze frame shows conditions inconsistent with catalyst testing (ECT < 70 °C, RPM not steady at cruise), the catalyst DTC is the later code and its freeze frame is missing.

---

## 2. Mandatory vs. extended freeze frame PIDs

#### 2.1 Mandatory minimum (SAE J1979 Mode $02)

| PID (hex) | Parameter | Unit | Diagnostic use |
|-----------|-----------|------|----------------|
| **02** | Freeze DTC | — | Which DTC triggered storage |
| **03** | Fuel system status | — | Open loop / closed loop for banks 1 and 2 |
| **04** | Calculated load value (CLV) | % | Engine load at fault time — see §3 |
| **05** | Engine coolant temperature | °C | ECT at fault time — see §4 |
| **06** | STFT Bank 1 | % | Instantaneous fuel correction at fault time |
| **07** | LTFT Bank 1 | % | Learned fuel correction at fault time |
| **0B** | Intake manifold absolute pressure | kPa | MAP at fault time |
| **0C** | Engine RPM | min⁻¹ | Engine speed at fault time |
| **0D** | Vehicle speed | km/h | Road speed at fault time |
| **0E** | Ignition timing advance | ° | Spark advance at fault time |
| **0F** | Intake air temperature | °C | IAT at fault time |
| **10** | MAF air flow rate | g/s | Airflow at fault time |
| **11** | Absolute throttle position | % | Throttle opening at fault time |

Sources: SAE J1979; Saab WIS OBD-II documentation; Ford PCED OBD-II reference.

#### 2.2 Manufacturer-extended PIDs (commonly available)

Beyond the mandatory set, many ECUs also store: O₂ sensor voltages (B1S1, B1S2, B2S1, B2S2), STFT/LTFT for Bank 2, commanded EGR (%), commanded EVAP purge (%), battery voltage, barometric pressure, fuel level, run time since engine start (seconds), and fuel rail pressure. These correspond to the `FreezeFrameRecord` fields in `engine/input_model.py`. Barometric pressure and commanded EGR are especially useful — see §8.

---

## 3. Calculated Load Value (CLV) — the most important freeze frame parameter

Calculated Load Value (CLV) is defined by SAE J1979 as the **percentage of peak available torque** at current RPM. It reaches 100 % at wide-open throttle at any altitude, any temperature, and any RPM — for both naturally aspirated and boosted engines. It is not the same as throttle position.

**SAE J1979 definition:** `CLV = (current airflow) / (peak airflow at WOT under standard conditions) × 100 %`

| CLV range | Engine condition | Diagnostic implication |
|-----------|-----------------|----------------------|
| **5–25 %** | Idle or very light cruise | Fault set at idle — check idle circuits, EVAP, EGR, vacuum leaks |
| **25–50 %** | Light to moderate cruise | Fault set under part-throttle — typical for sensor drift, sustained fuel trim codes |
| **50–70 %** | Moderate to heavy load | Fault set under significant demand — fuel delivery, MAF accuracy |
| **70–85 %** | Heavy acceleration, grade, towing | Fault set under physical stress — ignition breakdown, fuel pump volume, boost leaks |
| **85–100 %** | Near-WOT or WOT | Fault set at maximum demand — fuel pressure drop, MAF saturation, coil output |

**Physical basis for the 70 % threshold** used in the 4D engine: The 70 % CLV boundary is the established industry demarcation between "moderate load" and "high-stress load." Per Innova and Autodtcs diagnostic documentation, high load is defined as above 70–75 % CLV. Above 70 %, the engine is under significant demand — accelerating hard, climbing a grade, or towing. Fuel delivery, ignition output, and airflow are at or near their maximum demands. A fault setting above 70 % CLV is a stress-related fault; this directs the diagnostic path toward fuel delivery volume, ignition coil output under load, MAF saturation, and high-RPM sensor accuracy.

**Physical basis for the 30 % threshold:** Below 30 % CLV at moderate or low RPM, the engine is at idle or very light cruise. Per industry guidance: "Low load (under 30 %) at moderate RPM means the vehicle was cruising lightly or idling." This directs the path toward idle circuits (IAC, ETC), EVAP purge, EGR operation, vacuum-leak signatures at idle, and cold-start systems.

---

## 4. Engine coolant temperature (ECT) in freeze frame

| Freeze frame ECT | Engine state at fault time | 4D engine action |
|-----------------|---------------------------|-----------------|
| **< 40 °C** | Open-loop cold start | Flag `ff_ect_warmup`; suppress mechanical-rich and catalyst candidates; gate cold-start enrichment per `master_cold_start_guide.md §4` |
| **40–70 °C** | Warm-up transition (open-to-closed loop) | Flag `ff_ect_warmup`; mixture still stabilising; weight fuel trim evidence lower |
| **≥ 70 °C** | Fully warm — normal operating temperature | Freeze frame evidence is valid; all candidates eligible |
| **≥ 100 °C** | Unusually hot at fault time | Flag `ff_hot_running`; consider cooling system or heat-related component failure |

**Physical basis for the 70 °C threshold:** SAE and OEM service documentation consistently use 70 °C (158 °F) as the ECT threshold between "warm-up" and "normal operating temperature." At 70 °C, cold-start enrichment has fully decayed, the O₂ sensor has reached operating temperature, and the catalyst has surpassed light-off temperature (~250–300 °C internal). Nissan's OBD documentation explicitly gates freeze-frame interpretation on ECT ≥ 70 °C. If freeze frame ECT < 70 °C, the fault set during warm-up and its conditions may no longer be reproducible at hot idle.

**Catalyst monitor enable:** P0420 requires ECT ≥ 70 °C to be a valid test. A P0420 freeze frame with ECT < 70 °C was set before the catalyst reached operating temperature — flag `dtc_set_outside_enable_window` and demote the catalyst-failure candidate. Cross-ref `master_catalyst_guide.md §3`.

---

## 5. RPM in freeze frame

**Physical basis for the 900 RPM threshold:** Most warm petrol engines idle between 600–850 RPM. 900 RPM is the upper bound of normal warm idle speed; above this, either the engine was under some throttle input or the idle is elevated (A/C compressor, alternator load, cold fast-idle). A freeze frame showing ≤ 900 RPM combined with CLV ≤ 30 % and vehicle speed = 0 confirms a stationary-idle fault, reproducible in the workshop bay without a road test.

---

## 6. Vehicle speed in freeze frame

Vehicle speed = 0 km/h confirms the vehicle was stationary when the fault set. Combined with idle RPM and low CLV, this confirms the fault is reproducible at idle. Combined with high CLV and high RPM, this indicates a stationary revving test or a stationary high-idle condition (e.g., fast idle on cold start, A/C compressor load).

---

## 7. Fuel system status — the most critical freeze frame parameter for DTC validity

The fuel system status PID (Mode $01/$02 PID $03) indicates whether the ECU is in open or closed loop at fault time.

| Fuel system status | Meaning | Effect on DTC validity |
|-------------------|---------|----------------------|
| **OL (Open Loop)** | ECU using base fuel map; O₂ sensor not active | Fuel trim and mixture DTCs (P0171, P0172) are **not valid** — the ECU was not yet using O₂ feedback |
| **CL (Closed Loop)** | Normal O₂ feedback control | Fuel trim DTCs are valid |
| **OL-DRIVE** | Open loop due to driving conditions (high load, decel, WOT) | Rich DTC at high load may reflect intentional power enrichment, not a fault |
| **OL-FAULT** | Open loop due to a detected fault (O₂ sensor not ready) | The O₂ sensor was faulty at fault time — lean/rich DTCs may be O₂ sensor failures |

**Critical rule for the 4D engine:** If freeze frame `fuel_system_status = OL` or `OL_FAULT` for a fuel-trim DTC (P0171, P0172), the DTC was set before the O₂ sensor was active. Flag `ff_open_loop_at_fault` and demote all fuel-mixture fault candidates from that DTC. Cross-ref `master_cold_start_guide.md §5`.

---

## 8. Interpreting STFT/LTFT in freeze frame

Freeze frame fuel trims are the most context-rich diagnostic parameters — they show what the ECU was doing *at the exact moment* the fault was detected:

| Freeze frame trim pattern | Diagnostic interpretation |
|--------------------------|--------------------------|
| LTFT +20 % when P0171 set | Lean condition was **chronic** — accumulating for multiple drive cycles before the DTC confirmed |
| STFT swinging +20 % / −5 % | Active, fluctuating lean condition — consistent with an intermittent vacuum leak or fuel delivery issue |
| STFT pegged +25 %, LTFT 0 % | Codes recently cleared — ECU has not yet re-learned the persistent lean condition |
| Both STFT and LTFT within ±10 % | Fuel control was normal; DTC may not be a mixture fault in closed loop |
| LTFT −25 % sustained | Chronic rich condition; check EVAP purge, fuel pressure, leaking injector |
| STFT negative spike at specific RPM | Load-dependent rich event (EVAP purge open at cruise, GDI high-pressure fuel event) |

---

## 9. Physical justification for all thresholds.yaml freeze-frame values

The `schema/thresholds.yaml` `freeze_frame:` block in the 4D engine contains the following thresholds, each with documented physical basis:

| Parameter | Value | Physical basis |
|-----------|-------|---------------|
| `load_high_threshold` | **70 %** | SAE/Innova/Autodtcs industry standard for high-stress load boundary. Above 70 % CLV, fault is stress-related (fuel delivery, ignition, boost). |
| `load_low_threshold` | **30 %** | Below 30 % CLV at moderate RPM, engine is at idle or very light cruise. Fault is idle-circuit or EGR/EVAP-related. |
| `ect_warmup_max` | **60 °C** | Below 60 °C, the engine is still in warm-up transition (40–70 °C range). Fuel enrichment residuals may still be present. Faults before 60 °C are warm-up faults, not steady-state faults. |
| `load_rpm_threshold` | **1500 RPM** | Below 1500 RPM with CLV > 70 % indicates a high-load condition at low engine speed — consistent with stalling under load, torque converter stall, or clutch-slip scenario. This is abnormal and warrants flagging `ff_load_high_at_low_rpm`. |
| `timing_retard_threshold` | **−10°** | Timing advance < −10° (degrees retarded from TDC) indicates the ECU is pulling timing significantly — consistent with persistent knock, a retarded cam phaser, or a coolant temperature fault causing over-enrichment. The ECU typically retards 1–3° for a mild knock event; more than −10° is a structural fault. |
| `iat_ect_delta_threshold` | **30 °C** | When `|IAT − ECT| > 30 °C` at RPM = 0 (engine off), IAT and ECT should have equalised. A delta > 30 °C with RPM = 0 in freeze frame suggests one sensor is biased or the vehicle was parked in extreme ambient conditions when the fault set. |

---

## 10. Freeze frame symptom derivation rules for the 4D engine

The `freeze_frame.py` module derives six symptoms. Physical rationale for each:

| Symptom | Trigger condition | Physical rationale |
|---------|-------------------|-------------------|
| `ff_open_loop_at_fault` | `fuel_status ∈ {OL_DRIVE, OL_FAULT, OL}` | DTC was set before O₂ feedback was active — fuel trim DTCs are invalid |
| `ff_load_high_at_low_rpm` | CLV > 70 % AND RPM < 1500 | High load at low RPM = engine stalling under demand; fault is torque or fuel delivery |
| `ff_ect_warmup` | ECT < 60 °C | Fault set during warm-up transition; cold-enrichment residuals may still be present |
| `ff_iat_ect_biased` | `|IAT − ECT| > 30` AND RPM = 0 | One temperature sensor biased; check ECT or IAT wiring |
| `ff_timing_retard_severe` | ignition_advance < −10° | ECU pulled timing significantly — persistent knock, VVT retard, or enrichment fault |
| `ff_codes_cleared_invalidated` | `codes_cleared = True` (from context) | Codes were cleared before testing — LTFT is reset; DTC may not re-confirm in test session |

---

## 11. When freeze frame conditions contradict the current complaint

A stored code with freeze frame showing conditions completely different from the current complaint is probably a historical fault, not the current failure. Example: a car arrives with a crank-no-start complaint. Stored P0300 random misfire. Freeze frame: ECT 90 °C, CLV 78 %, vehicle speed 85 km/h. The misfire code set on a highway pull — not during cranking. The 4D engine should weight freeze-frame evidence lower when freeze-frame operating conditions contradict the reported symptoms. Flag `dtc_set_during_warmup` (if ECT differs significantly from current ECT and the DTC set at cold conditions) or note the historical nature of the code.

---

## 12. Barometric pressure in freeze frame

The freeze frame `barometric_pressure` PID — available on extended-freeze-frame vehicles — is the ECU's stored ambient pressure at fault time. The ECU uses this for fuel and ignition calculations. If the barometric pressure in freeze frame is significantly lower than the current reading (e.g., vehicle was at high altitude when fault set, now at sea level), fuel trim readings from that freeze frame may not be reproduced at the current location. The BARO PID updates accurately during high-load "snap-throttle" tests per `master_air_induction_guide.md §8`.

---

## 13. Freeze frame and 5-gas analysis — integrated interpretation

Freeze frame conditions contextualise gas readings that would otherwise be ambiguous.

#### 13.1 Idle-confirmed faults

When freeze frame shows vehicle speed = 0 km/h, RPM ≤ 900, and CLV ≤ 30 %, the fault set at stationary idle. The 5-gas idle test directly reproduces the fault conditions. If idle gases are clean but freeze frame shows high load and high RPM, the engine passed the idle test but may fail under the operating conditions where the DTC originally set. Do not clear the code on clean idle gases alone — reproduce the freeze frame conditions.

#### 13.2 ECT at fault time vs. ECT during test

| Freeze frame ECT | Test ECT | Diagnostic implication |
|-----------------|----------|----------------------|
| < 40 °C | 85 °C+ | Fault set cold; test is hot. Cold-start enrichment, EGR disable, and O₂ sensor not yet active at fault time. Reproduce cold. |
| 40–70 °C | 85 °C+ | Fault set during warm-up transition. Fuel trims still stabilising. Reproduce warm-up or cold soak. |
| 85 °C+ | 85 °C+ | Fault conditions reproduced. Test results are directly applicable. |

#### 13.3 Fuel trim at fault vs. fuel trim during test

Comparing freeze-frame STFT/LTFT with current live-data fuel trims at matching RPM/load reveals whether the fault is **chronic** (trims still abnormal — persistent condition), **intermittent** (trims normal now — fault was transient), or **recently cleared** (LTFT near zero, STFT active — ECU has not re-learned). A chronic lean freeze-frame trim that has since normalised strongly suggests an intermittent vacuum leak or a fuel delivery issue that is temperature-dependent.

#### 13.4 The open-loop-at-fault integration rule

When freeze frame shows OL or OL-FAULT fuel status and the DTC is P0171/P0172/P0174/P0175, the DTC was set *before* closed-loop fuel control was active. The O₂ sensor was not yet at operating temperature, or a sensor fault forced open-loop operation. The fuel trim values stored in this freeze frame reflect open-loop base-map operation, not closed-loop correction. Do not use open-loop freeze-frame fuel trims to diagnose a closed-loop fuel control problem. Flag `ff_open_loop_at_fault` and suppress mixture-fault routing for this DTC.

---

## 14. Common diagnostic pitfalls with freeze frame data

**Pitfall 1 — Treating freeze frame as current data.** Freeze frame is a snapshot of the *past*. The vehicle may have been driven hundreds of kilometres since the DTC set. Current live data may not match freeze frame conditions. Always compare freeze-frame operating conditions with current conditions before concluding the fault is still present.

**Pitfall 2 — Ignoring the single-frame priority rule.** If multiple DTCs are present and freeze frame shows conditions inconsistent with the primary DTC (e.g., cold ECT for a catalyst efficiency DTC), the frame belongs to an earlier DTC. The later DTC has no freeze frame of its own. Diagnose the DTC that owns the freeze frame first.

**Pitfall 3 — Misreading CLV as throttle position.** CLV is torque-based, not position-based. A turbocharged engine at 2500 RPM under boost can reach 85 % CLV at 30 % throttle opening. Using throttle position instead of CLV will misclassify the fault condition.

**Pitfall 4 — Assuming freeze frame conditions are reproducible.** A freeze frame captured during a transient event (gear shift, tip-in enrichment, decel fuel cut) may record conditions that cannot be held steady-state. Diagnose the pattern, not the exact snapshot values.

**Pitfall 5 — Neglecting era capability.** Pre-2006 vehicles have mandatory-only freeze frame — extended PIDs (BARO, commanded EGR, fuel level, run time) are absent. The 4D engine must not penalise confidence for missing extended PIDs on era-appropriate vehicles. Gate extended-PID expectations on the vehicle's era bucket per R6.

**Pitfall 6 — Misattributing fuel trim to the wrong DTC.** When multiple DTCs are stored and one is P0171, fuel trims stored in freeze frame belong to the DTC that owns the frame (first emissions-critical DTC set). Using P0171 freeze frame trims to diagnose a later P0420 is invalid.

**Pitfall 7 — Over-weighting freeze frame MAF at idle.** The MAF PID in freeze frame at idle (CLV < 30 %) is a low-airflow reading where hot-wire MAF contamination effects are most pronounced. A freeze-frame MAF reading at idle should not be used as a MAF accuracy check without corroborating cruise-RPM MAF data.

---

## 15. Freeze frame quick-reference — DTC-to-FF diagnostic routing

| DTC family | Critical FF PIDs to inspect | Diagnostic question |
|-----------|---------------------------|-------------------|
| P0171/P0174 (Lean) | STFT, LTFT, fuel system status, ECT | Was the ECU in closed loop? Was ECT ≥ 70 °C? Are trims confirming lean at fault time? |
| P0172/P0175 (Rich) | STFT, LTFT, fuel system status, ECT | Was the ECU in closed loop? Are trims negative at fault time? |
| P0300–P0308 (Misfire) | CLV, RPM, ECT, vehicle speed | Was the misfire under load or at idle? Cold or hot? |
| P0401 (EGR Insufficient) | CLV, RPM, vehicle speed, ECT | Was the fault at cruise load (where EGR should be open)? |
| P0402 (EGR Excessive) | CLV, RPM, ECT | Was the fault at idle (where stuck-open EGR hits hardest)? |
| P0420 (Catalyst) | ECT, RPM, vehicle speed, CLV | Was ECT ≥ 70 °C? Was the test at steady cruise? |
| P060x (ECU Internal) | Battery voltage, run time | Was battery voltage normal? Was this a cold-start event? |
| EVAP codes (P0440–P0457) | Fuel level, CLV, ECT, vehicle speed | Was fuel level 15–85 %? Was ECT cold (cold-start leak test) or hot (running-loss test)? |

---

## 16. Era-specific freeze frame capability and the 4D engine

Freeze frame data availability varies significantly by era bucket (R6). The 4D engine must adapt its evidence weighting based on what freeze frame data the vehicle's ECU is capable of storing.

| Era bucket | Mandatory PIDs | Extended PIDs typically available | 4D engine adaptation |
|------------|---------------|----------------------------------|---------------------|
| **1990–1995** | None — OBD-I; manufacturer-specific freeze frame if any | Rare; some high-end ECUs store rudimentary snapshots | Do not expect freeze frame. Gas analysis is primary. `freeze_frame_present` flag = false on most inputs. Confidence ceiling reduced per L16 (gas-only: 0.40). |
| **1996–2005** | 13 mandatory Mode $02 PIDs | Some extended PIDs on premium brands; BARO may be absent | Full freeze frame analysis for mandatory PIDs. Extended PIDs expected only if vehicle is CAN-equipped or premium-brand. Missing BARO is not a fault. |
| **2006–2015** | 13 mandatory + commonly 6–8 extended | BARO, commanded EGR, EVAP purge, fuel level, run time | Full freeze frame. Missing extended PIDs flagged as `ff_limited_capability` (warning, not blocking). |
| **2016–2020** | Full Mode $02 + Mode $09 calibration data | Rich freeze frame: BARO, fuel rail pressure, O₂ sensor heater status, GPF pressure | Full freeze frame analysis. Extended data expected. Missing BARO or fuel rail pressure on GDI vehicles is unusual — flag as `ff_data_gap`. |

**The `ff_limited_capability` warning:** When a vehicle's era bucket predicts extended PIDs should be available but the freeze frame contains only mandatory PIDs, the 4D engine surfaces `ff_limited_capability` as a non-blocking warning. This may indicate: a budget OBD-II scanner was used (not retrieving all available PIDs), the ECU does not support the extended PID set for that era, or the freeze frame memory was partially overwritten. The warning reduces evidence-layer confidence for freeze-frame-derived symptoms but does not block diagnosis.

---

## 17. Cross-references

- `master_obd_guide.md §7` — freeze frame attachment rules, SAE J1979 Mode $02
- `master_cold_start_guide.md §5` — open-loop fuel status in freeze frame as DTC validity gate
- `master_catalyst_guide.md §3` — catalyst monitor enable conditions in freeze frame
- `master_fuel_trim_guide.md §3` — normal STFT/LTFT ranges that contextualise freeze frame values
- `master_ecu_guide.md §5` — T15 startup phase and KAM reset effects on LTFT
- `master_air_induction_guide.md §8` — BARO PID update from snap-throttle test

---

## 18. Citations

- SAE J1979 — Mandatory and optional freeze frame PIDs, Mode $02 specification
- Saab WIS OBD-II technical documentation — ECT operating temperature gate
- Ford PCED (Powertrain Control/Emissions Diagnosis) OBD-II reference guide
- Innova Diagnostic Reference: Calculated load interpretation bands
- Autodtcs freeze frame documentation: 70 % load threshold definition
- Nissan OBD service documentation: ECT ≥ 70 °C gate for freeze frame validity
- AVI OnDemand: "Fuel Trim Diagnosis and O2 Sensor Performance"
- OBD-II PIDs — Wikipedia, accessed 2026-05-03
