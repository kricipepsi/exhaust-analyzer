# Code-quality principles every task must encode

This file is **architect-side reading** — the bootstrap skill reads it during
Step 2 (Breakdown) and Step 4 (Generate task files). The coder never loads
this file directly; the principles are *baked into* the artefacts the
bootstrap produces (task files, breakdown checklist, START_HERE working
rules).

Two source bodies are folded together here:

- **Karpathy's four LLM-coding rules** (from `multica-ai/andrej-karpathy-skills`)
- **`Improve Codebase Architecture` skill's four architectural checks** (the
  same checks that keep surfacing issues *after* code is written — we want
  them to fire *before* the code is written)

---

## A. Karpathy rules — applied at task authoring

### A1. Think Before Coding

State assumptions explicitly. If multiple interpretations exist, surface
them. Push back when a simpler approach exists. Stop when confused.

**Where this fires in a task file:**
- `### Context ###` must name the non-obvious design constraint the
  reader could otherwise misread silently.
- If the source prompt is ambiguous, the breakdown plan posted in chat
  must list each ambiguity. Do not silently pick.

### A2. Simplicity First

Minimum code that solves the problem. No features beyond what was asked.
No abstractions for single-use code. No "flexibility" or "configurability"
that wasn't requested. No error handling for impossible scenarios.

**Where this fires in a task file:**
- `### Deliverables ###` lists *only* what the source prompt asks for.
  If the task author finds themselves adding a "while we're here…"
  deliverable, delete it and re-read the source prompt.
- Test: would a senior engineer say this task is overcomplicated? If yes,
  shrink the scope, not the prose.

### A3. Surgical Changes

Touch only what you must. Match existing style. Don't refactor adjacent
code. Every changed line traces directly to a Deliverable. Mention dead
code, don't delete it.

**Where this fires in a task file:**
- `### Files to touch ###` is a closed set, not a starting point.
- `### Out of scope ###` must explicitly forbid drive-by improvements
  the coder will be tempted to make.
- If unrelated bugs exist, log them as `T##b` rows under "Unplanned
  follow-ups" in `PROGRESS.md` — never in the current task's diff.

### A4. Goal-Driven Execution

Define verifiable success criteria. Loop until verified. Transform
imperatives ("add validation", "fix the bug") into declaratives ("the
following test passes").

**Where this fires in a task file:**
- New `### Success criteria ###` section sits between `### Goal ###` and
  `### Context ###`. It lists the test(s) that, when green, mean the
  task is done. Phrased **tests-first** wherever possible:
  - "Add validation" → "`tests/x.py::test_invalid_email_rejected` passes."
  - "Fix the bug" → "`tests/y.py::test_reproduces_issue_42` passes."
  - "Refactor X" → "Existing tests `tests/z.py` pass before and after."
- `### Verification ###` then gives the *commands* to run those tests.
  Success criteria is the contract; Verification is the mechanism.

---

## B. Architecture-quality checks — applied at task authoring

These prevent the four issues `Improve Codebase Architecture` keeps
surfacing after the fact. They use that skill's vocabulary exactly:
**module / interface / depth / seam / adapter** (see
`_skills/Improve Codebase Architecture/LANGUAGE.md`).

### B1. Depth — is the interface shallow?

A **deep** module has a small interface hiding a large amount of
behaviour. A **shallow** module has an interface nearly as complex as
its implementation.

**Where this fires:**
- When `### Deliverables ###` names a new module, ask: what's its
  interface? Could a caller use it without learning its internals?
- If the interface is barely smaller than the implementation, the
  module is shallow — either merge it into its caller, or push the
  complexity inside the seam.

### B2. The deletion test

Before introducing a new module, imagine deleting it. If complexity
*vanishes*, it was a pass-through and shouldn't exist. If complexity
*reappears across N callers*, the module was earning its keep.

**Where this fires:**
- Any task that creates a new abstraction layer must justify it via the
  deletion test in `### Context ###`. One sentence: "If we deleted X,
  complexity would reappear in [N callers / specific places]."

### B3. Seam discipline — one adapter is hypothetical

A seam (port + adapter pattern) is only real when **at least two
adapters** justify it (typically production + test stand-in). One
adapter is just indirection.

**Where this fires:**
- Any task that defines a port / interface must name **both adapters**
  in `### Deliverables ###`. If only one exists, the task should use
  the concrete type directly and revisit if a second adapter ever
  appears.

### B4. The interface is the test surface

Tests should cross the same seam as callers. Tests reaching past the
interface to assert on internal state mean the module is the wrong
shape.

**Where this fires:**
- `### Success criteria ###` tests must be expressible *through* the
  module's public interface. If a test needs to touch internals to
  pass, the task is testing implementation, not behaviour — re-scope.

---

## C. The architect's pre-flight checklist

Run before writing any task file:

1. Have I stated each assumption that the source prompt didn't pin down?
2. Are the Deliverables strictly what the source prompt asks for —
   no speculative additions?
3. Does the `### Out of scope ###` paragraph forbid the most tempting
   drive-by improvement on the affected files?
4. Is there a `### Success criteria ###` that names the test(s) that go
   green when the task is done?
5. If a new module is introduced, does it pass the deletion test, and
   is its interface deep?
6. If a port is introduced, are both adapters listed?
7. Are the success-criteria tests expressible through the module's
   public interface, not its internals?

If any answer is "no", revise the task file before writing it. These
are the same checks `Improve Codebase Architecture` runs *after* code
ships — running them up-front saves the rewrite.

---

## Cross-references

- `breakdown-guide.md` — sizing rules; size and quality intersect at
  the deletion-test boundary (overlarge tasks often hide shallow modules)
- `checklists/breakdown-checklist.md` — mechanical version of section C
  above; apply per task
- `templates/task_file.md` — the `### Success criteria ###` field
  authored by this principle set
- `_skills/Improve Codebase Architecture/` —
  the after-the-fact review skill these checks pre-empt
- Karpathy source: `https://github.com/multica-ai/andrej-karpathy-skills`
