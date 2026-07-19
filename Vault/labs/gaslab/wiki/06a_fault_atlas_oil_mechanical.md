---
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "mechanical-wear-atlas"
implements:
  - "labs/gaslab/code/rule_engine.py"
  - "labs/gaslab/code/resolution.py"
  - "labs/gaslab/code/family_map.py"
  - "labs/gaslab/code/data/gas_lab_ontology.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py gas_co/gas_hc/gas_o2"
drift_guards:
  - "labs/gaslab/tests/unit/test_rule_engine.py"
  - "labs/gaslab/tests/unit/test_resolution.py"
  - "labs/gaslab/tests/unit/test_family_map.py"
tags: [gaslab, finished, wiki]
source: "labs/gaslab/wiki/06a_fault_atlas_oil_mechanical.md"
---

# 6A. Fault Atlas — Oil Burning & Mechanical Wear

> **Chunk summary.** The mechanical-wear and oil-ingestion entities, plus the single RPM-differential discriminator that resolves the `POA_SIGNATURE` catch-all to a specific leaf. v2 maps five field-documented oil-burn cases onto existing enum values and records candidate new values in → CONCEPT_PROPOSED_ENUM_ADDITIONS (GASWIKI-11).

---

### FAULT_FLAT_CAMSHAFT — lost cam lobe, reduced cylinder fill {#FAULT_FLAT_CAMSHAFT}
- **chemical_state:** `FLAT_CAMSHAFT` · **dna_gate:** none · **match_class:** SPECIFIC
- **gas_vector:** HC no change/slight decrease | CO **slight decrease** | CO₂ slight decrease | O₂ no change/slight decrease | NOₓ no change/slight decrease | λ ≈ 1.0
- **discriminator:** flattened lobe restricts charge entry; reduced charge still burns cleanly → subtle across-the-board gas depression with well-behaved λ. Confirm by camshaft inspection.

### FAULT_GDI_INTAKE_VALVE_CARBON — carbon on intake valves (GDI only) {#FAULT_GDI_INTAKE_VALVE_CARBON}
- **chemical_state:** `GDI_INTAKE_VALVE_CARBON` · **dna_gate:** `fuel_delivery_type = GDI` · **match_class:** SPECIFIC
- **gas_vector:** HC **> 100 ppm at idle** | CO low–moderate | CO₂ low–moderate | O₂ **high** | NOₓ variable | λ **> 1.0 at idle → ≈ 1.0 at 2500 RPM**
- **discriminator:** no port-wash on GDI → carbon builds on valve backs; localised lean pockets create a lean-misfire look at idle that **clears substantially at 2500 RPM** as air velocity overcomes the restriction. True lean/vacuum-leak faults do not normalise the same way (→ TEST_RPM_SEPARATION_MATRIX). In-scope for 2000–2010 GDI vehicles only.

