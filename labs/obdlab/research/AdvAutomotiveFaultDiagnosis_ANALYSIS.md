---
title: "Advanced Automotive Fault Diagnosis (Denton) — Architect Viability Analysis"
author: "4DLab architect"
date: "2026-06-08"
source_doc: "labs/obdlab/research/Advanced Automotive Fault Diagnosis.txt (Tom Denton, 2nd ed., Elsevier 2006)"
companion: "AdvAutomotiveFaultDiagnosis_VIABLE_prepped.md (viable petrol extract: Ch2,4,5,6,7)"
scope_filter: "petrol 1990-2010; 4DLab ingests gas/DTC/freeze-frame/PID values for petrol-engine inference"
role: "architect — analysis only, no code, no ledger rows"
status: "analysis complete — dispositions are RECOMMENDATIONS"
verdict: "high-value: authoritative OBD/monitor/DTC-state structure book 1 lacked; ~6 net-new candidates"
---

# Advanced Automotive Fault Diagnosis (Denton) — Architect Viability Analysis

## What this is

Same procedure as the cardiagnosis pass: prep → chunk the **viable** chapters
(petrol 1990–2010) → study → judge each technique against what 4DLab can
diagnose → tag with a named consumer. **Architect deliverable only — no code, no
`*_tasks/` rows.** Viable extract: `AdvAutomotiveFaultDiagnosis_VIABLE_prepped.md`.

Unlike the cardiagnosis book (a corroboration asset), **Denton supplies the
authoritative *structural* layer 4DLab was missing**: the OBD monitor taxonomy,
the DTC-state machine, readiness-flag logic, the mandated freeze-frame parameter
set, and the adaptive fuel-trim model. These are exactly the spines of DTCLab
(Stage 3) and the COMLab fault-atlas (Stage 4).

## Scope frame (unchanged from cardiagnosis analysis)

