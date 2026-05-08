# Master Turbo Guide — 4D Petrol Diagnostic Engine

**Purpose.** A single, self-contained reference for forced induction on petrol engines (MY 1990–2020) — the physics of boost, the boost-corrected breathing-cluster formula (MAP × IAT × RPM × boost_ratio) that the 4D engine uses to compute volumetric efficiency in M1, the canonical gas-analyser signatures for boost leak, wastegate fault, and turbo mechanical failure, the physical justification for every threshold the 4D engine uses in the `turbo_underboost`, `turbo_overboost`, `turbo_boost_leak`, and `turbo_mechanical_degraded` KG nodes, and the DTC-to-cause mapping for the P0234–P0299 family. Rows in the CSV that cite turbocharger faults as the expected diagnosis cite the rules below.

---

## 1. What a turbocharger does — the physics of forced induction

A turbocharger recovers exhaust-gas kinetic and thermal energy to drive a turbine, which spins a compressor that forces additional air mass into the engine. The result is higher charge density — more oxygen molecules per intake stroke — enabling more fuel to be burned per cycle and producing more power from the same displacement.

### 1.1 The energy chain

```
Exhaust pulse → turbine wheel (extracts ~25 % of exhaust enthalpy)
    → common shaft → compressor wheel (adiabatic compression)
        → compressed intake charge → charge air cooler (intercooler) → intake manifold
```

### 1.2 The three physical effects of boost

**Charge density increase (dominant):** At 1 bar boost (gauge), absolute manifold pressure is ~2.0 bar. The charge contains roughly twice the oxygen mass per unit volume compared to naturally aspirated operation. The actual density gain is less than the pressure ratio alone would suggest because compression heating raises charge temperature — this is why intercooling is critical.

**Compression heating (undesirable):** Adiabatic compression heats the charge. A compressor operating at 70 % efficiency producing a pressure ratio of 1.5 heats the charge by approximately 50–60 °C above ambient. Hotter charge = lower density = less oxygen per stroke = less power. The intercooler is the remedy — it rejects compression heat to ambient air before the charge enters the intake manifold.

**Exhaust backpressure penalty (trade-off):** The turbine restricts exhaust flow. Exhaust manifold pressure can reach 2–3× the intake boost pressure. This creates a pumping loss — the piston must push against elevated exhaust pressure during the exhaust stroke. A well-matched turbo keeps the intake-to-exhaust pressure ratio close to 1.0 at cruise; a mismatch (small turbo at high RPM) can drive exhaust pressure far higher, reducing net gain from boost.

---

## 2. The boost-corrected breathing-cluster formula

The 4D engine computes volumetric efficiency for forced-induction engines using the **boost-corrected breathing-cluster formula.** This is a required deliverable per the P0 task verification section.

```
breathing_cluster_score = f(MAP, IAT, RPM, boost_ratio)
```

Where:

| Variable | Definition | Unit | Sensor / Source |
|----------|-----------|------|----------------|
| **MAP** | Manifold Absolute Pressure | kPa | MAP sensor (OBD PID 0x0B) |
| **IAT** | Intake Air Temperature | °C (converted to K for density calc) | IAT sensor (OBD PID 0x0F) |
| **RPM** | Engine speed | min⁻¹ | Crankshaft position sensor (OBD PID 0x0C) |
| **boost_ratio** | MAP / barometric_pressure | dimensionless | Computed: MAP ÷ BARO (OBD PID 0x33) |

### 2.1 Physical interpretation

The breathing cluster quantifies how efficiently the engine moves air mass per cycle, accounting for forced induction. The formula corrects the naturally aspirated breathing model in three ways:

**MAP (forced-induction primary):** In a naturally aspirated engine, MAP is always ≤ BARO (vacuum or atmospheric). In a turbo engine, MAP exceeds BARO under boost — the MAP term captures this directly. A MAP reading of 150 kPa at sea level (BARO ≈ 101 kPa) implies boost_ratio ≈ 1.49.

