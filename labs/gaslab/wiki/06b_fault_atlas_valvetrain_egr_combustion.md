---
chunk_id: GASWIKI-06B
title: "Fault Atlas — Part 6B: Valvetrain, EGR, EVAP & Combustion-Quality Faults"
doc: GAS_WIKI
version: v2.0
summary: "Cam timing as three system-specific states (retarded-MAP rich, retarded-MAF lean, advanced both-systems), EGR stuck closed/open, VVT failure, EVAP saturation, EGR dilution misfire, incomplete oxidation/combustion, and internal coolant leak (with the head-gasket oil-to-cylinder breach sub-mode). Ends with the consolidated 34-entry enum lookup."
covers_v1_sections: ["7.24", "7.33"]
entities_defined: [FAULT_CAM_TIMING_RETARDED_MAP, FAULT_CAM_TIMING_RETARDED_MAF, FAULT_CAM_TIMING_ADVANCED, FAULT_EGR_STUCK_CLOSED, FAULT_EGR_STUCK_OPEN, FAULT_VVT_FAILURE, FAULT_EVAP_CANISTER_SATURATED, FAULT_EGR_DILUTION_MISFIRE, FAULT_INCOMPLETE_OXIDATION, FAULT_INCOMPLETE_COMBUSTION, FAULT_COOLANT_LEAK_INTERNAL, CONCEPT_ENUM_SUMMARY_TABLE]
related_chunks: [GASWIKI-05, GASWIKI-06A, GASWIKI-08, GASWIKI-10]
sources: ["GAS_WIKI.md v1.0 §7.24–7.33", "research q4", "research q7"]
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "valvetrain-egr-atlas"
implements:
  - "labs/gaslab/gaslab/rule_engine.py"
  - "labs/gaslab/gaslab/resolution.py"
  - "labs/gaslab/gaslab/data/gas_lab_ontology.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py gas_co/gas_hc/gas_o2"
drift_guards:
  - "labs/gaslab/tests/unit/test_rule_engine.py"
  - "labs/gaslab/tests/unit/test_rule_engine_reachability.py"
  - "labs/gaslab/tests/unit/test_resolution.py"
  - "labs/gaslab/tests/unit/test_t_p8_7_hc_discriminator.py"
tags: ["gaslab", "valvetrain-egr-atlas", "wiki"]
source: "labs/gaslab/wiki/06b_fault_atlas_valvetrain_egr_combustion.md"
---

# 6B. Fault Atlas — Valvetrain, EGR, EVAP & Combustion-Quality

> **Chunk summary.** The remaining valvetrain / EGR / combustion-quality entities plus the consolidated 34-value lookup. v2 refinements: the cam-timing split into three system-specific states `[v2.1: q7]` (retired `WRONG_VALVE_TIMING`) and the head-gasket oil-to-cylinder breach sub-mode of coolant leak (q4).

---

> **v2.1 cam-timing taxonomy** `[v2.1: q7]` — the single `WRONG_VALVE_TIMING` value is retired and split into three system-specific states sourced from the q1&7 timings dossier. A physically retarded cam lowers pumping efficiency and raises MAP (low vacuum); the *emissions* fingerprint then depends on the load-calc system (Speed-Density inverts rich vs MAF lean), while an advanced cam presents the same mild-lean internal-EGR pattern on both systems. **Consumer for all three:** COMLab `chemical_state` routing / fault-atlas (this chunk). Tailpipe gas cannot prove cam *phase* on its own (that needs CKP/CMP correlation, OBDLab/DTCLab) → `match_class` SPECIFIC, not DEFINITIVE.

