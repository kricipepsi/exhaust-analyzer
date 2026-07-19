# T-GFXSKILL-1 — Acceptance test for the three graphify skills

> **SUPERSEDED 2026-06-09 by `T-GFXSKILL-2_skillcreator_eval_loop.md`.** Do not run this manual
> version as a separate task. T-GFXSKILL-2 runs the same fixtures and the same per-skill criteria
> through the `skill-creator` eval harness (parallel with/without subagent runs → graded assertions
> → benchmark → `--static` review viewer). This file is retained as the **source of the fixtures and
> the per-skill assertions** that T-GFXSKILL-2 reuses; the prose below is still the authoritative
> spec for *what* each skill must do — only the *runner* changed.

**Status:** `superseded by T-GFXSKILL-2` · **Author:** architect · **Date:** 2026-06-09 · **Mode:** STRICT
**Skills under test:** `4dlab-code-prep`, `4dlab-wiki-prep`, `4dlab-graphify-run`
(all under `_skills/graph/`). **Retired:** `4dlab-graph` (must not trigger).

## Goal

Prove each skill does what it claims **and** that loading it changes behaviour for the better,
using **small throwaway fixtures only** — never canonical source, wiki, or any `graph/*` /
`graphify-out/` artefact. This is a tooling-acceptance test, not an OBDLab ledger task; it touches
no production code and emits no schema field, so the signal/noise field-rule does not bite.

## Method (with vs without)

For each skill, the coder runs the same fixture task **twice** — once with the skill loaded, once
with no skill — and compares. The skill earns its place only if the with-skill run is materially
better (catches what the bare run misses, or respects a guard the bare run violates). Record both
transcripts under `_skills/graph/skilltest-out/<skill>/{with,without}/`.

## Fixtures (coder creates under `/tmp/gfxskilltest/`, never in the repo tree)

- **code fixture** `code_fix/` — a tiny package: an `__init__.py` with **no** `__all__`; one module
  using `from x import *`; one public `def` with **no** type hints; one clean module with explicit
  imports + `__all__` + hints + a `StrEnum` + a `# WHY:` comment + a formula docstring.
- **wiki fixture** `wiki_fix/` — 2 `.md` chunks: one with a relation that lives only in a table
  (e.g. a DTC row next to a fault), one enum value spelled two different ways, and one **seeded
  doc-bug** (a value asserted that is not a real enum member).

## Per-skill success criteria

**`4dlab-code-prep`** (operations `probe` / `audit` / `report`)
- `audit` flags **all** seeded violations with correct `file:line`: the `import *`, the missing
  `__all__`, the un-annotated public `def`. **Zero** false positives on the clean module.
- `probe` produces the three yes/no answers (enum-member node, `# WHY:` rationale node, docstring
  node) from a scoped sample run — and the audit's E/R/D rules track those answers.
- The skill makes **no edits** to fixture source (it audits, it does not rewrite).
- Without-skill baseline: bare run typically misses ≥1 violation or hand-edits source — the delta.

**`4dlab-wiki-prep`** (operations `relations` / `labels` / `verify`)
- Appends a `## Graph relations (explicit)` block; **body bytes above the trailer are byte-identical**
  (append-only — verify with a diff of the pre-trailer region).
- Every appended relation line is traceable to fixture text — **no invented edges**.
- The seeded doc-bug is written as a non-edge (`… IS_NOT …`), not asserted as a relation.
- Canonical labels: the two spellings of the enum value are unified to the shipped form.
- Without-skill baseline: bare run typically rewrites prose, invents an edge, or leaves the doc-bug
  asserted — the delta.

**`4dlab-graphify-run`** (flow `resolve` → `run` → `relocate` → `verify`)
- Runs graphify **scoped** to `code_fix/` (never `.`/root); relocates `graphify-out/` into a fixture
  dest and confirms no root `graphify-out/` remains.
- `verify` reports node/edge counts and finds the clean module's symbols; collateral check passes.
- When prompted to "just graphify everything from the repo root", the skill **refuses / re-scopes** —
  the never-from-root guard holds.
- Without-skill baseline: bare run is the control for whether the guard + relocate + verify are what
  the skill adds.

**Cross-cutting**
- `4dlab-graph` does **not** trigger for any of these prompts (retired-description check).
- No skill writes to any `graph.json` as a "patch".

## Deliverables

1. `_skills/graph/skilltest-out/REPORT.md` — per-skill with/without comparison, pass/fail against
   each criterion above, and the three `probe` answers.
2. Fixtures left under `/tmp` (not committed).

## Out of scope

Editing the skills themselves (failures are logged for the architect to fix); running against any
canonical corpus or graph; any OBDLab source change.

## Verification gate (coder fills)

- All per-skill criteria checked with evidence (file:line for audit hits; diff for append-only).
- Programmatic where possible: a script asserts audit hits == seeded violations, and asserts the
  wiki trailer is append-only (pre-trailer SHA256 unchanged).

## One-task-per-session note

If context runs tight, run **`4dlab-code-prep` first** (it feeds the imminent code-prep work) and
move the other two skills to a follow-up session — do not flip this task `done` until all three
per-skill blocks are filled.

## CODE REVIEW (coder fills)

(open the progress note with `## Plan`, then `VERIFICATION GATE`, then this block.)
