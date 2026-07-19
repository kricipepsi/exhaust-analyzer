# Value-Confirmation Prompt — Cluster 9: confirming "no fault" reliably
*Focused companion to `research_answers/cluster9.1.md` + `cluster9.2.md`. The evidence set, decision rule, and a full signature table are established — **do not re-derive**. Answer ONLY the real-world **healthy-band values, tolerances, distributions** so provisional synthetic "healthy" data can be confirmed/corrected. Self-contained; copy below the line.*

---
### Role ###
Emissions/OBD **measurement-calibration** expert (I/M pass criteria, fuel-trim norms, Mode $06 margins, readiness). Numbers, ranges, tolerances, citations only.

### Already established in cluster9 — DO NOT re-answer ###
No-fault requires the JOINT set (any miss → ABSTAIN): all readiness monitors complete; no DTCs (confirmed/pending/permanent); Mode $06 margin ≥ 10% of limit range. Accepted healthy bands:
- STFT ±5%; LTFT ±10% (idle & 2500). Δtrim idle→2500 ≤ ±5%.
- O2 transition < 150 ms; amplitude min < 0.2 V, max > 0.8 V (osc 0.1–0.9 V).
- Idle 5-gas: HC ≤ 35 ppm (≤ 50 tolerable), CO 0.1–0.45%, CO2 14.5–16.0%, O2 < 1.0%.
- Two-point gas delta idle→2500: ΔHC ≤ +20 ppm, ΔCO ≤ +0.2%, ΔCO2 ≥ −0.5%, ΔO2 ≤ +0.5%.

### What we need — VALUES ONLY ###
For each healthy band: **confirmed central · range (min–max) · fleet spread (P10–P90/±σ) · distribution · verdict** (CONFIRM/WIDEN/TIGHTEN/SHIFT/REJECT). Units required. The point is the realistic **spread of genuinely healthy vehicles** so synthetic "no_fault" cases aren't unnaturally tight.
| Band | Established | Give range · spread · distribution |
| --- | --- | --- |
| STFT / LTFT healthy (%) | ±5 / ±10 | ? (real distribution around 0; how often healthy cars sit at ±7 LTFT) |
| Δtrim idle→2500 (pts) | ≤ ±5 | ? |
| O2 transition (ms) / amplitude (V) | <150 / 0.2–0.8 | ? healthy spread |
| Idle HC/CO/CO2/O2 | 35/0.1–0.45/14.5–16.0/<1.0 | ? real healthy spread per gas |
| Two-point gas deltas | ΔHC≤20, ΔCO≤0.2, ΔCO2≥−0.5, ΔO2≤0.5 | ? |
| Mode $06 margin (%) | ≥10 of limit range | ? typical healthy margin distribution |
| Warm-up cycles / miles since clear | (for confidence) | thresholds where readiness is trustworthy |

### Explicit framing ###
This is the **negative class** — we need the healthy population's realistic scatter, not a fault threshold. Flag any band that is an I/M **regulatory cut** (standardized) vs a workshop norm (anecdotal). Note engine-size / model-year dependence of the idle-gas bands.

### Output format ###
Confirmation matrix (`band | central | range | spread | distribution | standardized-or-anecdotal | verdict | citation`) + which healthy bands are too tight/wide + distribution guidance (healthy trims are ~normal about 0; gases skewed?).

### Source & evidence standards ###
EPA/CARB/BAR I/M standards (idle-gas cutpoints, readiness), SAE J1979/ISO 15031-5 (Mode $06, trim PIDs), OEM service. Tag each **standardized / manufacturer-typical / anecdotal**.

### Vehicle scope ###
Petrol light-duty, mixed makes/model-years (~2000–2024). State model-year dependence (tighter modern emissions → narrower healthy bands).

### Constraint ###
Numeric + tolerance-first; petrol; practically-acquirable (OBD Mode $01/$06 Tier-a; 5-gas Tier-b).
