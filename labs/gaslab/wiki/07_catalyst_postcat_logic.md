---
chunk_id: GASWIKI-07
title: "Catalyst & Post-Cat Logic"
doc: GAS_WIKI
version: v2.0
summary: "How a three-way catalyst works, pre/post-cat efficiency, the post-cat O₂ diagnostic (incl. the false-P0420 downstream-sensor trap), CO-drop expectations, NOₓ capacity, the CO-to-NOₓ failure transition, rejuvenation, the dual-idle (idle vs 2500 RPM) on-site test that separates a weak/lazy catalyst from a dead/poisoned one, the four catalyst/O₂-sensor poisoning agents (Si, P/Zn, S, Pb), and the healthy-catalyst masking limit where a working cat hides a feed-gas fault."
covers_v1_sections: [9]
entities_defined: [CONCEPT_TWC, CONCEPT_PRE_POST_CAT_EFFICIENCY, CONCEPT_POSTCAT_O2_DIAGNOSTIC, CONCEPT_NOX_CAPACITY, CONCEPT_CO_TO_NOX_TRANSITION, TEST_REJUVENATION, TEST_DUAL_IDLE_CATALYST, CONCEPT_CATALYST_POISONING_AGENTS, CONCEPT_HEALTHY_CAT_MASKING]
related_chunks: [GASWIKI-02, GASWIKI-05, GASWIKI-08]
sources: ["GAS_WIKI.md v1.0 §9", "research q10", "cases_petrol (poisoning agents)", "casesextra Case 7"]
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "catalyst-logic"
implements:
  - "labs/gaslab/gaslab/rule_engine.py"
  - "labs/gaslab/gaslab/resolution.py"
  - "labs/gaslab/gaslab/data/gas_lab_ontology.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py lambda_chem/gas_o2"
drift_guards:
  - "labs/gaslab/tests/unit/test_rule_engine.py"
  - "labs/gaslab/tests/unit/test_resolution.py"
tags: ["gaslab", "catalyst-logic", "wiki"]
source: "labs/gaslab/wiki/07_catalyst_postcat_logic.md"
---

# 7. Catalyst & Post-Cat Logic

> **Chunk summary.** TWC chemistry and the diagnostics that depend on it, ending with the v2 dual-idle catalyst test that distinguishes a recoverable weak converter from a dead one.

## 7.1 How a three-way cat works {#CONCEPT_TWC}

Monolithic ceramic honeycomb with Pt + Pd for oxidation and Rh for NOₓ reduction. Ceria–zirconia promoters store O₂ during lean phases and release it during rich phases.

```
Oxidation:  2 CO + O₂  →  2 CO₂
             CxHy + O₂  →  CO₂ + H₂O
Reduction:  2 NO + 2 CO →  N₂ + 2 CO₂
```

## 7.2 Pre- vs post-cat efficiency {#CONCEPT_PRE_POST_CAT_EFFICIENCY}

| Condition | Pre-cat CE | Post-cat CE | Tailpipe CO | Tailpipe HC | Tailpipe O₂ |
|---|---|---|---|---|---|
| Healthy engine + healthy cat | ~95 % | > 99 % | 0.1 – 0.45 % | < 35 ppm | < 0.35 % |
| Healthy engine + failed cat | ~95 % | < 97 % | 0.5 – 0.9 % | 75 – 125 ppm | 0.3 – 0.7 % |
| Rich mixture + healthy cat | < 90 % | ~ 90 % | High (> 1 %) | Moderate | Very low |
| Misfire + healthy cat | < 80 % | < 85 % | Moderate | Very high | High |

**CO-drop expectations:** no air pump — max CO drop ≈ 2 % across a working cat (1.0 → ~0.05 %); with air pump — up to 8 % drop (8 → 0.1 %).

## 7.3 Post-cat O₂ sensor diagnostic {#CONCEPT_POSTCAT_O2_DIAGNOSTIC}

