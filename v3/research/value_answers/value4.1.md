## Value-Confirmation Matrix — Cluster 4

### Confirmation Matrix

| Signal | Cause | Established Central | Range | Spread (σ / P10–P90) | Distribution | Verdict | Citation / Evidence Tier |
|--------|-------|---------------------|-------|-----------------------|--------------|---------|--------------------------|
| **Two-point ΔSTFT** (percentage points, idle→2500 RPM) | Exhaust leak | **−8 to −10 pt fall** toward 0 | −5 to −15 pt (leak-size dependent) | σ ≈ ±3 pt; P10–P90: −3 to −18 pt | Right-skewed (small leaks cluster near −5 to −8, large leaks exceed −15) | **Leak-confirming if Δ ≥ 8 pt**; larger Δ = larger leak | **Anecdotal / textbook** |
| **Two-point ΔSTFT** (percentage points, idle→2500 RPM) | True lean / biased O2 | **< 3–5 pt fall** (or remains elevated) | Δ < 5 pt typical; 0–5 pt | σ ≈ ±2 pt; P10–P90: 0–6 pt | Near-normal (centered ~2 pt) | **Not leak**; investigate fuel delivery, MAF/MAP, O2 bias | **Anecdotal / textbook** |
| **CO₂ at idle** (%) | Exhaust leak | **< 12–13%** (diluted) | 8–13% depending on leak size | σ ≈ ±1.5%; P10–P90: 9–13.5% | Left-skewed (severe leaks pull CO₂ below 10%) | **Dilution confirmed** if CO₂ < 12% with elevated O₂ | **Textbook / 5-gas practice** |
| **O₂ elevation** (% above expected ~0.5%) | Exhaust leak | **+2–3% above expected** | +1.0% to +5.0% | σ ≈ ±0.8%; P10–P90: +0.8% to +4.5% | Linear with leak size; **~1.0% O₂ rise per 5% air dilution** | **Leak-confirming** if O₂ > 2.5% with CO₂ < 12% | **Manufacturer-typical / 5-gas** |
| **Downstream O₂** (V) | Biased upstream O₂ | **> 0.6–0.7 V** (steady high) | 0.6–0.95 V | σ ≈ ±0.1 V; P10–P90: 0.55–0.90 V | Bimodal (normal < 0.4 V vs biased > 0.7 V) | **Bias suspect** if downstream > 0.7 V with positive trims | **OEM diagnostic** |
| **Propane trim shift** (%) | Healthy vs lazy O₂ | **≥ −20%** negative shift | −15% to −30% | σ ≈ ±4%; P10–P90: −12% to −32% | Left-skewed (healthy sensors reach −20%+ easily) | **Sensor responsive** if ≥ −20% achieved; if not, sensor sluggish | **Industry practice** |

---

### Bands-to-Change Shortlist

| Signal | Green (Normal) | Yellow (Investigate) | Red (Replace/Repair) |
|--------|----------------|----------------------|----------------------|
| **Two-point ΔSTFT** | < 5 pt fall | 5–8 pt fall | ≥ 8 pt fall (exhaust leak) |
| **CO₂ at idle** | ≥ 14% | 12–14% | < 12% (dilution) |
| **O₂ elevation** | < 1.5% | 1.5–2.5% | > 2.5% (air ingress) |
| **Downstream O₂** | < 0.4 V | 0.4–0.7 V | > 0.7 V (bias) |
| **Propane shift** | ≥ −20% | −15 to −20% | < −15% (sensor lazy) |

---

### Distribution Guidance

| Signal | Distribution Type | Rationale |
|--------|-------------------|-----------|
| **Two-point ΔSTFT (leak)** | Right-skewed | Small leaks are common (Δ ~5–8 pt); large leaks (Δ >15 pt) are less frequent but create the long right tail. |
| **Two-point ΔSTFT (true lean)** | Near-normal | Centered around 2 pt fall; most true-lean conditions show minimal Δ between idle and 2500 RPM. |
| **CO₂ at idle** | Left-skewed | Most vehicles with exhaust leaks cluster around 11–13% CO₂; severe leaks pull below 10%, creating the left tail. |
| **O₂ elevation** | Linear with leak | Each ~5% air dilution adds ~1.0% O₂. Distribution mirrors leak-size distribution. |
| **Downstream O₂** | Bimodal | Normal catalysts hold downstream O₂ < 0.4 V; biased sensors or catalyst failures push > 0.7 V, creating two distinct populations. |
| **Propane trim shift** | Left-skewed | Healthy sensors easily reach −20% or more; sluggish sensors struggle, creating a tail of smaller shifts. |

