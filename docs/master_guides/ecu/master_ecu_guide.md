# Master ECU Fault Patterns Guide — 4D Petrol Diagnostic Engine

**Purpose.** A single, self-contained reference for ECU (Engine Control Unit / ECM) fault patterns — internal control module hardware failures (P0601–P0606 family), ECU logic inversion patterns where the ECU's perceived mixture state contradicts physical tailpipe reality, relay and power-supply fault cascades, and the physical justification for the λ < 0.905 tightening used in the 4D engine's `ecu_logic_inversion` compound KG node. The architecture principle "chemistry beats ECU" depends on understanding when and how the ECU can produce false or contradictory information. Rows in the CSV that cite ECU inversion as the expected fault cite the rules below.

---

## 1. The ECU's role — diagnostician and fault source

The Engine Control Module (ECM/ECU) is simultaneously a diagnostician (it runs monitors, sets DTCs, commands fuel trim) and a potential fault source (it can be wrong). ECU faults fall into three categories:

1. **Internal hardware/software faults** — the ECU itself is broken.
2. **ECU logic inversion** — the ECU hardware is healthy, but its sensor inputs are biased, causing it to "perceive" a mixture state opposite to physical reality.
3. **ECU power/ground integrity faults** — the ECU produces cascade errors because its supply voltage or ground reference is corrupted.

This distinction is critical: logic inversion is not a broken ECU, it is a *deceived* ECU. The repair target for logic inversion is the sensor or exhaust leak — not the ECU itself.

---

## 2. Internal control module faults (P0601–P0606 family)

These DTCs indicate the ECU's internal microprocessor, memory, or programming integrity checks have failed. They are Type A DTCs (MIL illuminates immediately) and are among the highest-priority codes in any diagnostic session.

| DTC | Internal fault | Typical cause | Diagnostic priority |
|-----|---------------|---------------|---------------------|
| **P0601** | Memory Checksum Error | Corrupted ROM or flash memory | Very high — ECU may be operating on corrupted calibration data |
| **P0602** | Programming Error | Incomplete reflash or interrupted programming | High — ECU may have missing or partial calibration |
| **P0603** | Keep Alive Memory (KAM) Error | Lost learned values (fuel trim, idle adaptation) on power loss | Moderate — ECU reverts to base maps; fuel trim resets to zero |
| **P0604** | RAM Error | Random Access Memory failure; transient data corruption | Very high — unpredictability in all ECU outputs |
| **P0605** | ROM Error | Read-Only Memory failure; permanent calibration corruption | Very high — ECU cannot run correct calibration |
| **P0606** | Processor Fault | Internal microprocessor integrity failure detected by watchdog | Very high — ECU is fundamentally unreliable |

**Critical diagnostic rule:** Before condemning an ECU for any P060x code, verify power and ground integrity. Low battery voltage or momentary power/ground loss to the ECM may trigger these codes. The 4D engine must surface a `verify_ecu_power_ground` check whenever a P060x code is present before routing to `ECU_Internal_Checksum_Error` or similar fault nodes.

**5V reference rail:** The ECM's internal 5 V reference supply feeds all analogue sensors. If the reference rail drops below ~4.7 V or rises above ~5.1 V (caused by a shorted sensor or actuator on the rail), a P0606 may set. The root cause is the shorted component, not the ECU. All P060x codes must be preceded by battery voltage and ground resistance checks.

**P0603 special case:** KAM reset clears long-term fuel trim, idle adaptation, and misfire history. After battery disconnect or relay failure, LTFT reads zero and fuel trim behaviour appears erratic for the first drive cycle. Flag this as `verify_ecu_relay` before attributing the trim behaviour to a fuel fault.

---

## 2a. Era-specific ECU architecture — what changed 1990–2020

ECU diagnostic capabilities evolved significantly across the V2 era buckets. Understanding which capabilities exist on the vehicle under test prevents false conclusions from missing data.

