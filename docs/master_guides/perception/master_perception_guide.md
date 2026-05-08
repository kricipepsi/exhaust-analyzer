# Master Perception Gap Guide — 4D Petrol Diagnostic Engine

**Purpose.** A single, self-contained reference for the Truth-vs-Perception architecture of the 4D engine — the diagnostic space between what the ECU "believes" about the engine's mixture state (based on its sensors) and what is physically true at the tailpipe (based on the Brettschneider lambda from the 5-gas analyser). This guide defines every perception-gap mechanism, its physical basis, the trigger conditions in `engine/perception.py`, the KG nodes (`perception_lean_seen_rich`, `perception_rich_seen_lean`) and their edge wiring, the `expected_perception_gap` CSV flag semantics, and all boundary values with physical justification. The 4D engine's foundational rule is stated here: **chemistry is ground truth.**

---

## 1. The two truths

The 4D engine operates on a duality that is architecturally central:

**ECU truth (perception):** What the ECU measures via its sensors and reports via DTCs, fuel trims, and OBD PIDs.

**Chemistry truth (ground):** What the exhaust actually contains, measured by the 5-gas analyser at the tailpipe, expressed as Brettschneider lambda (λ).

When these two truths agree, the fault is a conventional mechanical, fuel, or ignition problem. When they disagree — when there is a **perception gap** — the diagnostic challenge is to determine which truth is corrupted and why.

**The foundational rule:** Chemistry is ground truth. When the analyser and the ECU disagree *and the analyser reading has been validated* (no sample leak, no probe-out, no calibration error), the Brettschneider λ takes precedence over the ECU's sensor output. The ECU is perception; the analyser is reality.

---

## 2. Perception gap mechanisms — the four physical causes

Every perception gap reduces to one of four physical mechanisms.

#### 2.1 Exhaust air leak before upstream O₂ sensor

**Physics:** Ambient air (20.9 % O₂) enters the exhaust stream between the cylinder head and the upstream O₂ sensor — typically through a cracked exhaust manifold, failed manifold gasket, or a loose oxygen sensor bung. The sensor sees elevated oxygen and reports "lean." The ECU adds fuel. The actual combustion is normal or rich, but the sensor is sampling oxygen-contaminated exhaust gas.

**Perception:** ECU thinks lean → positive fuel trim; may set P0171/P0174
**Reality (tailpipe):** λ ≤ 1.00 — stoich or rich; CO may be elevated from ECU enrichment
**Gas signature:** O₂ at tailpipe is normal or low (the leak is between head and sensor, upstream of the analyser probe); CO elevated from added fuel
**Key diagnostic evidence:** Visual inspection of exhaust manifold and gaskets; at idle, spraying a small amount of brake cleaner near suspect joints causes STFT to spike momentarily as the introduced combustibles displace the air leak

The leak is **downstream of combustion but upstream of the sensor** — it admits ambient air into already-burned gas. The tailpipe analyser, positioned further downstream (usually after the catalyst), may see the real combustion products if the leak is between the sensor and the cat.

#### 2.2 O₂ sensor contamination or voltage bias

**Physics:** The upstream O₂ sensor's output is chemically shifted. Silicone poisoning (from RTV sealants, silicone-containing coolant, silicone-based lubricants) coats the sensor's zirconia element with silica, causing it to read falsely rich (high voltage). Oil ash and lead deposits can cause false-lean readings. Phosphate/silicate coolant contamination degrades sensor switching speed (lazy sensor — see `master_o2_sensor_guide.md §6`).

**Perception (biased lean):** Sensor reads lean → ECU adds fuel (positive trim)
**Perception (biased rich):** Sensor reads rich → ECU subtracts fuel (negative trim)
**Reality:** Tailpipe λ contradicts the sensor's reading direction
**Progressive nature:** A sensor that was healthy 10,000 km ago can slowly drift. Many biased sensors never set a DTC — they operate within the ECU's ±25 % trim authority while producing wrong fuel delivery.

#### 2.3 MAF sensor reading error (under-reading or over-reading)

**Physics:** A contaminated hot-wire MAF sensor under-reads at low airflow (oil film insulates the sensing wire) or over-reads at high airflow (turbulence from contamination alters the velocity profile). The ECU calculates injector pulse width from the MAF reading — if the MAF is wrong, the entire fuel calculation is wrong.

**MAF under-reading:** ECU thinks less air → injects less fuel → actual mixture runs lean. Positive fuel trims at idle, often worsening at cruise or improving (complex RPM dependency). Cross-ref `master_air_induction_guide.md §3`.
**MAF over-reading:** ECU thinks more air → injects more fuel → actual mixture runs rich. Negative trims; the engine is rich but ECU believes it is compensating correctly.

