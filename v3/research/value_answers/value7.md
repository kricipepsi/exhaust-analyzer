# Value-Confirmation Matrix — Cluster 7: cam timing / VVT fault

> **Evidence key:** `[S]` = SAE/OBD standard; `[O]` = OEM/manufacturer-typical; `[A]` = anecdotal/field-estimate. All values petrol light-duty, ~2005–2024, intake or dual VVT.


## Confirmation Matrix

| Signal | Healthy Central | Fault Threshold | Range | Spread (±σ / P10–P90) | Distribution | Operating Point | Verdict | Citation |
|--------|----------------|----------------|-------|----------------------|--------------|-----------------|---------|----------|
| **VVT tracking error (deg)** | ≤2° CA | >5° CA for >4.5s; >6° CA for >2s (some OEMs) | 0–6° CA | ±2–3° CA | Lognormal (skewed toward lag) | **Off-idle only** (2500 rpm, 50–70% load) | **Firmest** — widely consistent across OEMs | Toyota: >5°CA for >4.5s; Hyundai: \|target−actual\| >6° for 2s; P0011 generic: >5°CA |
| **Cam-to-crank correlation (deg)** | Within ±5–6° crank (±2.5–3° cam) of nominal | **Varies by OEM:** GM: >6° crank (>12° cam); Saab: >9° adv / >12° ret; Toyota learning value: <25°CA or >51°CA; GM CMP falling edge: <−11° or >+14° from crank | ±6–25° crank (OEM-dependent) | ±3–10° crank | Bimodal (mechanical jump vs. slow drift) | **Off-idle only** (engine running, >50 RPM) | **Firmest** — SAE/OEM DTC criteria well-documented | Toyota VVT learning: <25° or >51°CA; GM: >6° crank; Saab: >9° adv/12° ret |
| **Volumetric efficiency η_v (%)** | Idle: ~60–70%; 2500 rpm/load: ~75–85% | Δ >8–12% below expected at 2500 rpm/load | 55–85% | ±3–5% (healthy); ±5–10% (faulted) | Normal | **2500 rpm, 50–70% load only** (idle VE too variable) | **Moderate** — VE depression is signal, but OEM thresholds not published | Peak VE ~75% at 2500 rpm; VE typically 75–85% at mid-range |
| **MAF-at-RPM (g/s)** | ~8–12 g/s at 2500 rpm (2.0L, no load); scales with displacement | >15–20% low vs. expected at WOT sweep | Depends on displacement | ±10–15% | Normal | **1000–4500 rpm sweep, WOT** | **Weaker** — highly engine-dependent; reversion over-counts, not under-counts | 2.0L: ~8 g/s at 2500 rpm stationary; idle MAF 5–7 g/s |
| **Combustion temp / NOx (ppm)** | NOx: 50–200 ppm (with iEGR); T_comb: <1370°C | NOx >500–1000 ppm; T_comb >1370°C | NOx: 50–1500+ ppm | ±100–300 ppm | Lognormal | **Off-idle, 2500 rpm load** | **Moderate** — directional but affected by catalyst and fuel | iEGR via VVT reduces NOx; internal EGR via valve overlap dilutes charge |
| **Idle manifold vacuum stability (inHg)** | 17–22 inHg steady | Stuck VVT: erratic flicker; 4 inHg drops; MAP <3 kPa drop from baro | 15–22 inHg | ±1–2 inHg | Normal | **Idle only** (but VVT stuck can manifest here) | **Weakest** — non-specific; many causes (sticking valves, vacuum leaks) | Normal idle vacuum 17–22 inHg; sticking valve flicker ~4 inHg |


## Signal Diagnostics — Off-Idle Only

The following signals are **only diagnostic off-idle** and should **not** be used for VVT fault confirmation at idle:

| Signal | Why idle is ineffective |
|--------|------------------------|
| **VVT tracking error** | Phaser target = 0° at idle (fully retarded); no command means no tracking error to measure |
| **Cam-to-crank correlation** | Idle learning values are stored, but DTC confirmation requires off-idle driving |
| **Volumetric efficiency** | Idle VE is dominated by throttle losses, not valve timing |
| **MAF-at-RPM** | Reversion effects are most pronounced off-idle; MAF over-reads at low RPM with retarded IVC |


## Evidence Strength Ranking

| Rank | Signal | Rationale |
|------|--------|-----------|
| **1 (Firmest)** | VVT tracking error | Consistent thresholds across Toyota (5°CA/4.5s), Hyundai (6°/2s), and generic P0011/P0014 (5°CA) |
| **2 (Firmest)** | Cam-to-crank correlation | Well-documented OEM DTC criteria; P0016 thresholds published by GM, Saab, Toyota |
| **3 (Moderate)** | VE depression | Physically grounded but lacks published OEM fault thresholds; Δ% is field-estimated |
| **4 (Moderate)** | NOx/T_comb | Directionally sound but affected by catalyst efficiency, fuel, and ambient conditions |
| **5 (Weaker)** | MAF-at-RPM | Highly engine-dependent; no universal g/s thresholds; reversion causes over-counting not under-counting |
| **6 (Weakest)** | Idle manifold vacuum | Non-specific; sticking valves, vacuum leaks, and PCV issues produce identical patterns |


## Make/Phaser-Type Dependence

| Parameter | Intake-Only VVT | Dual VVT | Notes |
|-----------|----------------|----------|-------|
| Tracking error threshold | 5–6° CA | 5–6° CA | Similar across both |
| P0016 threshold (cam learning) | Toyota: <25°/ >51°CA | Similar | Learning range wider than tracking error |
| Phaser response time | 250 ms to target | 100–300 ms | Modern systems faster |
| Phaser speed | Up to 550°/s (crank) | Similar | — |
| Internal EGR capability | Limited (intake only) | Full (overlap control) | Dual VVT enables iEGR without external EGR valve |

**Representative OEM ranges:**

- **Toyota:** 5°CA tracking error threshold; VVT learning <25°/ >51°CA
- **Hyundai/Kia:** 6°CA tracking error for 2s
- **GM:** 6° crank (>12° cam) for P0016; CMP falling edge <−11° or >+14°
- **Saab:** 9° advanced / 12° retarded for P0016
- **Generic (P0011/P0014):** 5°CA difference for >4.5s; desired/actual actuator 5–25°


## Practical OBD Acquisition Notes

| Signal | OBD Accessibility | Alternative |
|--------|-------------------|-------------|
| VVT tracking error | Live data (where supported) | OEM scan tool / oscilloscope |
| Cam-to-crank correlation | DTC only (P0016) | Scope (cam/crank waveform) |
| VE | Calculated (MAF + RPM + displacement) | Not directly PID |
| MAF | SAE J1979 PID 0x10 | — |
| NOx | Not OBD (except some Euro 6+) | Exhaust gas analyzer |
| Manifold vacuum | MAP PID (SAE J1979) | Mechanical vacuum gauge |