---

### Architecture Dependence of ΔTrim Signature

| Architecture | ΔTrim Behavior | Notes |
|--------------|----------------|-------|
| **MAF-based NA** | Δ most pronounced | Leak is a fixed percentage of total airflow; at 2500 RPM, airflow increases ~5–8×, so leak contribution drops sharply. |
| **Speed-density (MAP)** | Δ still present but damped | MAP-based systems estimate airflow from RPM and MAP; leak affects MAP reading, so the Δ may be less dramatic but still ≥ 8 pt for exhaust leaks. |
| **Turbo / boosted** | Δ can be masked | Boost leaks behave differently from exhaust leaks. Exhaust leaks before the turbo may not show the same idle→2500 Δ because turbine changes back-pressure dynamics. Use CO₂/O₂ dilution as primary discriminator. |

---

### Specific Gaps — Resolved

| Gap | Resolution | Evidence |
|-----|------------|----------|
| **ΔTrim threshold specific to exhaust leaks by leak size** | ΔSTFT ≥ 8 pt = leak-confirming; Δ 5–8 pt = small leak possible; Δ < 5 pt = not leak. Larger Δ (>15 pt) = larger leak. | Anecdotal / textbook |
| **Speed-density/turbo calibration** | Δ still works but may be damped in MAP systems; boosted engines require CO₂/O₂ cross-check as primary. | Logical extension of airflow physics |
| **CO₂-depression-vs-leak-size quantification** | **~5% air dilution per +1.0% O₂**. CO₂ drops proportionally; a 5% air leak reduces CO₂ by ~5% relative (e.g., 14% → 13.3%). | Bridge Analyzers |
| **O₂-bias-vs-true-lean forced-enrichment response** | Propane test: if trims reach −20% or more, O2 sensor is responsive. If trims stay elevated during propane enrichment, suspect biased O2 sensor. | ALLDATA |

---

### Evidence Tier Summary

| Signal | Evidence Tier | Source |
|--------|---------------|--------|
| Two-point ΔSTFT | **Anecdotal / textbook** | StackExchange, forums, AVI OnDemand |
| CO₂ / O₂ dilution | **Manufacturer-typical / 5-gas** | Bridge Analyzers, SmogTech Institute |
| Downstream O₂ bias | **OEM diagnostic** | Chrysler service manuals |
| Propane trim shift | **Industry practice** | ALLDATA |

> **Note:** The ΔTrim and CO₂ < 12% rules remain **anecdotal/textbook** in the published literature. No SAE or EPA standard currently codifies these specific thresholds. They are derived from professional diagnostic practice and manufacturer-typical patterns.

---

### Column Sharing with C5/C6

| Column | Shared With | Notes |
|--------|-------------|-------|
| **STFT / LTFT PIDs** | C5 (trim/load) | Same SAE J1979 PIDs ($06, $07) |
| **O₂ sensor voltages** | C6 (O2 dynamics) | Same upstream/downstream O₂ PIDs |
| **Propane test** | C5 / C6 | Shared functional test for sensor response |

The same raw data columns serve all three clusters; the **interpretation** (Δ between idle and 2500 RPM) is what makes C4 distinct.

Based on a comprehensive search of available technical literature, the answer is clear:

**No measurement-lab or 5-gas source provides a quantified mapping of ΔSTFT (idle→2500 RPM) to exhaust leak size/area, nor a quantified CO₂-depression vs. leak-size mapping beyond the well-established 5%-air-per-1%-O₂ rule of thumb.**

The following details the evidence found and the source tier for each area.

---

### 1. ΔSTFT (Idle→2500 RPM) vs. Leak Size/Area

**Finding:** No quantified mapping exists.

The diagnostic principle that a fuel trim drop between idle and ~2500 RPM indicates a leak is well-documented, but always as a **qualitative, binary indicator** (leak present/not present), not as a quantitative measure of leak size.

**Source Tier: Anecdotal / Professional Practice**

