---
name: wired-code-review
description: >
  Mandatory code-review skill for the `wired` composition app (strict mode).
  Load at the start of every wired coder session. Defines the per-diff
  `CODE REVIEW` block. Both this and the VERIFICATION GATE block must be clean in
  `wired_tasks/progress_notes/<task-id>.md` before a task flips to `done`.
  Includes the structural-craft WARNING axis (depth / deletion test / seam
  discipline / interface=test surface).
status: BUILT
---
# wired-code-review — per-diff self-review (strict)

Review the diff against the task's `### Deliverables ###` and the rules below.
Any **blocking** finding = fix before `done`. Produce the `CODE REVIEW` block.

## Blocking findings (must fix)
- **Scope creep.** A changed line that does not trace to a Deliverable. Adjacent
  "improvements" or refactors -> revert; log as a `T##b` follow-up instead.
- **Composition-only breach.** Any diagnostic decision in `wired/`, any edit
  under `labs/`, any import of a second lab from a lab, or an import of the
  deferred fusion path.
- **Unnamed consumer.** A field mapped lab->COMLab with no `# consumer:` comment,
  or a consumer that is a layer ("for COMLab") not a specific reader/branch.
- **Magic number.** A boundary literal with no `# wiki:`/`# dossier:` citation.
- **Missing docstring** on a new public function/mapper.
- **Contract drift unhandled.** A lab output field the mapper silently drops or
  coerces without naming why.

## Structural-craft WARNING axis (note even if non-blocking)
These are the highest-effect review checks; surface them explicitly:
- **Depth.** Is the mapper a thin, single-purpose seam, or has it accreted
  branching that belongs in a lab or in COMLab?
- **Deletion test.** Could any added code/param be deleted with no behaviour
  change? If yes, delete it (Karpathy simplicity).
- **Seam discipline.** Does each lab->COMLab mapping live in exactly one place
  (`composition.py`), or is mapping logic leaking into the runner / tests?
- **Interface = test surface.** Is `diagnose()` exercised through its public
  signature by the tests, not via private helpers?

## The block to paste
```
CODE REVIEW — <task-id>
Scope         : PASS/FAIL  (<every line traces to a deliverable?>)
Composition   : PASS/FAIL  (<no lab edits, no 2nd-lab import, no deferred path>)
Consumers     : PASS/FAIL  (<every mapped field names its reader>)
Literals      : PASS/FAIL  (<boundary numbers cited>)
Docstrings    : PASS/FAIL
Craft (WARN)  : <depth / deletion / seam / interface notes>
Result: CLEAN / BLOCKED (<finding>)
```
