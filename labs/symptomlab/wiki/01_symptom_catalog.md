---
chunk_id: SYMWIKI-01
title: "The Two-Tier Symptom Catalog (21 Pairs)"
lab: symptomlab
node_type: wiki
module: symptomlab
subsystem: symptom-catalog
implements:
  - "labs/symptomlab/symptomlab/data/allowed_combinations.yaml"
  - "labs/symptomlab/symptomlab/validator.py"
consumers:
  - "symptomlab: labs/symptomlab/symptomlab/validator.py SymptomValidator.validate (21-pair catalog enforcement)"
  - "dnalab: labs/dnalab/dnalab/assembly.py resolve() (catalog-validated triage selection)"
drift_guards:
  - "labs/symptomlab/tests/unit/test_validator.py"
  - "labs/symptomlab/tests/unit/test_drift_guard.py"
tags: [symptomlab, wiki, symptom-catalog]
source: "labs/symptomlab/wiki/01_symptom_catalog.md"
doc: SYMPTOM_WIKI
version: v2.0
date: 2026-06-12
kg_ingestion: extract
disposition: live
summary: "The canonical (tier_1, tier_2) driveability symptom catalog: 7 primary categories x 3 sub-filters = 21 allowed pairs. Prose mirror of allowed_combinations.yaml. Carries vocabulary only; the quantitative routing weights live in COMLab proposal COMLab-A."
related_chunks: [SYMWIKI-00, SYMWIKI-02, SYMWIKI-03, SYMWIKI-04]
mirrors_code:
  - "symptomlab/data/allowed_combinations.yaml"
  - "symptomlab/symptomlab/validator.py:SymptomValidator"
consumer: "symptomlab/symptomlab/validator.py:SymptomValidator.validate"
sources:
  - "labs/symptomlab/symptomlab/data/allowed_combinations.yaml"
  - "labs/dnalab/research/DNAresearch.md#Revised Driveability Symptom Catalog"
---

# 1. The Two-Tier Symptom Catalog

> **Chunk summary.** This note is the human-readable mirror of the symptom catalog
> SymptomLab actually enforces in code. It defines the **vocabulary** — the seven
> Tier-1 primary symptoms and their three Tier-2 sub-filters each — and names the
> candidate fault family each pair points at. It carries **no numbers**: the
> measured/estimated weightings, frequencies, and chemistry footprints that rank
> these families live in the COMLab proposals registry (see §1.4), never here.

## 1.1 What this catalog is {#CONCEPT_CATALOG}

A driver cannot report a fault family; they can only report a *sensation*. The
catalog turns that sensation into a constrained, machine-checkable selection:

- **Tier 1 — primary symptom.** A distinct physical sensation a non-expert driver
  can perceive (e.g. "rough idle and shudder").
- **Tier 2 — sub-filter.** The specific operational character of that sensation
  (e.g. "surging / hunting idle" vs "stalls on cold start").

Exactly one (tier_1, tier_2) pair is chosen per report. The catalog admits **21
pairs** — 7 Tier-1 categories, each with 3 Tier-2 sub-filters. This is the
structural invariant the validator enforces at construction (`len == 21`); any
pair outside the table is rejected.

```
 driver sensation ──► [ Tier 1 : primary symptom ]
                          └──► [ Tier 2 : sub-filter ]  ──► one allowed pair
                                   │
                                   ▼
                         SymptomValidator.validate()  (rejects non-catalog pairs)
```

# source: labs/symptomlab/symptomlab/data/allowed_combinations.yaml
# source: labs/symptomlab/symptomlab/validator.py (SymptomValidator, len == 21 invariant)

## 1.2 The 21 allowed pairs {#CONCEPT_CATALOG_PAIRS}

The candidate-fault-family column and one-line rationale below are navigational
context for the reader. They describe *which* family a pair points at, not *how
strongly* — the strength weighting is COMLab-owned (§1.4).

### Tier 1 — `vehicle_starting_issues`

| Tier 2 sub-filter | Candidate fault family | One-line rationale |
|---|---|---|
| `no_crank_silent` | Ignition Primary / Battery / Starter Circuit | Complete electrical silence points to a high-current circuit failure or battery depletion. |
| `fast_crank_whining` | Valve-Timing / Mechanical Compression | Rapid, resistance-free cranking indicates total compression loss (broken timing belt/chain). |
| `prolonged_crank_hard_start` | Fuel-Delivery / Coolant-Temp-Sensor | Injector or check-valve leakdown depressurises the rail, so the engine needs long cranking to prime. |