**IAT correction (density temperature-dependence):** The ideal gas law (PV = nRT) states that density ∝ 1/T for a given pressure. A 60 °C charge (333 K) carries ~18 % less oxygen per litre than a 20 °C charge (293 K) at the same MAP. The IAT term compensates for this, penalising high intake temperatures that reduce effective charge density despite high MAP readings.

**RPM × MAP interaction (airflow rate):** At a given MAP, higher RPM means more intake strokes per second → more air consumed → more power. The product MAP × RPM approximates the engine's airflow rate, which is the fundamental input to the fuel calculation.

**boost_ratio (normalisation factor):** Dividing MAP by BARO normalises for altitude. A MAP of 120 kPa at altitude (BARO = 85 kPa, boost_ratio = 1.41) represents more turbo work than 120 kPa at sea level (BARO = 101 kPa, boost_ratio = 1.19). Without boost_ratio, a high-altitude vehicle with a hard-working turbo could appear identical to a sea-level vehicle with a lazy turbo.

### 2.2 Cluster thresholds

| Parameter | Value | Unit | Condition | Source guide |
|-----------|-------|------|-----------|-------------|
| `boost_normal_idle_ratio` | 0.85–1.05 | — | Idle, warm, turbo not spooled | `docs/master_guides/turbo/master_turbo_guide.md` §2.2 |
| `boost_cruise_ratio_min` | 0.95 | — | Part-throttle cruise, wastegate modulating | `docs/master_guides/turbo/master_turbo_guide.md` §2.2 |
| `boost_wot_target_ratio` | 1.40–2.20 | — | WOT, dependent on engine and era | `docs/master_guides/turbo/master_turbo_guide.md` §4 |
| `boost_leak_ratio_deviation` | −15 | % | Deviation below target boost_ratio for given RPM/MAP | `docs/master_guides/turbo/master_turbo_guide.md` §5.2 |
| `boost_overboost_ratio_deviation` | +20 | % | Deviation above target → wastegate or VNT control fault | `docs/master_guides/turbo/master_turbo_guide.md` §5.3 |
| `iat_penalty_per_10c` | 3 | % | Per 10 °C IAT above 40 °C | `docs/master_guides/air_induction/master_air_induction_guide.md` |
| `intercooler_efficiency_min` | 70 | % | Charge air cooler temp drop ÷ (IAT_compressor_outlet − ambient) | `docs/master_guides/turbo/master_turbo_guide.md` §5.5 |

---

## 3. Turbocharger types in petrol engines (1990–2020)

| Type | Era | Boost control | Key failure modes | Notes |
|------|-----|--------------|-------------------|-------|
| **Single wastegated turbo** | 1980s–present | Pneumatic or electronic wastegate actuator bypasses exhaust around turbine at target boost | Wastegate stuck closed (overboost); wastegate stuck open (underboost); actuator diaphragm leak; boost control solenoid failure | Most common petrol turbo type. Wastegate spring sets base boost; ECU bleeds pressure to raise boost above spring value. |
| **Twin-scroll turbo** | Late 1990s–present | Wastegate as above; divided turbine housing separates exhaust pulses from paired cylinders | Same as wastegated + scroll divider cracking | Improves low-end response by reducing exhaust pulse interference. Common on BMW N54/N55, VAG EA888. |
| **VNT / VGT (variable geometry)** | Late 1990s–present (petrol); earlier on diesel | Movable vanes in turbine housing alter A/R ratio; ECU positions vanes for optimal response | Vane mechanism carbon-stuck; actuator failure; vane ring wear | Rare on petrol until ~2006+ due to higher exhaust temperatures (petrol ~950 °C vs diesel ~750 °C); requires high-temp materials (Inconel). |
| **Twin-turbo (parallel)** | 1990s–present | Two smaller turbos, one per bank (V6/V8) | One turbo failing → bank-to-bank imbalance; gas signature shows asymmetric breathing | Common on Nissan 300ZX, Audi 2.7T, BMW N54 (twin, not twin-scroll). |
| **Sequential twin-turbo** | 1990s–2000s | Small turbo for low RPM, large turbo for high RPM; transition valve controls handover | Transition valve stuck; one turbo offline; complex vacuum/boost control maze | Common on MkIV Supra 2JZ-GTE, Mazda RX-7 FD, Subaru Legacy B4. Harder to diagnose due to transitional behaviour. |
| **Electric supercharger** | 2016–2020 | Electric motor spins compressor; no exhaust turbine | Motor/controller failure; electrical, not mechanical, DTCs | Very late-era; Volvo, Audi mild-hybrid applications. |
| **Twin-charged (supercharger + turbo)** | 2000s | Roots/screw supercharger for low RPM; turbo for mid-high RPM; clutch-controlled handover | Handover clutch failure; bypass valve fault; complex breathing model needed | VW 1.4 TSI Twincharger. |