The characteristic MAF diagnostic fingerprint is a **trim reversal between idle and cruise**: a contaminated MAF that under-reads at low airflow produces positive trim at idle but may produce negative trim at 2500+ RPM where the contamination effect reverses.

#### 2.4 Misfire-induced O₂ sensor misinterpretation

**Physics:** During a severe ignition or mechanical misfire, both raw fuel (HC) and raw oxygen (O₂) exit the combustion chamber together. The narrowband O₂ sensor works via catalytic reaction on its ceramic surface — it converts combustibles in the presence of oxygen to produce voltage. If massive quantities of *both* HC and O₂ are present simultaneously, the catalytic reaction cannot complete, and the sensor may produce no voltage. The ECU interprets "no voltage" as lean and enriches further, worsening the misfire.

**Perception:** ECU sees "lean" (no voltage) → adds fuel → worsens misfire
**Reality:** HC very high (>800 ppm), O₂ high (>5 %), λ ≈ 1.00 (mixture is balanced — both HC and O₂ exit in proportion)
**Critical rule:** This is **not** an O₂ sensor fault. The sensor is responding correctly to an incomplete combustion environment. The 4D engine must route HC > 800 ppm + O₂ high + λ ≈ 1.00 to `Ignition_Misfire` or `Mechanical_Misfire`, not to `ECU_Logic_Inversion`. Cross-ref `master_ignition_guide.md §6`.

---

## 3. The two perception-gap conditions currently implemented in `perception.py`

The `perception.py` module covers two specific DTC+gas combinations. Each has a physical basis documented here.

#### 3.1 Rich gas (λ < 0.905) + lean DTC (P0171 or P0174) → `perception_lean_seen_rich`

**DTC says:** "System too lean" — ECU is adding fuel (positive trim).
**Gases show:** Rich — λ < 0.905, CO elevated (> 1.5 %), O₂ low.
**Perception gap:** The ECU is adding fuel to correct a perceived lean condition, but the engine is already severely rich. The upstream O₂ sensor is lying to the ECU.

**Physical verdict:** The O₂ sensor has failed lean (bias producing low or no voltage despite rich exhaust) OR there is a large exhaust air leak before the sensor (ambient O₂ entering the exhaust stream). The air leak is pulling in enough ambient oxygen to fool the sensor into reading lean despite the rich combustion.

**4D engine action:** Surface `perception_lean_seen_rich`; suppress normal lean-mixture candidates (`lean_condition`, `vacuum_leak`, `low_fuel_delivery`). Recommend: inspect exhaust manifold for leaks upstream of the O₂ sensor; if exhaust is intact, replace upstream O₂ sensor.

**Why λ < 0.905 (not 0.95):** See `master_ecu_guide.md §3.2` for the full physical justification. At λ 0.905–0.95 (moderate rich), a sufficiently large exhaust air leak could plausibly shift the sensor perception to lean. At λ < 0.905, the enrichment is severe enough (≈9.5 % excess fuel) that no plausible exhaust air leak can explain a simultaneous lean perception without the sensor having failed. The 0.905 threshold represents the physical point of impossible coincidence — below this, inversion is definitive.

#### 3.2 Lean gas (λ > 1.095) + rich DTC (P0172 or P0175) → `perception_rich_seen_lean`

**DTC says:** "System too rich" — ECU is subtracting fuel (negative trim).
**Gases show:** Lean — λ > 1.095, CO low, O₂ elevated (> 2.0 %).
**Perception gap:** The ECU is subtracting fuel to correct a perceived rich condition, but the engine is actually lean.

**Physical verdict:** The O₂ sensor is contaminated with silicone or another substance that produces false-rich voltage despite lean exhaust, OR the MAF sensor is grossly over-reading (causing the ECU to inject excess fuel, which it then "sees" as rich even though the actual enrichment is being undone by a lean-pulling condition).

**4D engine action:** Surface `perception_rich_seen_lean`; suppress normal rich-mixture candidates (`rich_mixture`, `leaking_injector`, `high_fuel_pressure`). Recommend: inspect O₂ sensor for silicone contamination (white/glassy coating); check MAF reading against expected g/s at idle.

**Why λ > 1.095 (symmetric threshold):** The same physical reasoning applies in the opposite direction. At λ > 1.095, the lean condition is severe enough that no O₂ sensor contamination producing false-rich voltage can be explained without the sensor being significantly compromised.

---

## 4. Perception gap mechanisms not yet covered — future implementation guidance

The current `perception.py` covers only the λ/DTC contradiction combos for P0171/P0174 and P0172/P0175. Additional perception-gap mechanisms documented here for future coder implementation:

#### 4.1 Moderate gap (0.905 ≤ λ < 0.95 rich, with P0171)

When the ECU has large positive fuel trims (+15 to +25 %) and tailpipe λ is 0.92–0.95 (mildly rich):
- Small exhaust leak admitting 3–5 % ambient air
- MAF under-reading at idle but over-reading at cruise
- Ageing O₂ sensor with slightly shifted switching voltage

This "moderate gap" zone should be flagged as a warning (`sensor_bias_lean` or `Lazy_O2_Sensor_Aging`) but should **not** trigger full `perception_lean_seen_rich` unless λ drops below 0.905.

#### 4.2 Lambda mismatch between analyser and OBD-reported λ PID

When the 5-gas analyser calculates λ via Brettschneider and the OBD PID (`obd_lambda`) reports a different λ from the ECU's wideband sensor:

| Delta |λ_analyser − λ_OBD| | Interpretation |
|-------|--------------------------|----------------|
| **< 0.05** | Sensors agree — normal sensor variation | No gap |
| **0.05–0.08** | Mild discrepancy — ageing sensor tolerance | Monitor; not yet actionable |
| **> 0.08** | Significant gap | Possible O₂ sensor drift, exhaust air leak, or analyser calibration error |

Threshold: `sensor_bias.delta_hot = 0.08` in `schema/thresholds.yaml`. Above this delta, the engine considers the OBD lambda unreliable.

#### 4.3 Misfire DTC (P0300–P0308) with contradictory fuel trim

A P0300 random misfire with fuel trims at +20 % could be either:
- **Lean misfire** (real lean condition causing misfire): O₂ very high (> 4 %), HC moderate (200–600 ppm)
- **Ignition misfire with ECU lean misread** (perception gap): HC very high (> 800 ppm), O₂ high, λ ≈ 1.00

The splitter: if HC > 800 ppm with O₂ high, it is an ignition misfire with ECU lean misread — not a lean condition. Route to `Ignition_Misfire`. If O₂ very high with HC moderate, it is a genuine lean misfire — route to `lean_condition` with `misfire` as a downstream effect.

#### 4.4 False-catalyst perception (P0420 with clean idle gases)

When P0420 sets but idle gases are clean (λ near 1.00, HC < 50 ppm, CO < 0.5 %), the catalyst efficiency monitor may have failed during a specific load/speed condition that is not reproducible at idle. This is not a perception gap per se — the cat efficiency test runs under driving conditions the idle test cannot replicate. Demote catalyst-failure and surface `dtc_set_outside_enable_window`. Cross-ref `master_catalyst_guide.md §6`.

---

## 5. Expanded perception-gap decision table

| ECU signal | Tailpipe λ | Gap direction | Diagnostic call |
|------------|-----------|---------------|----------------|
| P0171/P0174 + positive trim | λ < 0.905, CO > 1.5 % | **Definitive gap** | O₂ sensor bias low or exhaust air leak → `perception_lean_seen_rich` |
| P0172/P0175 + negative trim | λ > 1.095, O₂ > 2.0 % | **Definitive gap** | O₂ sensor contamination or MAF over-read → `perception_rich_seen_lean` |
| P0171 + LTFT +20 % | λ 1.00–1.05 (slight lean) | **Consistent — no gap** | Real lean condition → vacuum leak, fuel delivery, MAF under-read |
| P0172 + LTFT −20 % | λ 0.97–1.00 (slight rich) | **Consistent — no gap** | Real rich → fuel pressure, leaking injector, EVAP purge |
| LTFT +15 to +25 %, no DTC | λ 0.92–0.95 (mild rich) | **Moderate gap** | Flag as warning; small exhaust leak or ageing O₂ sensor |
| P0300 + STFT +20 % swinging | HC > 800, λ ≈ 1.00 | **Misfire misread** | Not an O₂ fault; route to ignition misfire |
| P0420 + clean idle gases | — | **Not a gap** | Cat test failed under load; test under load conditions |
| High CO + lean λ on analyser | λ > 1.05 on analyser | **Analyser sample leak** | Validate analyser first per §6 |

---

## 6. Perception gap validation protocol — analyser-first rule

Before concluding a perception gap, validate the analyser reading. A probe sample leak or uncalibrated analyser will produce a false-lean reading that masquerades as a perception gap.

