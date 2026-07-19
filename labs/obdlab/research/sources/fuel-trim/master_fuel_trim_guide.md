# Master Fuel Trim Guide — 4D Petrol Diagnostic Engine

**Purpose.** Define short-term and long-term fuel trim physics, sign convention, healthy operating ranges, idle-vs-cruise behaviour, trim-rail/sentinel values, and the decision tree that separates vacuum leak from fuel delivery from MAF contamination from EVAP fault. The engine cites this guide for every STFT/LTFT-derived symptom.

**Scope.** Petrol with closed-loop fuel control. Pre-1996 carburetted vehicles and pure GDI fuel pressure regulation are outside the trim-decision tree; for GDI cross-reference `master_fuel_system_guide.md` §6.

---

## 1. What fuel trim is

Fuel trim is the ECU's percentage adjustment to the base injector pulse width, compensating for deviations from the stoichiometric 14.7:1 AFR target. It is the ECU *learning* that the physical fuel-air system does not match its base map.

- **STFT — Short-Term Fuel Trim.** Moment-to-moment correction from upstream O₂ sensor feedback. Reacts in milliseconds. Oscillates rapidly between positive and negative as the ECU fine-tunes around stoichiometric. Think *acceleration*.
- **LTFT — Long-Term Fuel Trim.** Learned, averaged correction stored in non-volatile memory. Represents how much the fuel system deviates from base-map over time. Think *speed*. STFT corrections that persist transfer gradually to LTFT.

The two add: total trim = STFT + LTFT. The 4D engine evaluates total trim, not each in isolation.

---

## 2. Sign convention

| Sign | Meaning | What the ECU is doing |
|---|---|---|
| **Positive (+)** | System running lean | ECU is **adding** fuel |
| **Negative (−)** | System running rich | ECU is **subtracting** fuel |
| **0 %** | Perfect stoichiometric | No correction required |

Positive trim ⇔ engine is getting more air than the ECU expected (lean). Negative trim ⇔ engine is getting less air than expected, or extra fuel from somewhere unmetered (rich).

This sign convention is universal across all OBD-II vehicles per SAE J1979 PID `$06` (STFT B1) and `$07` (LTFT B1). Pre-OBD-II proprietary systems use opposite conventions on some Asian-market ECUs — flag `trim_sign_uncertain` if the vehicle is ≤ 1995.

---

## 3. Normal operating ranges

| Condition | STFT normal | LTFT normal | Total trim normal |
|---|---|---|---|
| Idle, warm, closed loop | −5 % to +5 % bouncing | −10 % to +10 % | within ±10 % |
| Steady cruise (60–100 km/h) | −5 % to +5 % bouncing | −10 % to +10 % | within ±10 % |
| Bank-to-bank match (V-engines) | within ±5 % between banks | within ±5 % between banks | — |

**DTC trigger thresholds:**

- LTFT ≈ +25 % sustained → P0171 (B1) or P0174 (B2) Type A.
- LTFT ≈ −25 % sustained → P0172 (B1) or P0175 (B2) Type A.
- ±127 % is the absolute register limit (signed 8-bit). A pegged value means "very large deviation, exact magnitude meaningless".

Values within ±10 % total are healthy; ±10 % to ±20 % is investigational; > ±20 % is a confirmed mixture problem.

---

## 4. Trim-pattern decision tree — the highest-leverage rule in the trim domain

This table is the single most diagnostic rule in fuel trim. Source: synthesised from `cases/library/automotive/mix/Ross-Tech_ VAG-COM_ Fuel Trim Info.pdf`, `Short Term Long Term Fuel Trim Explained.pdf`, and `Fuel trim can be a valuable diagnostic tool - Eastern Manufacturing.pdf`.

| Pattern | LTFT at idle | LTFT at 2500–3000 RPM | Root cause | Why |
|---|---|---|---|---|
| **Vacuum leak** | High positive (+15 % to +25 %) | Drops toward normal | Unmetered air leak post-MAF | At idle, leak is large % of total airflow; at cruise leak is a small %, so trim normalises |
| **Fuel delivery** | Moderate positive | **Worsens** (more positive) | Weak pump, clogged filter, low pressure | Fuel demand rises with RPM; pump cannot keep up |
| **MAF under-reading (contaminated)** | Positive at idle | Negative under load | Dirty hot-wire MAF | At high airflow, contamination insulates the wire → reads low → ECU enriches |
| **MAF over-reading** | Negative at idle | More negative under load | Faulty MAF, water in airbox | ECU sees inflated airflow → injects excess fuel |
| **Leaking injector** | Negative on **one bank** | Negative persists | Dripping injector on that bank | One-bank only; raw fuel enters regardless of airflow |
| **Stuck-open EVAP purge** | Negative at idle | Normalises at cruise | Purge valve stuck open | At idle, vapour is large % of total fuel; at cruise it dilutes |
| **High fuel pressure** | Negative at idle and cruise | Negative persists | Pinched return line, faulty FPR | Constant excess fuel delivery |
| **Stuck-open EGR** | High positive | Normalises at cruise | EGR valve stuck open | EGR dilution mimics vacuum leak (cross-ref `master_gas_guide.md §3 rule 6`) |
| **Exhaust leak before pre-cat O₂** | Positive (false-lean) | Persists | Exhaust manifold gasket, broken weld | False O₂ feedback drives ECU to add fuel |
| **Worn engine (low compression)** | Slight positive, often noisy | Slightly positive | Compression loss → leaner effective burn | Trims drift positive but not far; cross-ref `master_mechanical_guide.md` §6 |