---

## 4. Boost targets by era — reference table

| Era bucket | Typical boost (WOT, sea level) | Boost control | Typical turbo configuration |
|------------|-------------------------------|---------------|---------------------------|
| 1990–1995 | 0.5–0.8 bar (gauge) | Mechanical wastegate, simple boost control solenoid | Single journal-bearing, oil-cooled |
| 1996–2005 | 0.6–1.0 bar (gauge) | Electronic boost control, OBD-II monitored | Single water-cooled, ball-bearing optional |
| 2006–2015 | 0.7–1.5 bar (gauge) | ECU integrated, torque-target boost strategy | Twin-scroll or VNT emerging on petrol |
| 2016–2020 | 0.8–2.0+ bar (gauge) | Full ECU authority, cylinder-pressure modelling | Twin-scroll, VNT, or twin-turbo; electric wastegate |

**Altitude correction:** Boost pressure targets are absolute; the boost_ratio normalisation (§2) compensates for altitude automatically. A vehicle at 1500 m elevation (BARO ≈ 85 kPa) with a MAP of 120 kPa is operating at the same boost_ratio (1.41) as a sea-level vehicle at 142 kPa MAP.

---

## 5. Gas signatures — the four canonical turbo fault states

### 5.1 Normal forced-induction operation

| HC | CO | CO₂ | O₂ | λ | MAP (WOT) | boost_ratio |
|----|-----|------|-----|-----|-----------|------------|
| Normal | Normal | Normal (13–15 %) | Normal (0.5–1.5 %) | ≈1.00 | ≥ target per era | ≥ 1.20 at WOT |

All gas readings appear normal because the ECU's airflow model (MAF or speed-density) measures the actual air mass and fuels accordingly. Boost ≠ mixture change; boost = more air + proportionally more fuel → same lambda.

### 5.2 Boost leak (underboost)

| HC | CO | CO₂ | O₂ | λ | MAP | boost_ratio |
|----|-----|------|-----|-----|-----|------------|
| Normal | Normal | Normal | Normal | **> 1.00 (lean under load)** | Below target | Below target by ≥ 15 % |

**Physical mechanism:** Compressed charge escapes through a leak between compressor outlet and intake manifold — typically a split intercooler hose, loose hose clamp, punctured intercooler, or leaking blow-off/diverter valve. Air that the MAF measured and the ECU fuelled for does not reach the cylinders. Under load, λ goes lean because fuel is delivered for air volume that leaked. At idle and part-throttle (vacuum operation), the leak admits unmetered air (lean) or the leak is less significant (low boost).

**Key discriminator:** At WOT, λ > 1.00 with MAP below target → boost leak. Compare with fuel delivery fault: MAP near target but λ > 1.00 → fuel pump/injector issue, not boost leak. Compare with MAF under-reading: MAP near target, λ > 1.00, but MAF (g/s) below expected for RPM/MAP combination.

**DTCs:** P0299 (underboost)

**Splitter table — boost leak vs vacuum leak:**

