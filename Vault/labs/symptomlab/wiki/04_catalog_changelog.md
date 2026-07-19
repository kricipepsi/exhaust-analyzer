---
node_type: "wiki"
lab: "symptomlab"
module: "symptomlab"
subsystem: "catalog-provenance"
implements:
  - "labs/symptomlab/symptomlab/data/allowed_combinations.yaml"
consumers:
  - "symptomlab: labs/symptomlab/symptomlab/validator.py SymptomValidator (provenance for the live 21-pair invariant)"
drift_guards:
  - "labs/symptomlab/tests/unit/test_drift_guard.py"
tags: [symptomlab, finished, wiki]
source: "labs/symptomlab/wiki/04_catalog_changelog.md"
---

# 4. Catalog Changelog — Legacy to Revised

> **Chunk summary.** This note records *why* the live catalog (SYMWIKI-01) has the
> shape it does. Each row is an operational decision moving from the legacy catalog
> to the revised one: **KEEP**, **REWORD**, **DROP**, or **ADD**. It is the
> provenance layer — it explains lineage, it does not assign any weighting.

## 4.1 The two design moves {#CONCEPT_CHANGELOG_DESIGN}

Two principles drove every row below:

1. **Remove dimensional overlap.** Legacy Tier-2 sub-filters that encoded
   *temperature* or *time* (e.g. `cold_engine_only`, `only_when_hot`) duplicated
   the independent `occurs_during` axis and introduced multi-collinearity into the
   symptom-to-family weighting. They were dropped from Tier 2 and left to the axis.
2. **Add SAE-defined predictive complaints.** The legacy catalog lacked several
   highly discriminating, professionally-defined driveability complaints. New
   sub-filters (surging idle, stalls-on-cold-start, tip-in hesitation, knock under
   load, backfire) were added to fill those gaps.

```
 legacy catalog ──► [remove temperature/time sub-filters] ──► [add SAE complaints]
                 ──► [add load_state axis] ──► [add oil_consumption Tier-1] ──► live 21-pair catalog
```

# source: labs/dnalab/research/DNAresearch.md#Optimizing the Symptom Questionnaire Taxonomy

## 4.2 Symptom / sub-filter changelog {#CONCEPT_CHANGELOG_TABLE}

| Legacy symptom / sub-filter | Action | Revised nomenclature | Technical reason |
|---|---|---|---|
| `vehicle_wont_start` | KEEP | `vehicle_starting_issues` | Preserves the primary starting complaint as the Tier-1 category. |
| `no_crank_silent` | KEEP | `no_crank_silent` | Cleanly isolates high-current starter/battery open-circuit faults. |
| `fast_crank_whining` | KEEP | `fast_crank_whining` | Maps to mechanical compression loss (broken timing belt/chain). |
| `normal_crank_zero_rpm` | REWORD | `prolonged_crank_hard_start` | Reworded to capture fuel-rail leakdown and cold-sensor hard starts that delay (not prevent) starting. |
| `cold_engine_only` | DROP | — | Redundant with the `occurs_during` axis; removed to avoid multi-collinearity. |
| `hot_engine_only` | DROP | — | Redundant with the `occurs_during` axis; removed to keep variables independent. |
| `constant_shudder` | REWORD | `constant_vibration_shudder` | Captures misfire felt as physical vibration; resolves a naming gap. |
| _(new)_ | ADD | `surging_hunting_idle` | Resolves a driveability gap; maps to vacuum leaks and lazy idle-control. |
| _(new)_ | ADD | `stalls_on_cold_start` | Resolves a starting gap; maps to cold manifold-vacuum leaks and thermal-sensor faults. |
| `flat_sluggish_always` | KEEP | `flat_sluggish_always` | Separates steady-state flow restriction (melted catalyst) from transient fuelling. |
| `only_high_rpm_highway` | DROP | — | Better captured by the new `load_state` axis; simplifies Tier 2. |
| `sudden_jerk_stumble` | KEEP | `sudden_jerk_stumble` | Classic secondary-ignition insulation breakdown under high cylinder load. |
| _(new)_ | ADD | `hesitation_throttle_tip_in` | Fills a gap; isolates transient fuelling lag and throttle-position-sensor faults. |
| `just_poor_mpg` | KEEP | `just_poor_mpg` | Retained as a non-vague indicator of rich-running closed-loop sensor bias. |
| `strong_fuel_smell` | KEEP | `strong_fuel_smell` | Maps to high-severity fuel leaks (regulator rupture, leaking injector). |
| `right_after_fillup` | DROP | — | An environmental trigger, not a physical symptom; overlaps EVAP purge mapping. |
| _(new)_ | ADD | `knock_pinging_under_load` | Addresses a combustion gap; maps to EGR-flow failure or advanced timing under load. |
| `when_coasting_to_stop` | KEEP | `when_coasting_to_stop` | Predictive of carbon-restricted throttle bodies and lazy idle-control. |
| `intermittent_random` | REWORD | `intermittent_random_cutout` | Differentiates loss of crank-speed sync from transient fuelling/vacuum stumbles. |
| `only_when_hot` | DROP | — | Redundant with the `occurs_during` axis; removed to prevent duplication. |
| _(new)_ | ADD | `backfire_loud_pop` | Fills a combustion gap; points to mistimed spark or misaligned valves. |
| `black_smoke` | KEEP | `black_smoke` | Objective indicator of rich fuel-metering or leaking-injector failure. |
| `blue_oily_smell` | KEEP | `blue_oily_smell` | Objective indicator of oil past worn valve-stem guides or rings. |
| `white_sweet_smell` | KEEP | `white_sweet_smell` | Specific indicator of combustion-chamber coolant leakage (head gasket). |

