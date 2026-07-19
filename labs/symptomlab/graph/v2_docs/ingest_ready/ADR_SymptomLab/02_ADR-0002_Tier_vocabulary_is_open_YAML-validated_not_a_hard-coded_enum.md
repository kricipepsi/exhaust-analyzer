> **Context:** SymptomLab ADR v2.1 (2026-06-12) · Module: SymptomLab · ADR-0002: Tier vocabulary is open (YAML-validated), not a hard-coded enum · Parent document: ADR_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## ADR-0002: Tier vocabulary is open (YAML-validated), not a hard-coded enum

**Status:** Accepted (sibling split, T-RM-2-DNA)

### Context

The symptom vocabulary will grow as the catalog is researched and refined. Encoding tier
strings as a `StrEnum` would make every catalog change a code change with a release.

### Decision

`tier_1_primary_symptom` and `tier_2_subfield_filter` are typed `str`, validated at
runtime against `data/allowed_combinations.yaml`. Adding or renaming a symptom is a data
edit; the code is unchanged. The two **environmental** axes, being a small closed set,
remain typed enums (ADR-0004).

### Consequences

- **Positive:** the catalog evolves without code churn; research can iterate on the
  vocabulary directly.
- **Negative:** tier typos are caught at runtime (validation), not at import — mitigated
  by the actionable error message listing valid options.

### Alternatives Considered

1. **`StrEnum` tiers.** Rejected: turns every vocabulary change into a code change.
2. **No validation (free strings).** Rejected: COMLab's routing map needs a fixed,
   known key set.

---
---

## Graph relations (explicit)

**ADR_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**tier_1_primary_symptom** GATED_BY **open vocabulary** (YAML-validated str, not StrEnum)
**tier_2_subfield_filter** GATED_BY **open vocabulary** (YAML-validated str, not StrEnum)
