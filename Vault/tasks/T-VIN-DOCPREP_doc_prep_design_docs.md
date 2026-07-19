---
node_type: task
task_id: T-VIN-DOCPREP
status: pending
pack: VAULT
lab: vinlab
mode: architect/author + graph-tooling lane
blocked_by:
- T-VIN-DOCS-V2
consumers:
- graph/v2_docs — docs graph (prose graph waived; prep still feeds vault frontmatter)
- consumers.base — signal/noise audit view
- modules.base — module map view
tags:
- task
- vault
- vinlab
---

# T-VIN-DOCPREP — Doc-prep the six VINLab design docs for ingestion (`4dlab-doc-prep`)

**Status:** `pending` · **Pack:** VAULT (VINLab) · **Mode:** architect/author + graph-tooling lane (no lab inner-loop/gate)
**Origin:** pipeline guide §4 (doc prep) · **Blocked by:** T-VIN-DOCS-V2 (done — docs already v2)
**Consumer (signal/noise):** **Adds no schema field.** Explodes each monolithic design doc by header,
converts tables to entity blocks, and appends lineage-anchor + architectural-relation lines so the doc
relations become **EXTRACTED**. Even with the prose Pass-3 graph waived, these `ingest_ready/` chunks +
relation lines are what the vault frontmatter derivation reads — and each `CONSUMES`/`VERIFIES` line must
name a real, existing code path or sibling doc.

### Role note ###

`4dlab-doc-prep` writes to `graph/v2_docs/ingest_ready/<doc>/…` — it does **not** rewrite the source docs
and does **not** run graphify. Flow: `explode → tables → anchor → relations → verify`. Docs are
monolithic (unlike the pre-chunked wiki), hence the extra `explode`/`tables`/`anchor` steps.

### Scope — explicit file list (NOT a `docs/*.md` glob) ###

The **six design docs only**, in `labs/vinlab/docs/`:
`HLD_VINLab.md`, `DLD_VINLab.md`, `LLD_VINLab.md`, `ADR_VINLab.md`, `BDD_VINLab.md`, `PRD_VINLab.md`.

**Excluded** (exclusion discipline, guide §3·1D):
- `docs/VIN_VOCABULARY.md` — a vocabulary **duplicate** with its own `_vocabulary/` vault home
  (built in `T-VIN-VAULT` step 0 via `--vocab`). Never doc-prep it into the docs tier.
- Any handoff/inventory/superseded blueprint in `docs/` if present — ingest the explicit list above, not
  whatever else the folder holds.

### What to make explicit (real consumers only) ###

Append architectural-relation lines tying each doc section to its **named, existing** reader/implementer,
grep-confirmed:

- HLD/DLD module boundaries → `vinlab/decoder.py`, `models.py`, `overlay/*` (the shipped modules).
- LLD field/bound/enum rows → the `VinDNA` / `Emissions` / `AirMeteringArchitecture` dataclasses and the
  `StrEnum`s in `models.py`.
- BDD scenarios → the `tests/unit/` files that realise them (`VERIFIES` edges).
- The cross-lab emission/`rated_rpm`/`model` fields → their `DnaView` consumers (§5 of START_HERE).

### Success criteria ###

1. `4dlab-doc-prep explode → tables → anchor → relations → verify` run on the six-doc list; output under
   `graph/v2_docs/ingest_ready/<doc>/…`; source docs byte-unchanged.
2. `VIN_VOCABULARY.md` confirmed **excluded**; no `docs/*.md` glob used.
3. Every `CONSUMES`/`VERIFIES` line grep-backed to a real code path / test / sibling doc; proposals kept
   labelled; `verify` reports zero unflagged orphans.
4. No source-doc edit; no graphify; no schema field.

### Out of scope ###

- Running graphify / building `v2_docs` (prose Pass-3 **waived** this pack) · re-reconciling the docs
  (that was DOCS-V2, already done) · the vocabulary note (→ `T-VIN-VAULT` step 0).

### Files to touch ###

- `labs/vinlab/graph/v2_docs/ingest_ready/**` (generated chunks) — **not** the frozen `v2_current`/`v1_baseline`.
- The verify report appended to the progress note. Source `docs/*.md` are **read-only**.

### Verification ###

```bash
cd <repo>/4DLabV2
ls labs/vinlab/graph/v2_docs/ingest_ready/        # six doc dirs, no VIN_VOCABULARY
grep -rnE 'CONSUMES|VERIFIES' labs/vinlab/graph/v2_docs/ingest_ready/ | head -40
git status --porcelain labs/vinlab/docs labs/vinlab/graph/v2_current labs/vinlab/graph/v1_baseline \
  | grep . && echo "FAIL source/frozen touched" || echo "OK source+frozen untouched"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-VIN-DOCPREP.md` opens with the confirmed `## Plan` (the six-doc list +
exclusions); the run session fills `VERIFICATION GATE` (six docs exploded, vocab excluded, every
CONSUMES/VERIFIES grep-backed, zero unflagged orphans, source+frozen untouched) + `CODE REVIEW` (tables
converted, anchors + relations complete). Ledger row → `done` only when both are clean.