| Signal | Boost leak (WOT) | Vacuum leak (idle/cruise) |
|--------|------------------|--------------------------|
| MAP | Low for load/RPM | Normal |
| λ at WOT | Lean (> 1.00) | Normal (closed-loop corrects at cruise) |
| λ at idle | May be lean (leak admits unmetered air) | Lean |
| Fuel trim at idle | May be positive | Positive |
| Sound | Hissing under boost | Hissing, more prominent at idle |

### 5.3 Overboost (wastegate / VNT control failure)

| HC | CO | CO₂ | O₂ | λ | MAP | boost_ratio |
|----|-----|------|-----|-----|-----|------------|
| Normal | Normal | Normal | Normal | ≈1.00 (ECU fuelling follows MAF) | Above target | Above target by ≥ 20 % |

**Physical mechanism:** Wastegate actuator diaphragm ruptures, boost control solenoid sticks closed, or VNT vanes are stuck in the closed (max boost) position. Exhaust energy cannot bypass the turbine, so the compressor overspeeds → excessive boost. The ECU may initiate overboost fuel cut (sudden λ spike to lean) or throttle closure. Prolonged overboost can cause detonation, lifted cylinder heads, or turbo mechanical failure.

**DTCs:** P0234 (overboost), P0235–P0238 (boost sensor circuit), P0243–P0246 (wastegate solenoid)

### 5.4 Turbo mechanical degradation (worn bearings / oil seal leak)

| HC | CO | CO₂ | O₂ | λ | MAP | boost_ratio |
|----|-----|------|-----|-----|-----|------------|
| **May spike (oil burning)** | Normal | Normal | Normal | Normal | May be slow to build | Below target transiently (slow spool) |

**Physical mechanism:** Journal bearing wear allows the shaft to orbit, reducing compressor and turbine efficiency. Oil seals fail, admitting engine oil into the compressor outlet or turbine inlet — oil burning produces visible blue smoke and elevated HC. The turbo spools progressively slower as bearing clearance increases. A failing turbo often produces a distinctive whistle or siren sound at boost onset.

**DTCs:** P0299 (underboost — from slow spool response), P0234 (overboost — if worn actuator/wastegate prevents proper regulation)

### 5.5 Charge air cooler (intercooler) degradation

| HC | CO | CO₂ | O₂ | λ | IAT | boost_ratio |
|----|-----|------|-----|-----|-----|------------|
| Normal | Normal | Normal | Normal | Normal but less power | Elevated | Normal |

**Physical mechanism:** A fouled (external — bugs, leaves, bent fins) or internally oil-saturated intercooler reduces heat transfer. IAT rises because compression heat is not rejected. The ECU sees elevated IAT → retards timing → power loss. No DTC may be set if IAT remains within expected range at the lower power level.

**Gas signature:** All gases normal; the deficit is mechanical (less power at a given MAP) rather than mixture-based. Performance degradation is the primary signal. IAT at compressor outlet − IAT at intake manifold < 50 °C or less than 70 % of the expected temperature drop.

---

## 6. DTC families — turbocharger

| DTC family | Description | Primary evidence | Source guide |
|------------|-------------|-----------------|-------------|
| P0234 | Turbocharger overboost condition | MAP > target by ≥ 20 %; wastegate/VNT control offline | `docs/master_guides/turbo/master_turbo_guide.md` §5.3 |
| P0235–P0238 | Turbocharger boost sensor circuit | MAP sensor electrical fault; use freeze-frame BARO to cross-check | `docs/master_guides/turbo/master_turbo_guide.md` §2 |
| P0243–P0246 | Turbocharger wastegate solenoid circuit | Solenoid electrical fault; mechanical overboost from stuck-closed wastegate | `docs/master_guides/turbo/master_turbo_guide.md` §3 |
| P0299 | Turbocharger underboost condition | MAP < target by ≥ 15 %; boost leak, wastegate stuck open, or turbo mechanical degradation | `docs/master_guides/turbo/master_turbo_guide.md` §5.2, §5.4 |
| P2262 | Turbocharger boost pressure not detected — mechanical | No boost pressure rise above BARO; severe boost leak, fully open wastegate, or seized turbo | `docs/master_guides/turbo/master_turbo_guide.md` §5.2 |