### FAULT_CAM_TIMING_RETARDED_MAP — retarded cam, Speed-Density (MAP) fuelling {#FAULT_CAM_TIMING_RETARDED_MAP}
- **chemical_state:** `CAM_TIMING_RETARDED_MAP` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector (idle):** HC **400–1200 ppm** | CO **3.5–7.0 %** | CO₂ 8.0–10.5 % | O₂ **< 0.5 %** | NOₓ 0–10 | λ **0.75–0.88 (rich)**
- **gas_vector (2500 RPM):** HC 200–600 | CO 1.5–4.5 % | CO₂ 11.0–13.0 % | O₂ < 0.5 % | NOₓ 100–400 | λ 0.85–0.95
- **discriminator:** retarded cam → low vacuum / high MAP; a Speed-Density ECU reads the high MAP as load and over-fuels → pure-rich tailpipe. Overlaps → FAULT_RICH_MIXTURE chemically; the tell is **partial normalisation toward 2500 RPM** as vacuum recovers (λ 0.85–0.95, CO falls) whereas a sensor/fuelling rich-bias stays flat. OBD corroboration: total fuel trim −27 % to −45 % at idle, correcting to −18 % to −27 % at stress idle (OBDLab/DTCLab). DTC context P0016–P0019 is DTCLab territory.

### FAULT_CAM_TIMING_RETARDED_MAF — retarded cam, MAF fuelling {#FAULT_CAM_TIMING_RETARDED_MAF}
- **chemical_state:** `CAM_TIMING_RETARDED_MAF` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector (idle):** HC **300–900 ppm** | CO 0.10–0.50 % | CO₂ 9.0–11.5 % | O₂ **2.0–4.5 %** | NOₓ 0–15 | λ **1.08–1.18 (lean)**
- **gas_vector (2500 RPM):** HC 150–400 | CO 0.10–0.30 % | CO₂ 11.5–13.5 % | O₂ 1.0–2.5 % | NOₓ 150–500 | λ 1.03–1.09
- **discriminator:** reversion + late exhaust events leave unburned O₂; a MAF ECU reads lean → positive trims (+22 % to +42 %). **Separation from a vacuum leak:** a vacuum leak's lean / positive trims **normalise** at 2500 RPM (metered air dominates); this cam fault **persists or worsens** across the whole RPM band because the mechanical phasing error persists (→ TEST_RPM_SEPARATION_MATRIX).

### FAULT_CAM_TIMING_ADVANCED — advanced cam, both load systems {#FAULT_CAM_TIMING_ADVANCED}
- **chemical_state:** `CAM_TIMING_ADVANCED` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector (idle):** HC 250–600 ppm | CO 0.20–0.80 % | CO₂ 10.0–12.5 % | O₂ 1.20–2.50 % | NOₓ 10–40 | λ **1.03–1.08 (mild lean)**
- **gas_vector (2500 RPM):** HC 100–300 | CO 0.15–0.50 % | CO₂ 12.0–14.0 % | O₂ 0.80–1.80 % | NOₓ **300–900** | λ 1.01–1.05
- **discriminator:** advancing the cam opens/closes valves early and widens overlap → internal-EGR dilution → rough idle, HC up, mild CO. **No Speed-Density-vs-MAF inversion** (both systems present the same mild-lean idle). At 2500 RPM dynamic scavenging stabilises combustion (HC/CO fall) while NOₓ **rises** with peak pressure/temperature. Separation from → FAULT_TIMING_OVER_ADVANCED (ignition): advanced *cam* shows rough-idle HC + mild-lean λ at idle, not the clean idle / NOₓ-only high-idle spike of ignition over-advance.

### FAULT_EGR_STUCK_CLOSED {#FAULT_EGR_STUCK_CLOSED}
- **chemical_state:** `EGR_STUCK_CLOSED` · **dna_gate:** `emissions.egr_equipped = true` · **match_class:** SPECIFIC
- **gas_vector:** HC normal | CO normal | CO₂ normal | O₂ normal | NOₓ **> 1000 ppm under load**
- **discriminator:** same gas pattern as → FAULT_HIGH_COMBUSTION_TEMP; GASLab emits the specific class only when DNA confirms EGR equipment. If DTC later confirms, COMLab renames.
- **dual-idle NOₓ-escalation signature** `[v2.2: casesextra]`: with zero recirculation, peak combustion temperature climbs hard with RPM. NOₓ steps from **~1200 ppm at idle to > 2500–3000 ppm at 2500 RPM (Δ > 1500 ppm is decisive)** while **HC and CO stay pristine throughout** (combustion is complete; there is simply no thermal suppression). DTC context P0401. **Polarity caution** `[v2.2: casesextra]`: stuck-**open** EGR requires NOₓ ≈ 0 — a high NOₓ at 2500 RPM rules out stuck-open and points here (stuck-closed / restricted). **Consumer:** dual-idle delta routing (→ TEST_RPM_SEPARATION_MATRIX, GASWIKI-08). Source: `casesextra` Case 2.

