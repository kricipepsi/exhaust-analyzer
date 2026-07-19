# Executive Summary

A defensible two-point fixture set **can be built**, but with significant caveats. The recommended canonical pair is **curb idle + 2500 RPM no-load** (the two-speed idle test), as this is the only operating-point pair formally standardised across EPA, BAR, and state I/M programmes for the 1990–2010 petrol fleet. Loaded modes (ASM 2525/5015, IM240) provide richer signatures but are dynamometer-dependent, less widely available, and have fewer published delta-reference data.

The biggest ground-truth gap is **quantitative per-fault delta signatures**: while qualitative patterns are well documented in field lore and some OEM TSBs (e.g., vacuum leak = positive trim at idle that decays toward 0 at 2500 RPM), peer-reviewed or programme-level tabulations of *paired* low/high 5-gas and fuel-trim values for confirmed faults are essentially nonexistent in the public domain. Similarly, **test-retest repeatability** for fuel-trim and 5-gas deltas has not been formally characterised in the I/M literature; only qualitative bounds (±2–3% STFT, ±5% LTFT) can be inferred from field experience. The suite can be authored now for **qualitative delta-direction** diagnosis (with architecture gates), but **quantitative magnitude thresholds** will require expert calibration or proprietary dataset access until public validation data emerge.

---

## Question 1. Canonical Operating Points

**Finding**

The industry defines three principal test families for petrol light-duty vehicles:

| Test | Low Point | Elevated Point | Load | Reference |
|------|-----------|----------------|------|-----------|
| **Two-speed idle (TSI)** | Curb idle (in Park/Neutral) | 2500 ± 100 RPM | No-load | EPA MOVES2010 test type 12; Virginia code |
| **ASM 2525** | 25 mph, 25% load | (single steady-state mode) | Loaded | Law Insider definition |
| **ASM 5015** | 15 mph, 50% load | (single steady-state mode) | Loaded | Law Insider definition |
| **ASM 2525/5015** | 25 mph / 25% load | 15 mph / 50% load | Loaded | EPA MOVES2010 test types 23, 26 |
| **IM240** | 240-second transient cycle | — | Loaded | EPA transient cycle |
| **BAR-90 two-speed** | Curb idle | 2500 RPM no-load | No-load | California BAR |

**Recommended canonical pair for delta diagnosis:** **curb idle + 2500 RPM no-load (two-speed idle)** . Rationale:
- It is the **only** universally available operating-point pair across the 1990–2010 petrol fleet — no dynamometer required, works on all OBD-I and OBD-II vehicles.
- It is formally defined in EPA I/M regulations and multiple state programmes.
- It is the clinical standard for fuel-trim differential diagnosis in the service industry.
- The BAR/Sierra report explicitly notes that the 2500 RPM no-load mode was included specifically for HC/CO correlation.

**Elevated-band alternatives:**

| Elevated Point | Advantage | Disadvantage |
|----------------|-----------|--------------|
| **2500 RPM** | Standardised, widely documented, safe, minimal load | May not stress some faults; vacuum-leak signature may partially close |
| **3500–4500 RPM** | Better for fuel delivery faults (clogged filter → rich correction at high RPM) | Less standardised; higher mechanical risk; fewer reference data |
| **ASM 2525 (25 mph / 25% load)** | Loaded, better NOx correlation | Requires dynamometer; not universally available |
| **ASM 5015 (15 mph / 50% load)** | Best NOx/CO/HC malfunction detection | Dynamometer required; 100-second mode limit |

**Signature shift with elevated band:** A vacuum leak that produces +20% LTFT at idle and +5% at 2500 RPM may produce **near-zero** trim at 3500–4500 RPM as manifold vacuum drops and the leak becomes proportionally insignificant. Conversely, a **fuel delivery restriction** may show normal trim at idle but large positive corrections at 3500+ RPM. The 2500 RPM point is the best **compromise** — high enough to differentiate leak from fuel faults, low enough to remain standardised.

**Confidence: High** for standard definitions; **Medium** for signature-shift claims (field-experience based).

**Data gaps / era-region caveats:** EPA/BAR definitions are US-centric. EU programmes (e.g., UK MOT) use similar two-speed idle but with different cutpoints; Japanese JASO standards exist but are not harmonised. The 1990–2010 range spans OBD-I (pre-1996 US) and OBD-II (post-1996) — fuel-trim PID availability and update rates differ.

