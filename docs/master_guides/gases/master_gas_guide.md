# Master Gas Guide — 4D Petrol Diagnostic Engine

**Purpose.** A single, self-contained reference that consolidates the contents of `HC.md`, `CO.md`, `CO2.md`, `O2.md`, `NOx.md`, `gasrules1.md`, `Understanding Engine Exhaust Emissions.md`, `Understanding Catalitic Converters.md`, `lambda.pdf`, `leanmixture.pdf`, `richmixture.pdf`, `AFR.pdf`, and `enginefaults.pdf` into the inference logic that justifies every gas-by-gas reasoning sentence in the 4D test corpus. Rows in the CSV cite the rules below; this document is the citation target.

**Scope.** Petrol only (no diesel in v1). Idle and 2500 RPM tailpipe analysis with an analyser-grade probe. Lambda is the Brettschneider/Spindt computation from HC/CO/CO2/O2; AFR = λ × 14.71.

---

## 1. Combustion baseline

Ideal stoichiometric petrol combustion is `HC + O2 + N2 → H2O + CO2 + N2`, at AFR 14.71 : 1 (λ = 1.000). Real-world burn always leaks four diagnostic by-products: HC (unburned fuel), CO (partially burned fuel), free O2 (un-reacted air), and NOx (formed only above ~2500 °F under load). The job of gas analysis is to reverse-engineer what happened in the chamber from those four leakage products plus CO2 (the "good" product) and the lambda balance line.

The chemistry holds two simultaneous truths the engine must respect:

- **Balance** (lambda) — were there enough oxygen molecules for the carbon and hydrogen present? λ < 1 means rich (excess fuel), λ > 1 means lean (excess air).
- **Quality** (HC, CO2) — did the molecules actually react? A misfiring cylinder can still have correct *balance* (raw fuel + raw air come out together) so λ ≈ 1.0, while CO2 collapses and HC spikes.

A diagnosis that looks only at λ is half-blind. A diagnosis that looks only at HC and CO is half-blind in the opposite direction. The 4D engine must read both axes.

---

## 2. Per-gas behaviour cheat sheet

### HC — Hydrocarbons (ppm)

Unburned fuel. Approximate physics: 1 % wasted fuel ≈ 200 ppm HC. Rises whenever combustion is interrupted (ignition miss, lean misfire, mechanical leakage past valves/rings, EGR over-dilution) or whenever raw fuel is delivered without burning (very rich rich-misfire, leaking injector during overrun). Catalysts mask HC by oxidising it post-cat, so a "normal" tailpipe HC on a vehicle with a working three-way cat does not prove the engine is healthy. A truly *high* tailpipe HC (≥500 ppm at idle) almost always means combustion was incomplete — the cat is either failed or being overwhelmed.

Mental model used in the reasoning column:
- HC ≤ 50 ppm → clean burn or good cat scrubbing.
- HC 50–250 ppm → minor inefficiency; could be pre-cat normal or marginal misfire.
- HC 250–800 ppm → real combustion problem (lean misfire, vacuum leak, ignition).
- HC > 800 ppm → severe misfire, oil-burning, or catalyst failure.
- HC > 2000 ppm → almost always mechanical (rings, valve sealing) or hard ignition fault.

### CO — Carbon monoxide (%)

Partially burned fuel. CO exists if and only if combustion happened but ran out of oxygen. CO is therefore a one-way rich indicator. CO ≈ 0 does not prove lean (a clean stoich burn also reads near zero) — but CO > ~1.5 % effectively guarantees rich. The catalyst oxidises CO into CO2 when O2 is available, so a rich engine with a healthy three-way cat can still show low tailpipe CO; in that case the rich condition shows up via λ from the analyser plus the OBD trims.

Cut points:
- CO ≤ 0.5 % → consistent with stoich or catalyst clean-up.
- CO 0.5–1.5 % → mild rich, or pre-cat normal.
- CO 1.5–3 % → clear rich.
- CO > 3 % → very rich; expect concurrent HC rise once rich-misfire threshold is crossed.

### CO2 — Carbon dioxide (%)

