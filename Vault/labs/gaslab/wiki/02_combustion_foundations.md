---
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "lambda-model"
implements:
  - "labs/gaslab/code/brettschneider.py"
  - "labs/gaslab/code/contracts.py"
consumers:
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py lambda_chem"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py lambda_chem aggregation"
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py lambda_measured comparison"
drift_guards:
  - "labs/gaslab/tests/unit/test_brettschneider.py"
  - "labs/gaslab/tests/unit/test_contracts.py"
tags: [gaslab, finished, wiki]
source: "labs/gaslab/wiki/02_combustion_foundations.md"
---

# 2. Combustion Foundations

> **Chunk summary.** Stoichiometry, lambda, the Brettschneider equation and its reliability/uncertainty model, the catalyst window, the two-truths frame, combustion-integrity metrics, RPM buckets, Euro-category threshold scaling, and the effect of E5/E10 + altitude on idle readings.

## 2.1 The ideal reaction {#CONCEPT_IDEAL_REACTION}

Spark-ignition petrol combustion approximates octane burning in air:

```
2 C₈H₁₈ + 25 O₂  →  16 CO₂ + 18 H₂O   (+ atmospheric N₂ carried through)
```

In a perfect cycle every carbon finds two oxygens (→ CO₂) and every hydrogen pair finds one oxygen (→ H₂O). Four diagnostic by-products leak past the ideal:

| By-product | Why it exists |
|---|---|
| **HC** (unburned fuel) | Quench layers, ring-land / valve-pocket crevices, missed ignition, oil consumption |
| **CO** (partially burned fuel) | Flame ran out of O₂ before completing CO → CO₂ |
| **O₂** (un-reacted air) | Mixture lean, a cylinder missed, or air leaked in |
| **NOₓ** (thermal NO) | Combustion temperature exceeded ~2500 °F (~1370 °C), forcing N₂ + O₂ → NO |

CO₂ is the only "good" product worth measuring — it is the score card.

## 2.2 Stoichiometry and lambda {#CONCEPT_LAMBDA}

Stoichiometric AFR for pump petrol ≈ **14.71 : 1** by mass. Lambda is a fuel-independent normalisation: `λ = AFR_actual / AFR_stoichiometric`.

- `λ = 1.000` → perfect chemical balance.
- `λ < 1.000` → rich (excess fuel); `λ > 1.000` → lean (excess air).
- `λ = 1.050` → 5 % lean (a 5 % air leak shifts a true 1.000 to 1.050).

GASLab uses λ as the universal mixture axis. AFR is reported for context (`AFR = λ × 14.71`) but never as the primary metric.

## 2.3 The Brettschneider lambda equation {#CONCEPT_BRETTSCHNEIDER}

GASLab calculates λ purely from chemistry — no O₂ sensor required:

```
       [CO₂] + [CO]/2 + [O₂] + (Hcv/4 · [CO₂]/([CO₂]+[CO])) · [CO₂]
λ  =  ─────────────────────────────────────────────────────────────
                       [CO₂] + [CO] + [HC]
```

`Hcv` is the hydrogen-to-carbon ratio of the fuel (≈ 1.85 for pump petrol; 4 for methane). NOₓ contributes a small O₂-equivalence term (~0.05 % per 1 000 ppm NOₓ) supplied directly by the 5-gas analyser. Implementation note: `brettschneider.py` uses `hc_equiv = hc * 0.0025`, a standard and valid NDIR-scaling approach `[v2: q1]`.

**Three diagnostic consequences:**

- **λ is misfire-immune.** Raw fuel and raw air escaping a misfiring cylinder remain in chemical balance, so λ ≈ 1.000 even with HC spiking and CO₂ collapsing. Misfire detection therefore uses HC + CO₂ + NOₓ, not λ.
- **λ is air-leak sensitive.** A 5 % ambient dilution shifts a true 1.000 to 1.050. Air leaks MUST be ruled out before any "lean" verdict — the triangle gate (→ GATE_TRIANGLE) is the first defence.
- **Pre-cat and post-cat λ are identical** for a healthy system. The catalyst converts CO + HC into CO₂ + H₂O without changing the oxygen balance; λ alone cannot detect cat failure — the HC / CO axis is required.