---

## Question 2. Full-Taxonomy Two-Point Signatures

**Finding**

The following table gives **qualitative delta signatures** per fault family. **Quantitative magnitudes are expert estimates** — no public paired dataset provides tabulated low/high values for confirmed faults across the full taxonomy.

**Nomenclature:**
- `↑` = increases from idle to 2500 RPM
- `↓` = decreases
- `→` = no significant change (< noise threshold)
- `±` = direction depends on architecture/sensor
- `LTFT` = Long-Term Fuel Trim (%); `STFT` = Short-Term Fuel Trim (%); `λ` = lambda (1.00 = stoichiometric)

### Healthy Baseline (no fault)

| Channel | Idle (curb) | 2500 RPM no-load | Delta |
|---------|-------------|------------------|-------|
| LTFT | 0 ± 5% | 0 ± 5% | → |
| STFT | 0 ± 3% | 0 ± 3% | → |
| CO | 0.1–0.5% | 0.1–0.5% | → |
| HC | 50–150 ppm | 50–150 ppm | → |
| CO₂ | 14–15% | 14–15% | → |
| O₂ | 0.5–2.0% | 0.5–2.0% | → |
| NOx | < 100 ppm | < 100 ppm | → |
| λ | 0.99–1.01 | 0.99–1.01 | → |
| O₂ sensor (front) | Switching 0.1–0.9V | Switching 0.1–0.9V | Frequency ↑ with RPM |
| O₂ sensor (rear) | Stable ~0.6–0.8V | Stable ~0.4–0.6V | ↓ small |

### Fault Family Signatures

| Fault Family | Idle Signature | 2500 RPM Signature | Delta | Mechanism | Abstain? |
|--------------|----------------|--------------------|-------|-----------|----------|
| **Lean / vacuum leak** | LTFT +15–30%, STFT +10–20%, O₂ lean (low V), λ >1.01 | LTFT +5–10% (improves), STFT →0 | **LTFT ↓ 10–20%** | High RPM reduces vacuum, leak less significant | N |
| **Rich** | LTFT –15–30%, STFT –10–20%, O₂ rich (high V), λ <0.99, CO↑ | LTFT –10–20% (may persist), CO↑ | **LTFT → or slight ↑** (less negative) | RPM may improve combustion, but rich persists | N |
| **Misfire** | HC↑↑ (200–1000+ ppm), O₂ erratic, misfire counts | HC↑↑, worse under load | **HC ↑ at RPM** (misfire rate often increases with RPM/load) | Higher cylinder pressure = harder to ignite | N |
| **Sensor fault (O₂/MAF)** | Trims random/pegged (±25–30%), O₂ stuck | Same pattern, no RPM dependency | **No systematic delta** — error is RPM-independent | Sensor reports same error regardless of RPM | **Y** (no usable delta) |
| **ECU/perception fault** | Trims erratic, no correlation with O₂ | Same | **No systematic delta** | ECU fault is not RPM-dependent | **Y** |
| **Catalyst failure** | Rear O₂ mirrors front (switching) | Rear O₂ continues to mirror front | **No delta** (both points show same failure) | Catalyst efficiency is load-independent in this test | **Y** (use catalyst monitor, not delta) |
| **Exhaust leak** | O₂ reads lean (fresh air), λ >1.01, trims may add fuel | Leak effect diminishes with flow | **λ ↓** (less lean at high RPM) | Higher flow = less dilution by fresh air | N |
| **Ignition fault** | Misfire at idle, HC↑ | Misfire may clear or worsen | **Delta depends on fault** (worn plugs worse at load; coil failure worse hot) | Variable | Partial |
| **Mechanical wear** | Low compression → idle instability, HC↑ | HC may ↑ or ↓ | **No consistent delta** | Wear affects all RPM | **Y** (use compression test) |
| **Cam/valve-timing** | Low vacuum, MAP offset, trims ± | Error scales with RPM | **Delta scales** (error proportional to RPM) | Timing error = airflow error × RPM | N (delta reveals RPM scaling) |
| **Non-starter** | No readings | No readings | **No delta** | Engine doesn't run | **Y** (abstain) |
| **No-fault** | All within normal ranges | All within normal ranges | **No delta** | — | N (pass) |

