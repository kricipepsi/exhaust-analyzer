# 4DLabV2 — Migration Strategy (architect spec)

**Date:** 2026-06-05 · **Author:** architect · **Status:** proposal, awaiting owner ratification of decisions D1–D5
**Goal:** relocate the **v2 workflow** out of the cluttered `4DLab/` root into a clean,
self-contained `4DLab/4DLabV2/` workspace shaped by `docs/StructProp.md` (Architect-Builder / 12x.ai
scaffold) and `_skills/FolderStruct/skill.md` (flat-package technical layout) — **without** leaving a
trail of broken reference paths, and archiving everything non-essential so the result is *easier* to
navigate, not messier.

> This document is the **plan**, not the move. The architect authors it; the actual relocations,
> rewrites, and the inner loop are **coder-session** work this plan commissions (one phase = one
> session, per the one-task rule). Nothing in `4DLab/` is moved by writing this file.

---

## 1. What the recon found (the facts the plan is built on)

These are measured, not assumed:

- **The v2 footprint is small and tractable.** The *new* v2 workflow is essentially three things:
  `V2_ROADMAP.md` (the navigation spine), `GASLabV2/` (40 files), and `audit_2026-06-03/` (the
  source-of-truth audit). Only **3** `.md` files reference `V2_ROADMAP`, **14** reference `GASLabV2`,
  **1** references `audit_2026-06-03`. The reference web that breaks on a move is *enumerable*.
- **`GASLabV2/` is 100% documents** — 39 `.md` + 1 `.gitkeep`, **zero `.py`**. It is a
  spec/ledger/study *overlay*. The actual v2 **code** changes land in-place inside the **shared v1
  package** `GASLab/gaslab/*.py` (the "GASLab-revised-first, divergent until consumers catch up"
  model). This is the crux: moving the brain is trivial; moving the *code* means disentangling it from
  a package that `4DLabWired`, `registry`, `COMLab`, and the harness all still consume.
- **References break in BOTH directions.** Inbound: docs that point *into* the v2 work. Outbound: v2
  docs that point *out* to retained substrate — `GASLab/gaslab/*.py`, `docs/GASLab/wikiNEW/GAS_WIKI.md`
  (canonical wiki), `4DLabWired/wired/composition.py`, `registry/schema_v2.py`, `comlab/schemas/*`,
  `TestSuite/harness/`. A one-directional rewrite would silently miss the outbound half.
- **Naming-collision hazard.** Legacy `v2/` (1,972 files, explicitly *do-not-import* per root
  `CLAUDE.md`) sits at the root right beside the new `4DLabV2/`. "v2" now means two opposite things.
  This is the single biggest "more mess" risk and must be resolved in the same pass.
- **The ledger is at a clean cutover boundary.** Stage-1 GASLab is essentially all `done`. Only
  **T-GV2-15** is `pending`/runnable and **T-GV2-14** is `blocked` (owner decision needed). **T-GV2-2,
  FU-1, FU-2, FU-4** are deliberately deferred to the Stage-4 COMLab reconciliation — they carry their
  own state and travel *with* the workflow; they do not block the move.

---

## 2. Owner decisions to ratify before Phase 0 (D1–D5)

The architect recommends; the owner ratifies. Each is a one-line answer.

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| **D1** | How to disentangle the v2 **code** from the live v1 `GASLab/` package | (a) **fork-and-freeze**: copy `GASLab/gaslab` → `4DLabV2/labs/gaslab` as the new canonical, freeze the v1 copy · (b) **move-and-rewire**: physically move `GASLab/` and repoint every consumer now | **(a) fork-and-freeze** — lowest immediate breakage, gives a clean v2 home, and matches "archive the old" |
| **D2** | When to repoint live consumers (`wired`, `registry`, `COMLab`) at the forked code | (a) at the **Stage-4 COMLab** boundary · (b) immediately during the move | **(a) Stage-4** — that is exactly where FU-1/FU-4/T-GV2-2 already reconcile these consumers; doing it now duplicates that work against a moving target |
| **D3** | The canonical wiki `docs/GASLab/wikiNEW/` | (a) **link in place** (stays at root, v2 docs point to it) · (b) copy into `4DLabV2/docs/reference/` | **(a) link in place** — copying forks the *single source of truth*; never duplicate canon |
| **D4** | Legacy `v2/` (and `v6/`) | (a) **move to `ARCHIVE/legacy_v2/`** · (b) leave with a banner | **(a) archive** — kills the `v2/` vs `4DLabV2` collision outright; highest de-mess value |
| **D5** | The FX cross-lab pack (`FX_START_HERE.md` / `FX_PROGRESS.md`) and v1 labs | in v2 scope, or stays at root until v1 sunset? | **Stays at root** for now — out of the v2 brain; revisit at v1 sunset (see Q-A) |