### FAULT_EGR_STUCK_OPEN {#FAULT_EGR_STUCK_OPEN}
- **chemical_state:** `EGR_STUCK_OPEN` · **dna_gate:** `emissions.egr_equipped = true` · **match_class:** SPECIFIC · diagnosed **at idle**, not under load

| State | HC | CO | CO₂ | NOₓ |
|---|---|---|---|---|
| Idle | ↑ (rough) | ↑ | ↓ | low |
| Under load | normalises | normal | normal | low |

- **discriminator:** EGR opens at idle → inert exhaust crowds out intake air → HC rises, idle rough. Same flow under load is masked by available air.

### FAULT_VVT_FAILURE {#FAULT_VVT_FAILURE}
- **chemical_state:** `VVT_FAILURE` · **dna_gate:** none · **match_class:** CATCH_ALL

| VVT mode | Effect on gases |
|---|---|
| Failure to retard at idle | Excessive overlap, intake air short-circuits to exhaust → HC up, idle rough |
| Failure to advance under load | NOₓ up (loss of internal-EGR effect) |

- **discriminator:** GASLab confirms how the timing error affects combustion. Solenoid faults post P0011–P0014 — DTCLab's job.
- **phaser-lag dual-idle signature** `[v2.2: casesextra]`: a sluggish/mechanically-retarded phaser (worn phaser, low oil pressure, OCV-passage sludge) holds the cam at max retard **at idle** → poor scavenging, partial burn: HC **400 ppm**, CO₂ **12.2 %**, O₂ **1.1 %**, λ **1.04** at idle. At 2500 RPM oil pressure rises, the phaser reaches commanded angle and scavenging normalises: HC **→ 50 ppm (Δ ≈ −350 ppm)**, CO₂ **→ 14.0 %**, O₂ **→ 0.3 %**, λ **→ 1.005**. The **HC reversal on rev-up is the defining signature — a misfire does not clear this way**. DTC context P0011 / P0021. **Consumer:** dual-idle delta routing (→ TEST_RPM_SEPARATION_MATRIX, GASWIKI-08). Source: `casesextra` Case 3.

### FAULT_EVAP_CANISTER_SATURATED {#FAULT_EVAP_CANISTER_SATURATED}
- **chemical_state:** `EVAP_CANISTER_SATURATED` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector:** HC moderate | CO **moderate–high** | CO₂ low | O₂ low
- **discriminator:** saturated canister delivers continuous unmetered vapour; ECU pushes negative trims but cannot fully compensate. Manifests at mid-load (post tip-in), not idle. DTCs P0441–P0458 may or may not be set.
- **purge-valve-stuck-open dual-idle signature** `[v2.2: casesextra]`: at idle the purge solenoid is commanded closed, so gas reads clean; on rev-up the ECU raises purge duty and a stuck-open valve dumps canister vapour uncontrolled. Result is **rich specifically on rev-up**: λ **1.00 → 0.92 (Δλ ≈ −0.08)**, HC **40 → 250 ppm**, CO **0.12 → 2.0 %** from idle to 2500 RPM; DTC context P0441 + P0172. The **idle-clean→2500-rich delta is the differentiator** from → FAULT_VACUUM_REGULATOR_DIAPHRAGM_RUPTURE (rich *at idle*, **improves** on rev as vacuum drops) and from a steady fuelling-rich (flat across RPM). **Consumer:** dual-idle delta routing (→ TEST_RPM_SEPARATION_MATRIX, GASWIKI-08). Source: `casesextra` Case 1.

