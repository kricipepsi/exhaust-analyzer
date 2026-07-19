# Value-Confirmation Matrix — Cluster 3

## Confirmation Matrix

| Signal | Established | Range · Spread · Distribution | Verdict |
|--------|-------------|------------------------------|---------|
| **KOEO MAP−BARO delta (kPa)** | <5 ok / ≥5 fault | **Central:** ≤2 kPa typical scatter. **Range:** 0–5 kPa acceptable; ≥5 kPa fault threshold. **Spread (P10–P90):** ±1.5 kPa sensor-to-sensor at same altitude; ±3 kPa across temperature range (−20°C to +60°C). **Distribution:** Normal (Gaussian), centered on 0–1 kPa offset; 95% of healthy sensors within ±3 kPa. | **CONFIRM** — 5 kPa threshold is industry-accepted. Note: MAP KOEO should match actual baro (≈101 kPa at sea level). |
| **DLC/signal-ground drop under load (V)** | ≤0.2 ok | **Central:** ≤0.05 V (50 mV) for signal ground; ≤0.10 V per joint. **Range:** 0–0.05 V healthy signal ground; 0–0.10 V chassis ground. **Spread:** Typically 0.01–0.05 V on healthy circuits; up to 0.10 V acceptable on aged harnesses. **Distribution:** Skewed-right (most near 0.01–0.03 V, tail to 0.10 V). | **TIGHTEN** — Signal ground should be ≤0.05 V (50 mV); 0.10 V is per-joint maximum; 0.20 V is absolute ceiling under load. Generic band 0–0.05 V healthy. |
| **Control-module voltage (V)** | ≥12.0 (12.4–12.8 rest) | **Central (rest):** 12.6 V (battery nominal). **Central (running):** 13.8–14.4 V. **Range:** 12.0–15.0 V acceptable operating; <11.5 V = low. **Spread:** ±0.5 V rest; ±1.0 V loaded. **Distribution:** Bimodal (rest vs alternator-regulated). | **WIDEN** — Add 13.8–14.4 V running band; note PID measures ECU supply, not battery direct. |
| **Gas-vs-OBD lambda divergence (Δλ)** | ≥0.05 = control fault | **Central (healthy):** Δλ <0.02 (OBD lambda vs tailpipe gas analyzer). **Range:** 0.00–0.02 healthy scatter; 0.02–0.05 marginal; ≥0.05 = control-loop fault. **Spread:** Sensor-to-sensor ±0.005; temperature drift ±0.010. **Distribution:** Normal around 0.00–0.01 offset. | **CONFIRM** — 0.05 remains valid threshold; healthy scatter is <0.02. |
| **Fuel trim "railed" (%)** | ±25% limit; >+50% mismatch | **Central (normal):** ±5–10% combined STFT+LTFT. **Range:** ±10% normal; LTFT rails at ±20–25%; STFT can reach ±30%. **Spread:** P10–P90: −15% to +15% on healthy systems. **Distribution:** Normal, clipped at rail (±25% typical). | **CONFIRM** — 25% rail is standard; >50% combined indicates sensor mismatch. |
| **O2 transition time (ms)** | healthy <150; fault ~849 | **Central (healthy):** <100–150 ms. **Range:** 50–150 ms healthy; 150–300 ms degraded; >300 ms fault. **Spread:** New sensors: 50–100 ms; aged: 100–150 ms. **Distribution:** Normal, mean ~80 ms new, ~120 ms aged. **849 ms** = adaptation limit (OEM-specific Toyota/Chrysler P0133/P0153 threshold). | **SPLIT** — Generic healthy <150 ms confirmed. 849 ms is OEM-specific (Toyota adaptation timer), not generic. |
| **Bidirectional fuel response** | ±25% command → chemistry step | **Central:** ±25% injector pulse-width change yields ±20–25% fuel-mass change (linear in open-loop; closed-loop O2 feedback dampens observed response). **Range:** Expected chemistry λ shift: ±0.10–0.15 λ per 25% fuel command. **Spread:** ±5% command-to-delivery variance. **Distribution:** Linear within ±25%; saturates beyond. | **CONFIRM** — 25% command produces measurable λ response; reversal indicates control fault. |


## Generic vs OEM-Specific Bands