---

## 3. Target structure for `4DLabV2/`

Marries the three sources: StructProp's **brain + planning + docs + references** scaffold,
FolderStruct's **flat `src`-style package with `__all__` and absolute imports**, and the existing
4DLab conventions (`*_START_HERE.md`, `*_tasks/` ledgers, `progress_notes/`, the signal/noise rule).

```
4DLabV2/
├── AGENTS.md                 # ROUTER — first file any agent reads (StructProp). Maps role + which file to read first.
├── README.md                 # human overview of the v2 workspace
├── CLAUDE.md                 # THIN adapter: defers infra (sandbox-python, .venv-wired, git ritual) to root 4DLab/CLAUDE.md; v2-specific rules only
├── V2_START_HERE.md          # bootstrap (4DLab convention) → reads ROADMAP + the active stage ledger
├── ROADMAP.md                # ← migrated V2_ROADMAP.md (the navigation spine)
├── DECISIONS.md              # architectural/business decision log (seed: §2 D1–D5)
├── DOMAIN.md                 # petrol-only diagnostic domain: L1–L5 pipeline, Brettschneider-truth-vs-ECU-perception
├── RISKS.md                  # known traps (seed: §7)
├── QUESTIONS.md              # open research-gate questions (seed: roadmap RQ#1–5 + Q-A..Q-D)
├── docs/                     # durable technical docs (StructProp /docs)
│   ├── architecture.md       # lab isolation, JSON-only boundaries, no cross-lab imports, signal/noise rule
│   ├── data_model.md         # ChemicalSignature 34-surface, DNA views, contracts
│   ├── validation.md         # inner loop + verification-gate + code-review definition of done
│   └── reference/
│       └── audit_2026-06-03/ # ← migrated audit (source of truth); wikiNEW stays linked in place (D3)
├── planning/                 # StructProp /planning — "sprints" == 4DLab "stages"
│   └── sprints/
│       └── stage1_gaslab/
│           ├── START_HERE.md  # ← migrated GASLABV2_START_HERE.md
│           ├── PROGRESS.md    # ← migrated GASLABV2_PROGRESS.md (the ledger)
│           ├── tasks/         # ← migrated gaslabv2_tasks/  (task files == StructProp requirements+blueprint+acceptance+handoff)
│           │   └── progress_notes/
│           └── studies/       # ← STUDY_*.md, lastsess.md, SEQUENCING_gaslabv2_harness.md
│       └── stage2_obdlab/ … stage3_dtclab/ … stage4_comlab_registry/   # born here as each stage starts
├── labs/                     # v2 SOURCE CODE (FolderStruct: one flat package per lab, __all__, absolute imports)
│   ├── gaslab/               # Stage 1 — fork of v1 GASLab/gaslab (D1); v1 archived once green (Q-A)
│   ├── obdlab/               # Stage 2 — fork of v1 OBDLab; hosts re-homed bank-asymmetry (T-GV2-14 void)
│   ├── dtclab/               # Stage 3 — fork of v1 DTCLab (#1 leverage)
│   ├── comlab/               # Stage 4 (last) — fork of v1 COMLab + registry; deferred repoints land here
│   └── dnalab/               # DNALab/VINLab — feeds the COMLab prior (not a separate stage)
│       # each lab: __init__.py (explicit __all__) + tests/ (parallel dir) when its code lands
├── 4dlabwired_v2/            # composition + UI + harness — composes OVER labs (mirrors types, no imports)
└── references/               # static artefacts (sample cases, html) if any move

> **Born inside (Q-C, 2026-06-05):** all lab folders + `4dlabwired_v2/` are scaffolded now with README
> placeholders, so every lab has a home before its stage opens — no second migration later. Code forks
> in per the stage sequence (gaslab → obdlab → dtclab → comlab; dnalab feeds Stage-4).
```

Mapping of StructProp names → 4DLab reality, so nothing is invented twice: *sprint* = *stage*; the
four sprint docs (requirements / blueprint / acceptance / handoff) are already the single
**task file** per the GASLabV2 authoring model; *meetings* = the `progress_notes/` + study files.

---

## 4. Cutover sequencing (one phase = one coder session)