End-product of *complete* combustion. The "north star" of efficiency: anything that disturbs combustion — rich, lean, misfire, exhaust leak diluting the sample — drops CO2 below its theoretical 15.5 % ceiling. CO2 typically rises 1–2 % from idle to 2500 RPM as turbulence improves the burn. Whenever a row shows CO2 below ~13 %, the reasoning column must explain *why* (rich-fuel, lean-misfire, dilution, or sample leak) — CO2 collapse never happens by itself.

Reference levels (idle, healthy):
- ≥ 14.5 % with cat, ≥ 13 % without cat.
- 11–13 % at idle indicates a real combustion deficit.
- < 11 % is severe — large rich, large lean misfire, or analyser/sample dilution.

### O2 — Oxygen (%)

Free oxygen left after combustion. Ambient air ≈ 20.9 %, healthy tailpipe ≤ 1.5 % (without secondary air injection). O2 climbs sharply once λ > 1 because there is no fuel left to consume it. O2 is the most truthful **post-catalyst** mixture indicator because the cat does not consume O2 the way it consumes HC/CO. Air leaks (exhaust manifold, gasket, sample probe) inject ambient O2 and falsely raise the lean reading.

Cut points used by the reasoning column:
- O2 < 0.5 % → rich or perfect stoich.
- O2 0.5–1.5 % → typical pre-cat or mild lean.
- O2 1.5–4 % → clearly lean or misfire.
- O2 > 4 % → severe lean, big misfire, or air leak.
- O2 ≈ 20.9 % with HC=0, CO=0, CO2 ≈ 0.04 % → no combustion (cranking-only / non-starter).

### NOx — Oxides of nitrogen (ppm, 5-gas only)

Forms when peak combustion temperature exceeds ~2500 °F (~1370 °C). Only seen in meaningful quantities under **load** — at idle NOx is typically near 0 ppm. Peaks near stoichiometric under light load; suppressed by both rich mixtures (cooling effect of unburned fuel) and EGR (inert gas dilutes the charge). A 4-gas analyser reports NOx = 0 because it does not measure the channel; the engine must distinguish *zero-because-unmeasured* from *zero-because-rich*. Idle NOx above ~1000 ppm at idle is unusual and points to lean idle, EGR stuck, or cooling-system overheating.

### λ (Brettschneider lambda)

Calculated from HC/CO/CO2/O2 by the analyser. λ = 1.000 ⇔ AFR = 14.71. Property of *balance*, not quality. Lambda is immune to misfire (the residual fuel and air come out balanced) but is **sensitive to exhaust air leaks** — a 5 % air leak shifts a true 1.000 to 1.050 lean. Lambda is the truth axis the engine uses against the ECU's "perception" lambda from the upstream O2 sensor: when they disagree by more than ~0.05–0.08, the engine raises a contradiction symptom (false-lean or false-rich).

Window the engine uses:
- λ ≤ 0.95 → rich.
- 0.95 < λ < 0.97 → mild rich / borderline.
- 0.97 ≤ λ ≤ 1.03 → in the catalyst window.
- 1.03 < λ < 1.05 → mild lean / borderline.
- λ ≥ 1.05 → lean.
- λ ≥ 1.30 + low CO2 + high O2 → cranking / no-combustion / severe leak.

---

## 3. Inter-gas dependency rules (used as the reasoning grammar)

These rules collapse the source documents into the short justifications used in the CSV:

1. **CO ↔ O2 are inverse on the rich/lean axis.** CO up means O2 down (rich consumed the air). O2 up with CO ≈ 0 means lean. Both up at once ⇒ rich misfire (fuel dumped, never burned).
2. **HC + O2 both up, CO low ⇒ lean misfire** (ignition or dilution). The fuel never lit; the air slid past unreacted.
3. **HC + O2 + CO all up ⇒ rich misfire.** Excess fuel was dumped, partial burn happened, raw fuel and excess air both escape.
4. **CO2 always falls when anything is wrong.** Use CO2 as the efficiency axis: it is high only when combustion was both balanced *and* complete.
5. **HC ↔ NOx anti-correlate near stoich.** Burning the HC lifts peak temperature, which lifts NOx; quenching the burn (rich) suppresses NOx.
6. **NOx high + lean λ + low CO ⇒ lean combustion under load** (or stuck-open EGR, or cooling problem).
7. **Lambda from chemistry beats lambda from ECU.** When the analyser and the ECU disagree, the analyser is ground truth (subject to the air-leak caveat). This is the truth-vs-perception override the engine uses to rank `ECU_Logic_Inversion_*` faults.
8. **Cranking-shaped gases** (HC=0, CO=0, CO2 ≈ 0.04 %, O2 ≈ 20.9 %, λ → ∞) mean no combustion is occurring — route to the non-starter pipeline regardless of DTCs.
9. **NOx = 0 with a 4-gas analyser is missing-data, not evidence of rich.** Suppress the `nox_low` symptom unless the user has confirmed a 5-gas probe.
10. **Cold-start enrichment (ECT < ~30 °C) legitimately raises HC + CO and drops λ slightly**; the cold-start gate must demote mechanical-rich faults until temperature normalises.

