# Master O₂ / Wideband Sensor Guide — 4D Petrol Diagnostic Engine

**Purpose.** Define narrowband (zirconia) and wideband (UEGO/AFR) oxygen sensor physics, voltage and current ranges, switching behaviour, upstream-vs-downstream semantics, heater function, common DTC families, and the diagnostic patterns that distinguish a biased sensor from a real mixture fault. The engine uses this to validate the ECU's perceived lambda against the analyser's Brettschneider lambda.

**Scope.** Narrowband Bosch-style zirconia sensors (1980s–2000s) and wideband UEGO sensors (Bosch LSU 4.2 / 4.9, NTK / NGK universal, Denso) (2000s–present). Petrol only. Two-wire titania sensors (rare, mainly older Nissan) are not covered explicitly but obey the same upstream/downstream semantics.

---

## 1. Sensor types

| Feature | Narrowband (Zirconia, older) | Wideband (UEGO/AFR, modern) |
|---|---|---|
| Wires | 1–4 (signal, ground, +12V heater, heater ground) | 5–6 (signal, pump current, calibration resistor, reference, +12V heater, heater ground) |
| Output | 0–1 V switching voltage | Pump current proportional to λ; ECU reports λ or 0–5 V linear AFR |
| Range | Accurate only near λ = 1.0 (± 0.05) | Linear across λ 0.65–1.30+ |
| Stoichiometric value | ~0.45 V (450 mV) | Nernst cell held at 450 mV by pump cell; pump current ≈ 0 mA |
| Rich signal | ~0.8–0.9 V (low O₂) | Negative pump current (PCM pumps O₂ *into* sensor) |
| Lean signal | ~0.1–0.2 V (high O₂) | Positive pump current (PCM pumps O₂ *out* of sensor) |
| Use | Basic fuel trim, post-cat efficiency monitor | Precise AFR for fuel control + monitoring |

The 4D engine reads `o2_upstream_classification` (narrowband / wideband) from the v5 corpus row to choose the correct interpretation rules.

---

## 2. Narrowband voltage semantics

A zirconia O₂ sensor generates voltage by comparing exhaust O₂ to ambient air through its solid electrolyte. Below 0.45 V means lean of stoichiometric; above 0.45 V means rich.

**Healthy upstream (pre-cat) behaviour:**
- Switches rapidly (~1–2 Hz at idle) between ~0.1 V and ~0.9 V.
- Crosses 0.45 V cleanly each cycle.
- Cross-counts ≥ 8 in a 10-second sample at 2500 RPM.
- Switching frequency at 2500 RPM: **2–5 Hz for multi-port fuel injection; 2–3 Hz for throttle-body injection (TBI)**. A sensor reading < 0.5 Hz at 2500 RPM is slow regardless of voltage amplitude — static voltage tests alone cannot detect this.

**Failure patterns:**

| Condition | Voltage behaviour | Cause | Resulting fuel trim |
|---|---|---|---|
| **Stuck lean (bias low)** | Stays < 0.1 V | Exhaust leak before sensor; sensor poisoned; signal short-to-ground | Positive (ECU adds fuel chasing the false-lean signal) |
| **Stuck rich (bias high)** | Stays > 0.8 V | Silicone contamination (RTV sealant nearby); signal short-to-voltage; sensor end-of-life | Negative (ECU subtracts fuel) |
| **Sluggish / lazy** | Cross-counts < 8 in 10 s @ 2500 RPM; frequency < 0.5 Hz at 2500 RPM; rise/fall time > 100 ms; propane-enrichment response delay > 100 ms | Age, lead/silicone/phosphorus contamination, carbon deposits, faulty heater | Trims trail; misfire-feel under transient. **Note: sensor may pass a static voltage check and still be slow — always test frequency and propane response** |
| **Dead** | Voltage flat-lined at 0.45 V (bias voltage only) | Open heater circuit; broken signal wire; sensor cracked | None (ECU drops to open loop, sets P0134 or similar) |
| **Switching at wrong centreline** | Switches between, say, 0.3 V and 0.6 V instead of 0.1–0.9 V | Sensor near end of life, partial poisoning | Trims slightly off centre; cross-counts may still pass |

**Healthy downstream (post-cat) behaviour:** Stable, slow-moving signal around 0.5–0.7 V with very few cross-counts. The catalyst has damped the upstream switching.

