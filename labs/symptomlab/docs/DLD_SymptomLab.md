---
node_type: dld
lab: symptomlab
module: symptomlab
subsystem: detailed-design
implements:
  - "labs/symptomlab/symptomlab/__init__.py"
  - "labs/symptomlab/symptomlab/models.py"
  - "labs/symptomlab/symptomlab/validator.py"
  - "labs/symptomlab/symptomlab/data/allowed_combinations.yaml"
consumers:
  - "dnalab: labs/dnalab/dnalab/assembly.py resolve() -> VehicleDNA Part B"
  - "dnalab: labs/dnalab/dnalab/models.py SymptomDNA.from_json -> VehicleDNA.symptom_dna"
  - "comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (environmental_conditions)"
drift_guards:
  - "labs/symptomlab/tests/unit/test_validator.py"
  - "labs/symptomlab/tests/unit/test_models.py"
  - "labs/symptomlab/tests/unit/test_symptomdna_from_json.py"
  - "labs/symptomlab/tests/unit/test_resolve_isolation.py"
  - "labs/symptomlab/tests/unit/test_drift_guard.py"
tags: [symptomlab, detailed-design, dld]
source: "labs/symptomlab/docs/DLD_SymptomLab.md"
---

# DLD — SymptomLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_SymptomLab v2.0
**HLD Reference:** HLD_SymptomLab v2.1
**Version:** 2.1
**Date:** 2026-06-12

> Grounded in the live `symptomlab/` package as of 2026-06-12 — 18-pair catalog,
> `load_state` axis, and `will_not_start` wire value all shipped.

---

## 1. Module Map

```
symptomlab/
├── __init__.py        ← public surface: resolve(), SymptomDNA, EnvironmentalConditions, LoadState, SymptomValidationError
├── models.py          ← SymptomDNA, EnvironmentalConditions, OccursDuring, EngineState, LoadState, SymptomValidationError
├── validator.py       ← SymptomValidator (loads catalog, enforces 18-pair invariant, validate())
└── data/
    └── allowed_combinations.yaml  ← the 18-pair curated catalog (data, not code)
```

`resolve()` wraps an `lru_cache`d `SymptomValidator` per catalog path.

---

## 2. `models.py` — Enums (3 StrEnums)

The environmental axes are typed (closed, contract-fixed sets). The tier vocabulary is
**not** an enum — see §4.

| Enum | Members (wire value) |
|------|----------------------|
| `OccursDuring` | `ALWAYS="always"`, `COLD_ONLY="cold_only"`, `HOT_ONLY="hot_only"`, `INTERMITTENT="intermittent"` |
| `EngineState` | `RUNNING="running"`, `CRANKING="cranking"`, `WONT_START="will_not_start"` |
| `LoadState` | `IDLE="idle"`, `STEADY_CRUISE="steady_cruise"`, `TRANSIENT_ACCELERATION="transient_acceleration"`, `COASTING_DECELERATION="coasting_deceleration"` |

> Note the `WONT_START` member's wire value is the literal `will_not_start` (T-DNA-10
> renamed it from the legacy `won_not_start`; the umbrella `schema_version` moved 1.1→1.2).

---

## 3. `models.py` — Dataclasses

### `EnvironmentalConditions` (frozen)

| Field | Type |
|-------|------|
| `occurs_during` | `OccursDuring` |
| `engine_state` | `EngineState` |
| `load_state` | `LoadState` |

`to_json() → {"occurs_during": <value>, "engine_state": <value>, "load_state": <value>}`.

### `SymptomDNA` (frozen) — the 4-field Part B payload (contract §4.2)

| # | Field | Type | Default |
|---|-------|------|---------|
| 1 | `tier_1_primary_symptom` | `str` | — (required) |
| 2 | `tier_2_subfield_filter` | `str` | — (required) |
| 3 | `environmental_conditions` | `EnvironmentalConditions` | — (required) |
| 4 | `free_text_notes` | `str \| None` | `None` |

`to_json()` emits the four keys (environmental_conditions nested). `from_json(payload)`
is the inverse:

