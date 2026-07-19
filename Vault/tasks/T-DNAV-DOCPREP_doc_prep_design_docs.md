---
node_type: task
task_id: T-DNAV-DOCPREP
status: pending
pack: VAULT
lab: dnalab
mode: architect/author + graph-tooling lane
blocked_by:
- T-DNAV-DOCS-V2
consumers:
- graph/v2_docs — docs graph (prose graph waived; prep still feeds vault frontmatter)
- consumers.base — signal/noise audit view
- modules.base — module map view
tags:
- task
- vault
- dnalab
---

# T-DNAV-DOCPREP — Doc-prep the six DNALab design docs for ingestion (`4dlab-doc-prep`)

**Status:** `pending` · **Pack:** VAULT (DNALab) · **Mode:** architect/author + graph-tooling lane (no lab inner-loop/gate)
**Origin:** pipeline guide §4 (doc prep) · **Blocked by:** T-DNAV-DOCS-V2 (done — docs already v2)
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

The **six design docs only**, in `labs/dnalab/docs/`:
`HLD_DNALab.md`, `DLD_DNALab.md`, `LLD_DNALab.md`, `ADR_DNALab.md`, `BDD_DNALab.md`, `PRD_DNALab.md`.

**Excluded** (exclusion discipline, guide §3·1D):
- `docs/DNA_VOCABULARY.md` — a vocabulary note with its own `_vocabulary/` vault home (built in
  `T-DNAV-VAULT` step 0 via `--vocab`). Never doc-prep it into the docs tier.
- Any handoff/inventory/superseded blueprint in `docs/` if present — ingest the explicit list above, not
  whatever else the folder holds.

### What to make explicit (real consumers only) ###

Append architectural-relation lines tying each doc section to its **named, existing** reader/implementer,
grep-confirmed:

- HLD/DLD module boundaries → `dnalab/assembly.py`, `dnalab/models.py` (the shipped composition modules).
- LLD field/bound rows → the `VehicleDNA` dataclass + `SCHEMA_VERSION` / `to_json_payload` /
  `from_json_payload` in `models.py`, and `build_vehicle_dna` in `assembly.py`.
- BDD scenarios → the `tests/unit/` cases that realise them (`VERIFIES` edges — `test_assembly.py`,
  `test_models.py`, `test_vehicledna_roundtrip.py`, `test_assembly_integration.py`).
- The envelope's downstream reader → COMLab `OrchestratorInboundRequest.vehicle_dna` (`T-DNA-7`).

> **Proposal discipline carries here too.** Where a doc section describes the operator-symptom prior, its
> consumer is the COMLab-A/B **proposal** — label such a relation line a proposal, do not write it as a
> live `CONSUMES` (mirror T-DNAV-WIKIPREP).

### Success criteria ###

1. `4dlab-doc-prep explode → tables → anchor → relations → verify` run on the six-doc list; output under
   `graph/v2_docs/ingest_ready/<doc>/…`; source docs byte-unchanged.
2. `DNA_VOCABULARY.md` confirmed **excluded**; no `docs/*.md` glob used.
3. Every `CONSUMES`/`VERIFIES` line grep-backed to a real code path / test / sibling doc; symptom-prior
   relations kept labelled proposals; `verify` reports zero *unflagged* orphans.
4. No source-doc edit; no graphify; no schema field.

### Out of scope ###

- Running graphify / building `v2_docs` (prose Pass-3 **waived** this pack) · re-reconciling the docs
  (that was DOCS-V2, already done) · the vocabulary note (→ `T-DNAV-VAULT` step 0).

### Files to touch ###

- `labs/dnalab/graph/v2_docs/ingest_ready/**` (generated chunks) — **not** the frozen `v2_current`/`v1_baseline`.
- The verify report appended to the progress note. Source `docs/*.md` are **read-only**.

### Verification ###

```bash
cd <repo>/4DLabV2
ls labs/dnalab/graph/v2_docs/ingest_ready/        # six doc dirs, no DNA_VOCABULARY
grep -rnE 'CONSUMES|VERIFIES' labs/dnalab/graph/v2_docs/ingest_ready/ | head -40
git status --porcelain labs/dnalab/docs labs/dnalab/graph/v2_current labs/dnalab/graph/v1_baseline \
  | grep . && echo "FAIL source/frozen touched" || echo "OK source+frozen untouched"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DNAV-DOCPREP.md` opens with the confirmed `## Plan` (the six-doc list +
exclusions); the run session fills `VERIFICATION GATE` (six docs exploded, vocab excluded, every
CONSUMES/VERIFIES grep-backed, symptom-prior kept proposal, zero unflagged orphans, source+frozen
untouched) + `CODE REVIEW` (tables converted, anchors + relations complete). Ledger row → `done` only when
both are clean.
