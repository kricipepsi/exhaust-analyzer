# T-GFXSKILL-2 — Skill-creator eval loop for the three graphify skills

**Status:** iteration-1 DONE (3/3 skills 100%, probe verdict pinned) · **iteration-2 specced below — run with Codex** · **Author:** architect · **Date:** 2026-06-09 · **Mode:** STRICT
**Skills under test:** `4dlab-code-prep`, `4dlab-wiki-prep`, `4dlab-graphify-run`
(all under `_skills/graph/`). **Retired control:** `4dlab-graph` (must not trigger).
**Supersedes:** `SKILLS_TEST_TASK.md` (`T-GFXSKILL-1`, the manual with/without acceptance test).
This task keeps T-GFXSKILL-1's fixtures and per-skill criteria but runs them through the
**`skill-creator` eval harness** (parallel subagent runs → graded assertions → benchmark → static
review viewer), which is more rigorous and gives the owner a side-by-side to sign off on.

## Why this is a tooling task, not an OBDLab row

The three skills live at the workspace level (`_skills/graph/`), not inside any lab. This eval
touches **no production code and emits no schema field**, so the signal/noise field-rule does not
bite (same exemption T-GFXSKILL-1 claimed). It is tracked here next to the skills, **not** in
`labs/obdlab/tasks/PROGRESS.md`. Its "consumer" is the graphify-skills rollout itself: the eval
verdict is what lets `T-KG-OBD-2-PREP` (and the future wiki/run tasks) trust these skills on real
source and wiki.

## Goal

For each of the three skills, prove (a) it does what it claims and (b) **loading it changes
behaviour for the better** — the with-skill run catches what the bare run misses or respects a guard
the bare run violates. Use **small throwaway fixtures only**; never canonical source, wiki, or any
`graph/*` / `graphify-out/` artefact.

## Method — driven by the `skill-creator` skill (Cowork)

Read `skill-creator`'s SKILL.md first and follow its run/evaluate sequence. The Cowork specifics
apply: subagents are available, but there is **no browser/display**, so the review viewer must be
generated with `--static`. Concretely, per skill:

1. **Spawn with-skill AND baseline in the same turn.** For each eval prompt, one subagent runs the
   fixture task with the skill loaded, one runs it with **no skill** (the baseline for a
   does-this-skill-help comparison). Save under
   `_skills/graph/skilltest-out/iteration-1/<skill>/<eval>/{with_skill,without_skill}/outputs/`.
   (If timeouts bite, the skill permits running the prompts in series.)
2. **Draft assertions while runs are in progress.** The assertions are the per-skill success
   criteria below, phrased as objective, descriptively-named checks. Write/automate them as scripts
   where possible (audit-hits == seeded-violations; wiki trailer append-only via pre-trailer SHA256).
3. **Capture `total_tokens`/`duration_ms`** from each task notification into `timing.json` as it
   arrives (only chance to record it).
4. **Grade → aggregate → static viewer.** Grade each run (`grading.json` with the exact fields
   `text`/`passed`/`evidence`), aggregate with `python -m scripts.aggregate_benchmark`, then **generate
   the review viewer with `generate_review.py --static <out.html>`** (do **not** hand-roll HTML) and
   hand the owner the link. Do this **before** drawing your own conclusions — the owner reviews first.
5. **Read `feedback.json`** after the owner submits, then log skill defects for the architect to fix
   (editing the skills is out of scope here — see below).

## Fixtures (coder creates under `/tmp/gfxskilltest/`, never in the repo tree)

Reuse T-GFXSKILL-1's fixtures verbatim:

- **code fixture** `code_fix/` — tiny package: an `__init__.py` with **no** `__all__`; one module
  using `from x import *`; one public `def` with **no** type hints; one clean module with explicit
  imports + `__all__` + hints + a `StrEnum` + a `# WHY:` comment + a formula docstring.
- **wiki fixture** `wiki_fix/` — 2 `.md` chunks: one relation living only in a table (a DTC row next
  to a fault), one enum value spelled two ways, and one **seeded doc-bug** (a value asserted that is
  not a real enum member).

## Per-skill assertions (graded)

**`4dlab-code-prep`** (`probe` / `audit` / `report`)
- `audit` flags **all** seeded violations with correct `file:line` (the `import *`, the missing
  `__all__`, the un-annotated public `def`); **zero** false positives on the clean module.
- `probe` produces the three yes/no answers (enum-member node, `# WHY:` rationale node, docstring
  node) from a scoped sample, and the audit's E/R/D rules track those answers.
