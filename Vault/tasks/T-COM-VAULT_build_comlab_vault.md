---
node_type: task
task_id: T-COM-VAULT
status: done
pack: VAULT
lab: comlab
mode: architect/author + vault-tooling lane
blocked_by:
- T-COM-GRAPH-AST
- T-COM-PATHS-1
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- drift-guards.base — coverage view
- modules.base — module map view
- graph/v2_code — AST code graph
- graph/v2_tests — AST test graph
- apps/4DLabWired (LabPipelineAggregator consumer)
implements:
- graph/v2_code/graph.json
- graph/v2_tests/graph.json
- vault-map.comlab.yaml
tags:
- task
- vault
- comlab
---

# T-COM-VAULT — Author `vault-map.comlab.yaml`, dry-run, build, and install the COMLab vault tier

**Status:** `done` (2026-06-28) · **Pack:** VAULT (COMLab) · **Mode:** architect/author + vault-tooling lane (no lab inner-loop/gate)
**Origin:** pipeline guide §6 (Phase 4) · **Blocked by:** T-COM-GRAPH-AST, T-COM-PATHS-1
**Load skills:** **`4dlab-vault`**, **`comlab-vault-prep`** (consumer framing + exclusion list),
`comlab-verification-loop` (the anti-orphan / consumer gate).
**Consumer (signal/noise):** **The `consumers` field is the signal/noise gate itself.** Each framed COMLab
note ships only with a **named, existing** downstream consumer — and because COMLab is the **terminal fusion
spine**, that consumer is **COMLab-internal** (`analytics/`, `core/fault_atlas_router.py`, the
`.process()` aggregator) or the **app layer** (`apps/4DLabWired/`, `apps/ui/`), **never another lab**. The
three `.base` views are the live readers: `modules.base` (groups by `lab`→`module`), `consumers.base`
(every note has ≥1 named consumer), `drift-guards.base` (every `implements` target has ≥1 guarding test or
is marked untested). **An empty `consumers` list = the note is not ready to ship.**

### Role note ###

`build_lab_vault.py` is vault tooling — no `comlab/` inner-loop/gate. The vault is a **read-mostly window**:
it copies prepared lab sources and checks the required graph tiers **without re-extracting them**. For
COMLab, the prose graphs are waived, so `graph/v2_code/` + `graph/v2_tests/` are required and
`graph/v2_wiki/` + `graph/v2_docs/` are **not** (set by `T-COM-PATHS-1`). Authoring `vault-map.comlab.yaml`
is the architect-named consumer step; `consumers` is **never** auto-derived.

### Prerequisite path fix ###

This task assumes **T-COM-PATHS-1 is `done`**, so `--dry-run --lab comlab` resolves COMLab's `wiki/` +
two-tier graph. If it still aborts on a hardcoded `research/chunks` / `v2_wiki` / `v2_docs` path, stop and
route back to `T-COM-PATHS-1` — do not patch the script inside this task.

### Step 0 — `_vocabulary/` (check first; add only what's missing) ###

`Vault/_vocabulary/` already holds `DTC_VOCABULARY.md` and `OBD_VOCABULARY.md` — COMLab's
`docs/Vocabulary/DTC_VOCABULARY.md` / `OBD_VOCABULARY.md` are **mirrors of those existing homes → do NOT
re-copy or duplicate** (canonical lives at `labs/semantic/vocabul/`). **`SEMANTIC_CONTRACT.md` has no vault
home yet** and COMLab is its natural owner: if it is a shared vocab/contract note with a **named existing
consumer**, add it to `assets/vault-map.vocabulary.yaml` and build it via the `--vocab` path with
§-anchored frontmatter; if no consumer can be named, leave it out (signal/noise). Do not invent a consumer.

### Steps (guide §6) ###

1. Confirm eligibility (Phase 0): `labs/comlab/comlab/`, `tests/`, `wiki/`, `docs/`, plus
   `graph/v2_code/graph.json` and `graph/v2_tests/graph.json` present. Prose graphs are owner-waived.
2. **Author `assets/vault-map.comlab.yaml`** — `lab: comlab`, `module: comlab`, a `frame:` block per framed
   note (the design docs + the wiki chunks with a named consumer), and a `plain:` list for un-framed copies
   (`00_index.md`, `13_proposals_register.md`, and any note whose only story is a proposal). Model exactly
   on `vault-map.dtclab.yaml`.
3. `build_lab_vault.py --lab comlab --repo <repo>/4DLabV2 --dry-run` → review the copy/inject plan.
4. Drop `--dry-run` → copies `code/`, `tests/`, `wiki/`, `docs/` into `Vault/labs/comlab/`, injects
   frontmatter skeletons, fills semantic fields from the map, writes the lab landing note.