### FAULT_EGR_DILUTION_MISFIRE — EGR over-dilution causing partial misfire {#FAULT_EGR_DILUTION_MISFIRE}
- **chemical_state:** `EGR_DILUTION_MISFIRE` · **dna_gate:** `requires_dtc: true` (ontology-level gate, not a `dna_gate`; `resolution.py` does not consume `requires_dtc` in v1) · **match_class:** SPECIFIC
- **gas_vector:** HC moderate–high | CO low–moderate | CO₂ low | O₂ moderate–high | NOₓ low | λ variable
- **discriminator:** excess EGR dilutes the charge past the flammability limit → partial misfire. Distinct from → FAULT_EGR_STUCK_OPEN in that combustion is intermittently failing, not merely rough.

### FAULT_INCOMPLETE_OXIDATION — partial combustion, elevated CO + HC {#FAULT_INCOMPLETE_OXIDATION}
- **chemical_state:** `INCOMPLETE_OXIDATION` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector:** HC moderate | CO **moderate–high** | CO₂ low–moderate | O₂ low | NOₓ low | λ variable
- **discriminator:** combustion initiated but oxidation did not complete — CO stays elevated with HC while O₂ is consumed. Distinguished from → FAULT_RICH_MIXTURE by the λ band (may be stoich/lean despite elevated CO). Common in cold-start, worn plugs, borderline coil energy.

### FAULT_INCOMPLETE_COMBUSTION — combustion quenched early {#FAULT_INCOMPLETE_COMBUSTION}
- **chemical_state:** `INCOMPLETE_COMBUSTION` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector:** HC high | CO low | CO₂ very low | O₂ high | NOₓ very low | λ variable
- **discriminator:** flame kernel formed but quenched before consuming the charge — high HC + O₂ with collapsed CO₂. Distinguished from → FAULT_IGNITION_MISFIRE by lower HC magnitude and the presence of some CO (combustion started but stopped).

### FAULT_COOLANT_LEAK_INTERNAL — coolant (± oil) ingress into combustion chamber {#FAULT_COOLANT_LEAK_INTERNAL}
- **chemical_state:** `COOLANT_LEAK_INTERNAL` · **dna_gate:** none · **match_class:** DEFINITIVE (coolant-intrusion override)
- **gas_vector:** HC moderate (200–400) | CO low–moderate (elevated) | CO₂ **low (< 11.5 %)** | O₂ **high (> 2 %, false lean)** | NOₓ **very low (< 30 ppm, quenched)** | λ **> 1.05 (false lean)**
- **discriminator:** coolant entering the chamber quenches the flame, suppresses NOₓ, displaces CO₂ with steam, and produces white sweet-smelling exhaust. May present as `SAMPLE_INVALID` if water condenses in the sample line. **Signature persists at 2500 RPM** and crucially **NOₓ fails to rise** with revs (a healthy engine spikes NOₓ at 2500 RPM) — the endothermic vaporisation of entering water keeps temps below the thermal-NOₓ threshold. Confirm with cooling-system pressure test + combustion leak detector.
- **head-gasket oil-to-cylinder breach sub-mode** `[v2: q4]`: a head-gasket failure between a pressurised **oil** passage and the bore (often alongside a coolant passage) presents with the same false-lean + suppressed-NOₓ fingerprint (HC 340, CO 0.65, O₂ 2.6, NOₓ 18, λ 1.085 at idle; HC 440, O₂ 2.1, NOₓ 38, λ 1.055 at 2500). It routes to `COOLANT_LEAK_INTERNAL` for v2 emit; candidate value `HEAD_GASKET_OIL_BREACH` is recorded in → CONCEPT_PROPOSED_ENUM_ADDITIONS (GASWIKI-11). Tell-tale beyond gases: milky oil/coolant emulsion on the dipstick.

---

## 6B.1 Consolidated 34-entry enum lookup {#CONCEPT_ENUM_SUMMARY_TABLE}

The v2.1 contract surface. `chemical_state` ← one of these 34. (Candidate v2.x oil-burn additions are listed separately in GASWIKI-11 and are **not** part of this count.) The v2.1 timing-taxonomy revision retired `WRONG_VALVE_TIMING` for the three `CAM_TIMING_*` values; the canonical `OBD_VOCABULARY.md §17` mirror update is a coordinated cross-lab follow-up (→ GAS_VOCABULARY §21).