| Signal | Generic Band | OEM-Specific Notes |
|--------|--------------|---------------------|
| KOEO MAP−BARO delta | 0–5 kPa acceptable | Toyota/Chrysler may set DTC at 5–6 kPa; GM at 7 kPa |
| DLC ground drop | ≤0.05 V signal; ≤0.10 V chassis | All OBD-II per J1962 |
| Control-module voltage | 12.0–15.0 V | Some Euro platforms (VW/Audi) report 11.5–14.8 V |
| Lambda divergence | Δλ <0.02 healthy | Toyota A/F sensor scaling: 3.3 V = λ=1.0; 2.8 V rich / 3.8 V lean |
| Fuel trim rail | ±20–25% LTFT; ±30% STFT | GM: LTFT rails at 23–25%; Ford: 20–25%; Toyota: 25% |
| O2 transition time | <150 ms healthy | 849 ms = Toyota/Chrysler P0133/P0153 adaptation limit; GM uses 300–500 ms thresholds |
| A/F sensor voltage | 0–5 V wideband; 3.3 V stoic | Toyota: 2.4–4.8 V range; stoic = 3.3 V; other widebands may use 2.35 V stoic |


## Bands-to-Change Shortlist

| Signal | Current | Proposed | Justification |
|--------|---------|----------|---------------|
| **DLC ground drop** | ≤0.20 V ok | ≤0.05 V signal ground; ≤0.10 V chassis; 0.20 V = absolute max under full load | Industry standard is 50–100 mV |
| **Control-module voltage** | ≥12.0 (12.4–12.8 rest) | Add 13.8–14.4 V running; <11.5 V = low | Alternator-regulated range |
| **O2 transition time** | fault ~849 ms | Tag as **OEM-specific (Toyota/Chrysler)**; generic fault >300 ms | 849 ms is adaptation timer, not universal threshold |
| **Fuel trim normal** | ±10% | Add ±5–10% as ideal; ±20–25% as rail | Multiple sources confirm |
| **A/F sensor voltage** | Not in matrix | Add: Toyota 3.3 V stoic; 2.8 V rich / 3.8 V lean | Critical for Toyota/Chrysler platforms |


## Distribution Guidance

| Signal | Distribution | σ / P10–P90 | Sampling Recommendation |
|--------|--------------|-------------|------------------------|
| KOEO MAP−BARO delta | Normal (Gaussian) | σ ≈1.5 kPa; P10–P90: 0–3 kPa | Sample 0–5 kPa; mark ≥5 as fault |
| DLC ground drop | Skewed-right (log-normal) | P10: 5 mV; P90: 45 mV | Most mass near 10–30 mV; 50 mV = caution; 100 mV = warn |
| Control-module voltage | Bimodal | Rest: 12.4–12.8 V; Running: 13.8–14.4 V | Sample two modes separately |
| Lambda divergence | Normal | σ ≈0.005–0.010 | 0.00–0.02 healthy; ≥0.05 fault |
| Fuel trim | Normal (clipped) | σ ≈5%; P10–P90: −15% to +15% | Clip at ±25%; mark >+50% as mismatch |
| O2 transition time | Normal (right-skewed) | New: 50–100 ms; Aged: 100–150 ms | Sample 50–300 ms; >300 ms = degraded |


## Source Evidence Summary

| Signal | Standard / Source | Evidence |
|--------|-------------------|----------|
| MAP/BARO | SAE J1979 / OEM practice | MAP sensor resolution limited by J1979 spec; KOEO MAP ≈ baro |
| DLC ground | SAE J1962 / Snap-On manual | ≤0.1 V ignition-on; ≤50 mV signal ground |
| Fuel trim | OBD-II generic / MOTOR | LTFT rails at 20–25%; STFT can reach ±30% |
| O2 response | Mode $06 / OEM DTC | Healthy <150 ms; P0133 threshold varies by OEM |
| A/F sensor | Toyota service | 3.3 V stoic; 2.8 V rich / 3.8 V lean |


## Citation Key

- **Standardized**: SAE J1979, J1962, ISO 15031 (OBD-II PID definitions, DLC pinout)
- **Manufacturer-typical**: MOTOR Magazine empirical data across multiple makes
- **OEM-specific**: Toyota A/F sensor 3.3 V scaling; Chrysler/Toyota P0133 849 ms threshold
- **Anecdotal / forum**: Indicated where used; not primary evidence