# Value-Confirmation Prompt — Cluster 2: rich mixture vs catalyst failure
*Focused companion to `research_answers/cluster2.md`. Mechanisms, the discriminating signals, and central thresholds are already established — **do not re-derive**. Answer ONLY the real-world numeric **value bands, tolerances, distributions** per fault so our drafted synthetic bands can be confirmed/corrected. Self-contained; copy below the line.*

---
### Role ###
Emissions/OBD **measurement-calibration** expert (fuel trims, Mode $06 catalyst monitor scaling, OSC). Numbers, ranges, tolerances, citations — no mechanism prose.

### Already established in cluster2.md — DO NOT re-answer ###
Fuel trim is the gateway; catalyst OSC / Mode $06 index / decel 5-gas discriminate; thresholds accepted: **Total fuel trim ≤ −10% = rich**; **Mode $06 index ratio ≤ 0.20 = healthy cat**; **Δt_osc < 0.5 s = failed cat**; **decel CO > 0.8% = failed**; **ground-drop ≤ 50 mV** integrity gate; misfire/heater pre-gate voids the read.

### Provisional synthetic bands to CONFIRM (already drafted from cluster2 + quick web) ###
Critically confirm or correct each — these currently rest on repair-blog sources.
| Signal | Fault | Provisional band |
| --- | --- | --- |
| Total fuel trim, idle | rich_mixture | −25% … −12% |
| Total fuel trim, idle | catalyst/normal | −7% … +7% |
| Total fuel trim, idle | lean (confounder) | +12% … +26% (corrects at 2500) |
| Total fuel trim, idle | sensor skew | −8% … +16% (erratic) |
| Mode $06 catalyst index ratio | healthy | 0.05 … 0.18 |
| Mode $06 catalyst index ratio | failed | 0.55 … 0.90 |
| Mode $06 catalyst index ratio | O2/ground skew | 0.28 … 0.55 (false-pos) |
| Decel tailpipe CO (%) | healthy / failed | 0.05–0.60 / 0.90–2.20 |
| Pre→post-cat HC reduction (%) | healthy / failed | 70–90 drop / <15 drop |
| Pre→post-cat CO reduction (%) | healthy / failed | 70–90 drop / <15 drop |

### What we need — VALUES ONLY ###
For each row: **confirmed central · range (min–max) · fleet spread (P10–P90 or ±σ) · distribution shape · verdict** (CONFIRM/WIDEN/TIGHTEN/SHIFT/REJECT). We sample tolerance-wide, so give the realistic **spread** and whether the correct-vs-confusable separation is clean or overlapping in the tails.

### Specific value questions cluster2.md leaves open ###
- Mode $06 index ratio is noted to **vary by vehicle** — give the real OEM/standard range and how much it varies by make.
- Post-Mode-$04-clear default values contaminate the read — is there a documented settling/warm-up-cycle count before the monitor is trustworthy?
- STFT vs LTFT split for a true rich fault (how much sits in each at idle vs 2500).

### Output format ###
Confirmation matrix (`signal | fault | central | range | spread | distribution | verdict | citation`) + bands-to-change shortlist + distribution guidance.

### Source & evidence standards ###
SAE J1979-2 (Mode $06 test-value scaling), ISO 15031, EPA/CARB I/M, OEM emissions spec, peer-reviewed. Tag each number **standardized / manufacturer-typical / anecdotal**; explicitly seek standardized/OEM confirmation for the ±10% trim norm, the 0.20 index, and the 0.8% decel-CO cut (currently anecdotal).

### Vehicle scope ###
Petrol light-duty, mixed makes/model-years (~2000–2024), closed-loop three-way-cat. Note make dependence of the index ratio.

### Constraint ###
Numeric + tolerance-first; petrol; practically-acquirable (generic OBD Mode $01/$06, standard 5-gas). Lab-only only to bound it.
