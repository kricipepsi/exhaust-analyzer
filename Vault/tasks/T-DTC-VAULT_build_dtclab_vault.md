---
node_type: task
task_id: T-DTC-VAULT
status: pending
pack: VAULT
lab: dtclab
mode: architect/author + vault-tooling lane
blocked_by:
- T-DTC-GRAPH-AST
- T-DTC-PATHS-1
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- drift-guards.base — coverage view
- modules.base — module map view
- graph/v2_code — AST code graph
- graph/v2_tests — AST test graph
- graph/v2_docs — docs graph
- graph/v2_wiki — wiki graph
- COMLab analytics / fault-atlas routing
implements:
- graph/v2_docs/graph.json
- graph/v2_code/graph.json
- graph/v2_tests/graph.json
- vault-map.dtclab.yaml
- vault-map.gaslab.yaml
tags:
- task
- vault
- dtclab
---

# T-DTC-VAULT — Author `vault-map.dtclab.yaml`, dry-run, build, and install the DTCLab vault tier

**Status:** `pending` · **Pack:** VAULT (DTCLab) · **Mode:** architect/author + vault-tooling lane (no lab inner-loop/gate)
**Origin:** pipeline guide §6 (Phase 4) + plan §6 · **Blocked by:** T-DTC-GRAPH-AST, T-DTC-PATHS-1
**Consumer (signal/noise):** **The `consumers` field is the signal/noise gate itself.** Each framed
DTCLab note ships only with a **named, existing** downstream consumer (a code path, a sibling design doc,
or a COMLab analytic). The three `.base` views are the live readers: `modules.base` (groups by
`lab`→`module`), `consumers.base` (the signal/noise audit — every note must have ≥1 named consumer),
`drift-guards.base` (every `implements` target has ≥1 guarding test or is marked untested). **An empty
`consumers` list = the note is not ready to ship.**

### Role note ###

`build_lab_vault.py` is vault tooling — no `dtclab/` inner-loop/gate. The vault is a **read-mostly
window**: it copies prepared lab sources and checks the required graph tiers without re-extracting them.
For DTCLab, "skip graph testing" means `graph/v2_code/` and `graph/v2_tests/` are required, while
`graph/v2_wiki/` and `graph/v2_docs/graph.json` are **not** (prose graphs waived). Authoring
`vault-map.dtclab.yaml` is the architect-named consumer step; `consumers` is **never** auto-derived.

### Prerequisite path fix ###

This task assumes **T-DTC-PATHS-1 is `done`**, so the build resolves DTCLab's `wiki/` + two-tier graph.
If `--dry-run --lab dtclab` still aborts on a hardcoded `research/chunks` / `v2_wiki` / `v2_docs` path,
stop and route back to T-DTC-PATHS-1 — do not patch the script inside this task.

### Steps (plan §6 / guide §6) ###

0. `_vocabulary/` — build `Vault/_vocabulary/DTC_VOCABULARY.md` from canonical (`--vocab` path), if not
   already present, with §-anchored frontmatter + named consumers (mirror OBDLab `T-VAULT-VOCAB-1` /
   GASLab). `docs/DTC_VOCABULARY.md` is the vocab source and is **excluded** from the docs tier (see
   `T-DTC-DOCPREP`).
1. Confirm eligibility (Phase 0): `labs/dtclab/dtclab/`, `tests/`, `wiki/`, `docs/`, plus
   `graph/v2_code/graph.json` and `graph/v2_tests/graph.json` present. Prose graphs are owner-waived.
2. **Author `assets/vault-map.dtclab.yaml`** — `lab: dtclab`, `module: …`, a `frame:` block per framed
   note, and a `plain:` list for un-framed copies. Model exactly on `vault-map.gaslab.yaml`.
