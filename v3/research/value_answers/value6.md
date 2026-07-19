# Value-Confirmation Matrix — Cluster 6: Sensor Under-Detection

> **Executive Summary:** Public numeric thresholds for O₂ response times are indeed sparse and vehicle-specific, as established in `cluster6.md`. What follows is the **best available cross-OEM synthesis** — a composite of SAE J1979 Mode $06 definitions, CARB OBD II response-rate frameworks, Bosch/DENSO component data, and manufacturer-specific DTC criteria. Where a universal number does not exist, representative ranges and variation bands are provided.


## Confirmation Matrix

| Signal | Healthy Central | Fault Threshold | Range | Spread (±σ / P10–P90) | Distribution | Class | Verdict | Citation |
|--------|-----------------|-----------------|-------|----------------------|--------------|-------|---------|----------|
| **O₂ rich→lean transition time (narrowband)** | **< 100 ms** (upstream) / **< 150 ms** (downstream) | **> 200–500 ms** (OEM-dependent; P015B typical trigger) | 50–500+ ms | Healthy: 50–150 ms; Lazy: 200–500+ ms | Right-skewed (aging sensors drift toward longer times) | **Manufacturer-typical** | 100 ms is the industry benchmark; 327 ms is a documented threshold for rear O₂; P015B sets at 200–500 ms depending on make |  |
| **O₂ lean→rich transition time (narrowband)** | **< 100 ms** (upstream) / **< 150 ms** (downstream) | **> 200–500 ms** (OEM-dependent) | 50–500+ ms | Similar to rich→lean; asymmetry common | Right-skewed; often slightly slower than rich→lean | **Manufacturer-typical** | CARB distinguishes symmetric vs asymmetric degradation; some OEMs monitor directions separately |  |
| **O₂ switch rate / cross-counts (idle)** | **1–5 Hz** (narrowband upstream) | **< 1 Hz** at idle (lazy) | 0.5–8 Hz | Healthy: 1–5 Hz at idle, up to 8 Hz at 2500 RPM | Bimodal (rich/lean dwell times) | **Empirical** | No universal floor; cross-counts demoted per cluster6. 3–10 Hz cited for Zr sensors; 1–5/sec at 2500 RPM |  |
| **Wideband O₂ transition time** | **< 100 ms** (Bosch LSU 4.9) | Typically > 100–200 ms (OEM-specific) | < 50–300 ms | Tight; widebands are faster than narrowbands | Near-normal | **Manufacturer-typical** | Bosch LSU 4.9: < 100 ms response; wideband operates via current (mA), not voltage switching |  |
| **MAF measured-vs-calculated deviation (%)** | **< ±5%** (OEM-grade) | **> 10–15%** (P006A threshold) / **> 25–30%** (P00BC threshold) | 0–50% | Healthy: ±1–5%; Fault trigger: 10–30% | Normal around 0%; fault modes at extremes | **Standardized / Manufacturer-typical** | P006A: 10–15% MAP-MAF correlation mismatch; P00BC: 25–30% below predicted; Bosch: ±5% deviation can set CEL |  |
| **MAF absolute error masking-limit (%)** | **< ±3–5%** (trim can mask) | **> 10–15%** (exceeds trim authority) | ±3–20% | ±3–5% masked by fuel trims; 10–15% breaks through | Normal; long-term trim shifts | **Empirical** | Fuel trims typically correct ±10–15%; sustained MAF error beyond this becomes detectable | — |
| **Heater light-off / activity time (s)** | **< 20–30 s** | **> 30–60 s** (fault) | 10–60 s | Healthy: 10–30 s; Faulted: 30–60+ s | Near-normal; aging shifts right | **Manufacturer-typical** | Bosch LSU 4.9: 20 s to 700–800°C; CARB rough ~30 s per cluster6 |  |


## Detailed Signal-by-Signal Analysis

### 1. O₂ Rich→Lean Transition Time (ms)

**Narrowband (upstream):**
- **Healthy central:** < 100 ms. Some sources cite < 150 ms for good sensors.
- **Fault threshold:** 200–500 ms, manufacturer-dependent. P015B triggers when rich-to-lean transition exceeds 200–500 ms for 5+ drive cycles. A documented rear O₂ threshold is **327 ms** (0.5 V → 0.3 V drop).
- **Range:** Healthy 50–150 ms; lazy 200–500+ ms.
- **Spread:** Significant OEM variation; no single universal number exists.

**Narrowband (downstream / rear):**
- Slower than upstream by design; thresholds are typically higher.
- Documented example: rear O₂ threshold ≥ 327 ms for rich→lean (0.5 V → 0.3 V).

**Wideband:**
- **Healthy central:** < 100 ms.
- **Fault threshold:** OEM-specific; typically > 100–200 ms.
- Widebands use current-based (mA) measurement, not voltage switching.

**Distribution:** Right-skewed — healthy sensors cluster below 100 ms; aging sensors drift toward longer times. Asymmetric degradation (rich→lean vs lean→rich) is recognized.

### 2. O₂ Lean→Rich Transition Time (ms)

- Similar to rich→lean but often slightly slower.
- CARB distinguishes symmetric vs asymmetric degradation.
- Some OEMs monitor rich→lean and lean→rich separately; P0139 judges NG if **either** direction fails.
- Thresholds: typically 200–500 ms, OEM-dependent.