# source: labs/dnalab/research/DNAresearch.md#Symptom Questionnaire Changelog

## 4.3 Axis change {#CONCEPT_CHANGELOG_AXIS}

| Change | Action | Result | Technical reason |
|---|---|---|---|
| Add a third context axis | ADD | `load_state` (`idle`, `steady_cruise`, `transient_acceleration`, `coasting_deceleration`) | Separates static air-metering faults from transient load faults; manifold vacuum behaves inversely to throttle opening (SYMWIKI-02). |

# source: https://www.dinmedia.de/en/standard/sae-j-2944/365090629
# source: https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=9101EUTV.TXT

## 4.4 `oil_consumption` Tier-1 addition {#CONCEPT_CHANGELOG_OIL}

The seventh Tier-1 category was added by the live oil-consumption build, taking the
catalog from six categories (18 pairs) to seven (21 pairs). Its three sub-filters
distinguish oil-entry paths a driver can actually perceive.

| Sub-filter | Action | Technical reason |
|---|---|---|
| `blue_smoke_on_cold_start_clears` | ADD | Cold-start cloud clearing on driving = valve-stem-seal leak. |
| `blue_smoke_under_acceleration` | ADD | Smoke worsening under load = piston rings or turbine seal. |
| `oil_loss_no_visible_smoke` | ADD | Oil loss without visible smoke = stuck-open PCV slow draw. |

Routing of these three into named fault families is registered proposal-only in
COMLab-A and COMLab-OIL-KG; only the catalog vocabulary is live here.

# source: https://www.sae.org/standards/j1635_199808-sae-cold-start-driveability-procedure
# source: https://static.nhtsa.gov/odi/inv/2010/INRD-PE10019-48742.pdf
# source: labs/comlab/comlab/config/proposals/entries.yaml (COMLab-A oil_consumption mappings)

## 4.5 Source-quality note {#CONCEPT_CHANGELOG_SOURCES}

Several legacy citations were retail/DIY blogs. Per the source-quality upgrade,
the engineering reasons above anchor to primary standards where one exists: SAE
J1635 (cold-start driveability), SAE J2944 (driving-performance measures), the EPA
light-duty driveability investigation, and the NHTSA PE10-019 defects
investigation. Retail blogs are retained only where no primary equivalent covers
the specific complaint.

# source: labs/symptomlab/AnswerSymLab.md#Upgrades to High-Quality Reference Sources


## Graph relations (explicit)