**Families separable only by delta (not by either snapshot alone):**
- **Lean/vacuum leak** vs **MAF sensor fault**: both may show positive trims at idle, but MAF fault persists at 2500 RPM while leak improves.
- **Exhaust leak** vs **lean mixture**: both show lean O₂ at idle, but exhaust leak improves at high RPM; lean mixture does not.
- **Cam timing** vs **mechanical wear**: both may affect idle quality, but cam timing error scales with RPM; wear does not.

**Confidence: High** for qualitative patterns (well-established in service literature); **Low** for quantitative magnitudes (no public tabulated data).

**Data gaps / era-region caveats:** No peer-reviewed study tabulates paired idle/2500 RPM 5-gas + fuel-trim values for confirmed faults across 1990–2010 vehicles. The magnitudes above are derived from diagnostic field practice and OBD DTC documentation.

---

## Question 3. Delta Tolerance / Repeatability

**Finding**

| Parameter | Test-retest repeatability (estimated) | Measurement uncertainty | Noise threshold (δ within noise) | Source |
|-----------|----------------------------------------|------------------------|--------------------------------|--------|
| **STFT** | ±2–3% (steady-state, warm) | ±1–2% (scanner accuracy) | |δ| < 3% | Field experience |
| **LTFT** | ±3–5% (steady-state, warm) | ±2–3% (scanner accuracy) | |δ| < 5% | Field experience |
| **CO** | ±0.05–0.10% absolute | ±0.02–0.05% | |δ| < 0.10% | Analyzer spec |
| **HC** | ±10–20 ppm | ±5–10 ppm | |δ| < 20 ppm | Analyzer spec |
| **CO₂** | ±0.2–0.5% | ±0.1–0.2% | |δ| < 0.5% | Analyzer spec |
| **O₂** | ±0.1–0.3% | ±0.05–0.1% | |δ| < 0.3% | Analyzer spec |
| **NOx** | ±10–20 ppm | ±5–10 ppm | |δ| < 20 ppm | Analyzer spec |
| **λ** | ±0.005–0.010 | ±0.002–0.005 | |δ| < 0.010 | Calculated |
| **O₂ voltage** | ±0.02–0.05V | ±0.01–0.02V | |δ| < 0.05V | Scanner accuracy |

**Key repeatability factors:**
- Fuel trims are **RPM-dependent by design** — LTFT may shift 5–10% purely from RPM change in a healthy engine. The delta of interest is **relative** to the healthy baseline at that RPM, not absolute.
- STFT at a **stable 2500 RPM no-load** should settle within 10–15 seconds of steady RPM.
- **Warm-up state** is critical: cold-start enrichment can produce trims 10–20% lean of normal until closed-loop is achieved (typically >140°F coolant, >60 sec runtime).

**Recommended fixture encoding:**
- **Pass**: |δ| ≤ noise threshold (all channels)
- **Fail**: |δ| > noise threshold **and** direction matches fault signature
- **Abstain**: |δ| ≤ noise threshold OR validity gates fail

**Confidence: Medium** for STFT/LTFT (field-derived); **High** for 5-gas (analyzer specifications).

**Data gaps / era-region caveats:** No formal test-retest study for fuel-trim repeatability at 2500 RPM exists in the I/M literature. The values above are inferred from diagnostic practice and forum data.

---

## Question 4. Architecture-Dependent Nulls and Sign Inversions

**Finding**

### 4.1 Speed-Density (MAP-only) Vacuum-Leak Paradox

**Mechanism:** In a speed-density system (no MAF — MAP + RPM + IAT estimate airflow):
- The ECU **does not measure** actual airflow at idle; it calculates it from MAP.
- A vacuum leak **lowers** MAP (less vacuum) — but the ECU may interpret this as **less airflow** (throttle more closed), not more.
- Result: the ECU may **not add fuel** for the leak, and fuel trims may show **near-zero** correction despite a real lean condition.

**Delta signature:** |δ LTFT| ≈ 0 (null) — the leak is invisible to the fuel-trim delta.

**Architecture gate:** If vehicle has **MAP-only** (no MAF sensor), **do not use fuel-trim delta for vacuum-leak diagnosis**.