- The skill makes **no edits** to fixture source (audits, does not rewrite).
- Baseline delta: the bare run typically misses ≥1 violation or hand-edits source.

**`4dlab-wiki-prep`** (`relations` / `labels` / `verify`)
- Appends a `## Graph relations (explicit)` block; **body bytes above the trailer are byte-identical**
  (append-only — assert via diff/SHA256 of the pre-trailer region).
- Every appended relation line is traceable to fixture text — **no invented edges**.
- The seeded doc-bug is written as a non-edge (`… IS_NOT …`), not asserted as a relation.
- The two spellings of the enum value are unified to the shipped form.
- Baseline delta: the bare run rewrites prose, invents an edge, or leaves the doc-bug asserted.

**`4dlab-graphify-run`** (`resolve` → `run` → `relocate` → `verify`)
- Runs graphify **scoped** to `code_fix/` (never `.`/root); relocates `graphify-out/` into a fixture
  dest; confirms no root `graphify-out/` remains.
- `verify` reports node/edge counts and finds the clean module's symbols; collateral check passes.
- When prompted "just graphify everything from the repo root", the skill **refuses / re-scopes** —
  the never-from-root guard holds.
- Baseline delta: the bare run is the control for whether guard + relocate + verify are the skill's add.

**Cross-cutting**
- `4dlab-graph` does **not** trigger for any of these prompts (retired-description check).
- No skill writes to any `graph.json` as a "patch".

## Deliverables

1. `_skills/graph/skilltest-out/iteration-1/REPORT.md` — per-skill with/without comparison, pass/fail
   against each assertion, and the three `probe` answers. (Mirrors T-GFXSKILL-1's REPORT.md target so
   the supersession is a clean swap.)
2. `_skills/graph/skilltest-out/iteration-1/benchmark.{json,md}` + the `--static` review HTML.
3. A **skill-defect log** (in REPORT.md) of anything that failed, for the architect to fix in a
   separate authoring session. **No skill edits in this task.**
4. Fixtures left under `/tmp` (not committed).

## Out of scope

Editing the skills themselves (failures are logged for the architect). Running against any canonical
corpus, wiki, or graph. Any OBDLab source change. Description-optimization (`run_loop.py`) — defer
until the skills are confirmed good; if the owner wants it, it is a follow-up.

## One-task-per-session note

If context runs tight, evaluate **`4dlab-code-prep` first** (it feeds the imminent
`T-KG-OBD-2-PREP`) and move the other two skills to `iteration-1` follow-up runs in a fresh session —
but do not flip this task `done` until all three per-skill blocks are graded and the owner has
reviewed the viewer.

---

# Iteration 2 — re-run with Codex + hardening additions

**Goal of this iteration:** (a) confirm the iteration-1 result is **not an artefact of one executor
model** by re-running the eval with **Codex** as the executor, and (b) close the coverage and
methodology gaps the iteration-1 analysis surfaced. Everything in the spec above still applies —
this section only states the **deltas**. Results go to a new `_skills/graph/skilltest-out/iteration-2/`
tree (do not overwrite iteration-1; it is the comparison baseline).

## Δ1 — Executor model = Codex (cross-model guard check)

Run the with/without subagent runs with **Codex** as the executor model and record it in
`benchmark.json` `metadata.executor_model` (iteration-1 used `deepseek-v4-pro`). The point is the
**model-dependent** results — they must hold regardless of who runs the skill:

- `4dlab-graphify-run`'s **never-from-root guard** must still **REFUSE** the "graphify everything from
  root" prompt on Codex (iteration-1's bare baseline rationalized it away — the guard is the whole
  point).
- The **retired `4dlab-graph`** must still **not trigger** on Codex.

If either flips on Codex, that **is** a skill defect (the guard/description is not robust across
models) — log it for the architect; do not patch the skill in this task.

When generating the viewer, pass `--previous-workspace _skills/graph/skilltest-out/iteration-1` so the
owner sees Codex (iteration-2) beside deepseek (iteration-1) per eval.

## Δ2 — Add positive tests for rules C and S (the coverage hole)

Iteration-1 reported **C=0 and S=0 violations**, so the audit's *detection* of those rules was never
exercised — only their correct absence. Extend the **code fixture** `code_fix/` with a module that
seeds both (still under `/tmp/gfxskilltest/`, never the repo tree):

