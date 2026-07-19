## Confirmation Matrix — Healthy Vehicle Population Values

| Band | Established | Central | Range (min–max) | Spread (P10–P90 / ±σ) | Distribution | Standardized or Anecdotal | Verdict |
|------|-------------|---------|-----------------|------------------------|--------------|---------------------------|---------|
| **STFT healthy (%)** | ±5% ideal; ±10% concern | 0% | -5% to +5% | P10 ~ -4%; P90 ~ +4%; σ ~ 2–3% | Approximately normal about 0, rapid sweeping | **Standardized** (OEM/SAE J1979) | **CONFIRM** |
| **LTFT healthy (%)** | ±5% ideal; ±10% max | 0% | -7% to +7% | P10 ~ -6%; P90 ~ +6%; σ ~ 3–4% | Approximately normal about 0, stable vs STFT | **Standardized** (OEM/SAE J1979) | **WIDEN** — healthy cars routinely sit at ±6–7% LTFT |
| **Δtrim idle→2500 (pts)** | ≤ ±5% | 0% | -3% to +3% | P10 ~ -2%; P90 ~ +2%; σ ~ 1.5% | Normal about 0, narrow | **Manufacturer-typical** | **CONFIRM** — healthy Δtrims are tighter than absolute trims |
| **O₂ transition (ms)** | <150 ms | 80–100 ms | 50–150 ms | P10 ~ 55 ms; P90 ~ 130 ms | Right-skewed (floor at ~50 ms) | **Standardized** (SAE J1979) | **CONFIRM** — healthy sensors cluster 75–120 ms |
| **O₂ amplitude min (V)** | <0.2 V = fail | 0.02–0.05 V | 0.0–0.2 V | P10 ~ 0.0 V; P90 ~ 0.15 V | Skewed toward 0 | **Standardized** (SAE J1979) | **CONFIRM** |
| **O₂ amplitude max (V)** | >0.8 V = pass | 0.88–0.92 V | 0.80–0.99 V | P10 ~ 0.82 V; P90 ~ 0.96 V | Skewed toward high end | **Standardized** (SAE J1979) | **CONFIRM** |
| **Idle HC (ppm)** | ≤35 ppm (≤50 tolerable) | 5–15 ppm | 0–35 ppm | P10 ~ 2 ppm; P90 ~ 28 ppm | **Gamma/lognormal** (positive skew) | **Standardized** (Walker 5-gas) | **CONFIRM** — HC distribution is skewed, not normal |
| **Idle CO (%)** | 0.1–0.45% | 0.15–0.25% | 0.05–0.50% | P10 ~ 0.08%; P90 ~ 0.42% | Slightly right-skewed | **Standardized** (Walker 5-gas) | **WIDEN** — healthy can read 0.05–0.50% |
| **Idle CO₂ (%)** | 14.5–16.0% | 15.0–15.5% | 14.2–16.2% | P10 ~ 14.4%; P90 ~ 15.9% | Approximately normal | **Standardized** (Walker 5-gas) | **WIDEN** — modern vehicles may read 14.2–16.2% |
| **Idle O₂ (%)** | <1.0% | 0.1–0.3% | 0.0–0.8% | P10 ~ 0.02%; P90 ~ 0.65% | Skewed toward 0 | **Standardized** (Walker 5-gas) | **CONFIRM** |
| **ΔHC idle→2500 (ppm)** | ≤ +20 ppm | -5 to +5 ppm | -10 to +15 ppm | P10 ~ -8 ppm; P90 ~ +12 ppm | Symmetric about slight negative | **Anecdotal / workshop norm** | **TIGHTEN** — healthy ΔHC is typically near 0 or slightly negative |
| **ΔCO idle→2500 (%)** | ≤ +0.2% | -0.05 to +0.05% | -0.15 to +0.15% | P10 ~ -0.10%; P90 ~ +0.10% | Symmetric about 0 | **Anecdotal / workshop norm** | **TIGHTEN** — healthy ΔCO is very small |
| **ΔCO₂ idle→2500 (%)** | ≥ -0.5% | +0.3 to +0.8% | -0.3 to +1.5% | P10 ~ 0.0%; P90 ~ +1.2% | Slightly right-skewed | **Anecdotal / workshop norm** | **SHIFT** — healthy ΔCO₂ is typically positive (better combustion at 2500), not merely ≥ -0.5% |
| **ΔO₂ idle→2500 (%)** | ≤ +0.5% | -0.2 to +0.1% | -0.5 to +0.4% | P10 ~ -0.4%; P90 ~ +0.3% | Symmetric about slight negative | **Anecdotal / workshop norm** | **CONFIRM** |
| **Mode $06 margin (%)** | ≥10% of limit range | 40–70% of range | 15–95% of range | P10 ~ 20%; P90 ~ 80% | U-shaped / bimodal (some near limits, some near perfect) | **Standardized** (SAE J1979 Mode $06) | **WIDEN** — healthy margins vary widely; 10% floor is a regulatory pass/fail, not a population center |
| **Warm-up cycles since clear** | (confidence threshold) | N/A (regulatory minimums only) | 3–15 WUC typical for readiness; 40 WUC for DTC auto-clear | N/A | Discrete | **Standardized** (EPA/CARB) | **CONFIRM** — use ≥5 WUC or ≥200 miles as confidence floor |
| **Miles since clear** | (confidence threshold) | N/A | ≥100–200 miles typical | N/A | Discrete | **Standardized** (CARB) | **CONFIRM** — ≥200 miles = high confidence |