### Tier 1 — `rough_idle_shudder`

| Tier 2 sub-filter | Candidate fault family | One-line rationale |
|---|---|---|
| `constant_vibration_shudder` | Ignition-Coil / Spark Plug (Misfire) | Persistent shaking at idle is a single-cylinder combustion drop. |
| `surging_hunting_idle` | Vacuum Leak / Idle-Control | Rhythmic RPM oscillation reflects the ECM fighting unmetered air. |
| `stalls_on_cold_start` | Coolant-Temp-Sensor / Vacuum Leak | Immediate post-start stall = thermal manifold-shrink leak or wrong cold-start enrichment. |

### Tier 1 — `lack_of_power_hesitation`

| Tier 2 sub-filter | Candidate fault family | One-line rationale |
|---|---|---|
| `flat_sluggish_always` | Catalyst / Air-Fuel Metering (MAF) | Persistent sluggishness points to exhaust restriction or an air-mass calculation bias. |
| `hesitation_throttle_tip_in` | Throttle Sensor / Transient Fueling | Tip-in delay points to transient fuelling lag or a worn throttle-position potentiometer. |
| `sudden_jerk_stumble` | Ignition-Coil (Dielectric Breakdown) | Stumble under load = spark escaping weak coil insulation at high cylinder pressure. |

### Tier 1 — `poor_economy_fuel_odor_sound`

| Tier 2 sub-filter | Candidate fault family | One-line rationale |
|---|---|---|
| `just_poor_mpg` | Oxygen-Sensor / Coolant-Temp-Sensor | An MPG drop alone reflects sensor-induced rich adaptation keeping the ECU in open loop. |
| `strong_fuel_smell` | Fuel-Delivery (Leaking Injector) | Raw gasoline odour indicates a rail leak or an injector stuck open and drooling fuel. |
| `knock_pinging_under_load` | EGR-System / Lean-Misfire | Metallic pinging under load reflects high combustion temperature from failed exhaust dilution. |

### Tier 1 — `engine_dies_or_stalls`

| Tier 2 sub-filter | Candidate fault family | One-line rationale |
|---|---|---|
| `when_coasting_to_stop` | Idle-Control (Carbon Restriction) | Stalling on throttle release indicates carbon-clogged idle-bypass ports. |
| `intermittent_random_cutout` | Crank/Cam Position Sensors | Instant cutout without stumbling is a complete loss of crank-speed synchronisation. |
| `backfire_loud_pop` | Ignition-Coil / Valve-Timing | Mistimed spark or misaligned valves ignite unburned fuel in the manifold. |

### Tier 1 — `visible_exhaust_smoke`

| Tier 2 sub-filter | Candidate fault family | One-line rationale |
|---|---|---|
| `black_smoke` | Fuel-Delivery (Extreme Rich Mixture) | Dark carbon soot is the byproduct of raw, unburned gasoline in rich combustion. |
| `blue_oily_smell` | Engine Mechanical (Valve Stem Seals) | Oil migrating past worn guides/rings burns bluish-grey in the cylinders. |
| `white_sweet_smell` | Engine Mechanical (Head Gasket) | Billowing white steam indicates coolant leaking into the combustion chamber. |

### Tier 1 — `oil_consumption`

`oil_consumption` is the seventh Tier-1 category, added by the live oil-consumption
build (see SYMWIKI-04 changelog). Its routing into named fault families is
registered as proposal-only in COMLab-A / COMLab-OIL-KG.

| Tier 2 sub-filter | Candidate fault family | One-line rationale |
|---|---|---|
| `blue_smoke_on_cold_start_clears` | Engine Mechanical (Valve Stem Seals) | A cold-start cloud that clears on driving indicates oil past degraded valve-stem seals. |
| `blue_smoke_under_acceleration` | Engine Mechanical (Piston Rings) | Smoke worsening under load indicates oil past worn rings or a turbine seal. |
| `oil_loss_no_visible_smoke` | Engine Mechanical (PCV/Crankcase) | Oil loss without visible smoke is typical of a stuck-open PCV drawing oil at low load. |