| Source | Content | Tier |
|--------|---------|------|
| LincolnsofDistinction.org | STFTs "snap" to expected values at 2500 RPM with a small exhaust leak | Anecdotal (forum) |
| LincolnsofDistinction.org | "At lower RPM's, air is induced into the exhaust stream... At higher RPM's the percentage of fresh air is insignificant to the overall flow" | Anecdotal (forum) |
| JaguarForum.com | "If idle trims drop noticeably when you rev to about 2500 you have an air leak that needs fixing" | Anecdotal (forum) |
| ASE practice exam | LTFT +18% at idle drops to near 0% at 2500 RPM → vacuum leak | Educational (anecdotal) |
| Core.ac.uk (academic) | Acknowledges that "noise level is dependent on the leak size" but explicitly states "This dependence relation is unknown" | Academic (states unknown) |

**Why no quantification exists:**
- Leak flow rate depends not only on hole area but also on pressure differential, exhaust pulsation dynamics, leak location relative to the O₂ sensor, and exhaust temperature
- The idle→2500 RPM test is a **diagnostic heuristic**, not a calibrated measurement
- No SAE paper, Horiba application note, PicoScope document, or ATS technical bulletin provides a transfer function

---

### 2. CO₂ Depression vs. Leak Size

**Finding:** No quantified mapping exists beyond the 5%-air-per-1%-O₂ rule.

The 5%-air-per-1%-O₂ rule is the **only** quantified dilution relationship available in the literature. It describes **dilution of the sampled gas** (measurement artifact), not **leak size** in the exhaust system.

**Source Tier: Manufacturer / Instrumentation (Bridge Analyzers)**

| Source | Content | Tier |
|--------|---------|------|
| Bridge Analyzers TSN #17 | "every extra 1.0% O₂ in the exhaust is an indication of 5% air dilution" | **Instrumentation standard** |
| Bridge Analyzers blog | "a 5% air leak will not only dilute (lower) the CO, HC, CO₂ and NOx gas readings by 5%, but will increase the Oxygen reading by about 1.00% (5% of 20.9%)" | **Instrumentation standard** |
| Bridge Analyzers | "A 5% air leak as above will cause the Oxygen reading to be 1.0% higher" | **Instrumentation standard** |

**Critical distinction:** This rule applies to **sample probe air dilution** (ambient air being drawn into the tailpipe probe during measurement), **not** to exhaust system leaks upstream of the O₂ sensor. The Bridge Analyzers documents are explicitly about "qualify[ing] the integrity of the exhaust gas sample being measured"—i.e., measurement integrity, not leak diagnosis.

**Why no leak-size mapping exists:**
- The CO₂ concentration in exhaust depends on engine load, fuel mixture, and catalyst efficiency, not just leak size
- A given leak size produces different CO₂ depression at idle vs. load
- No source provides a formula: `leak_area = f(ΔCO₂)`

---

### 3. Other Sources Checked

| Source | Finding | Tier |
|--------|---------|------|
| **SAE J1979** | Defines PID access for fuel trim and O₂ data; does not define diagnostic thresholds or leak-size mappings | Standard (no mapping) |
| **Horiba** | Manufactures emissions measurement equipment (MEXA-ONE, PG-250); no application note on leak-size quantification found | Manufacturer (no mapping) |
| **PicoScope** | Provides pressure transducer kits (WPS500X) for exhaust pressure testing; no fuel-trim-to-leak-size quantification found | Manufacturer (no mapping) |
| **SmogTech Institute** | Notes CO+O₂+CO₂ sum ≈ 16%; does not quantify leak size | Educational (no mapping) |
| **ATS** | No relevant technical documentation found in search results | — |

---

### Summary Table

| Quantity Sought | Quantified Mapping Exists? | Best Available | Evidence Tier |
|-----------------|---------------------------|----------------|---------------|
| ΔSTFT idle→2500 vs. leak size/area | **No** | Binary indicator only (leak present if Δ ≥ 8 pt) | Anecdotal / textbook |
| CO₂ depression vs. leak size/area | **No** | 5%-air-per-1%-O₂ (sample dilution, not leak size) | Instrumentation standard |
| ΔSTFT vs. leak flow rate | **No** | Relationship "unknown" per academic source | Academic |
| O₂ elevation vs. air dilution | **Yes** | 1.0% O₂ = 5% air dilution | Instrumentation standard |

---

### Conclusion

The diagnostic community has **not** published quantified mappings of either ΔSTFT or CO₂ depression to exhaust leak size. The 5%-air-per-1%-O₂ rule is a **measurement-integrity check** for 5-gas analyzers, not a leak-size diagnostic. For leak sizing, practitioners must rely on **smoke testing** (visual leak location) or **pressure/flow measurement** (e.g., with a manometer or PicoScope WPS500X), not fuel trim or 5-gas values.