The downstream O₂ sensor is a switching narrowband for OBD-II monitoring. With a healthy cat the rear sensor is slow and flat (oxygen storage absorbs ECU oscillations). When the cat degrades it begins to mirror the upstream — high-frequency switching at cross-counts approaching 1:1 is the OBD test for P0420/P0430. GASLab does not consume the switching directly (OBDLab's job), but COMLab can pass `downstream_o2_sensor_switching` so GASLab can raise `rule_downstream_mirroring_upstream` if the chemistry agrees.

**The false-P0420 trap (gas refutes the DTC) `[v2.2: casesextra]`.** A failed *downstream* O₂ sensor that mimics upstream switching sets P0420 on a **perfectly healthy catalyst**. The gas analyser breaks the tie: a truly failed cat produces breakthrough gases (tailpipe **HC > 80 ppm, CO > 0.2 %, and/or elevated O₂**), whereas pristine tailpipe chemistry — **CO < 0.05 %, HC < 25 ppm, CO₂ > 14.5 %, λ 0.98–1.02 at both idle and 2500 RPM** — with P0420 set is a **downstream-sensor fault until proven otherwise**, not a cat. **Routing:** `P0420 present AND tailpipe chemistry clean at both speeds` ⇒ suppress `CATALYST_OVERWHELMED`/`CATALYST_NOT_LIGHTING_OFF` and surface the downstream-O₂-sensor candidate (OBDLab confirms via the rear-sensor waveform). **Consumer:** catalyst-vs-sensor disambiguation in COMLab fault-atlas routing — prevents an expensive catalyst misdiagnosis. Source: `casesextra` Case 7.

## 7.4 NOₓ capacity and the CO-to-NOₓ transition {#CONCEPT_NOX_CAPACITY}

The reduction bed can process ≈ **2000 ppm NOₓ** under normal conditions; NOₓ above this cannot be addressed by the converter alone — focus on EGR, timing, combustion temperature, not converter replacement.

**The CO-to-NOₓ failure transition (clinical trap) {#CONCEPT_CO_TO_NOX_TRANSITION}.** A vehicle arrives failing CO; rich is corrected; on retest CO is normal but **NOₓ is now elevated**. Mechanism: rich running deposited carbon in the chamber and Rh bed; with stoich restored, peak temperature rises and the compromised Rh bed lets NOₓ through. **Action:** after repairing any sustained rich condition, check compression and decarbonise if elevated.

## 7.5 Converter rejuvenation — controlled misfire {#TEST_REJUVENATION}

Converters coated with carbon/sulfur (not physically destroyed) can be revived by controlled heating: confirm structurally intact → induce a controlled misfire to push extra HC to the cat → HC oxidises on the surface, raising temperature → burns off the coating. **Never let shell temperature exceed 800 °F (427 °C).** Last resort, not routine.

## 7.6 The dual-idle catalyst efficiency test {#TEST_DUAL_IDLE_CATALYST}

`[v2: q10]` An on-site method for 1990–2010 petrol that isolates whether an emissions failure is a dead converter, a weak/degraded converter, or engine-out fuel control — using a **low-idle + 2500 RPM 5-gas and λ** comparison.

**Step 1 — precondition (validate fuel control first).** A cat cannot process bad feed gas. Check tailpipe λ at both speeds: it must hold tightly in **0.995–1.005** (or at least 0.98–1.02 to light off). Because λ is combustion-invariant (→ CONCEPT_BRETTSCHNEIDER), if λ sits in window but pollutants are high, fuel management is healthy and the failure is purely catalytic.

**Step 2 — the idle ↔ 2500 RPM delta:**

| Case | At 2500 RPM (hot, high flow) | At low idle (cooled) | Verdict |
|---|---|---|---|
| **Weak / degraded** (thermal "go-out") | CO₂ 14.5–16 %, O₂ < 0.5 %, CO < 0.2 %, HC < 35 ppm | **distinct divergence**: CO₂ 13.5–14.5 %, O₂ 0.3–0.7 %, CO 0.5–0.9 %, HC 75–125 ppm — despite λ ≈ 1.000 | Weak/lazy/partially contaminated cat (lost active surface area, "goes out" when cooled) |
| **Dead / melted / poisoned** | raw engine-out: CO₂ < 13.5 %, HC > 100, CO > 0.5 %, O₂ > 0.5 % | identical raw readings — **no delta** | Catastrophic loss of all oxygen-storage/conversion |

**Step 3 — confirming chemical markers:** (1) **CO₂ maximisation** — healthy CO₂ is 1–2 % higher at 2500 RPM than idle, peaking ~15–16 %; healthy engine but CO₂ < 14 % at 2500 ⇒ cat failing to oxidise carbon. (2) **O₂/CO balance** — both > 0.5 % simultaneously while λ is perfect ⇒ reactants present but the cat is inactive and failing to combine them.

**Routing.** A clear idle-vs-2500 delta with λ in window ⇒ `CATALYST_NOT_LIGHTING_OFF` (recoverable, → FAULT_CATALYST_NOT_LIGHTING_OFF); raw readings at both speeds with engine-out pollution beyond cat capacity ⇒ `CATALYST_OVERWHELMED` (→ FAULT_CATALYST_OVERWHELMED). This test is the catalyst arm of → TEST_RPM_SEPARATION_MATRIX (GASWIKI-08).

## 7.7 Catalyst & O₂-sensor poisoning agents {#CONCEPT_CATALYST_POISONING_AGENTS}

`[v2.2: cases_petrol]` Poisoning is chemically distinct from thermal failure: a poisoned cat is coated/adsorbed (often recoverable for sulphur, never for lead), a thermally-failed cat is melted/collapsed. **History splits them:** oil-burn / coolant-leak / leaded-fuel ⇒ poisoning; prolonged misfire / very-rich / over-rev ⇒ thermal. The four field agents, their source, tailpipe/sensor signature, reversibility, and the DNA gate COMLab uses to admit the agent-specific verdict:

| Agent | Source | Signature (gas + sensor) | Reversible? | DNA / co-signature gate |
|---|---|---|---|---|
| **Silicon (Si)** | RTV silicone sealant in intake/exhaust; coolant silicate inhibitors entering the chamber | Glassy SiO₂ on Pt/Pd sites. **O₂ sensor poisoned first** — white/beige glassy deposit on the sensor tip, then HC creeps up and efficiency falls over weeks | **No** (mechanical coating) | `contamination_history.silicone` OR coolant-loss co-signature; pairs with → FAULT_O2_SENSOR_BIASED_LOW (GASWIKI-05) |
| **Phosphorus / Zinc (P/Zn, ZDDP)** | ZDDP anti-wear additive in engine oil, entering when oil burns (rings / valve seals) | Oil-burn signature (**HC high, fuel trims ≈ 0 %**) **plus** progressive efficiency decline. Commonest long-term poison on high-mileage engines | **No** (gradual, months) | **Always gated on an oil-burn co-signature** (→ FAULT_WORN_VALVE_SEALS / FAULT_WORN_PISTON_RINGS / FAULT_POA_SIGNATURE). Fix the oil burn first or the new cat re-poisons |
| **Sulphur (S)** | High-sulphur fuel | Temporary efficiency loss; **rotten-egg H₂S smell** (a healthy cat converts H₂S → odourless SO₂; a poisoned bed lets H₂S pass). **Intermittent P0420 after high-S fuelling that clears after a desulph event** | **Partial** — desulphurises on sustained high-load (cat > ~600 °C) | `fuel_quality.high_sulphur`; intermittent-P0420-with-no-mechanical-cause prior |
| **Lead (Pb)** | Leaded fuel / AvGas / aftermarket lead-substitute additives | **Immediate, permanent destruction at any concentration**; **CO and HC spike together**; onset within a single tank / drive cycle | **No** (immediate + irreversible) | `fuel_contamination_history.lead` |

**Consumer.** Catalyst fault-atlas routing (poisoning-vs-thermal branch on → CONCEPT_TWC / → TEST_DUAL_IDLE_CATALYST) plus DNA-gated contaminant ingestion: the agent-specific verdict ships **only** when its DNA/co-signature gate is satisfied — silicone needs a contamination/coolant signal, P/Zn needs an oil-burn co-signature, sulphur needs a fuel-quality prior, lead needs a fuel-contamination history. Without the gate GASLab emits the generic catalyst state, not the named agent. Sources: `cases_petrol` "Catalyst Poisoning Agents" + "Agent Detail" (Wikipedia — Catalyst Poisoning; Sustainability Directory — Catalyst Poisoning Mechanisms).

## 7.8 Healthy-catalyst masking (the "filter of truth" limit) {#CONCEPT_HEALTHY_CAT_MASKING}

`[v2.3: EP-CAT-02, EP-CAT-05; Vol1 N-008]` This is the inverse of a catalyst-failure diagnosis: the catalyst is healthy, lit, and high-OSC, so it scrubs the evidence of a sick engine before the tailpipe probe can see it. A leaking injector, high fuel pressure, GDI HPFP leak, or oil-burn feed can arrive at the cat as rich / HC-heavy gas; the converter oxidises CO + HC, buffers O₂ swings, and the **tailpipe** may still show near-normal HC/CO/O₂ with λ inside the catalyst window (0.97–1.03). The cat is doing its job; that is exactly why it hides the engine.

**What tailpipe gas can contribute.** Usually little on its own, and that is the teaching point. Two weak tells are still worth keeping:

- If the rich feed persists long enough, the cat saturates and tailpipe CO/HC begin to climb. By then masking is failing, not absent.
- The dual-idle / RPM behaviour (→ TEST_DUAL_IDLE_CATALYST §7.6; → TEST_RPM_SEPARATION_MATRIX in GASWIKI-08) can still expose a *cat* fault. A healthy cat masking a rich engine may show no useful gas delta, which is the trap.

**What tailpipe gas cannot do.** Tailpipe 5-gas alone cannot confirm or exonerate the engine upstream of a healthy catalyst. A clean downstream sample means the post-cat chemistry is clean; it does **not** prove the engine-out feed gas was healthy. This concept only applies when a catalyst is present / known, consistent with the `has_catalyst` scope shrinkage in GASWIKI-10 §10.2.

**Resolution lives outside GASLab.** The channels that break the ambiguity are perception / fusion inputs:

- **Pre-cat (upstream) O₂ stuck rich (> ~0.7 V) + negative LTFT at idle and cruise, while tailpipe λ remains in-window** ⇒ masked rich engine (EP-CAT-02). Pre-cat O₂ and LTFT are OBDLab perception channels and COMLab fusion evidence, not GASLab analyser inputs.
- **Pre-cat inference from catalyst inlet/outlet ΔT** (EP-CAT-05) ⇒ infer the feed-gas chemistry from the heat the cat releases; this is a COMLab L5 step, not a GASLab verdict.

**Routing rule.** When tailpipe chemistry is clean **but** pre-cat O₂ / LTFT indicate rich operation, COMLab should assert a masked-rich candidate (for example `Catalyst_Masking_Rich`) rather than returning `insufficient_evidence` or clean. GASLab's own emission remains the truthful tailpipe state; it does **not** fabricate an engine verdict the downstream gases cannot chemically support.

**Urgency.** Masked rich can drive the catalyst substrate toward thermal damage (~1000 °C, Denton §5). Flag and route it; do not clear it as a healthy engine.

## Graph relations (explicit)

**CONCEPT_TWC** DESCRIBES **Pt/Pd oxidation + Rh reduction + ceria O₂ storage**
**CONCEPT_TWC** ENABLES **post-cat diagnostics** — O₂ storage buffers ECU oscillations
**CONCEPT_PRE_POST_CAT_EFFICIENCY** COMPARES **engine-out CE (~95 %)** vs **tailpipe CE (> 99 % with working cat)**
**CONCEPT_POSTCAT_O2_DIAGNOSTIC** DESCRIBES **false-P0420 trap** — clean tailpipe chemistry + P0420 = downstream sensor fault
**CONCEPT_POSTCAT_O2_DIAGNOSTIC** ROUTES_TO **COMLab catalyst-vs-sensor disambiguation**
**CONCEPT_NOX_CAPACITY** STATES **Rh bed limit ≈ 2000 ppm NOₓ** — above this, focus on EGR/timing not converter
**CONCEPT_CO_TO_NOX_TRANSITION** WARNS **CO→NOₓ transition** after rich correction — carbon deposits mask NOₓ
**TEST_REJUVENATION** DESCRIBES **controlled-misfire carbon/sulfur burn-off** — last resort, shell < 800 °F
**TEST_DUAL_IDLE_CATALYST** DISAMBIGUATED_BY **idle vs 2500 RPM delta** — weak/lazy (delta present, λ in window) vs dead/poisoned (no delta, engine-out readings)
**TEST_DUAL_IDLE_CATALYST** ROUTES_TO **FAULT_CATALYST_NOT_LIGHTING_OFF** (recoverable) or **FAULT_CATALYST_OVERWHELMED** (catastrophic)
**TEST_DUAL_IDLE_CATALYST** IS catalyst arm of **TEST_RPM_SEPARATION_MATRIX** (GASWIKI-08)
**CONCEPT_CATALYST_POISONING_AGENTS** ENUMERATES **Silicon (Si)**, **Phosphorus/Zinc (P/Zn, ZDDP)**, **Sulphur (S)**, **Lead (Pb)**
**Silicon poisoning** ROUTES_TO **FAULT_O2_SENSOR_BIASED_LOW** — sensor poisoned first, then cat
**Silicon poisoning** GATED_BY **contamination_history.silicone** OR coolant-loss co-signature
**P/Zn poisoning** GATED_BY **oil-burn co-signature** — FAULT_WORN_VALVE_SEALS / FAULT_WORN_PISTON_RINGS / FAULT_POA_SIGNATURE
**Sulphur poisoning** INDICATED_BY **rotten-egg H₂S**, **intermittent P0420** — partially reversible via desulphurisation
**Lead poisoning** INDICATED_BY **immediate CO+HC spike**, **single-tank onset** — irreversible
**CONCEPT_HEALTHY_CAT_MASKING** MASKS **feed-gas faults** — healthy cat scrubs rich/lean evidence before tailpipe
**CONCEPT_HEALTHY_CAT_MASKING** ROUTES_TO **COMLab pre-cat O₂ + LTFT fusion** — tailpipe 5-gas alone cannot confirm/exonerate upstream engine
**CONCEPT_HEALTHY_CAT_MASKING** WARNS **masked rich → thermal damage risk (~1000 °C)**

## Core Entities

- **CONCEPT_TWC** — three-way catalyst: Pt/Pd oxidation, Rh reduction, ceria-zirconia O₂ storage. Consumer: `TEST_DUAL_IDLE_CATALYST`, `CONCEPT_CATALYST_POISONING_AGENTS`.
- **CONCEPT_PRE_POST_CAT_EFFICIENCY** — CE improvement from ~95 % (engine-out) to > 99 % (tailpipe) with working cat. Consumer: `FAULT_CATALYST_NOT_LIGHTING_OFF` gas vector thresholds.
- **CONCEPT_POSTCAT_O2_DIAGNOSTIC** — downstream O₂ sensor switching diagnostic; false-P0420 trap (clean chemistry + P0420 = sensor fault). Consumer: COMLab catalyst-vs-sensor disambiguation (not GASLab code directly).
- **CONCEPT_NOX_CAPACITY** — Rh bed ~2000 ppm NOₓ limit; failure above that is EGR/timing, not converter. Consumer: `FAULT_HIGH_COMBUSTION_TEMP` threshold.
- **CONCEPT_CO_TO_NOX_TRANSITION** — clinical trap: rich→stoich exposes compromised Rh bed. Consumer: post-repair verification logic (COMLab).
- **TEST_REJUVENATION** — controlled-misfire carbon burn-off for coated cats. Consumer: field diagnostic procedure (not automated).
- **TEST_DUAL_IDLE_CATALYST** — idle vs 2500 RPM delta: weak/lazy (delta present) vs dead (no delta). Consumer: `FAULT_CATALYST_NOT_LIGHTING_OFF` / `FAULT_CATALYST_OVERWHELMED` routing.
- **CONCEPT_CATALYST_POISONING_AGENTS** — Si, P/Zn, S, Pb: sources, signatures, DNA gates, reversibility. Consumer: catalyst fault-atlas routing (COMLab), DNA-gated contaminant ingestion.
- **CONCEPT_HEALTHY_CAT_MASKING** — working cat hides feed-gas faults; tailpipe 5-gas alone cannot confirm upstream engine health. Consumer: COMLab fusion (`Catalyst_Masking_Rich` candidate).
