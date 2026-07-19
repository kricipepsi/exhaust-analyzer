# Value-Confirmation Prompt — Cluster 3: ECU / control-reference fault vs true chemistry deviation
*Focused companion to `research_answers/cluster3.md` (+ `cluster3_prepped.md`). The discriminators, physics, protocol, and many thresholds are established — **do not re-derive**. Answer ONLY the real-world **value bands, tolerances, distributions** so provisional synthetic values can be confirmed/corrected. Self-contained; copy below the line.*

---
### Role ###
Powertrain-control / OBD **measurement-calibration** expert (fuel-trim adaptation, sensor-reference/ground offsets, gas-vs-OBD divergence). Numbers, ranges, tolerances, citations only.

### Already established in cluster3.md — DO NOT re-answer ###
Discriminator ladder: KOEO MAP-vs-BARO plausibility → DLC ground-drop under load → closed-loop gas-vs-OBD lambda divergence → active bidirectional. Accepted centrals:
- KOEO MAP−BARO delta: **< 5 kPa** plausible; ≥ 5 kPa (e.g. 6 kPa) = electrical/reference fault. Control-module voltage ≥ 12.0 V (rest 12.4–12.8 V).
- DLC signal-ground drop under load: **≤ 0.2 V** ok; > 0.2 V = ground offset.
- Gas-vs-OBD lambda divergence: **Δλ ≥ 0.05** = control-loop (chemistry moves opposite to OBD command).
- Fuel trim: ±10% = active compensation; combined **> +50%** = mismatched/biased sensor (false P0171/P0174). Bidirectional ±25% injector step.
- O2 response: healthy transition **< 150 ms**; P-jump adaptation **849 ms** sets P0133/P0153. (OEM examples: Toyota A/F 3.3 V ±0.3 V, <2.8 V rich / >4.0 V lean; Siemens downstream/upstream ratio > 0.3 → P0420.)

### What we need — VALUES ONLY ###
For each: **confirmed central · range · fleet spread (±σ/P10–P90) · distribution · verdict** (CONFIRM/WIDEN/TIGHTEN/SHIFT/REJECT). Units required. Separate **generic** bands from **OEM-specific** ones.
| Signal | Established | Give range · spread · distribution |
| --- | --- | --- |
| KOEO MAP−BARO delta (kPa) | <5 ok / ≥5 fault | ? (normal sensor scatter at KOEO) |
| DLC/signal-ground drop under load (V) | ≤0.2 ok | ? (and the >0.10 V per-joint sub-band) |
| Control-module voltage (V) | ≥12.0 (12.4–12.8 rest) | ? loaded vs rest spread |
| Gas-vs-OBD lambda divergence (Δλ) | ≥0.05 = control | ? healthy scatter vs fault |
| Fuel trim "railed" (%) | ±25% limit; >+50% mismatch | ? distribution near the rails |
| O2 transition time (ms) | healthy <150; fault ~849 adapt | ? healthy band + fault fleet spread |
| Bidirectional fuel response | ±25% command → chemistry step | expected % chemistry response (bool if reversed) |

### Explicit framing ###
Much of cluster3's precision is **OEM-specific** (Toyota/Chrysler/Siemens examples). Give the **generic** confirmable band per signal AND flag which numbers only hold for specific platforms, so synthetic sampling uses generic bands with OEM outliers noted.

### Output format ###
Confirmation matrix (`signal | central | range | spread | distribution | generic-or-OEM | verdict | citation`) + bands-to-change shortlist + distribution guidance.

### Source & evidence standards ###
SAE J1979/J1979-2 (Mode $06 TID/CID O2-response & the trim/MAP/BARO PIDs), ISO 15031, OEM service (ground-drop specs, A/F-sensor scaling), peer-reviewed. Tag each **standardized / manufacturer-typical / anecdotal**.

### Vehicle scope ###
Petrol light-duty, mixed makes/model-years (~2000–2024); narrowband, wideband, and A/F-sensor platforms. State make dependence explicitly.

### Constraint ###
Numeric + tolerance-first; petrol; practically-acquirable (OBD live PIDs Tier-a; DMM/breakout & bidirectional scan tool Tier-c).
