# Research Prompt — Real-World Value Bands & Tolerances to Confirm Synthetic Sensor Data
*Companion to `RESEARCH_PROMPT_blocking_measurements.md` (which established **which** signals discriminate). This prompt establishes **what numeric values** those signals take on real vehicles, per fault family, with tolerances — so provisional synthetic sensor data can be confirmed, tightened, widened, or shifted. Copy everything below the line into your research tool (deep-research LLM or a domain researcher). It is self-contained.*

---
### Role ###
You are an automotive emissions-and-diagnostics **measurement-calibration** expert (combustion, exhaust-gas analysis, OBD-II/SAE J1979 & J1979-2, fuel-trim behaviour, Mode $06 test-value scaling, in-shop test protocols). You write for an engineer who has **already chosen the discriminating signals** and now needs the **real-world numeric range and tolerance of each signal, per fault family**, to validate synthetic data. Assume deep familiarity with 5-gas analysis, STFT/LTFT, lambda, DTCs, freeze frame, Mode $06. Do not explain basics; give numbers, ranges, and citations.

### Background / why this prompt exists ###
A rule-based petrol diagnostic engine classifies a fault family from a warm-idle measurement set. Real per-case sensor readings do not yet exist (pre-launch), so each residual case is seeded with **provisional synthetic values** derived from its known (oracle) fault family through published signatures, deliberately **tolerance-wide** because real cars are not lab devices. We need those bands **confirmed against authoritative, real-world evidence** before they harden. For each signal below we give our current **provisional band**; your task is to critically confirm or correct it — not merely agree.

### Objective ###
For each **signal × fault-family** pair in the tables below, determine from real-world evidence:
1. the **central/typical value** on an affected vehicle;
2. the **realistic range** (give min–max and, where possible, a P10–P90 or ±tolerance spread) — capturing vehicle-to-vehicle variation, not a single lab point;
3. the **distribution shape** (roughly normal, skewed, bimodal, long-tailed) and what drives the spread (engine size, mileage, ambient, fuel, sensor age);
4. the **RPM/load/temperature dependence** (does the value hold at warm idle, or only appear at 2500 rpm / load / decel?);
5. the **decision threshold** that separates this family from its confusables, **with the uncertainty band** around that threshold;
6. a **verdict on our provisional band**: `CONFIRM` / `WIDEN` / `TIGHTEN` / `SHIFT` / `REJECT`, with the corrected band.

### Signals & provisional bands to confirm ###
Values are warm-idle unless noted. "Total trim" = STFT + LTFT. Confirm each row.

**Cluster 2 — rich mixture vs catalyst failure (worked example; bands already drafted):**
| Signal | Family | Provisional band (confirm/correct) |
| --- | --- | --- |
| Total fuel trim, idle | rich_mixture | −25% … −12% |
| Total fuel trim, idle | catalyst_failure / normal | −7% … +7% |
| Total fuel trim, idle | lean_condition | +12% … +26% (corrects toward 0 at 2500) |
| Total fuel trim, idle | sensor skew (confounder) | −8% … +16% (erratic) |
| Mode $06 catalyst index ratio (rear/front O2) | healthy cat | 0.05 … 0.18 |
| Mode $06 catalyst index ratio | failed cat | 0.55 … 0.90 |
| Mode $06 catalyst index ratio | O2/ground skew | 0.28 … 0.55 (false-positive) |
| Decel tailpipe CO% (2500→idle) | healthy / failed cat | 0.05–0.60% / 0.90–2.20% |
| Pre→post-cat HC reduction | healthy / failed | ~70–90% drop / <~15% drop |

**Cluster 5 — lean root cause (vacuum leak vs fuel delivery vs MAF):** confirm STFT/LTFT at **idle vs ~2500 vs load**, calculated load %, MAF g/s at idle & 2500, fuel-rail pressure under load, wideband λ at WOT. Give the numeric trim *pattern* per sub-cause (e.g. vacuum leak: idle trim +__%, corrects to +__% by 2500; fuel-delivery: worsens under load by __%; MAF under-read: __% split idle-vs-load).

**Cluster 6 — sensor under-detection (lazy/biased O2 or MAF):** confirm O2 rich→lean & lean→rich transition times (ms) for healthy vs lazy sensors, O2 switch/cross-count rate, and MAF actual-vs-calculated airflow % deviation (idle & 2500) that indicates a fault.

