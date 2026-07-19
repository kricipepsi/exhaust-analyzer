---
chunk_id: GASWIKI-04
title: "Inter-Gas Grammar & Validity Gates"
doc: GAS_WIKI
version: v2.0
summary: "The validity gates (Exhaust Gas Triangle, dilution screen, cranking shape) run before anything else, plus the reasoning grammar that turns five numbers into one verdict: seesaws, truth tables, named overrides (masking, collision, cam-timing, λ-mismatch). Includes pre-cat-leak-vs-sampling-error resolution and quantified ECU-vs-tailpipe divergence magnitudes."
covers_v1_sections: [6, 8]
entities_defined: [GATE_TRIANGLE, GATE_DILUTION, GATE_CRANKING_SHAPE, RULE_SEESAW, RULE_HC_O2_CO_TRUTH_TABLE, RULE_HC_NOX_ANTICORR, RULE_MASKING, RULE_COLLISION, RULE_WVT, RULE_LAMBDA_MISMATCH, RULE_SANITY_RAILS, CONCEPT_DIVERGENCE_MAGNITUDE, CONCEPT_LEAK_VS_SAMPLING]
related_chunks: [GASWIKI-02, GASWIKI-03, GASWIKI-05, GASWIKI-08]
sources: ["GAS_WIKI.md v1.0 §6, §8", "research q3", "research q6"]
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "validity-grammar"
implements:
  - "labs/gaslab/gaslab/validity_gates.py"
  - "labs/gaslab/gaslab/rule_engine.py"
  - "labs/gaslab/gaslab/resolution.py"
  - "labs/gaslab/gaslab/audits.py"
  - "labs/gaslab/gaslab/data/gas_lab_ontology.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py sample_validity"
  - "comlab: labs/comlab/comlab/schemas/vocabulary.py sample_validity mirror"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
drift_guards:
  - "labs/gaslab/tests/unit/test_validity_gates.py"
  - "labs/gaslab/tests/unit/test_rule_engine.py"
  - "labs/gaslab/tests/unit/test_resolution.py"
  - "labs/gaslab/tests/unit/test_validators.py"
tags: ["gaslab", "validity-grammar", "wiki"]
source: "labs/gaslab/wiki/04_inter_gas_grammar_validity_gates.md"
---

# 4. Inter-Gas Grammar & Validity Gates

> **Chunk summary.** Chemistry-level validity gates first, then the reasoning rules and named overrides. Two v2 additions: how to tell a real pre-cat air leak from a sampling-apparatus leak, and how far tailpipe chemistry diverges from ECU perception per fault.

---

## Part A — Validity gates (run before anything else)

### 4.1 The Exhaust Gas Triangle (Rule of 16 / Rule of 15) {#GATE_TRIANGLE}

In a clean petrol burn the sum `[CO] + [CO₂] + [O₂] ≈ 14 – 16 %` is **invariant** regardless of mixture — the reaction shuffles oxygen between CO and CO₂; the total stays the same.

| Sum value (vol %) | `sample_validity` | Behaviour |
|---|---|---|
| 14.0 – 16.0 | `VALID` | proceed |
| 16.0 – 18.0 | `EXTERNAL_O2_SUSPECT` | warn + run; downstream rules still evaluate |
| < 14.0 | `INVALID` | halt — `chemical_state = SAMPLE_INVALID` |
| > 18.0 | `INVALID` | halt — likely ambient-air probe / sensor fault |

This is the **only** gate that can halt evaluation outright. The sum drifts outside [14,16] only via (a) ambient-air dilution (sum rises past 16) or (b) probe-insertion failure (sum collapses or spikes to ambient). **Do not relax `SUM_VALID_MIN = 14.0`** for ethanol blends or altitude (→ CONCEPT_FUEL_ALTITUDE) — re-validate with other data instead.

### 4.2 The dilution screen {#GATE_DILUTION}

Rapid sanity check: `[CO] + [CO₂] > 6 %`. An undiluted sample always satisfies it; ≤ 6 % indicates heavy dilution.

### 4.3 The cranking / ambient-air shape {#GATE_CRANKING_SHAPE}