3. `build_lab_vault.py --lab dtclab --repo <repo>/4DLabV2 --dry-run` → review the copy/inject plan.
4. Drop `--dry-run` → copies `code/`, `tests/`, `wiki/`, `docs/` into `Vault/labs/dtclab/`, injects
   frontmatter skeletons, fills semantic fields from the map, writes the lab landing note.
5. Copy the three `.base` views into `Vault/_bases/` (if not shared already); refresh `System-Map.md`
   + `_meta/PROVENANCE.md` with the DTC provenance.
6. Open `Vault/` in Obsidian; confirm the three Bases render and `orphans` / `unresolved` are empty or
   explained.

### Consumer evidence to use (name real readers, not invented ones) ###

Use the named COMLab/Wired consumers already pinned in the v2 design docs — confirm each by grep before
framing a note on it:

- `routing_tags` → COMLab `fault_atlas_router` (+ `POA_HISTORY` injection, T-FX-3).
- `mode_06_monitors` → COMLab aggregator scoring via `DTC_CONFIDENCE_WEIGHTS`.
- `historical_fault_context`, `freeze_frame` → COMLab fault ranking / OBDLab PID forwarding.
- `classify_top3()` `(family, confidence)` → COMLab Bayesian `combine()` (FU-1) via the Wired adapter
  `T-DTW-1`.

> **Do NOT frame** a note whose only "consumer" would be a **proposal** (`EP-DTC-NOSTART-1`, or the
> `wiki/11_proposals_register.md` P-DTC-1/2/3 slate). A proposal is not a live consumer — leave such a
> note `plain:` or keep the field labelled a proposal; do not fabricate a consumer to make it frame.

### Success criteria (plan §7) ###

1. `Vault/labs/dtclab/` shows `code/`, `tests/`, `wiki/`, `docs/` and a working graph view in Obsidian.
2. All three `.base` views render with DTC rows: modules grouped; **every framed note has ≥1 named
   consumer**; every `implements` target has ≥1 `drift_guard` or is explicitly marked untested.
3. **Consumer completeness:** no framed DTC note ships with an empty `consumers` list; no proposal is
   framed as a live consumer.
4. **No `graph.json` re-extraction** was run; existing `graph/v2_code`, `graph/v2_tests`,
   `graph/v2_current`, `graph/v1_baseline` byte-unchanged.
5. `build_lab_vault.py` is idempotent and dry-run-safe (re-run updates in place, never duplicates).

### Out of scope ###

- Building any other lab's vault tier · re-graphifying any corpus · auto-deriving `consumers`.
- The Pass-3 graph cross-check (skipped for this pack) · the GPF out-of-era decision (START_HERE §5).

### Files to touch ###

- `_skills/graph/4dlab-vault/assets/vault-map.dtclab.yaml` (new — the architect consumer map).
- `Vault/labs/dtclab/…` (generated), `Vault/_vocabulary/DTC_VOCABULARY.md`, `Vault/_bases/*` (if not
  shared), `Vault/System-Map.md`, `Vault/_meta/PROVENANCE.md`.

### Verification ###

```bash
cd <repo>/4DLabV2
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab dtclab --repo "$PWD" --dry-run | head -50
# every framed note must carry a non-empty consumers list:
grep -A3 'node_type' Vault/labs/dtclab/wiki/*.md Vault/labs/dtclab/docs/*.md | grep -c 'consumers'
git status --porcelain labs/dtclab/graph | grep . && echo "FAIL graph touched" || echo "OK graph untouched"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-VAULT.md` opens with the confirmed `## Plan` (the framed-note roster +
each note's named consumer); the run session fills `VERIFICATION GATE` (Bases render, every framed note
≥1 consumer, no empty list, no proposal framed, no re-extraction, idempotent) + `CODE REVIEW` (map
authored against Phase-2 prose prep plus code/test graphs, consumers all named/grep-backed,
orphans/unresolved empty or explained). Ledger row → `done` only when both blocks are clean — this closes
the DTCLab vault pack.
