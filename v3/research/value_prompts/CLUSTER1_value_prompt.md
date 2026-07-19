# Value-Confirmation Prompt — Cluster 1: mechanical compression loss vs ignition misfire vs coolant intrusion
*Focused companion to `research_answers/cluster1.md`. That research already fixed the mechanisms, the discriminating tests, and central thresholds — **do not re-derive them**. Answer ONLY the real-world numeric **value bands, tolerances, and distributions** per fault, so a provisional synthetic dataset can be confirmed or corrected. Self-contained; copy everything below the line.*

---
### Role ###
Automotive emissions/OBD **measurement-calibration** expert. Give numbers, ranges, tolerances, citations — not mechanism explanations (already established).

### Already established in cluster1.md — DO NOT re-answer ###
The discriminating set (Mode $06 misfire + freeze-frame, cooling-headspace HC, in-cylinder pressure, two-point idle→2500 HC), the physics, and these **central** signatures are already accepted:
- Cranking compression: healthy >90 psi; mechanical loss <90 psi. Running compression: healthy 65–90 psi; mech loss <65 psi.
- Cooling-headspace HC: healthy 0 ppm; coolant intrusion >50 ppm (often >500).
- Tailpipe HC: healthy <100 ppm; mechanical 100–300 ppm; misfire >500 ppm/cyl.
- Tailpipe O2: healthy <1%; mechanical 1–2%; single-cyl misfire ~5% (4-cyl).
- Tailpipe CO2: healthy 14–15%; mech/misfire 10–12%.
- Relative-compression starter current: 100–200 A avg, ~500 A inrush; >90% uniformity = false pass.
- NDIR/FID HC ratio: ~1.0 raw fuel vs <0.4 oil (lab-only). Two-point HC decays (valve seal) vs stays elevated at 2500 (rings). Snap-throttle rejected.

### What we need — VALUES ONLY ###
For each signal × cause below, supply: **confirmed central value · realistic range (min–max) · fleet spread (P10–P90 or ±σ) · distribution shape · a verdict** (CONFIRM / WIDEN / TIGHTEN / SHIFT / REJECT) against the established number. Units required. We seed tolerance-wide synthetic data, so the **spread across vehicles** matters more than a single point.
| Signal | Cause | Established central | Give: range · spread · distribution |
| --- | --- | --- | --- |
| Cranking compression (psi) | healthy / mech-loss | >90 / <90 | ? |
| Running compression (psi) | healthy / mech-loss | 65–90 / <65 | ? |
| Cooling-headspace HC (ppm) | coolant intrusion | >50 (often >500) | ? (spread + how high it realistically goes) |
| Tailpipe HC (ppm) | healthy / mech / misfire | <100 / 100–300 / >500 per cyl | ? |
| Tailpipe O2 (%) | healthy / mech / misfire | <1 / 1–2 / ~5 | ? (and O2 spread per # of misfiring cyls) |
| Tailpipe CO2 (%) | healthy / mech / misfire | 14–15 / 10–12 | ? |
| Mode $06 misfire counts | mech (idle-only) / ignition (load) / coolant (cold-start<30s) | qualitative | approx count ranges + spread |

### Specific gaps cluster1.md flagged — resolve if evidence exists ###
Synthetic-oil NDIR/FID response factors (PAO/Grp III–IV); temperature gradient that opens microscopic head-gasket fissures (false-negative threshold); NDIR bench settling time on modern low-emission vehicles.

### Output format ###
1. Confirmation matrix: `signal | cause | central | range | spread (P10–P90/±σ) | distribution | verdict | citation`.
2. Bands-to-change shortlist (which established numbers are off, and by how much).
3. Distribution guidance (where to sample non-uniform).

### Source & evidence standards ###
Prefer SAE J1979/J1979-2, ISO 15031, EPA/CARB I/M, OEM service data, peer-reviewed, Pico/ATS/Horiba measurement literature. Tag every number **standardized / manufacturer-typical / anecdotal**; upgrade any anecdotal figure with a stronger source or flag it.

### Vehicle scope ###
Petrol light-duty, mixed makes and model years (~2000–2024), 3–8 cyl. State where a band depends on displacement/cylinder count (e.g. the O2 misfire spike scales with 1/#cyl).

### Constraint ###
Deliverable is **numeric + tolerance-first** (ranges and spreads, not directions). Petrol, practically-acquirable signals; note lab-only only to bound it.
