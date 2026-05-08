# Master Ignition / Misfire Guide — 4D Petrol Diagnostic Engine

**Purpose.** Define ignition system architectures (distributor, wasted-spark, COP), misfire detection physics (CKP tooth-period variation), ignition coil diagnostics, spark plug reading, secondary ignition waveform interpretation (firing line, burn time, coil oscillations), and the gas signatures that separate ignition misfire from fuel misfire from mechanical misfire.

**Scope.** Petrol 1990–2020. Distributors (pre-2000), wasted-spark DIS (1990s–2000s), coil-on-plug (2000s–present), coil-near-plug variants. CDI (capacitive discharge) systems on Saab and some BMWs touched briefly. Diesel glow-plug ignition out of scope.

---

## 1. Misfire detection — how the ECU knows

Modern ECUs detect misfire by measuring crankshaft acceleration variations between cylinder firing events. A 60-tooth (60-2) CKP sensor wheel provides angular resolution fine enough to detect the momentary deceleration when a cylinder fails to fire. The CMP sensor identifies which cylinder is on its compression stroke, enabling cylinder-specific identification.

A misfire DTC requires the misfire count to exceed a calibrated percentage of firing events over a monitoring window:

- **Type A — catalyst-damaging misfire.** Detected within 200 engine revolutions. **MIL flashes** during active misfire. Typical threshold: 2–4 % misfire rate. Sets P0300 (random) or P0301–P0312 (specific cylinder).
- **Type B — emissions-relevant misfire.** Detected within 1000 engine revolutions. MIL steady on (after second consecutive trip). Typical threshold: 0.5–1 % misfire rate.

The 4D engine should surface `catalyst_damage_imminent` when the user reports flashing MIL plus an active P030x — driving with catalyst-damaging misfire melts the cat in minutes to hours.

**Cylinder-specific misfire DTCs:** the digit after `P030` is the cylinder number (P0301 = cyl 1, P0302 = cyl 2, … P0308 = cyl 8). On 10/12-cylinder vehicles, P0309–P030C extend the range.

---

## 2. Ignition system architectures (petrol, 1990–2020)

| Type | Era | Description | Key diagnostic |
|---|---|---|---|
| **Distributor + single coil** | Pre-2000 | One coil fires all cylinders via mechanical rotor/cap | Worn cap/rotor/HT leads cause crossfire and random misfire; check rotor air gap and cap centre electrode |
| **Wasted spark (DIS)** | 1990s–2000s | One coil per cylinder pair; both plugs fire simultaneously each rotation | Secondary resistance check per coil pair; one cylinder fires under compression, other on exhaust stroke |
| **Coil-on-plug (COP)** | 2000s–present | One coil per cylinder, mounted directly on plug, no HT lead | Individual coil swap test (move suspect coil to a different cylinder; if misfire follows, coil is the fault); per-coil DTCs P0351–P0358 |
| **Coil-near-plug (CNP)** | Some applications | Coil mounted near plug with very short HT lead | Similar to COP diagnostics |
| **CDI (capacitive discharge)** | Saab, some BMW | High voltage stored in capacitor, discharged via SCR | Different waveform (faster rise, shorter burn); waveform reference is per-application |

---

## 3. Ignition coil diagnostics

| Parameter | Specification | Notes |
|---|---|---|
| Primary resistance | 0.3–1.0 Ω typical | Varies by manufacturer; cold engine; 4-wire ohm-meter required |
| Secondary resistance | 5,000–15,000 Ω typical | > 20 kΩ indicates open or degraded winding |
| Spark output voltage at plug | ≥ 25,000 V at cranking | Below 25 kV with normal cylinder pressure → weak coil or low primary supply |
| Primary voltage drop | < 0.5 V | Voltage-drop test from ignition supply to coil primary terminal |
| Coil saturation time (dwell) | 2–5 ms typical | Too-short dwell starves the coil of current; too-long can overheat the driver |

A slight resistance on any ignition control circuit can cause a misfire **before** a DTC (P0351–P0354) is set — primary-current monitoring on modern ECUs is sensitive but not perfect.

---

## 4. Spark plug reading — physical witness to combustion

Spark plugs are the primary physical witness to combustion conditions. Read them alongside gas analysis.

| Plug appearance | Indicates | Gas correlate |
|---|---|---|
| **Normal** — light brown / tan | Correct heat range, good combustion, healthy mixture | Normal gases (`master_gas_guide.md §8.6` with-cat reference values) |
| **Carbon-fouled — dry, sooty black** | Rich mixture, cold plug, weak ignition, retarded timing, short-trip use | High CO, low CO₂; LTFT negative |
| **Oil-fouled — wet, black, oily** | Worn rings or valve seals, PCV fault, head gasket coolant entry | High HC at idle (oil burning); blue smoke; λ stays balanced |
| **Overheated — white / blistered electrode** | Lean mixture, too-hot plug heat range, over-advanced timing, cooling fault | Low CO, high O₂, high NOx |
| **Fuel-fouled — wet, smells of petrol** | No-spark on that cylinder, flooding, immobiliser cut | Cranking-shaped gases (`master_non_starter_guide.md §2`) |
| **Deposits / ash buildup** | Oil-additive-derived ash; fuel additive deposits; long service interval | Gradual HC rise |
| **Cracked insulator / damaged ground electrode** | Mechanical impact, detonation, pre-ignition | Sudden misfire onset |