**Degraded downstream:** When S2 begins to mirror S1 switching activity, the catalyst has lost oxygen storage capacity → triggers P0420 (B1) / P0430 (B2). This is the catalyst monitor's principal evidence — see `master_catalyst_guide.md §3`.

---

## 3. Wideband (UEGO/AFR) semantics

Wideband sensors use a dual-cell architecture: a Nernst sensing cell maintained at exactly 450 mV by a pump cell. The ECU varies pump current (Ip) — typically −2 mA to +2 mA — to keep the Nernst cell at setpoint. That pump current is the diagnostic parameter.

| Mixture | Pump current Ip | ECU-reported λ | What the sensor is doing |
|---|---|---|---|
| λ = 1.0 (stoich) | ~0 mA | 1.000 | No oxygen transfer needed |
| Rich (λ < 1.0) | Negative | < 1.000 | Pumping O₂ *into* the sensor chamber |
| Lean (λ > 1.0) | Positive | > 1.000 | Pumping O₂ *out* of the sensor chamber |
| WOT power | −0.5 to −1.5 mA | 0.85–0.92 | ECU has commanded power enrichment |
| DFCO | +1.5 to +2.0 mA | 1.30+ | Fuel cut, mostly air |

The 4D engine must read the **reported λ PID** (`obd_lambda` column in the v5 corpus), not raw voltage. Raw voltage from a wideband is meaningless without the calibration resistor value.

**Wideband failure modes:**

- **Heater out of spec:** Sensor stays cold, ECU runs open loop. Sets P0030 / P0036 / P0050 / P0056 family.
- **Calibration resistor failure:** Sensor reports λ off by a fixed offset across all conditions. The 4D engine should suspect this when the analyser's λ disagrees with `obd_lambda` by a constant offset across multiple measurements.
- **Reference voltage drift:** Some ECUs feed a 2.5 V reference to the sensor. Drift causes proportional λ error.

---

## 4. Upstream vs downstream — different roles, different rules

| Position | Naming | Role | Expected behaviour | Drives |
|---|---|---|---|---|
| **Sensor 1, B1** | Pre-cat, Bank 1 (B1S1) | Fuel control feedback | Rapid switching (NB) or live λ (WB) | STFT/LTFT |
| **Sensor 2, B1** | Post-cat, Bank 1 (B1S2) | Catalyst efficiency monitor | Slow, mostly stable around 0.5–0.7 V | P0420 monitor only — does not drive fuel control on most ECUs |
| **Sensor 1, B2** | Pre-cat, Bank 2 | Same as B1S1 for Bank 2 | Same | STFT_b2 / LTFT_b2 |
| **Sensor 2, B2** | Post-cat, Bank 2 | Same as B1S2 for Bank 2 | Same | P0430 monitor only |

**Rule:** A failing post-cat sensor does not affect fuel trim. If the user sees fuel-trim drift and only a P0136/P0156 (rear sensor) DTC, the rear sensor fault is *not* the cause of the trim drift — keep looking.

---

## 5. Heater circuits

O₂ sensors require ≥ ~350 °C to function. Built-in heaters bring them online within 20–60 seconds of cold start, enabling earlier closed-loop entry.

| Parameter | Spec | Notes |
|---|---|---|
| Heater current | 0.5–2.0 A typical (older NB), up to 8 A (some WB) | Reduce to 0 A momentarily during sample of resistance |
| Heater resistance (cold) | 4–14 Ω narrowband; 2.5–10 Ω wideband | Varies by sensor; low resistance = pulled-up heater wire |
| Time to closed loop | 20–60 s post cold start | If never reaches CL, suspect heater open or sensor cold-stuck |

**Common heater DTCs:** P0030 (B1S1), P0050 (B2S1), P0036 (B1S2), P0056 (B2S2), and the family P0135 / P0141 / P0155 / P0161 for the older "Heater Performance" variants.

---

## 6. Sensor bias vs real mixture — the diagnostic rule

This is the single most important rule in this guide. When the O₂ sensor reports rich but tailpipe gases / Brettschneider λ are lean (or vice versa), the engine must differentiate:

| Sensor reading | Tailpipe gases / Brettschneider λ | Verdict |
|---|---|---|
| Lean | Rich or normal | **Sensor stuck low** — exhaust leak before sensor, O₂ silicone poisoning, circuit fault. Surface `Exhaust_Air_Leak_Pre_Cat` or `O2_Sensor_Bias_Lean`. ECU is feeding fuel into a fine engine. |
| Rich | Lean or normal | **Sensor stuck high** — silicone poisoning (most common), short-to-voltage, end-of-life sensor. Surface `O2_Sensor_Bias_Rich`. ECU is starving a fine engine. |
| Lean | Lean (gas λ ≥ 1.05) | **Real lean condition** — vacuum leak, low fuel pressure, MAF under-reading. Surface lean candidates per `master_fuel_trim_guide.md §4`. |
| Rich | Rich (gas λ ≤ 0.95) | **Real rich condition** — high fuel pressure, leaking injector, EVAP purge stuck open. Surface rich candidates per `master_fuel_trim_guide.md §4`. |

The Truth-vs-Perception override (`master_gas_guide.md §3 rule 7`): when in doubt, gas chemistry wins. Subject to one caveat: a 5 % exhaust air leak shifts the analyser λ 0.05 lean (`master_gas_guide.md §8.5`). Rule out exhaust leak before declaring sensor bias.

---

## 7. Common DTC families

| Code | Definition | Bank/Sensor | Common cause |
|---|---|---|---|
| P0130 | O₂ Circuit Malfunction | B1 S1 | Wiring, connector, sensor end-of-life |
| P0131 | O₂ Circuit Low Voltage | B1 S1 | Stuck lean — exhaust leak, short-to-ground |
| P0132 | O₂ Circuit High Voltage | B1 S1 | Stuck rich — silicone, short-to-voltage |
| P0133 | Slow Response | B1 S1 | Lazy / aged sensor |
| P0134 | No Activity Detected | B1 S1 | Open circuit, dead sensor, never reaches operating temp |
| P0135 | Heater Circuit | B1 S1 | Heater fuse, heater open, heater short |
| P0136–P0141 | (same family) | B1 S2 | Post-cat — affects only catalyst monitor |
| P0150–P0161 | (same family) | B2 S1/S2 | Bank 2 mirror of P0130–P0141 |
| P0030 / P0036 / P0050 / P0056 | Heater Control Circuit | B1S1 / B1S2 / B2S1 / B2S2 | Newer codes; same physical fault as P0135/P0141/P0155/P0161 |
| P2A00–P2A03 | A/F sensor circuit (wideband) | by bank/sensor | Wideband-specific equivalents of P013x |

---

## 8. Cross-checks the engine must perform

- **Sensor ↔ analyser λ delta:** if `|obd_lambda − lambda_analyser|` ≥ 0.08 and gases are otherwise consistent, surface `perception_contradiction` and consult `master_gas_guide.md §3 rule 7`.
- **Pre-cat ↔ post-cat switching ratio:** if rear sensor cross-count ≥ 0.5 × front, suspect catalyst (`master_catalyst_guide.md §3`), not the rear sensor.
- **Both banks rich, but only B1 O₂ shows rich voltage:** suspect B2 sensor stuck low (false-lean), feeding bank-mismatched fuel control. Cross-ref `master_fuel_trim_guide.md §5`.
- **Sensor reports λ but trims are zero:** ECU may be in open loop. Check `fuel_sys_status` PID. Open-loop trims are invalid (`master_cold_start_guide.md §1`).

---

## 9. Citations

- Bosch Technical Information — LSU 4.2 / 4.9 wideband sensor datasheet (pump-current calibration).
- SAE J1939 / J1979 PID definitions — `$14`–`$1B` (O₂ sensor voltages), `$24`–`$2B` (wideband sensor data).
- `cases/library/automotive/mix/extracted/Lambda sensors _ exhaust oxygen sensors.md` — narrowband/wideband side-by-side reference.
- `cases/library/automotive/mix/extracted/Air Fuel A_F Ratio Basics _ Wideband vs Narrow O2 sensor.md` — practical voltage/current ranges.
- `cases/library/automotive/mix/Oxygen Sensor Codes - A Complete Guide On Diagnosing Automotive Oxygen Sensors.pdf` — failure-mode tree.
- `cases/library/automotive/mix/oxygen-sensor-codes-guide.md` — extracted summary.
- Cross-ref: `master_obd_guide.md §5.5` (P013x family); `master_gas_guide.md §3 rule 7` (truth-vs-perception override).