## 2.4 Brettschneider reliability — λ is a property of the sample, not the engine {#CONCEPT_BRETTSCHNEIDER_RELIABILITY}

`[v2: q1, q2]` Brettschneider is mathematically robust but frequently misread as a direct measure of in-cylinder combustion "ground truth." It is an **exhaust-gas mass-balance equation**: given valid concentrations it yields a mathematically accurate λ *for that gas sample*. Whether that equals the engine's true stoichiometry depends entirely on **sample-stream integrity**. Garbage in, garbage out.

**Per-fault reliability:**

| Fault type | Effect on λ | Reliability as ground truth |
|---|---|---|
| **Misfire** (raised O₂ + HC) | Stable, near target | **High.** The equation accounts for unburned HC and excess O₂ and balances them back toward stoichiometry. λ stays ≈ 1.0 while raw HC spikes — read HC/O₂ separately, not λ, to see the misfire. λ only drifts if the ECU is actively trimming fuel off a wideband sensor. |
| **Pre-cat / sampling air leak** | False lean | **Low — primary failure mode.** Tramp air (venturi effect at exhaust pulses) adds O₂; the equation cannot tell it from combustion O₂ and reports lean even on a perfectly stoichiometric engine. More detectable at idle (low flow, high vacuum at the leak) and often masked at high idle (positive pressure pushes gas out). |
| **Catalyst masking** | Variable | **Conditional.** Valid downstream of the cat, but post-cat λ reflects the converter's oxygen-storage/release state, not engine intent — diverges from pre-cat especially during transients and when the cat is failing. |

**Uncertainty band.** There is no single universal ± figure, because the uncertainty lives in the **inputs** and the **environment**, not the formula:

- **Instrument:** a well-calibrated 5-gas analyser holds λ to roughly **±0.05–0.10 absolute**; a drifted O₂ cell breaks the calculation. Headline equation accuracy is often quoted as **~±1 %** when inputs are clean.
- **Sample integrity (the ground-truth killer):** in a verified-sealed system Brettschneider is the gold standard. In a repair-bay with an unverified exhaust system, a leak can swing λ by **0.05–0.15 (5–15 % false-lean)**.
- **HC carbon-mass modelling:** the standard NDIR factor under-measures true carbon mass in gasoline exhaust by up to ~50 %, motivating the "Modified Brettschneider" (HC factor 12 instead of 6) for higher accuracy. GASLab's current scaling is documented and acceptable; the modified form is noted for future calibration only.

**Strategy rule:** treat λ as a measure of the *sample*. If λ ≈ 1.0 but HC is high → misfire. If λ shifts leaner at idle than at high idle → suspect a leak upstream of the probe. Never calibrate engine fuelling from tailpipe λ without first verifying ~0 % exhaust leakage. The leak-vs-sampling-error resolution lives at → TEST_PROBE_OCCLUSION and → CONCEPT_DIVERGENCE_MAGNITUDE (GASWIKI-04).

## 2.5 The catalyst window {#CONCEPT_CATALYST_WINDOW}

| Band | λ range | Behaviour |
|---|---|---|
| Peak efficiency | 0.995 – 1.005 | All three TWC reactions > 99 % conversion |
| Light-off window | 0.98 – 1.02 | Cat reaches operating temperature and stays active |
| NOₓ breakthrough | λ > 1.03 | Rh sites saturated by O₂; reduction stops |
| CO / HC breakthrough | λ < 0.97 | Stored O₂ depleted; oxidation stops |