| Era | ECU architecture | Diagnostic capability | Implications for 4D engine |
|-----|-----------------|----------------------|---------------------------|
| **1990–1995** | Simple microprocessor; limited or no flash memory; KAM via battery-backed RAM | P0601–P0606 may not exist as defined DTCs; OBD-I codes are manufacturer-specific | ECU internal self-test is rudimentary; the absence of P060x codes does not mean the ECU is healthy. Gas analysis carries proportionally more weight. |
| **1996–2005** | OBD-II mandated; first flash-programmable ECUs; KAM in non-volatile memory or battery-backed | P0600–P0606 family defined; Mode $06 monitor data available; freeze-frame mandated | ECU faults are now coded and retrievable. Freeze-frame available. P0603 may still fire on battery disconnect — distinguish from genuine KAM corruption. |
| **2006–2015** | CAN-bus ECUs; multi-processor architectures; 5V reference rail monitor | P060x extended; CAN communication DTCs (U-codes) can cascade from ECU faults; Mode $09 calibration ID | ECU internal diagnostics are sophisticated. But CAN errors from a failing ECU can generate dozens of spurious U-code DTCs — the ECU fault may hide behind a wall of communication errors. |
| **2016–2020** | High-speed CAN FD; ECU-internal current monitoring per injector/coil driver; O₂ sensor heater circuit monitor per sensor | Rich DTC taxonomy for ECU-internal faults; per-driver diagnostics; GPF sensor integration | ECU fault detection is now granular. A single injector driver fault (P020x) is more likely to be the ECU than the wiring. But the ECU may report individual driver faults when the root cause is a failing MFI relay — apply Rule 5 (§7) before condemning the ECU. |

**Pre-OBD-II special rule (1990–1995):** The absence of ECU DTCs (P060x family) or freeze-frame data in pre-OBD-II vehicles means the 4D engine cannot rely on ECU self-reported faults. Gas analysis, vacuum gauge, and the physical symptom pattern carry higher diagnostic weight. When an OBD-I vehicle exhibits behaviour consistent with ECU logic inversion (false-lean or false-rich), the engine must not default to `insufficient_evidence` simply because the ECU cannot self-report; treat the gas signature as primary evidence.

---

## 3. ECU logic inversion — the central fault class

ECU logic inversion occurs when the ECU's *perceived* mixture state contradicts physical reality as measured by the tailpipe gas analyser. The ECU hardware is healthy; the sensor data it receives is biased or corrupted.

#### 3.1 The three canonical inversion patterns

| Pattern | ECU perceives | Physical reality (tailpipe) | Most likely cause |
|---------|--------------|---------------------------|-------------------|
| **False-lean (most common)** | Lean → ECU adds fuel; positive trim; may set P0171/P0174 | Rich (λ < 1.00, high CO, low O₂) | Exhaust air leak before upstream O₂ sensor; O₂ sensor bias low; MAF under-reading |
| **False-rich** | Rich → ECU subtracts fuel; negative trim; may set P0172/P0175 | Lean (λ > 1.00, low CO, high O₂) | O₂ sensor bias high (silicone poisoning); MAF over-reading |
| **DTC+gas contradiction** | ECU sets lean DTC (P0171) | Tailpipe is rich (λ < 1.00) | O₂ sensor failure or exhaust leak causing ECU to "see lean" while engine runs rich |

#### 3.2 Physical justification for the λ < 0.905 inversion threshold

The 4D engine's `ecu_logic_inversion` trigger was tightened from the original λ < 0.95 boundary to **λ < 0.905**. This is the physical boundary where a rich-running engine is rich enough that the ECU's simultaneous lean perception becomes *impossible* to reconcile with normal sensor tolerance or a plausible exhaust leak.

**Lambda boundary analysis:**

