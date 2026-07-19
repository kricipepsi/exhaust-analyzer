> **Context:** DNALab PRD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: Section · Parent document: PRD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Section 3 — Background

**Context.** The 4D engine wants the symptom/identity prior as a single packet: the
physical hardware (from the VIN) and the operator's complaint (from triage), stamped with
a session id and timestamp so the orchestrator can correlate it with the rest of the
pipeline. Assembling these in the UI or in COMLab would scatter the composition logic and
the schema-version contract.

**Why now.** With VINLab and SymptomLab split into independent sibling modules
(T-RM-2-DNA), there needs to be exactly one place that knows how to call both and join
their outputs under the §4.3 contract. DNALab is that place — a thin, deterministic
orchestrator with a versioned envelope.

**What recently became possible.** Both producers expose clean, typed APIs
(`vinlab.decode`, `symptomlab.resolve`) and JSON round-trip (`to_json`/`from_json`).
DNALab composes them, delegating serialization to each model so the umbrella never
duplicates field knowledge. The `schema_version` field makes the combined payload
self-describing for COMLab.

---

## Graph relations (explicit)

**VehicleDNA** DESCRIBES **single packet joining physical identity + operator complaint**
**dnalab** DESCRIBES **thin, deterministic orchestrator with versioned envelope**
**vinlab.decode() + symptomlab.resolve()** DESCRIBES **clean, typed producer APIs**
