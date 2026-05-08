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