| Lambda range | Engine state | Exhaust leak explanation viable? | Inversion verdict |
|-------------|-------------|----------------------------------|-------------------|
| **0.97–1.00** | Mild rich | Yes — a 2–3 % ambient air leak can shift perceived λ to ≈1.00 | Not an inversion |
| **0.95–0.97** | Borderline rich | Possibly — a moderate leak could explain it | Warning but not definitive |
| **0.905–0.95** | Moderate rich | Suspicious — a leak this large would be audible and cause obvious driveability symptoms | Inversion probable |
| **< 0.905** | Severe rich (~9.5 % excess fuel) | **No** — shifting this to a sensor-perceived lean condition requires ≥10 % ambient air leak, physically impossible without being immediately obvious | **Definitive ECU logic inversion** |

At λ < 0.905, the O₂ sensor has failed, is biased, or the exhaust leak is catastrophically large. The sensor is reading lean despite clearly rich combustion. This is the definitive threshold for the `ecu_logic_inversion` node. The narrowing from 0.95 to 0.905 reduces false positives where borderline-rich mixtures could be explained by a large exhaust leak, while maintaining detection of unequivocal sensor failures.

The symmetric threshold for false-rich inversion is **λ > 1.095** — a definitively lean engine with a DTC saying rich is equally impossible under normal sensor tolerance.

#### 3.3 The feedback-loop trap during misfire

During a severe ignition or mechanical misfire, raw fuel (HC) and raw oxygen (O₂) exit together. The upstream narrowband O₂ sensor — which produces voltage only when combustibles exceed oxygen — may produce no voltage because incomplete combustion leaves both species unreacted. The ECU interprets "no voltage" as lean and enriches further, worsening the misfire. This is **not** an O₂ sensor fault; the sensor responds correctly to an impossible catalytic environment. The 4D engine must route HC > 800 ppm + O₂ high + λ ≈ 1.00 to `Mechanical_Misfire` or `Ignition_Misfire`, not to `ECU_Logic_Inversion`. Cross-ref `master_ignition_guide.md §6`.

---

## 4. ECU relay and power-supply fault cascades

Many vehicles use an MFI relay or main ECU relay to supply power to the ECM and its actuators. A failing relay causes:

- P0603 (KAM reset — learned values lost)
- P0606 (processor fault from voltage dip)
- Random injector and ignition circuit DTCs that clear after restart
- Intermittent no-start conditions

**Routing rule:** When multiple ECU-internal DTCs appear simultaneously (especially P0603 + P0606 or multiple P020x injector codes), and they clear after battery reset, flag `verify_ecu_relay` before routing to any specific sensor or actuator fault. The relay is the common-cause candidate.

**Battery voltage effects:** At < 10.5 V (cranking) or < 11.5 V (running), the ECU may not function correctly. Many ECU fault codes clear permanently after battery is charged to normal levels. Always verify battery state before interpreting P060x codes.

---

## 5. T15 transition — startup and loop-acquisition phase

The T15 (terminal 15 = ignition-on) startup sequence is the critical phase where the ECU establishes closed-loop fuel control. During T15:

- KAM values are loaded; if P0603 cleared them, the ECU starts with zero LTFT (base map only)
- ECT-gated enrichment is active until the closed-loop transition threshold (ECT ≥ ~40 °C + O₂ sensor active)
- STFT polarity should go negative within approximately 15–30 seconds of closed-loop entry (ECU pulling back from the open-loop enrichment baseline)
- The P0172 DTC trigger deviation threshold is typically ±25 % LTFT sustained across a drive cycle — `DTC_P0172_Deviation_Pct = −25%`
- The safe "rich-load" lambda window for WOT power enrichment: λ 0.85–0.92

The 4D engine must suppress `ecu_logic_inversion` during the first 30 seconds of cold-start open loop (before the O₂ sensor reaches operating temperature) because the sensor's signal is invalid and any reading is noise. Cross-ref `master_cold_start_guide.md §5`.

---

## 5a. Freeze-frame interpretation for ECU faults

Freeze-frame data is the ECU's "snapshot" of operating conditions at the moment a fault code was set. For ECU-internal faults and logic-inversion patterns, freeze-frame interpretation follows different rules than for combustion or sensor faults.

#### 5a.1 What freeze-frame tells you about ECU faults