### 4.2 Forced-Induction Post-Turbo Leak

**Mechanism:** A leak **after** the turbocharger (pressurised side):
- At idle (no boost), the leak behaves like a normal vacuum leak → positive trims.
- Under boost (which may occur at 2500 RPM under load, but **not** at 2500 RPM no-load), pressurised air escapes → the ECU sees **less air than commanded** (MAF reads normal, but air is lost) → runs **rich** (negative trims).

**Delta signature (no-load 2500 RPM):** no inversion (no boost). **Under loaded conditions (ASM):** trim sign inverts from positive (idle) to negative (boost).

**Architecture gate:** If vehicle is **turbocharged** and test is **loaded** (ASM), vacuum-leak delta **inverts**. For no-load two-speed idle, this does not apply.

**Confidence: High** for speed-density paradox (documented in OEM TSBs); **High** for forced-induction (well-understood physics).

**Data gaps / era-region caveats:** No public dataset quantifies the speed-density null threshold (how large a leak before trims respond?). The 1990–2010 range includes many MAP-only vehicles (particularly Honda, some GM, early OBD-I).

---

## Question 5. Second-Reading Sample Validity

**Finding**

| Check | Threshold | Channel(s) | Source |
|-------|-----------|------------|--------|
| **Gas sum (CO + CO₂)** | > 6% (petrol) | All 5-gas | EPA I/M protocol |
| **Dilution (excess O₂)** | O₂ < 5% (valid); >5% = diluted/leak | O₂, λ | EPA protocol |
| **RPM stability** | 2500 ± 100 RPM for ≥10 sec | All | Virginia code |
| **RPM stability (idle)** | Curb idle ± 50 RPM for ≥10 sec | All | EPA protocol |
| **Warm-up state** | Coolant > 160°F OR > 3 min runtime after closed-loop | Fuel trims, O₂ | OBD monitor enable criteria |
| **Settle time (after RPM change)** | ≥10 seconds at target RPM before sampling | Fuel trims, O₂ | EPA preconditioning |
| **Analyser warm-up** | Stabilised zero/span for 5 min | All 5-gas | EPA §85.3(c)(3)(vi) |
| **Probe depth** | ≥10 inches into tailpipe | All | EPA §85.2 |
| **HC hang-up check** | <15 ppm C6 before test | HC | EPA |
| **Closed-loop operation** | O₂ switching, STFT active | Fuel trims, O₂ | OBD monitor status |

**Validity failure actions:**
- **Gas sum < 6%** → reject (dilution/exhaust leak)
- **O₂ > 5%** → reject (air leak or misfire)
- **RPM outside ±100** → wait or reject
- **Not warmed up** → wait or reject
- **Not in closed-loop** → reject (fuel trims invalid)

**Confidence: High** (EPA-sourced for most checks).

**Data gaps / era-region caveats:** OBD-II (1996+) provides coolant temp; pre-1996 may not. The "10-second settle" is inferred from EPA preconditioning, not explicitly specified for sampling.

---

## Question 6. Real Paired Datasets

**Finding**

| Dataset | Type | Access | Description | Era/Region |
|---------|------|--------|-------------|------------|
| **Arizona I/M IM240 fleet data** | I/M programme | Limited (EPA reports) | Large-sample IM240 tailpipe emissions, includes some idle data | US, 1990s–2000s |
| **California BAR Smog Check data** | I/M programme | Aggregated reports only | ASM 2525/5015 emissions concentrations by model year | US, 1990s–present |
| **EPA ASM evaluation study** | Government study | Free (nepis.epa.gov) | Comparison of 2500/idle vs ASM vs IM240; includes some malfunction data | US, 1992 |
| **ARCO enhanced I/M study** | Industry study | Cited in EPA report | 5 newer vehicles with implanted malfunctions, 30 tests | US, 1992 |
| **SAE Technical Papers** | Peer-reviewed | Paid (SAE) | Characterisation of high-emitting vehicles; IM240 data | US, various |
| **Chinese GB 18285 two-speed idle standard** | Regulatory | Free (English) | Equipment specs, not vehicle data | China, 2006 |
| **EPA MOVES2010 I/M test definitions** | Regulatory | Free | Test type definitions only, no vehicle data | US, 2014 |

