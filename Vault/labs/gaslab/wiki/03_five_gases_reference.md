---
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "gas-payload"
implements:
  - "labs/gaslab/code/contracts.py"
  - "labs/gaslab/code/data/gas_lab_ontology.yaml"
consumers:
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py gas_co/gas_hc/gas_o2"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py GasLabPayload forwarding"
drift_guards:
  - "labs/gaslab/tests/unit/test_contracts.py"
  - "labs/gaslab/tests/unit/test_ontology.py"
tags: [gaslab, finished, wiki]
source: "labs/gaslab/wiki/03_five_gases_reference.md"
---

# 3. The Five Gases

> **Chunk summary.** For each gas: chemistry, sensor, normal ranges, behaviour bands, and cross-sensitivity. Numeric thresholds are normative — every rule in `gas_lab_rules.yaml` cites this chunk.

## 3.1 HC — Hydrocarbons (ppm) {#GAS_HC}

Unburned fuel. Rule of thumb: 1 % wasted fuel ≈ 200 ppm HC. Spikes when combustion is interrupted (misfire, lean misfire, leakage past valves/rings, EGR over-dilution) or when raw fuel is delivered without burning.

**Sensor:** NDIR tuned to the C–H absorption band ~3.4 µm. Heavy oil hydrocarbons read with reduced response — oil consumption can look smaller than it is.

**Normal ranges (idle, warm):**

| Condition | HC ceiling |
|---|---|
| Tailpipe, working three-way cat | ≤ 35 ppm (≤ 50 ppm tolerable) |
| Tailpipe, no catalyst | ≤ 250 ppm |
| Pre-cat (engine-out), healthy engine | ≤ 100 ppm |

**Behaviour bands:** ≤ 50 ppm clean/active-cat; 50–250 ppm minor inefficiency or pre-cat normal; 250–800 ppm real combustion problem; 800–2000 ppm severe misfire / oil burning / cat failure; > 2000 ppm almost always mechanical or hard ignition fault.

**U-shape vs λ:** HC spikes at both extremes — rich-side fuel saturation; lean-side too thin to ignite; mechanical from oil/ring fault.

## 3.2 CO — Carbon monoxide (vol %) {#GAS_CO}

Partial-oxidation product. CO exists only if combustion happened but ran out of oxygen. **One-way rich indicator:** CO ≈ 0 does not prove lean, but CO > ~1.5 % effectively guarantees rich.

**Sensor:** NDIR ~4.7 µm with chemical filters to suppress H₂ interference. Electrochemical CO cells over-read on H₂ from rich combustion; NDIR is mandatory for diagnostic-grade work.

**Normal ranges (idle, warm):**

| Condition | CO range |
|---|---|
| Tailpipe, working cat | 0.1 – 0.45 % |
| Tailpipe, cat not lighting off | 0.5 – 0.9 % |
| Pre-cat | up to 1.5 % can be normal |

**Behaviour bands:** ≤ 0.5 % stoich/clean-up; 0.5–1.5 % mild rich or normal pre-cat; 1.5–3 % clear rich; > 3 % very rich (expect concurrent HC rise).

**Post-cat rule.** With a working cat at idle, CO < 0.3 %. Closed-loop control reported yet tailpipe CO > 0.8 % ⇒ catalyst failing or poisoned.

## 3.3 CO₂ — Carbon dioxide (vol %) {#GAS_CO2}

End product of *complete* combustion — the "north star" of efficiency. Anything that disturbs combustion drops CO₂ below its ~15.5 % ceiling. CO₂ forms a bell curve against λ, peaking at λ ≈ 1.000.

**Sensor:** NDIR ~4.3 µm. Highly stable, primary efficiency reference.

**Normal ranges (idle, warm):**

| Condition | CO₂ target |
|---|---|
| Working cat | 14.5 – 16.0 % |
| Cat not lighting off | 13.5 – 14.5 % |
| Without catalyst | ≥ 13 % |
| Mild combustion deficit | 11 – 13 % |
| Severe combustion failure | < 11 % |

CO₂ typically rises 1–2 % from idle to 2500 RPM as turbulence improves the burn — a CO₂ that *falls* with revs is a red flag. If CO₂ < 13 % the reasoning must explain *why* — CO₂ collapse never happens on its own.