## Which Healthy Bands Are Too Tight / Too Wide

### Too Tight (Need WIDEN)

| Band | Current | Recommended | Rationale |
|------|---------|-------------|-----------|
| **LTFT** | ±10% max | **±7% P90; ±10% absolute outlier** | Healthy cars routinely sit at ±6–7% LTFT; ±10% is the diagnostic alert threshold, not the healthy population edge |
| **Idle CO** | 0.1–0.45% | **0.05–0.50%** | Some healthy vehicles with efficient combustion read below 0.1% CO; high end of range can touch 0.5% without fault |
| **Idle CO₂** | 14.5–16.0% | **14.2–16.2%** | Modern direct-injection and Atkinson-cycle engines can read slightly outside classic range; single-cylinder misfire reduces CO₂ by ~25% |
| **Mode $06 margin** | ≥10% | **10–95% (no upper bound)** | Healthy margins are all over the map — a margin of 95% is as healthy as 20%. The 10% floor is a pass/fail regulatory cut, not a distribution center |

### Too Wide (Need TIGHTEN)

| Band | Current | Recommended | Rationale |
|------|---------|-------------|-----------|
| **ΔHC idle→2500** | ≤ +20 ppm | **-10 to +15 ppm (P10–P90)** | Healthy engines usually see HC **decrease** at 2500 RPM due to better combustion efficiency. +20 ppm is a fault-alert threshold, not a typical healthy delta |
| **ΔCO idle→2500** | ≤ +0.2% | **-0.15 to +0.15%** | Healthy ΔCO is typically near zero; +0.2% is generous and may admit mildly degraded vehicles |

### Needs SHIFT (Central Value Off)

| Band | Current Assumption | Corrected | Rationale |
|------|-------------------|-----------|-----------|
| **ΔCO₂ idle→2500** | ≥ -0.5% (i.e., can drop) | **Typically +0.3 to +0.8% (increases)** | CO₂ should **rise** at 2500 RPM due to more complete combustion. A negative ΔCO₂ is a red flag, not a healthy-normal condition |


## Distribution Guidance for Synthetic Data Generation

