
> **Context:** DTCLab PRD v2.0 (2026-06-11) · Module: DTCLab · Section: Section 7 — Solution · Parent document: PRD_DTCLab.md
## Section 7 — Solution

### Key Features (all P0)

- P0: DTC format validation (`^[BCPU][0-3][0-9A-F]{3}$`) for modes `$03`, `$07`, `$0A`.
  Fail-fast on first invalid code.
- P0: Freeze-frame extraction (12 mandatory PIDs, 7 optional, 6 derived symptom flags).
- P0: Historical fault-context classification (4 states, strict priority order).
- P0: Mode $06 margin tri-state evaluation (33-MID dictionary, LRU-cached load).
- P0: DTC routing-tag mapping — 30 entries (27 ungated + 3 DNA-gated).
- P0: Cross-field coolant/fluid signatures (step 5b) → `COOLANT_SYSTEM_MALFUNCTION`,
  `CYLINDER_FLUID_MISFIRE`.
- P0: DNA confidence three-branch (HIGH strict / PARTIAL log+emit / NONE emit).
- P0: `DTCLabPayload` Pydantic output model (9 fields).
- P0: **Phase-2 scorer** (`ranking.py`) — `rank_candidates` / `classify_top3` → top-3
  `(family, confidence)` for COMLab Bayesian fusion (FU-1), via the Wired adapter (T-DTW-1).
- P0: `DTC_CONFIDENCE_WEIGHTS` published for COMLab aggregator use.

### Technology

- Python 3.14 (workspace standard; `StrEnum` requires ≥ 3.11). Pydantic ≥ 2.5. PyYAML.
  `functools.lru_cache`. No cross-lab imports.
- Package: `dtclab`, standalone `pyproject.toml`.
- Entry point: `dtclab.DataFusionSanitizer.sanitize(...) → DTCLabPayload`.
- Optional surface: `dtclab.ranking.classify_top3(payload, dna_view=...) → list[(family, conf)]`.

### Assumptions

### Assumption: `DTC_CONFIDENCE_WEIGHTS` values are correct for COMLab aggregation and Phase-2 scoring
- **Validation**: Sourced from `DTC_VOCABULARY.md §16`; no drift-guard test yet (open issue)

### Assumption: `mode_06_hex_dictionary.json` covers needed universal CAN MIDs
- **Validation**: 33 entries from `§13.2`; manufacturer-specific MIDs deferred

### Assumption: `dtc_severity_map.yaml` not required
- **Validation**: `DTCSeverityClass` enum defined (reserved); severity logic deferred

### Assumption: Phase-2 scorer needs no new numeric literal
- **Validation**: All confidence from §16 weights × §14.2 DNA factor

---


## Graph relations (explicit)

**Section 7 — Solution** DESCRIBES **DTCLab PRD v2.0**
**DataFusionSanitizer.sanitize** CONSUMES **DtcLabDnaView** -- entry point
**ranking.classify_top3** CONSUMES **DTCLabPayload, DtcLabDnaView** -- Phase-2 candidate ranking