## 3.4 O₂ — Oxygen (vol %) {#GAS_O2}

Free oxygen remaining after combustion. Ambient air is 20.9 %; a healthy idle tailpipe is ≤ 1.5 % (≤ 0.35 % post-cat). O₂ climbs sharply once λ > 1.

**Sensor:** Electrochemical (Pb-O₂ wet cell) or paramagnetic. The most truthful **post-catalyst** mixture indicator — the cat does not consume O₂ the way it consumes CO and HC.

**Normal ranges (idle, warm):**

| Condition | O₂ range |
|---|---|
| Working cat, stoich | ≤ 0.35 % |
| Working cat, edge of light-off | 0.3 – 0.7 % |
| No catalyst | 0.5 – 1.5 % |

**Behaviour bands:** < 0.5 % rich or perfect stoich; 0.5–1.5 % typical pre-cat or mild lean; 1.5–4 % clearly lean or misfire; > 4 % severe lean, big misfire, or air leak; ≈ 20.9 % with HC=0, CO=0, CO₂≈0.04 % ⇒ no combustion (cranking / probe out).

**Per-cylinder misfire math.** A misfiring cylinder dumps its air charge unreacted:

```
ΔO₂ per misfiring cylinder ≈ 21 % / cylinder_count
```

One dead cylinder on a 4-cyl ≈ 5.25 % O₂ rise; 6-cyl ≈ 3.5 %; 8-cyl ≈ 2.6 %. `cylinder_count` comes from `GasLabDnaView`.

**Air-leak warning.** Manifold cracks and probe-fitting leaks inject ambient O₂ and falsely raise the lean reading without affecting CO or HC. "Lean λ + high O₂ + normal HC + normal CO" is a leak, not a real lean condition (→ FAULT_EXHAUST_AIR_LEAK, → TEST_PROBE_OCCLUSION).

## 3.5 NOₓ — Oxides of nitrogen (ppm) {#GAS_NOX}

Thermal NO formation requires peak temperatures > ~2500 °F (~1370 °C). At idle without load, NOₓ ≈ 0. Peaks **under load** near stoichiometric; suppressed by rich mixtures (cooling) and EGR (inert dilution).

**Sensor:** Electrochemical. Cross-sensitive to H₂S — readings can swing negative on NO₂ channels and slightly positive on NO channels when sulfur is present.

**Normal ranges:**

| Condition | NOₓ |
|---|---|
| Idle, warm, healthy | < 100 ppm |
| Idle, elevated | 100 – 500 ppm |
| High-idle (2500 RPM), healthy | 100 – 1000 ppm |
| Under load, healthy | 500 – 1500 ppm |
| Under load, EGR / cooling / timing fault | > 1500 ppm |

**Two interpretive rules:**

- **NOₓ and CO are anti-correlated** through chamber temperature: rich raises CO and cools the cylinder, killing NOₓ; lean cuts CO and heats it, raising NOₓ.
- **The masking rule** (low NOₓ + high HC + high O₂ + low CO₂) — classic ignition misfire. No combustion → no heat → no NOₓ, despite the air looking "lean" (→ RULE_MASKING).

## 3.6 The 5-gas cheat sheet {#CONCEPT_5GAS_CHEATSHEET}

| Parameter | Symbol | Ideal idle | Rich | Lean | Misfire |
|---|---|---|---|---|---|
| Hydrocarbons | HC | 0 – 35 ppm | Moderate | Low | Very high (> 1000 ppm) |
| Carbon monoxide | CO | 0.1 – 0.45 % | High (> 1.0 %) | Very low (< 0.1 %) | Low – moderate |
| Carbon dioxide | CO₂ | 14.5 – 16.0 % | Low (< 12 %) | Low (< 12 %) | Very low (< 10 %) |
| Oxygen | O₂ | 0 – 0.35 % | Low (< 0.2 %) | High (> 1.0 %) | High (> 4.0 %) |
| Nitric oxide | NOₓ | < 100 ppm | Very low | Very high | Low |
| Lambda | λ | 0.995 – 1.005 | < 1.000 | > 1.000 | > 1.000 (false-lean) |