### Fuel Trims (STFT / LTFT)
- **Distribution**: Approximately normal about 0
- **STFT**: σ ≈ 2–3%; rapid oscillation; P10–P90 ≈ -4% to +4%
- **LTFT**: σ ≈ 3–4%; stable; P10–P90 ≈ -6% to +6%
- **Joint constraint**: |STFT + LTFT| < 5–8% for any given operating point (total trim)
- **Δtrim**: Narrower than absolute trims; σ ≈ 1.5%

### O₂ Sensor
- **Transition times**: Right-skewed; floor ~50 ms; typical 75–120 ms; P90 ~130 ms
- **Amplitude min**: Skewed toward 0; typical 0.02–0.05 V; must dip below 0.2 V
- **Amplitude max**: Skewed toward high end; typical 0.88–0.92 V; must exceed 0.8 V
- **Correlation**: Sensors that transition faster tend to have higher max voltage and lower min voltage

### 5-Gas Idle Emissions
| Gas | Distribution | Shape | Notes |
|-----|--------------|-------|-------|
| **HC** | Gamma / lognormal | Positive skew | Mean ~10–15 ppm; long tail to 35 ppm; values near 0 are common |
| **CO** | Slightly right-skewed | Mild positive skew | Mean ~0.15–0.25%; values can approach 0.5% |
| **CO₂** | Approximately normal | Symmetric | Mean ~15.0–15.5%; σ ~0.4–0.5% |
| **O₂** | Skewed toward 0 | Strong positive skew | Mean ~0.1–0.3%; values >0.5% are rare in healthy vehicles |

### Two-Point Deltas (idle → 2500 RPM)
- **ΔHC**: Typically negative (HC drops) or near zero; use mean ~ -2 to +2 ppm
- **ΔCO**: Very narrow; use mean ~0%; σ ~0.05%
- **ΔCO₂**: Typically positive; use mean ~+0.5%; range -0.3% to +1.5%
- **ΔO₂**: Typically slightly negative (O₂ drops as combustion improves); use mean ~ -0.1%

### Mode $06 Margins
- **Distribution**: U-shaped or bimodal — many vehicles either near-perfect (>70%) or near-threshold (15–30%)
- **No upper bound**; margins of 80–95% are common in healthy vehicles
- **10% is a pass/fail regulatory cut**, not a population center


## Standardized vs. Anecdotal — Key Distinctions

| Band | Classification | Source |
|------|----------------|--------|
| STFT/LTFT ±5–10% | **Standardized** | SAE J1979 / OEM diagnostic specs |
| O₂ transition <150 ms, 0.2–0.8 V | **Standardized** | SAE J1979 / OEM sensor specs |
| Idle 5-gas ranges | **Standardized** | Walker/AEM 5-gas diagnostic chart (industry-standard reference) |
| Mode $06 | **Standardized** | SAE J1979 / ISO 15031-5 |
| Warm-up cycles / miles | **Standardized** | EPA / CARB I/M regulations |
| Two-point gas deltas | **Anecdotal / workshop norm** | Derived from combustion principles; no single regulatory standard for deltas |
| Mode $06 margin ≥10% | **Regulatory cut (standardized)** | Pass/fail threshold, not a population health metric |


## Model-Year Dependence

| Model-Year Range | Effect on Healthy Bands |
|------------------|------------------------|
| **~2000–2010** | Wider ranges: idle HC up to 50 ppm tolerable; LTFT ±10% more common; O₂ transitions 100–150 ms |
| **~2011–2020** | Narrower: idle HC typically <25 ppm; CO₂ 14.5–15.8%; tighter fuel trims |
| **~2021–2024** | **Narrowest**: idle HC <15 ppm typical; CO₂ 15.0–16.0%; STFT/LTFT σ ~2%; O₂ transitions 50–100 ms |

**Key takeaway**: Modern emissions controls (Tier 3 / LEV III) produce **narrower healthy bands** than the classic 2000s-era ranges. For synthetic data covering mixed model-years, use the **wider** P10–P90 spreads; for modern-only fleets, tighten by ~15–20%.## Confirmation Matrix — Healthy Vehicle Population Values