---

## 4. Pattern-to-fault quick map (drives the CSV expected_top_fault column)

| Pattern (idle, warm) | λ | Diagnosis class | Notes |
|---|---|---|---|
| CO low, CO2 high, HC low, O2 low | ≈1.00 | clean burn | catalyst working |
| CO high, CO2 low, HC moderate, O2 low | <0.95 | rich mixture | leaking injector / high fuel pressure / MAF over-read |
| CO low, CO2 low, HC high, O2 high | >1.05 | lean misfire | vacuum leak / lean DTC / dirty MAF |
| CO low, CO2 normal, HC very high, O2 normal | ≈1.00 | mechanical / oil consumption | rings, valve seals — λ stays balanced |
| CO low, CO2 normal, HC high, O2 high, NOx low | >1.03 | ignition misfire (random) | P0300 family |
| CO normal, CO2 low, HC low, O2 high | >1.05 | exhaust air leak | falsely lean λ; analyser shows leak signature |
| CO 0, CO2 ≈ 0, HC 0, O2 ≈ 20.9 | ∞ | no combustion / non-starter | route to NS pipeline |
| CO mod, CO2 low, HC high, O2 high | <1.00 | rich misfire | very rich + ignition fault, or valve-timing way off |
| CO low, CO2 high, HC low, O2 low, NOx very high | ≈1.00 under load | high combustion temp | cooling fault, EGR stuck closed, over-advanced timing |
| CO low, CO2 high, HC low, O2 low, NOx very high | >1.05 idle | lean idle + hot burn | EGR stuck open or vacuum leak with hot chamber |

---

## 5. Catalyst-aware caveats

A healthy three-way cat scrubs HC and CO post-cat, raises CO2 slightly, and pulls O2 toward zero by oxidation. This means a rich-running engine with a good cat can present a *clean* tailpipe HC/CO while still showing rich λ and rich OBD trims — the reasoning column should call this out as "cat masking" whenever both `dtcs=P0420` and the gases look unexpectedly clean. Conversely, a P0420 with healthy gases at idle does not prove the cat is bad: P0420 is set on a drive-cycle test and the catalyst can fail only at higher load (Case 24 in the corpus).

---

## 6. Cross-channel sanity rails

- HC, CO, CO2, O2 should be *physically* consistent: in a healthy idle, CO + CO2 + O2 ≈ 14.5–16 %. A row outside that band is either a sensor problem, an air leak, or analyser drift.
- λ from the analyser within ±0.08 of the ECU's reported λ is normal; a wider gap raises a perception-contradiction symptom.
- Idle NOx > ~1000 ppm is suspicious — confirm load, EGR, and cooling.
- Trims (STFT/LTFT) outside ±25 % at idle indicate either a real large mixture issue or a sensor rail-out (P0131/P0132 etc.).

---

## 7. How the reasoning column is written

For every row in the test CSV, the `reasoning` cell follows this grammar:

> `HC=<value> (<short physical explanation>); CO=<value> (<short>); CO2=<value> (<short>); O2=<value> (<short>); NOx=<value> (<short>); λ=<value> (<short, including any contradiction with the OBD/ECU lambda>).`

Each parenthetical is one short clause derived from §2 (per-gas behaviour) and §3 (inter-gas rules). When the case is intentionally *contradictory* (e.g., rich gas with lean DTC), the λ clause names the contradiction explicitly. When a value is "normal", the clause says so and points to the rule that makes it normal. This is what makes the corpus self-documenting: every number in every row is justified by a rule in this guide.