**The "Three-Speed Test" (Proposal B §3):** Measure trims at idle, 2500 RPM, and 3000 RPM (or under load via decel). The RPM-dependence of the trim is the discriminator — values themselves are secondary.

---

## 5. Bank-to-bank comparison (V-engines and inline-six with two pre-cat O₂)

The single most powerful test on V-engines:

- **Both banks show the same deviation (within ±5 %):** common-mode cause — MAF, fuel pump, fuel pressure, EVAP, intake plenum leak, exhaust manifold leak feeding both pre-cat O₂ sensors.
- **Only one bank deviates:** bank-specific cause — intake-port gasket on that bank, single clogged or leaking injector, single-bank fuel rail issue, single-bank O₂ sensor bias.
- **Banks deviate in *opposite* directions:** rare — usually a swapped O₂ harness or a single failing wideband. Treat as `o2_sensor_swap_suspected` and cross-ref `master_o2_sensor_guide.md`.

---

## 6. Trim rails and sentinels

- **±25 %:** Typical OBD-II DTC trigger point. Beyond this, the ECU stops learning.
- **±127 %:** Absolute register maximum. Treat as "very large, magnitude unknown".
- **Frozen at last value:** During open-loop operation (cold-start, WOT, decel-fuel-cut, O₂ fault), the ECU does not update trims. Per `master_cold_start_guide.md §1`, do **not** interpret trim values when `fuel_sys_status = OL` (open loop).
- **Reset to zero:** After codes cleared or battery disconnect, LTFT resets. The engine relearns over ~1 drive cycle. Do not draw conclusions from trim < 1 drive cycle after `codes_cleared = true`.

---

## 7. Trim direction vs gas chemistry — the cross-check rule

The 4D Truth-vs-Perception override (`PRD_4D_App.md §5`): when fuel trim and gas chemistry disagree, gas chemistry (Brettschneider lambda from analyser) is ground truth, trim is *what the ECU thinks is happening*.

| Gas λ | Trim direction | Verdict |
|---|---|---|
| ≤ 0.95 (rich) | Negative | Agreement — real rich condition |
| ≤ 0.95 (rich) | Positive | **Contradiction** — ECU is over-fuelling because pre-cat O₂ reads lean. Suspect O₂ sensor bias or exhaust leak before sensor (`master_o2_sensor_guide.md §6`) |
| ≥ 1.05 (lean) | Positive | Agreement — real lean condition |
| ≥ 1.05 (lean) | Negative | **Contradiction** — ECU subtracting fuel because pre-cat O₂ reads rich. Suspect O₂ silicone poisoning or wideband sensor bias |
| 0.97–1.03 (stoich) | Within ±10 % | Healthy |
| 0.97–1.03 (stoich) | > ±15 % | ECU fighting an unknown disturbance — suspect `ECU_Logic_Inversion` or a sensor with biased reference |

---

## 8. Procedure for the 4D app user

1. Confirm closed loop: read `fuel_sys_status` PID. Must equal CL (closed loop) for trim values to be meaningful.
2. Warm engine to ECT ≥ ~80 °C.
3. Record STFT and LTFT for both banks at idle.
4. Raise to steady 2500–3000 RPM (or hold at 60–80 km/h cruise). Record again.
5. Map the pattern against §4 decision tree.
6. If all trims within ±10 % and both banks match, the fuel-control system is fine — look for the fault elsewhere (gas chemistry, mechanical, ignition).

---

## 9. Pre-conditions for valid trim interpretation

The 4D engine must validate these before consuming fuel-trim symptoms:

- ECT ≥ 70 °C (cold-start enrichment masks real trims).
- `fuel_sys_status = CL` (closed loop).
- No active P0130–P0161 (O₂ sensor faults invalidate trims).
- No active P0335 or P0340 (CKP/CMP failure → batch fire / open loop).
- Time since last `codes_cleared = true`: ≥ 1 drive cycle.
- WOT not engaged (open-loop power enrichment).
- DFCO not active (fuel cut → no trim update).

If any precondition fails, the engine flags `fuel_trim_invalid` and demotes all trim-derived candidates.

---

## 10. Citations

- SAE J1979 — PID `$06` (STFT B1), `$07` (LTFT B1), `$08` (STFT B2), `$09` (LTFT B2).
- `cases/library/automotive/mix/Ross-Tech_ VAG-COM_ Fuel Trim Info.pdf` — VAG-specific trim ranges and cross-checked against generic.
- `cases/library/automotive/mix/Short Term Long Term Fuel Trim Explained.pdf` — STFT vs LTFT physics, 'acceleration vs speed' analogy.
- `cases/library/automotive/mix/Fuel trim can be a valuable diagnostic tool - Eastern Manufacturing.pdf` — three-speed test methodology.
- `cases/library/automotive/mix/extracted/Fuel Trim Info - Ross-Tech Wiki.md` — cleaned markdown for grep.
- `cases/library/automotive/mix/fuel-trim-analysis.md` — already-extracted summary.
- Cross-ref: `master_obd_guide.md §5.1` and §5.2 (lean/rich DTC mapping); `master_gas_guide.md §3 rule 7` (truth-vs-perception override).