# source: https://www.sae.org/standards/j1635_200210-sae-cold-start-driveability-procedure
# source: https://www.sae.org/standards/j1635_199808-sae-cold-start-driveability-procedure
# source: https://static.nhtsa.gov/odi/inv/2010/INRD-PE10019-48742.pdf
# source: https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=9101EUTV.TXT
# source: https://www.dinmedia.de/en/standard/sae-j-2944/365090629

## 1.3 Why the catalog is shaped this way {#CONCEPT_CATALOG_DESIGN}

The two-tier shape is deliberate: it keeps the *symptom* axis orthogonal to the
*environmental context* axes (SYMWIKI-02). The legacy catalog folded temperature
states (e.g. `cold_engine_only`, `hot_engine_only`) into Tier 2, which collided
with the independent `occurs_during` axis and blurred the symptom-to-family signal.
The revised catalog removes those temperature sub-filters and replaces them with
distinct, SAE-defined complaints (surging idle, prolonged crank, tip-in
hesitation, backfire). The full move-by-move history is SYMWIKI-04.

# source: labs/dnalab/research/DNAresearch.md#Optimizing the Symptom Questionnaire Taxonomy

## 1.4 Where the numbers live (deliberately not here) {#CONCEPT_CATALOG_SPLIT}

This note owns the **vocabulary** SymptomLab's validator enforces. It does **not**
own — and must never carry — the quantitative material that ranks the candidate
families above:

- the per-Tier-1 weighting bands (how strongly each family is favoured) →
  COMLab proposal **COMLab-F**;
- the exhaust-chemistry footprints per fault family →
  COMLab proposal **COMLab-G**;
- the (tier_1, tier_2) → fault-family routing weights →
  COMLab proposal **COMLab-A**;
- the context-modifier promotions/demotions and the report-trust cap →
  COMLab proposal **COMLab-B**.

(The exact COMLab consumer symbol and code path for each proposal is recorded in
the registry entry itself, `entries.yaml`, not duplicated here.)

```
 SymptomLab (this wiki)            COMLab proposals registry
 ──────────────────────           ──────────────────────────────
 catalog vocabulary  ──key──►  COMLab-A  routing weights
 (21 pairs, families)          COMLab-B  context modifiers + report-trust cap
                               COMLab-F  per-tier weighting bands
                               COMLab-G  exhaust-chemistry footprints
```

The boundary is the signal/noise rule: a numeric weighting in this note would have
no SymptomLab consumer (the validator reads only the pairs and axis enums), so it
would be noise. SymptomLab supplies the vocabulary those numbers key off; it never
carries the numbers.

# source: labs/comlab/comlab/config/proposals/entries.yaml (COMLab-A, COMLab-B, COMLab-F, COMLab-G)


## Graph relations (explicit)

