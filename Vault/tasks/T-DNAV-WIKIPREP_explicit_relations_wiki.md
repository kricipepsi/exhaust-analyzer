---
node_type: task
task_id: T-DNAV-WIKIPREP
status: pending
pack: VAULT
lab: dnalab
mode: architect/author + graph-tooling lane
blocked_by: []
consumers:
- graph/v2_wiki — wiki graph (prose graph waived; prep still feeds vault frontmatter)
- consumers.base — signal/noise audit view
- COMLab analytics / fault-atlas routing
tags:
- task
- vault
- dnalab
---

# T-DNAV-WIKIPREP — Make wiki relations explicit for ingestion (`4dlab-wiki-prep`)

**Status:** `pending` · **Pack:** VAULT (DNALab) · **Mode:** architect/author + graph-tooling lane (append-only prose prep; no lab inner-loop/gate)
**Origin:** pipeline guide §4 (wiki prep) · **Blocked by:** — (wiki is current at source)
**Consumer (signal/noise):** **Adds no schema field.** Appends explicit `**SUBJECT** PREDICATE **OBJECT**`
relation lines + canonical entity labels so implied links become **EXTRACTED** facts. Even with the prose
Pass-3 graph waived for this pack, the explicit `CONSUMES`/`VERIFIES` trailers are the source the vault
frontmatter derivation reads — and the signal/noise gate at the edge: **every `CONSUMES`/`VERIFIES` line
must name a real, existing code path or test.**

### Role note ###

`4dlab-wiki-prep` is **append-only** — it adds trailer blocks to the note files, never rewrites or moves
them. Do **not** rename or relocate `wiki/` (graph-canonical at its source). The skill never writes
`graph.json` and never runs graphify. Flow: `relations → labels → roster → verify`.

### Scope — 10 notes, MIXED TYPE (the crux of this task) ###

`labs/dnalab/wiki/` holds two distinct kinds of note. Treat them differently — this split is *why* the
prose graph is waived (START_HERE §0.4):

```
CONTRACT SPEC (live consumers — frame normally):
  10_vehicle_dna_envelope.md   → VehicleDNA envelope → COMLab OrchestratorInboundRequest.vehicle_dna (T-DNA-7)
  11_schema_versioning.md      → SCHEMA_VERSION "1.2" + VehicleDNA.from_json_payload mismatch raise
  12_assembly_contract.md      → assembly.build_vehicle_dna(vin, triage); load_state/engine_state triage keys (T-DNA-2)
  13_session_identity.md       → VehicleDNA.new() session_id / timestamp fields
  00_index.md                  → index/roster note (labels only, few relations)

RESEARCH PROSE (consumer = COMLab-A/B symptom prior — still a PROPOSAL):
  90_research_index.md             92_symptom_vocabulary_and_context.md
  91_operator_symptom_predictiveness.md   93_vin_decode_resolution.md   94_reference_data_and_aftermarket.md
```

### What to make explicit (real consumers only) ###

For the **contract notes (10–13, 00)**, append `**SUBJECT** PREDICATE **OBJECT**` lines tying each concept
to its **named, existing** reader. Confirm each by grep before writing the line:

- `10_vehicle_dna_envelope` → `VehicleDNA` (`dnalab/models.py`) CONSUMED-BY COMLab
  `OrchestratorInboundRequest.vehicle_dna` (`T-DNA-7`).
- `11_schema_versioning` → `SCHEMA_VERSION` + `VehicleDNA.from_json_payload` mismatch raise (the
  compatibility gate).
- `12_assembly_contract` → `build_vehicle_dna` triage required keys (`load_state`/`engine_state`,
  `T-DNA-2`); `engine_state` → COMLab `symptom_router.route_symptom` (`T-DNA-10`, live).

> **PROPOSALS STAY PROPOSALS — this is the DNALab-specific trap.** For the **research notes (90–94)**, the
> only downstream reader is the COMLab-A/B symptom-prior, which is **not live — it is a proposal**
> (`labs/comlab/comlab/config/proposals/`). Any relation line you append for these notes must be **labelled
> a proposal**, never written as a live `CONSUMES`. The skill's `verify` step flags an orphan if a line
> names no existing code path — for 90–94 that is the *expected* state until COMLab-A/B ship live (the
> prose-graph lift trigger, START_HERE §6). Do **not** fabricate a live consumer to make these notes frame.

### Success criteria ###

1. `4dlab-wiki-prep relations → labels → roster → verify` run over the 10 notes; append-only trailers
   added; note bodies above the trailer byte-unchanged.
2. Contract notes (10–13): every `CONSUMES`/`VERIFIES` line names a real code path/test (grep-confirmed).
3. Research notes (90–94): every prior/predictiveness relation is **labelled a proposal** (COMLab-A/B),
   none framed as a live consumer; the `verify` step's orphan flags on these are recorded as *expected*.
4. Canonical entity labels assigned (so the same concept isn't two nodes); a roster of entities produced.
5. No file moved/renamed; no graphify; no schema field.

### Out of scope ###

- Running graphify / building `v2_wiki` (prose Pass-3 **waived** this pack) · editing code or docs.
- Promoting any COMLab-A/B prior to a live consumer · adding `oil_consumption`/`T-OIL-1` content (separate pack).

### Files to touch ###

- `labs/dnalab/wiki/*.md` — append-only relation/label trailers only.
- The roster + verify report appended to the progress note.

### Verification ###

```bash
cd <repo>/4DLabV2
# contract-note CONSUMES/VERIFIES targets must resolve in code:
grep -rnE 'CONSUMES|VERIFIES' labs/dnalab/wiki/1[0-3]_*.md labs/dnalab/wiki/00_*.md | head -40
grep -rn 'def build_vehicle_dna\|class VehicleDNA\|SCHEMA_VERSION\|def from_json_payload' labs/dnalab/dnalab/
# research-note lines must read as PROPOSAL, not live CONSUMES:
grep -rniE 'proposal' labs/dnalab/wiki/9[0-4]_*.md | head -20
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DNAV-WIKIPREP.md` opens with the confirmed `## Plan` (the 10-note split +
which notes frame live vs proposal); the run session fills `VERIFICATION GATE` (append-only confirmed,
relation count, contract-note CONSUMES/VERIFIES grep-backed, research-note priors kept as proposals,
orphan flags on 90–94 recorded as expected) + `CODE REVIEW` (labels canonical, roster complete). Ledger
row → `done` only when both are clean.
