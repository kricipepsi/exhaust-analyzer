---
node_type: task
task_id: T-DNAV-VAULT
status: done
pack: VAULT
lab: dnalab
mode: architect/author + vault-tooling lane
blocked_by:
- T-DNAV-GRAPH-AST
- T-DNAV-PATHS-1
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- drift-guards.base — coverage view
- modules.base — module map view
- graph/v2_code — AST code graph
- graph/v2_tests — AST test graph
- COMLab analytics / fault-atlas routing
implements:
- graph/v2_code/graph.json
- graph/v2_tests/graph.json
- vault-map.dnalab.yaml
tags:
- task
- vault
- dnalab
---

# T-DNAV-VAULT — Author `vault-map.dnalab.yaml`, dry-run, build, and install the DNALab vault tier

**Status:** `pending` · **Pack:** VAULT (DNALab) · **Mode:** architect/author + vault-tooling lane (no lab inner-loop/gate)
**Origin:** pipeline guide §6 (Phase 4) · **Blocked by:** T-DNAV-GRAPH-AST, T-DNAV-PATHS-1
**Consumer (signal/noise):** **The `consumers` field is the signal/noise gate itself.** Each framed
DNALab note ships only with a **named, existing** downstream consumer (a code path, a sibling design doc,
or a COMLab/DnaView analytic). The three `.base` views are the live readers: `modules.base` (groups by
`lab`→`module`), `consumers.base` (the signal/noise audit — every note must have ≥1 named consumer),
`drift-guards.base` (every `implements` target has ≥1 guarding test or is marked untested). **An empty
`consumers` list = the note is not ready to ship.**

### Role note ###

`build_lab_vault.py` is vault tooling — no `dnalab/` inner-loop/gate. The vault is a **read-mostly
window**: it copies prepared lab sources and checks the required graph tiers without re-extracting them.
For DNALab, "skip graph testing" means `graph/v2_code/` and `graph/v2_tests/` are required, while
`graph/v2_wiki/` and `graph/v2_docs/graph.json` are **not** (prose graphs waived). Authoring
`vault-map.dnalab.yaml` is the architect-named consumer step; `consumers` is **never** auto-derived.

### Prerequisite path fix ###

This task assumes **T-DNAV-PATHS-1 is `done`**, so the build resolves DNALab's `wiki/` + two-tier graph.
If `--dry-run --lab dnalab` still aborts on a hardcoded `research/chunks` / `v2_wiki` / `v2_docs` path,
stop and route back to T-DNAV-PATHS-1 — do not patch the script inside this task.

### Steps (guide §6) ###

0. `_vocabulary/` — build `Vault/_vocabulary/DNA_VOCABULARY.md` from canonical (`--vocab` path), if not
   already present, with §-anchored frontmatter + named consumers (mirror OBDLab `T-VAULT-VOCAB-1` /
   GASLab / DTCLab). `docs/DNA_VOCABULARY.md` is the vocab source and is **excluded** from the docs tier
   (see `T-DNAV-DOCPREP`).
1. Confirm eligibility (Phase 0): `labs/dnalab/dnalab/`, `tests/`, `wiki/`, `docs/`, plus
   `graph/v2_code/graph.json` and `graph/v2_tests/graph.json` present. Prose graphs are owner-waived.
2. **Author `assets/vault-map.dnalab.yaml`** — `lab: dnalab`, `module: …`, a `frame:` block per framed
   note, and a `plain:` list for un-framed copies. Model exactly on `vault-map.gaslab.yaml` /
   `vault-map.dtclab.yaml`. **Frame the contract notes; leave the research-prose notes (90–94) `plain:`**
   — their only consumer is the COMLab-A/B proposal (see below), so they are not ready to frame as live.
3. `build_lab_vault.py --lab dnalab --repo <repo>/4DLabV2 --dry-run` → review the copy/inject plan.
4. Drop `--dry-run` → copies `code/`, `tests/`, `wiki/`, `docs/` into `Vault/labs/dnalab/`, injects
   frontmatter skeletons, fills semantic fields from the map, writes the lab landing note.
