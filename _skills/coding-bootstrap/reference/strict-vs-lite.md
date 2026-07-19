# Rigor profile: strict vs lite

A project picks one profile for its entire life. Don't mix.

## Strict — the V2 regime

Use when **any** of:

- Project will run > 10 tasks.
- Project has architectural invariants that silent regressions could break
  (multi-module pipeline, schema contracts, model accuracy).
- More than one coder will work on it (you + future you counts).
- Project will be deployed and is hard to roll back.

What you get:

- 4 mandatory skills loaded at every session start (language + design rules +
  verification-loop + code-review).
- On-demand skill load based on which files the task touches.
- Per-file Inner Loop after every edit.
- Per-task `### Verification ###` block.
- 6-phase outer `VERIFICATION GATE` block (pasted into `progress_notes/`).
- Per-diff `CODE REVIEW` block (pasted into `progress_notes/`).
- Both gate blocks must be clean before the task flips to `done`.

What it costs:

- ~10–20 % more time per task (running the gates, writing the blocks).
- Discipline overhead — agent must not be tempted to skip a gate.

What it prevents:

- The V1 plateau. Forty-four percent accuracy that twenty remediation
  tasks couldn't fix, because every fix introduced silent regressions
  the gate would have caught.

## Lite — fast iteration

Use when **all** of:

- Project will run < 10 tasks.
- Single-author, short-lived, easy to throw away.
- No deployed system depends on it.
- The cost of a regression is "redo this task", not "production incident".

What you get:

- Language skill loaded at session start (the Inner Loop is still mandatory).
- Workspace CLAUDE.md loaded.
- Per-file Inner Loop after every edit (this is in the language skill — not
  optional).
- Per-task `### Verification ###` block. Must pass before commit.
- Commit + update PROGRESS.md row.

What you skip:

- Design-rules skill load (no separate design-rules skill exists for the
  project).
- verification-loop and code-review skill loads.
- The `VERIFICATION GATE` and `CODE REVIEW` blocks.
- `progress_notes/` per-task files.

What it costs:

- You will catch some bugs at the next task (because no diff review now)
  or in integration (because no outer gate). Worth it if the project is
  small enough that this catch-up cost stays below the gate-running cost.

## How to convert a template from strict to lite

Every block in `templates/start_here.md` that starts with `**[STRICT-ONLY]`
or is gated by `STRICT_OR_LITE` / `STRICT_GATE_CONFIRMATION_FRAGMENT`:
delete it in lite mode. Specifically:

| Section in `start_here.md` | Strict | Lite |
|---|---|---|
| Bootstrap step 2 (design rules) | KEEP | DELETE |
| Bootstrap step 4 (verification-loop) | KEEP | DELETE |
| Bootstrap step 5 (code-review) | KEEP | DELETE |
| Session-end step 2 (VERIFICATION GATE) | KEEP | DELETE |
| Session-end step 3 (CODE REVIEW) | KEEP | DELETE |
| Session-end step 5 progress-notes paragraph | KEEP | DELETE |
| Confirmation line fragment | "both blocks clean" | drop the fragment |

In `templates/task_file.md`, the `Load skills:` line in Context becomes
optional (only if a project skill exists).

In `templates/progress.md`, the "Phase gates" section is optional in
either profile — keep it only if the project has them.