---

## 8. Cross-reference tables from the PDF library (added after OCR pass 2026-05-03)

The five PDFs in this folder were OCR'd and verified. Their tables resolve into four canonical "fingerprint" rows that the engine should treat as primary classification anchors. Each row is **directional** — high vs low — not numeric, because the PDF charts are colour-coded High/Low/Moderate labels. Use the per-gas thresholds in §2 to map the row to a numeric measurement.

### 8.1 The four canonical rows (from `lambda.pdf` page 1)

| Lambda direction | CO | CO2 | HC | O2 | Class |
|---|---|---|---|---|---|
| λ < 1.0 | High | Low | High | Low | **Rich Mixture** |
| λ > 1.0 | Low | Low | **Low** | High | **Exhaust / sample air leak** (HC stays low because the leak is downstream of combustion) |
| λ > 1.0 | Low | Low | **High** | High | **Lean Mixture** (HC rises from lean misfire) |
| λ ≈ 1.0 | Low | High | Low | Low | **Tuned** (catalyst working) |

The split between *exhaust leak* and *true lean* on the HC axis is critical: an air leak reads falsely lean on lambda but does *not* lift HC, while a real lean burn lifts HC through misfire. The 4D engine should use this distinction to demote `lean_condition` candidates when O2 is high but HC is normal, and instead surface `exhaust_air_leak` or sample-leak candidates.

### 8.2 Engine-faults cross-reference (from `enginefaults.pdf`)

| CO | CO2 | HC | O2 | Most likely problem |
|---|---|---|---|---|
| Low–Moderate | Low | Low–Moderate | Low | **Major engine fault** — low compression, insufficient camshaft lobe lift |
| Low–Moderate | Low | Low–Moderate | Low | **Minor engine fault** — ignition timing over-advanced, spark plug/wire grounded or open, ECM compensating for a vacuum leak |
| Low | High | Low | High | Injector misfire, catalytic converter operating correctly |
| High | Low | High | Low | Thermostat or coolant temperature sensor faulty — "cold-running engine" |
| Low | High | Low | Low | Thermostat or coolant temperature sensor faulty — "hot-running engine" |
| Low | Low | Low | High | Exhaust leak **after** the catalytic converter |
| High | High | High | High | Combination of rich mixture + vacuum leak + injector misfire + dead cat |
| Low | High | Low | Low | Good combustion efficiency and catalytic converter working properly |

**Key implication.** Rows 1 and 2 share an identical gas signature; rows 5 and 8 also share one. Gases alone cannot split them — the engine must use trim direction (hot/cold ECT, STFT/LTFT bias) and DTC priors. This is why the schema's discriminator nodes exist.

### 8.3 Lean-mixture causes (from `leanmixture.pdf`)

When the canonical lean row fires (Low CO + Low CO2 + High HC + High O2), the cause is one of:

lean fuel mixture; ignition misfire; vacuum leaks / air leaks (between MAF and throttle body); bad EGR valve or vacuum hoses misrouted; carburettor settings incorrect; fuel injector(s) bad; O2 sensor bad or failing; ECM malfunctioning; float level too low.

These map directly onto the existing 4D children of `lean_condition` (`vacuum_leak`, `contaminated_maf`, `egr_fault`, `pcv_fault`, `evap_leak`, `sensor_fault`).

### 8.4 Rich-mixture causes and the WRONG VALVE TIMING signature (from `richmixture.pdf`)

Rich (High CO + Low CO2 + Low–Moderate HC + Low O2): rich fuel mixture; leaking injectors; incorrect carburettor adjustment; power valve leaking; choke operating rich; float level too high; dirty air filter; EVAP canister purge faulty; PCV system problem; ECM malfunctioning; crankcase contaminated with raw fuel.

With a working three-way cat the same rich condition reads as Moderate-to-High CO + Low CO2 + Low–Moderate HC + Low O2, because the cat oxidises some of the CO into CO2.

**Rich + ignition misfire** is the High CO + Low CO2 + High HC + High O2 row — the diagnostic giveaway is that *both* CO and O2 are high, which is impossible in pure rich (rich consumes O2) or pure lean (lean has no CO). It tells the engine that fuel is being dumped *and* not lit.

