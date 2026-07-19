> **Context:** SymptomLab PRD v2.1 (2026-06-12) · Module: SymptomLab · Section 1 — Summary · Parent document: PRD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

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
---

## Graph relations (explicit)

**PRD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**SymptomLab** DESCRIBES **operator-symptom channel** (Part B DNA producer)
**symptomlab.resolve** DESCRIBES **single public entry point**