**Cluster 1 — mechanical vs misfire vs coolant intrusion:** confirm idle/2500 HC (ppm) bands per cause, relative-compression % and leak-down % fault thresholds, cooling-system headspace HC (ppm) indicating combustion-gas intrusion, and any two-point (idle vs 2500) HC/O2 signature. Critically evaluate the "valve-seal transient HC plume" claim against real evidence.

**Cluster 3 — ECU/control-reference fault:** confirm KOEO MAP-vs-BARO plausibility delta (kPa), module supply/ground voltage-drop thresholds (V) under load, gas-derived-vs-OBD lambda divergence, and fuel-trim "railed" limits (±%) that indicate control rather than chemistry.

**Cluster 8 — non-starter:** confirm cranking RPM (normal vs slow), cranking vacuum (inHg), KOEO & cranking fuel-rail pressure (kPa/psi) pass/fail, injector pulse width (ms) presence, and relative-compression % during crank per no-start root cause.

**Cluster 7 — cam timing / VVT:** confirm VVT command-vs-actual tracking-error (deg) fault threshold, cam-to-crank correlation (deg, P0016-class), and the volumetric-efficiency / MAF-at-RPM depression signature vs a healthy engine.

**Cluster 9 — confirming no-fault:** confirm the numeric "healthy" bands that jointly prove no fault — trims within ±__%, Mode $06 monitor margins (% headroom), readiness/DTC state, warm-up cycles & miles since clear needed for confidence, and two-point gas stability.

### Research questions (answer for each signal × family) ###
1. **Central value + range/tolerance:** the number and its realistic spread (min–max, P10–P90 or ±σ). State units.
2. **What drives the spread:** engine displacement, mileage/wear, ambient/altitude, fuel grade, sensor aging.
3. **Operating-point dependence:** warm idle vs 2500 rpm vs load vs decel; note if the value is only diagnostic at a specific point.
4. **Threshold + uncertainty:** the separating threshold vs the confusable family, and how sharp/fuzzy it is.
5. **Verdict on our provisional band** (where given): CONFIRM / WIDEN / TIGHTEN / SHIFT / REJECT + corrected band.
6. **Evidence:** cite authoritative sources and note each source's reliability tier.

### Required output format ###
1. **Confirmation matrix** — one row per signal × family: `signal | family | confirmed central | confirmed range (min–max) | spread (P10–P90 or ±σ) | operating point | threshold ± uncertainty | verdict | primary citation`.
2. **Per-cluster notes** — brief prose on any band we got wrong (too tight, too wide, shifted) and why, with numbers.
3. **Bands-to-change summary** — the shortlist of provisional bands that need WIDEN/TIGHTEN/SHIFT/REJECT, ranked by how far off they are.
4. **Distribution guidance** — for the top signals, the distribution shape to sample from (uniform is our current default; say where normal/skewed/bimodal is more realistic).
5. **Open gaps** — signals where authoritative numeric evidence is thin and only real-vehicle data collection will settle it; suggest a minimal data-collection plan.

### Source & evidence standards ###
- Prefer: SAE J1979 / J1979-2 (OBD PIDs & Mode $06 test scaling), ISO 15031, EPA/CARB I/M and OBD guidance, OEM service/emissions spec data, peer-reviewed combustion/emissions research, and reputable measurement-grade industry references.
- For **every** numeric band, cite the source and mark it **standardized**, **manufacturer-typical**, or **empirical/anecdotal**. Explicitly downgrade repair-forum/blog figures to "anecdotal" and seek a stronger source for the same number.
- Where our provisional band came from anecdotal web sources (fuel-trim ±10% norms, catalyst index ~0.20, decel CO cut-points), prioritise finding a standardized or OEM-grade confirmation or correction.
- Distinguish measurement science from shop folklore; flag any claim lacking solid backing.

### Constraints ###
- **Petrol** engines; practically-acquirable signals (generic OBD-II / Mode $06, standard 5-gas, common shop tools). Note lab-only methods only to bound them.
- The deliverable is **numeric**: ranges and tolerances, not qualitative direction. Where the literature only supports a direction, say so and give your best-estimate range flagged as low-confidence.
- Assume the values seed a **tolerance-wide** synthetic dataset: prefer reporting the realistic *spread* a fleet shows, not a single representative reading.
