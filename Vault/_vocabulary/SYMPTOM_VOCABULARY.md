---
node_type: "wiki"
lab: "symptomlab"
module: "semantic-vocabulary"
subsystem: "symptom-enums-catalog"
implements:
  - "labs/symptomlab/symptomlab/models.py"
  - "labs/symptomlab/symptomlab/data/allowed_combinations.yaml"
consumers:
  - "symptomlab: labs/symptomlab/symptomlab/validator.py SymptomValidator.validate (catalog + axis-enum vocabulary)"
  - "dnalab: labs/dnalab/dnalab/models.py SymptomDNA.from_json (axis-enum membership)"
  - "comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (engine_state / occurs_during literals)"
drift_guards:
  - "labs/symptomlab/tests/unit/test_validator.py"
  - "labs/symptomlab/tests/unit/test_models.py"
tags: [vocabulary, symptom, semantic, finished]
source: "labs/symptomlab/docs/SYMPTOM_VOCABULARY.md"
---
# SYMPTOM_VOCABULARY — SymptomLab (v2)
**Status:** Current (reflects shipped `models.py` + `allowed_combinations.yaml`)
**Date:** 2026-06-12
**Source of truth:** `SEMANTIC_CONTRACT.md §4.2, §8`; `VehicleDNA.md` triage diagram.

This file is the single reference for every vocabulary string SymptomLab emits on
`SymptomDNA`. The **tier** vocabulary is open (YAML-validated `str`); the
**environmental** vocabulary is closed (`StrEnum`). Drift between this file, the YAML
catalog, and `models.py` is a code-review stop.

---

## 1. Tier vocabulary — the 18-pair catalog (open, YAML-validated)

Curated in `data/allowed_combinations.yaml`. 6 `tier_1` × 3 `tier_2` = 18 pairs. These
strings are the routing keys COMLab's `fault_atlas_router` consumes (proposal COMLab-A).

| `tier_1` (primary symptom) | `tier_2` (sub-filter) |
|----------------------------|-----------------------|
| `vehicle_starting_issues` | `no_crank_silent`, `fast_crank_whining`, `prolonged_crank_hard_start` |
| `rough_idle_shudder` | `constant_vibration_shudder`, `surging_hunting_idle`, `stalls_on_cold_start` |
| `lack_of_power_hesitation` | `flat_sluggish_always`, `hesitation_throttle_tip_in`, `sudden_jerk_stumble` |
| `poor_economy_fuel_odor_sound` | `just_poor_mpg`, `strong_fuel_smell`, `knock_pinging_under_load` |
| `engine_dies_or_stalls` | `when_coasting_to_stop`, `intermittent_random_cutout`, `backfire_loud_pop` |
| `visible_exhaust_smoke` | `black_smoke`, `blue_oily_smell`, `white_sweet_smell` |

> **Live-file state (T-DNA-1 / T-DNA-8):** the shipped catalog matches this table — 18
> pairs, with `visible_exhaust_smoke = {black_smoke, blue_oily_smell, white_sweet_smell}`.
> T-DNA-8 added `white_sweet_smell` and renamed the legacy `blue_oily` to
> `blue_oily_smell`. The 18-pair invariant passes.

### Renamed `tier_1` categories (T-DNA-1)
| Legacy | Revised |
|--------|---------|
| `vehicle_wont_start` | `vehicle_starting_issues` |
| `poor_economy_fuel_odor` | `poor_economy_fuel_odor_sound` |

### Dropped legacy `tier_2` values (dimensional overlap)
`cold_engine_only`, `hot_engine_only`, `only_when_hot` (duplicated `occurs_during`);
`only_high_rpm_highway`, `right_after_fillup` (duplicated the load axis);
`normal_crank_zero_rpm`, `constant_shudder`, `intermittent_random` (reworded).

---

## 2. Environmental vocabulary — closed `StrEnum`s

### `OccursDuring` (`models.py`)
| Member | Wire value |
|--------|-----------|
| `ALWAYS` | `always` |
| `COLD_ONLY` | `cold_only` |
| `HOT_ONLY` | `hot_only` |
| `INTERMITTENT` | `intermittent` |

### `EngineState` (`models.py`)
| Member | Wire value |
|--------|-----------|
| `RUNNING` | `running` |
| `CRANKING` | `cranking` |
| `WONT_START` | `will_not_start` |

> T-DNA-10 renamed the `WONT_START` wire value from the legacy `won_not_start` to
> `will_not_start` (both ends), bumping the umbrella `schema_version` 1.1→1.2.

### `LoadState` — third axis (`models.py`, shipped T-DNA-2)
| Member | Wire value |
|--------|-----------|
| `IDLE` | `idle` |
| `STEADY_CRUISE` | `steady_cruise` |
| `TRANSIENT_ACCELERATION` | `transient_acceleration` |
| `COASTING_DECELERATION` | `coasting_deceleration` |

Source SAE J2944. Consumer: COMLab context-modifier prior (forward-registered COMLab-B /
`T-COMV2-CTXMOD-1`) + the 65% symptom trust-ceiling cap.

---

## 3. `SymptomDNA` keys (JSON contract surface, §4.2)

`tier_1_primary_symptom` (str), `tier_2_subfield_filter` (str),
`environmental_conditions` (`{occurs_during, engine_state, load_state}`), `free_text_notes`
(str | None).

---

## 4. Forbidden / retired tokens

| Token | Status |
|-------|--------|
| `suppress_modes`, `prioritize_modes`, `target_backend_equation`, `ui_input_fields` | forbidden on `SymptomDNA` — routing is COMLab-owned (§4.2) |
| `StrEnum` for `tier_1`/`tier_2` | forbidden — tiers are open YAML-validated `str` (ADR-0002) |
| legacy overlapping tier_2 values (§1) | retired by T-DNA-1 |
| legacy `blue_oily` (tier_2) | retired — renamed to `blue_oily_smell` (T-DNA-8) |
| legacy `won_not_start` (engine_state wire value) | retired — renamed to `will_not_start` (T-DNA-10) |
| cross-lab import (except `dnalab → symptomlab`) | forbidden — DNA-family boundary |
| catalog size ≠ 18 | forbidden — construction-time invariant |

---

## 5. Proposed Oil-Consumption Symptom Vocabulary (Proposals Registry)

To maintain the live 18-pair catalog invariant, the three new symptom-triage pairs for oil-burning diagnostics are registered as **proposals only** in the proposals registry:

| Proposed `tier_1` | Proposed `tier_2` | Target Fault / Live Registry Rule ID | Future Consumer |
|---|---|---|---|
| `oil_consumption` | `blue_smoke_on_cold_start_clears` | Valve stem seals (`MW-002`) | U-OIL-KG-1 (v2 KG enrichment) |
| `oil_consumption` | `blue_smoke_under_acceleration` | Piston rings (`MW-001`) / Turbo seals (`MW-009`) | T-OIL-R5 (turbo rule) + U-OIL-KG-1 |
| `oil_consumption` | `oil_loss_no_visible_smoke` | Stuck-open PCV (`MW-008`) | T-OIL-R4 (PCV rule) + U-OIL-KG-1 |

