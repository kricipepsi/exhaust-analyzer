> **Context:** SymptomLab PRD v2.1 (2026-06-12) · Module: SymptomLab · Section 7 — Solution · Parent document: PRD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

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
---

## Graph relations (explicit)

**PRD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**SymptomDNA** ENUMERATES **4 contract fields** (tier_1, tier_2, environmental_conditions, free_text_notes)
**SymptomValidator** GATED_BY **18-pair invariant at construction**