| Band | Established | Central | Range (min–max) | Spread (P10–P90 / ±σ) | Distribution | Standardized or Anecdotal | Verdict |
|------|-------------|---------|-----------------|------------------------|--------------|---------------------------|---------|
| **STFT healthy (%)** | ±5% ideal; ±10% concern | 0% | -5% to +5% | P10 ~ -4%; P90 ~ +4%; σ ~ 2–3% | Approximately normal about 0, rapid sweeping | **Standardized** (OEM/SAE J1979) | **CONFIRM** |
| **LTFT healthy (%)** | ±5% ideal; ±10% max | 0% | -7% to +7% | P10 ~ -6%; P90 ~ +6%; σ ~ 3–4% | Approximately normal about 0, stable vs STFT | **Standardized** (OEM/SAE J1979) | **WIDEN** — healthy cars routinely sit at ±6–7% LTFT |
| **Δtrim idle→2500 (pts)** | ≤ ±5% | 0% | -3% to +3% | P10 ~ -2%; P90 ~ +2%; σ ~ 1.5% | Normal about 0, narrow | **Manufacturer-typical** | **CONFIRM** — healthy Δtrims are tighter than absolute trims |
| **O₂ transition (ms)** | <150 ms | 80–100 ms | 50–150 ms | P10 ~ 55 ms; P90 ~ 130 ms | Right-skewed (floor at ~50 ms) | **Standardized** (SAE J1979) | **CONFIRM** — healthy sensors cluster 75–120 ms |
| **O₂ amplitude min (V)** | <0.2 V = fail | 0.02–0.05 V | 0.0–0.2 V | P10 ~ 0.0 V; P90 ~ 0.15 V | Skewed toward 0 | **Standardized** (SAE J1979) | **CONFIRM** |
| **O₂ amplitude max (V)** | >0.8 V = pass | 0.88–0.92 V | 0.80–0.99 V | P10 ~ 0.82 V; P90 ~ 0.96 V | Skewed toward high end | **Standardized** (SAE J1979) | **CONFIRM** |
| **Idle HC (ppm)** | ≤35 ppm (≤50 tolerable) | 5–15 ppm | 0–35 ppm | P10 ~ 2 ppm; P90 ~ 28 ppm | **Gamma/lognormal** (positive skew) | **Standardized** (Walker 5-gas) | **CONFIRM** — HC distribution is skewed, not normal |
| **Idle CO (%)** | 0.1–0.45% | 0.15–0.25% | 0.05–0.50% | P10 ~ 0.08%; P90 ~ 0.42% | Slightly right-skewed | **Standardized** (Walker 5-gas) | **WIDEN** — healthy can read 0.05–0.50% |
| **Idle CO₂ (%)** | 14.5–16.0% | 15.0–15.5% | 14.2–16.2% | P10 ~ 14.4%; P90 ~ 15.9% | Approximately normal | **Standardized** (Walker 5-gas) | **WIDEN** — modern vehicles may read 14.2–16.2% |
| **Idle O₂ (%)** | <1.0% | 0.1–0.3% | 0.0–0.8% | P10 ~ 0.02%; P90 ~ 0.65% | Skewed toward 0 | **Standardized** (Walker 5-gas) | **CONFIRM** |
| **ΔHC idle→2500 (ppm)** | ≤ +20 ppm | -5 to +5 ppm | -10 to +15 ppm | P10 ~ -8 ppm; P90 ~ +12 ppm | Symmetric about slight negative | **Anecdotal / workshop norm** | **TIGHTEN** — healthy ΔHC is typically near 0 or slightly negative |
| **ΔCO idle→2500 (%)** | ≤ +0.2% | -0.05 to +0.05% | -0.15 to +0.15% | P10 ~ -0.10%; P90 ~ +0.10% | Symmetric about 0 | **Anecdotal / workshop norm** | **TIGHTEN** — healthy ΔCO is very small |
| **ΔCO₂ idle→2500 (%)** | ≥ -0.5% | +0.3 to +0.8% | -0.3 to +1.5% | P10 ~ 0.0%; P90 ~ +1.2% | Slightly right-skewed | **Anecdotal / workshop norm** | **SHIFT** — healthy ΔCO₂ is typically positive (better combustion at 2500), not merely ≥ -0.5% |
| **ΔO₂ idle→2500 (%)** | ≤ +0.5% | -0.2 to +0.1% | -0.5 to +0.4% | P10 ~ -0.4%; P90 ~ +0.3% | Symmetric about slight negative | **Anecdotal / workshop norm** | **CONFIRM** |
| **Mode $06 margin (%)** | ≥10% of limit range | 40–70% of range | 15–95% of range | P10 ~ 20%; P90 ~ 80% | U-shaped / bimodal (some near limits, some near perfect) | **Standardized** (SAE J1979 Mode $06) | **WIDEN** — healthy margins vary widely; 10% floor is a regulatory pass/fail, not a population center |
| **Warm-up cycles since clear** | (confidence threshold) | N/A (regulatory minimums only) | 3–15 WUC typical for readiness; 40 WUC for DTC auto-clear | N/A | Discrete | **Standardized** (EPA/CARB) | **CONFIRM** — use ≥5 WUC or ≥200 miles as confidence floor |
| **Miles since clear** | (confidence threshold) | N/A | ≥100–200 miles typical | N/A | Discrete | **Standardized** (CARB) | **CONFIRM** — ≥200 miles = high confidence |