| Freeze-frame PID | P060x internal fault | P0171 + tailpipe λ < 0.905 | P0172 + tailpipe λ > 1.095 |
|-----------------|---------------------|---------------------------|---------------------------|
| **ECT** | Usually normal; fault may set at key-on (cold) | Often at operating temperature | Often at operating temperature |
| **RPM** | May be 0 (key-on, engine off) — hardware check runs at power-up | Typically idle or low-load cruise | Typically idle or low-load cruise |
| **Load (calculated)** | Often 0 % | Low load (< 30 %) — highest vacuum draws exhaust leak | Variable |
| **STFT** | N/A — ECU fault supersedes trim | **Positive** (+15 to +25 %) — ECU adding fuel | **Negative** (–15 to –25 %) — ECU subtracting fuel |
| **LTFT** | May read 0 % (P0603 cleared KAM) | Positive | Negative |
| **Loop status** | May not have reached closed loop | Closed loop | Closed loop |
| **MAP/MAF** | Often no valid reading | Low MAP at idle for exhaust leak scenario | Can be elevated |
| **O₂ sensor voltage** | May be stuck at bias voltage | **Low (< 0.3 V)** — sensor sees lean (but tailpipe is rich) | **High (> 0.7 V)** — sensor sees rich (but tailpipe is lean) |

#### 5a.2 Freeze-frame diagnostic rules for ECU faults

**Rule FF-1 — Key-on, engine-off fault setting:** If P060x freeze-frame shows RPM = 0 and ECT = ambient, the ECU ran its internal self-check at key-on and found a hardware fault. This is a genuine ECU internal fault — not a cascade from a sensor or actuator. Verify power and ground before condemning the ECU.

**Rule FF-2 — Contradicting fuel trim vs tailpipe:** When the freeze-frame shows STFT sharply positive (+20 % or more) but the tailpipe gas analyser reads λ < 0.905 (rich), the ECU is enriching an engine that is already rich. This is the quintessential false-lean signature. The freeze-frame confirms the ECU's *intent* (enrich) and the tailpipe confirms the *reality* (already rich). The sensor or exhaust leak is the root cause.

**Rule FF-3 — Contradicting fuel trim vs tailpipe (inverse):** When the freeze-frame shows STFT sharply negative (–20 % or more) but the tailpipe reads λ > 1.095 (lean), the ECU is leaning an engine that is already lean — false-rich signature.

**Rule FF-4 — Multiple P060x in the same freeze-frame:** When P0603, P0606, and P020x injector codes all appear with the same freeze-frame timestamp, the common cause is an ECU power-supply interruption (relay, fuse, or ground). Do not replace the ECU; verify the power supply first.

**Rule FF-5 — Freeze-frame capture-point bias:** The ECU captures freeze-frame at the moment of fault detection, which for P0171/P0172 may be after the fuel trim has already deviated significantly. The freeze-frame shows the *end state* of the fault, not the *initiating* condition. The 4D engine should weight freeze-frame data as confirmatory, not as the primary trigger for logic-inversion detection.

---

## 5b. ECU threshold provenance — every λ and trim threshold cited

This table maps the numeric thresholds the 4D engine uses for ECU-logic and ECU-internal fault nodes to their physical justification:

| Threshold | Value | 4D engine node(s) | Physical justification | Source guide § |
|-----------|-------|-------------------|----------------------|----------------|
| `lambda_rich_inversion` | 0.905 | `ECU_Logic_Inversion_False_Lean` | > 10 % ambient air leak required to shift perceived λ lean from λ < 0.905 | `master_ecu_guide.md §3.2` |
| `lambda_lean_inversion` | 1.095 | `ECU_Logic_Inversion_False_Rich` | Symmetric false-rich boundary; equally impossible under normal sensor tolerance | `master_ecu_guide.md §3.2` |
| `co_rich_gate` | 1.5 % | `ECU_Logic_Inversion_False_Lean` | CO > 1.5 % confirms rich combustion; contradicts lean DTC | `master_ecu_guide.md §3.2` |
| `o2_lean_gate` | 2.0 % | `ECU_Logic_Inversion_False_Rich` | O₂ > 2.0 % confirms lean combustion; contradicts rich DTC | `master_ecu_guide.md §7 rule 3` |
| `hc_misfire_trap` | 800 ppm | Misfire-not-inversion routing | HC > 800 ppm routes to misfire, not ECU inversion | `master_ecu_guide.md §3.3` |
| `o2_misfire_trap` | 5.0 % | Misfire-not-inversion routing | O₂ > 5 % with HC > 800 ppm = incomplete combustion | `master_ecu_guide.md §3.3`, `master_ignition_guide.md §6` |
| `ltft_deviation_p0171` | +25 % | `sensor_bias_lean`, `ECU_Logic_Inversion_False_Lean` | LTFT at max authority +25 % — ECU cannot compensate further | `master_ecu_guide.md §5` |
| `stft_positive_threshold` | +20 % | False-lean detection | STFT > +20 % sustained with rich tailpipe confirms contradiction | `master_ecu_guide.md §5a.2 rule FF-2` |
| `stft_negative_threshold` | –20 % | False-rich detection | STFT < –20 % sustained with lean tailpipe confirms contradiction | `master_ecu_guide.md §5a.2 rule FF-3` |
| `vbatt_min_running` | 11.5 V | `ECU_Internal_Fault`, P060x routing | Below 11.5 V running — ECU may not function correctly | `master_ecu_guide.md §4` |
| `vref_5v_lower` | 4.7 V | P0606 routing | 5 V reference rail below 4.7 V — shorted sensor or actuator | `master_ecu_guide.md §2` |
| `vref_5v_upper` | 5.1 V | P0606 routing | 5 V reference rail above 5.1 V — supply regulation fault | `master_ecu_guide.md §2` |

---

## 6. ECU electronic faults — DTC reference

| DTC | Pattern in 4D engine | Routing rule |
|-----|---------------------|-------------|
| **P0601** | `ECU_Internal_Checksum_Error` | Verify power+ground first; check for recent programming |
| **P0603** | KAM reset — treat all LTFT as zero; re-baseline fuel trim | Verify relay and battery; do not condemn fuel system until LTFT re-learns |
| **P0604** | RAM error — ECU outputs may be erratic | Same as P0601 |
| **P0606** | `ECU_Internal_Checksum_Error` | Verify 5V reference rail for shorted sensor; verify power+ground |
| **P0171 + tailpipe λ < 0.905** | `ECU_Logic_Inversion_False_Lean` | O₂ sensor or exhaust leak before sensor — suppress lean-mixture candidates |
| **P0172 + tailpipe λ > 1.095** | `ECU_Logic_Inversion_False_Rich` | O₂ sensor contaminated or MAF over-reading — suppress rich-mixture candidates |
| **P020x** (injector driver) | `ECU_Injector_Driver_Fail` or injector wiring | Verify injector resistance; check for ECU relay fault |

---

## 7. The 4D engine's routing rules for ECU fault patterns