**Phase 0 — Freeze gate (coder sessions, BEFORE any move).** This is the "finish the coder tasks
first" you asked for. Reach a ledger state with **zero `in_progress` rows** and both gates clean on
every `done` row:
1. Finish **T-GV2-15** (closes FU-CYL; ratify its (a)/(b) flag first).
2. Resolve **T-GV2-14** disposition — either unblock it with a named consumer or formally park it as
   `blocked (owner)`. A `blocked` row is allowed to cross the cutover; an `in_progress` one is not.
3. Confirm `T-GV2-2`, `FU-1`, `FU-2`, `FU-4` remain `deferred` (Stage-4) — they migrate as-is.
   *Exit criterion:* the freeze commit. Everything after this is the move itself.

**Phase 1 — Author the two manifests + scaffold spec (architect).** Additive, moves nothing.
- `MIGRATION_MANIFEST.md` = the **path map** (§5) — single source of truth for every old→new path.
- `CLASSIFICATION.md` = the **migrate / keep / archive** verdict per item (§6 policy + starter table).
- Seed the brain docs (agents/README/CLAUDE/DECISIONS/DOMAIN/RISKS/QUESTIONS) from §2/§3/§7.

**Phase 2 — Create the empty scaffold (coder).** Make the `4DLabV2/` tree and drop in the seed brain
docs. Purely additive — breaks nothing, so it can land and be reviewed on its own.

**Phase 3 — Relocate the v2 brain (coder).** Copy the v2 *documents* (ROADMAP, audit, GASLabV2 ledger
+ tasks + studies) to their new homes per the manifest, then **rewrite inbound references** (§5).
Use **copy → grep-gate → remove**, never in-place `mv`, so the source survives until the gate is green.

**Phase 4 — Disentangle the v2 code (coder).** Per D1, fork `GASLab/gaslab` → `4DLabV2/labs/gaslab`
(+ tests), add `__all__`, switch to absolute imports (FolderStruct). Rewrite the **outbound** refs in
the migrated docs to the retained substrate's stable path. **Do not** repoint live consumers yet —
that is scheduled into the Stage-4 COMLab reconciliation (D2), where FU-1/FU-4/T-GV2-2 already live.
Run the inner loop on the forked package only.

**Phase 5 — Archive sweep (coder).** Move legacy `v2/` (and `v6/` if present) → `ARCHIVE/legacy_v2/`
to kill the naming collision (D4), and superseded root docs → `ARCHIVE/root_docs_2026-06/` (§6). Add a
one-line banner to `ARCHIVE/README.md` so no future session mistakes archived-v2 for `4DLabV2`.