---

## 5. Secondary ignition waveform — the microscope

While the OBD misfire monitor detects *that* a cylinder missed, only the secondary ignition waveform reveals *why*. The waveform divides into the **firing line** (peak voltage required to bridge the spark gap) and the **spark line** (duration the arc is sustained, called burn time).

| Segment | Spec | Diagnostic |
|---|---|---|
| **Firing voltage (firing line)** | 8–15 kV at warm idle | Standard requirement to bridge the plug gap |
| **Burn time (spark line)** | 1.0–2.5 ms | Ideal duration of a complete combustion spark |
| **High firing line (> 25 kV)** | Worn plugs, wide gap, lean mixture, open wire | Plug has too-wide a gap or air-fuel charge is too lean to conduct readily |
| **Low firing line (< 8 kV)** | Rich mixture, fouled plug, low compression | Charge is too conductive (rich); plug has shunted resistance (fouling) |
| **Short burn time (< 0.8 ms)** | Weak coil, lean mixture, high secondary resistance | Coil running out of stored energy too fast |
| **Long burn time (> 2.5 ms)** | Rich mixture, low compression, fouled plug | Conductive charge holds the arc longer than it should |
| **Spark line slope** | Slight upward | Reflects changing cylinder pressure at end of combustion |
| **Coil oscillations (post-spark)** | ≥ 3 ripples after the spark line | Confirms residual coil energy and intact secondary winding |
| **Missing oscillations** | < 3 ripples | Internally shorted coil or fouled plug bleeding energy |
| **Reversed polarity** | Positive spike on firing line (instead of negative) | Common in wasted-spark systems for the cylinder firing on exhaust stroke; can elevate kV requirement |

**Diagnostic split — ignition vs lean misfire from waveform:**
- **High firing line + short burn time + 3+ oscillations** → ignition system is delivering, the charge is hard to ignite (lean misfire). Cross-ref `master_fuel_trim_guide.md §4` for vacuum-leak / low-fuel-pressure causes.
- **High firing line + short burn time + < 3 oscillations** → coil is failing. Replace the coil.
- **Low firing line + long burn time** → rich misfire or fouled plug. Cross-ref `master_fuel_system_guide.md §3`.
- **Normal firing line + missing burn segment entirely** → no spark at all on that cycle. Coil driver, primary wire, ECU output stage.

---

## 6. Gas signatures of misfire types — the splitter

| Misfire type | HC | CO | CO₂ | O₂ | λ (analyser) | Mechanism |
|---|---|---|---|---|---|---|
| **Ignition misfire** | **Very high (> 1000 ppm)** | Low | Low | High | ≈ 1.00 (raw fuel + raw air balance) | No spark; near-complete fuel exits unburned alongside the air |
| **Lean misfire** | High | Low | Low | High | > 1.05 | Too little fuel to ignite; the charge fails to light |
| **Rich misfire** | Very high | High | Low | High | < 0.95 | Excess fuel quenches the spark; raw fuel + partial burn + excess air all exit |
| **Mechanical misfire** | Very high | Low | Low–Normal | Normal–High | ≈ 1.00 (balanced) | Compression too low to support combustion; mixture enters but burn is poor |

**The key diagnostic splitter:** ignition misfire typically produces the **highest HC readings** (often > 1000 ppm for an active misfire) because near-complete fuel enters and exits without burning. A lean misfire produces only somewhat elevated HC because the charge is partly air. A rich misfire produces high HC AND high CO together, the only condition where both rich-side and lean-side products coexist (`master_gas_guide.md §3 rule 3`).

---

## 6.1 Secondary waveform pass/fail benchmarks

These numerical thresholds are the shop-floor pass/fail criteria for secondary ignition diagnostics, sourced from `Spark Burn Time.pdf` and `Spark Line Study.pdf`:

| Parameter | Pass | Fail | Interpretation |
|-----------|------|------|---------------|
| **Spark burn line duration (idle)** | **1.3–2.0 ms** | **< 0.75 ms** | Burn line < 0.75 ms at idle = lean mixture or weak spark output. Short burn = insufficient energy to sustain the arc through the combustion event. |
| **Spark plug wire resistance** | **< 8,000 Ω/ft** | **> 8,000 Ω/ft** | Excessive resistance attenuates coil secondary voltage; can cause misfire under load when cylinder pressure is high. |
| **Spark plug gap** | **0.028–0.043 in** (0.71–1.09 mm) | Outside range | Too wide = misfires at high RPM/load; too narrow = pre-ignition risk, sooty plug. |
| **Misfire rate threshold** | **≤ 1 %** | **> 1 %** | Above 1 % misfire rate, the catalyst receives sufficient raw HC and O₂ to overheat internally. Type A misfire (catalyst-damaging): rate threshold is manufacturer-calibrated but physically tied to this 1 % boundary. |

