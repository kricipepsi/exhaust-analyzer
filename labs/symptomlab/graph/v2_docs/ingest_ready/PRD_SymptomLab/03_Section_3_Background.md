> **Context:** SymptomLab PRD v2.1 (2026-06-12) · Module: SymptomLab · Section 3 — Background · Parent document: PRD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

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
---

## Graph relations (explicit)

**PRD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**allowed_combinations.yaml** DERIVED_FROM **VehicleDNA.md triage diagram**
