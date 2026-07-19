
> **Context:** COMLab HLD v2.0 · Module: COMLab · Section: Preamble · Parent document: COMLab PRD v2.0
# COMLab High-Level Design (HLD)

**Document type:** HLD — architecture. Companion documents now all exist and are
binding: `COMLab_LLD.md` (file/class spec), `COMLab_DLD.md` (resource manifest +
ops), `COMLab_PRD.md` (wizard UX), `docs/adr/` (numbered decision records), and
`COMLab_BDD.md` (behavioural scenarios).

**Status:** v2.0 — **as-built**, reconciled to the shipped `comlab/` package
(2026-06-21). Supersedes the v1.0 draft (2026-05-21), archived at
`docs/ARCHIVE/COMLab_HLD_v1.0_2026-05-21.md`. The v1.0 "open questions for
sign-off" (§12) are all now resolved in code; §12 records the resolutions.

**What changed v1.0 → v2.0 (as-built reconciliation):**

- The Fault-Atlas KG ships as a **directory of 13 per-family JSON files** under
  `comlab/config/kg/` (plus `_kg_schema.json`), not a single file (resolves §12 Q2).
- Three modules the v1.0 draft did not name are now load-bearing:
  `core/perception_contradiction.py`, `core/ecu_hardware_checker.py`, and
  `analytics/delta_engine.py` (the two-operating-point Δ engine feeding the
  router's Phase 5).
- `execution_meta.lab_routing_directive` is **surfaced** in the outbound payload
  (resolves §12 Q6); `user_input_echo_audit` is **kept** COMLab-emitted
  (resolves §12 Q4).
- Observability is real: `comlab/observability/_tracer.py` provides an
  OpenTelemetry-or-no-op tracer; the router and aggregator open spans per stage.

**Authoritative inputs reconciled in this document:**

- `wiki/01_role_boundaries_fusion_spine.md` … `wiki/14_sources_appendices.md` —
  the COMLab domain wiki (canonical truth; code reconciles up to it).
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` — the binding JSON boundary protocol
  between the five labs.
- `docs/Vocabulary/OBD_VOCABULARY.md`, `docs/Vocabulary/DTC_VOCABULARY.md` —
  canonical identifiers, enums, ranges.
- `CROSS_LAB_DEPENDENCIES.md` — the forward registry of emitter→fusion pairs
  (DEP-1…DEP-10) that COMLab consumes in this final stage.
- The NewArch horizontal DNA-flow architecture (DNA reaches every lab on *input*,
  not after the fact) and its per-lab projection contract (`LabDnaView`).

**Non-goals of this HLD:**

- File-level class signatures and method bodies — `COMLab_LLD.md`.
- JSON schema files for `global_fault_registry.json` and the KG files — `COMLab_LLD.md` §8.
- Resource budgets, latency targets, deployment topology — `COMLab_DLD.md`.
- Wizard screen flow, plausibility error copy, UI gating decisions — `COMLab_PRD.md`.

---


## Graph relations (explicit)

**COMLab_HLD.md** DESCRIBES **COMLab HLD v2.0**
**COMLab HLD v2.0** MIRRORS_CONTRACT_IN **COMLab PRD v2.0**
**COMLab HLD v2.0** SUPERSEDES **COMLabDesign.md**
