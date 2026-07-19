# 4DLabV2 — Migration Manifest (Phase-1 deliverable)

**Date:** 2026-06-05 · **Author:** architect · **Companion to:** `MIGRATION_STRATEGY.md`
**Role:** the **single source of truth** for every old→new path and every reference rewrite. Phase 3–6
coder sessions execute against *this file*; the §F grep gate proves the execution is complete.

All paths are relative to the repo root `4DLab/` unless absolute. The new home is `4DLab/4DLabV2/`.

## How to execute (discipline — applies to every move below)

1. **Copy, don't move.** `copy old → new`, run the §F grep gate, **then** delete the old. Never
   in-place `mv` — the source is the rollback until the gate is green (RISK R6).
2. **One phase = one session** (Phase 3 brain, Phase 4 code, Phase 5 archive, Phase 6 verify).
3. **Rewrite rule for migrated docs:** add this line to the top of each migrated ledger/task once —
   *"Paths in this file are relative to the `4DLab/` repo root."* — then apply §C so every link is
   root-relative (FolderStruct: absolute/anchored beats brittle `../..`).
4. Do **not** start until Phase 0 freeze gate is met (ledger has zero `in_progress`; T-GV2-15 done;
   T-GV2-14 dispositioned).

---

## EXECUTION LOG

| Phase | Status | Notes |
|---|---|---|
| 0 freeze | **DONE** 2026-06-05 | T-GV2-14 `void`, T-GV2-15 `done`; ledger has no pending/in_progress/blocked. |
| 3 brain relocation | **DONE** 2026-06-05 | 40 GASLabV2 docs + audit + ROADMAP + SEQUENCING → `4DLabV2/`; refs rewritten in `CLAUDE.md`, PROPOSAL, `GRAPH_REPORT.md`, `T-TH-14`; sources deleted; **token gate PASS**. Empty `GASLabV2/` husk remains (file lock; `rmdir` later — git ignores empty dirs). |
| 5 archive sweep | **DONE** 2026-06-05 | legacy `v2/` → `ARCHIVE/legacy_v2/` (1,972 files — collision killed); 16 superseded root docs → `ARCHIVE/root_docs_2026-06/`; `ARCHIVE/README.md` banner added. |
| 4 code fork | **DONE** | `T-MIG-4`. Fork is canonical at `4DLabV2/labs/gaslab`; `GASLab/` archived to `ARCHIVE/legacy_gaslab_v1/`; `ARCHIVE/README.md` banner added. Post-archive gate green: ruff clean, pyright 0 errors, 207 GAS passed, import resolves to fork, `test_composition.py` 48 passed, content byte-identical. `docs/wiki/{GAS_VOCABULARY,GAS_WIKI}.md` copied (real files, needed by `test_validators.py`). Suite-runner SAI staleness carved to `T-MIG-5`. |
| 4b follow-up | **DONE** 2026-06-06 | `T-MIG-5`: SAI drift fixed, and expected-state corpus refreshed to the v2 timing taxonomy and specificity rules under F-9. All four suite CSVs run 100% green (passes: with-DNA 48/48, basic 51/51, high-idle with-DNA 48/48, high-idle basic 48/48). |
| 6 verify + commit | **DONE** 2026-06-06 | bootstrap row updated; token gate PASS; T-MIG-4 fork/archive verification complete; memory MEMORY.md pointer/body refresh complete. |

## A0. Born-inside lab scaffold (created 2026-06-05, Q-C — already on disk)

Per Q-C, every lab has a home **now**, not just gaslab, so no lab needs a second migration. These exist
as README placeholders; code forks in per stage (D1 / Q-A — v1 lab archived once its v2 is green).

| Folder | Stage | v1 source to fork → then archive |
|---|---|---|
| `4DLabV2/labs/gaslab/` | 1 | `GASLab/gaslab/` |
| `4DLabV2/labs/obdlab/` | 2 | `OBDLab/` (hosts re-homed bank-asymmetry; T-GV2-14 voided in GASLab) |
| `4DLabV2/labs/dtclab/` | 3 | `DTCLab/` |
| `4DLabV2/labs/comlab/` | 4 (last) | `COMLab/` + `registry/` |
| `4DLabV2/labs/dnalab/` | feeds Stage-4 prior | `DNALab/` (+ VINLab) |
| `4DLabV2/4dlabwired_v2/` | per-lab | `4DLabWired/` |

Decisions backing this: `DECISIONS.md` (Q-A..Q-D, D1–D5). FX pack stays at root (Q-D).

## A. Directory-level moves (the bulk — Phase 3)

Move the whole directory; the rename rule covers every file inside.

| # | Old dir | New dir |
|---|---|---|
| A1 | `GASLabV2/gaslabv2_tasks/` (24 files incl. `progress_notes/`) | `4DLabV2/planning/sprints/stage1_gaslab/tasks/` |
| A2 | `GASLabV2/gaslabv2_tasks/progress_notes/` (16 files + `.gitkeep`) | `4DLabV2/planning/sprints/stage1_gaslab/tasks/progress_notes/` |
| A3 | `audit_2026-06-03/` (1 file) | `4DLabV2/docs/reference/audit_2026-06-03/` |