A working catalyst raises Combustion Efficiency from ~95 % engine-out to > 99 % tailpipe; the same scrubbing can also mask a feed-gas fault upstream of the cat (→ CONCEPT_HEALTHY_CAT_MASKING, GASWIKI-07 §7.8). Outside the light-off band the catalyst is, in effect, a hollow can. Catalyst diagnosis detail → CONCEPT_TWC and → TEST_DUAL_IDLE_CATALYST (GASWIKI-07).

## 2.6 The two simultaneous truths {#CONCEPT_TWO_TRUTHS}

Every gas diagnosis has two axes: **Balance** (λ axis — was the O₂-to-combustibles ratio correct?) and **Quality** (HC + CO₂ axis — did the molecules react?). A misfire is correct on balance (λ ≈ 1.0) but catastrophic on quality (HC spikes, CO₂ collapses). A vacuum leak is wrong on balance and may or may not affect quality. A one-axis verdict is half-blind. The fault atlas (GASWIKI-05/06A/06B) names which combination each `chemical_state` represents.

## 2.7 RPM measurement points {#CONCEPT_RPM_BUCKET}

| Bucket | RPM band | Where it comes from |
|---|---|---|
| `STABILIZED_IDLE` | 650 – 900 | warm idle, closed-loop, 60 s settle |
| `REGULATORY_HIGH_IDLE` | 2200 – 2800 (commonly 2500) | SAE J1667 / BAR Two-Speed Idle |
| `STRESS_IDLE` | 3500 – 4500, VIN-dependent | clinical diagnostic point |

The bucket affects HC and NOₓ thresholds (turbulence improves the burn; cat heats up at higher RPM). Cold open-loop samples are **rejected** by the operating envelope — no cold-start enrichment fault class exists in v1/v2. The idle→2500 RPM transition is also the engine of the RPM-differential discriminators (oil-burn sub-modes, GDI carbon, timing) — see → TEST_RPM_SEPARATION_MATRIX (GASWIKI-08).

## 2.8 Euro-scaled thresholds {#CONCEPT_EURO_SCALING}

Numeric thresholds in the atlas are stated for a baseline Euro 4 vehicle with a working three-way cat. When DNA supplies `euro_emission_category` and per-vehicle CoC bounds, GASLab tightens or loosens:

| Euro | CO ceiling (idle, with cat) | HC ceiling (2500 RPM) | Source |
|---|---|---|---|
| EURO 1 | 4.5 % | — | type-approval limits |
| EURO 2 | 0.5 % | 1200 ppm | type-approval limits |
| EURO 3 | 0.3 % | 200 ppm | UK MOT |
| EURO 4 | 0.2 % | 200 ppm | UK MOT |
| EURO 5 | 0.2 % | 200 ppm | type-approval (2009–2010, upper edge of scope) |

When `confidence = HIGH` the per-vehicle CoC bounds override these defaults; see GASWIKI-10. (Euro 6/7 are out of the 1990–2010 scope and intentionally omitted.)

## 2.9 Fuel formulation and altitude {#CONCEPT_FUEL_ALTITUDE}

`[v2: q9]` Fuel blend and altitude shift idle readings enough to cause lean/rich misclassification if ignored.

- **Ethanol (E5/E10).** Blending ethanol consistently **lowers idle HC and CO** versus straight gasoline (oxygenated fuel burns cleaner). A car on E10 can read naturally lower HC/CO than the same car on pure petrol.
- **Effect on the triangle.** Lower HC/CO drag the dilution-screen sum and can nudge the Exhaust-Gas-Triangle sum (CO+CO₂+O₂) toward the lower edge — a near-14 % sample can tip into `INVALID`.
- **Altitude.** The Brettschneider equation is a mass balance and **needs no altitude input** — λ math is altitude-invariant. What altitude affects is the *ECU's* ability to hold the target AFR, which can indirectly shift exhaust composition; that is a perception issue, not a chemistry-math issue.

**Design rules:**