The burn-line duration is load-sensitive: at 2500 RPM the line shortens (less time between spark events); at idle it should be comfortably in the 1.3–2.0 ms window. A lean-misfire condition (unmetered air leak, low fuel pressure) consistently produces a short burn line because lean mixtures require more energy to ignite and the arc quenches earlier.

---

## 7. CKP / CMP sensor failure patterns

| Sensor | Failure | DTC | Effect |
|---|---|---|---|
| **CKP** | Open or shorted | P0335 / P0336 | No RPM signal during cranking. ECU disables BOTH fuel injection AND ignition. Engine cranks but never starts. Single most common no-start cause that mimics fuel and spark problems simultaneously. |
| **CKP** | Reluctor wheel damaged / loose | P0335 intermittent | Engine starts, then stalls; misfire under transient |
| **CMP** | Open or shorted | P0340 / P0341 | On modern ECUs: fall-back to batch fire, hard start, but engine usually runs. Misfire-monitor degrades to P0300 only (cannot identify which cylinder). |
| **CMP** | Reluctor degraded | Intermittent P0340 | Cylinder-specific misfire detection unreliable; P0300 instead of P0301–P030x |

Cross-ref `master_non_starter_guide.md §5` for cranking-time CKP/CMP rules.

---

## 8. Spark timing — what the ECU controls and what it leaks

The ECU commands ignition timing in degrees BTDC (before top dead centre). The 4D engine reads `ff_ignition_advance` from freeze-frame and live `ignition_advance` PID where available.

| Condition | Typical advance | Notes |
|---|---|---|
| Idle, warm | 8–15° BTDC | Varies by engine; low-load idle setpoint |
| Steady cruise | 25–35° BTDC | Maximum advance for fuel economy |
| WOT, low RPM | 5–15° BTDC | Pulled back to prevent knock under load |
| Knock retard | Up to −10° from base | Knock sensor commands retard in increments |

**Late-timing signature:** retarded ignition (e.g. timing belt jumped a tooth, VVT phaser stuck retarded, knock-retard maxed) shortens combustion duration before exhaust valve opens. Result: high tailpipe HC, lower CO₂, mild rich λ (0.93–0.99). Per `master_gas_guide.md §8.4` and the v4 audit finding F2/F3, the SKG's `late_timing` thresholds need HC ≥ 1200 (not 5000), λ ∈ [0.93, 0.99] (not [0.75, 0.92]).

**Over-advanced timing signature:** elevated NOx (high combustion temperature), tendency to knock, possible crackling sound on decel. Less common than retarded.

---

## 9. Cross-reference rules

- **Misfire + low CO + high HC** ⇒ check `master_gas_guide.md §3 rule 5` (single-cyl misfire). The corresponding gas-module pattern is `individual_cylinder_misfire`.
- **Random misfire + lean trims + vacuum-leak signature** ⇒ cross-ref `master_air_induction_guide.md §5` (vacuum-leak topology) and `master_fuel_trim_guide.md §4` (decision tree).
- **P0300 with mixed cylinder misfires** ⇒ check coil pack (wasted-spark systems share coils across cylinder pairs).
- **Misfire only at idle, clears at 2500 RPM** ⇒ EGR stuck open, vacuum leak, or low fuel pressure at idle.
- **Misfire only under load** ⇒ ignition coil breaking down at high cylinder pressure, fuel-pump volume insufficient, fuel filter clogged.
- **Misfire on cold start, clears warm** ⇒ valve-stem seal leak (oil at startup fouls plug); cold-start-rich plug fouling; sticky valve.

---

## 10. Citations

- SAE J1979 — Mode $06 misfire monitor PIDs (TID $A1, $A2 misfire counters per cylinder).
- `cases/library/automotive/mix/Analyzing Ignition Misfires_0106ta.pdf` — practical secondary-waveform interpretation.
- `cases/library/automotive/mix/analyzing-ignition-misfires.md` — extracted summary.
- `cases/library/automotive/mix/Spark Burn Time.pdf` and `Spark Line Study.pdf` — burn time and spark-line interpretation.
- `cases/library/automotive/mix/Spark Timing Myths Debunked - Spark Timing Myths Explained.pdf` — common myth-busting on advance/retard.
- `cases/library/automotive/mix/extracted/Ignition Timing Explained_Timing an Unknown Engine.md` — timing fundamentals.
- `cases/library/automotive/mix/Random-Misfire Page2.pdf` — random misfire diagnostic flow.
- `cases/library/automotive/mix/extracted/Engine Misfire Diagnosis.md` — extracted reference.
- `cases/library/automotive/mix/misfire-diagnosis.md` and `misfire.md` — extracted summaries.
- `cases/library/automotive/mix/ignition-diagnostics.md` and `ignition-timing.md` — already-extracted local references.
- Cross-ref: `master_gas_guide.md §3 rule 5` (single-cyl misfire low CO), `§8.4` (late timing); `master_obd_guide.md §5.3` (P030x family).