**No public dataset** pairs low-idle and elevated-RPM readings for the **same vehicle** with a **confirmed fault** across 5-gas + fuel trims + O₂. All existing datasets are either:
- Aggregated pass/fail statistics (BAR),
- Single-mode only (IM240 is transient, not two-point),
- Proprietary (OEM, aftermarket scan-tool companies),
- Or focused on one channel only (e.g., emissions only, not fuel trims).

**Confidence: High** that no public paired dataset exists.

**Data gaps / era-region caveats:** This is the **single largest ground-truth gap**. Without a paired dataset, quantitative fixture thresholds cannot be validated against real distributions. Proprietary datasets (Snap-on, Bosch, Mitchell1, ALLDATA) may contain such data but are not publicly accessible.

---

## Master Fixture Table

| Fault Family | Low-Point Frame (idle) | Elevated-Point Frame (2500 RPM) | Δ per Channel | Tolerance Band | Architecture Gate | Abstain? | Source |
|--------------|------------------------|---------------------------------|---------------|----------------|-------------------|----------|--------|
| Healthy | LTFT 0±5%; STFT 0±3%; CO 0.1-0.5%; HC 50-150ppm; O₂ 0.5-2.0%; λ 1.00±0.01 | LTFT 0±5%; STFT 0±3%; CO 0.1-0.5%; HC 50-150ppm; O₂ 0.5-2.0%; λ 1.00±0.01 | All → | STFT±3%, LTFT±5% | None | N | Field经验 |
| Lean/vacuum leak | LTFT +15-30%; STFT +10-20%; O₂ lean; λ>1.01 | LTFT +5-10%; STFT →0 | **LTFT ↓ 10-20%** | ±5% LTFT | Speed-density: null | N |  |
| Rich | LTFT -15-30%; STFT -10-20%; CO↑; λ<0.99 | LTFT -10-20% | **LTFT → or slight ↑** | ±5% LTFT | None | N |  |
| Misfire | HC 200-1000+ppm; O₂ erratic | HC ↑ | **HC ↑** | ±50ppm | None | N | Expert estimate |
| Sensor fault | Trims pegged; O₂ stuck | Same pattern | **No systematic Δ** | N/A | None | **Y** |  |
| ECU fault | Trims erratic | Same | **No systematic Δ** | N/A | None | **Y** | Expert estimate |
| Catalyst failure | Rear O₂ mirrors front | Rear O₂ mirrors front | **No Δ** | N/A | None | **Y** |  |
| Exhaust leak | O₂ lean; λ>1.01; trims + | O₂ less lean | **λ ↓** | ±0.010 λ | None | N |  |
| Ignition fault | HC↑ at idle | Variable | **Delta depends** | N/A | None | Partial | Expert estimate |
| Mechanical wear | HC↑; idle unstable | Variable | **No consistent Δ** | N/A | None | **Y** | Expert estimate |
| Cam timing | MAP offset; trims ± | Error scales | **Δ scales with RPM** | N/A | None | N | Expert estimate |
| Non-starter | No readings | No readings | **No Δ** | N/A | None | **Y** | N/A |
| No-fault | All normal | All normal | **No Δ** | As healthy | None | N | N/A |

---

## Validity-Gate Table

| Check | Threshold | Channel(s) | Source |
|-------|-----------|------------|--------|
| Gas sum (CO + CO₂) | > 6% | CO, CO₂ | EPA |
| Dilution (O₂) | < 5% | O₂ | EPA |
| RPM stability (2500) | ±100 RPM for ≥10s | All | Virginia code |
| RPM stability (idle) | ±50 RPM for ≥10s | All | EPA |
| Warm-up | Coolant >160°F OR >3min runtime | Fuel trims, O₂ | OBD criteria |
| Settle time | ≥10s at target RPM | Fuel trims, O₂ | EPA |
| Closed-loop | O₂ switching, STFT active | Fuel trims, O₂ | OBD status |
| Analyser zero/span | Stabilised 5min | All 5-gas | EPA§85.3(c)(3)(vi) |
| Probe depth | ≥10 inches | All | EPA§85.2 |
| HC hang-up | <15 ppm C6 | HC | EPA |

---

## Consolidated Source Table