4DLab does inference on *ingested* petrol data (no live comms, no bench
multimeter), idle-centric L1–L5, truth(gas)-vs-perception(ECU), strict
signal/noise (named consumer + code path or it doesn't ship). Denton is a UK
textbook squarely in the OBD2/EOBD era (US OBD2 1996, EOBD petrol 1 Jan 2001),
so its OBD content is directly on-era.

## Chapter scope verdict

| Chapter | In/Out | Why |
|---|---|---|
| 1 Introduction, 3 Tools & equipment | **OUT** | Workshop tools, safety, report-writing |
| 2 Diagnostic techniques | **IN (method)** | Fault-code logic, on/off-board, data sources |
| 4 Oscilloscope diagnostics | partial | Expected sensor/ignition/alternator behaviour useful; waveforms themselves OUT (4DLab ingests values, not traces) |
| **5 On-board diagnostics** | **IN — core** | Monitor taxonomy, DTC-state machine, readiness, freeze-frame, fuel-trim model — the net-new spine |
| 6 Sensors and actuators | **IN** | Sensor signal behaviour (largely corroborates) |
| 7 Engine systems | **IN (petrol)** | Fuel/ignition/emissions/EM/charging; **diesel 7.13–7.14 excluded**; cooling/lube partial |
| 8 Chassis, 10 Transmission, 11 Conclusion | **OUT** | Non-engine / out of L1–L5 |
| 9 Electrical | mostly OUT | 9.1–9.2 (components, CAN) context only; lighting/ICE/body/HVAC/airbags OUT |

## A. Net-new candidates (consumer nameable — author later, not now)

These are genuinely new to the 4DLab corpus and each names a consumer. They are
recommendations; nothing is registered.

1. **DTC-state machine — authoritative pin (DTCLab spine).**
   Denton §5.4.4 gives the exact lifecycle: a failure is stored as a **pending
   code immediately**, MIL **not** lit; MIL is illuminated on the **3rd
   consecutive driving cycle** in which the failure recurs → **confirmed**; MIL
   **heals after 3 subsequent clean driving cycles**; the code/distance/freeze-
   frame is **erased after ≥ 40 warm-up cycles** without recurrence. This *pins*
   cardiagnosis book 1's vague "~40 times" and is the precise weighting model for
   DTCLab's pending/confirmed/permanent states.
   *Consumer:* DTCLab DTC-state weighting → COMLab fault-atlas (state-weighted
   DTC confidence). *Disposition:* **PROPOSAL-CANDIDATE** for DTCLab Stage 3.

2. **Readiness-flag / monitor-status perception-trust gate (strong).**
   §5.4.6: each monitor carries a **Ready / Not-Ready** flag; continuous monitors
   = misfire + fuel-system; others run only under preconditions; flags reset to
   Not-Ready on **battery disconnect or scan-tool clear**; MY1996–2000 may have 2
   flags Not-Ready, 2001+ only 1, before a valid test. The 4DLab-viable use: **do
   not trust a monitor's "no fault" when its readiness = Not-Ready**, and flag
   battery-disconnect-reset state (explains "all clear" that is actually
   untested). *Consumer:* OBDLab `analytics_preconditions` / monitor-readiness
   gate (same family as `T-OBDV2-6`) → COMLab confidence weighting.
   *Disposition:* **PROPOSAL-CANDIDATE** — likely a precondition/trust flag, not a
   verdict field. Supersedes/augments cardiagnosis candidate **B3** (EVAP 15–85 %),
   which Denton confirms is one of several readiness preconditions
   (EVAP = temperature + fuel-fill constraints).

3. **Freeze-frame parameter set — authoritative pin (DTCLab L4).**
   §5.4.4 mandates the stored set: **calculated/derived load, engine speed,
   STFT/LTFT, fuel pressure, vehicle speed, coolant temp, intake-manifold
   pressure, open/closed-loop status, and the triggering DTC.** This is exactly
   the L4 freeze-frame schema DTCLab needs — pin it from here.
   *Consumer:* DTCLab freeze-frame params → COMLab fusion (FF-conditioned
   routing). *Disposition:* **PROPOSAL-CANDIDATE** for DTCLab Stage 3.

4. **Misfire severity model (Type A / Type B) + idle threshold (idle-relevant).**
   §5.3.9: **Type A** = catalyst-damaging rate (MIL **flashes 1 Hz**); **Type B**
   = emissions-exceeding rate. Rate-to-damage is load-dependent: **~45 % misfire
   at neutral idle**, falling to **~5 % at 80 % load / 4000 rpm**; EU monitors
   **≤ 4500 rpm**; "similar conditions" for re-flag = **±375 rpm, ±20 % load,
   same warm-up**. Because 4DLab is **idle-centric**, the ~45 %-at-idle
   catalyst-damage threshold and the Type-A flashing-MIL distinction are directly
   usable to grade misfire severity. *Consumer:* COMLab misfire-severity fusion +
   DTCLab (pairs with EP-OBD-IN-07 misfire, unallocated `T-OBDV2-9/10`); GASLab
   `COMBUSTION_FAIL` is the truth side. *Disposition:* **PROPOSAL-CANDIDATE**.

5. **Catalyst-efficiency monitor pattern (pre/post-O2 correlation).**
   §5.3.6: catalyst health is inferred from **oxygen storage** — a healthy cat
   makes the downstream O2 quiet; as it degrades the **downstream sensor begins
   to mirror the upstream** (P0420 family). 4DLab already models downstream-O2
   masking (`T-OBDV2-3`) and has GASLab gas truth. *Consumer:* COMLab
   catalyst-efficiency fault-atlas node cross-referencing downstream-mirror +
   GASLab post-cat chemistry. *Disposition:* **PROPOSAL-CANDIDATE**, but note the
   classic monitor needs cruise data; the **4DLab-viable form is the post-cat
   chemistry cross-check at idle**, not the drive-cycle correlation.

6. **FMEM / limp-home perception-trust flag (concept).**
   §5.2.1: on a sensor fault the ECU substitutes a **safe default value (FMEM)**.
   A PID reading under FMEM is not a real measurement → OBDLab perception of it
   should be down-trusted. *Consumer:* OBDLab perception-trust / `analytics_
   preconditions` → COMLab. *Disposition:* **PROPOSAL-CANDIDATE (weak)** — viable
   only if FMEM state is detectable from available PIDs/DTCs; otherwise DEFER.

## B. Corroborations (cite Denton against existing work; no new proposal)

| Denton technique | Corroborates |
|---|---|
| Adaptive fuel-trim model: STFT instantaneous, **LTFT learned/stored, robust to battery, reset only by tech**; fuel-mass = (air-mass × LTFT)/(STFT × **14.64**); LTFT-limit ⇒ fuel-system DTC | OBDLab trim channels (`BANK-ASYM-1`, trim analytics), COMLab fusion |
| Rationality testing: sensor vs **mapped value normalised by rpm/throttle** (MAF example) | OBDLab `DUAL_MAF_MAP_CROSSCHECK` / VE gate (`T-OBDV2-2`) |
| O2 monitor failure modes: **stuck lean/rich**, **slowed/lazy = reduced amplitude+frequency**; zirconia **0.6–0.8 V rich** | OBDLab `o2_failure_mode` (LAZY_SWITCHING/BIASED); cardiagnosis A2 |
| EVAP monitor: temperature + **fuel-fill** constraints; EU not required | cardiagnosis B3 / EVAP precondition |
| Warm-up cycle = **coolant +22 °C and ≥ 70 °C** | The ≥75 °C measurement-condition / CTS candidate **B2** (book 1) |
| EGR monitor (DPFE differential-pressure / AFR-excursion / temperature methods) | cardiagnosis EGR (DTCLab P040x) |
| Ignition fault table (erratic idle→plug gap/timing; misfire-at-idle→coil/cap; pinking→timing/knock) | cardiagnosis misfire; SymptomLab prior (weak) |

## C. Defer / Out

- **Secondary-air monitor** (§5.3.11) — cold-start light-off system (~260 °C cat
  light-off); 4DLab measures at ≥75 °C, no cold-start capture. **DEFER.**
- **Oscilloscope waveforms** (Ch4: ignition primary/secondary, alternator ripple,
  relative-compression cranking amps, CAN-H/L) — 4DLab ingests *values*, not
  traces. The *expected behaviours* are reference only. **OUT as technique**
  (alternator-ripple links weakly to existing `T-OBDV2-8` VPWR/`EP-FA-05`).
- **Bench electrical tests** (coil 1.5–3 Ω / 5–10 kΩ, plug 400–900 °C, gap
  0.6–1.2 mm, DLC pinout) — no resistance probe, no live socket. **OUT.**
- **EOBD g/km emission-limit tables** (Euro III/IV) — drive-cycle mass limits,
  not idle ppm; not 4DLab idle-gas scope. **Reference only.**
- Diesel injection (7.13–7.14), chassis (8), transmission (10), body/ICE/HVAC
  (9.3+). **OUT** (petrol-only / non-engine).

## D. Citeable thresholds harvested (reconcile to wiki before any code)

Numeric-literal rule: anything reaching `obdlab/`/`gaslab/` code needs a **wiki**
citation; Denton is corroboration — pin the shipping value from `OBDLab_KG_Wiki.md`.

- DTC state: pending immediately → **MIL on 3rd consecutive driving cycle** →
  **heal after 3 clean cycles** → **erase after ≥ 40 warm-up cycles**.
- Warm-up cycle: **coolant +22 °C from start AND ≥ 70 °C**.
- Monitor fault threshold: **1.5 × emission limit** (catalyst/misfire/O2).
- EVAP leak detection: **1 mm (0.040") 1996–1999**, **0.5 mm (0.020") post-2000**.
- Misfire: catalyst-damage **~45 % at idle → ~5 % at 80 % load/4000 rpm**; EU
  monitored **≤ 4500 rpm**; Type-A MIL **flash 1 Hz**; similar-cond **±375 rpm /
  ±20 % load**.
- Fuel model: AFR constant **14.64**; STFT (instant) vs LTFT (learned, battery-robust).
- O2 (zirconia narrowband): **0.6–0.8 V rich**, low V lean.
- Readiness allowance: **MY1996–2000 ≤ 2 Not-Ready; 2001+ ≤ 1 Not-Ready**.

## E. Cross-book reconciliation (important)

- **DTC-state "~40 cycles":** cardiagnosis said "~40 restarts"; Denton pins it as
  **≥ 40 warm-up cycles** (distinct from the **3 driving cycles** to confirm and
  **3** to heal). Use Denton's three-number model.
- **Warm/operating temp:** owner pinned 4DLab readings at **≥ 75 °C**; Denton's
  *warm-up cycle* minimum is **≥ 70 °C** (+22 °C rise). The ≥75 °C operating
  measurement sits safely above the 70 °C warm-up floor — consistent; B2's
  stuck-cold-while-warm logic holds.
- **O2 voltage:** cardiagnosis "0.1–0.9 V", Denton "0.6–0.8 V rich" — same sensor,
  different reporting band; treat as switch-around-0.45 V, rich-high.
- **AFR:** cardiagnosis "14.7:1" (stoich), Denton "14.64" (fuel-mass constant);
  both ~stoichiometric — keep 14.7 as the physical stoich, note 14.64 is Denton's
  trim-equation constant.

## F. Recommended next actions (future authoring sessions — NOT done here)

1. When **DTCLab (Stage 3)** opens: author the **DTC-state machine** (A1) and the
   **freeze-frame parameter set** (A3) from Denton §5.4.4 — these are spine specs,
   not optional.
2. Author the **readiness-flag perception-trust gate** (A2) as an OBDLab
   precondition proposal, absorbing cardiagnosis B3 (EVAP) as one precondition.
3. Author **misfire severity (Type A/B + 45 %-idle)** (A4) alongside the existing
   EP-OBD-IN-07 misfire promotion.
4. Evaluate the **catalyst-efficiency idle cross-check** (A5) at COMLab Stage 4
   against GASLab post-cat chemistry; keep it idle-form, not drive-cycle.
5. Attach Denton as a **citation source** to OBDLab trim tasks (`BANK-ASYM-1`),
   `T-OBDV2-2` (rationality), `T-OBDV2-3` (catalyst/downstream), and the misfire
   promotion.

> One-task-per-session: this analysis is the deliverable. No `*_tasks/` rows
> created or flipped. Net-new candidates A1–A6 are recommendations for separate
> authoring sessions, each with a named consumer per signal/noise.
