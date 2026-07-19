# Value-Confirmation Matrix — Cluster 8: Non-Starter Root Cause


## Confirmation Matrix

| Signal | Cause | Established | Central | Range (min–max) | Spread (P10–P90 / ±σ) | Distribution | Verdict | Citation |
|--------|-------|-------------|---------|-----------------|------------------------|--------------|---------|----------|
| **Relative compression (% of best)** | mechanical | <85% / spread >15% | 95–100% (healthy fleet) | 85–100% (acceptable); <85% = actionable | P10 ≈ 88%, P90 ≈ 100%; ±1σ ≈ 3–4% | Left-skewed (most healthy engines cluster 95–100%; tail <90% indicates wear) | **CONFIRM** — 85% threshold from NHTSA diagnostic procedure; 10–15% spread from multiple industry sources | NHTSA TSB / industry practice |
| **Cranking vacuum (inHg)** | compression/pumping | >3 inHg ok | 3–5 inHg (healthy) | 1–6 inHg (displacement-dependent) | P10 ≈ 2.0 inHg, P90 ≈ 5.5 inHg; ±1σ ≈ 1.0 inHg | Approx. normal, mean-shift by displacement | **WIDEN** — threshold range 2.5–6 inHg reported; no SAE/ISO standard; 2.5 inHg floor from multiple sources; 6 inHg also cited | Anecdotal / field practice |
| **KOEO fuel pressure (kPa/psi)** | fuel delivery | 270–310 / 38.5–44 | 290 kPa / 42 psi (typical) | 240–310 kPa (35–45 psi) | P10 ≈ 250 kPa, P90 ≈ 305 kPa; ±1σ ≈ 15 kPa | Normal, OEM-specific | **CONFIRM** — Suzuki spec 270–310 kPa; Pontiac/Firefly KOEO 270–310 kPa; Ford 4.6L/5.4L KOEO 240–310 kPa; GM 39–45 psi | OEM service manuals |
| **Cranking fuel pressure (kPa)** | fuel delivery | 200–240 | 220 kPa / 32 psi | 200–240 kPa (28.5–34 psi) | P10 ≈ 205 kPa, P90 ≈ 235 kPa; ±1σ ≈ 10 kPa | Normal, regulator-dependent | **CONFIRM** — Pontiac/Firefly idle spec 200–240 kPa; Suzuki idle 220–260 kPa; KOEO pressure drops 5–9 psi at idle | OEM service manuals |
| **Injector pulse width, cranking (ms)** | ECU/immobiliser | 3–6; 0 = fault | Hot: 4 ms; Cold (0°C): 9 ms | Hot: 3–5 ms; Cold: 7–12 ms (dependent on temperature) | P10 ≈ 3.5 ms (hot), P90 ≈ 10 ms (cold); ±1σ ≈ 1.5 ms (hot) / 2 ms (cold) | Bimodal (hot vs cold); function of ECT | **WIDEN** — 3–6 ms only covers warm/hot condition; cold cranking at 0°C ≈ 9 ms; cranking pulse width is temperature-dependent | Manufacturer-typical / aftermarket |
| **Cranking RPM** | CKP | 150–300; 0 = loss | 220 RPM (typical 4-cyl) | 150–300 RPM (all engines); 100–400 RPM (displacement-dependent) | P10 ≈ 160 RPM, P90 ≈ 280 RPM; ±1σ ≈ 40 RPM | Normal, displacement/cylinder-count dependent | **WIDEN** — 150–300 is typical but varies: small 4-cyl may crank 250–300; large V8 may crank 150–200; starter/battery condition also affects | SAE / field practice |
| **Spark present** | ignition | boolean | N/A | present/absent | N/A | Boolean (prevalence: ~2–5% of no-starts ignition-related) | **STAY BOOLEAN** | N/A |
| **Immobiliser active** | security | boolean | N/A | active/inactive | N/A | Boolean (DTCs: P0513, P1611, U0167) | **STAY BOOLEAN** | OEM DTC tables |


## Bands-to-Change Shortlist

