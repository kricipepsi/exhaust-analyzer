# Value-Confirmation Prompt — Cluster 7: cam timing / VVT fault
*Focused companion to `research_answers/cluster7.md`. The discriminating signals, mechanisms, VE formula, and protocol are established — **do not re-derive**. cluster7.md is strong on physics but **thin on hard numeric thresholds**; this prompt asks ONLY for those **values, bands, and tolerances**. Self-contained; copy below the line.*

---
### Role ###
Powertrain/OBD **measurement-calibration** expert (VVT phaser control, cam-crank correlation, volumetric efficiency). Numbers, ranges, tolerances, citations only.

### Already established in cluster7.md — DO NOT re-answer ###
Discriminators (ranked): VVT solenoid command vs measured cam-angle tracking error; cam-to-crank correlation (P0016-class); VE delta idle→2500-load; VE/MAF-at-RPM WOT signature; P0011/P0014 freeze-frame. Idle phaser target = 0°. Retarded IVC depresses VE; lost internal EGR spikes combustion temp >2500°F (1370°C) → NOx. Pre-gates ECT≥75°C, ≥11 V, closed loop; Maneuvers A(idle)/B(WOT 1000–4500)/C(2500 rpm, 50–70% load, ≥10 Hz). VE = (AVF/TAF)×100.

### What we need — VALUES ONLY (cluster7 left these unquantified) ###
For each: **central value · fault threshold · range · fleet spread (±σ/P10–P90) · distribution · verdict**. Units required.
| Signal | What to quantify |
| --- | --- |
| VVT command-vs-actual tracking error (deg) | fault threshold (deg of lag) + healthy spread; time-to-target (ms) for a healthy phaser |
| Cam-to-crank correlation (deg) | P0016-class fault threshold (deg) + healthy tolerance band |
| Volumetric efficiency η_v (%) | healthy VE at idle & 2500-load vs retarded-cam VE; the depression magnitude (Δ%) that flags a fault |
| MAF-at-RPM (g/s) | healthy vs charge-reversion signature across the 1000–4500 sweep (approx g/s or % low) |
| Combustion temp / NOx (ppm) | NOx magnitude when internal EGR is lost vs baseline (ppm range) |
| Idle manifold vacuum stability (inHg) | any usable band for VVT-stuck vs healthy |

### Specific note ###
cluster7 states cam/VVT ≈ 25% of the unresolved hard corpus and that idle diagnosis is ineffective (phaser target 0° at idle) — so give the **loaded/2500-rpm** value separations, not idle. Flag which signals are only diagnostic off-idle.

### Output format ###
Confirmation matrix (`signal | healthy central | fault threshold | range | spread | distribution | operating-point | verdict | citation`) + which bands are firmest vs weakest evidence.

### Source & evidence standards ###
SAE J1979 (PIDs), OEM VVT/phaser service data (P0011/P0014/P0016 set-criteria), peer-reviewed VE/valve-timing research. Tag each number **standardized / manufacturer-typical / anecdotal**. Cam/VVT thresholds are often OEM-specific — give representative ranges and note make dependence.

### Vehicle scope ###
Petrol light-duty with intake or dual VVT, mixed makes/model-years (~2005–2024). State make/phaser-type dependence.

### Constraint ###
Numeric + tolerance-first; petrol; practically-acquirable (OBD live cam-angle/VE where supported; scope/OEM tool Tier-c where not).
