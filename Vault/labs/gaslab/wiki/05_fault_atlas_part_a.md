---
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "fault-atlas-core"
implements:
  - "labs/gaslab/code/rule_engine.py"
  - "labs/gaslab/code/resolution.py"
  - "labs/gaslab/code/data/gas_lab_ontology.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py gas_co/gas_hc/gas_o2"
drift_guards:
  - "labs/gaslab/tests/unit/test_rule_engine.py"
  - "labs/gaslab/tests/unit/test_rule_engine_reachability.py"
  - "labs/gaslab/tests/unit/test_resolution.py"
  - "labs/gaslab/tests/unit/test_validators.py"
tags: [gaslab, finished, wiki]
source: "labs/gaslab/wiki/05_fault_atlas_part_a.md"
---

# 5. Fault Signature Atlas — Part A

> **Chunk summary.** Sixteen `chemical_state` entities. Each is a typed record (gas vector + DNA gate + match class + discriminator + cross-refs). Numeric thresholds are normative; directional patterns are the lookup key. `match_class` feeds the confidence ceiling (→ CONCEPT_CONFIDENCE_CEILING, GASWIKI-10).

---

### FAULT_NORMAL_OPERATION — healthy idle {#FAULT_NORMAL_OPERATION}
- **chemical_state:** `NORMAL_OPERATION` · **dna_gate:** none · **match_class:** FALLBACK
- **gas_vector:** HC 0–35 ppm | CO 0.1–0.45 % | CO₂ 14.5–16 % | O₂ 0–0.35 % | NOₓ < 100 ppm | λ 0.995–1.005
- Catalyst lit, mixture in window, triangle valid. Emitted by absence of any matching fault.

### FAULT_RICH_MIXTURE — too much fuel {#FAULT_RICH_MIXTURE}
- **chemical_state:** `RICH_MIXTURE` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector:** HC normal–moderate | CO **> 1.5 %** | CO₂ < 13 % | O₂ **< 0.5 %** | NOₓ very low | λ **< 0.95**
- **discriminator:** triangle valid; CO and O₂ in pure seesaw (→ RULE_SEESAW). Causes: high fuel pressure, leaking injectors, dirty MAF over-reading, choke stuck closed, EVAP purge fault, faulty ECT.

### FAULT_LEAN_MIXTURE — too much air {#FAULT_LEAN_MIXTURE}
- **chemical_state:** `LEAN_MIXTURE` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector:** HC low (< 300 ppm) | CO **< 0.1 %** | CO₂ < 13 % | O₂ **> 2.5 %** | NOₓ very high under load | λ **> 1.05**
- **discriminator:** triangle valid, HC modest. If HC rises significantly, route to → FAULT_LEAN_MISFIRE.

### FAULT_IGNITION_MISFIRE — classic spark fault {#FAULT_IGNITION_MISFIRE}
- **chemical_state:** `IGNITION_MISFIRE` · **dna_gate:** none (cylinder math needs `cylinder_count`) · **match_class:** DEFINITIVE (via → RULE_MASKING)
- **gas_vector:** HC **> 1000 ppm** | CO normal–low | CO₂ **< 10 %** | O₂ **> 3.0 %** | NOₓ **< 50 ppm** | λ ≥ 1.0 (false-lean)
- **discriminator:** masking rule fires. `inferred_misfiring_cylinder_count ≈ round(O₂ / (21 / cylinder_count))`. Note `[v2: q6]`: ECU may chase the O₂ spike with up to 30–77 % added fuel — chemistry λ stays misfire-immune while perception swings; expect a large Δλ (→ CONCEPT_DIVERGENCE_MAGNITUDE).

### FAULT_LEAN_MISFIRE — mixture too thin to flame {#FAULT_LEAN_MISFIRE}
- **chemical_state:** `LEAN_MISFIRE` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector:** HC 200–600 ppm | CO **< 0.2 %** | CO₂ < 12 % | O₂ **> 4 %** | NOₓ variable | λ **> 1.15**
- **discriminator:** if NOₓ also high (> 500 ppm) suspect EGR failure or oil burning (chamber hot enough to make NOₓ despite lean).