```
RULE 1 — P060x internal fault:
  IF DTC ∈ {P0601, P0604, P0605, P0606}:
    → surface ECU_Internal_Fault with high priority
    → surface verify_ecu_power_ground as required check
    → do NOT route to sensor or actuator faults until power/ground verified
    → do NOT route to ecu_logic_inversion (these are hardware faults, not perception faults)

RULE 2 — False-lean inversion (definitive):
  IF DTC ∈ {P0171, P0174} AND tailpipe λ < 0.905 AND CO > 1.5%:
    → surface ECU_Logic_Inversion_False_Lean
    → root cause: O₂ sensor bias or exhaust leak before sensor
    → suppress all lean-mixture fault candidates

RULE 3 — False-rich inversion (definitive):
  IF DTC ∈ {P0172, P0175} AND tailpipe λ > 1.095 AND O₂ > 2.0%:
    → surface ECU_Logic_Inversion_False_Rich
    → root cause: O₂ sensor contaminated or MAF over-reading
    → suppress all rich-mixture fault candidates

RULE 4 — Misfire trap (do not confuse with inversion):
  IF HC > 800 ppm AND O₂ > 5% AND λ ≈ 1.00 AND CO < 1.5%:
    → route to Ignition_Misfire or Mechanical_Misfire, NOT ECU_Logic_Inversion
    → the O₂ sensor is responding correctly to incomplete combustion

RULE 5 — Multi-DTC ECU relay cascade:
  IF P0603 AND (P0606 OR multiple P020x):
    → flag verify_ecu_relay before all other routing
    → after relay verification, re-run diagnosis with fresh LTFT baseline

RULE 6 — Pre-OBD-II ECU suspicion (1990–1995 only):
  IF MY 1990–1995 AND λ contradiction observed (ECU enrichening, tailpipe rich, or vice versa)
     AND no DTCs available (pre-OBD-II):
    → treat gas signature as primary evidence
    → do NOT default to insufficient_evidence because ECU cannot self-report
    → surface ECU_Logic_Inversion with a note: "pre-OBD-II — no ECU DTC confirmation available"

RULE 7 — ECU 5V reference rail short cascade:
  IF P0606 AND (multiple sensor DTCs from different sensors on the same reference rail):
    → one sensor or actuator on the 5V rail is shorted, pulling down the rail
    → unplug sensors one at a time while monitoring the 5V reference PID
    → when reference voltage returns to 4.7–5.1 V, the last unplugged sensor is the shorted component
    → do NOT replace ECU until all sensors on the rail have been checked

RULE 8 — ECU logic inversion during misfire suppression:
  IF HC < 800 ppm AND O₂ < 5 % AND λ < 0.905 AND P0171:
    → proceed with ECU_Logic_Inversion_False_Lean (the misfire trap is not triggered)
  IF HC > 800 ppm AND O₂ > 5 % AND λ ≈ 1.00:
    → misfire trap active; route to ignition/mechanical, not ECU
    → the O₂ sensor is reading correctly; the combustion chemistry is the problem
```

---

## 8. Sensor bias vs ECU logic inversion — the boundary

Sensor bias (a continuously drifted O₂ sensor) produces a *graded* perception gap that may be within the ECU's trim authority — the ECU compensates and no DTC fires. ECU logic inversion is a *categorical* contradiction — the ECU has been fooled so badly that it is heading in the opposite direction from reality.

| Condition | Fuel trim | DTC | 4D engine call |
|-----------|-----------|-----|----------------|
| Sensor drifted lean by 0.04 λ | LTFT +8 to +15 % | None (within trim authority) | `Lazy_O2_Sensor_Aging` |
| Sensor drifted lean by 0.10 λ | LTFT +20 to +25 % | P0171 may set | `sensor_bias_lean` or `ecu_misread_lean_confirmed` |
| Sensor failed lean; exhaust λ < 0.905 | LTFT maxed +25 % | P0171 set; CO > 1.5 % | `ECU_Logic_Inversion_False_Lean` |

Cross-ref `master_o2_sensor_guide.md §6` for the sensor-bias-vs-real-mixture rule.

---

## 8a. The perception gap — when ECU reality contradicts physical reality

The perception gap is the central concept linking ECU diagnostics to gas analysis. The ECU's model of the engine state is built from sensor data. When a sensor is biased, the ECU acts on a perception that diverges from physical reality. The gap between "what the ECU thinks is happening" and "what the tailpipe says is happening" is the diagnostic signal.

#### 8a.1 Three perception-gap severities