**legacy_symptom_catalog** PREDECESSOR_OF **revised_21_pair_catalog**
**vehicle_starting_issues** KEPT as **vehicle_starting_issues**
**no_crank_silent** KEPT as **no_crank_silent**
**fast_crank_whining** KEPT as **fast_crank_whining**
**normal_crank_zero_rpm** REWORDED_TO **prolonged_crank_hard_start**
**cold_engine_only** IS_NOT a **Tier-2 sub-filter** (DROPPED — redundant with OccursDuring)
**hot_engine_only** IS_NOT a **Tier-2 sub-filter** (DROPPED — redundant with OccursDuring)
**constant_shudder** REWORDED_TO **constant_vibration_shudder**
**surging_hunting_idle** IS a **Tier-2 sub-filter** (ADDED — vacuum leak / idle-control mapping)
**stalls_on_cold_start** IS a **Tier-2 sub-filter** (ADDED — cold manifold leak / thermal sensor mapping)
**flat_sluggish_always** KEPT as **flat_sluggish_always**
**only_high_rpm_highway** IS_NOT a **Tier-2 sub-filter** (DROPPED — captured by LoadState)
**sudden_jerk_stumble** KEPT as **sudden_jerk_stumble**
**hesitation_throttle_tip_in** IS a **Tier-2 sub-filter** (ADDED — transient fuelling / TPS mapping)
**just_poor_mpg** KEPT as **just_poor_mpg**
**strong_fuel_smell** KEPT as **strong_fuel_smell**
**right_after_fillup** IS_NOT a **Tier-2 sub-filter** (DROPPED — EVAP overlap)
**knock_pinging_under_load** IS a **Tier-2 sub-filter** (ADDED — EGR / advanced timing mapping)
**when_coasting_to_stop** KEPT as **when_coasting_to_stop**
**intermittent_random** REWORDED_TO **intermittent_random_cutout**
**only_when_hot** IS_NOT a **Tier-2 sub-filter** (DROPPED — redundant with OccursDuring)
**backfire_loud_pop** IS a **Tier-2 sub-filter** (ADDED — mistimed spark / misaligned valves mapping)
**black_smoke** KEPT as **black_smoke**
**blue_oily_smell** KEPT as **blue_oily_smell**
**white_sweet_smell** KEPT as **white_sweet_smell**
**LoadState** ADDED as **third context axis** (idle, steady_cruise, transient_acceleration, coasting_deceleration)
**oil_consumption** ADDED as **seventh Tier-1 category** (blue_smoke_on_cold_start_clears, blue_smoke_under_acceleration, oil_loss_no_visible_smoke)
**SAE_J1635** SOURCED **cold_start_driveability** (standard cold-start procedure)
**SAE_J2944** SOURCED **driving_performance_measures** (operational definitions)
**EPA_light_duty_investigation** SOURCED **driveability_survey** (customer complaint frequency)
**NHTSA_PE10_019** SOURCED **defects_investigation** (manufacturer defect patterns)
**retail_blogs** SUPPRESSED as **primary source** (replaced by SAE/EPA/NHTSA standards)


## Core Entities

- **legacy_symptom_catalog** (historical) — PREDECESSOR_OF **revised_21_pair_catalog**
- **revised_21_pair_catalog** (live) — CONSUMED_BY **SymptomValidator** (symptomlab/symptomlab/validator.py)
- **LoadState** (StrEnum, live) — CONSUMED_BY **EnvironmentalConditions**, **SymptomValidator.validate** (symptomlab/symptomlab/models.py)
- **oil_consumption** (Tier-1, live) — CONSUMED_BY **SymptomValidator.validate** (symptomlab/symptomlab/validator.py)
- **DROPPED sub-filters**: cold_engine_only, hot_engine_only, only_high_rpm_highway, right_after_fillup, only_when_hot (non-edges, no live consumer)
- **ADDED sub-filters**: surging_hunting_idle, stalls_on_cold_start, hesitation_throttle_tip_in, knock_pinging_under_load, backfire_loud_pop (live, CONSUMED_BY SymptomValidator.validate)
- **SAE J1635** (standard) — SOURCED **cold-start driveability complaints**
- **SAE J2944** (standard) — SOURCED **driving-performance measures**
