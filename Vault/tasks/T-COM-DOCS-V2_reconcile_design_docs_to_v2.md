---
node_type: task
task_id: T-COM-DOCS-V2
status: done
pack: VAULT
lab: comlab
mode: architect/author lane
blocked_by: []
consumers:
- graph/v2_docs — docs graph (frontmatter source; prose graph waived this pack)
- COMLab design→code spine
tags:
- task
- vault
- comlab
---

# T-COM-DOCS-V2 — Reconcile the six design docs to the shipped v2 `comlab/` package

**Status:** `done` (verified at audit 2026-06-26) · **Pack:** VAULT (COMLab) · **Mode:** architect/author lane
**Origin:** pipeline guide §3·1D (PRD-refresh model) · **Blocked by:** —
**Load skills:** — (author lane; no inner-loop). **Consumer (signal/noise):** **Adds no schema field.** The
six v2 docs are the lineage spine `T-COM-DOCPREP` ingests; their `implements`/`consumers` derive from the
shipped code and named app-layer consumers.

### Why this ships `done` (audit finding 2026-06-26) ###

Unlike a fresh lab, COMLab's design docs were **already reconciled to the shipped package** during the
Stage-4 build close-out (all dated 2026-06-21, after the last `T-COMV2-*` code task). The audit confirmed:

- `COMLab_HLD.md`, `COMLab_DLD.md`, `COMLab_LLD.md`, `COMLab_PRD.md` — each headed
  **"v2.0 — as-built, reconciled to the shipped `comlab/` package."**
- `COMLab_BDD.md` — Status **Approved**, v1.0, **Code baseline: COMLab v2 as-built** (its first version,
  authored against v2 — a current peer, not a superseded draft).
- `docs/adr/` — a **living index of 11 Accepted records** (`ADR-0001 … ADR-0011`, 2026-06-21) covering the
  standing decisions (read-only fusion spine, no cross-lab imports, signal/noise, petrol 1990–2010 Euro 1–5,
  DNALab-resolves-horizon, registry-vs-atlas split, Brettschneider ground truth, emitters-emit-channels,
  two-point-delta, deterministic five-phase triage, surface routing directive).
- Superseded v1.0 drafts are in `docs/ARCHIVE/` (excluded from the docs tier).

So the six "HLD/DLD/LLD/ADR/BDD/PRD" design-doc peers are current v2 and complete. **No reconciliation work
remains** — this row exists so the chain is explicit and `T-COM-DOCPREP` has a named, satisfied blocker.

### If a later code-clean (A–D) changes a public surface ###

CODE-CLEAN is legibility-only (no behaviour/contract change), so the docs should stay accurate. If a
code-clean task nonetheless renames a public symbol the docs cite, record a one-line doc touch-up as an
architect out-of-band patch (in the COMLab build `PROGRESS.md` table) — **do not** reopen this row.

### Success criteria (met at audit) ###

1. Six design-doc peers exist and describe the shipped `comlab/` package (HLD/DLD/LLD/PRD v2.0 as-built;
   BDD v2-baselined; 11 ADR records Accepted). ✓
2. Superseded blueprints/duplicates excluded/archived (`docs/ARCHIVE/`). ✓
3. Petrol 1990–2010 Euro 1–5 scope holds; GPF/LSPI/SAI marked out of scope in PRD/HLD. ✓ (one wiki residual
   to confirm at WIKIPREP — START_HERE §5, not a docs issue).

### Out of scope ###

- Re-writing current docs · the `Vocabulary/` files (→ `_vocabulary/` tier in `T-COM-VAULT`) · doc-prep
  itself (→ `T-COM-DOCPREP`). **GRAPH GUARDRAIL:** no graphify.

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-DOCS-V2.md`: `## Plan` = "verify the six v2 docs at audit"; `VERIFICATION
GATE` = the audit checklist above (all ✓ 2026-06-26); `CODE REVIEW` = n/a (no code). Row is `done`.
