---
title: "Cluster 9 — Confirming No Fault: Evidence-Based Protocol for Reliable Healthy-Vehicle Classification"
domain: "automotive diagnostics, OBD-II, emissions, fault discrimination"
concepts:
  - "OBD readiness monitors"
  - "fuel trim (STFT/LTFT)"
  - "Mode $06 monitor margins"
  - "oxygen sensor dynamics"
  - "two-point gas stability"
toc: true
---

# Cluster 9 — Confirming "No Fault" Reliably: Minimum Evidence Set and Decision Protocol

## 1. Ranked Answer to Question 1: Discriminating Measurements

Each candidate is marked **kept / replaced / rejected** with rationale.

| Rank | Candidate | Verdict | Rationale |
|------|-----------|---------|-----------|
| **1** | **All OBD readiness monitors complete** + **no DTCs of any class** | **Kept** | This is the single most powerful discriminator. A complete readiness set proves that every non-continuously monitored emissions system has executed its self-test since the last memory clear. EPA/CARB I/M programs treat completeness as the gateway to a valid emissions pass. Without completeness, a "clean" gas reading may simply reflect that the monitor has not yet run——the vehicle is *unknown*, not healthy. |
| **2** | **Mode $06 test values with margin** (not merely pass/fail) | **Kept** | Pass/fail is binary and binary only tells you the system has not yet failed. Mode $06 exposes the *numeric test value* and the *test limit* (malfunction threshold). A component whose test value is trending toward the limit is likely to fail soon even though it currently passes. Margin quantifies *remaining life* and separates a genuinely healthy system from one that is marginal but has not yet set a DTC. |
| **3** | **Fuel trims within band** (STFT/LTFT near zero) across idle and 2500 RPM | **Kept** | Fuel trims are the positive evidence of healthy fuel control. STFT within ±5% and LTFT within ±10% is the widely accepted normal band; values beyond ±10% indicate the PCM is actively compensating for a perceived lean or rich condition and will typically set a DTC. The two-point check (idle → 2500 RPM) exposes load-dependent fuel delivery faults that a single idle snapshot cannot. |
| **4** | **Two-point gas stability** (idle → 2500 RPM) | **Kept** | The 4DLab system context identifies the RPM-step as the single most promising discriminator for the hardest collisions. A healthy engine maintains 5-gas values within normative bands across the RPM step; a fault that is latent at idle often expresses as a shift at elevated RPM. This is standardized across EPA/BAR I/M practice for 1990–2010 vehicles and requires no dynamometer. |
| **5** | **O2 sensor dynamics nominal** (switch rate / response time) | **Kept** | A lazy O2 sensor can hide behind clean tailpipe gas. A good sensor's transition time is less than 150 ms; degraded sensors switch more slowly, biasing fuel control without necessarily setting a DTC until the degradation crosses the malfunction threshold. This is practically acquirable via OBD Mode $01 (oxygen sensor voltage) with a scan tool that graphs voltage over time. |
| **6** | **No pending/permanent DTCs** | **Kept** (redundant with Rank 1) | This is subsumed by Rank 1 (readiness complete necessarily implies no pending DTCs that would block completeness), but retained as a standalone check for vehicles where readiness is incomplete. |
| **7** | **Single warm-idle 5-gas snapshot** | **Rejected** | The 4DLab context explicitly states this does not prove health: "a lazy sensor, an intermittent pending fault, or a healthy-catalyst-masked engine problem can all hide behind clean tailpipe gas." A single snapshot is necessary but insufficient. |

---

## 2. Signature Table

