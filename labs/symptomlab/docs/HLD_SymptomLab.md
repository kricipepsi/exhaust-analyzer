---
node_type: hld
lab: symptomlab
module: symptomlab
subsystem: architecture
implements: []
consumers:
  - "lld: labs/symptomlab/docs/LLD_SymptomLab.md"
  - "dld: labs/symptomlab/docs/DLD_SymptomLab.md"
  - "dnalab: labs/dnalab/dnalab/assembly.py resolve() integration"
  - "comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (SymptomDNA env conditions)"
drift_guards: []
tags: [symptomlab, architecture, hld]
source: "labs/symptomlab/docs/HLD_SymptomLab.md"
---

# HLD — SymptomLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_SymptomLab v2.0
**Version:** 2.1
**Date:** 2026-06-12

> **Refresh note (2026-06-12):** updated to the landed state of the DNA-family pack.
> The 18-pair catalog (T-DNA-1/T-DNA-8), the `load_state` third axis (T-DNA-2), and the
> `will_not_start` engine-state wire value (T-DNA-10) are now shipped; the earlier
> 17-pair "known gap" is closed. Fields, enums, and the catalog invariant are transcribed
> from the shipped source.

---

## 1. Responsibility

SymptomLab is the **operator-symptom channel** of the 4D petrol diagnostic pipeline. It
validates a two-tier triage selection and packages it as a typed `SymptomDNA` — the
**symptom DNA** (Part B). It is a **validator/packager, not a router**: it confirms the
selection is legal and types the environmental context; it never decides routing or
fault families. `SymptomDNA`'s schema is governed by `SEMANTIC_CONTRACT.md §4.2` (exactly
four fields, no routing).

The symptom signal it produces must stay a **prior** downstream, never an override.

---

## 2. Architecture Position

```
UI two-tier triage  +  environmental context
  │  (tier_1, tier_2, occurs_during, engine_state, load_state, free_text_notes?)
  ▼
DNALab assembly.build_vehicle_dna  ── calls ──▶  symptomlab.resolve(...)
  │
  ▼
symptomlab.__init__.resolve
  │  _get_validator(allowed_path)  ── lru_cache per catalog path
  ▼
SymptomValidator.validate
  │  [1] (tier_1, tier_2) ∈ 18-pair catalog?   else SymptomValidationError(valid options)
  │  [2] OccursDuring(occurs_during)            else SymptomValidationError
  │  [3] EngineState(engine_state)              else SymptomValidationError
  │  [4] LoadState(load_state)                  else SymptomValidationError
  ▼
SymptomDNA  (4 fields: tier_1, tier_2, environmental_conditions, free_text_notes;
             environmental_conditions now carries 3 axes)
  │
  ▼
COMLab mirrors SymptomDNA and routes tier_1/tier_2 → fault families (the prior).
```

Zero cross-lab Python imports. COMLab mirrors `SymptomDNA` locally.

---

## 3. Internal Flow (validate)

```
SymptomValidator(allowed_path):                    # constructed once, lru_cached
    load allowed_combinations.yaml
    self._allowed = {(t1, t2) for t1, [t2...] in doc["combinations"]}
    assert len(self._allowed) == 18  else ValueError   # hard invariant

validate(tier_1, tier_2, occurs_during, engine_state, load_state, free_text_notes=None):
    if (tier_1, tier_2) not in self._allowed:
        list valid tier_2 for tier_1 (or valid tier_1 values) → SymptomValidationError
    occ  = OccursDuring(occurs_during)  # ValueError → SymptomValidationError
    eng  = EngineState(engine_state)    # ValueError → SymptomValidationError
    load = LoadState(load_state)        # ValueError → SymptomValidationError
    return SymptomDNA(tier_1, tier_2, EnvironmentalConditions(occ, eng, load), free_text_notes)
```

The 18-pair invariant is enforced at **construction**: a catalog of any other size fails
fast before any triage is validated.

---

## 4. The Catalog (`data/allowed_combinations.yaml`)

The catalog is the curated symptom vocabulary: 6 `tier_1` categories × 3 `tier_2`
sub-filters = 18 pairs. It is **data, not code** — tier strings are open vocabulary
validated against this file, so adding a symptom is a YAML edit. Source: the
`VehicleDNA.md` "Complete Universal Triage & Diagnostic Mapping Diagram"; contract
`§4.2` declares these strings the enum source.

Shipped (revised, T-DNA-1 / reconciled T-DNA-8) 6 × 3 catalog:

| tier_1 | tier_2 (3 each) |
|--------|-----------------|
| `vehicle_starting_issues` | `no_crank_silent`, `fast_crank_whining`, `prolonged_crank_hard_start` |
| `rough_idle_shudder` | `constant_vibration_shudder`, `surging_hunting_idle`, `stalls_on_cold_start` |
| `lack_of_power_hesitation` | `flat_sluggish_always`, `hesitation_throttle_tip_in`, `sudden_jerk_stumble` |
| `poor_economy_fuel_odor_sound` | `just_poor_mpg`, `strong_fuel_smell`, `knock_pinging_under_load` |
| `engine_dies_or_stalls` | `when_coasting_to_stop`, `intermittent_random_cutout`, `backfire_loud_pop` |
| `visible_exhaust_smoke` | `black_smoke`, `blue_oily_smell`, `white_sweet_smell` |

The rework removed tier_2 values that duplicated the `occurs_during` axis
(`cold_engine_only`, `only_when_hot`) and the load axis
(`only_high_rpm_highway`, `right_after_fillup`), and filled gaps (surging idle,
prolonged crank, tip-in hesitation, knock, backfire).

> **Live-file note:** the shipped file matches this table exactly — 18 pairs, with
> `visible_exhaust_smoke = {black_smoke, blue_oily_smell, white_sweet_smell}` (reconciled
> by T-DNA-8). The validator's `len == 18` invariant passes at construction.

---

## 5. Environmental Context

`EnvironmentalConditions` (frozen) carries the three environmental axes that are typed
enums (unlike the open tier vocabulary):

| Axis | Enum | Members |
|------|------|---------|
| `occurs_during` | `OccursDuring` | `always`, `cold_only`, `hot_only`, `intermittent` |
| `engine_state` | `EngineState` | `running`, `cranking`, `will_not_start` |
| `load_state` | `LoadState` | `idle`, `steady_cruise`, `transient_acceleration`, `coasting_deceleration` |

These are typed because they are a small, closed, contract-fixed set — the diagnostic
engine branches on them, so an out-of-vocabulary value must fail at the boundary.
The third axis, `load_state` (mechanical load), is **shipped** (T-DNA-2); it separates
static air-metering faults from transient load failures. Its COMLab consumer is the
context-modifier prior with a 65% trust ceiling (forward-registered as COMLab-B).

---

## 6. Downstream Integration Points (consumers)

| `SymptomDNA` content | Consumer | Status |
|----------------------|----------|--------|
| `tier_1_primary_symptom` / `tier_2_subfield_filter` | COMLab `fault_atlas_router` symptom→family prior | proposal COMLab-A (T-DNA-1) |
| `environmental_conditions.occurs_during` / `engine_state` | COMLab context modifiers | live mirror |
| `environmental_conditions.load_state` | COMLab context-modifier prior + 65% trust ceiling | shipped (T-DNA-2); consumer forward-registered COMLab-B / `T-COMV2-CTXMOD-1` (Stage 4) |
| `free_text_notes` | operator-facing context only (not routed) | passthrough |

> **Cross-lab note:** the prior probability tables and context-modifier weights live in
> COMLab, not here. SymptomLab supplies the *vocabulary*; COMLab owns the *numbers* and
> the trust ceiling that keeps the symptom signal a prior, not an override.

---

## 7. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Catalog size | exactly 18 `(tier_1, tier_2)` pairs (enforced at construction) |
| Routing fields on `SymptomDNA` | 0 (routing is COMLab's) |
| Import isolation | 0 cross-lab Python imports (one-way: `dnalab → symptomlab`) |
| Vocabulary openness | tier strings validated by YAML, no code change to add a symptom |
| Signal/noise | every new symptom string / axis value has a named COMLab consumer (proposal) |

---

## 8. Error Behaviour

| Condition | Result |
|-----------|--------|
| Catalog `len != 18` at load | `ValueError` (construction fails) |
| `(tier_1, tier_2)` not in catalog | `SymptomValidationError` listing valid options |
| `occurs_during` / `engine_state` / `load_state` not in enum | `SymptomValidationError` |
| `from_json` missing required field | `SymptomValidationError` (wraps `KeyError`) |
| `from_json` bad enum string | `SymptomValidationError` (wraps `ValueError`) |

---

## 9. Known Gaps / Accepted Behaviour

| ID | Description | Status |
|----|-------------|--------|
| `from_json` scope | `SymptomDNA.from_json()` validates enum membership + presence only, **not** the 18-pair invariant — callers building from user input must use `resolve()` | Accepted (documented) |
| Routing absence | `SymptomDNA` deliberately omits `suppress_modes` / `target_backend_equation` | By design (COMLab-owned) |
| `oil_consumption` symptom | Owner-requested 7th-symptom candidate, mapping to worn rings / valve-stem seals / turbo seal / PCV. Needs a catalog-cap disposition (new tier_1 → raise invariant to 21, vs new tier_2) and a named COMLab-A consumer extension. | Deferred — T-DNA-9 (with the coder; not in this schema) |