### FAULT_RICH_MISFIRE — fuel dumped, partially burnt {#FAULT_RICH_MISFIRE}
- **chemical_state:** `RICH_MISFIRE` · **dna_gate:** none · **match_class:** DEFINITIVE (via → RULE_COLLISION)
- **gas_vector:** HC high | CO **> 1.0 %** | CO₂ low | O₂ **> 2.0 %** | NOₓ low | λ < 1.0
- **discriminator:** collision pattern (CO and O₂ both high). Triangle disambiguates: sum > 16 % ⇒ ingress (→ FAULT_EXHAUST_AIR_LEAK); sum ≈ 15.5 % ⇒ rich misfire.

### FAULT_EXHAUST_AIR_LEAK — sample dilution {#FAULT_EXHAUST_AIR_LEAK}
- **chemical_state:** `EXHAUST_AIR_LEAK` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector:** HC normal | CO normal | CO₂ low | O₂ **> 2 %** | NOₓ low | λ falsely **> 1.05**
- **discriminator:** triangle sum < 14 % or > 16 % is the smoking gun. λ reads lean because Brettschneider sees ambient O₂ dilution; HC/CO unaffected (leak is downstream of combustion). **v2:** a physical leak and a sampling-apparatus leak look identical here — resolve via OBD STFT + probe occlusion (→ CONCEPT_LEAK_VS_SAMPLING, → TEST_PROBE_OCCLUSION).

### FAULT_HIGH_COMBUSTION_TEMP — EGR / cooling / over-advance {#FAULT_HIGH_COMBUSTION_TEMP}
- **chemical_state:** `HIGH_COMBUSTION_TEMP` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector:** HC normal | CO normal | CO₂ normal–high | O₂ normal | NOₓ **> 1000 ppm** under load | λ ≈ 1.0
- **discriminator:** all four "regular" gases look perfect — only NOₓ is off. Candidates: EGR blocked/stuck closed, coolant fault, timing over-advanced, lean under load.

### FAULT_CATALYST_NOT_LIGHTING_OFF — engine fine, cat cold / contaminated {#FAULT_CATALYST_NOT_LIGHTING_OFF}
- **chemical_state:** `CATALYST_NOT_LIGHTING_OFF` · **dna_gate:** `emissions.has_catalyst = true` · **match_class:** SPECIFIC
- **gas_vector:** HC 75–125 ppm | CO 0.5–0.9 % | CO₂ 13.5–14.5 % | O₂ 0.3–0.7 % | NOₓ normal | λ 0.995–1.005
- **discriminator:** engine in stoich window; converter failing to oxidise the small HC/CO remainder. Confirm weak-vs-dead with the dual-idle test (→ TEST_DUAL_IDLE_CATALYST). Causes: thermal damage, oil-ash poisoning, coolant contamination, fracture, or not yet warm.

### FAULT_CATALYST_OVERWHELMED — system-wide failure {#FAULT_CATALYST_OVERWHELMED}
- **chemical_state:** `CATALYST_OVERWHELMED` · **dna_gate:** `emissions.has_catalyst = true` · **match_class:** SPECIFIC
- **gas_vector:** HC > 200 ppm | CO > 1.0 % | CO₂ < 12 % | O₂ variable | NOₓ > 500 ppm | λ variable
- **discriminator:** engine making more pollution than the cat can convert, even if the cat works. Treat as multi-fault — escalate to COMLab.

### FAULT_SAMPLE_INVALID — analyser cannot diagnose {#FAULT_SAMPLE_INVALID}
- **chemical_state:** `SAMPLE_INVALID` · **dna_gate:** none · **match_class:** DEFINITIVE (via → GATE_TRIANGLE)
- **discriminator:** triangle sum outside [14, 18]. Probe not seated, exhaust leak, analyser drift, water condensation, or ambient air. The only value where `sample_validity = INVALID`. Refuse to diagnose; instruct re-prime.