| Candidate | Maneuver / Point | Expected Direction & Magnitude | Threshold | Feasibility Tier | Primary Citation |
|-----------|------------------|-------------------------------|-----------|------------------|------------------|
| OBD readiness monitors complete | Drive cycle completed since last memory clear; read via Mode $01 PID 0x01 | All supported monitors = COMPLETE / READY | 100% of supported monitors complete for no-fault call; any incomplete → ABSTAIN | (a) Generic OBD-II live data | SAE J1979; CARB OBD regs; EPA I/M guidance |
| Mode $06 margin | Read test value and test limit for each non-continuous monitor (catalyst, O2 sensor, EVAP, EGR, etc.) | Test value must be inside limit with margin; margin = \|limit − value\| | Margin ≥ 10% of limit range (empirical-anecdotal); any value within 10% of limit → ABSTAIN | (a) Generic OBD-II Mode $06 | SAE J1979 / ISO 15031-5 Service $06; manufacturer service info |
| STFT | Warm idle, closed loop, no load | STFT = 0% ± corrections | −5% to +5% (manufacturer-typical) | (a) Generic OBD-II Mode $01 PID 0x06 | SAE J1979 PID 0x06 |
| LTFT | Warm idle, closed loop, no load | LTFT = 0% ± long-term adaptation | −10% to +10% (manufacturer-typical) | (a) Generic OBD-II Mode $01 PID 0x07 | SAE J1979 PID 0x07 |
| STFT / LTFT at 2500 RPM | Steady 2500 RPM no load, closed loop | Trims should not shift by more than ±5% from idle values | ΔSTFT ≤ ±5%, ΔLTFT ≤ ±5% from idle (empirical-anecdotal) | (a) Generic OBD-II live data | Workshop practice |
| O2 sensor switch rate | Warm idle, closed loop; graph O2 sensor voltage (Mode $01 PID 0x14 / 0x15 / 0x34 / 0x35) | Voltage crosses 0.45 V lean↔rich | Transition time < 150 ms | (a) Generic OBD-II live data with graphing | Motor.com diagnostic article |
| O2 sensor amplitude | Warm idle, closed loop | Voltage swings from ~0.1 V (lean) to ~0.9 V (rich) | Min < 0.2 V, max > 0.8 V (manufacturer-typical) | (a) Generic OBD-II live data | Workshop practice |
| HC at idle | Warm idle, 5-gas analyzer | ≤ 35 ppm (working catalyst); ≤ 50 ppm tolerable | ≤ 50 ppm (standardized)【4DLab context】 | (b) Existing 5-gas analyzer | EPA/BAR I/M standards |
| CO at idle | Warm idle, 5-gas analyzer | 0.1–0.45% | 0.1–0.45% (standardized)【4DLab context】 | (b) Existing 5-gas analyzer | EPA/BAR I/M standards |
| CO2 at idle | Warm idle, 5-gas analyzer | 14.5–16.0% | 14.5–16.0% (standardized)【4DLab context】 | (b) Existing 5-gas analyzer | EPA/BAR I/M standards |
| O2 at idle | Warm idle, 5-gas analyzer | Low single digits | < 1.0% with working catalyst (standardized)【4DLab context】 | (b) Existing 5-gas analyzer | EPA/BAR I/M standards |
| NOx at idle | Warm idle, 5-gas analyzer | Varies by engine; high indicates high combustion temp | Within manufacturer spec; low NOx + high HC + high O2 = misfire pattern【4DLab context】 | (b) Existing 5-gas analyzer | EPA/BAR I/M standards |
| Gas delta: idle → 2500 RPM | Idle → 2500 RPM no load, 5-gas at each point | HC/CO/O2 should not rise; CO2 should not fall | ΔHC ≤ +20 ppm, ΔCO ≤ +0.2%, ΔCO2 ≥ −0.5%, ΔO2 ≤ +0.5% (empirical-anecdotal) | (b) Existing 5-gas analyzer (two-point capture) | EPA/BAR I/M two-speed practice【4DLab context】 |

---

## 3. Bottom Line

**The single recommended measurement to add is not one measurement but a combination: OBD readiness completeness (all monitors complete) plus Mode $06 numeric test values with quantified margin.**

This is **Feasibility Tier (a)** — generic OBD-II live data and Mode $06, available on any OBD-II scan tool that supports Mode $06 (which most professional-grade and many consumer-grade tools do). The expected post-add separability is high: readiness completeness eliminates the "unknown" state where a clean gas reading reflects unrun monitors rather than genuine health; Mode $06 margin separates marginal systems that pass today but are approaching failure from genuinely healthy systems with ample headroom.

