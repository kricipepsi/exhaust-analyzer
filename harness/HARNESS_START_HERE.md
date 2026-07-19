# HARNESS — Session Bootstrap (Generative Test Harness)

This file is a **procedure, not documentation**. Execute it step by step before
producing any other output. Do not ask the user what to work on until the
bootstrap is complete.

## 0. Environment

Restore sandbox Python 3.14 first (see `4DLab/CLAUDE.md → Sandbox Python` — open
only that section; do not re-`Read` the whole ~14 k `CLAUDE.md`, it auto-loads as
a project rule). Invoke as `python3.14`. Never bare `python`/`python3` (3.10).

## 0a. CONTEXT BUDGET — read narrow (read this before any Read)

The recurring failure is the bootstrap eating ~half of context **before code
starts**, by whole-reading large reference files the task does not need. The
task file is the spec; it pins the exact sections, files, and box rows. **Read
the task file, then read only what it names.**

**Bootstrap budget: ≤ 30 k tokens of reads before the first edit.** Past that,
you are reading too wide — stop and narrow.

**READ-NARROW rule (hard):**
- **Never whole-read** `PER_MODULE_TESTSUITE_DESIGN_SPEC.md` (~4.4 k, 392 L),
  `HARNESS_PROPOSAL.md`, `CLAUDE.md` (~14 k), `gas_lab_ontology.yaml` (~8 k), or
  any `tests/test_*.py` (~9 k). These are reference/working files, not preamble.
- Open the cited part only, by line range: `grep -n "<§ or anchor>" <file>` then
  `Read` with `offset`/`limit` (≈ 60 lines) — not the whole file. For code, read
  the **target function** (`grep -n "def <name>"`), not the module; whole-read a
  code file only if it is < ~150 lines.
- A truncation warning means you read too wide — re-do it scoped.

## 1. Find the next task, then read only what it names (in order)

1. `TestSuite/harness/HARNESS_PROGRESS.md` — the ledger. **This is the only file
   that tells you the next task.** Read the task table; apply the stale-ledger
   guard before proceeding.
2. The matching task file `harness_tasks/<task-id>_*.md` **end-to-end** (these
   are small, ~2–5 k). It pins the files to touch, the cited design-spec
   sections, and the tests. **Everything else you read is dictated by it.**
3. `TestSuite/PER_MODULE_TESTSUITE_DESIGN_SPEC.md` — read **only** the section
   the task file cites (e.g. §5 GASLab is the pilot consumer's contract), by line
   range. Do not whole-read it.
4. `TestSuite/harness/HARNESS_PROPOSAL.md` — consult **only** if the task file
   points at a specific menu item / isolation rule you need; read that span only.

## 2. Mandatory skills

Load the GASLab coding skills used by the pilot consumer: `gaslab-python`,
`gaslab-verification-loop`, `gaslab-code-review`, and `gaslab-wiki-provenance`
(box-table / numeric-literal edits carry wiki citations). Do **not** load the
rest of the bundle.

These are **not registered under `~/.claude/skills/`** — they are plain
`SKILL.md` files in the GASLab tree. Read them by path:
`GASLab/_gaslab_skills/<skill-name>/SKILL.md` (e.g.
`GASLab/_gaslab_skills/gaslab-python/SKILL.md`). "Load" here means Read those
files, not invoke a registered skill.

## 3. Pick the next task

In `HARNESS_PROGRESS.md`, find the **first `pending` task whose `Blocked by` is
clear**. Linear sequence: T-TH-0 → {T-TH-1, T-TH-2} → T-TH-3..7 → T-TH-8.

- **The coder does NOT author task files.** Task specs are pre-authored by the
  architect/owner. If the next row still reads `_author at start_` or has no
  task-file path, **STOP and ask the owner to author it** — do not write the
  spec yourself. (Decision 2026-06-04: coder-authored specs produced unreliable
  scope; authoring moved owner-side.)
- Implement only against a task file that already exists with a full spec
  (Goal, Success criteria, Context, Deliverables, Files to touch, Out of scope,
  Verification). Stop and ask one clarifying question only for a **critical
  ambiguity** (unnamed signal/noise consumer; a files/scope question the spec
  does not resolve and you cannot resolve from the repo; a cited literal/section
  that does not exist) — never edit the spec. Anything you can resolve from the
  task file or repo is not critical: proceed.

## 4. Confirm scope (one paragraph), then proceed

Name: the files you will touch, the tests you will write, and the **named
signal/noise consumer** (which forked suite runs this generator). **After
posting it, proceed directly to coding — do not wait for the user to confirm.**
Stop only for a **critical ambiguity**: you cannot name the signal/noise
consumer, or a files/scope question the task file does not resolve and you
cannot resolve from the repo. On those, ask one clarifying question — do not
guess. Everything else: note the assumption and continue.

## 5. Work order (strict, per task)

read skill → confirm scope → code → inner loop (`ruff` → `pyright` →
`pytest -x -q`, after **every** meaningful edit) → VERIFICATION GATE →
CODE REVIEW → both clean in `harness_tasks/progress_notes/<task-id>.md` → flip
ledger row to `done`. Reports are `.md` only. One task per session.

## 6. Git

Only action is the final commit, run **by the user** in PowerShell, staging
deliverables by **explicit path** (`4DLab/CLAUDE.md → Git`). Never `git add -A`.
When the staged paths wrap across lines, end each line with a PowerShell
line-continuation **backtick** (`` ` ``) — never `\`, never `;` — so the user can
paste the whole block into the terminal as one command without a broken line:

```powershell
git add `
  TestSuite/harness/harness/generators/foo.py `
  TestSuite/harness/harness_tasks/progress_notes/T-TH-N.md
git commit -m "T-TH-N: <one-line summary>"
```

The backtick must be the **last** character on the line (no trailing space).
