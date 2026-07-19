
> **Context:** COMLab PRD v2.0 · Module: COMLab · Section: Preamble · Parent document: None
# COMLab Product Requirements Document (PRD)

**Document type:** PRD — what COMLab promises to the technician/user and how
that promise is shaped by the manual-input, petrol-only, no-hardware-pairing
operational context.

**Status:** v2.0 — **as-built**, reconciled to the shipped `comlab/` package
(2026-06-21). Supersedes the v1.0 draft (2026-05-21), archived at
`docs/ARCHIVE/COMLab_PRD_v1.0_2026-05-21.md`. Screen-6 commitments are reconciled
to the `OrchestratorFinalUIOutput` contract; UI-side screen behaviour remains a
front-end commitment.

**Scope (binding, per `wiki/04_horizon_eras.md`):** petrol **1990–2010, Euro
1–5**, manual-input, no hardware pairing. Post-2010 Euro 6+ technology —
secondary-air injection (SAI), GPF/DPF, LSPI, boost-era perks — is **out of
scope**: no SAI checkbox, no GPF/Boost quick-tags, no such fields in the payload.

**Companion to:** `COMLab_HLD.md` (architecture, binding), `COMLab_LLD.md`,
`COMLab_DLD.md`, `docs/adr/`, `COMLab_BDD.md`. This PRD inherits every
architectural decision from them and does not re-litigate them.

**Out of scope:**

- File-level class/method specifications — `COMLab_LLD.md`.
- Resource budgets, latency allocation, CI build script — `COMLab_DLD.md`.
- UI visual design / branding / typography; native-app vs PWA — front-end team.

**Authoritative inputs:**

- `COMLab_HLD.md` — architecture (binding).
- `wiki/` — domain truth (esp. `04_horizon_eras` scope; `10_differential_and_symptom_prior`).
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` — boundary protocol.
- The six v1.0 rulings, now settled in code and recorded in `docs/adr/`
  (siblings cap 5; KG per-family directory; `user_input_echo_audit` kept;
  filename kept; `lab_routing_directive` surfaced in `execution_meta`).

---


## Graph relations (explicit)

**COMLab_PRD.md** DESCRIBES **COMLab PRD v2.0**
**COMLab PRD v2.0** MIRRORS_CONTRACT_IN **COMLab HLD v2.0**