For vehicles where OBD-II data are sparse or absent (pre-1996, or cases where the OBD channel is not captured), the fallback is **two-point 5-gas (idle + 2500 RPM)** — Feasibility Tier (b) — which provides a dynamic signature of fuel and combustion health that a single idle snapshot cannot.

**If a vehicle has all readiness monitors complete, no DTCs of any class, Mode $06 test values with ≥10% margin from all limits, STFT within ±5% and LTFT within ±10% at both idle and 2500 RPM, and a stable two-point gas signature, then "no_fault" can be confirmed with high confidence. If any of these conditions is not met, the correct verdict is ABSTAIN ("clean on available evidence, but evidence insufficient to confirm health").**

---

## 4. Decision Rule: No-Fault vs. Abstain

Define the following decision rule for the COMLab fusion stage:

```
IF (all supported readiness monitors == COMPLETE)
AND (no DTCs present: confirmed, pending, or permanent)
AND (for each Mode $06 monitor: |test_value - test_limit| >= 0.10 * |test_limit_range|)
AND (|STFT| <= 5% at idle AND |STFT| <= 5% at 2500 RPM)
AND (|LTFT| <= 10% at idle AND |LTFT| <= 10% at 2500 RPM)
AND (|ΔSTFT| <= 5% AND |ΔLTFT| <= 5% from idle to 2500 RPM)
AND (O2 sensor transition time < 150 ms)
AND (5-gas values within normative bands at both idle and 2500 RPM)
THEN
    verdict = "NO_FAULT" (confidence = HIGH)
ELSE IF (all readiness monitors complete AND no DTCs AND 5-gas values normal)
THEN
    verdict = "NO_FAULT" (confidence = MEDIUM)   // OBD data sufficient even without Mode $06 margin
ELSE IF (5-gas values normal but readiness incomplete OR any DTC present)
THEN
    verdict = "ABSTAIN" — "clean on available evidence, but evidence insufficient to confirm health"
ELSE
    verdict = proceed to fault-family classification
```

