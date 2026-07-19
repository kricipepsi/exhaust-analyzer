
> **Context:** COMLab DLD v2.0 · Module: COMLab · Section: Preamble · Parent document: COMLab HLD v2.0
# COMLab Detailed/Deployment Design (DLD)

**Document type:** DLD — runtime resource budgets, latency targets, boot
sequence, logging and observability strategy, build-validation CI script,
integration test harness shape, cross-version compatibility, deployment
model, failure-mode recovery.

**Status:** v2.0 — **as-built**, reconciled to the shipped `comlab/` package
(2026-06-21). Supersedes the v1.0 draft (2026-05-21), archived at
`docs/ARCHIVE/COMLab_DLD_v1.0_2026-05-21.md`. Resource budgets and latency
targets remain *commitments* (the operational envelope each release must hit),
not measured facts; module/config/observability details are reconciled to code.

**Scope (binding, per `wiki/04_horizon_eras.md`):** petrol **1990–2010, Euro
1–5**; post-2010 Euro 6+ tech (GPF/LSPI/SAI) out of scope.

**Companion to:** `COMLab_HLD.md` (binding architecture), `COMLab_LLD.md`
(binding file/class spec), `COMLab_PRD.md` (binding user-facing
commitments), `docs/adr/` (decisions). The DLD does not relitigate any decision
in those documents; it specifies the *operational envelope* every COMLab release
must hit and the CI machinery that proves it.

**Out of scope:**

- Class signatures and method contracts — `COMLab_LLD.md`.
- Wizard UX copy — `COMLab_PRD.md`.
- Architectural reconciliation with sibling labs — `COMLab_HLD.md` §11.
- Choice of cloud vendor / container orchestrator. The DLD specifies a
  resource envelope; how the surrounding 4DApp infrastructure provisions
  it is owned outside this lab.

**Authoritative inputs:**

- `COMLab_HLD.md` §4 (the four pipeline stages — they drive the latency
  allocation in §3).
- `COMLab_LLD.md` §6, §8, §9 (modules + config schemas + tests — they
  drive the boot sequence in §4 and the build-validation in §7).
- `COMLab_PRD.md` §7 (latency commitment to the user) and §8 (operational
  requirements) — bind §3 and §6.
- `docs/adr/` — the mandatory automated build-validation + two-reviewer ruling
  directly feeds §7; the other decisions flow through the HLD/LLD/PRD references
  above.

---


## Graph relations (explicit)

**COMLab_DLD.md** DESCRIBES **COMLab DLD v2.0**
**COMLab DLD v2.0** MIRRORS_CONTRACT_IN **COMLab HLD v2.0**
