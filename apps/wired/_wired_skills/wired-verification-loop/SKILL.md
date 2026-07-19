---
name: wired-verification-loop
description: >
  Mandatory verification skill for the `wired` composition app (strict mode).
  Load at the start of every wired coder session. Defines the 6-phase outer gate
  and the `VERIFICATION GATE` block pasted into
  `wired_tasks/progress_notes/<task-id>.md` at session end. A task does not flip
  to `done` until this block is clean.
status: BUILT
---
# wired-verification-loop — the outer gate (strict)

Run this at task end, after the per-file Inner Loop has been green throughout.
Produce the `VERIFICATION GATE` block below and paste it into the task's progress
note. Any failed phase = **stop**; fix in-session or hand back `blocked`.

## The 6 phases
1. **Syntax/compile** — `py_compile` on every file touched, clean.
2. **Lint** — `ruff check` on every file touched, clean.
3. **Types** — `pyright` on `apps/wired/`, 0 errors. (Run `cd apps/wired; pyright .`
   if the root-level invocation cannot discover `apps/wired/pyproject.toml` — a
   known prior gotcha, `U-WV2-3`.)
4. **Tests** — the task's `### Verification ###` test commands, all green. Run
   from a neutral cwd (`/agent_workspace`) so editable lab packages resolve.
5. **Contract/structural** — the task's structural checks (file/function present,
   `diagnose()` returns `OrchestratorFinalUIOutput`, deferred path absent, every
   mapped field has a `# consumer:` comment).
6. **Anti-orphan** — if the task added/mapped a field with a named consumer,
   `grep` that consumer name and confirm it is actually **read** in the live
   COMLab path the task named, not just defined.

## The block to paste
```
VERIFICATION GATE — <task-id>
1. Compile : PASS/FAIL  (<files>)
2. Lint    : PASS/FAIL  (ruff)
3. Types   : PASS/FAIL  (pyright, N errors)
4. Tests   : PASS/FAIL  (<command> -> N passed)
5. Contract: PASS/FAIL  (<what was asserted>)
6. Orphan  : PASS/FAIL/N-A  (<consumer grep result>)
Result: CLEAN / BLOCKED (<reason>)
```
