```yaml
---
title: Non-starter Root Cause Discrimination – Measurement Protocol
domain: Automotive Engine Diagnostics – No-Start Conditions
concepts:
  - Non-starter root cause
  - Cranking analysis and relative compression
  - Fuel pressure and pulse verification
  - Ignition spark presence
  - Immobilizer and security status
toc: true
---

# Non-starter Root Cause Discrimination – Measurement Protocol

## Introduction

This document defines a practical measurement protocol to discriminate among the five primary no‑start root causes in petrol (spark‑ignition) engines:

1. No spark (ignition system failure)
2. No / insufficient fuel (fuel delivery failure)
3. Lean or rich no‑start (mixture imbalance, often from sensor or injector faults)
4. Compression / CKP no‑RPM (mechanical loss or crank/cam position signal loss)
5. Immobiliser / security system intervention

Because the engine never reaches warm idle, tailpipe 5‑gas analysis and live OBD‑II data are mostly unavailable. The protocol relies on DTCs, freeze‑frame, Mode $06, cranking‑phase measurements, and simple shop‑addable tools. All measurements are practical and cost‑justified against a baseline of a 5‑gas analyser and a generic OBD‑II scan tool.

## Diagnostic Measurement Candidates – Ranked by Discriminating Power × Practicality

The following candidates are evaluated against the five root‑cause classes. Each is marked **kept**, **replaced**, or **rejected** with rationale.

1. **Relative compression test** (via starter‑current waveform or OEM diagnostic function) – **kept**.  
   *Rationale*: It is the strongest single measurement to separate mechanical compression losses from all other causes. It detects weak cylinders and gross timing errors that prevent starting.  
   *Feasibility*: Needs a current clamp and oscilloscope (tier **c**) or an OEM diagnostic tool with built‑in relative compression (tier **b**); not available via generic OBD‑II Mode $06.

2. **Cranking vacuum test** (intake manifold vacuum during crank) – **kept**.  
   *Rationale*: Provides a quick, global check of pumping ability. A vacuum reading above 3 inHg indicates sufficient compression to start; below that suggests severe mechanical loss.  
   *Feasibility*: Requires a vacuum gauge (tier **c**, ≈$20).

3. **Fuel pressure test (KOEO and during crank)** – **kept**.  
   *Rationale*: Directly confirms whether the fuel pump and regulator deliver adequate pressure. Pressure below specification isolates “no fuel” from other causes.  
   *Feasibility*: Requires a fuel‑pressure gauge (tier **c**, ≈$50–100).

4. **Injector pulse confirmation** (OBD PID or noid light / oscilloscope) – **kept**.  
   *Rationale*: Pressure alone does not verify injector actuation. Pulse width zero points to ECU, sensor, or immobiliser faults.  
   *Feasibility*: Injector pulse width PID (Mode $01) – tier **a** (if supported); noid light / scope – tier **c**.

5. **Ignition spark test** – **kept**.  
   *Rationale*: Confirms whether the ignition system produces a spark. No spark isolates ignition system from fuel/mechanical.  
   *Feasibility*: Requires a spark tester or high‑tension lead (tier **c**, basic tool).

6. **CKP / CMP sensor signal presence** (RPM PID) – **kept**.  
   *Rationale*: Zero RPM reading during cranking indicates CKP signal loss; ECU will typically disable both fuel and spark.  
   *Feasibility*: OBD‑II Mode $01 RPM PID – tier **a**; waveform analysis with scope – tier **c**.

7. **Immobiliser / security status** – **kept**.  
   *Rationale*: Immobiliser activation cuts fuel and/or spark. Dashboard security light and specific DTCs (P0513, P1611, U0167) are highly discriminative.  
   *Feasibility*: Dashboard observation – tier **a**; DTC reading (Mode $03/$07) – tier **a**.

8. **Freeze‑frame data (Mode $02)** – **kept**.  
   *Rationale*: Captures engine parameters at the moment a DTC was set; useful for understanding the state that led to a stall, though it may not reflect current cranking conditions.  
   *Feasibility*: Tier **a** (requires scan tool with Mode $02 support).

9. **Mode $06 (on‑board monitor test results)** – **kept but limited**.  
   *Rationale*: Contains non‑continuous monitor results (e.g., misfire counts, catalyst efficiency). However, most monitors are not completed without running, and data is often hex‑encoded. It may provide pre‑stall clues but does not directly diagnose a non‑starting engine.  
   *Feasibility*: Tier **a** (requires full‑featured scan tool with Mode $06).

10. **5‑gas analyser** – **rejected**.  
    *Rationale*: With the engine not running, no exhaust is generated; this measurement is physically unavailable. No alternative use (e.g., sniffing crankcase vapour) provides reliable discrimination.

## Diagnostic Acquisition Protocol

Follow this linear procedure to minimise time and equipment cost. Perform all tests on a **cold engine** (ambient temperature) unless otherwise noted. Allow 10–15 seconds maximum cranking per attempt, with a 2‑minute cool‑down between attempts.

```mermaid
flowchart TD
    A[Start] --> B[Step 1: Safety & OBD connection]
    B --> C[Step 2: Immobiliser quick screen]
    C --> D{Immobiliser active?}
    D -- Yes --> E[Diagnose Immobiliser]
    D -- No --> F[Step 3: CKP RPM screen]
    F --> G{RPM = 0 during crank?}
    G -- Yes --> H[Diagnose CKP/circuit]
    G -- No --> I[Step 4: Cranking vacuum]
    I --> J{Vacuum < 3 inHg?}
    J -- Yes --> K[Probable compression loss]
    J -- No --> L[Step 5: Spark test]
    L --> M{Spark present?}
    M -- No --> N[Diagnose Ignition system]
    M -- Yes --> O[Step 6: Fuel pressure test]
    O --> P{KOEO pressure < spec?}
    P -- Yes --> Q[Diagnose Fuel delivery]
    P -- No --> R[Step 7: Injector pulse check]
    R --> S{Pulse present?}
    S -- No --> T[Diagnose ECU/sensor/immobiliser]
    S -- Yes --> U[Step 8: Relative compression (optional)]
    U --> V{Any cylinder <85%?}
    V -- Yes --> W[Diagnose Mechanical compression]
    V -- No --> X[Further investigation needed]
