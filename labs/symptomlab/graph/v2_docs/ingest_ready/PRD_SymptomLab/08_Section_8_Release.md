> **Context:** SymptomLab PRD v2.1 (2026-06-12) · Module: SymptomLab · Section 8 — Release · Parent document: PRD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

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
---

## Graph relations (explicit)

**PRD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**T-DNA-1/T-DNA-8** SUPERSEDES **legacy 18-pair catalog** (revised vocabulary, reconciled)
**T-DNA-2** DESCRIBES **load_state environmental axis** (consumer: COMLab-B)
**T-DNA-10** DESCRIBES **will_not_start wire value rename** (schema_version 1.1→1.2)
