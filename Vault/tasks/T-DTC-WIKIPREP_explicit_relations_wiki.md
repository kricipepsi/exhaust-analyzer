---
node_type: task
task_id: T-DTC-WIKIPREP
status: done
pack: VAULT
lab: dtclab
mode: architect/author lane
blocked_by: []
consumers:
- COMLab analytics / fault-atlas routing
tags:
- task
- vault
- dtclab
---

# T-DTC-WIKIPREP — Make wiki relations explicit (`4dlab-wiki-prep` on `labs/dtclab/wiki/`)

**Status:** `done` · **Pack:** VAULT (DTCLab) · **Mode:** architect/author lane (graph-tooling; no lab inner-loop)
**Origin:** pipeline guide §4 (wiki prep) · **Blocked by:** — (wiki is current as of 2026-06-11)
**Consumer (signal/noise):** **Adds no schema field.** Appends append-only trailer blocks that make
implied wiki relations **explicit** so graphify (were the prose graph built) tags edges `EXTRACTED`.
Even with the prose graph waived this pack, the explicit `CONSUMES`/`VERIFIES` lines are the
signal/noise audit surface the vault docs/wiki frontmatter leans on — every such line must name a
**real, existing** COMLab/fault-atlas code path or test. No new fields.

### Role note ###

`4dlab-wiki-prep` runs `relations → labels → roster → verify`. It is **append-only** (trailer blocks +
canonical entity labels); it does **not** move or rename `wiki/` — that folder is graph-canonical at its
source. It never writes `graph.json` and never runs graphify.

### Scope ###

- `labs/dtclab/wiki/` — 13 chunks: `00_INDEX.md` + `01_dtc_state_lifecycle` … `12_ranking_discriminator`,
  including `11_proposals_register.md`.
- Make each implied `<DTC range> → <routing tag>`, `<tag> → <canonical family>`, and
  `<field> CONSUMED-BY <COMLab path>` relation explicit as `**SUBJECT** PREDICATE **OBJECT**` lines.

### Signal/noise at the edge (critical) ###

- Every `CONSUMES`/`VERIFIES` line must name a real, existing code path or test. Orphans are flagged,
  not shipped.
- **Proposals stay labelled proposals.** `11_proposals_register.md` (P-DTC-1/2/3) and the
  `EP-DTC-NOSTART-1` no-start proposal must remain marked `PROPOSAL` — never promoted to a live
  `CONSUMES` edge. The register's own discipline (§11 header) is authoritative.
- `POA_HISTORY` relations must show it as **COMLab-injected** (T-FX-3), never emitted by DTCLab.

### Success criteria ###

1. `4dlab-wiki-prep relations → labels → roster → verify` run over all 13 chunks; trailer blocks appended.
2. Every appended `CONSUMES`/`VERIFIES` names an existing code path/test; **zero orphans** (or each
   orphan explicitly routed back as a prep gap, not patched).
3. Proposals remain labelled; no proposal token appears as a live consumer edge.
4. Canonical entity labels consistent across chunks (e.g. `DTCRoutingTag`, `Mode06MonitorState`,
   `DtcLabDnaView`); `verify` step clean.
5. Source files unmoved/unrenamed; diffs are append-only trailer blocks.

### Out of scope ###

- Running graphify (prose Pass-3 is **waived** this pack) · editing `DTC_VOCABULARY.md` (docs/vocab tier).
- Promoting any proposal to live · the GPF out-of-era decision (START_HERE §5).

### Files to touch ###

- `labs/dtclab/wiki/*.md` — append-only relation/label trailer blocks (skill convention).

### Verification ###

```bash
cd <repo>/labs/dtclab
grep -rln 'PROPOSAL' wiki/ | head        # proposals still labelled
grep -rn 'CONSUMES\|VERIFIES' wiki/ | wc -l   # explicit relation lines appended
# spot-check a sample of appended CONSUMES targets resolve to a real dtclab/ or comlab path
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-WIKIPREP.md` opens with the confirmed `## Plan` (chunk roster); the run
session fills `VERIFICATION GATE` (all chunks prepped, zero orphans, proposals labelled) + `CODE REVIEW`
(relation counts, label consistency). Ledger row → `done` only when the block is clean.
