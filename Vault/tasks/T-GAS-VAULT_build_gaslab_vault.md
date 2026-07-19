---
node_type: task
task_id: T-GAS-VAULT
status: done
pack: VAULT
lab: gaslab
mode: architect/author + vault-tooling lane
blocked_by:
- T-GAS-GRAPH-AST
- T-GAS-PATHS-1
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
- vault-map.gaslab.yaml
- vault-map.obdlab.yaml
tags:
- task
- vault
- gaslab
---

# T-GAS-VAULT — Author `vault-map.gaslab.yaml`, dry-run, build, and install the GASLab vault tier

**Status:** `done` · **Pack:** VAULT (GASLab) · **Mode:** architect/author + vault-tooling lane (no lab inner-loop/gate)
**Origin:** pipeline guide §6 (Phase 4) + plan §6 · **Blocked by:** T-GAS-GRAPH-AST, T-GAS-PATHS-1
**Consumer (signal/noise):** **The `consumers` field is the signal/noise gate itself.** Each framed
GASLab note ships only with a **named, existing** downstream consumer (a code path, a sibling design
doc, or a COMLab analytic). The three `.base` views are the live readers: `modules.base` (groups by
`lab`→`module`), `consumers.base` (the signal/noise audit — every note must have ≥1 named consumer),
`drift-guards.base` (every `implements` target has ≥1 guarding test or is marked untested). **An empty
`consumers` list = the note is not ready to ship** (plan §4).

### Role note ###

`build_lab_vault.py` is vault tooling (plan §5) — no `gaslab/` inner-loop/gate. The vault is a
**read-mostly window**: it copies prepared lab sources and checks the required graph tiers without
re-extracting them. For GASLab, owner direction on 2026-06-11 waived prose Pass-3; `graph/v2_code/`
and `graph/v2_tests/` are required, while `graph/v2_wiki/` and `graph/v2_docs/graph.json` are not.
Authoring `vault-map.gaslab.yaml` is the architect-named consumer step;
`consumers` is **never** auto-derived from the graph.

### Prerequisite path fix ###

This task assumes **T-GAS-PATHS-1 is `done`**, so the build resolves GAS's `wiki/` + four-tier graph.
If `--dry-run --lab gaslab` still aborts on a hardcoded `research/chunks` / `graphify-out` path, stop
and route back to T-GAS-PATHS-1 — do not patch the script inside this task.

### Steps (plan §6 / guide §6) ###

0. `_vocabulary/` — build `Vault/_vocabulary/GAS_VOCABULARY.md` from canonical (`--vocab` path), if not
   already present, with §4 frontmatter + named consumers (mirror OBDLab `T-VAULT-VOCAB-1`). The
   `docs/GAS_VOCABULARY.md` is the vocab source and is **excluded** from the docs tier (see T-GAS-DOCPREP).
1. Confirm eligibility (Phase 0): `labs/gaslab/gaslab/`, `tests/`, `wiki/`, `docs/`, plus
   `graph/v2_code/graph.json` and `graph/v2_tests/graph.json` present. Prose graphs are owner-waived
   for this pack because Phase-2 wiki/doc prep is sufficient.
2. **Author `assets/vault-map.gaslab.yaml`** — `lab: gaslab`, `module: …`, a `frame:` block per framed
   note, and a `plain:` list for un-framed copies. Model exactly on `vault-map.obdlab.yaml`.
3. `build_lab_vault.py --lab gaslab --repo <repo>/4DLabV2 --dry-run` → review the copy/inject plan.
4. Drop `--dry-run` → copies `code/`, `tests/`, `wiki/`, `docs/` into `Vault/labs/gaslab/`, injects
   frontmatter skeletons, fills semantic fields from the map, writes the lab landing note.
5. Copy the three `.base` views into `Vault/_bases/` (if not shared already); refresh `System-Map.md`
   + `_meta/PROVENANCE.md` with the GAS provenance.
6. Open `Vault/` in Obsidian; confirm the three Bases render and `orphans` / `unresolved` are empty or
   explained.

### Consumer evidence to use (already grep-verified in AUDIT_2026-06-10 §2) ###

The output payload's live COMLab readers are named and confirmed — use these as the authored
`consumers`, not invented ones:

- `chemical_state` → `comlab/.../core/fault_atlas_router.py`
- `lambda_chem` / `lambda_measured` → `analytics/power_loss_analytics.py`,
  `core/lab_pipeline_aggregator.py`, `core/perception_contradiction.py`
- `gas_co` / `gas_hc` / `gas_o2` → `analytics/power_loss_analytics.py`
- `sample_validity` → `core/lab_pipeline_aggregator.py`, `schemas/vocabulary.py`

> **Do NOT frame** notes whose only "consumer" would be `gas_co2` / `gas_nox` (carried across the
> boundary but **no live COMLab analytic reads them** — consumer-deferred to the COMLab v2 rework,
> AUD-5). A note resting solely on those has no live consumer yet → leave it `plain:` or mark the
> field a proposal; do not fabricate a consumer to make it frame.

### Success criteria (plan §7) ###

1. `Vault/labs/gaslab/` shows `code/`, `tests/`, `wiki/`, `docs/` and a working graph view in Obsidian.
2. All three `.base` views render with GAS rows: modules grouped; **every framed note has ≥1 named
   consumer**; every `implements` target has ≥1 `drift_guard` or is explicitly marked untested.
3. **Consumer completeness:** no framed GAS note ships with an empty `consumers` list.
4. **No `graph.json` re-extraction** was run; existing `graph/v2_code` and `graph/v2_tests`
   byte-unchanged.
5. `build_lab_vault.py` is idempotent and dry-run-safe (re-run updates in place, never duplicates).

### Out of scope ###

- Building any other lab's vault tier · re-graphifying any corpus · auto-deriving `consumers`.
- The Pass-3 graph cross-check (owner-deferred for this pack).

### Files to touch ###

- `_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml` (new — the architect consumer map).
- `Vault/labs/gaslab/…` (generated), `Vault/_vocabulary/GAS_VOCABULARY.md`, `Vault/_bases/*` (if not shared),
  `Vault/System-Map.md`, `Vault/_meta/PROVENANCE.md`.

### Verification ###

```bash
cd <repo>/4DLabV2
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab gaslab --repo "$PWD" --dry-run | head -50
# every framed note must carry a non-empty consumers list:
grep -A3 'node_type' Vault/labs/gaslab/wiki/*.md Vault/labs/gaslab/docs/*.md | grep -c 'consumers'
git status --porcelain labs/gaslab/graph | grep . && echo "FAIL graph touched" || echo "OK graph untouched"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-VAULT.md` opens with the confirmed `## Plan` (the framed-note roster +
each note's named consumer); the run session fills `VERIFICATION GATE` (Bases render, every framed note
≥1 consumer, no empty list, no re-extraction, idempotent) + `CODE REVIEW` (map authored against
Phase-2 prose prep plus code/test graphs, consumers all named/grep-backed, orphans/unresolved empty or
explained). Ledger row → `done` only when both blocks are clean — this closes the GASLab vault pack.