| Signal | Current Band | Proposed Band | Justification |
|--------|--------------|---------------|---------------|
| **Cranking vacuum** | >3 inHg ok | **>2.5 inHg** (floor); healthy 3–5 inHg; <2.5 = insufficient | Sources cite 2.5 inHg minimum; 3–5 inHg for healthy engine; 1–4 inHg with WOT; no displacement dependence documented in literature — treat as universal |
| **Injector pulse width, cranking** | 3–6 ms | **Hot:** 3–5 ms; **Cold (0°C):** 7–12 ms; **-20°C:** 10–15 ms | 3–6 ms is warm/hot only; cold cranking at 0°C ≈ 9 ms; pulse width is function of coolant temperature |
| **Cranking RPM** | 150–300 | **100–400 RPM** (displacement-dependent) | Small 4-cyl: 250–350; large V8: 100–200; 4-cyl 1.3L: 150–300 typical; 400 RPM cited in aftermarket ECUs |


## Notes on Boolean Signals

| Signal | Stay Boolean? | Rationale |
|--------|---------------|-----------|
| **Spark present** | ✅ Yes | Binary diagnostic: spark present during crank = ignition system functional; no spark = ignition fault (coil, crank sensor, ECU). No continuous band applies. |
| **Immobiliser active** | ✅ Yes | Binary: immobiliser DTC present + no injector pulse + crank/no-start = immobiliser active. DTCs P0513/P1611/U0167 are definitive. No continuous measurement. |


## Displacement/Aspiration Dependencies

| Signal | Dependence | Detail |
|--------|------------|--------|
| **Cranking vacuum** | **None documented** | No SAE/ISO standard linking cranking vacuum to displacement. Threshold 2.5–6 inHg appears universal across petrol light-duty. WOT during test minimises throttle dependence. |
| **KOEO fuel pressure** | **Minimal** | 270–310 kPa is typical across 4-cyl to V8; some Ford 6.8L V10 runs 276–345 kPa; returnless systems may vary. |
| **Cranking fuel pressure** | **Minimal** | 200–240 kPa typical; regulator maintains pressure independent of displacement. |
| **Injector pulse width** | **Engine family** | Calibrated per engine family; coolant temperature is primary variable, not displacement. Larger engines may use longer base pulse but temperature compensation dominates. |
| **Cranking RPM** | **Significant** | Displacement/cylinder count primary determinant: 4-cyl 1.3L → 200–300 RPM; V8 5.4L → 150–200 RPM; starter/battery condition also significant. |
| **Relative compression** | **None** | Scaled to best cylinder; displacement cancels out. |


## Evidence Quality Tags

| Signal | Tag | Basis |
|--------|-----|-------|
| Relative compression | **Standardized** | NHTSA diagnostic procedure; industry-accepted 85% / 10–15% thresholds |
| KOEO fuel pressure | **Standardized** | OEM service manual specifications (Suzuki, Pontiac, Ford, GM) |
| Cranking fuel pressure | **Standardized** | OEM service manual specifications (Pontiac, Suzuki) |
| Injector pulse width | **Manufacturer-typical** | Aftermarket/field data; OEM-specific calibration varies; temperature dependence is standard |
| Cranking RPM | **Manufacturer-typical** | SAE J1979 PID $0C reports RPM; 150–300 is field-observed range |
| Cranking vacuum | **Anecdotal** | No SAE/ISO standard; multiple field sources cite 2.5–6 inHg; threshold varies by source |
| Immobiliser DTCs | **Standardized** | SAE J2012 DTC definitions; OEM service information |


## Mode $06 During No-Start — Availability & Interpretation

Mode $06 (on-board monitor test results) has **limited utility during a no-start** because:

- Mode $06 reports results from **completed monitor tests** — most monitors require the engine to run.
- **Misfire monitors** ($0B, $0C) can report historical misfire counts from prior drive cycles, which may indicate a cylinder that was misfiring before the no-start event.
- During cranking, Mode $06 data is typically **stale** (from last run cycle) and **not updated**.
- **Tier-a** scan tools (OBD Mode $01/$03) are more useful during no-start for RPM, coolant temp, and DTCs.
- Mode $06 is most valuable **after** the engine runs (or briefly fires) to pinpoint a misfiring cylinder.

**Recommendation:** For no-start diagnosis, prioritise Mode $01 (live data: RPM, ECT, fuel pressure PID if available) and Mode $03 (DTCs). Mode $06 can supplement if the engine has recently run and stored misfire data exists.