5. Copy the three `.base` views into `Vault/_bases/` (if not shared already); refresh `System-Map.md`
   + `_meta/PROVENANCE.md` with the DNA provenance.
6. Open `Vault/` in Obsidian; confirm the three Bases render and `orphans` / `unresolved` are empty or
   explained.

### Consumer evidence to use (name real readers, not invented ones) ###

DNALab's contract surface is the `VehicleDNA` envelope, read downstream by COMLab. Confirm each by grep
before framing a note on it:

- `VehicleDNA` envelope → COMLab `OrchestratorInboundRequest.vehicle_dna` ingestion (`T-DNA-7`).
- `SCHEMA_VERSION` / `from_json_payload` mismatch raise → COMLab ingestion compatibility gate.
- `load_state` / `engine_state` triage keys → `assembly.build_vehicle_dna` (`T-DNA-2`); `engine_state` →
  COMLab `symptom_router.route_symptom` (`T-DNA-10`, live).
- Composed `VinDNA` sub-payload → VINLab `DnaView` mirrors (rated_rpm/CoC/model).

> **Do NOT frame** a note whose only "consumer" would be the COMLab-A/B symptom-prior **proposal**
> (the research-prose wiki half, 90–94). A proposal is not a live consumer — leave such a note `plain:`
> or keep the field labelled a proposal; do not fabricate a consumer to make it frame.

### Success criteria ###

1. `Vault/labs/dnalab/` shows `code/`, `tests/`, `wiki/`, `docs/` and a working graph view in Obsidian.
2. All three `.base` views render with DNA rows: modules grouped; **every framed note has ≥1 named
   consumer**; every `implements` target has ≥1 `drift_guard` or is explicitly marked untested.
3. **Consumer completeness:** no framed DNA note ships with an empty `consumers` list; the research-prose
   notes (90–94) are `plain:` (not framed as live) because their only reader is the COMLab-A/B proposal.
4. **No `graph.json` re-extraction** was run; existing `graph/v2_code`, `graph/v2_tests`,
   `graph/v2_current`, `graph/v1_baseline` byte-unchanged.
5. `build_lab_vault.py` is idempotent and dry-run-safe (re-run updates in place, never duplicates).

### Out of scope ###

- Building any other lab's vault tier · re-graphifying any corpus · auto-deriving `consumers`.
- The Pass-3 graph cross-check (skipped for this pack) · promoting the COMLab-A/B prior proposal.

### Files to touch ###

- `_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml` (new — the architect consumer map).
- `Vault/labs/dnalab/…` (generated), `Vault/_vocabulary/DNA_VOCABULARY.md`, `Vault/_bases/*` (if not
  shared), `Vault/System-Map.md`, `Vault/_meta/PROVENANCE.md`.

### Verification ###

```bash
cd <repo>/4DLabV2
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab dnalab --repo "$PWD" --dry-run | head -50
# every framed note must carry a non-empty consumers list:
grep -A3 'node_type' Vault/labs/dnalab/wiki/*.md Vault/labs/dnalab/docs/*.md | grep -c 'consumers'
git status --porcelain labs/dnalab/graph | grep . && echo "FAIL graph touched" || echo "OK graph untouched"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DNAV-VAULT.md` opens with the confirmed `## Plan` (the framed-note roster +
each note's named consumer, and the 90–94 `plain:` decision); the run session fills `VERIFICATION GATE`
(Bases render, every framed note ≥1 consumer, no empty list, no proposal framed, no re-extraction,
idempotent) + `CODE REVIEW` (map authored against Phase-2 prose prep plus code/test graphs, consumers all
named/grep-backed, orphans/unresolved empty or explained). Ledger row → `done` only when both blocks are
clean — this closes the DNALab vault pack.