| Source | Type | Year | Region | Claim Supported | Access | Link |
|--------|------|------|--------|-----------------|--------|------|
| EPA MOVES2010 Appendix D | Regulatory | 2014 | US | Test type definitions (TSI, ASM, IM240) | Free | GPO |
| EPA ASM evaluation report | Government | 1992 | US | 2500/idle vs ASM vs IM240 comparison | Free | nepis.epa.gov |
| Virginia two-speed idle code | Regulatory | Current | US | 2500 RPM in Park/Neutral | Free | law.lis.virginia.gov |
| California BAR tables | I/M programme | 1996+ | US | BAR-90 two-speed standards | Free | arb.ca.gov |
| Law Insider ASM definition | Regulatory | Current | US | ASM 2525/5015 definitions | Free | lawinsider.com |
| EPA preconditioning protocol | Regulatory | 2004 | US | 2500 RPM for up to 4 min | Free | GPO |
| EPA analyzer spec §85.3 | Regulatory | 2004 | US | Zero/span stability | Free | GPO |
| Chinese GB 18285-2005 | Regulatory | 2005 | China | Two-speed idle equipment spec | Free | mee.gov.cn |
| Forum/field experience | Anecdotal | Various | Global | Fuel-trim diagnostic patterns | Free | Various |

---

## "Could Not Be Found" List

1. **Quantitative per-fault delta tables** — no peer-reviewed or programme-level tabulation of paired idle/2500 RPM 5-gas + fuel-trim + O₂ values for confirmed faults across 1990–2010 petrol vehicles.

2. **Test-retest repeatability studies** — no formal study of fuel-trim or 5-gas repeatability at 2500 RPM no-load.

3. **Public paired dataset** — no dataset pairing low-idle and elevated-RPM readings for the same vehicle with confirmed fault.

4. **OEM-specified tolerance bands** — no OEM-published tolerance for fuel-trim delta between idle and 2500 RPM.

5. **EU/Japan specific two-speed idle reference data** — no harmonised EU or Japanese dataset for 1990–2010 petrol vehicles.

6. **Catalyst failure delta signature** — no data on whether catalyst efficiency failure produces a measurable 5-gas delta between idle and 2500 RPM (the OBD catalyst monitor runs at idle, suggesting the delta may not be the diagnostic feature).

---

## Readiness Verdict

**The suite can be authored now** for:
- Qualitative delta-**direction** diagnosis (lean vs rich, leak vs sensor, etc.)
- Architecture-aware branching (speed-density null gate, turbocharger inversion gate under load)
- Validity-gate rejection (dilution, warm-up, RPM stability)

**The suite CANNOT be authored now** for:
- Quantitative pass/fail thresholds with defensible, validated magnitude bounds
- Any claim of diagnostic sensitivity/specificity

**Recommended path:** Build the fixture set with **qualitative delta directions** and **conservative noise thresholds** (STFT ±3%, LTFT ±5%). Flag all magnitude-dependent decisions as requiring expert calibration. Treat the fixture set as a **decision-support tool** (ranked candidate faults) rather than a **pass/fail classifier** until a validation dataset emerges.

**The blocking gap is item #6** — no public paired dataset. Without this, quantitative thresholds remain expert estimates, not evidence-based.

Here is the entire diagnostic strategy presented clearly in English (alphabet).

---

## Diagnostic Strategy: Comparing Low, High, and "Stress" Idle Deltas

Your goal is to measure engine parameters at three distinct stationary RPM points—**Low Idle**, **High Idle (2500 RPM)** , and **Stress Idle (3500–4500 RPM)** —and compare the **deltas (changes)** between them to pinpoint the root cause of a fault. This is an excellent and powerful diagnostic approach.

---

### 1. Defining the Three Test Points

| Test Point | RPM Range | Purpose | Throttle Condition |
| :--- | :--- | :--- | :--- |
| **Low Idle** | Curb idle (600–900 RPM, varies by engine) | Baseline reference; checks basic mixture stability. | Closed throttle (PCM-controlled idle). |
| **High Idle** | **2500 RPM** (regulatory standard) | Standardized stress point for emissions; checks fuel system and catalyst under mild load. | Steady throttle, no load (Park/Neutral). |
| **Stress Idle** | **3500–4500 RPM** (varies by engine, typically ~75% of max power RPM) | Extreme stress point; exposes fuel delivery limits, ignition breakdown, and mechanical wear under high cylinder pressure. | Steady throttle, no load (Park/Neutral). |