| Enum value | Primary signal | Cross-check | DNA gate |
|---|---|---|---|
| `NORMAL_OPERATION` | all gases in window | λ 0.99–1.01 | any |
| `RICH_MIXTURE` | CO > 1.5 %, O₂ low, λ < 0.95 | triangle valid | any |
| `LEAN_MIXTURE` | O₂ > 2.5 %, CO < 0.1 %, λ > 1.05 | HC low | any |
| `IGNITION_MISFIRE` | HC > 1000, O₂ > 3 %, NOₓ < 50 | masking rule | any |
| `LEAN_MISFIRE` | HC 200–600, O₂ > 4 %, λ > 1.15 | NOₓ variable | any |
| `RICH_MISFIRE` | CO > 1 % AND O₂ > 2 % AND triangle valid | collision | any |
| `EXHAUST_AIR_LEAK` | triangle sum > 16 OR < 14 | HC normal; STFT/probe test | any |
| `HIGH_COMBUSTION_TEMP` | NOₓ > 1000 under load | other gases normal | any |
| `CATALYST_NOT_LIGHTING_OFF` | HC 75–125 + CO 0.5–0.9 at stoich λ | dual-idle delta | has_catalyst |
| `CATALYST_OVERWHELMED` | all four gases off + NOₓ > 500 | multi-fault | has_catalyst |
| `SAMPLE_INVALID` | triangle ∉ [14, 18] | always halts | any |
| `TIMING_OVER_ADVANCED` | NOₓ very high at 2500, others normal | pinging audible | any |
| `TIMING_RETARDED` | NOₓ very low, HC high, λ false-lean | cat / exhaust hot | any |
| `O2_SENSOR_BIASED_LOW` | chem rich + ECU perceives lean | OBD trims +ve; Δλ 0.15–0.23 | any |
| `O2_SENSOR_BIASED_HIGH` | chem lean + ECU perceives rich | OBD trims −ve | any |
| `WORN_ENGINE` | HC moderate, CO slight, λ ~1, flat across RPM | absence of POA | any |
| `FLAT_CAMSHAFT` | CO + CO₂ slightly depressed, λ ~1 | cyl-contribution | any |
| `GDI_INTAKE_VALVE_CARBON` | HC + O₂ at idle, clears at 2500 | RPM-differential | GDI |
| `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` | CO > 3 %, λ < 0.85, trims pegged | unmetered fuel | any |
| `GDI_HPFP_INTERNAL_SEAL_LEAK` | CO > 3 %, λ < 0.85, oil contamination | crankcase evidence | GDI |
| `WORN_VALVE_SEALS` | HC high + rich offset at idle, drops at 2500 | RPM-differential | any |
| `WORN_PISTON_RINGS` | HC + CO high at 2500, trims ≤ −12 % | RPM-differential | any |
| `POA_SIGNATURE` | composite oil-burning syndrome (incl. PCV, turbo-seal sub-modes) | secondary signatures | any |
| `CAM_TIMING_RETARDED_MAP` | retarded cam, rich: CO 3.5–7 %, O₂ ≈ 0, λ 0.75–0.88 | partial normalise at 2500; trims −27…−45 % | any |
| `CAM_TIMING_RETARDED_MAF` | retarded cam, lean: O₂ 2–4.5 %, HC 300–900, λ 1.08–1.18 | persists across RPM; trims +22…+42 % | any |
| `CAM_TIMING_ADVANCED` | advanced cam, mild-lean idle (λ 1.03–1.08), NOₓ rises at 2500 | both load systems; rough-idle internal EGR | any |
| `EGR_STUCK_CLOSED` | NOₓ > 1000 under load | DTC confirms | egr_equipped |
| `EGR_STUCK_OPEN` | rough idle, HC up at idle, normalises with load | DTC confirms | egr_equipped |
| `VVT_FAILURE` | HC up at idle OR NOₓ up under load | P001x DTCs | any |
| `EVAP_CANISTER_SATURATED` | CO mid-load, idle normal | DTC P044x | any |
| `EGR_DILUTION_MISFIRE` | HC + O₂ moderate-high, CO₂ low, NOₓ low | DTC confirms EGR | requires_dtc |
| `INCOMPLETE_OXIDATION` | CO + HC moderate-high, O₂ low | λ may be stoich despite CO | any |
| `INCOMPLETE_COMBUSTION` | HC high, O₂ high, CO₂ collapsed | partial-burn pattern | any |
| `COOLANT_LEAK_INTERNAL` | CO₂ displaced, NOₓ suppressed, false lean, white smoke | cooling-system pressure test | any |

