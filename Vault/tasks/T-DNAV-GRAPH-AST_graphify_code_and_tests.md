---
node_type: task
task_id: T-DNAV-GRAPH-AST
status: done
pack: VAULT
lab: dnalab
mode: graph-tooling + coder lane
blocked_by:
- T-DNAV-CODEPREP
- T-DNAV-TESTPREP
consumers:
- graph/v2_code — AST code graph
- graph/v2_tests — AST test graph
- modules.base — module map view
- drift-guards.base — coverage view
implements:
- graph/v2_code/graph.json
- graph/v2_tests/graph.json
tags:
- task
- vault
- dnalab
---

# T-DNAV-GRAPH-AST — Graphify the DNALab code + tests (Pass 1, AST, offline) → `v2_code` / `v2_tests`

**Status:** `pending` · **Pack:** VAULT (DNALab) · **Mode:** GRAPH-TOOLING + coder lane (sanctioned graphify run)
**Origin:** pipeline guide §5 (Phase 3) + §5.5 (health-check) · **Blocked by:** T-DNAV-CODEPREP, T-DNAV-TESTPREP
**Consumer (signal/noise):** **Adds no schema field.** Builds the two AST graphs whose consumer is the
**vault build's frontmatter derivation** (`implements`/`module`/`source`) and the design→code→test spine
in the three `.base` views — both real and existing once `T-DNAV-VAULT` wires them. Pass 1 is the
tree-sitter AST read (offline, no LLM, no token cost).

### Role note — this is the ONLY sanctioned graphify run in the pack ###

graphify is forbidden as a side-effect of any other task. Here it is scoped to the **package** and the
**tests** dir, building the **new** tier dirs `graph/v2_code/` and `graph/v2_tests/`. It **never**
re-extracts the frozen `graph/v2_current/` or `graph/v1_baseline/`. Flow per corpus:
`resolve → run → relocate → verify`. Driving skill: `_skills/graph/4dlab-graphify-run/`.

### Hard guards (guide §5 — never skip) ###

- **Never `/graphify .` from the repo root** — scope to `labs/dnalab/dnalab/` (code) and
  `labs/dnalab/tests/` (tests) explicitly. (The 81.9k-node incident rule.)
- **Confirm the graphify-run skill has resolved branches for code + tests** before running.
- **Relocate, then confirm no root `graphify-out/` survives** — move `graph.json` + `GRAPH_REPORT.md`
  + `graph.html` into `graph/v2_code/` and `graph/v2_tests/` respectively.
- **No collateral:** `graph/v2_current/`, `graph/v1_baseline/`, `DIFF_REPORT.md` and every other
  `graph/*` byte-unchanged (`git status --porcelain` + mtime).

### Build ###

1. Code → Pass 1 AST on `labs/dnalab/dnalab/` → relocate to `labs/dnalab/graph/v2_code/`.
2. Tests → Pass 1 AST on `labs/dnalab/tests/` → relocate to `labs/dnalab/graph/v2_tests/`.

(`T-DNAV-GRAPH-LLM` is **waived** — prose Pass-3 wiki/docs graphs not built, mirror VIN/GAS/DTC.)

### Verify — health-check Part-A only (no LLM, no tokens, no re-extraction) ###

Run the eval skills in **health-only mode** (single graph arg) and read the GOOD/CHECK verdict:

```bash
cd <repo>/4DLabV2
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/dnalab/graph/v2_code/graph.json
# tests reuse the code-graph eval (both Pass-1 AST):
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/dnalab/graph/v2_tests/graph.json
```

Read the verdict: **dangling > 0 is always a defect** (route back to prep, never patch `graph.json`);
**isolated > 0 is a defect for code/tests** (every node should be wired); a higher INFERRED share is a
**baseline property** of Pass-1 AST graphs, not a fault. A missing edge is a **prep gap routed back to
`T-DNAV-CODEPREP`/`T-DNAV-TESTPREP`** — never patched into the graph.

> **Small-package note:** the DNALab package is 3 files (`__init__`, `assembly`, `models`) so `v2_code`
> will be a small graph — a low node count is expected, not a defect. The bar is still dangling=0,
> isolated=0, and the key symbols present (below).

### Success criteria ###

1. `graph/v2_code/graph.json` and `graph/v2_tests/graph.json` exist, node/edge counts > 0, relocated
   cleanly (no surviving root `graphify-out/`).
2. Health-check Part-A: both verdicts GOOD; dangling = 0; isolated = 0 (or each isolated node explained);
   key symbols spot-checked present (`build_vehicle_dna`, `VehicleDNA`, `from_json_payload`,
   `SCHEMA_VERSION`).
3. **Frozen graphs untouched:** `graph/v2_current/`, `graph/v1_baseline/`, `DIFF_REPORT.md` byte-unchanged.
4. No prose Pass-3 run; no schema field; no source edit.

### Out of scope ###

- Building `v2_wiki`/`v2_docs` (waived) · the Pass-3 cross-check tier (not authored) · re-extracting any
  frozen graph · editing source to chase an edge (route gaps back to prep).

### Files to touch ###

- `labs/dnalab/graph/v2_code/**`, `labs/dnalab/graph/v2_tests/**` (generated + relocated).
- Health-check verdicts pasted into the progress note.

### Progress hook ###

`Vault/tasks/progress_notes/T-DNAV-GRAPH-AST.md` opens with the confirmed `## Plan` (scope dirs + dest
tiers); the run session fills `VERIFICATION GATE` (both graphs built + relocated, Part-A GOOD, dangling=0,
isolated=0/explained, frozen graphs untouched) + `CODE REVIEW` (counts, top hubs, key symbols present).
Ledger row → `done` only when both are clean.
