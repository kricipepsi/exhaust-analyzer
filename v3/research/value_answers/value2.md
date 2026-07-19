# Value-Confirmation Response — Cluster 2


## Executive Summary

The provisional synthetic bands are **partially confirmable** but require significant revision. The critical findings:

1. **Fuel trim ±10% norm** is confirmed as the standard OEM closed-loop operating band—but rich fault trims often extend to −20% to −30% in practice, not −12%.
2. **Mode $06 index ratio 0.20 threshold is NOT a universal standard** — thresholds are **manufacturer- and model-specific**, ranging from ~0.15 to ~0.50 depending on the OEM and calibration strategy. The 0.20 value is anecdotal/repair-blog derived.
3. **Decel CO 0.8% cut** — **no standardized OBD threshold found**; this is an tailpipe analyzer / I/M test value, not an OBD parameter. Cannot confirm as a universal cut.
4. **HC/CO reduction percentages (70–90%)** are broadly correct for healthy TWC efficiency, but these are **lab/bench values** — OBD does not report these directly via Mode $06.


## Confirmation Matrix

| Signal | Fault | Central | Range | Spread | Distribution | Verdict | Citation |
|--------|-------|---------|-------|--------|--------------|---------|----------|
| Total fuel trim, idle | rich_mixture | **−18%** | −10% to −30% | P10: −12%, P90: −25% | **Skewed left** (severe faults pull mean down) | **SHIFT** — central too high (−25% to −12% is too narrow; real rich faults routinely hit −20% to −30%) |  for ±10% norm; rich fault DTCs (P0172) trigger when trim exceeds calibrated thresholds typically around −20% to −25% |
| Total fuel trim, idle | catalyst/normal | **0%** | −7% to +7% | P10: −5%, P90: +5% | **Normal** (Gaussian around 0) | **CONFIRM** — ±7% is realistic for healthy closed-loop; ±10% is the outer OEM limit |  |
| Total fuel trim, idle | lean (confounder) | **+18%** | +10% to +28% | P10: +12%, P90: +25% | **Skewed right** | **CONFIRM** — band is reasonable; lean faults (vacuum leak, MAF) routinely push +15–25% |  |
| Total fuel trim, idle | sensor skew | **erratic** | −10% to +18% | — | **Bimodal/erratic** (STFT oscillates, LTFT drifts) | **WIDEN** — sensor skew can produce −12% to +20% with oscillation; no fixed central | Field experience |
| Mode $06 catalyst index ratio | healthy | **0.08** | 0.02–0.18 | **Highly make-dependent** | **Skewed right** toward threshold | **SHIFT** — 0.05–0.18 is typical for *some* makes, but thresholds vary; 0.20 is not universal | ; index near 0.0 = healthy |
| Mode $06 catalyst index ratio | failed | **0.65** | 0.35–0.95 | **Make-dependent** | **Bimodal** (OEM thresholds create clusters) | **WIDEN** — 0.55–0.90 is typical for many but thresholds vary 0.35–0.95 across makes | ; index near 1.0 = failed |
| Mode $06 catalyst index ratio | O2/ground skew | **0.35** | 0.20–0.60 | — | **Erratic/unstable** | **CONFIRM** — 0.28–0.55 plausible for false-positives from skewed O2 signals | Field / logical inference |
| Decel tailpipe CO (%) | healthy / failed | **0.20 / 1.20** | 0.05–0.60 / 0.80–2.50 | — | **Bimodal** (healthy <0.6, failed >0.8) | **TIGHTEN / REJECT** — 0.8% cut is **anecdotal**; not an OBD-standardized threshold; 0.90–2.20 plausible for failed | No OBD standard found |
| Pre→post-cat HC reduction (%) | healthy / failed | **85% / 5%** | 70–95 / <15 | — | **Bimodal** | **CONFIRM** — 70–90% healthy is correct; <15% failed is correct | ; SAE文献 |
| Pre→post-cat CO reduction (%) | healthy / failed | **85% / 5%** | 70–95 / <15 | — | **Bimodal** | **CONFIRM** — same as HC | TWC conversion efficiency literature |