**Wrong valve timing.** High CO + Low CO2 + **HC > 1000 ppm** + **O2 > 5 %** is the classic "what enters gets out only partially burned" mechanical fingerprint. The rich and lean canonical rules cannot explain this combination. The 4D engine should map it to a cam-timing / valve-mechanical fault, not a fuel-mixture fault.

### 8.5 Quantitative rules from `lambda.pdf`

- **Brettschneider equation.** Lambda is calculated from O2, CO, CO2, HC, NOx and (estimated) water vapour. It compares all oxygen in the exhaust to all carbon and hydrogen.
- **A 4-gas analyser is adequate** for lambda. NOx adds only 0.05 % O2 equivalence per 1 000 ppm. At idle NOx ≈ 0 ppm so 4-gas omission has no effect. Above idle and under load, the analyser substitutes an estimation equation. The engine must therefore treat NOx = 0 as *unmeasured*, not as low-NOx evidence.
- **5 % air leak → 5 % lean shift on lambda.** A real lambda of 1.000 reads 1.050 if 5 % of the sample is ambient air. Air leaks (sample probe, exhaust manifold, secondary-air injection still active) **always** bias lambda toward lean and must be ruled out before any lambda diagnosis. This is why `Exhaust_Air_Leak_Pre_Cat` exists as a node and why the engine's lambda-mismatch warning has to consider leak signatures before flagging an ECU contradiction.
- **Lambda is misfire-immune.** Engine misfire has *no effect* on the lambda calculation because the balance of oxygen to combustibles is preserved whether or not the burn happens.
- **Pre-cat and post-cat lambda are identical** for a healthy system. The cat converts CO + HC into CO2 + H2O but does not change the oxygen balance. This means the engine cannot use lambda alone to detect a cat failure — it must use the HC/CO axis (which the cat *does* change).
- **Catalyst window 0.97–1.03.** Inside this lambda band the three-way cat works. Outside it (especially > 1.03) the cat cannot reduce NOx because there is not enough CO to drive the reduction reaction.

### 8.6 Reference emission values (from `lambda.pdf`)

| Condition | CO | CO2 | HC | O2 | Lambda | AFR |
|---|---|---|---|---|---|---|
| With catalyst (good system) | ≤ 0.5 % | ≥ 14.5 % | ≤ 50 ppm | ≤ 0.5 % | 0.97–1.03 | 14.3:1–15.1:1 |
| Without catalyst | ≤ 1.5 % | ≥ 13 % | ≤ 250 ppm | 0.5–2 % | 0.90–1.10 | 13.2:1–16.2:1 |
| Before cat (efficient) | 0.6 % | 14.7 % | 100 ppm | 0.7 % | 1.0 | 14.7 |
| After cat (efficient) | 0.1 % | 15.2 % | 15 ppm | 0.1 % | 1.0 | 14.7 |

These bounds ground the "normal" calls in the reasoning column: HC ≤ 50 ppm at the tailpipe with a working cat is normal, HC ≤ 250 ppm without one is normal, and the cat should reduce HC by roughly an order of magnitude.

### 8.7 AFR-vs-engine-condition consequence chart (from `AFR.pdf`)

| Too Lean | Slightly Lean | Slightly Rich | Too Rich |
|---|---|---|---|
| Poor engine power | High fuel mileage | Maximum engine power | Poor fuel mileage |
| Misfire at cruise speeds | Low exhaust emissions | Higher emissions | Misfiring |
| Burned valves | Reduced engine power | Higher fuel consumption | Increased air pollution |
| Burned pistons | Some tendency to knock or ping | Lower tendency to knock or ping | Oil contamination |
| Scored cylinders |  |  | Black exhaust |
| Spark knock or ping |  |  |  |

This chart is the consequence model the 4D engine should reference when explaining *why* a sustained AFR error matters, not just *that* it is present.

---

*Sources consolidated:* `HC.md`, `CO.md`, `CO2.md`, `O2.md`, `NOx.md`, `gasrules1.md`, `Understanding Engine Exhaust Emissions.md`, `Understanding Catalitic Converters.md`, plus the OCR'd `AFR.md`, `enginefaults.md`, `lambda.md`, `leanmixture.md`, `richmixture.md` (extracted from the PDFs in this folder on 2026-05-03).