| Severity | Δλ (actual vs perceived) | Fuel trim response | DTC set? | 4D engine action |
|----------|--------------------------|-------------------|----------|-----------------|
| **Mild (sensor aging)** | < 0.04 λ | LTFT 5–15 % compensating | No | Surface `Lazy_O2_Sensor_Aging` as supplementary symptom; continue diagnosis |
| **Moderate (sensor bias)** | 0.04–0.10 λ | LTFT 15–25 %; approaching authority limit | P0171/P0172 may set | Surface `sensor_bias_lean` or `sensor_bias_rich`; flag for sensor replacement |
| **Severe (logic inversion)** | > 0.10 λ | LTFT at limit (±25 %); sensor voltage contradicts tailpipe | P0171/P0172 set | Surface `ECU_Logic_Inversion_False_Lean` or `ECU_Logic_Inversion_False_Rich`; suppress all mixture fault candidates |

#### 8a.2 Perception-gap diagnostic flow

```
1. Measure tailpipe λ with 5-gas analyser.
2. Read O₂ sensor voltage or wideband λ from scan tool.
3. Compute perceived λ:
   - Narrowband: voltage < 0.3 V → ECU perceives lean; voltage > 0.7 V → ECU perceives rich
   - Wideband: read λ directly from PID
4. Compare tailpipe λ vs perceived λ:
   - Tailpipe λ < 0.905 AND ECU perceives lean → FALSE-LEAN INVERSION
   - Tailpipe λ > 1.095 AND ECU perceives rich → FALSE-RICH INVERSION
   - Δλ < 0.04 AND fuel trim compensating → SENSOR AGING (non-blocking)
   - 0.04 ≤ Δλ ≤ 0.10 → SENSOR BIAS (requires sensor replacement)
5. If FALSE-LEAN INVERSION confirmed:
   - Check for exhaust leak before upstream O₂ sensor
   - Check O₂ sensor ground and heater circuit
   - If no leak and heater OK, replace O₂ sensor
6. If FALSE-RICH INVERSION confirmed:
   - Check O₂ sensor for silicone contamination (white powder on sensor tip)
   - Check MAF for contamination causing over-reading
   - If DTC + tailpipe contradict but sensor swap doesn't fix → investigate ECU analog-to-digital channel
```

#### 8a.3 The "chemistry beats ECU" architecture principle

The 4D engine's foundational architecture rule is: **gas chemistry (Brettschneider lambda) is ground truth; ECU perception is fallible.** This means:

- When tailpipe λ and ECU-perceived λ agree within tolerance → normal diagnostic flow.
- When tailpipe λ and ECU-perceived λ disagree beyond the thresholds above → the ECU is in error. Trust the tailpipe.
- This principle overrides all fuel-trim-based fault hypotheses: if the ECU is enrichening because it perceives lean, but the tailpipe is actually rich, the rich-mixture fault candidates (injector leak, high fuel pressure) are suppressed because the root cause is a *false* perception of leanness — not an actual rich condition that requires correction.

The λ < 0.905 and λ > 1.095 thresholds are calibrated to ensure that only physically impossible perception gaps trigger the inversion logic. Sensor aging and borderline cases remain in the "bias" category and do not suppress mixture fault candidates — they inform the sensor health diagnostic alongside normal mixture fault diagnosis.

---

## 9. Cross-references

- `master_o2_sensor_guide.md §6` — sensor bias threshold and the Δλ delta gate
- `master_gas_guide.md §3 rule 4` — CO high + trim negative = real rich, not perceived lean
- `master_ignition_guide.md §6` — misfire gas signature (HC very high + O₂ high + λ ≈ 1.00)
- `master_cold_start_guide.md §5` — suppress inversion during open-loop startup
- `master_obd_guide.md §2` — P060x DTC sub-system index
- `master_perception_guide.md §3` — expanded perception-gap decision table

---

## 10. Citations

- SAE J1979 — Mode $01/$03 DTC definitions; Mode $06 monitor enable conditions
- GM TechLink: ECM internal DTC diagnostic bulletins (P0601, P0606 power/ground verification)
- Haltech Knowledge Base: Narrowband vs Wideband oxygen sensor signal interpretation
- Innova Diagnostic Reference: High-load and idle freeze frame interpretation
- AVI OnDemand: "Fuel Trim Diagnosis and O2 Sensor Performance"
- OBD-II PIDs — Wikipedia, accessed 2026-05-03
