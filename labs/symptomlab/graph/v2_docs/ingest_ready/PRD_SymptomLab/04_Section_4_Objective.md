> **Context:** SymptomLab PRD v2.1 (2026-06-12) · Module: SymptomLab · Section 4 — Objective · Parent document: PRD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

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
---

## Graph relations (explicit)

**PRD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**SymptomLab PRD** GATED_BY **KR1-KR6** (4-field DNA, 18-pair catalog, actionable errors, open vocab, no routing, no cross-lab imports)