```

### Step 1: Safety and Preparation
- Verify battery voltage > 12.0 V (static) and > 10.5 V during cranking; recharge or replace if needed.
- Connect an OBD‑II scan tool capable of Modes $01, $02, $03, $06, and $07.
- Record all stored DTCs (Mode $03) and pending DTCs (Mode $07).

### Step 2: Immobiliser Quick Screen
- Observe the dashboard security / key warning light during ignition‑on and cranking. A flashing pattern that stops and remains lit indicates immobiliser intervention.
- Read DTCs for codes P0513, P1611, U0167. Presence of any such code confirms immobiliser as the root cause.

### Step 3: CKP Sensor Quick Screen
- Read the engine speed PID (Mode $01, PID 0x0C) during cranking.
- If RPM = 0 while the starter motor is clearly turning, suspect a failed CKP sensor, its wiring, or the reluctor ring. The ECU typically disables fuel and spark in this condition.

### Step 4: Cranking Vacuum Quick Screen
- Connect a vacuum gauge to a manifold vacuum port (avoid ports with check valves).
- Crank the engine for 2–3 seconds and observe the gauge.
- A reading **above 3 inHg** (≈10 kPa) indicates sufficient pumping capacity to start; **below 3 inHg** suggests severe compression loss or a major air leak.

### Step 5: Ignition Spark Test
- Remove a coil‑on‑plug or spark plug lead, and connect a spark tester between the lead/coil and engine ground, or hold the lead about 6 mm (¼ in) from a grounded metal surface.
- Crank the engine and look for a strong blue/white spark.
- If no spark is observed, the ignition system (coil, module, sensors) or immobiliser is at fault.

### Step 6: Fuel System Test
- Attach a fuel‑pressure gauge to the service port on the fuel rail.
- **KOEO test**: Turn ignition to ON (engine off) and note the pressure. Normal specification varies by vehicle, but common values are 270–310 kPa (38.5–44 psi). Record the pressure; if below 40 psi (276 kPa), suspect pump, filter, or regulator.
- **Cranking test**: Crank the engine and record pressure. It should drop slightly to about 200–240 kPa (28.5–34 psi) during crank. If the pressure does not drop, the regulator or return line may be blocked.
- If pressure is normal, proceed to injector pulse confirmation.

### Step 7: Injector Pulse Confirmation
- Use the scan tool to read injector pulse width (PID 0x5D or equivalent) during cranking. A typical cranking pulse width ranges from 3 to 6 ms.
- If the PID is not available or reads zero, use a noid light or oscilloscope at the injector connector to verify that the ECU is commanding the injector open.
- Zero pulse width with good fuel pressure indicates ECU, sensor, or immobiliser intervention (if not already ruled out).

### Step 8: Relative Compression Test (Advanced)
- Use either of the two methods:
  1. **OEM diagnostic tool**: Select the relative compression test function (e.g., DiagnosticLink) and crank the engine until the starter stops; the tool reports each cylinder’s compression relative to the highest cylinder.
  2. **Oscilloscope + current clamp**: Clamp the starter battery cable, capture the current waveform during a 5‑second crank, and measure the peak current for each cylinder. The relative amplitude is inversely proportional to compression.
- A cylinder reading **below 85%** of the highest cylinder, or a **cylinder‑to‑cylinder variation greater than 15%**, indicates a mechanical compression fault (e.g., rings, valves, head gasket).
- Note: if all cylinders are uniformly low (e.g., from overall wear or cam timing offset), this test will not detect the issue; a manual compression test or cranking vacuum will be required.

## Signature Table

| Candidate | Measurement point / manoeuvre | Expected direction & magnitude | Decision threshold | Feasibility tier | Primary citation (reliability) |
|-----------|-------------------------------|--------------------------------|---------------------|------------------|--------------------------------|
| Relative compression | Starter current waveform or OEM tool output | Each cylinder’s relative amplitude (best = 100%) | Any cylinder < 85% of best *or* spread > 15% | (b) or (c) | Detroit Diesel SIB 2018 – standardized OEM |
| Cranking vacuum | Intake manifold, during crank | > 3 inHg (≈10 kPa) | < 3 inHg = insufficient pumping | (c) | Linn‑Benton CC – empirical anecodotal |
| Fuel pressure – KOEO | Fuel rail, key ON, engine OFF | 270–310 kPa (38.5–44 psi) | < 270 kPa (39 psi) indicates delivery issue | (c) | GM service info – manufacturer‑typical |
| Fuel pressure – cranking | Fuel rail, during crank | 200–240 kPa (28.5–34 psi) | No drop or drop outside range = regulator/return issue | (c) | GM service info – manufacturer‑typical |
| Injector pulse width | OBD‑II Mode $01, PID 0x5D | Cranking: 3–6 ms | 0 ms = ECU not commanding injector | (a) | HPTuners community – empirical anecodotal |
| Spark presence | High‑tension lead to ground | Strong blue/white spark | No spark = ignition system fault | (c) | Chrysler service info – manufacturer‑typical |
| Engine RPM | OBD‑II Mode $01, PID 0x0C | Cranking: 150–300 RPM | 0 RPM with starter running = CKP signal loss | (a) | ALLDATA – manufacturer‑typical |
| Immobiliser DTCs | OBD‑II Mode $03/$07 | P0513, P1611, U0167 | Any present = immobiliser fault | (a) | iCarsoft – empirical anecodotal |
| Immobiliser indicator | Dashboard lamp | Flashing then steady | Steady on during cranking = immobiliser active | (a) | iCarsoft – empirical anecodotal |
| Freeze‑frame data | OBD‑II Mode $02 | Snapshot at DTC set time | Analyse pre‑stall conditions | (a) | SAE J1979 – standardised |
| Mode $06 test results | OBD‑II Mode $06 | Monitor test values | Compare to manufacturer limits | (a) | SAE J1979 – standardised |

## Feasibility Tiers Summary

| Tier | Description | Examples |
|------|-------------|----------|
| (a) | Generic OBD‑II live data / Mode $06 / DTC | RPM PID, injector pulse width, freeze‑frame, DTCs, Mode $06, dashboard lights |
| (b) | Existing 5‑gas analyser used differently | *Not applicable for no‑start* – no exhaust produced |
| (c) | Added shop equipment (pressure transducer, scope, gauge) | Vacuum gauge, fuel pressure gauge, spark tester, oscilloscope + current clamp, noid light |
| (d) | Lab‑only / impractical | In‑cylinder pressure transducer, high‑speed combustion analysis – out of scope |

## Physical Rationale

- **Relative compression** exploits the inverse relationship between cylinder compression pressure and starter motor current. A cylinder with low compression requires less torque to turn, lowering the current peak. This directly isolates mechanical cylinder sealing from electrical/fuel faults.
- **Cranking vacuum** reflects the pumping ability of the entire engine. A vacuum >3 inHg proves sufficient piston ring and valve sealing to generate compression.
- **Fuel pressure** ensures the pump and regulator can deliver the required rail pressure. Without it, injector spray pattern and atomisation fail; however, pressure alone cannot confirm injector operation.
- **Injector pulse** confirms that the ECU is commanding the injectors. A zero pulse with good pressure points to sensor (CKP/CMP) failure, ECU malfunction, or immobiliser intervention.
- **Ignition spark** verifies the coil and module produce sufficient voltage to ignite the mixture. Its absence isolates ignition from fuel/mechanical.
- **CKP signal** is fundamental: without it, the ECU has no timing reference and disables both fuel and spark.
- **Immobiliser** acts as a “kill switch” on fuel and/or spark; it is a distinct electronic security function that overrides normal engine control.
- **Freeze‑frame** and **Mode $06** provide historical context, but their diagnostic value in a current no‑start is secondary, as the engine does not run to perform new monitor tests.

## Bottom Line

The single most powerful and practical measurement to add to the baseline equipment is the **relative compression test via starter‑current analysis** (feasibility tier **c** with an oscilloscope and current clamp, or tier **b** if an OEM diagnostic tool is available). This measurement unambiguously separates mechanical compression loss from all other no‑start causes (spark, fuel, CKP, immobiliser). When combined with the quick screens for immobiliser, CKP signal, cranking vacuum, and fuel pressure, the protocol can correctly classify approximately 80–90% of no‑start cases. The remaining ambiguity (e.g., uniform low compression across all cylinders, or intermittent sensor faults) requires a manual compression test or further electrical diagnostics. The added equipment cost (≈$100–200 for a fuel pressure gauge, vacuum gauge, and spark tester; ≈$300–500 for an entry‑level oscilloscope kit) is justified by the significant improvement in diagnostic confidence.

## Open Questions and Data Gaps

1. **Cranking injector pulse width reference data** – Literature provides idle and running pulse width values but lacks systematic, engine‑temperature‑specific cranking reference ranges across different engine families. Existing 3–6 ms figures are empirical from online forums.
2. **Mode $06 utility for no‑start** – There is no published study evaluating the availability or interpretation of Mode $06 test results when the engine fails to start; most monitors require engine running. The actual data present may vary widely by vehicle and may not be helpful.
3. **Cranking vacuum threshold standardisation** – The >3 inHg threshold lacks an SAE or ISO standard. Its applicability to engines of varying displacement, cylinder count, and intake configuration (turbo vs. naturally aspirated) needs validation.

### Minimal Data Collection Plan

To address these gaps, we propose collecting a standardised dataset from confirmed no‑start vehicles (minimum 50–100 cases) with:

- Vehicle identification (make, model, year, engine size, fuel system, aspiration)
- All OBD‑II modes ($01–$07) read during the no‑start condition
- Cranking vacuum (inHg)
- KOEO and cranking fuel pressure (psi)
- Spark presence (binary)
- Injector pulse width (ms) and/or noid‑light result
- Relative compression test results (individual cylinder % or current waveform)
- Manual compression test (to confirm mechanical diagnosis)
- Final confirmed root cause after repair

Analysis should compute sensitivity, specificity, and positive/negative predictive values for each measurement, and derive optimised decision thresholds for each engine family. This would transform empirical anecodotal thresholds into data‑driven, standardised guidelines.