**Confidence capping:** As per the 4DLab system principle, a single evidence channel is never allowed to claim certainty. The "no_fault" verdict with all evidence present is capped at **0.85** (high but not certain); with OBD data only (no Mode $06 margin) at **0.70**; with gas only at **0.50** (the system's current baseline).

---

## 5. Acquisition Protocol

### 5.1 Preconditions
- Engine at **normal operating temperature** (coolant ≥ 80°C / 176°F).
- **Closed-loop fuel control** active (verify via Mode $01 PID 0x03 — fuel system status).
- **No active MIL** (though MIL may be off with pending codes — do not rely on MIL alone).
- **Battery not recently disconnected** (readiness will be incomplete if memory was cleared within the last drive cycle).

### 5.2 OBD Readiness Check (Mode $01)
1. Connect generic OBD-II scan tool to DLC.
2. Read **Mode $01 PID 0x01** — monitor status since DTCs cleared.
3. Record status for each supported monitor:
   - Catalyst monitor
   - Oxygen sensor monitor
   - Oxygen sensor heater monitor
   - EGR/VVT monitor
   - EVAP monitor (if supported)
   - Secondary air monitor (if supported)
   - Fuel system monitor
   - Comprehensive component monitor
4. **All supported monitors must read COMPLETE** for a no-fault call. If any read INCOMPLETE, the correct response is **ABSTAIN** — the vehicle may be healthy but the evidence is insufficient.
5. Read **Mode $01 PID 0x01** for DTC count — must be 0.

### 5.3 Mode $06 Margin Check
1. Enter **Mode $06** (test results for non-continuously monitored systems).
2. For each monitor (catalyst, O2 sensor, EVAP, EGR, etc.), read:
   - **Test value** (VAL)
   - **Test limit** (LMT)
   - **Test limit type** (TLT: 0 = max limit, 1 = min limit)
3. Compute margin: if TLT = 0 (test value must be ≤ limit), margin = limit − value; if TLT = 1 (test value must be ≥ limit), margin = value − limit.
4. **If margin < 10% of the limit range for any monitor**, the system is marginal — record as **ABSTAIN** (or "NO_FAULT with caution").
5. **If margin ≥ 10% for all monitors**, record as positive evidence of health.

### 5.4 Fuel Trim Check (Mode $01)
1. At **warm idle**, read:
   - **STFT** (PID 0x06 for Bank 1, PID 0x08 for Bank 2)
   - **LTFT** (PID 0x07 for Bank 1, PID 0x09 for Bank 2)
2. Increase engine speed to **2500 RPM no load** and hold steady.
3. Read STFT and LTFT again.
4. **Acceptable range:** |STFT| ≤ 5% at both points; |LTFT| ≤ 10% at both points.
5. **Delta check:** |ΔSTFT| ≤ 5% and |ΔLTFT| ≤ 5% from idle to 2500 RPM.
6. If trims exceed these bounds, the fuel control system is compensating — do not call no_fault.

### 5.5 O2 Sensor Dynamics Check (Mode $01)
1. At warm idle in closed loop, graph **oxygen sensor voltage** (PID 0x14 for Sensor 1 Bank 1, PID 0x15 for Sensor 2 Bank 1, etc.) over time.
2. Measure **transition time** from lean to rich and rich to lean (time to cross 0.45 V).
3. **Acceptable:** transition time < 150 ms.
4. **Amplitude check:** voltage should swing from < 0.2 V (lean) to > 0.8 V (rich).
5. If transition time > 150 ms or amplitude is reduced, the sensor is lazy — do not call no_fault.

### 5.6 Two-Point 5-Gas Check (if OBD data sparse)
1. At warm idle, record 5-gas values (HC, CO, CO2, O2, NOx).
2. Increase to **2500 RPM no load**, hold steady, record 5-gas values.
3. **Normative idle bands**【4DLab context】:
   - HC ≤ 35 ppm (≤ 50 tolerable)
   - CO: 0.1–0.45%
   - CO2: 14.5–16.0%
   - O2: low single digits (< 1.0% with working catalyst)
4. **Delta check:**
   - ΔHC ≤ +20 ppm
   - ΔCO ≤ +0.2%
   - ΔCO2 ≥ −0.5%
   - ΔO2 ≤ +0.5%
5. If any value falls outside these bands or any delta exceeds the limit, do not call no_fault.

---

## 6. Open Questions / Data Gaps

| Gap | Description | Minimal Collection Plan |
|-----|-------------|------------------------|
| **Mode $06 margin thresholds** | The 10% margin rule is empirical-anecdotal; no standardized threshold exists in SAE J1979 or ISO 15031-5 for "how much margin constitutes health." | Collect Mode $06 test values and limits from 100+ healthy vehicles across multiple makes/models. Compute distribution of margin values. Determine 5th percentile margin — use that as the minimum acceptable margin. |
| **Two-point gas delta thresholds** | The delta thresholds (ΔHC ≤ +20 ppm, etc.) are derived from workshop practice, not from a published standard. | Conduct controlled experiments on known-healthy vehicles (n ≥ 30) at idle and 2500 RPM. Measure 5-gas at both points. Compute mean and standard deviation of each delta. Set threshold at mean + 2σ. |
| **Fuel trim delta with air metering type** | The 4DLab context notes that air-metering type (speed-density vs. MAF) affects trim-delta behavior. The thresholds above assume MAF-based systems. | For speed-density (MAP-only) systems, collect trim data at idle and 2500 RPM. Determine whether the same ±5% delta threshold applies or whether a different threshold is needed. |
| **O2 sensor transition time by sensor type** | The 150 ms threshold is for traditional zirconia sensors. Wideband (air-fuel ratio) sensors have different dynamics. | Collect O2 sensor transition times for both narrowband and wideband sensors on known-healthy vehicles. Establish separate thresholds by sensor type. |
| **Readiness completeness vs. monitor count** | Different vehicles support different numbers of monitors; "all monitors complete" means different things for different vehicles. | Document the monitor set for each major vehicle platform (e.g., Toyota, Honda, Ford, GM, VW/Audi). Create a lookup table of supported monitors by platform. |

---



