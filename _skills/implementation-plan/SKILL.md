---
name: implementation-plan
description: >
  Author a machine-readable implementation plan document for a feature, module,
  refactor, upgrade, or architecture change. Load this skill whenever the user
  says "prepare implementation plan", "create a plan for <X>", "plan the
  implementation of <proposal/HLD/spec>", or hands you a design document that
  must become an executable plan. The output is a single deterministic Markdown
  plan (phases → atomic tasks) that AI coder agents or humans can execute
  without interpretation. Use BEFORE any coding-session bootstrap: the plan is
  the input that a later coding-bootstrap run atomizes into a task pack.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---
# Implementation Plan Skill

Produces one plan file that is **fully executable without interpretation**:
deterministic language, explicit paths/literals, phases with measurable
completion criteria, and standardized identifiers. The plan is AI-to-AI
communication — every sentence is either executable or validation criteria.

## Relationship to coding-bootstrap

This skill writes the **plan**; `_skills/coding-bootstrap` later turns an
approved plan into the five-piece session infrastructure (task pack,
START_HERE, PROGRESS, skill bundle). Do not generate that infrastructure here.
But author every phase so the handoff is mechanical — the sizing and quality
rules below are lifted from coding-bootstrap so its breakdown step becomes a
1:1 mapping from plan phases to task files.

## Procedure

### Step 0 — Read sources and surface ambiguity
Read the source design doc(s) the user names, plus the project `CLAUDE.md`
(locked facts there override older statements in the design doc — note each
override explicitly in the plan). List open questions from the source doc.
Classify each: **resolved** (cite where), **blocking** (plan must front-load a
disclosure task), or **deferred** (out of scope, say why). Ask the user only
about ambiguities that change the plan's shape (stack, scope, consumers) —
don't guess, per the owner's rules.

### Step 1 — Fix scope
Write the goal in one sentence. List explicit non-goals from the source doc.
If scope is "limited/reworked from <existing module>", read the existing
module's structure (file list + key contracts, not whole files) and pin in the
plan exactly which behaviours are kept, which are dropped, and where the
authoritative domain knowledge stays (it is NOT re-authored in the new module).

### Step 2 — Derive requirements
Extract requirements as identifier rows: `REQ-` (functional), `SEC-` (safety/
security), `CON-` (constraints), `GUD-` (guidelines), `PAT-` (patterns to
follow). Every row cites its source (`doc §N` or `file:line`). No requirement
without a source; no source read wider than needed (READ-NARROW).

### Step 3 — Phase the work (sizing + ordering rules)
Break implementation into phases of atomic tasks. Rules, all load-bearing:
- **Half-session sizing.** Each task ≤ 50% of a fresh coder session: ~5–15
  files, ~200–600 lines incl. tests. A task bigger than that gets split.
- **Disclosure-first ordering.** A task that *reveals* a fact (a format, a
  measured value, a feasibility) is upstream of every task that *commits* to a
  decision that fact informs. If one task does both, split it.
- **Measurable completion.** Every phase has completion criteria a machine can
  check (a test passes, a file round-trips byte-identical, a value matches).
- **Named consumer.** Any task that adds a schema element (field, enum, fault,
  signal) names the consumer `file.py::function` that reads it. No orphans.
- **Pinned citations.** Task descriptions cite exact sections/literals
  (`WIKI §N.M`, `config key = value`) so the coder can read 60 lines, not 25k.
- **Parallel by default.** Tasks in a phase are parallel unless a `Blocked by`
  dependency is declared.

### Step 4 — Fill the template
Use `templates/plan_template.md`. Every section is required; no placeholder
text may survive. Front matter must be complete and valid. Status starts
`Planned` (blue badge) and is shown as a badge in the introduction.

### Step 5 — Validate before handing back
Mechanical checks — run them, don't eyeball:
1. All front-matter fields present; status is one of Completed / In progress /
   Planned / Deprecated / On Hold.
2. Section headers match the template exactly (case-sensitive).
3. Every identifier uses its prefix and is unique (`grep -oE '(REQ|SEC|CON|GUD|PAT|GOAL|TASK|ALT|DEP|FILE|TEST|RISK|ASSUMPTION)-[0-9]+'` | sort | uniq -d → empty).
4. Every task table has all required columns; every TASK- row has explicit
   file paths or names a disclosure that will produce them.
5. No `{PLACEHOLDER}`, `TBD`, or "see the doc" without a pinned citation.
6. Blocking open questions from Step 0 each map to an early disclosure task.

## Output location & naming
Save to `<project_root>/plan/[purpose]-[component]-[version].md`.
Purpose ∈ `upgrade|refactor|feature|data|infrastructure|process|architecture|design`.
Example: `feature-vemseco-1.md`. Create `plan/` if absent.

## Anti-patterns
- **The narrative plan.** Prose that explains instead of instructs. If a
  sentence can't be executed or checked, delete it.
- **The interpretive task.** "Handle errors appropriately", "integrate with
  X as needed" — requires a human decision mid-execution. Pin the decision in
  the plan or front-load a disclosure task.
- **The re-authored domain.** Copying domain knowledge from a source module's
  wiki into the plan. Reference the boundary contract instead; the knowledge
  stays where it lives.
- **The unsourced literal.** A threshold, axis, or scaling factor stated
  without `file:line`/`§` provenance. Reality wins over memory — cite it.
- **The pre-committed phase.** Scheduling decision-gated work before the task
  that discloses whether it's warranted (see disclosure-first, Step 3).
