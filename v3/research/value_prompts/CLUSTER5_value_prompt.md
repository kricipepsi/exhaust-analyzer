# Value-Confirmation Prompt — Cluster 5: lean root cause (vacuum leak vs fuel delivery vs MAF under-read)
*Focused companion to `research_answers/cluster5.md`. Mechanisms, the multi-point protocol, and central thresholds are established — **do not re-derive**. Answer ONLY the real-world numeric **value bands, tolerances, distributions** per sub-cause so provisional synthetic values can be confirmed/corrected. Self-contained; copy below the line.*

---
### Role ###
Emissions/OBD **measurement-calibration** expert (fuel-trim analytics, MAF/MAP, calculated load, λ). Numbers, ranges, tolerances, citations only.

### Already established in cluster5.md — DO NOT re-answer ###
The discriminator is the multi-point trim/load/λ behaviour across idle → 2500 → WOT. Accepted centrals:
- Lean declared: λ > 1.03 or Total Fuel Trim (STFT+LTFT) ≥ +15%. Idle MAF 2.0–5.0 g/s; idle MAP ~30–35 kPa.
- **Vacuum leak:** idle TFT ≈ +20–30%, ΔTFT(idle→2500) drop ≥ +15%, recovers by 2500 (speed-density NA: ~neutral trims).
- **Fuel delivery:** rail target 45–60 psi (310–414 kPa); drop > 5 psi (35 kPa) under load; λ > 1.05 at WOT (fails to enrich).
- **MAF under-read:** peak Calculated Load (PID 04) < 80% (typ 60–70%) at WOT; positive trims across all ranges.
- Turbo boost leak: STFT −10 to −20% under boost.

### What we need — VALUES ONLY ###
For each signal × sub-cause: **confirmed central · range (min–max) · fleet spread (P10–P90 or ±σ) · distribution · verdict** (CONFIRM/WIDEN/TIGHTEN/SHIFT/REJECT). Units required.
| Signal | Sub-cause | Established | Give range · spread · distribution |
| --- | --- | --- | --- |
| Idle TFT (%) | vacuum leak | +20–30 | ? |
| ΔTFT idle→2500 (pts) | vacuum leak | ≥ +15 drop | ? (how fully it recovers) |
| Rail pressure drop under load (psi/kPa) | fuel delivery | >5 psi / 35 kPa | ? |
| λ at WOT | fuel delivery | >1.05 | ? |
| Peak Calculated Load (%) at WOT | MAF under-read | <80 (60–70) | ? |
| TFT across range (%) | MAF under-read | positive all ranges | ? (idle vs load magnitudes) |
| STFT under boost (%) | turbo boost leak | −10 to −20 | ? |
| Idle MAF (g/s) / MAP (kPa) | baseline | 2–5 / 30–35 | ? spread |

### Specific gap cluster5.md flagged ###
High-altitude behaviour of Calculated Load (PID 04) and the universality of the 80% WOT threshold across OEMs/elevations — give elevation- and OEM-dependent bands if evidence exists.

### Output format ###
Confirmation matrix (`signal | sub-cause | central | range | spread | distribution | operating-point | verdict | citation`) + bands-to-change shortlist + distribution guidance.

### Source & evidence standards ###
SAE J1979 (PID 04 LOAD_PCT formula, fuel-trim PIDs), ISO 15031, OEM spec, peer-reviewed. Tag each number **standardized / manufacturer-typical / anecdotal**.

### Vehicle scope ###
Petrol light-duty, mixed makes/model-years (~2000–2024): MAF-NA, speed-density-NA, and turbo. State induction-type dependence explicitly (the sub-cause signatures differ by architecture).

### Constraint ###
Numeric + tolerance-first; petrol; practically-acquirable (generic OBD live PIDs; fuel gauge Tier-c only where no rail-pressure PID).