## Graph relations (explicit)

**FAULT_CAM_TIMING_RETARDED_MAP** INDICATES **CAM_TIMING_RETARDED_MAP** — rich branch (Speed-Density): CO 3.5–7.0 %, O₂ ≈ 0, λ 0.75–0.88, partial normalise at 2500 RPM
**FAULT_CAM_TIMING_RETARDED_MAP** DISAMBIGUATED_BY **RPM-normalisation** — distinct from FAULT_RICH_MIXTURE (no RPM cleanup)
**FAULT_CAM_TIMING_RETARDED_MAF** INDICATES **CAM_TIMING_RETARDED_MAF** — lean/mixed branch (MAF): HC 300–900, O₂ 2.0–4.5 %, λ 1.08–1.18, persists at 2500 RPM
**FAULT_CAM_TIMING_RETARDED_MAF** DISAMBIGUATED_BY **TEST_RPM_SEPARATION_MATRIX** and OBD trims +22…+42 %
**FAULT_CAM_TIMING_ADVANCED** INDICATES **CAM_TIMING_ADVANCED** — mild-lean idle (λ 1.03–1.08), NOₓ rises at 2500 RPM, rough idle internal EGR
**FAULT_CAM_TIMING_ADVANCED** DISAMBIGUATED_BY **no NOₓ spike at idle** — distinct from FAULT_TIMING_OVER_ADVANCED (ignition)
**FAULT_EGR_STUCK_CLOSED** INDICATES **EGR_STUCK_CLOSED** — NOₓ > 1000 under load, idle normal
**FAULT_EGR_STUCK_CLOSED** GATED_BY **egr_equipped = true**
**FAULT_EGR_STUCK_CLOSED** VERIFIED_BY **EGR DTC** and **TEST_RPM_SEPARATION_MATRIX**
**FAULT_EGR_STUCK_OPEN** INDICATES **EGR_STUCK_OPEN** — rough idle, HC up at idle, normalises with load
**FAULT_EGR_STUCK_OPEN** GATED_BY **egr_equipped = true**
**FAULT_VVT_FAILURE** INDICATES **VVT_FAILURE** — HC up at idle OR NOₓ up under load, P001x DTCs
**FAULT_VVT_FAILURE** DISAMBIGUATED_BY **TEST_RPM_SEPARATION_MATRIX** and phaser-lag persistence
**FAULT_EVAP_CANISTER_SATURATED** INDICATES **EVAP_CANISTER_SATURATED** — CO mid-load, idle normal, P044x DTCs
**FAULT_EVAP_CANISTER_SATURATED** DISAMBIGUATED_BY **TEST_RPM_SEPARATION_MATRIX** — distinct from FAULT_VACUUM_REGULATOR_DIAPHRAGM_RUPTURE
**FAULT_EGR_DILUTION_MISFIRE** INDICATES **EGR_DILUTION_MISFIRE** — HC + O₂ moderate-high, CO₂ low, NOₓ low
**FAULT_EGR_DILUTION_MISFIRE** VERIFIED_BY **EGR DTC** — requires_dtc gate
**FAULT_INCOMPLETE_OXIDATION** INDICATES **INCOMPLETE_OXIDATION** — CO + HC moderate-high, O₂ low, λ may be stoich despite CO
**FAULT_INCOMPLETE_COMBUSTION** INDICATES **INCOMPLETE_COMBUSTION** — HC high, O₂ high, CO₂ collapsed
**FAULT_INCOMPLETE_COMBUSTION** DISAMBIGUATED_BY **distinct from FAULT_IGNITION_MISFIRE** (partial-burn vs no-burn pattern)
**FAULT_COOLANT_LEAK_INTERNAL** INDICATES **COOLANT_LEAK_INTERNAL** — CO₂ displaced, NOₓ suppressed, false lean, white smoke
**FAULT_COOLANT_LEAK_INTERNAL** DISAMBIGUATED_BY **NOₓ fails to rise at 2500 RPM** — endothermic water vapourisation
**FAULT_COOLANT_LEAK_INTERNAL** ROUTES_TO **CONCEPT_PROPOSED_ENUM_ADDITIONS** (GASWIKI-11) for HEAD_GASKET_OIL_BREACH sub-mode
**WRONG_VALVE_TIMING** RETIRED_BY **CAM_TIMING_RETARDED_MAP**, **CAM_TIMING_RETARDED_MAF**, **CAM_TIMING_ADVANCED** (v2.1)
**CONCEPT_ENUM_SUMMARY_TABLE** ENUMERATES **34 ChemicalSignature values** — v2.1 contract surface
**CONCEPT_ENUM_SUMMARY_TABLE** CONSUMED_BY **gaslab.contracts.ChemicalSignature** (StrEnum)
**RULE_WVT** MAPS_TO **CAM_TIMING_RETARDED_MAP**, **CAM_TIMING_RETARDED_MAF**, **CAM_TIMING_ADVANCED** via three-branch discriminator
**gas_lab_ontology.yaml** WVT rule CONSUMED_BY **gaslab.resolution** differentiator