### FAULT_TIMING_OVER_ADVANCED — Over-Advanced Ignition Timing (spark firing too early) {#FAULT_TIMING_OVER_ADVANCED}
- **chemical_state:** `TIMING_OVER_ADVANCED` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector (idle):** HC slight increase (120–250 ppm) | CO slight (0.10–0.30 %) | CO₂ 11.5–13 % | O₂ 0.8–1.5 % | NOₓ 20–60 | λ 1.01–1.04
- **gas_vector (2500 RPM):** NOₓ **very high (> 1200 ppm)**, others near normal | λ ≈ 1.0–1.06
- **discriminator** `[v2: q7]`: the signature is **RPM-dependent** — at idle thermal energy is low so NOₓ barely moves; at 2500 RPM under load peak temps exceed ~2500 °F and NOₓ spikes hard while the closed loop holds λ ≈ 1.0 with normal MAP. Distinct from → FAULT_HIGH_COMBUSTION_TEMP by the clean idle and the NOₓ-only high-idle spike. Pinging often audible. Carbon deposits / head machining raise effective compression and mimic this. Distinct from the *cam*-timing family (→ FAULT_CAM_TIMING_ADVANCED, → FAULT_CAM_TIMING_RETARDED_MAP, → FAULT_CAM_TIMING_RETARDED_MAF, GASWIKI-06B), which show rough idle and a λ offset *at idle* rather than a clean idle with a NOₓ-only high-idle spike.

### FAULT_TIMING_RETARDED — Retarded Ignition Timing (spark firing too late) {#FAULT_TIMING_RETARDED}
- **chemical_state:** `TIMING_RETARDED` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector (idle):** HC **300–800 ppm** | CO 0.05–0.15 % | CO₂ **< 11 %** | O₂ **1.5–3.5 %** | NOₓ **0–5 ppm** | λ **1.05–1.15 (false lean)**
- **gas_vector (2500 RPM):** HC 250–600 ppm | CO₂ 9–11.5 % | NOₓ near zero | λ 1.04–1.12
- **discriminator** `[v2: q7]`: late combustion continues into the exhaust stroke — peak temp and NOₓ collapse, EGT rises, cat/pipe run hot. The excess unreacted O₂ shifts the **calculated** λ artificially lean even though delivered AFR is stoichiometric (a chemistry-reads-lean / engine-is-fine case). HC stays high across both speeds; NOₓ stays near zero at both. Check base timing, cam timing, CKP sensor. This is the *ignition*-retard signature; a mechanically retarded *cam* routes instead to → FAULT_CAM_TIMING_RETARDED_MAP (rich) or → FAULT_CAM_TIMING_RETARDED_MAF (lean) per the load-calc system (GASWIKI-06B).

### FAULT_O2_SENSOR_BIASED_LOW — sensor under-reads O₂, ECU enriches {#FAULT_O2_SENSOR_BIASED_LOW}
- **chemical_state:** `O2_SENSOR_BIASED_LOW` · **dna_gate:** none · **match_class:** SPECIFIC (DEFINITIVE when → RULE_LAMBDA_MISMATCH fires)
- **gas_vector:** HC slight increase | CO **moderate–high increase** | CO₂ slight decrease | O₂ **low** | NOₓ slight decrease | λ(chem) **< 1.0 (rich)**
- **discriminator:** sensor signals less O₂ than present; ECU enriches. Chemistry λ rich while ECU perceives lean — truth-vs-perception mismatch, positive fuel trims on scan tool. `[v2: q6]` expect Δλ ≈ 0.15–0.23 with CO frequently 5–8 %. Causes: contamination, ageing, heater-circuit failure.
- **silicone-poisoning sub-case** `[v2.2: casesextra]`: Si from RTV sealant / silicone sprays / silicate coolant glazes the zirconia element and **locks the sensor at ~0.10–0.15 V (stuck lean, switch-rate < 4 / 10 s)** — distinct from a *lazy* sensor, which still switches. The ECU pegs trims (STFT/LTFT **> +15 %**), driving the engine severely rich (**λ(chem) ≈ 0.86, CO 4–5 %, HC ~400 ppm**) while it sets a **lean DTC (P0171)** — a **negative δλ** (gas richer than OBD, e.g. λ_gas 0.86 vs λ_OBD 1.07). The same agent then migrates to the cat → see → CONCEPT_CATALYST_POISONING_AGENTS (GASWIKI-07, Si row). Inspect the sensor tip for white/grey glassy deposit; the catalyst may already be thermally damaged. Source: `casesextra` Case 8.

