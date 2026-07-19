# Value-Confirmation Prompt — Cluster 4: exhaust leak vs true lean vs biased O2 sensor
*Focused companion to `research_answers/cluster4.md`. The discriminators, physics, and thresholds are established — **do not re-derive**. C4 reuses C5 trim/load + C6 O2-dynamics columns but has its OWN separating values; answer ONLY those **value bands, tolerances, distributions**. Self-contained; copy below the line.*

---
### Role ###
Emissions/OBD **measurement-calibration** expert (fuel trim vs load, exhaust dilution chemistry, up/down O2 cross-check). Numbers, ranges, tolerances, citations only.

### Already established in cluster4.md — DO NOT re-answer ###
Discriminator order: two-point ΔTrim (idle→2500, architecture-gated) → CO2-depression/O2-elevation dilution → O2 waveform vs load → up/down O2 cross-check → smoke/propane. Accepted centrals:
- Healthy λ 0.995–1.005; upstream O2 osc 0.1–0.9 V; total trim ±10%; >+20% (2 cycles) = lean.
- **Two-point ΔTrim:** leak → STFT falls ≥ 8–10 pts toward 0 at 2500; true-lean/bias → stays elevated (Δ < 3–5 pts). ΔSTFT ≥ 8% = leak, < 5% = fuel/sensor.
- **CO2 dilution (exhaust leak):** CO2 < 12–13% with O2 > 2–3% above expected; **~5% air dilution per +1.0% O2**.
- **Up vs down O2:** downstream O2 > 0.6–0.7 V with positive upstream trims = sensor-bias suspect.
- Propane: ≥ 20% negative trim shift = sensor responsive. Smoke test = boolean.

### What we need — VALUES ONLY ###
For each signal × cause (exhaust-leak / true-lean / biased-O2): **confirmed central · range · fleet spread (±σ/P10–P90) · distribution · verdict**. Units required.
| Signal | Cause | Established | Give range · spread · distribution |
| --- | --- | --- | --- |
| Two-point ΔSTFT (pts) | exhaust leak | ≥8–10 fall | ? (leak-size dependence) |
| Two-point ΔSTFT (pts) | true lean / bias | <3–5 | ? |
| CO2 at idle (%) | exhaust leak | <12–13 | ? vs leak size |
| O2 elevation (%) | exhaust leak | +2–3 above | ? (confirm 5%-air-per-1%-O2) |
| Downstream O2 (V) | biased upstream O2 | >0.6–0.7 | ? |
| Propane trim shift (%) | healthy vs lazy O2 | ≥20 neg | ? |

### Specific gaps cluster4.md flagged — resolve if evidence exists ###
ΔTrim threshold **specific to exhaust leaks** (vs intake vacuum leaks) by leak size; speed-density/turbo calibration; CO2-depression-vs-leak-size quantification; O2-bias-vs-true-lean forced-enrichment response.

### Output format ###
Confirmation matrix (`signal | cause | central | range | spread | distribution | verdict | citation`) + bands-to-change shortlist + distribution guidance. Note where C4 shares a column with C5/C6 (so the same band serves both).

### Source & evidence standards ###
SAE J1979 (trim/O2 PIDs), EPA/BAR I/M (idle-gas), OEM/professional service (ΔTrim practice, dilution notes). Tag each **standardized / manufacturer-typical / anecdotal** (the ΔTrim and CO2<12% rules are currently anecdotal/textbook — seek stronger).

### Vehicle scope ###
Petrol light-duty, mixed makes/model-years (~2000–2024); MAF-NA, speed-density, turbo. State architecture dependence of the ΔTrim signature.

### Constraint ###
Numeric + tolerance-first; petrol; practically-acquirable (OBD live PIDs Tier-a; 5-gas Tier-b; smoke/propane Tier-c).