---

## 7. Forced induction — gas signatures for companion faults

Turbocharger faults rarely occur in isolation on older engines. The following companion fault signatures are often misattributed to the turbo:

| Symptom | Gas signature | Likely actual cause | Why it's mistaken for turbo |
|---------|--------------|---------------------|---------------------------|
| Low power + λ lean | O₂ elevated at WOT, CO low | Fuel pump weak at high demand | MAP is normal — the turbo is fine; the fuel system can't match the airflow |
| Low power + λ rich | CO elevated at WOT, O₂ low | MAF over-reading or boost leak downstream of MAF but upstream of O₂ sensor | MAP may be normal; the mixture is wrong, not the boost |
| Intermittent power loss at speed | All normal at idle and part-throttle | VVT phaser stuck or cam solenoid intermittent | Both affect breathing at mid-RPM; turbo MAP looks normal because the wastegate compensates |

The breathing-cluster formula (§2) distinguishes these: a turbo fault produces a breathing_cluster_score outside the expected boost_ratio range for the given RPM/MAP combination. A fuel delivery fault produces a normal breathing_cluster_score with an abnormal lambda deviation.

---

## 8. Turbo thresholds — provenance table

Every numeric threshold the 4D engine applies to turbocharger and forced-induction signals. All values are petrol-only, MY 1990–2020.

| Parameter | Value | Unit | Applies to | Physical basis | Source guide |
|-----------|-------|------|-----------|----------------|-------------|
| `boost_ratio_idle_max` | 1.10 | — | Idle | Turbo not spooled at idle; MAP ≈ BARO (±5 % sensor tolerance) | `docs/master_guides/turbo/master_turbo_guide.md` §2.2 |
| `boost_leak_deviation` | −15 | % | WOT or part-throttle boost | Below 15 % of target boost_ratio → metered air not reaching cylinders | `docs/master_guides/turbo/master_turbo_guide.md` §5.2 |
| `overboost_deviation` | +20 | % | Any condition | Above 20 % of target → wastegate/VNT not regulating; ECU overboost fuel cut imminent | `docs/master_guides/turbo/master_turbo_guide.md` §5.3 |
| `intercooler_efficiency_min` | 70 | % | Under boost | ΔT across intercooler ÷ (T_compressor_outlet − T_ambient) ≥ 0.70 | `docs/master_guides/turbo/master_turbo_guide.md` §5.5 |
| `turbo_spool_time_max` | 2.5 | s | From closed-throttle idle to target boost at WOT snap | Wheel inertia + exhaust enthalpy; > 2.5 s → bearing drag or exhaust restriction pre-turbine | `docs/master_guides/turbo/master_turbo_guide.md` §5.4 |
| `turbo_noise_freq_range` | 2–8 | kHz | Audible whine at turbocharger | Compressor blade-pass frequency; bearing whistle shifts with RPM | `docs/master_guides/turbo/master_turbo_guide.md` §5.4 |
| `wastegate_base_spring_pressure` | 0.35–0.50 | bar (gauge) | Mechanical wastegate | Wastegate spring determines minimum boost before ECU can modulate | `docs/master_guides/turbo/master_turbo_guide.md` §3 |
| `iat_max_under_boost` | 80 | °C | Post-intercooler, under sustained boost | Above 80 °C IAT → timing retard → power loss; intercooler insufficient or ambient > 45 °C | `docs/master_guides/air_induction/master_air_induction_guide.md` |

---

## 9. Turbo — engine-state modifiers

Turbo behaviour changes fundamentally across engine states. The 4D engine must gate turbo symptoms on M0's `engine_state` output.

