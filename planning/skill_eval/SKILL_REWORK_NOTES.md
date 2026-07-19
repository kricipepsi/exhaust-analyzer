# Skill Rework Notes — applying the eval verdicts

**Date:** 2026-06-10 · **Pack:** `planning/skill_eval/`
**Basis:** `skill_eval_final_report.md`, `cohort_testcraft_report.md`, `cohort_gateoverlap_report.md`

This note records the corrections applied to `_skills/` after the skill-eval pack
completed. Two actions were taken: dedupe true duplicate copies, and rework the two
skills the test results show underperform. Dead/redirect/retired non-duplicate skills
were **left in place** (per owner instruction — delete only double copies).

---

## 1. Dedupe — byte-identical duplicate directories removed

Both were confirmed identical across **every** file in the directory (not just `SKILL.md`)
via `diff -rq`, so the canonical copy loses nothing.

| Removed (duplicate) | Canonical kept | Proof |
|---|---|---|
| `_skills/Improve Codebase Architecture/` (top-level) | `_skills/codingskills/Improve Codebase Architecture/` | SHA256 `9E9B617B…`, dirs `diff -rq` identical |
| `_skills/excel/excel-data-analysis/` | `_skills/excel/excel-analysis/` | SHA256 `FB681B86…`, dirs `diff -rq` identical |

Skill-file count: **38 → 36**.

**Not deleted** (owner rule — not duplicates, kept despite DEAD disposition in the eval):
`pythonskill/python` (redirect stub), `codingskills/code-simplifier`, `FolderStruct/skill.md`,
`doc/project-architecture-guidelines-template-…`, `graph/4dlab-graph` (retired).

**Left for owner decision** — the 4× byte-identical `sync/SKILL.md` stubs each live inside a
separate `mcpmarket-…` plugin bundle (with their own `plugin.json`, hooks, shared scripts),
so they are not clean standalone skill directories. Removing only the stub from inside a
plugin bundle is a partial edit; flagged rather than actioned.

---

## 2. Rework — the two TRIM skills

The eval graded these "positive but sub-bar": they help, but not enough to clear the
≥1-SD keep bar. In both cases the cohort report pinned *exactly which defects leaked*, so
the rework targets that gap directly rather than rewriting the skill wholesale.

### 2.1 `ai-regression-testing` — add a proactive boundary/failure-path pass

**Evidence (T-SE-4, `cohort_testcraft_report.md` §3):** the skill's entire escaped-defect
signal came from two boundary mutants on `task_02_csv_stats` — single-value `stdev`
(`len>1`→`len>=1`, a `StatisticsError`) and row-iteration (`rows[0]`→`rows[1]`, off-by-one).
It caught 2/8 there vs 0/8 baseline, but the cross-task mean diluted to +0.083 (sub-bar).
The skill was framed **reactively** ("test where bugs were found") and even carried a
DON'T — *"write tests for code that has never had a bug"* — that actively discourages the
boundary tests which produced its only win.

**Changes:**
- Reframed the core problem as **two** blind spots: re-introduced bugs *and* untested
  failure paths the writer-reviewer pair skips.
- Added a **Proactive Boundary & Failure-Path Pattern** section: a short checklist
  (empty collection, single element, zero/division, off-by-one index, `None`/`NaN`) with
  the reasoning for why an AI writer skips each, plus two worked pytest examples.
- Replaced the self-defeating DON'T with guidance not to mistake a green happy-path suite
  for a thorough one.

### 2.2 `verification-loop` — add an import-existence guard and a boundary review pass

**Evidence (T-SE-5, `cohort_gateoverlap_report.md` §2):** recovery was +1.0 (bar 1.92,
sub-bar). It recovered **0** escaped defects on two tasks:
- `task_03_trap_api` — it hallucinated `fast_fetch` / `disk_cache` (non-existent libraries)
  identically to the no-skill control: *"no library-existence guard in this skill."*
- `task_02_csv_stats` — boundary defects (single-value/empty/zero) slipped through.

**Changes:**
- Phase 1 renamed **Syntax & Import-Existence Check**: actually `importlib.import_module`
  the changed module so a plausible-but-invented dependency fails here, not at runtime;
  added the reasoning (parsing ≠ importing) and a confirm-the-package note.
- Phase 6 diff review now names the boundary/failure paths explicitly (empty / single /
  zero / off-by-one) and flags any added code path with no test exercising its boundary.
- Output-format block gained an `Imports:` line.

Each edit carries an inline `<!-- Rework basis: … -->` comment citing the cohort report
section, so the change is traceable to its evidence.

---

## 3. Not reworked (deliberately)

- **`python-testing`** (KEEP) — its `mutation_score` showed no effect, but its KEEP rests
  on `rubric_test_meaningfulness` (d=1.35) and the flat mutation result is partly the
  equivalent-mutant artefact (FU-SE-6). It is a winner; editing it risks regressing what
  works. The proactive-boundary idea added to `ai-regression-testing` would also lift it —
  logged as an optional follow-up, not actioned, to keep this change scoped.
- **KEEP skills** (`python`, `uncle-bob-craft`, `improve-codebase-architecture`,
  `code-review-excellence`) — cleared the bar; no rework needed.

---

## 4. Follow-ups

| ID | Finding | Status |
|---|---|---|
| FU-RW-1 | `_skills` inventory drifted 37→38 since the 2026-06-09 triage: new `graph/4dlab-vault` skill (valid `name:`, KG tooling → OUT-OF-SCOPE) was added after the eval. Triage/final-report counts are now stale by +1. | logged — refresh inventory next eval pass |
| FU-RW-2 | 4× byte-identical `sync/SKILL.md` plugin stubs — dedupe deferred (partial-plugin-edit risk). | owner decision |
| FU-RW-3 | Optional: empirically re-validate the two reworks by re-running the T-SE-4 / T-SE-5 cohorts on the edited skills (skill-creator eval loop or the pack's own runner). | optional |
| FU-RW-4 | Optional: apply the proactive-boundary pattern to `python-testing` and re-measure `mutation_score`. | optional |