### FAULT_O2_SENSOR_BIASED_HIGH — sensor over-reads O₂, ECU leans out {#FAULT_O2_SENSOR_BIASED_HIGH}
- **chemical_state:** `O2_SENSOR_BIASED_HIGH` · **dna_gate:** none · **match_class:** SPECIFIC (DEFINITIVE when → RULE_LAMBDA_MISMATCH fires)
- **gas_vector:** HC slight increase | CO **low** | CO₂ slight decrease | O₂ slight increase | NOₓ slight increase | λ(chem) **> 1.0 (lean)**
- **discriminator:** opposite of biased-low. Chemistry λ lean while ECU perceives rich — negative fuel trims. Wiring ground offset can also shift sensor voltage high. Late-era wideband calibration-resistor damage can produce erratic large Δλ (0.12–0.18) `[v2: q6]`.

### FAULT_WORN_ENGINE — generalised mechanical wear {#FAULT_WORN_ENGINE}
- **chemical_state:** `WORN_ENGINE` · **dna_gate:** none · **match_class:** CATCH_ALL (mechanical-wear fallback)
- **gas_vector:** HC slight–moderate increase (150–300 ppm) | CO slight increase | CO₂ slight decrease (11–13 %) | O₂ **slight increase (1–2 %)** | NOₓ no change/slight decrease | λ ≈ 1.0–1.03
- **discriminator:** worn rings/valve seals reduce compression and efficiency across all cylinders. **No RPM cleanup** (rules out valve seals) and **no high-idle spike** (rules out isolated piston-ring blow-by) — flat, lazy, inefficient at both speeds. Distinguish from oil burning by absence of λ mismatch / cat poisoning; from misfire by absence of a large O₂ spike. Routing detail → FAULT_POA_SIGNATURE discriminator (GASWIKI-06A).

## Graph relations (explicit)