HC ≈ 0, CO ≈ 0, CO₂ ≈ 0.04 %, O₂ ≈ 20.9 % gives a triangle sum ≈ 20.94 %, rejected as `INVALID`. There is no separate "no combustion" fault class — the triangle subsumes it (the envelope requires a warm running engine).

### 4.4 Pre-cat air leak vs sample-handling error {#CONCEPT_LEAK_VS_SAMPLING}

`[v2: q3]` The signature **low CO + elevated O₂ + low HC** is classic *dilution* — and a physical exhaust leak (cracked manifold, failed flex pipe) is **chemically identical** to a sampling-apparatus leak (loose probe, leaking hose). Both inject ~20.9 % O₂ atmospheric air.

**Key limitation:** while the triangle sum is still inside 14–18 %, the analyser **cannot** distinguish the two from gas data alone. The gate confirms the gas is "exhaust-like"; it cannot confirm the exhaust solely represents the engine's output. Resolution needs a **second source of truth** — OBD fuel trims — plus a mechanical check:

| Indicator | Pre-cat exhaust leak (real) | Sampling-apparatus (probe) leak |
|---|---|---|
| Analysed O₂ | High | High |
| STFT (OBD) | Positive — ECU adding fuel | Normal (≈ 0 % / oscillating) |
| Upstream O₂ sensor | Reads lean (ECU reacts) | Reads normal (true exhaust) |
| Engine performance | Possible rough idle / misfire | Smooth |

**Protocol.** (1) High analyser O₂ → read STFT. Positive STFT ⇒ engine truly lean / leak is **physical**. STFT ≈ 0 with high analyser O₂ ⇒ leak is in the **sampling apparatus**. (2) Confirm with the **probe-occlusion test** (→ TEST_PROBE_OCCLUSION, GASWIKI-08): block the probe tip; the pump should stall and O₂ should drop to near 0. If it doesn't, the sampling system leaks. The escalation that follows a triangle breach lives at → FAULT_EXHAUST_AIR_LEAK (GASWIKI-05).

---

## Part B — Inter-gas reasoning grammar

These laws turn five numbers into one verdict. Every rule in the engine is grounded in one or more of them.

### 4.5 The CO ↔ O₂ seesaw {#RULE_SEESAW}

CO and O₂ sit on opposite ends of one balance:

- CO up, O₂ down → rich; CO down (≈ 0), O₂ up → lean.
- **CO up AND O₂ up together → COLLISION** — physically impossible in a single balanced event. Two explanations: rich-side fuel dump with partial misfire, or downstream air ingress. Disambiguated by the triangle (→ GATE_TRIANGLE): sum ≈ 15 ⇒ rich misfire; sum > 16 ⇒ ingress.

The quantified form of this discriminator lives at → CONCEPT_COMBUSTION_INTEGRITY (GASWIKI-02 §2.10); keep the formula there so this section remains the rule grammar.

### 4.6 The HC + O₂ + CO truth table {#RULE_HC_O2_CO_TRUTH_TABLE}

| HC | O₂ | CO | Outcome |
|---|---|---|---|
| Low | Low | Low | Clean burn (verify CO₂ high) |
| Low | Low | High | Rich mixture (excess fuel, O₂ consumed) |
| Low | High | Low | Lean mixture **or** exhaust leak — disambiguate with CO₂ and triangle |
| Low | High | High | Downstream air ingress on rich engine (collision) |
| High | Low | Low | Mechanical / oil-burn (HC up, balance preserved) |
| High | Low | High | Rich misfire (fuel dump + partial ignition) |
| High | High | Low | Lean misfire (ignition failed, raw air + raw fuel escape) |
| High | High | High | Severe rich misfire / multi-mode / sample contamination |

The O₂-vs-CO reasoning behind the misfire/rich split is summarised at → CONCEPT_COMBUSTION_INTEGRITY (GASWIKI-02 §2.10), without adding a separate numeric ratio threshold.

### 4.7 The HC ↔ NOₓ anti-correlation near stoichiometry {#RULE_HC_NOX_ANTICORR}

Burning HC lifts peak temperature → NOₓ rises; quenching the burn (rich or misfire) suppresses NOₓ.