**Phase 6 — Verification gate + cutover commit (coder).** §8. Update the root `CLAUDE.md` bootstrap
table row and `MEMORY.md` pointers; run the grep gate and link-check; hand the owner the single
`git add … && git commit` line (the user's git ritual).

---

## 5. Reference handling — the core concern, solved

Policy (your choice): **identify every referencing document and rewrite all paths; no shims.** The
manifest is the contract; the grep gate is the proof.

### 5.1 Path map (old → new) — the rewrite source of truth

| Old (under `4DLab/`) | New |
|---|---|
| `V2_ROADMAP.md` | `4DLabV2/ROADMAP.md` |
| `audit_2026-06-03/` | `4DLabV2/docs/reference/audit_2026-06-03/` |
| `GASLabV2/GASLABV2_START_HERE.md` | `4DLabV2/planning/sprints/stage1_gaslab/START_HERE.md` |
| `GASLabV2/GASLABV2_PROGRESS.md` | `4DLabV2/planning/sprints/stage1_gaslab/PROGRESS.md` |
| `GASLabV2/gaslabv2_tasks/` (+ `progress_notes/`) | `4DLabV2/planning/sprints/stage1_gaslab/tasks/` |
| `GASLabV2/STUDY_*.md`, `GASLabV2/lastsess.md` | `4DLabV2/planning/sprints/stage1_gaslab/studies/` |
| `SEQUENCING_gaslabv2_harness.md` | `4DLabV2/planning/sprints/stage1_gaslab/studies/SEQUENCING_gaslabv2_harness.md` |
| `GASLab/gaslab/` (v2 code, D1) | `4DLabV2/labs/gaslab/` |
| `docs/GASLab/wikiNEW/` (D3) | **stays in place** — outbound refs rewrite to this retained path |

### 5.2 Documents to rewrite (measured inventory)

| File | Ref type | Action |
|---|---|---|
| `CLAUDE.md` (root) | bootstrap-table row + 6 `GASLabV2` mentions | rewrite the one bootstrap row → new `START_HERE`; rewrite mentions |
| `docs/GASLab/v2_prep/PROPOSAL_GASLabV2_InOut_and_Rebuild.md` | inbound → GASLabV2 | rewrite to new paths |
| `graphify-out/GRAPH_REPORT.md` | inbound → GASLabV2 (authored `.md`) | rewrite the prose refs |
| `graphify-out/graph.json`, `manifest.json`, `cache/ast/*.json` (~44 files) | **derived index**, not authored — embeds old file paths | **do not edit, do not re-run graphify** — see §5.4 |
| `TestSuite/harness/harness_tasks/T-TH-14_dual_rpm_faultbox_extension.md` | inbound → GASLabV2 | rewrite to new paths |
| `GASLabV2/*` (all 39, incl. PROGRESS, task files, studies, START_HERE) | **outbound** → `GASLab/gaslab`, `wikiNEW`, `4DLabWired`, `registry`, `comlab`, `TestSuite/harness` | rewrite outbound targets to retained stable paths |
| `docs/GASLab/wikiNEW/GAS_WIKI.md` | possible back-ref to GASLabV2 | rewrite only if it points at moved paths; wiki itself stays |
| Memory: `MEMORY.md` + `project_gaslabv2_wiki_canonical.md` (+ siblings) | path mentions in bodies | update pointers/bodies in Phase 6 |
| Code consumers: `4DLabWired/wired/composition.py`, `registry/schema_v2.py`, `comlab/schemas/*` | reference the GASLab **contract**, not GASLabV2 docs | **untouched in the doc move**; repoint only at Stage-4 (D2) |

### 5.3 Rewrite mechanics

- **Match every string form** of each token, not just the canonical one: `GASLabV2`, `./GASLabV2`,
  `4DLab/GASLabV2`, the bare filename `V2_ROADMAP.md`, `audit_2026-06-03`. The grep gate (§8) enforces
  zero survivors in active docs.
- **Prefer workspace-absolute or repo-root-relative paths** for the rewritten targets, not brittle
  `../../` chains — this is FolderStruct's "absolute imports survive reorganization" rule applied to
  documentation links.
- **Things that do NOT need rewriting** (verified): the sandbox-Python cache `…/mnt/4DLab/.sandbox-py`
  and `.venv-wired` both live at the `4DLab` root, *above* `4DLabV2`, so the move leaves them intact;
  memory `[[slug]]` links resolve by slug, not path, so only the path *bodies* need a touch. No `.py`
  or config file references the `GASLabV2` token (verified) — code consumers couple via the GASLab
  **contract/types**, not the folder path, so the doc move does not touch them.

### 5.4 Special case — `graphify-out/` (the canonical graph + AST cache)

The graph index embeds old file paths in `graph.json`, `manifest.json`, and ~44 content-addressed
`cache/ast/*.json` files. These are **derived artefacts**, and `CLAUDE.md` forbids re-running graphify
(`graph.json` is the canonical artefact, re-extract only when explicitly instructed). So: rewrite only
the authored `GRAPH_REPORT.md` prose; **leave the machine cache untouched**. The graph will reference
the pre-move layout until a future, explicitly-instructed single re-extraction (the `T-GV2-KG`
optional row) re-aligns it. The §8 grep gate is `.md`-scoped precisely so it does not flag — or tempt
anyone to hand-edit — these cache files.

---

## 6. Essential-vs-archive policy

**Rule:** an item *migrates* only if it is part of the live v2 workflow (a brain doc, an active ledger
or task, a study a future session will read, or v2 code). It *stays at root* if it is shared infra
that v1 still needs. Otherwise it is *non-essential* → `ARCHIVE/`. "Might be useful later" is not a
reason to migrate — same discipline as the signal/noise rule.

| Verdict | Items (starter — finalize in `CLASSIFICATION.md`, Phase 1) |
|---|---|
| **Migrate → 4DLabV2** | `V2_ROADMAP.md`, `audit_2026-06-03/`, `GASLabV2/*`, `SEQUENCING_gaslabv2_harness.md`, forked `GASLab/gaslab` (D1) |
| **Keep at root** | `CLAUDE.md`, `WINDOWS_SETUP_ONCE.md`, `settings*.json`, `.venv-wired`, `.sandbox-py`, `docs/GASLab/wikiNEW/` (D3), active v1 labs, `FX_*` (D5), `graphify-out/` |
| **Archive → `ARCHIVE/legacy_v2/`** | `v2/` (1,972 files), `v6/` if present |
| **Archive → `ARCHIVE/root_docs_2026-06/`** | `HANDOFF_2026-05-22_*`, `HANDOFF_2026-05-23_*`, `BUILD_OUT_PLAN_2026-05-22.md`, `NewArchProposal.md`, `NewArchProposal_ImplementationPlan.md`, `GasLabIteration.md`, `4DLab_Codebase_Analysis.md`, `CROSS_APP_DIAGNOSTIC_COMPARISON.md`, `casesextra_extraction_report.md`, `data_flow_report.md`, `recc.md`, `MDskillProposal.md`, `TaskRoadmap.md`, `AGENT_SETUP_GUIDE.md`, `COWORK_RULE_CODING_BOOTSTRAP.md`, `Osensorguide.md` |

Before archiving any doc, grep it as a *target* — if a live doc references it, either the reference is
also stale (rewrite/drop) or the doc is not actually non-essential (re-classify). Nothing gets
archived while a live path still points at it.

---

## 7. Risks (seed for `RISKS.md`)

| ID | Risk | Mitigation |
|---|---|---|
| R1 | `v2/` vs `4DLabV2` collision → edits/imports hit the wrong tree | Archive legacy `v2/` (D4); banner in `ARCHIVE/README.md` |
| R2 | Outbound refs (v2 docs → live v1 code) break silently — inbound-only grep misses them | Grep **both** directions; manifest lists outbound targets explicitly (§5.2) |
| R3 | Forking `GASLab/` makes two divergent copies; future edits to the wrong one | Freeze the v1 copy read-only + banner; the only canonical is `4DLabV2/labs/gaslab` |
| R4 | Moving mid-task leaves a stale ledger across the cutover | Phase-0 freeze gate: zero `in_progress`, both gates clean |
| R5 | Memory `[[links]]`/path bodies go stale | Update `MEMORY.md` + `project_*` bodies in Phase 6 |
| R6 | `mv` mid-flight loses data | copy → grep-gate → remove; never in-place move |

---

## 8. Verification gate (Phase 6 — must be clean before the cutover commit)

1. **Stale-token grep gate:** `grep -rl 'GASLabV2\|V2_ROADMAP\|audit_2026-06-03' --include=*.md` over
   *active* dirs returns **only** the new `4DLabV2/` locations (ARCHIVE copies are allowed). Zero
   stale pointers in any live doc.
2. **Outbound link-check:** every rewritten outbound target in the migrated v2 docs resolves to a file
   that exists at its retained path.
3. **Inner loop on the forked code** (`ruff` → `pyright` → `pytest -x -q` on `4DLabV2/labs/gaslab`) —
   the GASLab suite that was green pre-move (204 GAS) is green post-fork.
4. **Bootstrap reachability:** root `CLAUDE.md` table row points at the new `START_HERE`; a fresh
   session can reach the active ledger from the table alone.
5. **No-orphan / signal-noise unchanged:** the move adds no schema field, so every existing field keeps
   its existing named consumer; no cross-lab Python import is introduced by the fork.
6. **Rollback = git** (the undo button per `CLAUDE.md`): each phase commit is a restore point; the copy
   sources survive until each phase's grep gate passes.

---

## 9. Open questions (seed for `QUESTIONS.md`)

- **Q-A:** Is v1 being **sunset** entirely (then v1 labs eventually archive too, and the GASLab fork is
  permanent), or kept running in parallel (fork is a long-lived divergence)? Governs D1's end-state.
- **Q-B:** T-GV2-14 disposition — unblock with a named consumer, or park as `blocked (owner)`?
- **Q-C:** Are OBDLabV2 / DTCLabV2 / COMLabV2 **born inside** `4DLabV2/labs` from day one of their
  stage, or stood up at root and migrated later? (Recommend: born inside — avoids a second migration.)
- **Q-D:** FX cross-lab pack scope (D5) — in the v2 brain, or root until v1 sunset?

---

## 10. Unplanned follow-ups (off-scope; logged, not actioned)

| ID | One-liner | Status |
|---|---|---|
| FU-MIG-1 | Workspace has **2,207 `.md`** files; a broader doc-hygiene pass (beyond v2) would further de-clutter — but it is out of this migration's scope | open — separate effort |
| FU-MIG-2 | `4DLabWired` / `registry` / `COMLab` consumer repoint to the forked GASLab is parked into the **Stage-4** reconciliation alongside FU-1/FU-4/T-GV2-2 (D2) | open — Stage-4 |