**FAULT_NORMAL_OPERATION** INDICATES **NORMAL_OPERATION** — healthy idle, all gases in window
**FAULT_NORMAL_OPERATION** IS **FALLBACK** (match_class) — emitted by absence of any matching fault
**FAULT_RICH_MIXTURE** INDICATES **RICH_MIXTURE** — CO > 1.5 %, O₂ < 0.5 %, λ < 0.95
**FAULT_LEAN_MIXTURE** INDICATES **LEAN_MIXTURE** — CO < 0.1 %, O₂ > 2.5 %, λ > 1.05
**FAULT_IGNITION_MISFIRE** INDICATES **IGNITION_MISFIRE** — HC > 1000, O₂ > 3.0 %, NOₓ < 50
**FAULT_IGNITION_MISFIRE** VERIFIED_BY **RULE_MASKING** (priority 85, DEFINITIVE)
**FAULT_LEAN_MISFIRE** INDICATES **LEAN_MISFIRE** — HC 200–600, CO < 0.2 %, O₂ > 4 %, λ > 1.15
**FAULT_RICH_MISFIRE** INDICATES **RICH_MISFIRE** — collision pattern (CO + O₂ both high, triangle ≈ 15.5 %)
**FAULT_RICH_MISFIRE** VERIFIED_BY **RULE_COLLISION** (priority 80, DEFINITIVE)
**FAULT_EXHAUST_AIR_LEAK** INDICATES **EXHAUST_AIR_LEAK** — triangle sum outside valid range, λ false-lean
**FAULT_EXHAUST_AIR_LEAK** DISAMBIGUATED_BY **CONCEPT_LEAK_VS_SAMPLING** and **TEST_PROBE_OCCLUSION**
**FAULT_HIGH_COMBUSTION_TEMP** INDICATES **HIGH_COMBUSTION_TEMP** — NOₓ > 1000 under load, all other gases normal
**FAULT_CATALYST_NOT_LIGHTING_OFF** INDICATES **CATALYST_NOT_LIGHTING_OFF** — HC 75–125, CO 0.5–0.9, weak conversion
**FAULT_CATALYST_NOT_LIGHTING_OFF** GATED_BY **emissions.has_catalyst = true**
**FAULT_CATALYST_NOT_LIGHTING_OFF** DISAMBIGUATED_BY **TEST_DUAL_IDLE_CATALYST** (weak vs dead)
**FAULT_CATALYST_OVERWHELMED** INDICATES **CATALYST_OVERWHELMED** — HC > 200, CO > 1.0, NOₓ > 500
**FAULT_CATALYST_OVERWHELMED** GATED_BY **emissions.has_catalyst = true**
**FAULT_CATALYST_OVERWHELMED** ROUTES_TO **COMLab** — multi-fault escalation
**FAULT_SAMPLE_INVALID** INDICATES **SAMPLE_INVALID** — triangle sum outside [14, 18]
**FAULT_SAMPLE_INVALID** VERIFIED_BY **GATE_TRIANGLE** (DEFINITIVE)
**FAULT_TIMING_OVER_ADVANCED** INDICATES **TIMING_OVER_ADVANCED** — clean idle, NOₓ spikes at 2500 RPM (> 1200 ppm)
**FAULT_TIMING_OVER_ADVANCED** DISAMBIGUATED_BY **RPM-dependence** — distinct from FAULT_HIGH_COMBUSTION_TEMP and CAM_TIMING_* family
**FAULT_TIMING_OVER_ADVANCED** CONSUMES **GasLabDnaView.cylinder_count** via `inferred_misfiring_cylinder_count`
**FAULT_TIMING_RETARDED** INDICATES **TIMING_RETARDED** — HC 300–800, CO₂ < 11 %, NOₓ near zero, λ false-lean
**FAULT_TIMING_RETARDED** DISAMBIGUATED_BY **ignition-retard** vs **cam-retard** (routes to CAM_TIMING_RETARDED_MAP/_MAF)
**FAULT_O2_SENSOR_BIASED_LOW** INDICATES **O2_SENSOR_BIASED_LOW** — λ(chem) rich, ECU perceives lean, Δλ ≈ 0.15–0.23
**FAULT_O2_SENSOR_BIASED_LOW** VERIFIED_BY **RULE_LAMBDA_MISMATCH** (DEFINITIVE when fires)
**FAULT_O2_SENSOR_BIASED_LOW** ROUTES_TO **CONCEPT_CATALYST_POISONING_AGENTS** (Si poisoning, GASWIKI-07)
**FAULT_O2_SENSOR_BIASED_HIGH** INDICATES **O2_SENSOR_BIASED_HIGH** — λ(chem) lean, ECU perceives rich
**FAULT_O2_SENSOR_BIASED_HIGH** VERIFIED_BY **RULE_LAMBDA_MISMATCH** (DEFINITIVE when fires)
**FAULT_WORN_ENGINE** INDICATES **WORN_ENGINE** — flat, lazy at both speeds, no RPM cleanup, no O₂ spike
**FAULT_WORN_ENGINE** IS **CATCH_ALL** (match_class) — mechanical-wear fallback
**FAULT_WORN_ENGINE** DISAMBIGUATED_BY **FAULT_POA_SIGNATURE** (GASWIKI-06A)
**match_class** GATED_BY **CONCEPT_CONFIDENCE_CEILING** (GASWIKI-10) — FALLBACK → LOW, SPECIFIC → MEDIUM, DEFINITIVE → HIGH

