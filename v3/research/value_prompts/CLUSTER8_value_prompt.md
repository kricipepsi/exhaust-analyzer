# Value-Confirmation Prompt — Cluster 8: non-starter root cause
*Focused companion to `research_answers/cluster8.md`. The discriminators, protocol, and a full signature table are established — **do not re-derive**. Answer ONLY the real-world **value bands, tolerances, distributions** per no-start cause so provisional synthetic values can be confirmed/corrected. Self-contained; copy below the line.*

---
### Role ###
Automotive **measurement-calibration** expert (cranking-phase diagnostics, fuel pressure, CKP/immobiliser). Numbers, ranges, tolerances, citations only.

### Already established in cluster8.md — DO NOT re-answer ###
Five no-start causes (spark / fuel / mixture / compression-CKP / immobiliser); 5-gas unavailable (no exhaust). Accepted signature table:
- Relative compression: any cylinder < 85% of best, or spread > 15% = mechanical.
- Cranking vacuum: > 3 inHg (~10 kPa) ok; < 3 = insufficient pumping.
- Fuel pressure KOEO: 270–310 kPa (38.5–44 psi); < 270 = delivery fault. Cranking: 200–240 kPa (28.5–34 psi).
- Injector pulse width, cranking: 3–6 ms; 0 = ECU/immobiliser.
- Engine RPM, cranking: 150–300 RPM; 0 with starter turning = CKP loss.
- Immobiliser: DTCs P0513/P1611/U0167, dash lamp steady during crank. Battery > 12.0 V static, > 10.5 V cranking.

### What we need — VALUES ONLY ###
For each signal × cause: **confirmed central · range (min–max) · fleet spread (P10–P90/±σ) · distribution · verdict** (CONFIRM/WIDEN/TIGHTEN/SHIFT/REJECT). Units required. Note where a value is a hard pass/fail (bool: spark present, immobiliser active) vs a continuous band.
| Signal | Cause | Established | Give range · spread · distribution |
| --- | --- | --- | --- |
| Relative compression (% of best) | mechanical | <85 / spread>15 | ? |
| Cranking vacuum (inHg) | compression/pumping | >3 ok | ? spread + displacement dependence |
| KOEO fuel pressure (kPa/psi) | fuel delivery | 270–310 / 38.5–44 | ? (OEM spread across platforms) |
| Cranking fuel pressure (kPa) | fuel delivery | 200–240 | ? |
| Injector pulse width, cranking (ms) | ECU/immobiliser | 3–6; 0=fault | ? spread by engine family + temp |
| Cranking RPM | CKP | 150–300; 0=loss | ? spread |
| Spark present / immobiliser active | ignition / security | boolean | prevalence only; keep boolean |

### Specific gaps cluster8.md flagged — resolve if evidence exists ###
Cranking injector pulse-width reference **by engine family and temperature** (current 3–6 ms is anecdotal); Mode $06 availability/interpretation during no-start; cranking-vacuum >3 inHg threshold **by displacement / cylinder count / aspiration** (no SAE/ISO standard).

### Output format ###
Confirmation matrix (`signal | cause | central | range | spread | distribution | verdict | citation`) + bands-to-change shortlist + note which stay boolean.

### Source & evidence standards ###
SAE J1979 (RPM/pulse/freeze-frame PIDs), OEM service (fuel-pressure specs, immobiliser DTCs), peer-reviewed where available. Tag each number **standardized / manufacturer-typical / anecdotal**; upgrade the anecdotal cranking pulse-width and vacuum thresholds if possible.

### Vehicle scope ###
Petrol light-duty, mixed makes/model-years (~2000–2024), varied displacement/aspiration. State displacement/aspiration dependence (esp. cranking vacuum and fuel-pressure spec).

### Constraint ###
Numeric + tolerance-first; petrol; practically-acquirable (OBD Mode $01/$03/$07 Tier-a; gauges/scope Tier-c). No idle 5-gas (engine never runs).