**Analyser validation checklist:**
1. O₂ reading at ambient air (probe out) should be ≈ 20.9 %. If it reads < 20 % or > 21.2 %, the analyser has a calibration error.
2. CO₂ reading at ambient air should be ≈ 0.04 %. If CO₂ > 1 % with probe out, the probe is picking up exhaust.
3. If probe is inserted but O₂ > 20 %, there is a sample leak at the probe connection or the probe tube.
4. `validate_input()` in the engine's `validators.py` runs the INVALID_Probe_In_Open_Air_Sentinel check automatically — any O₂ > 20.2 % with CO₂ < 1 % triggers a sentinel finding.

**The foundational rule restated:** The analyser is ground truth — but *only after validation*. A validated analyser reading overrides ECU output. An unvalidated analyser reading must not be used to declare a perception gap.

---

## 7. The perception gap and the `expected_perception_gap` CSV column

In `cases_petrol_master_v5.csv`, the `expected_perception_gap` boolean column marks cases where the ground-truth reasoning contains a definitive contradiction between the ECU's reported signal and the gas chemistry. Rules:

- **`true`:** The case contains a DTC/gas chemistry contradiction where the 4D engine should explicitly recognise the ECU perception gap and route accordingly. Currently: P0171 + λ < 0.905 with CO > 1.5 % and OBD_λ > 1.05, or P0172 + λ > 1.095 with O₂ > 2.0 % and OBD_λ < 0.95.
- **`false`:** The case has consistent ECU and gas chemistry — no perception gap.
- **Empty/unlabelled:** The case does not have sufficient OBD lambda data to evaluate a gap.

Any case with `expected_perception_gap = true` where the engine does **not** return a perception-gap node in its top candidates is a MISS of the highest severity. These cases are the primary validation target for the `perception.py` module.

---

## 8. Routing rules for the 4D engine

1. **Always validate the analyser first** (§6). A sample leak is the most common false-perception-gap trigger.
2. **Require DTC + gas contradiction, not just gas anomaly.** The perception gap is defined by *disagreement* between what the ECU reports and what the gases show. A gas anomaly without a related DTC is a fuel/ignition/mechanical fault, not a perception gap.
3. **λ threshold semantics:** `< 0.905` for definitive rich perception; `> 1.095` for definitive lean perception. Within these bounds, apply `sensor_bias_*` nodes, not perception inversion nodes.
4. **Perception gap in either direction → upstream O₂ sensor is the primary suspect.** The upstream O₂ sensor is the single most likely component to produce a mixture-perception contradiction. Always test the sensor before replacing the ECU.
5. **Suppress competing candidates when inversion is definitive.** When `perception_lean_seen_rich` fires, suppress `lean_condition`, `vacuum_leak`, `contaminated_maf`, `low_fuel_delivery`. When `perception_rich_seen_lean` fires, suppress `rich_mixture`, `leaking_injector`, `high_fuel_pressure`.
6. **Do not fire perception nodes during cold start.** The O₂ sensor is not yet at operating temperature. Any DTC set during open-loop startup reflects cold-start conditions, not a steady-state perception gap. Gate on ECT ≥ 70 °C (freeze frame ECT if available) per `master_cold_start_guide.md §3`.

---

## 9. Cross-references

- `master_ecu_guide.md §3.2` — physical justification for the λ < 0.905 inversion threshold
- `master_o2_sensor_guide.md §6` — sensor bias rule; boundary between bias and inversion
- `master_gas_guide.md §3 rule 4` — CO high + negative trim = real rich, not perceived lean
- `master_ignition_guide.md §6` — misfire gas signature (HC very high + O₂ high + λ ≈ 1.00); route away from perception gap
- `master_cold_start_guide.md §3` — suppress perception evaluation during open-loop cold start
- `master_catalyst_guide.md §6` — false-catalyst P0420 perception (§4.4 above)
- `master_air_induction_guide.md §3` — MAF contamination pattern (under-reading/over-reading RPM dependency)
- `master_fuel_trim_guide.md §7` — trim direction vs gas chemistry cross-check (the complement rule to perception gap)

---

## 10. Citations

- SAE J1979 — OBD-II PID and DTC standard; Mode $01 lambda sensor PID
- Haltech Knowledge Base: Narrowband vs Wideband O₂ sensor signal behaviour (silicon poisoning, bias mechanisms)
- MOTOR Information Systems: "5-Gas Analysis" — MAF double-gap pattern, EGR perception-gap traps
- AVI OnDemand: "Fuel Trim Diagnosis and O2 Sensor Performance" — LTFT-vs-gas discordance interpretation
- Automotive Test Solutions: "Advanced Diagnostics Using the Five Gas Analyzer" — Brettschneider lambda as ground truth
- Phearable.net: Wideband O₂ sensor contamination modes
- DSX Tuning: Fuel Pressure Explained — rich-side perception mechanisms
- OBD-II PIDs — Wikipedia, accessed 2026-05-03
