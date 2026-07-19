---
node_type: prd
lab: symptomlab
module: symptomlab
subsystem: requirements
implements: []
consumers:
  - "hld: labs/symptomlab/docs/HLD_SymptomLab.md"
  - "dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (Part-B producer contract)"
drift_guards: []
tags: [symptomlab, requirements, prd]
source: "labs/symptomlab/docs/PRD_SymptomLab.md"
---

# PRD — SymptomLab
**Status:** Approved
**Version:** 2.1
**Date:** 2026-06-12
**Scope:** Petrol-only, v2 — operator-symptom triage module (Part B DNA producer)

---

## Section 1 — Summary

SymptomLab is the **operator-symptom channel** of the 4D petrol diagnostic pipeline. It
takes a two-tier triage selection (a primary symptom and a sub-filter) plus the
environmental context (when the symptom occurs, the engine state, and the load state),
validates the selection against a curated catalog, and packages it as a typed
`SymptomDNA` — the **symptom DNA** (Part B) of the diagnosis. The single public entry
point is `symptomlab.resolve(tier_1, tier_2, *, occurs_during, engine_state, load_state)
→ SymptomDNA`.

SymptomLab is one of the three sibling labs of the **DNA family** (`vinlab` +
`symptomlab` → `dnalab`). Its `SymptomDNA` is Part B; VINLab supplies Part A; DNALab
composes both into `VehicleDNA`. `SymptomDNA`'s shape is governed by
`SEMANTIC_CONTRACT.md §4.2` — exactly four fields, no routing.

SymptomLab is a **validator/packager, not a router.** It confirms the triage selection
is legal and types the environmental context; it does **not** decide which OBD modes to
suppress, which equation to run, or which fault family to favour. All routing
(`suppress_modes`, `target_backend_equation`, the symptom→family prior) lives in
**COMLab**. Critically, the symptom signal must remain a **prior**, never an override.

---

## Section 2 — Contacts

| Name | Role | Responsibility |
|------|------|----------------|
| SymptomLab Owner | Module Owner | Catalog curation, the 18-pair invariant, environmental enums, validation |
| COMLab Team | Integration Consumer | Mirrors `SymptomDNA`; routes tier_1/tier_2 to fault families in `fault_atlas_router` (the symptom prior); applies context modifiers; enforces the 65% trust ceiling |
| DNALab (assembly) | In-family Consumer | Calls `resolve()` with the triage dict; embeds `SymptomDNA` into `VehicleDNA` |
| 4DApp Engineering Lead | Architecture | Signal/noise rule; "prior, not override"; open-vocabulary-via-YAML decision |

---

## Section 3 — Background