- **Rule C (dynamic dispatch)** — a real hidden call site, e.g. `handler = getattr(obj, name);
  handler(x)`, or a dispatch dict `{"a": fn_a}[key]()`. The audit must flag it (advisory) with
  `file:line` and explain the missing `calls` edge — and must **not** demand its removal.
- **Rule S (runtime-built symbol)** — a symbol the team would query but that is built at runtime, e.g.
  `Foo = type("Foo", (), {...})` or classes/functions assigned in a loop. The audit must flag it with
  `file:line` as a symbol that will never appear as a node.

Add the matching graded assertions:

- `audit flags the seeded C dispatch site (advisory) with file:line`
- `audit flags the seeded S runtime symbol with file:line`
- `audit still has zero false positives on clean_module.py` (now that C/S exist elsewhere, the clean
  module must remain clean — this guards against over-flagging).

Leave I/A/T/E/R/D fixtures and assertions as in iteration-1. The probe verdict is already pinned
(v0.8.13: enum-member=NO, `# WHY:`=YES, docstring=YES) — re-run the `/tmp` probe **only** to confirm
the graphify build is still v0.8.13; if so, reuse the verdict.

## Δ3 — Benchmark methodology (make the numbers trustworthy)

Iteration-1's headline ("100% vs 33%") compared **uneven assertion sets** (16 with-skill vs 12
baseline) at `runs_per_configuration: 1`, and **lost with-skill timing/tokens** (logged as 0, making
the token "saving" an artefact). Fix all three:

- **Align the graded set across configs.** Grade with-skill and baseline on the **same** assertions
  wherever the check is applicable. For checks that are inherently skill-only (e.g. "ran the probe",
  "retired skill not loaded"), report them in a **separate skill-only block** rather than letting them
  inflate or deflate a shared denominator. State each config's denominator explicitly in `benchmark.md`.
- **`runs_per_configuration` ≥ 2 (3 preferred).** One run per config gives a meaningless stddev. Run
  each (eval × config) at least twice so the viewer's mean ± stddev reflects real run-to-run variance.
- **Capture `timing.json` for BOTH configs.** `total_tokens`/`duration_ms` arrive in the task
  notification and are not persisted elsewhere — write each to its run dir **as the notification
  arrives** (iteration-1 only captured the baseline; with-skill came back 0). If a timing value is
  genuinely unavailable, record `null`, not `0`, so the aggregate does not compute a false delta.

## Iteration-2 deliverables

1. `_skills/graph/skilltest-out/iteration-2/REPORT.md` — Codex with/without per skill; explicit
   cross-model note on the never-from-root guard and retired-skill non-trigger; the new C/S assertion
   results; per-config assertion denominators.
2. `_skills/graph/skilltest-out/iteration-2/benchmark.{json,md}` (`executor_model: codex`,
   `runs_per_configuration ≥ 2`, real or `null` timing) + the `--static` viewer with
   `--previous-workspace iteration-1`.
3. Updated skill-defect log — **only** if a guard/trigger flipped on Codex or C/S detection failed.
   No skill edits in this task.
4. Fixtures (incl. the new C/S module) left under `/tmp`, not committed.

## Iteration-2 out of scope

Editing the skills (defects → architect). Re-deriving the probe verdict unless the graphify build
version changed. Touching iteration-1's tree. Description-optimization (`run_loop.py`).

---

## Verification gate (coder fills)

- All per-skill assertions checked with evidence (file:line for audit hits; SHA256/diff for the
  wiki append-only check; node/edge counts for the run).
- Programmatic where possible: a script asserts `audit hits == seeded violations` and that the wiki
  trailer is append-only (pre-trailer SHA256 unchanged).
- The static review viewer was generated with `generate_review.py --static` and handed to the owner
  **before** the coder's own conclusions; `feedback.json` read and reflected in the defect log.

**Iteration-2 additions to the gate:**
- `benchmark.json` records `executor_model: codex` and `runs_per_configuration ≥ 2`; timing is real
  or `null` (never a stand-in `0`); per-config assertion denominators stated in `benchmark.md`.
- The never-from-root **refusal** and the retired-skill **non-trigger** are confirmed on Codex (a flip
  is logged as a skill defect).
- The seeded **C** dispatch site and **S** runtime symbol are each flagged with `file:line`, and
  `clean_module.py` is still zero false positives.
- Viewer generated with `--previous-workspace iteration-1`; iteration-1 tree untouched.

## CODE REVIEW (coder fills)

(open the progress block with `## Plan`, then `VERIFICATION GATE`, then this block. Confirm: no skill
files edited, no canonical artefact touched, viewer generated via the script not hand-rolled.)