| Engine state | Turbo behaviour | Diagnostic meaning |
|-------------|----------------|-------------------|
| Cold start (ECT < 40 °C) | Turbo not producing meaningful boost; exhaust enthalpy low | Do not evaluate boost targets until warm |
| Warm idle | Turbo not spooled; MAP ≈ BARO (±5 %); wastegate may be open | boost_ratio should be 0.85–1.05 |
| Closed-loop cruise, light load | Turbo may be producing light boost or operating in vacuum depending on engine load | boost_ratio target is engine-specific; compare to era reference table (§4) |
| Open-loop WOT | Turbo at full boost; wastegate/VNT controlling to target | Target boost_ratio from era reference table (§4); deviation triggers underboost/overboost |
| Decel fuel cut (DFCO) | Turbo not producing boost; compressor may surge if blow-off/bypass valve not functioning | BOV/BPV function audible; surge flutter on lift-off |

---

## 10. Era-specific turbo considerations

**1990–1995 (Pre-OBD-II):** Basic wastegate, no electronic boost control on many engines. Boost is purely mechanical — no DTCs for underboost/overboost. Diagnosis relies entirely on gas analysis, mechanical inspection, and performance testing. The 4D engine's breathing cluster is the primary diagnostic tool for this era — there are no OBD PIDs to confirm a boost problem.

**1996–2005 (OBD-II, pre-CAN):** Electronic boost control becomes common. P0234/P0299 DTCs exist but thresholds are manufacturer-defined and inconsistent. MAP and BARO PIDs are available. Boost control is typically a simple duty-cycle solenoid; PID for wastegate duty cycle may or may not be present.

**2006–2015 (CAN-bus era):** Full ECU boost control with torque-target strategy. MAP, BARO, IAT, wastegate position (commanded and actual), and boost pressure sensor are standard PIDs on most engines. VNT appears on petrol. Boost control is integrated into the engine torque model — the ECU targets torque, and boost is one actuator among many (throttle, timing, fuel, cam position, boost).

**2016–2020 (modern OBD):** Cylinder-pressure modelling, electric wastegate actuators with position feedback, water-to-air intercooling on some engines. Boost system diagnostics are mature; underboost/overboost detection is reliable. The 4D engine's challenge in this era is not detecting a boost fault but attributing it to the correct cause among many interacting sub-systems (turbo, VVT, high-pressure fuel, ignition).

---

## 11. Petrol-only scope boundary (R12)

This guide covers spark-ignition petrol turbochargers only. Diesel turbocharger diagnosis differs fundamentally:
- Diesel engines operate with excess air at all times (no throttle, λ always lean)
- Diesel turbos run cooler (lower exhaust temperature) but at higher boost pressure (1.5–3.0+ bar)
- Diesel turbo faults manifest as black smoke (overfueling from boost loss) rather than lean-mixture symptoms
- Diesel VNT is mature and near-universal from the late 1990s; petrol VNT is rare until 2006+
- No diesel-specific turbo thresholds, DTCs, or diagnostic pathways appear in this guide or in the 4D engine.

---

## 12. Cross-references

| Domain | Guide | Why linked |
|--------|-------|-----------|
| Air induction | `docs/master_guides/air_induction/master_air_induction_guide.md` | Intake path shared with forced induction; IAT and MAF are in the breathing cluster formula |
| Mechanical | `docs/master_guides/mechanical/master_mechanical_guide.md` | VVT affects effective compression and breathing; cam timing interacts with boost onset |
| Ignition | `docs/master_guides/ignition/master_ignition_guide.md` | Timing retard under boost (knock control); overboost can cause detonation |
| Fuel system | `docs/master_guides/fuel_system/master_fuel_system_guide.md` | Fuel delivery must match boosted airflow; weak fuel pump mimics underboost |
| Fuel trim | `docs/master_guides/fuel_trim/master_fuel_trim_guide.md` | Boost leak shows as positive fuel trim at idle (unmetered air); fuel trims help distinguish boost leak from fuel fault |
| O₂ sensor | `docs/master_guides/o2_sensor/master_o2_sensor_guide.md` | Wideband O₂ under boost; sensor response during WOT enrichment |
| Freeze frame | `docs/master_guides/freeze_frame/master_freeze_frame_guide.md` | FF captures MAP, BARO, IAT, RPM, LOAD_PCT at DTC freeze — all breathing-cluster inputs |