1. **Do NOT relax the triangle gate** (`SUM_VALID_MIN = 14.0`) for high-ethanol or high-altitude samples. It is a critical sample-integrity gate; re-validate with other data (e.g. OBD trims, probe-occlusion test) instead of widening it.
2. The `NORMAL_OPERATION` bounds *may* be widened slightly to absorb ethanol shifts, accepting some loss of sensitivity to subtle mixture faults — a deliberate, documented trade-off, not a gate change.
3. `fuel_type` and `altitude_band` are carried as **context only** (→ CONCEPT_GASLABDNAVIEW). They annotate the diagnosis; they do not move the validity boundary.

## 2.10 Combustion-integrity metrics {#CONCEPT_COMBUSTION_INTEGRITY}

`[v2.3: EP-GAS-03 / F-GAS-04, F-GAS-05]` The two-truths frame (→ CONCEPT_TWO_TRUTHS) needs one numeric handle for **Quality** and one explicit O₂-vs-CO discriminator for the rich/misfire split. Both are derived from the same five gases already in the sample; neither adds a new analyser channel or payload field.

**Chemical efficiency** is the carbon-oxidation score:

```text
chemical_efficiency = CO₂/(CO₂+CO)     # CO₂ and CO in vol %

healthy               >= ~0.95
combustion deficit     < ~0.95
```

Low chemical efficiency means carbon is not being fully oxidised into CO₂. That is a fundamental combustion-quality failure — pumping loss, misfire, bad timing, or another incomplete-burn mechanism — and it is independent of whether the fuel/air balance (`λ`) is rich, lean, or near stoichiometric.

Worked anchors from the warm-idle reference (GASWIKI-11 §11.2.1):

| Condition | CO₂ | CO | chemical_efficiency | Reading |
|---|---:|---:|---:|---|
| Healthy idle | ≈ 14.7 % | ≈ 0.6 % | ≈ 0.96 | carbon mostly oxidised |
| Severe rich / incomplete burn | ≈ 10.0 % | ≈ 5.0 % | ≈ 0.67 | major combustion deficit |

**Oxygen usage** is the qualitative O₂-vs-CO discriminator behind the CO↔O₂ seesaw (→ RULE_SEESAW) and the HC/O₂/CO truth table (→ RULE_HC_O2_CO_TRUTH_TABLE):

```text
high O₂ + high HC/CO   -> MISFIRE   # both reactants escaped unburned
high CO + O₂ ≈ 0       -> pure RICH over-fuelling
```

Do not turn this into a new numeric ratio threshold. The bands come from the existing CO and O₂ threshold tables; the diagnostic point is the chemistry: if both free oxygen and combustibles arrive together, combustion did not happen, so the "rich and lean at once" pattern resolves through the misfire/masking path (→ RULE_MASKING), not through a simple fuelling verdict.

## Graph relations (explicit)

