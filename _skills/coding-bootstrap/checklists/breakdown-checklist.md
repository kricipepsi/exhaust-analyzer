# Breakdown checklist — verify a task is genuinely half-session

Apply to every task file before writing it. If any answer is "no", split
the task and re-run the checklist on each half.

## Size

- [ ] Files touched ≤ 12 (soft cap 5)
- [ ] New/changed lines ≤ 800 (soft cap 300)
- [ ] New tests ≤ 25 cases (soft cap 8)
- [ ] External tools used ≤ 3 (soft cap 1)
- [ ] Architectural decisions made ≤ 5 (soft cap 2)

### Per-unit workload (DO NOT skip — this is the failure mode that blows budgets)

A task whose deliverable count looks small can still overflow if each
deliverable hides a per-unit inner loop. Size the **actual work the coder
performs**, not the number of files written.

- [ ] If a deliverable is a list / table / CSV / audit log with **N rows**,
      multiply: `N × per-row work` (read source, run check, cite wiki,
      write line). If `N ≥ 20` and per-row work involves any of {tool call,
      grep, file read, recompute, wiki lookup}, **split**.
- [ ] If a task replays a function over a fixture set (`process()`, decode,
      validate) and records each result, count one unit of work per replay.
- [ ] If a task audits / triages candidates (keep-or-drop with reasoning),
      count one unit of work per candidate considered — not per candidate
      kept.
- [ ] Rule of thumb: **20 units of per-row work ≈ one half-session task.**
      A 50-row audit is two tasks (extract + characterize → audit + reject).
      A 100-row migration is three.

Worked example of this failure: T-GAS-6 in
`4DLab/TestSuite/TESTSUITE_PROGRESS.md` shipped
as one task with one deliverable (`gaslab_suite_AUDIT.md`) but carried
~50 candidates × per-row replay-and-cite work. It hit the context wall mid-
audit. The fix in retrospect: split into T-GAS-6a (extract + characterize,
emit raw candidate list with `process()` outputs) and T-GAS-6b (audit +
reject + cite, consume the list and emit the audit log). One audit log,
two tasks.

## Shape

- [ ] Task ID + filename follow `T-<CODE>-<N>_<three_word_slug>` (snake_case,
      ~3 descriptive words after the code and number); the filename slug and the
      PROGRESS.md row ID match exactly. See SKILL.md "Task file naming convention".
- [ ] Goal can be stated in one paragraph naming a concrete artefact.
- [ ] Deliverables list has ≤ 6 items.
- [ ] Verification commands are all copy-pasteable and produce pass/fail.
- [ ] Out-of-scope section names at least one tempting thing the task does NOT do.
- [ ] No deliverable depends on a file the task itself doesn't create or
      modify, unless that file is created by a `Blocked by` task already
      in `PROGRESS.md`.
- [ ] No unfilled `{UPPER_SNAKE}` template placeholder remains in the file
      (`grep -nE '\{[A-Z][A-Z0-9_]{2,}\}'` returns nothing but legitimate
      literals) — a stray `{TASK_ID}`/`{REPO_ROOT}` means a template token was
      never filled.

## Independence

- [ ] If the agent runs this task in a fresh session with no memory of
      prior tasks, the bootstrap (`START_HERE.md`) + the task file gives
      enough context to start.
- [ ] No section says "you'll remember from earlier" or assumes prior
      conversation.
- [ ] All external paths (skill paths, file paths, repo paths) are
      absolute, not relative to some implicit cwd.

## Verification rigor

- [ ] Verification block includes language Inner Loop commands.
- [ ] Verification block includes at least one structural check (file
      exists, function present, contract held).
- [ ] Verification block includes at least one functional check (test
      passes, smoke check succeeds).
- [ ] Failure of any single verification command means the task is NOT
      done (no "best effort" pass).

## Quality (Karpathy + architecture pre-checks)

See `reference/code-quality-principles.md` for the full rules.

- [ ] `### Success criteria ###` names the test(s) that go green when the
      task is done — phrased tests-first ("test X passes"), not imperative
      ("add validation").
- [ ] Deliverables list is strictly what the source prompt asks for — no
      speculative additions, no abstractions for single-use code, no
      configurability that wasn't requested.
- [ ] `### Out of scope ###` forbids the most tempting drive-by improvement
      on the touched files. Surgical-change rule: every changed line traces
      to a Deliverable.
- [ ] **Signal/noise consumer is named in the spec, not deferred to the coder.**
      If any deliverable adds or widens a schema (field, enum, fault, signal),
      the `### Consumer (signal/noise) ###` field names a specific consumer
      (COMLab analytics / fault-atlas routing) AND the exact `file.py::function`
      that reads it — or marks it `PROPOSAL` with the same-diff reader and a
      proposals-registry path. An unnamed consumer is a spec defect (the coder
      will stall on it mid-session): fix the task file, don't ship it.
- [ ] If the task introduces a new module, it passes the **deletion test**:
      removing it would re-spread complexity across N callers, not just
      vanish it.
- [ ] If the task introduces a port / interface seam, **both** adapters
      (production + test, or two real production adapters) are in the
      Deliverables list. One-adapter seams are forbidden.
- [ ] Success-criteria tests are expressible through the module's public
      interface — no asserting on internals.

## Disclosure (progressive disclosure)

- [ ] If this task *reveals* a fact a later decision needs (a number,
      residual, feasibility), it is `Blocked by`-upstream of the tasks that act on it.
- [ ] No task both *discloses* a fact and *commits* a policy calibrated on it;
      if it did, it was split and the commit task is `Blocked by` the disclosure.
- [ ] Measurement/checkpoint tasks tier their output essential-first (headline
      → summary → per-case detail in JSON), not one flat dump.
- [ ] The task names what it must **surface, not hide** — a shortfall or
      surprise is reported, never dressed as complete.
- [ ] For step-by-step packs: only the next runnable task is authored in full;
      the rest are forward-registered ledger rows, not committed specs.

## Skill coverage (cross-task — the skipped-authoring guard)
This is the one check that spans task files, so run it when the *pack* is drafted,
not just per task. See `reference/custom-skill-authoring.md`.
- [ ] If this task's `### Context ###` inlines a non-obvious invariant (naming
      rule, forbidden pattern, threshold table, schema convention) that >= 2
      other task files also inline, that surface has crossed the >= 3-task
      threshold — author or promote an on-demand skill and replace the inline
      copies with a `Load skills:` line, instead of inlining a third time.
- [ ] Every skill named on this task's `Load skills:` line exists in `_INDEX.md`
      and on disk (no phantom skill reference; the inverse orphan/under-author
      pair is verified in SKILL.md Step 5 items 3 and 8).

## If you fail any item

- **Size fail** → split. Often: discovery becomes its own task, or tests
  become their own task.
- **Shape fail** → tighten language. If you can't tighten without losing
  meaning, the task scope is muddled — split or rewrite the Goal.
- **Independence fail** → either move the missing context into Context,
  or add a `Blocked by` dependency on the task that produces it.
- **Verification fail** → add the missing checks. If you can't (e.g., the
  contract is too fuzzy to mechanically check), surface this to the user;
  fuzzy verification is the V1 plateau bug.
- **Quality fail** → revise before writing. A shallow module or speculative
  adapter that slips into a task file becomes a finding in `Improve
  Codebase Architecture` later — running these checks up front saves the
  rewrite. See `reference/code-quality-principles.md`.