### FAULT_VACUUM_REGULATOR_DIAPHRAGM_RUPTURE — unmetered fuel via FPR vacuum line {#FAULT_VACUUM_REGULATOR_DIAPHRAGM_RUPTURE}
- **chemical_state:** `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` · **dna_gate:** none (FPR universal) · **match_class:** SPECIFIC
- **gas_vector:** HC high | CO **> 3.0 %** | CO₂ low | O₂ **very low** | NOₓ very low | λ **< 0.85**
- **discriminator:** ruptured FPR diaphragm lets raw liquid fuel into the manifold via the vacuum hose, bypassing injectors. **OBD differentiator:** STFT ≤ −20 %, LTFT ≤ −23 %, pegged at the floor with the rich condition still present (a stuck-open injector pushes trims negative too, but ECU correction partially reduces the rich reading; FPR's trims sit at the floor with zero effect). **Confirm:** disconnect the FPR vacuum hose engine-running — raw fuel/vapour present is conclusive.

### FAULT_GDI_HPFP_INTERNAL_SEAL_LEAK — unmetered fuel via HPFP shaft seal into crankcase {#FAULT_GDI_HPFP_INTERNAL_SEAL_LEAK}
- **chemical_state:** `GDI_HPFP_INTERNAL_SEAL_LEAK` · **dna_gate:** `fuel_delivery_type = GDI` · **match_class:** SPECIFIC
- **gas_vector:** HC high | CO **> 3.0 %** | CO₂ low | O₂ **very low** | NOₓ very low | λ **< 0.85** (tailpipe identical to FPR rupture)
- **discriminator:** failed HPFP shaft seal admits high-pressure fuel into the oil sump; petrol-contaminated oil is drawn through PCV as unmetered vapour. Differentiator is **crankcase evidence**: dipstick fuel smell / level above max; abnormal positive crankcase-pressure deviation; fuel vapour/droplets at the PCV supply hose. **Severity:** stop-drive — fuel-diluted oil loses viscosity fast. In-scope for 2000–2010 GDI vehicles only.

---

### FAULT_WORN_VALVE_SEALS — idle-vacuum oil ingestion, clears at 2500 RPM {#FAULT_WORN_VALVE_SEALS}
- **chemical_state:** `WORN_VALVE_SEALS` · **dna_gate:** none · **match_class:** SPECIFIC (via → CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR)

| State | HC | CO | CO₂ | O₂ | NOₓ | λ | Fuel trims |
|---|---|---|---|---|---|---|---|
| Idle | **300–500 ppm** | 0.8–1.2 % (rich offset) | 12.5–13.5 % | < 0.5 % | low | **0.95–0.97 (rich)** | ± 8 % (stable) |
| 2500 RPM | **≤ 35 ppm** | ≤ 0.15 % | 14.5–15.5 % (rises) | normal | low | ~ 1.0 | ± 8 % (stable) |
| Δ direction | **↓ sharply** | ↓ | ↑ | unchanged | unchanged | rich→stoich | unchanged |

- **physics:** high idle vacuum draws oil down the valve guides onto the intake-valve backs → elevated HC and a rich offset at idle (heavy oil acts as extra fuel). At 2500 RPM vacuum collapses, the oil siphon stops, residual oil burns off, cat heats → **rapid cleanup**. `[v2: q4]` the rich-offset-at-idle refinement (CO ~0.95 %, λ ~0.96) supersedes the v1 "trims stable, HC 75–250" range, which described a milder presentation; both are the same fault at different severities.

### FAULT_WORN_PISTON_RINGS — blow-by oil vapour via PCV under cylinder load {#FAULT_WORN_PISTON_RINGS}
- **chemical_state:** `WORN_PISTON_RINGS` · **dna_gate:** none · **match_class:** SPECIFIC (via → CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR)

| State | HC | CO | CO₂ | O₂ | NOₓ | λ | Fuel trims |
|---|---|---|---|---|---|---|---|
| Idle | 100–150 ppm | near normal | normal (~14 %) | < 0.5 % | low | ~ 1.0 | ~ 0 % |
| 2500 RPM | **> 300 ppm** | **0.5–1.0 %** | drops (12.5–13.5 %) | < 0.7 % | normal | **< 0.99 (rich)** | **≤ −12 %** |
| Δ direction | **↑ spikes, stays elevated** | ↑ | ↓ | unchanged | unchanged | →rich | **↓ ECU cuts fuel hard** |

- **physics:** under load, peak cylinder pressure forces combustion gas and vaporised oil past worn rings into the crankcase; PCV draws the oil-and-fuel vapour into the intake as unmetered fuel — genuine rich at the tailpipe, with the heavy oil thermally cracking and consuming chamber O₂. Negative trims at load + persistent rich distinguish this from simple over-fuelling. **Worsens with RPM** (opposite of valve seals). `[v2: q4]`

---

### FAULT_POA_SIGNATURE — oil burning (Poisoning + Oil-ash + Abundant HC) {#FAULT_POA_SIGNATURE}
- **chemical_state:** `POA_SIGNATURE` · **dna_gate:** none · **match_class:** CATCH_ALL (ranked last by `_candidate_rank`)

| Sub-mode | Gas pattern |
|---|---|
| Worn valve seals | High HC at idle that cleans up when revved; possible λ mismatch; P0420 |
| Worn piston rings | High HC + CO at high RPM; blue smoke on accel; load-dependent trim direction |
| Clogged / stuck-open PCV | High HC + heavy rich at idle, rough running, clears as vacuum falls |
| Turbo turbine-seal oil leak | Extreme tailpipe HC with **stoichiometric λ** (oil cracks in the exhaust, not the cylinder) |
| Severe oil burning | HC > 500 ppm persists across RPM, λ mismatch + P0420 |
| Catastrophic | HC > 2000 ppm, continuous λ mismatch, dead cat |

- **detection caveat:** workshop analysers cannot see the oil molecule directly — GASLab sees only the secondary signatures.
- **repair caveat:** high CO contaminates the oil with fuel. After fixing a rich condition the oil must be changed, or fuel in the oil is pulled through PCV and perpetuates the fault.

#### New oil-burn sub-modes (v2, mapped to existing enum) {#CONCEPT_OILBURN_SUBMODES}

`[v2: q4]` Five field-documented oil-ingestion modes. Per the v2 enum decision they are **mapped onto existing values now** (no contract break) and recorded as candidate new values in → CONCEPT_PROPOSED_ENUM_ADDITIONS (GASWIKI-11).

| Field case | Idle signature | 2500 RPM signature | Maps to (v2 emit) | Proposed v2.x value |
|---|---|---|---|---|
| Worn piston rings | HC 120, CO 0.15, λ 1.00 | HC 380, CO 0.85, λ 0.985 (worsens) | `WORN_PISTON_RINGS` | — (exists) |
| Degraded valve-stem seals | HC 450, CO 0.95, λ 0.96 | HC 65, λ 1.00 (cleans up) | `WORN_VALVE_SEALS` | — (exists) |
| Stuck-open PCV valve | HC 610, CO 1.90, λ 0.925 (heavy rich) | HC 170, CO 0.45, λ 0.988 | `POA_SIGNATURE` (clogged-PCV sub-mode) | `PCV_STUCK_OPEN` |
| Head-gasket oil-to-cylinder breach | HC 340, CO 0.65, O₂ 2.6, NOₓ 18, λ 1.085 (false lean) | HC 440, O₂ 2.1, NOₓ 38, λ 1.055 | `COOLANT_LEAK_INTERNAL` (oil+coolant breach, → GASWIKI-06B) | `HEAD_GASKET_OIL_BREACH` |
| Worn turbo turbine seals | HC 720, CO 0.07, λ 1.000 (stoich) | HC 130, λ 1.002 | `POA_SIGNATURE` (turbo-seal sub-mode); gate on `induction_type` forced | `TURBO_SEAL_OIL_LEAK` |

**Disambiguating logic** `[v2: q4]`: *high tailpipe HC with perfect stoichiometric λ and near-zero CO* ⇒ oil cracking **outside** the cylinder (turbo turbine seal) — combustion is intact, so it cannot be a mixture or misfire fault. *Heavy rich at closed-throttle idle that clears as manifold vacuum falls* ⇒ stuck-open PCV drawing crankcase oil aerosol. *False-lean O₂ with suppressed NOₓ and white steam* ⇒ coolant/oil head-gasket breach (route to `COOLANT_LEAK_INTERNAL`). Always **inspect/replace the PCV valve before authorising ring or short-block work** — a stuck-open PCV replicates severe ring-failure emissions at idle.

#### 6A.1 RPM-differential discriminator — resolving POA_SIGNATURE to a leaf {#CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR}

`POA_SIGNATURE` is the catch-all an oil-burning sample lands on first. To emit the *specific* wear fault, compare the idle reading against the 2500 RPM reading and match the **HC change direction** plus load-state CO and fuel-trim columns. This is the single discriminator the atlas uses to route a catch-all oil hit to a leaf. **All thresholds are inherited from the cited sources — this table introduces no new numbers, only consolidates them for routing.**

| Route to | HC @ idle | HC @ 2500 | HC Δ | CO @ 2500 | Trims @ 2500 | λ | Source |
|---|---|---|---|---|---|---|---|
| `WORN_VALVE_SEALS` | 300–500 (rich offset) | ≤ 35 | **↓ sharply** | low | ± 8 % | 0.96→1.0 | FAULT_WORN_VALVE_SEALS |
| `WORN_PISTON_RINGS` | 100–150 | > 300 | **↑ stays elevated** | > 0.5 % | ≤ −12 % | →< 0.99 | FAULT_WORN_PISTON_RINGS |
| `WORN_ENGINE` | 150–300 | ~ unchanged | **flat** (no cleanup) | slight increase | ~ 0 % | 1.0–1.03 | FAULT_WORN_ENGINE |
| `POA_SIGNATURE` (turbo-seal) | > 500, CO ≈ 0 | drops | **↓** but λ stays 1.0 | ≈ 0 | ~ 0 % | **1.0 (stoich)** | turbo sub-mode above |
| `POA_SIGNATURE` (severe/catastrophic) | > 500 | > 500 (persists) | **flat, high** | variable | variable | λ mismatch | FAULT_POA_SIGNATURE |
| `COOLANT_LEAK_INTERNAL` | HC 200–400, O₂ > 2, NOₓ < 30 | persists, NOₓ stays < 30 | **flat** | elevated | — | false lean | GASWIKI-06B |

**Routing precedence:** sharp HC drop at 2500 ⇒ `WORN_VALVE_SEALS`; HC rising/elevated with negative trims and CO > 0.5 % under load ⇒ `WORN_PISTON_RINGS`; moderate HC that neither cleans up nor spikes, only generalised drift, no λ mismatch ⇒ `WORN_ENGINE`; extreme HC with stoich λ and ~0 CO ⇒ turbo-seal `POA_SIGNATURE`; HC > 500 persisting both states with λ mismatch ⇒ leave on `POA_SIGNATURE`; false-lean O₂ + suppressed NOₓ ⇒ `COOLANT_LEAK_INTERNAL`. The CO-@-idle and `RICH_MISFIRE` collision cases are disambiguated upstream (→ FAULT_RICH_MISFIRE, → RULE_COLLISION) before this discriminator runs.

> Fuel trim is a perception/DNA-context signal, **not** a 5-gas channel (vocabulary home: `GAS_VOCABULARY §10.8`). The HC change-direction and CO-@-2500 columns are the gas-visible primary discriminators; the trim column corroborates only when DNA context supplies it.

## Graph relations (explicit)

**FAULT_FLAT_CAMSHAFT** INDICATES **FLAT_CAMSHAFT** — HC 150–300, O₂ 1.5–3.0 %, NOₓ near zero, λ false-lean
**FAULT_FLAT_CAMSHAFT** DISAMBIGUATED_BY **persists at both RPMs** — no cleanup
**FAULT_GDI_INTAKE_VALVE_CARBON** INDICATES **GDI_INTAKE_VALVE_CARBON** — HC 250–600, O₂ 0.8–2.0 %, CO low
**FAULT_GDI_INTAKE_VALVE_CARBON** GATED_BY **fuel_delivery_type = GDI**
**FAULT_GDI_INTAKE_VALVE_CARBON** DISAMBIGUATED_BY **TEST_RPM_SEPARATION_MATRIX**
**FAULT_VACUUM_REGULATOR_DIAPHRAGM_RUPTURE** INDICATES **VACUUM_REGULATOR_DIAPHRAGM_RUPTURE** — CO 2.0–5.0 %, λ < 0.90, HC moderate
**FAULT_VACUUM_REGULATOR_DIAPHRAGM_RUPTURE** DISAMBIGUATED_BY **heavy rich at idle** from fuel drawn through vacuum reference line
**FAULT_GDI_HPFP_INTERNAL_SEAL_LEAK** INDICATES **GDI_HPFP_INTERNAL_SEAL_LEAK** — fuel dilution into oil → HC rise
**FAULT_GDI_HPFP_INTERNAL_SEAL_LEAK** GATED_BY **fuel_delivery_type = GDI**
**FAULT_WORN_VALVE_SEALS** INDICATES **WORN_VALVE_SEALS** — HC 300–500 at idle, drops sharply at 2500 RPM
**FAULT_WORN_VALVE_SEALS** SUB_MODE_OF **CONCEPT_OILBURN_SUBMODES** (RPM-cleanup pattern)
**FAULT_WORN_PISTON_RINGS** INDICATES **WORN_PISTON_RINGS** — HC 100–150 at idle, rises > 300 at 2500 RPM, CO > 0.5 %
**FAULT_WORN_PISTON_RINGS** SUB_MODE_OF **CONCEPT_OILBURN_SUBMODES** (RPM-worsening pattern)
**FAULT_POA_SIGNATURE** INDICATES **POA_SIGNATURE** — oil-burn catch-all, HC > 500, λ mismatch
**FAULT_POA_SIGNATURE** SUB_MODE_OF **CONCEPT_OILBURN_SUBMODES** (turbo-seal, PCV, head-gasket routes)
**CONCEPT_OILBURN_SUBMODES** ENUMERATES **worn valve seals**, **worn piston rings**, **stuck-open PCV**, **head-gasket oil breach**, **turbo turbine-seal leak**
**CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR** DISAMBIGUATED_BY **HC change direction at idle→2500 RPM** — ↓ sharply → valve seals, ↑ stays elevated → rings, flat → worn engine, stoich λ + ~0 CO → turbo seal
**CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR** CONSUMED_BY **gaslab.resolution.apply_differentiators**
**PCV_STUCK_OPEN** (proposed) PROPOSED_FOR **POA_SIGNATURE** sub-mode — heavy rich at idle, clears with RPM
**HEAD_GASKET_OIL_BREACH** (proposed) PROPOSED_FOR **COOLANT_LEAK_INTERNAL** oil-breach sub-mode — false-lean O₂ + suppressed NOₓ + white steam
**TURBO_SEAL_OIL_LEAK** (proposed) PROPOSED_FOR **POA_SIGNATURE** sub-mode — high HC + stoich λ + ~0 CO
**FAULT_RICH_MISFIRE** DISAMBIGUATED_BY **RULE_COLLISION** — runs before CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR

## Core Entities

- **FAULT_FLAT_CAMSHAFT** — `FLAT_CAMSHAFT`, SPECIFIC. HC 150–300, O₂ 1.5–3.0 %, λ false-lean, persists at both RPMs. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_GDI_INTAKE_VALVE_CARBON** — `GDI_INTAKE_VALVE_CARBON`, SPECIFIC. HC 250–600, O₂ 0.8–2.0 %. Gated by `fuel_delivery_type = GDI`. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_VACUUM_REGULATOR_DIAPHRAGM_RUPTURE** — `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE`, SPECIFIC. CO 2.0–5.0 %, λ < 0.90. FPR diaphragm failure draws fuel through vacuum line. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_GDI_HPFP_INTERNAL_SEAL_LEAK** — `GDI_HPFP_INTERNAL_SEAL_LEAK`, SPECIFIC. Fuel dilution into oil. Gated by `fuel_delivery_type = GDI`. Consumer: `rule_engine._matching_fault_candidates`.
- **FAULT_WORN_VALVE_SEALS** — `WORN_VALVE_SEALS`, SPECIFIC. HC drops sharply idle→2500. Consumer: `gaslab.resolution.apply_differentiators` + `CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR`.
- **FAULT_WORN_PISTON_RINGS** — `WORN_PISTON_RINGS`, SPECIFIC. HC rises/elevated at 2500, CO > 0.5 %. Consumer: `gaslab.resolution.apply_differentiators` + `CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR`.
- **FAULT_POA_SIGNATURE** — `POA_SIGNATURE`, oil-burn catch-all. HC > 500, λ mismatch. Routes to specific wear fault via RPM-differential discriminator. Consumer: `gaslab.resolution.apply_differentiators`.
- **CONCEPT_OILBURN_SUBMODES** — five oil-burn failure modes: valve seals, rings, PCV, head gasket, turbo seal. Consumer: `FAULT_POA_SIGNATURE` discriminator routing.
- **CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR** — idle vs 2500 RPM HC/CO/λ comparison for oil-burn fault routing. Consumer: `gaslab.resolution.apply_differentiators`.
- **PCV_STUCK_OPEN** (proposed), **HEAD_GASKET_OIL_BREACH** (proposed), **TURBO_SEAL_OIL_LEAK** (proposed) — candidate v2.x enum additions. Consumer: `CONCEPT_PROPOSED_ENUM_ADDITIONS` (GASWIKI-11).