## Core Entities

- **FAULT_NORMAL_OPERATION** — `NORMAL_OPERATION`, FALLBACK. HC 0–35, CO 0.1–0.45 %, CO₂ 14.5–16 %, O₂ 0–0.35 %, NOₓ < 100, λ 0.995–1.005. Consumer: `rule_engine.classify` (default output).
- **FAULT_RICH_MIXTURE** — `RICH_MIXTURE`, SPECIFIC. CO > 1.5 %, O₂ < 0.5 %, λ < 0.95. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_LEAN_MIXTURE** — `LEAN_MIXTURE`, SPECIFIC. CO < 0.1 %, O₂ > 2.5 %, λ > 1.05. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_IGNITION_MISFIRE** — `IGNITION_MISFIRE`, DEFINITIVE (via RULE_MASKING). HC > 1000, O₂ > 3.0 %, NOₓ < 50. Consumer: `rule_engine._definitive_match` (priority 85).
- **FAULT_LEAN_MISFIRE** — `LEAN_MISFIRE`, SPECIFIC. HC 200–600, CO < 0.2 %, O₂ > 4 %, λ > 1.15. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_RICH_MISFIRE** — `RICH_MISFIRE`, DEFINITIVE (via RULE_COLLISION). CO+O₂ both high, triangle ≈ 15 %. Consumer: `rule_engine._definitive_match` (priority 80).
- **FAULT_EXHAUST_AIR_LEAK** — `EXHAUST_AIR_LEAK`, SPECIFIC. Triangle outside [14,18], O₂ high, HC/CO normal. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_HIGH_COMBUSTION_TEMP** — `HIGH_COMBUSTION_TEMP`, SPECIFIC. NOₓ > 1000 under load, all other gases normal. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_CATALYST_NOT_LIGHTING_OFF** — `CATALYST_NOT_LIGHTING_OFF`, SPECIFIC. HC 75–125, CO 0.5–0.9, λ ≈ 1.0. Gated by `has_catalyst`. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_CATALYST_OVERWHELMED** — `CATALYST_OVERWHELMED`, SPECIFIC. Multi-fault escalation to COMLab. Gated by `has_catalyst`. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_SAMPLE_INVALID** — `SAMPLE_INVALID`, DEFINITIVE (via GATE_TRIANGLE). Triangle sum outside [14,18]. Consumer: `gaslab.validity_gates.sample_validity`.
- **FAULT_TIMING_OVER_ADVANCED** — `TIMING_OVER_ADVANCED`, SPECIFIC. Clean idle, NOₓ spike at 2500 RPM > 1200. RPM-dependent; distinct from CAM_TIMING_* family. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_TIMING_RETARDED** — `TIMING_RETARDED`, SPECIFIC. HC 300–800, CO₂ < 11 %, NOₓ near zero, λ false-lean. Ignition-retard; distinct from cam-retard. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_O2_SENSOR_BIASED_LOW** — `O2_SENSOR_BIASED_LOW`, SPECIFIC→DEFINITIVE (via RULE_LAMBDA_MISMATCH). λ(chem) rich, ECU lean, Δλ 0.15–0.23. Consumer: `rule_engine._definitive_match`.
- **FAULT_O2_SENSOR_BIASED_HIGH** — `O2_SENSOR_BIASED_HIGH`, SPECIFIC→DEFINITIVE (via RULE_LAMBDA_MISMATCH). λ(chem) lean, ECU rich. Consumer: `rule_engine._definitive_match`.
- **FAULT_WORN_ENGINE** — `WORN_ENGINE`, CATCH_ALL. Flat lazy at both speeds, no RPM cleanup. Consumer: `rule_engine._candidate_rank` (last-ranked fallback).