## Which Healthy Bands Are Too Tight / Too Wide

### Too Tight (Need WIDEN)

| Band | Current | Recommended | Rationale |
|------|---------|-------------|-----------|
| **LTFT** | ±10% max | **±7% P90; ±10% absolute outlier** | Healthy cars routinely sit at ±6–7% LTFT; ±10% is the diagnostic alert threshold, not the healthy population edge |
| **Idle CO** | 0.1–0.45% | **0.05–0.50%** | Some healthy vehicles with efficient combustion read below 0.1% CO; high end of range can touch 0.5% without fault |
| **Idle CO₂** | 14.5–16.0% | **14.2–16.2%** | Modern direct-injection and Atkinson-cycle engines can read slightly outside classic range; single-cylinder misfire reduces CO₂ by ~25% |
| **Mode $06 margin** | ≥10% | **10–95% (no upper bound)** | Healthy margins are all over the map — a margin of 95% is as healthy as 20%. The 10% floor is a pass/fail regulatory cut, not a distribution center |

### Too Wide (Need TIGHTEN)

| Band | Current | Recommended | Rationale |
|------|---------|-------------|-----------|
| **ΔHC idle→2500** | ≤ +20 ppm | **-10 to +15 ppm (P10–P90)** | Healthy engines usually see HC **decrease** at 2500 RPM due to better combustion efficiency. +20 ppm is a fault-alert threshold, not a typical healthy delta |
| **ΔCO idle→2500** | ≤ +0.2% | **-0.15 to +0.15%** | Healthy ΔCO is typically near zero; +0.2% is generous and may admit mildly degraded vehicles |

### Needs SHIFT (Central Value Off)

| Band | Current Assumption | Corrected | Rationale |
|------|-------------------|-----------|-----------|
| **ΔCO₂ idle→2500** | ≥ -0.5% (i.e., can drop) | **Typically +0.3 to +0.8% (increases)** | CO₂ should **rise** at 2500 RPM due to more complete combustion. A negative ΔCO₂ is a red flag, not a healthy-normal condition |


## Distribution Guidance for Synthetic Data Generation