A2 is a child of A1 — moving A1 carries it; listed for the grep gate's sake.

---

## B. File-level moves (renames that don't follow a dir rule — Phase 3)

| # | Old file | New file |
|---|---|---|
| B1 | `V2_ROADMAP.md` | `4DLabV2/ROADMAP.md` |
| B2 | `GASLabV2/GASLABV2_START_HERE.md` | `4DLabV2/planning/sprints/stage1_gaslab/START_HERE.md` |
| B3 | `GASLabV2/GASLABV2_PROGRESS.md` | `4DLabV2/planning/sprints/stage1_gaslab/PROGRESS.md` |
| B4 | `GASLabV2/lastsess.md` | `4DLabV2/planning/sprints/stage1_gaslab/studies/lastsess.md` |
| B5 | `GASLabV2/EcuGasSignature.md` | `4DLabV2/planning/sprints/stage1_gaslab/studies/EcuGasSignature.md` |
| B6 | `GASLabV2/STUDY_ecu_fault_gas_signatures_merge.md` | `4DLabV2/planning/sprints/stage1_gaslab/studies/STUDY_ecu_fault_gas_signatures_merge.md` |
| B7 | `GASLabV2/PreviousSequence.md` | `4DLabV2/planning/sprints/stage1_gaslab/studies/PreviousSequence.md` |
| B8 | `SEQUENCING_gaslabv2_harness.md` | `4DLabV2/planning/sprints/stage1_gaslab/studies/SEQUENCING_gaslabv2_harness.md` |

After A1–A3 + B1–B8, the `GASLabV2/` directory is empty → delete it.

---

## C. Reference rewrites (Phase 3 for docs; the find→replace contract)

Apply these **token → replacement** substitutions across the referrers in C.2. Match every string
form: bare (`GASLabV2/…`), `./`-prefixed, and `4DLab/`-prefixed.

### C.1 Substitution table (inbound — pointers *into* the moved files)

| Find (any prefix form) | Replace with |
|---|---|
| `V2_ROADMAP.md` | `4DLabV2/ROADMAP.md` |
| `audit_2026-06-03/` | `4DLabV2/docs/reference/audit_2026-06-03/` |
| `GASLabV2/GASLABV2_START_HERE.md` | `4DLabV2/planning/sprints/stage1_gaslab/START_HERE.md` |
| `GASLabV2/GASLABV2_PROGRESS.md` | `4DLabV2/planning/sprints/stage1_gaslab/PROGRESS.md` |
| `GASLabV2/gaslabv2_tasks/` | `4DLabV2/planning/sprints/stage1_gaslab/tasks/` |
| `GASLabV2/STUDY_…` / `lastsess.md` / `EcuGasSignature.md` / `PreviousSequence.md` | `4DLabV2/planning/sprints/stage1_gaslab/studies/…` |
| `SEQUENCING_gaslabv2_harness.md` | `4DLabV2/planning/sprints/stage1_gaslab/studies/SEQUENCING_gaslabv2_harness.md` |
| bare folder token `GASLabV2` (prose, e.g. "the GASLabV2 pack") | `4DLabV2 / stage1_gaslab` (prose; no path semantics) |

### C.2 Referrers to rewrite (measured — every authored file that hits a moving token)

| # | File | What it references | Rule |
|---|---|---|---|
| C-1 | `CLAUDE.md` (root) | bootstrap-table row → `GASLabV2/GASLABV2_START_HERE.md` + 6 prose mentions | rewrite the **one** bootstrap row to B2's new path; rewrite prose mentions |
| C-2 | `docs/GASLab/v2_prep/PROPOSAL_GASLabV2_InOut_and_Rebuild.md` | inbound → GASLabV2 | apply C.1 |
| C-3 | `graphify-out/GRAPH_REPORT.md` | inbound → GASLabV2 (authored prose only) | apply C.1 to prose; **do not** touch the `.json` cache (§E) |
| C-4 | `TestSuite/harness/harness_tasks/T-TH-14_dual_rpm_faultbox_extension.md` | inbound → GASLabV2 | apply C.1 |
| C-5 | **migrated** `ROADMAP.md` (was `V2_ROADMAP.md`) | → `audit_2026-06-03/`, `GASLabV2/GASLABV2_PROGRESS.md`, `GASLabV2/GASLABV2_START_HERE.md` | apply C.1 **and** C.3 (it also points outward) |
| C-6 | **migrated** `stage1_gaslab/PROGRESS.md` + all `tasks/*.md` + `studies/*.md` | outbound → `GASLab/gaslab/*.py`, `docs/GASLab/wikiNEW/`, `4DLabWired/`, `registry/`, `comlab/`, `TestSuite/harness/`, plus self-refs to sibling task files | apply **C.3** (outbound) + self-refs become `tasks/…`/`studies/…` relative |
| C-7 | Memory: `…/memory/MEMORY.md` + `project_gaslabv2_wiki_canonical.md` (+ any sibling with a path body) | path mentions in bodies | apply C.1; `[[slug]]` links unchanged (resolve by slug) |