## Core Entities

- **FAULT_CAM_TIMING_RETARDED_MAP** — `CAM_TIMING_RETARDED_MAP`, SPECIFIC. Rich branch (Speed-Density): CO 3.5–7.0 %, λ 0.75–0.88, partial normalise at 2500 RPM, trims −27…−45 %. Consumer: `rule_engine._definitive_match` (priority 82, RULE_WVT).
- **FAULT_CAM_TIMING_RETARDED_MAF** — `CAM_TIMING_RETARDED_MAF`, SPECIFIC. Lean/mixed branch (MAF): HC 300–900, O₂ 2.0–4.5 %, λ 1.08–1.18, persists at 2500 RPM. Consumer: `rule_engine._definitive_match` (priority 82, RULE_WVT).
- **FAULT_CAM_TIMING_ADVANCED** — `CAM_TIMING_ADVANCED`, SPECIFIC. Mild-lean idle (λ 1.03–1.08), NOₓ rises at 2500 RPM, rough-idle internal EGR. Consumer: `rule_engine._definitive_match` (priority 82, RULE_WVT).
- **FAULT_EGR_STUCK_CLOSED** — `EGR_STUCK_CLOSED`, SPECIFIC. NOₓ > 1000 under load. Gated by `egr_equipped`. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_EGR_STUCK_OPEN** — `EGR_STUCK_OPEN`, SPECIFIC. Rough idle, HC up at idle, normalises with load. Gated by `egr_equipped`. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_VVT_FAILURE** — `VVT_FAILURE`, SPECIFIC. HC up at idle OR NOₓ up under load, P001x DTCs. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_EVAP_CANISTER_SATURATED** — `EVAP_CANISTER_SATURATED`, SPECIFIC. CO mid-load, idle normal. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_EGR_DILUTION_MISFIRE** — `EGR_DILUTION_MISFIRE`, SPECIFIC. Requires DTC gate. Consumer: `rule_engine._matching_fault_candidates` (requires_dtc).
- **FAULT_INCOMPLETE_OXIDATION** — `INCOMPLETE_OXIDATION`, SPECIFIC. CO + HC moderate-high, O₂ low, λ may be stoich despite CO. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_INCOMPLETE_COMBUSTION** — `INCOMPLETE_COMBUSTION`, SPECIFIC. HC high, O₂ high, CO₂ collapsed. Distinct from IGNITION_MISFIRE (partial-burn vs no-burn). Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_COOLANT_LEAK_INTERNAL** — `COOLANT_LEAK_INTERNAL`, SPECIFIC. CO₂ displaced, NOₓ suppressed, false lean, white smoke. Consumer: `rule_engine._matching_fault_candidates`.
- **CONCEPT_ENUM_SUMMARY_TABLE** — 34-value `ChemicalSignature` contract surface (v2.1). Consumer: `gaslab.contracts.ChemicalSignature`.