### 3. O₂ Switch Rate / Cross-Counts (Hz) at Idle

- **Healthy central:** 1–5 Hz at idle; up to 8 Hz at 2500 RPM.
- **Fault threshold:** < 1 Hz at idle indicates lazy sensor.
- **Range:** 0.5–8 Hz.
- **Distribution:** Bimodal (time spent in rich vs lean states).
- **Note:** Cross-counts have no universal floor (per cluster6). Some sources cite 3–10 Hz minimum for Zr sensors.
- **Verdict:** Empirical; secondary discriminator only.

### 4. MAF Measured-vs-Calculated Deviation (%)

- **Healthy central:** < ±5% — OEM-grade MAF sensors maintain ±5% accuracy; some specs cite ±1–2%.
- **Fault threshold (P006A):** 10–15% MAP-MAF correlation mismatch triggers code.
- **Fault threshold (P00BC):** 25–30% below predicted value.
- **Range:** 0–50% deviation.
- **Distribution:** Normal around 0%; fault modes at extremes.
- **Verdict:** P006A threshold (10–15%) is manufacturer-typical; P00BC threshold (25–30%) is documented; Bosch ±5% CEL trigger is manufacturer-typical.

### 5. MAF Absolute Error Masking-Limit (%)

- **Healthy central:** < ±3–5% (fully masked by closed-loop fuel trims).
- **Fault threshold:** > 10–15% — exceeds typical fuel trim correction authority (±10–15%).
- **Range:** ±3–20%.
- **Distribution:** Normal; long-term fuel trim shifts indicate persistent bias.
- **Verdict:** Empirical; trims typically correct ±10–15% before setting lean/rich codes.

### 6. Heater Light-Off / Activity Time (s)

- **Healthy central:** < 20–30 s.
- **Fault threshold:** > 30–60 s (delayed warm-up).
- **Range:** 10–60 s.
- **Distribution:** Near-normal; aging shifts right.
- **Verdict:** Bosch LSU 4.9 reaches 700–800°C in ≤ 20 s; CARB rough ~30 s per cluster6.


## Universal vs Vehicle-Specific Summary

| Category | Genuinely Universal | Manufacturer-Typical | Vehicle-Specific (Mode $06) |
|----------|-------------------|---------------------|----------------------------|
| O₂ 100 ms benchmark | ✅ Industry standard | — | — |
| O₂ fault threshold (ms) | — | ✅ 200–500 ms band | ✅ **Exact fail-line** (read from Mode $06 TID) |
| O₂ switch rate (Hz) | — | ✅ 1–5 Hz idle | — |
| MAF 10–15% deviation | — | ✅ P006A threshold | — |
| MAF 25–30% deviation | — | ✅ P00BC threshold | — |
| MAF ±5% accuracy | — | ✅ Bosch spec | — |
| Heater 20–30 s | — | ✅ Bosch/CARB typical | — |
| **Mode $06 O₂ TID limits** | ❌ | ❌ | ✅ **Read from vehicle** |


## Distribution Guidance

| Signal | Distribution Type | Parameters |
|--------|-------------------|------------|
| O₂ transition time (healthy) | Right-skewed / log-normal | μ ≈ 60–80 ms, σ ≈ 20–40 ms |
| O₂ transition time (aging) | Right-skewed / exponential | λ ≈ 0.005–0.01 (failures > 200 ms) |
| O₂ cross-counts | Bimodal | Rich/lean dwell times |
| MAF deviation | Normal | μ = 0%, σ ≈ 2–3% (OEM) |
| Heater time | Near-normal | μ ≈ 20 s, σ ≈ 5–10 s |


## Source Evidence Summary

| Source | Evidence Type | Key Numbers |
|--------|--------------|-------------|
| Bosch LSU 4.9 spec | Manufacturer-typical | < 100 ms response; 20 s heater |
| P015B description | Manufacturer-typical | < 100 ms healthy; 200–500 ms fault |
| P0139 threshold | Manufacturer-typical | ≥ 327 ms rear O₂ threshold |
| P006A correlation | Manufacturer-typical | 10–15% MAP-MAF mismatch |
| P00BC threshold | Manufacturer-typical | 25–30% below predicted |
| Bosch MAF spec | Manufacturer-typical | ±5% deviation → CEL |
| Switch frequency | Empirical | 1–5 Hz idle; 8 Hz at 2500 RPM |
| Motor Magazine | Industry | < 150 ms good sensor |
| SAE J1979 Mode $06 | Standardized | Test value vs test limit framework |


## Key Takeaways

1. **O₂ response time fail-lines are vehicle-specific** — the exact number must be read from Mode $06 TIDs for the specific vehicle.

2. **The 100 ms benchmark is industry-standard** for healthy upstream narrowband and wideband sensors.

3. **MAF deviation triggers at two levels:**
   - **10–15%** → MAP-MAF correlation fault (P006A)
   - **25–30%** → MAF too low (P00BC)

4. **Bosch MAF sensors:** ±5% deviation can set a CEL.

5. **Heater light-off:** ≤ 20 s for modern wideband (Bosch LSU 4.9); ≤ 30 s rough CARB benchmark.

6. **Cross-counts remain demoted** — no universal floor; use only as secondary indicator.

7. **Mode $06 is the authoritative source** for the vehicle's actual O₂ monitor pass/fail thresholds.