5. The four `.base` views already exist in `Vault/_bases/` (shared) — confirm, don't re-copy. **Add the
   COMLab row to `Vault/System-Map.md`** (it has none today) and refresh `_meta/PROVENANCE.md` (the build
   writes the COMLab provenance with the "v2_wiki/v2_docs waived" note).
6. Open `Vault/` in Obsidian; confirm the Bases render with COMLab rows and `orphans`/`unresolved` are empty
   or explained.

### Consumer evidence to use (name real readers, not invented ones) ###

COMLab is consumed by the **application layer** and **itself** — grep-confirm each before framing:

- `from comlab import LabPipelineAggregator` → `.process(OrchestratorInboundRequest)` →
  `OrchestratorFinalUIOutput` — the Wired app (`apps/4DLabWired/wired/composition.py`,
  `apps/4DLabWired/harness/diagnostic_classify.py`).
- `comlab.core.fault_atlas_router.FaultAtlasRouter`, `comlab.core.lab_pipeline_aggregator.LabPipelineAggregator`
  — imported by `apps/4DLabWired/tests/test_registry_select.py` / `test_registry_guard.py`.
- COMLab-internal: `analytics/power_loss_analytics.py` (scoring), `analytics/delta_engine.py` (delta),
  `core/perception_contradiction.py` (perception axis), `core/fault_atlas_router.py` (family routing).

> **Do NOT frame** a note whose only "consumer" would be a **proposal** (`comlab/config/proposals/` —
> `COMLab-DELTA`, `EP-*`; `wiki/13_proposals_register.md`) or a default-off flag-gated capability whose live
> value is still Gate-gated. Leave such a note `plain:` — do not fabricate a consumer to make it frame.
> **Never name another diagnostic lab as a COMLab consumer** (they are inputs).

### Success criteria ###

1. `Vault/labs/comlab/` shows `code/`, `tests/`, `wiki/`, `docs/` and a working graph view in Obsidian.
2. The three `.base` views render with COMLab rows: modules grouped; **every framed note has ≥1 named
   consumer**; every `implements` target has ≥1 `drift_guard` or is explicitly marked untested.
3. **Consumer completeness:** no framed COMLab note ships with an empty `consumers` list; no proposal /
   flag-gated token is framed as a live consumer; no other lab named as a consumer.
4. **No `graph.json` re-extraction**; `graph/v2_code`, `graph/v2_tests`, `graph/v1_baseline` byte-unchanged.
5. `build_lab_vault.py` is idempotent and dry-run-safe (re-run updates in place, never duplicates).
6. `Vault/System-Map.md` and `_meta/PROVENANCE.md` carry the COMLab tier.

### Out of scope ###

- Building any other lab's vault tier · the **registry** vault tier (separate pack — START_HERE §5) ·
  re-graphifying any corpus · auto-deriving `consumers` · lifting the prose-graph waiver (→ `T-COM-GRAPH-LLM`).
  **GRAPH GUARDRAIL:** no graphify / re-extraction.

### Files to touch ###

- `_skills/graph/4dlab-vault/assets/vault-map.comlab.yaml` (new — the architect consumer map);
  optionally a `SEMANTIC_CONTRACT.md` entry in `assets/vault-map.vocabulary.yaml`.
- `Vault/labs/comlab/…` (generated), `Vault/System-Map.md`, `Vault/_meta/PROVENANCE.md`,
  `Vault/_vocabulary/SEMANTIC_CONTRACT.md` (only if a consumer is named).

### Verification ###

```bash
cd <repo>/4DLabV2
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab comlab --repo "$PWD" --dry-run | head -50
# every framed note must carry a non-empty consumers list:
grep -A3 'node_type' Vault/labs/comlab/wiki/*.md Vault/labs/comlab/docs/*.md | grep -c 'consumers'
# no other lab named as a COMLab consumer:
grep -rn 'consumers' -A6 _skills/graph/4dlab-vault/assets/vault-map.comlab.yaml | grep -E 'gaslab:|obdlab:|dtclab:|dnalab:' && echo "FAIL lab-as-consumer" || echo "OK terminal-spine"
git status --porcelain labs/comlab/graph/v1_baseline | grep . && echo "FAIL graph touched" || echo "OK graph untouched"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-VAULT.md` opens with the confirmed `## Plan` (the framed-note roster +
each note's named consumer); the run session fills `VERIFICATION GATE` (Bases render, every framed note ≥1
consumer, no empty list, no proposal/flag/lab framed, no re-extraction, idempotent, System-Map+PROVENANCE
updated) + `CODE REVIEW` (map authored against the prep output + code/test graphs, consumers all
named/grep-backed, orphans/unresolved empty or explained). Ledger row → `done` only when both blocks are
clean — this closes the COMLab vault pack.