## 3.7 Sensor cross-sensitivity reference {#CONCEPT_CROSS_SENSITIVITY}

| Target sensor | Interfering gas | Applied conc. | Response | Resulting error |
|---|---|---|---|---|
| CO | H₂ | 100 ppm | < 50 % | False high |
| CO | H₂S | 5 ppm | < 0.1 % | Minimal (filtered) |
| NO₂ | H₂S | 5 ppm | < −80 % | False low (negative) |
| NO | H₂S | 5 ppm | < 20 % | False high |
| NO | NO₂ | 5 ppm | < 7 % | False high |

GASLab raises `SENSOR_INTERFERENCE_SUSPECT` when companion-gas patterns suggest cross-talk is biasing a primary reading.

## Graph relations (explicit)

**GAS_HC** CONSUMED_BY **gaslab.rule_engine._matching_fault_candidates** via **GasReading**
**GAS_CO** CONSUMED_BY **gaslab.rule_engine._matching_fault_candidates** via **GasReading**
**GAS_CO2** CONSUMED_BY **gaslab.rule_engine._matching_fault_candidates** via **GasReading**
**GAS_O2** CONSUMED_BY **gaslab.rule_engine._matching_fault_candidates** via **GasReading**
**GAS_NOX** CONSUMED_BY **gaslab.rule_engine._matching_fault_candidates** via **GasReading**
**GAS_CO** INDICATES **rich mixture** when > 1.5 %
**GAS_O2** INDICATES **lean mixture** when > 2.5 %, **misfire** when > 3.0 % with high HC, **air leak** when high with normal HC/CO
**GAS_HC** INDICATES **combustion failure** when > 1000 ppm
**GAS_NOX** INDICATES **combustion temperature** — suppressed by rich, elevated by lean/EGR fault
**CONCEPT_5GAS_CHEATSHEET** MAPS_TO **five-gas directional patterns** (Rich, Lean, Misfire) for rapid triage
**CONCEPT_CROSS_SENSITIVITY** DESCRIBES **H₂ interference on CO NDIR**, **H₂S interference on NO/NO₂ electrochemical**
**SENSOR_INTERFERENCE_SUSPECT** INDICATES **cross-sensitivity bias** detected by companion-gas pattern
**ΔO₂ per misfiring cylinder** CONSUMED_BY **cylinder_count** from **GasLabDnaView** (≈ 21 % / N)
**per-cylinder misfire math** CONSUMES **GasLabDnaView.cylinder_count**
**CO₂** INDICATES **combustion efficiency** — peaks at λ ≈ 1.000, falls below ceiling with any combustion disturbance

## Core Entities

- **GAS_HC** — Hydrocarbons (ppm), NDIR ~3.4 µm. Normal: ≤ 35 ppm (with cat), ≤ 250 ppm (no cat). Consumer: `GasReading` → `rule_engine._signature_values`.
- **GAS_CO** — Carbon monoxide (vol %), NDIR ~4.7 µm. Normal: 0.1–0.45 % (with cat). One-way rich indicator. Consumer: `GasReading` → `rule_engine._signature_values`.
- **GAS_CO2** — Carbon dioxide (vol %), NDIR ~4.3 µm. Normal: 14.5–16.0 % (with cat). Combustion efficiency score card. Consumer: `GasReading` → `rule_engine._signature_values`.
- **GAS_O2** — Oxygen (vol %), electrochemical/paramagnetic. Normal: ≤ 0.35 % (post-cat). Truthful post-catalyst mixture indicator. Consumer: `GasReading` → `rule_engine._signature_values`.
- **GAS_NOX** — Oxides of nitrogen (ppm), electrochemical. Normal: < 100 ppm (idle). Thermal NO indicator. Consumer: `GasReading` → `rule_engine._signature_values`.
- **CONCEPT_5GAS_CHEATSHEET** — directional pattern table (Rich/Lean/Misfire) for rapid triage. Consumer: `gaslab.rule_engine._matching_fault_candidates`.
- **CONCEPT_CROSS_SENSITIVITY** — sensor interference reference (H₂ on CO, H₂S on NO/NO₂). Consumer: `SENSOR_INTERFERENCE_SUSPECT` logic.