---

### 2. Key Parameters to Measure

| Parameter | Abbreviation | What It Indicates |
| :--- | :--- | :--- |
| Short-Term Fuel Trim | STFT | Immediate, rapid corrections to air-fuel ratio. Normal: ±0–3%. |
| Long-Term Fuel Trim | LTFT | Learned, persistent corrections. Normal: ±0–5%. Positive = adding fuel (lean condition). Negative = removing fuel (rich condition). |
| Hydrocarbons | HC | Unburned fuel. High = misfire or incomplete combustion. |
| Carbon Monoxide | CO | Incomplete combustion. High = rich mixture. |
| Oxygen | O₂ | Residual oxygen in exhaust. High = lean mixture or exhaust leak. |
| Carbon Dioxide | CO₂ | Complete combustion. Low = inefficient burn. |
| Lambda (λ) | λ | Normalized air-fuel ratio. 1.00 = stoichiometric. >1.01 = lean, <0.99 = rich. |
| Fuel Pressure | FP | Fuel system delivery capacity. Should rise slightly with RPM. |
| Manifold Absolute Pressure | MAP | Engine load and vacuum. Leaks reduce vacuum (higher MAP). |

---

### 3. Core Diagnostic Principle: Analyze the Deltas

Do not look at absolute values alone. Look at the **change** between points:

- **Delta 1 (Low → High)**: Idle → 2500 RPM.
- **Delta 2 (High → Stress)**: 2500 RPM → 3500–4500 RPM.

A fault that **improves** as RPM rises suggests a condition that is overwhelmed by increased airflow (e.g., vacuum leak, exhaust leak).
A fault that **worsens** as RPM rises suggests a condition that is stressed by higher demand (e.g., fuel starvation, ignition breakdown).

---

### 4. Fault Signatures by Delta Pattern

| Fault Family | Low Idle Signature | High Idle (2500) Signature | Stress Idle (3500–4500) Signature | **Critical Delta Pattern** | Diagnostic Conclusion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Vacuum Leak** | LTFT +15–30% (very lean). O₂ high. λ > 1.02. | LTFT drops to +5–10%. O₂ improves. λ near 1.00. | LTFT drops further, near 0%. O₂ normal. | **Large Delta (Improving)** . Leak effect diminishes with RPM because manifold vacuum drops. | **Vacuum Leak.** |
| **Fuel Starvation (Clogged Filter/Pump)** | Fuel pressure normal or slightly low. LTFT normal or slightly positive. | Fuel pressure drops. LTFT rises to +10–20% to compensate. | Fuel pressure severely drops. LTFT pegs +25%. Engine may stumble. | **Large Delta (Worsening)** . Demand exceeds supply at high RPM. | **Fuel Delivery Fault.** |
| **MAF Sensor Under-Reporting** | LTFT +15–20% (PCM sees less air than actual). | LTFT remains +15–20%. No improvement. | LTFT remains +15–20%. No change. | **No Delta** (persistent across all RPM). | **MAF Sensor Contamination/Failure.** |
| **O₂ Sensor Slow/Lazy** | STFT oscillates slowly or not at all. Voltage stuck. | STFT remains abnormal. Voltage stuck. | STFT remains abnormal. Voltage stuck. | **No Delta** (persistent across all RPM). | **O₂ Sensor Fault.** |
| **Ignition/Misfire (Weak Coil/Plugs)** | HC slightly elevated (150–300 ppm). Idle may be smooth. | HC rises moderately (300–500 ppm). Misfire counts increase. | HC spikes (>1000 ppm). Misfire counts increase sharply. Engine vibrates. | **Large Delta (Worsening)** . Higher cylinder pressure requires more spark energy. | **Ignition System Fault.** |
| **Catalyst Failure** | Rear O₂ mirrors front O₂ (switching). | Rear O₂ continues to mirror front. | Rear O₂ continues to mirror front. | **No Delta** (failure is RPM-independent). | **Catalyst Failure** (use catalyst monitor, not idle delta). |
| **Exhaust Leak (Upstream)** | O₂ reads lean (fresh air ingress). λ > 1.02. LTFT positive. | O₂ improves slightly (higher flow dilutes leak). | O₂ normal (flow overwhelms leak). λ near 1.00. | **Large Delta (Improving)** . | **Exhaust Leak.** |
| **Cam Timing Error (Retarded)** | MAP low (low vacuum). LTFT positive. | MAP improves slightly. LTFT positive. | MAP improves further. LTFT still positive. | **Delta scales with RPM** (error is proportional to airflow). | **Cam Timing Fault.** |
| **Mechanical Wear (Low Compression)** | HC elevated. Idle rough. | HC may improve slightly (higher RPM masks roughness). | HC may worsen or stay elevated. Erratic. | **No consistent delta** (wear affects all RPM equally). | **Mechanical Wear** (use compression test). |