**Context.** A layman operator describes a driveability problem in plain terms ("rough
idle", "black smoke"). To keep the diagnostic engine focused, the UI captures this as a
**two-tier menu**: Tier 1 is the primary observation; Tier 2 is a dynamic filtering
gate that narrows it. Together with environmental context (cold/hot, running/cranking,
idle/cruise/accel/coasting), this becomes a structured symptom record the engine can
route on — *without* free-text
parsing.

**Why now.** The symptom/identity channel is the cheapest independent prior in the 4D
engine. To use it honestly, the symptom vocabulary has to be curated (so two operators
describing the same problem land on the same pair) and bounded (so the routing map has a
fixed, testable surface). The catalog is the curated vocabulary; the validator enforces
its invariants.

**What recently became possible (v2 sibling split, T-RM-2-DNA, 2026-06-06).** SymptomLab
forked from v1 `DNALab/SymptomLab/` into an **independent module** with its own
`pyproject.toml`. The catalog moved to a YAML file (`allowed_combinations.yaml`) so the
tier vocabulary is an **open vocabulary validated by data**, not a hard-coded enum —
adding a symptom is a data edit, not a code change. The research-revised catalog
(T-DNA-1) reworked the pairs to remove dimensional overlap with the environmental axes.

---

## Section 4 — Objective

**Business benefit.** Turn an operator's plain-language complaint into a typed,
validated, routable symptom record — the input half of COMLab's symptom prior.

**Customer benefit.** The operator taps through a short, curated menu; impossible or
nonsensical combinations are rejected with a helpful message listing the valid options.

**Key Results:**

- **KR1:** `resolve()` returns a 4-field `SymptomDNA` for every legal triage selection
  (contract §4.2).
- **KR2:** The catalog holds **exactly 18** `(tier_1, tier_2)` pairs (6 × 3); the
  validator refuses to load any other count.
- **KR3:** Out-of-catalog pairs and out-of-vocabulary environmental values raise
  `SymptomValidationError` with the valid options listed.
- **KR4:** Tier vocabulary is open (YAML-driven) — adding a symptom requires **no** code
  change.
- **KR5:** `SymptomDNA` carries **no** routing fields (routing lives in COMLab).
- **KR6:** Zero cross-lab Python imports (DNA-family boundary; COMLab mirrors the type).

---

## Section 5 — Market Segment

**Layman operator + advanced technician.** The two-tier menu lets a non-expert describe
the problem in everyday terms while producing a record precise enough for the
diagnostic engine. The technician benefits because the symptom prior narrows the search
before any PID is read.

---

## Section 6 — Value Proposition

- **Jobs addressed:** triage validation, environmental-context typing, symptom-record
  packaging.
- **Gains created:** one `resolve()` call yields a contract-shaped `SymptomDNA`;
  invalid selections are caught at the boundary with actionable error messages; the
  catalog is curated to one canonical pair per real-world symptom.
- **Pains relieved:** no free-text NLP; no routing logic leaking into the symptom
  record; the open-vocabulary YAML means the catalog evolves without code churn.
- **Competitive advantage:** the channel is honest by construction — the lab produces a
  *prior input*, and the architecture forbids it from becoming an override. The 18-pair
  invariant keeps COMLab's routing map a fixed, fully-tested surface.

---

## Section 7 — Solution

### Key Features (all P0)

- P0: **Two-tier triage validation** — `(tier_1, tier_2)` must be one of the 18 catalog
  pairs, else `SymptomValidationError` listing the valid `tier_2` values for that
  `tier_1` (or the valid `tier_1` values).
- P0: **18-pair invariant** — the validator raises on construction if the catalog does
  not define exactly 18 pairs.
- P0: **Environmental typing** — `occurs_during` → `OccursDuring`, `engine_state` →
  `EngineState`, `load_state` → `LoadState`; an out-of-vocabulary value raises
  `SymptomValidationError`.
- P0: **Open tier vocabulary** — tier strings are `str`, validated by YAML, not enums.
- P0: **`SymptomDNA` output** — 4 fields, `to_json()` / `from_json()`; `from_json()`
  validates enum membership + presence only (not the 18-pair invariant — that is
  `resolve()`'s job).
- P0: **Routing-free** — no `suppress_modes` / `target_backend_equation` / prior numbers.

### Technology

- Python 3.14 + PyYAML. Package `symptomlab`, standalone `pyproject.toml`.
- Entry point: `symptomlab.resolve(...)`, wrapping an `lru_cache`d `SymptomValidator`
  per catalog path.
- Exception: `SymptomValidationError(ValueError)`.
- No cross-lab imports — COMLab mirrors `SymptomDNA` locally.

### `SymptomDNA` fields (4, contract §4.2)

| # | Field | Type | Notes |
|---|-------|------|-------|
| 1 | `tier_1_primary_symptom` | `str` | open vocabulary (YAML catalog) |
| 2 | `tier_2_subfield_filter` | `str` | open vocabulary (YAML catalog) |
| 3 | `environmental_conditions` | `EnvironmentalConditions` | `occurs_during` + `engine_state` + `load_state` |
| 4 | `free_text_notes` | `str \| None` | optional operator note (default `None`) |

### Assumptions

| Assumption | Validation |
|-----------|-----------|
| The catalog is exactly 18 pairs (6 tier_1 × 3 tier_2) | `SymptomValidator.__init__` raises `ValueError` if `len != 18` |
| Tier vocabulary may grow without code change | tier fields are `str` validated against the YAML, not enums |
| Routing is COMLab-owned | `SymptomDNA` has no routing fields (`DNALab_TO_COMLab_FLOW.md §4`) |
| The symptom signal is a prior, never an override | enforced downstream in COMLab (65% trust ceiling, COMLab-B) |

---

## Section 8 — Release

### v2 Scope

All P0 features above, post sibling-split (T-RM-2-DNA) with the YAML-driven catalog and
enum-typed environmental conditions.

### Landed (DNA-family pack — see `labs/dnalab/tasks/PROGRESS.md`)

- **T-DNA-1 / T-DNA-8 — revised symptom catalog (`done`).** The catalog was reworked to
  remove dimensional overlap with the environmental axes, then reconciled to the full
  **18** pairs: `visible_exhaust_smoke = {black_smoke, blue_oily_smell, white_sweet_smell}`.
  The live `allowed_combinations.yaml` now satisfies the 18-pair invariant.
- **T-DNA-2 — `load_state` environmental axis (`done`, shipped).** A third axis
  (`idle` / `steady_cruise` / `transient_acceleration` / `coasting_deceleration`, SAE
  J2944) separating static air-metering faults from transient load failures. It is part
  of `EnvironmentalConditions` and a required `resolve()` argument. Consumer: COMLab
  context-modifier prior (forward-registered COMLab-B / `T-COMV2-CTXMOD-1`) + the 65%
  trust-ceiling cap.
- **T-DNA-10 — `engine_state` wire value rename (`done`).** `will_not_start` replaced the
  legacy `won_not_start`; the umbrella `schema_version` moved 1.1→1.2.

### Explicitly Deferred

- The symptom→family prior probability numbers and context-modifier weights (COMLab
  owns them — COMLab-A / COMLab-B).
- **T-DNA-9 — `oil_consumption` symptom.** Owner-deferred; with the coder. Needs a
  catalog-cap disposition (new tier_1, raising the invariant to 21, vs a new tier_2) and
  a named COMLab-A consumer extension before it can ship. Not in the current schema.

### Success Criteria

1. KR1–KR6 hold.
2. The catalog loads at exactly 18 pairs and every legal pair resolves.
3. Every illegal pair / out-of-vocabulary environmental value raises
   `SymptomValidationError`.
4. No routing fields on `SymptomDNA`; no cross-lab Python imports.