**vehicle_starting_issues** ENUMERATES **no_crank_silent**, **fast_crank_whining**, **prolonged_crank_hard_start**
**rough_idle_shudder** ENUMERATES **constant_vibration_shudder**, **surging_hunting_idle**, **stalls_on_cold_start**
**lack_of_power_hesitation** ENUMERATES **flat_sluggish_always**, **hesitation_throttle_tip_in**, **sudden_jerk_stumble**
**poor_economy_fuel_odor_sound** ENUMERATES **just_poor_mpg**, **strong_fuel_smell**, **knock_pinging_under_load**
**engine_dies_or_stalls** ENUMERATES **when_coasting_to_stop**, **intermittent_random_cutout**, **backfire_loud_pop**
**visible_exhaust_smoke** ENUMERATES **black_smoke**, **blue_oily_smell**, **white_sweet_smell**
**oil_consumption** ENUMERATES **blue_smoke_on_cold_start_clears**, **blue_smoke_under_acceleration**, **oil_loss_no_visible_smoke**
**no_crank_silent** MAPS_TO **Ignition Primary / Battery / Starter Circuit**
**fast_crank_whining** MAPS_TO **Valve-Timing / Mechanical Compression**
**prolonged_crank_hard_start** MAPS_TO **Fuel-Delivery / Coolant-Temp-Sensor**
**constant_vibration_shudder** MAPS_TO **Ignition-Coil / Spark Plug (Misfire)**
**surging_hunting_idle** MAPS_TO **Vacuum Leak / Idle-Control**
**stalls_on_cold_start** MAPS_TO **Coolant-Temp-Sensor / Vacuum Leak**
**flat_sluggish_always** MAPS_TO **Catalyst / Air-Fuel Metering (MAF)**
**hesitation_throttle_tip_in** MAPS_TO **Throttle Sensor / Transient Fueling**
**sudden_jerk_stumble** MAPS_TO **Ignition-Coil (Dielectric Breakdown)**
**just_poor_mpg** MAPS_TO **Oxygen-Sensor / Coolant-Temp-Sensor**
**strong_fuel_smell** MAPS_TO **Fuel-Delivery (Leaking Injector)**
**knock_pinging_under_load** MAPS_TO **EGR-System / Lean-Misfire**
**when_coasting_to_stop** MAPS_TO **Idle-Control (Carbon Restriction)**
**intermittent_random_cutout** MAPS_TO **Crank/Cam Position Sensors**
**backfire_loud_pop** MAPS_TO **Ignition-Coil / Valve-Timing**
**black_smoke** MAPS_TO **Fuel-Delivery (Extreme Rich Mixture)**
**blue_oily_smell** MAPS_TO **Engine Mechanical (Valve Stem Seals)**
**white_sweet_smell** MAPS_TO **Engine Mechanical (Head Gasket)**
**blue_smoke_on_cold_start_clears** MAPS_TO **Engine Mechanical (Valve Stem Seals)**
**blue_smoke_under_acceleration** MAPS_TO **Engine Mechanical (Piston Rings)**
**oil_loss_no_visible_smoke** MAPS_TO **Engine Mechanical (PCV/Crankcase)**
**allowed_combinations.yaml** MIRRORS_CONTRACT_IN **SymptomValidator.validate**
**symptom_catalog** CONSUMED_BY **SymptomValidator.validate**
**COMLab-A** ROUTES_TO **symptom_catalog** (via allowed_combinations.yaml keys)
**COMLab-F** DESCRIBES **tier_1_weighting_bands**
**COMLab-G** DESCRIBES **exhaust_chemistry_footprints**
**cold_engine_only** IS_NOT a **Tier-2 sub-filter** (DROPPED — redundant with OccursDuring)
**hot_engine_only** IS_NOT a **Tier-2 sub-filter** (DROPPED — redundant with OccursDuring)
**only_high_rpm_highway** IS_NOT a **Tier-2 sub-filter** (DROPPED — captured by LoadState)
**right_after_fillup** IS_NOT a **Tier-2 sub-filter** (DROPPED — EVAP overlap)
**only_when_hot** IS_NOT a **Tier-2 sub-filter** (DROPPED — redundant with OccursDuring)


## Core Entities

- **vehicle_starting_issues** (Tier-1, live) — CONSUMED_BY **SymptomValidator.validate** (symptomlab/symptomlab/validator.py)
- **rough_idle_shudder** (Tier-1, live) — CONSUMED_BY **SymptomValidator.validate** (symptomlab/symptomlab/validator.py)
- **lack_of_power_hesitation** (Tier-1, live) — CONSUMED_BY **SymptomValidator.validate** (symptomlab/symptomlab/validator.py)
- **poor_economy_fuel_odor_sound** (Tier-1, live) — CONSUMED_BY **SymptomValidator.validate** (symptomlab/symptomlab/validator.py)
- **engine_dies_or_stalls** (Tier-1, live) — CONSUMED_BY **SymptomValidator.validate** (symptomlab/symptomlab/validator.py)
- **visible_exhaust_smoke** (Tier-1, live) — CONSUMED_BY **SymptomValidator.validate** (symptomlab/symptomlab/validator.py)
- **oil_consumption** (Tier-1, live) — CONSUMED_BY **SymptomValidator.validate** (symptomlab/symptomlab/validator.py)
- **SymptomValidator.validate** (live) — CONSUMED_BY **DNALab resolve entrypoint**
- **allowed_combinations.yaml** (live) — CONSUMED_BY **SymptomValidator.__init__**
- **COMLab-A** (proposal) — CONSUMED_BY **FaultAtlasRouter** (catalog routing weights)
- **COMLab-F** (proposal) — CONSUMED_BY **FaultAtlasRouter** (per-tier weighting bands)
- **COMLab-G** (proposal) — CONSUMED_BY **FaultAtlasRouter** (exhaust-chemistry footprints)
