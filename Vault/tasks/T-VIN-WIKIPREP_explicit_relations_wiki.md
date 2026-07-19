---
node_type: task
task_id: T-VIN-WIKIPREP
status: done
pack: VAULT
lab: vinlab
mode: architect/author + graph-tooling lane
blocked_by: []
consumers:
- graph/v2_wiki — wiki graph (prose graph waived; prep still feeds vault frontmatter)
- consumers.base — signal/noise audit view
- COMLab analytics / fault-atlas routing
tags:
- task
- vault
- vinlab
---

# T-VIN-WIKIPREP — Make wiki relations explicit for ingestion (`4dlab-wiki-prep`)

**Status:** `done` · **Pack:** VAULT (VINLab) · **Mode:** architect/author + graph-tooling lane (append-only prose prep; no lab inner-loop/gate)
**Origin:** pipeline guide §4 (wiki prep) · **Blocked by:** — (wiki is current at source)
**Consumer (signal/noise):** **Adds no schema field.** Appends explicit `**SUBJECT** PREDICATE **OBJECT**`
relation lines + canonical entity labels so implied links become **EXTRACTED** facts. Even with the
prose Pass-3 graph waived for this pack, the explicit `CONSUMES`/`VERIFIES` trailers are the source the
vault frontmatter derivation reads — and the signal/noise gate at the edge: **every `CONSUMES`/`VERIFIES`
line must name a real, existing code path or test.**

### Role note ###

`4dlab-wiki-prep` is **append-only** — it adds trailer blocks to the chunk files, never rewrites or moves
them. Do **not** rename or relocate `wiki/` (graph-canonical at its source). The skill never writes
`graph.json` and never runs graphify. Flow: `relations → labels → roster → verify`.

### Scope ###

- `labs/vinlab/wiki/` — 4 chunks: `00_index.md`, `10_decode_scope_rules.md`, `11_engine_resolution.md`,
  `12_brand_cylinder_rules.md`.

### What to make explicit (real consumers only) ###

Append `**SUBJECT** PREDICATE **OBJECT**` lines that the chunk text already implies, tying each VINLab
concept to its **named, existing** downstream reader. Confirm each by grep before writing the line:

- decode-scope / petrol-only reject (`10_decode_scope_rules.md`) → `RobustVINDecoder._is_non_petrol`
  reject path.
- euro → horizon and `rated_rpm` (`11_engine_resolution.md`) → `euro_to_horizon`; `rated_rpm` →
  `ObdLabDnaView.rated_rpm` (OBDLab RPM ceiling, `T-DNA-3`).
- brand cylinder rules (`12_brand_cylinder_rules.md`) → `overlay/cylinder_heuristic.infer_cylinder`
  fallback chain.

> **Proposals stay proposals.** The `fuel_type` E5/E10 blend item (gaslab wiki §1.4, `T-DNA-6`) is a
> proposal — if it appears, label its line a proposal; **never** write it as a live `CONSUMES`. Orphans
> (a relation naming no existing code path) are flagged by the skill, not shipped.

### Success criteria ###

1. `4dlab-wiki-prep relations → labels → roster → verify` run over the 4 chunks; append-only trailers
   added; chunk bodies above the trailer byte-unchanged.
2. Every `CONSUMES`/`VERIFIES` line names a real code path/test (grep-confirmed); proposals labelled as
   proposals; the skill's `verify` step reports zero unflagged orphans.
3. Canonical entity labels assigned (so the same concept isn't two nodes); a roster of entities produced.
4. No file moved/renamed; no graphify; no schema field.

### Out of scope ###

- Running graphify / building `v2_wiki` (prose Pass-3 **waived** this pack) · editing code or docs.
- Promoting any proposal to a live consumer.

### Files to touch ###

- `labs/vinlab/wiki/*.md` — append-only relation/label trailers only.
- The roster + verify report appended to the progress note.

### Verification ###

```bash
cd <repo>/4DLabV2
# every appended CONSUMES/VERIFIES target must exist in code/tests:
grep -rnE 'CONSUMES|VERIFIES' labs/vinlab/wiki/ | head -40
# spot-check a named symbol resolves:
grep -rn 'def infer_cylinder\|def euro_to_horizon\|_is_non_petrol' labs/vinlab/vinlab/
```

### Progress hook ###

`Vault/tasks/progress_notes/T-VIN-WIKIPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (append-only confirmed, relation count, every CONSUMES/VERIFIES grep-backed, proposals
kept as proposals, zero unflagged orphans) + `CODE REVIEW` (labels canonical, roster complete). Ledger row
→ `done` only when both are clean.