**CONCEPT_LAMBDA** EVALUATES_STATE_OF **fuel-air mixture** (λ = AFR_actual / AFR_stoichiometric, ≈ 14.71:1)
**CONCEPT_BRETTSCHNEIDER** CONSUMED_BY **gaslab.brettschneider**
**CONCEPT_BRETTSCHNEIDER_RELIABILITY** DESCRIBES **λ as property of the sample, not the engine**
**CONCEPT_BRETTSCHNEIDER_RELIABILITY** WARNS **pre-cat air leak produces false lean**
**CONCEPT_BRETTSCHNEIDER_RELIABILITY** WARNS **catalyst masking diverges post-cat λ from engine truth**
**CONCEPT_CATALYST_WINDOW** GATED_BY **λ 0.995–1.005** (peak efficiency), **λ 0.98–1.02** (light-off)
**CONCEPT_CATALYST_WINDOW** DESCRIBES **NOₓ breakthrough at λ > 1.03**, **CO/HC breakthrough at λ < 0.97**
**CONCEPT_TWO_TRUTHS** DISAMBIGUATED_BY **Balance axis (λ)** and **Quality axis (HC + CO₂)**
**CONCEPT_RPM_BUCKET** GATED_BY **STABILIZED_IDLE** (650–900), **REGULATORY_HIGH_IDLE** (2200–2800), **STRESS_IDLE** (3500–4500)
**CONCEPT_RPM_BUCKET** CONSUMED_BY **engine_state_bucket** input field
**CONCEPT_EURO_SCALING** CONSUMED_BY **euro_emission_category** from **GasLabDnaView**
**CONCEPT_EURO_SCALING** SCALES **CO ceiling** and **HC ceiling** per Euro 1–5
**CONCEPT_FUEL_ALTITUDE** DESCRIBES **E5/E10 ethanol blend effects** on idle HC/CO
**CONCEPT_FUEL_ALTITUDE** STATES **do NOT relax GATE_TRIANGLE** for ethanol or altitude
**fuel_type** (proposed) CARRIED_AS **context only** — does not move validity boundary
**altitude_band** (proposed) CARRIED_AS **context only** — λ math is altitude-invariant
**CONCEPT_COMBUSTION_INTEGRITY** DEFINES **chemical_efficiency = CO₂/(CO₂+CO)**
**CONCEPT_COMBUSTION_INTEGRITY** DISAMBIGUATED_BY **high O₂ + high HC/CO → MISFIRE**, **high CO + O₂ ≈ 0 → pure RICH**
**CONCEPT_COMBUSTION_INTEGRITY** ROUTES_TO **RULE_MASKING** for rich+lean collision resolution
**CONCEPT_COMBUSTION_INTEGRITY** ROUTES_TO **RULE_SEESAW** for CO↔O₂ balance

## Core Entities

- **CONCEPT_IDEAL_REACTION** — 2 C₈H₁₈ + 25 O₂ → 16 CO₂ + 18 H₂O; four diagnostic by-products (HC, CO, O₂, NOₓ). Consumer: all gas interpretation rules.
- **CONCEPT_LAMBDA** — universal mixture axis (λ = AFR_actual / AFR_stoichiometric, petrol baseline 14.71:1). Consumer: `brettschneider.py`, all `λ` thresholds in rule engine.
- **CONCEPT_BRETTSCHNEIDER** — exhaust-gas mass-balance λ equation (5-gas input). Consumer: `gaslab.brettschneider`.
- **CONCEPT_BRETTSCHNEIDER_RELIABILITY** — λ accuracy depends on sample-stream integrity; per-fault reliability table; uncertainty band ~±0.05–0.10 with clean inputs. Consumer: `RULE_LAMBDA_MISMATCH` truth-vs-perception detector.
- **CONCEPT_CATALYST_WINDOW** — λ bands for TWC peak efficiency, light-off, and breakthrough. Consumer: `CONCEPT_TWC` (GASWIKI-07), `TEST_DUAL_IDLE_CATALYST`.
- **CONCEPT_TWO_TRUTHS** — every diagnosis has Balance (λ) and Quality (HC+CO₂) axes. Consumer: fault atlas (GASWIKI-05/06A/06B).
- **CONCEPT_RPM_BUCKET** — three measurement points governing HC/NOₓ thresholds. Consumer: `engine_state_bucket` input, `TEST_RPM_SEPARATION_MATRIX` (GASWIKI-08).
- **CONCEPT_EURO_SCALING** — per-Euro CO/HC ceilings scaled by `euro_emission_category` DNA field. Consumer: `gaslab/rule_engine.py` threshold lookup.
- **CONCEPT_FUEL_ALTITUDE** — E5/E10 and altitude effects; design rules (never relax triangle gate). Consumer: `fuel_type`/`altitude_band` DNA fields (context only).
- **CONCEPT_COMBUSTION_INTEGRITY** — `chemical_efficiency` (CO₂/(CO₂+CO)) and oxygen_usage discriminator; GW-ENH-1. Consumer: `RULE_SEESAW`, `RULE_MASKING`, fault atlas.
