> **Context:** SymptomLab PRD v2.1 (2026-06-12) · Module: SymptomLab · Section 6 — Value Proposition · Parent document: PRD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

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
---

## Graph relations (explicit)

**PRD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