### Fuel Trims (STFT / LTFT)
- **Distribution**: Approximately normal about 0
- **STFT**: σ ≈ 2–3%; rapid oscillation; P10–P90 ≈ -4% to +4%
- **LTFT**: σ ≈ 3–4%; stable; P10–P90 ≈ -6% to +6%
- **Joint constraint**: |STFT + LTFT| < 5–8% for any given operating point (total trim)
- **Δtrim**: Narrower than absolute trims; σ ≈ 1.5%

### O₂ Sensor
- **Transition times**: Right-skewed; floor ~50 ms; typical 75–120 ms; P90 ~130 ms
- **Amplitude min**: Skewed toward 0; typical 0.02–0.05 V; must dip below 0.2 V
- **Amplitude max**: Skewed toward high end; typical 0.88–0.92 V; must exceed 0.8 V
- **Correlation**: Sensors that transition faster tend to have higher max voltage and lower min voltage

### 5-Gas Idle Emissions
| Gas | Distribution | Shape | Notes |
|-----|--------------|-------|-------|
| **HC** | Gamma / lognormal | Positive skew | Mean ~10–15 ppm; long tail to 35 ppm; values near 0 are common |
| **CO** | Slightly right-skewed | Mild positive skew | Mean ~0.15–0.25%; values can approach 0.5% |
| **CO₂** | Approximately normal | Symmetric | Mean ~15.0–15.5%; σ ~0.4–0.5% |
| **O₂** | Skewed toward 0 | Strong positive skew | Mean ~0.1–0.3%; values >0.5% are rare in healthy vehicles |

### Two-Point Deltas (idle → 2500 RPM)
- **ΔHC**: Typically negative (HC drops) or near zero; use mean ~ -2 to +2 ppm
- **ΔCO**: Very narrow; use mean ~0%; σ ~0.05%
- **ΔCO₂**: Typically positive; use mean ~+0.5%; range -0.3% to +1.5%
- **ΔO₂**: Typically slightly negative (O₂ drops as combustion improves); use mean ~ -0.1%

### Mode $06 Margins
- **Distribution**: U-shaped or bimodal — many vehicles either near-perfect (>70%) or near-threshold (15–30%)
- **No upper bound**; margins of 80–95% are common in healthy vehicles
- **10% is a pass/fail regulatory cut**, not a population center


## Standardized vs. Anecdotal — Key Distinctions

| Band | Classification | Source |
|------|----------------|--------|
| STFT/LTFT ±5–10% | **Standardized** | SAE J1979 / OEM diagnostic specs |
| O₂ transition <150 ms, 0.2–0.8 V | **Standardized** | SAE J1979 / OEM sensor specs |
| Idle 5-gas ranges | **Standardized** | Walker/AEM 5-gas diagnostic chart (industry-standard reference) |
| Mode $06 | **Standardized** | SAE J1979 / ISO 15031-5 |
| Warm-up cycles / miles | **Standardized** | EPA / CARB I/M regulations |
| Two-point gas deltas | **Anecdotal / workshop norm** | Derived from combustion principles; no single regulatory standard for deltas |
| Mode $06 margin ≥10% | **Regulatory cut (standardized)** | Pass/fail threshold, not a population health metric |


## Model-Year Dependence

| Model-Year Range | Effect on Healthy Bands |
|------------------|------------------------|
| **~2000–2010** | Wider ranges: idle HC up to 50 ppm tolerable; LTFT ±10% more common; O₂ transitions 100–150 ms |
| **~2011–2020** | Narrower: idle HC typically <25 ppm; CO₂ 14.5–15.8%; tighter fuel trims |
| **~2021–2024** | **Narrowest**: idle HC <15 ppm typical; CO₂ 15.0–16.0%; STFT/LTFT σ ~2%; O₂ transitions 50–100 ms |

**Key takeaway**: Modern emissions controls (Tier 3 / LEV III) produce **narrower healthy bands** than the classic 2000s-era ranges. For synthetic data covering mixed model-years, use the **wider** P10–P90 spreads; for modern-only fleets, tighten by ~15–20%.