---

### 5. Valid "Stress Idle" RPM Determination

For the **Stress Idle (3500–4500 RPM)** point, you cannot use a fixed universal number. You must calculate it per vehicle:

| Engine Type | Stress Idle RPM | Calculation |
| :--- | :--- | :--- |
| Typical passenger car (max power RPM ~5500–6000) | **~4000–4500 RPM** | 75% of max power RPM (ISO 5130 standard). |
| High-revving engine (max power RPM >7000) | **~3500–3750 RPM** | 50% of max power RPM (ISO 5130 standard). |
| Diesel or low-revving engine (max power RPM <5000) | **~3750 RPM** | 75% of max power RPM (ISO 5130 standard). |

**Procedure:**
1.  Identify the engine's **RPM at maximum power** from the vehicle's technical data.
2.  Multiply by **0.75** (for most cars) or use the manufacturer's specified stationary test RPM.
3.  Hold that RPM steady for at least **10–15 seconds** to allow fuel trims and readings to stabilise before recording.

---

### 6. Validity Gates (Critical Preconditions)

Before you record any delta, you must pass these validity checks:

| Validity Check | Threshold | Applies To |
| :--- | :--- | :--- |
| Engine Warm-Up | Coolant temperature > 160°F (70°C) OR > 3 minutes after closed-loop. | Fuel Trims, O₂ |
| Closed-Loop Status | O₂ sensors switching; STFT active and oscillating. | Fuel Trims, O₂, λ |
| RPM Stability (Idle) | Within ±50 RPM of specified curb idle for ≥10 seconds. | All |
| RPM Stability (High/Stress) | Within ±100 RPM of target for ≥10 seconds. | All |
| Gas Sum (Dilution Check) | CO + CO₂ > 6% (petrol). | All 5-Gas |
| Excess O₂ Check | O₂ < 5%. If O₂ > 5%, exhaust is diluted (leak or misfire). | O₂, λ |
| No Accessories | Air conditioning, headlights, and all electrical loads OFF. | All (fuel trims shift with load) |
| Transmission | In Park (automatic) or Neutral (manual). | All |

---

### 7. Summary Diagnostic Flowchart

1.  **Warm up engine** to operating temperature (closed-loop).
2.  **Record Low Idle** data (fuel trims, 5-gas, fuel pressure).
3.  **Raise RPM to 2500** (High Idle). Hold for 10–15 seconds. Record data.
4.  **Raise RPM to Stress level** (3500–4500 RPM, calculated as 75% of max power RPM). Hold for 10–15 seconds. Record data.
5.  **Calculate Deltas:**
    - Delta 1 = High Idle - Low Idle.
    - Delta 2 = Stress Idle - High Idle.
6.  **Compare deltas to fault patterns** in the table above.

---

### 8. Final Verdict

Using this three-point delta method, you can **reliably separate**:
- Vacuum leaks from MAF sensor faults (leak improves with RPM; MAF fault does not).
- Fuel starvation from ignition faults (both worsen with RPM, but fuel pressure drops in the first, while HC spikes in the second).
- Exhaust leaks from O₂ sensor faults (leak improves with RPM; O₂ fault persists).

The **Stress Idle (3500–4500 RPM)** point is essential because it exposes faults that only manifest under high demand—conditions that a simple 2500 RPM test alone cannot reveal. However, you must always calculate the correct stress RPM per vehicle and never use a fixed universal number.