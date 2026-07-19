---
node_type: lld
lab: symptomlab
module: symptomlab
subsystem: low-level-design
implements:
  - "labs/symptomlab/symptomlab/__init__.py"
  - "labs/symptomlab/symptomlab/models.py"
  - "labs/symptomlab/symptomlab/validator.py"
  - "labs/symptomlab/symptomlab/data/allowed_combinations.yaml"
consumers:
  - "dld: labs/symptomlab/docs/DLD_SymptomLab.md"
  - "dnalab: labs/dnalab/dnalab/assembly.py resolve() -> VehicleDNA Part B"
  - "comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (environmental_conditions)"
drift_guards:
  - "labs/symptomlab/tests/unit/test_validator.py"
  - "labs/symptomlab/tests/unit/test_models.py"
  - "labs/symptomlab/tests/unit/test_symptomdna_from_json.py"
  - "labs/symptomlab/tests/unit/test_resolve_isolation.py"
  - "labs/symptomlab/tests/unit/test_drift_guard.py"
tags: [symptomlab, low-level-design, lld]
source: "labs/symptomlab/docs/LLD_SymptomLab.md"
---

# LLD — SymptomLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_SymptomLab v2.0
**HLD / DLD Reference:** HLD_SymptomLab v2.1 / DLD_SymptomLab v2.1
**Version:** 2.1
**Date:** 2026-06-12

SymptomLab carries one numeric literal of significance — the catalog-size invariant.
Everything else is vocabulary, not arithmetic.

---

## 1. The 18-Pair Invariant (`validator.py`)

```python
if len(self._allowed) != 18:                # source: SEMANTIC_CONTRACT.md §4.2
    raise ValueError(
        f"allowed_combinations.yaml must define exactly 18 pairs, got {len(...)}"
    )
```

`18 = 6 tier_1 × 3 tier_2`. The invariant is checked at **construction**, so a malformed
catalog fails before any triage is validated. There are no other tunable numeric
literals in the package.

---

## 2. Pair-Set Construction (`validator.py`)

```python
self._allowed: set[tuple[str, str]] = {
    (tier_1, tier_2)
    for tier_1, tier_2_list in doc["combinations"].items()
    for tier_2 in tier_2_list
}
```

A `set` of `(str, str)` tuples — membership test is O(1). Order in the YAML is
irrelevant; duplicates would silently collapse (and then fail the `== 18` count).

---

## 3. Environmental Enum Coercion (`validator.py`)

```python
try:
    occ  = OccursDuring(occurs_during)  # "always" | "cold_only" | "hot_only" | "intermittent"
    eng  = EngineState(engine_state)    # "running" | "cranking" | "will_not_start"
    load = LoadState(load_state)        # "idle" | "steady_cruise" | "transient_acceleration" | "coasting_deceleration"
except ValueError as exc:
    raise SymptomValidationError(str(exc)) from exc
```

The `StrEnum(value)` call is the validation: an out-of-vocabulary string raises
`ValueError`, re-wrapped as `SymptomValidationError`.

---

## 4. Error-Message Construction (`validator.py`)

When `(tier_1, tier_2)` is rejected, the message is built to be actionable:

```python
valid_tier_2s = sorted(t2 for (t1, t2) in self._allowed if t1 == tier_1)
if valid_tier_2s:
    msg = f"Unknown (tier_1={tier_1!r}, tier_2={tier_2!r}). Valid tier_2 for {tier_1!r}: {valid_tier_2s}"
else:
    tier_1s = sorted({t1 for (t1, _) in self._allowed})
    msg = f"Unknown tier_1={tier_1!r}. Valid tier_1 values: {tier_1s}"
```

A wrong sub-filter lists the valid sub-filters for that category; a wrong category lists
the valid categories.

---

## 5. Serialization (`models.py`)

```python
EnvironmentalConditions.to_json() → {"occurs_during": occ.value, "engine_state": eng.value, "load_state": load.value}

SymptomDNA.to_json() → {
    "tier_1_primary_symptom": ...,
    "tier_2_subfield_filter": ...,
    "environmental_conditions": {...},
    "free_text_notes": ...,         # may be None
}
```

`from_json` reconstructs via `OccursDuring(env["occurs_during"])` /
`EngineState(env["engine_state"])` / `LoadState(env.get("load_state", LoadState.IDLE))`
(a pre-`load_state` payload defaults to `idle`), catching `KeyError` (missing field) and
`ValueError` (bad enum) and re-raising both as `SymptomValidationError`.

---

## 6. Catalog Literals (`data/allowed_combinations.yaml`)

The 18 tier strings — these are the only "literals" that matter, and they are data:

```
tier_1 (6):  vehicle_starting_issues, rough_idle_shudder, lack_of_power_hesitation,
             poor_economy_fuel_odor_sound, engine_dies_or_stalls, visible_exhaust_smoke
tier_2 (3 each): see HLD §4
```

> **Live-file state:** `visible_exhaust_smoke` ships with 3 entries
> (`black_smoke`, `blue_oily_smell`, `white_sweet_smell`) → 18 total, satisfying §1
> (reconciled by T-DNA-8).

---

## 7. Forbidden Patterns (SymptomLab-specific)

| Pattern | Enforcement |
|---------|-------------|
| `from gaslab/obdlab/dtclab/comlab/vinlab import …` | DNA-family import boundary (one-way: `dnalab → symptomlab`) |
| Tier vocabulary as a hard-coded `StrEnum` | open-vocabulary rule — tier strings stay `str`, validated by YAML |
| Routing fields (`suppress_modes`, `target_backend_equation`, prior numbers) on `SymptomDNA` | routing is COMLab-owned (contract §4.2) |
| A catalog of any size other than 18 | construction-time `ValueError` invariant |
| Re-running graphify against `graph/` | frozen verified artefact; not in the inner loop |