- High HC + high NOₓ → lean misfire under load (or EGR fault, or oil burning).
- High HC + low NOₓ → ignition misfire (cylinder didn't fire, no heat).

### 4.8 The masking rule (named override) {#RULE_MASKING}

```
HC > 1000 ppm  AND  O₂ > 3.0 %  AND  NOₓ < 50 ppm
  ⇒  IGNITION_MISFIRE  (override any LEAN verdict)
```

No combustion → no heat → no NOₓ despite the air looking lean. **Priority 85** (above all lean/rich rules at 80).

### 4.9 The collision rule (named override) {#RULE_COLLISION}

```
CO > tier_max  AND  O₂ > 2.0 %
  AND triangle 14 – 16 %  ⇒  RICH_MISFIRE
  AND triangle > 16 %     ⇒  EXHAUST_AIR_LEAK (downstream ingress on rich)
```

**Priority 80.**

### 4.10 The cam-timing rule (named override) {#RULE_WVT}

`[v2.1: q7]` Retargeted from the retired single `WRONG_VALVE_TIMING` to the three system-specific cam-timing states (→ FAULT_CAM_TIMING_RETARDED_MAF, → FAULT_CAM_TIMING_ADVANCED, → FAULT_CAM_TIMING_RETARDED_MAP, GASWIKI-06B). Pure rich and pure lean cannot explain HC + CO + O₂ all elevated — mechanical, not fuel-mixture.

```text
# Lean / mixed branch — Priority 82 (above collision, below masking)
HC > 1000 ppm  AND  CO present  AND  O₂ > 2.0 %
  → O₂ 2.0–4.5 %, λ 1.08–1.18, signature PERSISTS at 2500 RPM   ⇒ CAM_TIMING_RETARDED_MAF
  → O₂ 1.2–2.5 %, λ 1.03–1.08, NOₓ RISES at 2500 RPM            ⇒ CAM_TIMING_ADVANCED

# Rich branch (Speed-Density over-fuelling) — Priority 40 fallback
CO 3.5–7.0 %  AND  O₂ ≈ 0  AND  λ 0.75–0.88
  AND signature PARTIALLY normalises toward 2500 RPM            ⇒ CAM_TIMING_RETARDED_MAP
  (disambiguated from RICH_MIXTURE by the RPM-normalisation tell + OBD trims −27…−45 %)
```

> Ontology / code note: the ontology (`gas_lab_ontology.yaml` WVT rule) and `resolution.py` currently emit the single `WRONG_VALVE_TIMING` on `HC > 1000` and `O₂ > 5.0%`. Re-binding this rule to the three `CAM_TIMING_*` states (and the rich-branch RPM-normalisation discriminator) is part of the coordinated cross-lab change in → GAS_VOCABULARY §21; superseding the older T-DOC-13 row 18 note.

### 4.11 The λ-mismatch (truth-vs-perception) rule {#RULE_LAMBDA_MISMATCH}

λ from chemistry (Brettschneider on tailpipe gases) is **ground truth**; λ from the ECU (upstream O₂ sensor) is **perception**. When they disagree:

| Δλ | Verdict |
|---|---|
| ≤ 0.05 | Sensors agree — proceed |
| 0.05 – 0.08 | Borderline — investigate fuel trims and exhaust leak first |
| > 0.08 | Mismatch — raise the truth-vs-perception override |

Most likely candidates: upstream O₂ sensor skewed, exhaust leak upstream of the sensor, ECU calibration drift. This surfaces as `O2_SENSOR_BIASED_LOW` / `_HIGH` in the atlas (→ FAULT_O2_SENSOR_BIASED_LOW, GASWIKI-05).

### 4.12 ECU-vs-tailpipe divergence magnitudes {#CONCEPT_DIVERGENCE_MAGNITUDE}

`[v2: q6]` The λ-mismatch detector needs to know how *much* divergence each fault produces — if divergence is usually small the detector has little to work with. Empirically (1990–2010 petrol) divergence is common and frequently large, because the onboard O₂/AFR sensor measures only oxygen and is biased by physical/chemical degradation, whereas Brettschneider balances all five gases.

| Divergence scenario | Typical magnitude | Mechanism (perception vs reality) |
|---|---|---|
| **Ignition misfire** | up to **Δλ ≈ 0.24** | O₂ spike (~4 % pre-cat, 6-cyl single miss) reads "false lean"; early-era ECUs chase it, adding up to 30–77 % fuel. Tailpipe truth: actual λ ≈ 0.76–0.85 (rich). |
| **O₂-sensor poisoning / signal bias** | **Δλ ≈ 0.15 – 0.23** | Silicone/silicate/oil contamination skews sensor voltage low (lean); ECU enriches. Tailpipe truth: λ ≈ 0.77–0.85, CO often 5–8 %. |
| **Upstream exhaust air leak** | **Δλ ≈ 0.05 – 0.10** | Tramp O₂ drives sensor lean; ECU enriches ~5 % to re-centre → actual λ ≈ 0.950 against a reported 1.000. |
| **Wideband calibration-resistor damage** (late-2000s LSU 4.2/4.9) | **Δλ ≈ 0.12 – 0.18** | Corroded pins / damaged trim resistor break the current-to-λ curve; probe may report 1.30 while actual is 1.10, or 0.82 while actual is 0.95 — erratic over-correction. |

**Reading:** a measured Δλ between chemistry and ECU is not noise — it sizes the fault. Δλ ≈ 0.05–0.10 with normal-looking gases points to a leak; Δλ > 0.15 with high CO points to sensor bias or chased misfire. Cross-check against the gas vector before naming the bias direction.

### 4.13 Cross-channel sanity rails {#RULE_SANITY_RAILS}

- HC/CO/CO₂/O₂ must be physically consistent: triangle sum 14–16 % at idle. Outside that ⇒ sensor problem, air leak, or analyser drift.
- λ from analyser within ±0.08 of ECU's λ is normal; wider raises perception-contradiction (→ RULE_LAMBDA_MISMATCH).
- Idle NOₓ > ~1000 ppm is suspicious — confirm load, EGR, cooling.
- Trims (STFT/LTFT) outside ±25 % at idle indicate a real large mixture issue or sensor rail-out — OBDLab's job, surfaced to COMLab.

### 4.14 The cranking-shape rule {#RULE_CRANKING}

Handled by the triangle gate (→ GATE_CRANKING_SHAPE). No separate "no combustion" class exists because the envelope requires a warm running engine.

## Graph relations (explicit)

**GATE_TRIANGLE** VALIDATES **sample_validity** — halts on `INVALID`, warns on `EXTERNAL_O2_SUSPECT`
**GATE_TRIANGLE** CONSUMED_BY **gaslab.validity_gates.sample_validity**
**GATE_DILUTION** VALIDATES **sample_validity** — rapid CO+CO₂ > 6 % check
**GATE_DILUTION** CONSUMED_BY **gaslab.validity_gates.sample_validity**
**GATE_CRANKING_SHAPE** SUBSUMED_BY **GATE_TRIANGLE** (sum ≈ 20.94 % → INVALID)
**CONCEPT_LEAK_VS_SAMPLING** DISAMBIGUATED_BY **STFT** (OBD) and **TEST_PROBE_OCCLUSION**
**CONCEPT_LEAK_VS_SAMPLING** ROUTES_TO **FAULT_EXHAUST_AIR_LEAK** when leak confirmed physical
**RULE_SEESAW** DISAMBIGUATED_BY **CO up + O₂ down → rich**, **CO down + O₂ up → lean**, **CO up + O₂ up → COLLISION**
**RULE_HC_O2_CO_TRUTH_TABLE** MAPS_TO **eight directional patterns** feeding fault-matching
**RULE_HC_NOX_ANTICORR** STATES **high HC + high NOₓ → lean under load or EGR fault**
**RULE_MASKING** OVERRIDES **all lean verdicts** at priority 85 (HC > 1000, O₂ > 3.0 %, NOₓ < 50 → IGNITION_MISFIRE)
**RULE_MASKING** CONSUMED_BY **gaslab.rule_engine._definitive_match**
**RULE_COLLISION** DISAMBIGUATED_BY **GATE_TRIANGLE** — sum ≈ 15 % → RICH_MISFIRE; sum > 16 % → EXHAUST_AIR_LEAK
**RULE_COLLISION** CONSUMED_BY **gaslab.rule_engine._definitive_match** at priority 80
**RULE_WVT** MAPS_TO **CAM_TIMING_RETARDED_MAF** (lean/mixed branch, O₂ 2.0–4.5 %, λ 1.08–1.18), **CAM_TIMING_ADVANCED** (lean branch, O₂ 1.2–2.5 %, λ 1.03–1.08), **CAM_TIMING_RETARDED_MAP** (rich branch, CO 3.5–7.0 %, λ 0.75–0.88)
**RULE_WVT** CONSUMED_BY **gaslab.rule_engine._definitive_match** at priority 82
**RULE_LAMBDA_MISMATCH** COMPARES **Brettschneider λ (ground truth)** vs **ECU λ (perception)**
**RULE_LAMBDA_MISMATCH** INDICATES **O2_SENSOR_BIASED_LOW** or **O2_SENSOR_BIASED_HIGH** when Δλ > 0.08
**CONCEPT_DIVERGENCE_MAGNITUDE** QUANTIFIES **Δλ per fault type** — misfire up to ~0.24, O₂-sensor bias ~0.15–0.23, air leak ~0.05–0.10, wideband damage ~0.12–0.18
**CONCEPT_DIVERGENCE_MAGNITUDE** CONSUMED_BY **RULE_LAMBDA_MISMATCH** truth-vs-perception detector
**RULE_SANITY_RAILS** FLAGS **OBD trims outside ±25 %**, **idle NOₓ > 1000 ppm**, **λ mismatch > 0.08**
**RULE_WVT** ROUTES_TO **gaslab.ontology.gas_lab_ontology.yaml** (rule definition)
**RULE_WVT** ROUTES_TO **gaslab.resolution** (differentiator application)

## Core Entities

- **GATE_TRIANGLE** — CO+CO₂+O₂ sum 14.0–16.0 % = VALID; 16.0–18.0 % = EXTERNAL_O2_SUSPECT; <14.0 or >18.0 = INVALID. Consumer: `gaslab.validity_gates.sample_validity`.
- **GATE_DILUTION** — CO+CO₂ > 6 % rapid sanity check. Consumer: `gaslab.validity_gates.sample_validity`.
- **GATE_CRANKING_SHAPE** — ambient-air signature detection (HC≈0, CO≈0, CO₂≈0.04 %, O₂≈20.9 %). Subsumed by GATE_TRIANGLE.
- **CONCEPT_LEAK_VS_SAMPLING** — pre-cat exhaust leak vs probe-apparatus leak resolution via STFT + probe-occlusion test. Consumer: `RULE_COLLISION`, `TEST_PROBE_OCCLUSION`.
- **RULE_SEESAW** — CO↔O₂ inverse balance; collision when both high. Consumer: `gaslab.rule_engine._matching_fault_candidates`.
- **RULE_HC_O2_CO_TRUTH_TABLE** — eight-pattern truth table mapping HC/O₂/CO combinations to outcomes. Consumer: `gaslab.rule_engine._matching_fault_candidates`.
- **RULE_HC_NOX_ANTICORR** — HC↔NOₓ anti-correlation near stoichiometry. Consumer: `gaslab.rule_engine._matching_fault_candidates`.
- **RULE_MASKING** — named override (priority 85): HC>1000 + O₂>3.0% + NOₓ<50 → IGNITION_MISFIRE. Consumer: `gaslab.rule_engine._definitive_match`.
- **RULE_COLLISION** — named override (priority 80): CO+O₂ both high, triangle-disambiguated. Consumer: `gaslab.rule_engine._definitive_match`.
- **RULE_WVT** — cam-timing rule (priority 82 lean/mixed, 40 rich fallback): three-branch CAM_TIMING_* discrimination via RPM-normalisation. Consumer: `gaslab.rule_engine._definitive_match`, `gaslab.resolution`.
- **RULE_LAMBDA_MISMATCH** — truth-vs-perception λ comparison (Δλ > 0.08 triggers override). Consumer: `RULE_LAMBDA_MISMATCH` in rule engine.
- **CONCEPT_DIVERGENCE_MAGNITUDE** — per-fault ECU-vs-tailpipe Δλ magnitudes (misfire ~0.24, sensor bias ~0.15–0.23). Consumer: `RULE_LAMBDA_MISMATCH`.
- **RULE_SANITY_RAILS** — cross-channel consistency checks (trims, NOₓ, λ mismatch). Consumer: `gaslab.rule_engine._definitive_match`.