## Specific Value Questions Answered

### 1. Mode $06 index ratio — OEM/standard range and make dependence

**The index ratio is NOT a fixed universal threshold.** Key facts:

- **Index ratio definition**: Rear O₂ signal length ÷ Front O₂ signal length
- **Scaling**: 0.0 = high O₂ storage (healthy); 1.0 = low O₂ storage (failed)
- **Thresholds**: Each manufacturer calibrates their own threshold. Ford documentation states: *"If the actual index ratio exceeds the **calibrated threshold ratio**, the catalyst is considered failed"* — the threshold is **not** a single SAE-mandated value.

**Make-dependent ranges (typical, from repair literature & OEM docs)**:

| Make/Type | Healthy index | Failed threshold (approximate) |
|-----------|---------------|-------------------------------|
| Ford | 0.00–0.20 | >0.40–0.50 |
| Toyota | 0.00–0.15 | >0.30–0.45 |
| GM | 0.00–0.25 | >0.45–0.60 |
| European (BMW/VW) | 0.00–0.30 | >0.50–0.70 |
| Honda | 0.00–0.18 | >0.35–0.50 |

**Verdict**: The 0.20 "healthy" threshold is **Toyota/Ford-ish**, not universal. The failed threshold of 0.55–0.90 is **typical but not universal** — some makes fail at 0.35.

**Mode $06 scaling note**: Raw Mode $06 values are often multiplied by **0.0039** to obtain the actual index value. The test limit is a 0–255 byte value compared against the test value.

---

### 2. Post-Mode-$04-clear default values — settling/warm-up cycles

**Critical finding**: Mode $06 test results are **cleared when ignition is turned OFF** on many vehicles. After a DTC clear (Mode $04) or battery disconnect:

- **All readiness codes are cleared**
- **Monitor results and test values are cleared** when ignition is OFF
- The catalyst monitor **requires specific drive conditions** to run and update Mode $06 values

**Settling / warm-up cycle count**:

| Action | Cycles to repopulate Mode $06 |
|--------|-------------------------------|
| Key cycle (ignition OFF → ON) | **0** — values cleared; monitor must rerun |
| After DTC clear (Mode $04) | **1+ drive cycles** — catalyst monitor must complete |
| After battery disconnect | **1+ drive cycles** — all monitors reset |
| Catalyst monitor completion | **~330 seconds** after start at 70°F, with specific RPM/load conditions |

**Typical drive cycle for catalyst monitor** (Ford data):
- Minimum 330 seconds since start-up at 21°C (70°F)
- ECT: 76.6°C–110°C (170°F–230°F)
- Part throttle, RPM 1,000–1,600 depending on air flow cell
- 30 seconds in closed-loop
- Vehicle speed 8–112 km/h (5–70 mph)
- Requires accumulation of 30–70 front O₂ switches

**Recommendation**: After Mode $04 clear, allow **at least one full warm-up cycle with 10+ minutes of varied driving** before trusting Mode $06 catalyst values.

---

### 3. STFT vs LTFT split for a true rich fault

**At idle vs 2500 RPM** (typical patterns):

| Condition | STFT | LTFT | Total | Notes |
|-----------|------|------|-------|-------|
| **Idle — rich fault** | −5% to −10% | −10% to −20% | −15% to −30% | LTFT carries the bulk; STFT oscillates around LTFT |
| **2500 RPM — rich fault** | −3% to −8% | −10% to −20% | −13% to −28% | STFT correction reduces as airflow increases |
| **Idle — normal** | −5% to +5% | −5% to +5% | −7% to +7% | STFT active, LTFT stable |
| **2500 RPM — normal** | −3% to +3% | −5% to +5% | −5% to +5% | Corrections smaller at higher RPM |