### C.3 Outbound-anchor rule (retained substrate — Phase 3 for docs, Phase 4 for forked code)

Targets that **stay put** keep their root-relative path string; from the new doc location they are
written **root-relative** (the once-at-top note in §"How to execute" §3 makes this unambiguous). These
targets do **not** move during the brain migration:
`docs/GASLab/wikiNEW/` (D3 — canonical, link in place), `GASLab/gaslab/*.py` (until D1 fork lands in
Phase 4), `4DLabWired/`, `registry/`, `comlab/`, `TestSuite/harness/`, `graphify-out/`.
**After the Phase-4 fork** (D1), references in migrated docs that point at GASLab *v2 code* repoint
from `GASLab/gaslab/…` → `4DLabV2/labs/gaslab/…`; the live consumer repoint (`4DLabWired`/`registry`/
`COMLab`) is **not** here — it is parked into Stage-4 (D2 / FU-1 / FU-4 / T-GV2-2).

---

## D. Archive moves (Phase 5)

| # | Old | New | Why |
|---|---|---|---|
| D1 | `v2/` (1,972 files) | `ARCHIVE/legacy_v2/` | kills the `v2/` vs `4DLabV2` collision (RISK R1) |
| D2 | `v6/` (if present) | `ARCHIVE/legacy_v6/` | legacy, do-not-import |
| D3 | superseded root docs † | `ARCHIVE/root_docs_2026-06/` | de-clutter root |
| D4 | add banner to `ARCHIVE/README.md` | — | "legacy_v2 ≠ 4DLabV2 (the live v2 workspace)" |

† D3 set: `HANDOFF_2026-05-22_wiring_gate.md`, `HANDOFF_2026-05-23_o2map_session.md`,
`BUILD_OUT_PLAN_2026-05-22.md`, `NewArchProposal.md`, `NewArchProposal_ImplementationPlan.md`,
`GasLabIteration.md`, `4DLab_Codebase_Analysis.md`, `CROSS_APP_DIAGNOSTIC_COMPARISON.md`,
`casesextra_extraction_report.md`, `data_flow_report.md`, `recc.md`, `MDskillProposal.md`,
`TaskRoadmap.md`, `AGENT_SETUP_GUIDE.md`, `COWORK_RULE_CODING_BOOTSTRAP.md`, `Osensorguide.md`.
**Before archiving each:** grep it as a *target*; if a live doc still points at it, rewrite/drop that
link first, or re-classify the doc as essential (§6 of the strategy).

---

## E. Do NOT touch (verified)

| Item | Reason |
|---|---|
| `graphify-out/graph.json`, `manifest.json`, `cache/ast/*.json` (~44 files) | derived index; **never re-run graphify**; re-align only via the instructed `T-GV2-KG` re-extraction (strategy §5.4) |
| `4DLabWired/wired/composition.py`, `registry/schema_v2.py`, `comlab/schemas/*` | couple via the GASLab **contract/types**, not the `GASLabV2` path token (no `.py`/config references it — verified). Repoint at Stage-4, not now |
| `.venv-wired/`, `.sandbox-py/` | live at `4DLab` root, above `4DLabV2`; move leaves them intact |
| `docs/GASLab/wikiNEW/` | canonical single source of truth (D3) — link, never copy |

---

## F. Verification gate per phase (the proof)

Run from `4DLab/` root.

**After Phase 3 (brain moved + inbound rewrites):**
```
# zero stale pointers in active .md (ARCHIVE excluded; graphify .json excluded by --include)
grep -rl 'GASLabV2\|V2_ROADMAP\|audit_2026-06-03' --include=*.md . | grep -v '/4DLabV2/\|/ARCHIVE/'
# expect: NO output
ls GASLabV2 2>/dev/null   # expect: not found (dir deleted)
```
**After Phase 4 (code fork):** inner loop green on `4DLabV2/labs/gaslab` (`ruff`→`pyright`→`pytest -x -q`,
the 204-GAS suite); no new cross-lab import introduced.
**After Phase 5 (archive):** `ls v2 v6 2>/dev/null` → not found; root `.md` count dropped by the D3 set.
**After Phase 6:** root `CLAUDE.md` bootstrap row reaches the new `START_HERE`; `MEMORY.md` pointers
updated; hand the owner the single `git add … && git commit` line (paths by literal name).

---

## G. Coverage check (this manifest vs. the measured grep)

The Phase-1 grep found these authored referrers — all are covered above: `CLAUDE.md` (C-1),
`PROPOSAL_GASLabV2_InOut_and_Rebuild.md` (C-2), `GRAPH_REPORT.md` (C-3), `T-TH-14…md` (C-4),
`V2_ROADMAP.md` (C-5/B1), `SEQUENCING_gaslabv2_harness.md` (C-5 rule/B8), all `GASLabV2/*` internal
(A1/A2/B2–B7/C-6), memory (C-7). The graphify `.json` hits are the only non-authored referrers and are
deliberately **out of scope** (§E). No `.py`/`.yaml`/non-graphify `.json` references the token.