- Validates **enum membership** (`OccursDuring`, `EngineState`, `LoadState`) and **field
  presence** only. A payload that predates the `load_state` axis deserialises
  deterministically to `LoadState.IDLE` (`env.get("load_state", LoadState.IDLE)`).
- Does **not** check the 18-pair catalog invariant — that is `SymptomValidator.validate()`
  / `resolve()`'s job. `from_json()` is for deserialising an already-validated payload at
  the JSON boundary.
- Missing field → `SymptomValidationError` (wraps `KeyError`); bad enum string →
  `SymptomValidationError` (wraps `ValueError`).

`tier_1` / `tier_2` are `str`, **not** `StrEnum`, by deliberate design: they are open
vocabularies validated by the YAML catalog, so adding a symptom must not require a code
change.

---

## 4. `validator.py` — `SymptomValidator`

**`__init__(allowed_path)`** loads the YAML and builds the pair set:

```python
self._allowed = {
    (tier_1, tier_2)
    for tier_1, tier_2_list in doc["combinations"].items()
    for tier_2 in tier_2_list
}
if len(self._allowed) != 18:                # SEMANTIC_CONTRACT §4.2 hard invariant
    raise ValueError("must define exactly 18 pairs, got N")
```

**`validate(tier_1, tier_2, occurs_during, engine_state, load_state, free_text_notes=None) →
SymptomDNA`**:

1. If `(tier_1, tier_2)` not allowed → `SymptomValidationError`. The message lists the
   valid `tier_2` values for that `tier_1` when the `tier_1` is known, otherwise lists
   the valid `tier_1` values — an actionable error, not a bare rejection.
2. `OccursDuring(occurs_during)` / `EngineState(engine_state)` / `LoadState(load_state)`;
   a `ValueError` becomes a `SymptomValidationError`.
3. Returns `SymptomDNA(tier_1, tier_2, EnvironmentalConditions(occ, eng, load), free_text_notes)`.

---

## 5. `__init__.py` — public surface

```python
resolve(tier_1, tier_2, *, occurs_during, engine_state, load_state,
        free_text_notes=None, allowed_path=None) → SymptomDNA
```

Defaults `allowed_path` to `data/allowed_combinations.yaml`, fetches the `lru_cache`d
validator, and delegates to `validate()`. Routing (`suppress_modes`,
`target_backend_equation`) is explicitly **not** this lab's job (see the docstring).

`__all__ = ["resolve", "SymptomDNA", "EnvironmentalConditions", "LoadState", "SymptomValidationError"]`.

---

## 6. `data/allowed_combinations.yaml`

Structure: `combinations: {tier_1: [tier_2, ...]}`. Source: `VehicleDNA.md` triage
diagram; contract §4.2. Routing is **not** here (it lives in COMLab per
`DNALab_TO_COMLab_FLOW.md §4`).

Revised catalog = 18 pairs (HLD §4), shipped. **Live state:** 18 pairs —
`visible_exhaust_smoke = {black_smoke, blue_oily_smell, white_sweet_smell}` (reconciled by
T-DNA-8: `white_sweet_smell` added, legacy `blue_oily` renamed to `blue_oily_smell`). The
construction-time `len == 18` invariant passes.

---

## 7. Error Types

| Error | Base | Raised when |
|-------|------|-------------|
| `SymptomValidationError` | `ValueError` | pair not in catalog; environmental value out of enum; `from_json` missing field or bad enum |
| `ValueError` | — | catalog `len != 18` at construction (invariant breach) |

---

## 8. Test Coverage (current)

| Area | File |
|------|------|
| `SymptomDNA` / enums | `tests/test_models.py` |
| Validator (pairs + environmental) | `tests/test_validator.py` |
| `from_json` boundary | `tests/test_symptomdna_from_json.py` |
| Import isolation | `tests/test_resolve_isolation.py` |
| Catalog drift guard | `tests/test_drift_guard.py` |

> `graph/v1_baseline` vs `graph/v2_current` are frozen verified artefacts — no code
> reads them; not in the inner loop or verification gate.
