# Value-Confirmation Prompt — Cluster 6: sensor under-detection (lazy/biased O2, under-reading MAF)
*Focused companion to `research_answers/cluster6.md`. The discriminator combination, physics, and feasibility are established — **do not re-derive**. cluster6.md explicitly found **public numeric thresholds are sparse**; this prompt asks ONLY for those missing **value bands, tolerances, distributions**. Self-contained; copy below the line.*

---
### Role ###
Emissions/OBD **measurement-calibration** expert (O2-sensor response dynamics, Mode $06 monitor scaling, MAF plausibility). Numbers, ranges, tolerances, citations only.

### Already established in cluster6.md — DO NOT re-answer ###
Separation is on **dynamics, not static magnitude**. Discriminator = Mode $06 O2 monitor vs its own min/max limits + forced rich↔lean timing fallback; plus MAF measured-vs-calculated airflow at warm idle & 2500 rpm no-load. Cross-counts demoted (no universal floor); heater demoted; static single value rejected. Anchors already accepted: Bosch HFM ±4% accuracy, ≤20 ms time constant; CARB fuel-shutoff rich→lean check from ~0.7 V; MAF sustained deviation >10–15% vs model = provisional fault (empirical-inferred); heater light-off ~30 s (rough).

### What we need — VALUES ONLY (the sparse layer cluster6 could not pin) ###
For each: **healthy central · fault threshold · range · fleet spread (±σ/P10–P90) · distribution · verdict**. Units required. Mark each **standardized / manufacturer-typical / empirical**.
| Signal | What to quantify |
| --- | --- |
| O2 rich→lean transition time (ms) | healthy vs lazy fail-line; range + spread. Narrowband vs wideband separately. |
| O2 lean→rich transition time (ms) | same; note asymmetry (CARB distinguishes symmetric/asymmetric) |
| O2 switch rate / cross-counts (Hz) at idle | healthy vs lazy band, even if only secondary |
| MAF measured-vs-calculated deviation (%) | confirm/correct the 10–15% provisional fault band + spread; idle vs 2500 |
| MAF absolute error masking-limit (%) | how much bias closed-loop trim hides before it shows |
| Heater light-off / activity time (s) | healthy vs faulted band |

### Explicit framing (from cluster6) ###
cluster6 concluded exact O2 ms fail-lines are **vehicle-specific (read Mode $06 limits)** — so where a universal number doesn't exist, give the **representative range + how much it varies by sensor type/OEM**, and say so. Narrowband vs wideband must be split. State where honest abstention is the only correct answer.

### Output format ###
Confirmation matrix (`signal | healthy | fault threshold | range | spread | distribution | class | verdict | citation`) + which numbers are genuinely universal vs vehicle-specific + distribution guidance.

### Source & evidence standards ###
SAE J1979/J1979-2 (Mode $06 O2-monitor test IDs & scaling), CARB OBD II response-rate definitions, Bosch/DENSO component data, peer-reviewed. Tag every number **standardized / manufacturer-typical / empirical**. Prioritise upgrading the O2 ms fail-line and the 10–15% MAF band above their current empirical status if a stronger source exists.

### Vehicle scope ###
Petrol light-duty, mixed makes/model-years (~2000–2024); narrowband and wideband O2; MAF-equipped (speed-density → MAF branch N/A). State sensor-type and make dependence.

### Constraint ###
Numeric + tolerance-first; petrol; practically-acquirable (Mode $06 Tier-a; scope Tier-c for ms timing). Note where only the vehicle's own monitor band applies.