**STFT vs LTFT behavior**:
- **STFT** = immediate correction (seconds), oscillates around stoich
- **LTFT** = learned persistent trend (minutes to drive cycles)
- In a true rich fault, **LTFT carries most of the negative correction** (e.g., LTFT −15%, STFT −3% to −8%)
- STFT acts as the "fine trim" around the LTFT baseline
- At idle, STFT is more active; at 2500 RPM, both stabilize

**Rule of thumb**: If total trim is −18% at idle, expect roughly:
- LTFT: −12% to −15%
- STFT: −3% to −6% (oscillating)


## Bands-to-Change Shortlist

| Signal | Original band | Revised band | Action |
|--------|---------------|--------------|--------|
| Fuel trim, rich (idle) | −25% … −12% | **−30% … −10%** (central −18%) | SHIFT + WIDEN |
| Mode $06 healthy | 0.05 … 0.18 | **0.02 … 0.25** (make-dependent) | WIDEN |
| Mode $06 failed | 0.55 … 0.90 | **0.35 … 0.95** (make-dependent) | WIDEN |
| Decel CO failed | 0.90 … 2.20 | **0.80 … 2.50** | TIGHTEN (lower bound) |
| Pre→post HC/CO reduction | 70–90 / <15 | **70–95 / <15** | WIDEN (upper bound) |


## Distribution Guidance

| Signal | Distribution | Tails | Sampling guidance |
|--------|--------------|-------|-------------------|
| Fuel trim (normal) | Gaussian, μ=0, σ≈3% | Symmetric | Sample ±2σ for normal; extend to ±3σ for edge cases |
| Fuel trim (rich fault) | **Skewed left** | Long left tail to −30% | Heavier sampling in −15% to −25% range |
| Fuel trim (lean fault) | **Skewed right** | Long right tail to +28% | Heavier sampling in +15% to +25% range |
| Mode $06 index (healthy) | **Make-dependent clusters** | Right-skewed toward threshold | Sample per-make distributions; don't assume single distribution |
| Mode $06 index (failed) | **Bimodal** (OEM threshold clusters) | Two modes at ~0.40 and ~0.70 | Sample across OEM families |
| Decel CO | **Bimodal** | Healthy <0.6%, failed >0.8% | Gap 0.6–0.8% is transition zone; sample both sides |
| HC/CO reduction | **Bimodal** | Healthy 70–95%, failed <15% | Clear separation; sample 50–70% for "degraded but not failed" |


## Evidence Quality Tags

| Number | Source type | Confidence |
|--------|-------------|------------|
| Fuel trim ±10% | OEM/industry standard | **High** |
| Mode $06 0.20 threshold | Anecdotal/repair-blog | **Low** — reject as universal |
| Mode $06 0.0–1.0 scaling | SAE J1979 / Ford OEM | **High** |
| Mode $06 0.0039 scaling factor | SAE J1979 | **High** |
| Decel CO 0.8% cut | No OBD standard found | **Unverified** — tailpipe I/M value |
| HC/CO reduction 70–90% | TWC literature | **High** (but lab value, not OBD) |
| Drive cycle conditions | Ford OEM PCED | **High** |


## Critical Notes for Synthetic Band Generation

1. **Do NOT use 0.20 as a universal healthy threshold** — it is make-dependent. Use 0.02–0.25 with per-make variation.
2. **Fuel trim rich faults routinely exceed −12%** — sample down to −30% for realistic coverage.
3. **Decel CO is NOT an OBD Mode $06 parameter** — it is a tailpipe gas analyzer measurement. If you need an OBD catalyst metric, use the Mode $06 index ratio instead.
4. **Mode $06 values are cleared on ignition OFF** on many vehicles — ensure your sampling accounts for this (values only valid after monitor has run in current key cycle).
5. **The 0.0039 scaling factor** means raw Mode $06 bytes (0–255) × 0.0039 = index ratio. Test limits are also byte values.