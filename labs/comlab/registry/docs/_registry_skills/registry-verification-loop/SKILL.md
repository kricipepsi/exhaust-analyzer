---
name: registry-verification-loop
description: >
  6-phase outer gate for 4DLab registry task completion. Load at every
  session start. Produces the VERIFICATION GATE block that must appear in
  registry/registry_tasks/progress_notes/<task-id>.md before any task flips
  to done.
allowed-tools: [Read, Bash, Grep]
---

# registry-verification-loop — 6-Phase Outer Gate

This skill owns the **task-completion gate** for the registry workstream.
A task is not done until all 6 phases below are clean. The output is a
structured `VERIFICATION GATE` block written to
`registry/registry_tasks/progress_notes/<task-id>.md`.

---

## The 6 phases

Run in order, from the workspace root `C:\Users\muto\claude\4DApp\4DLab\`
with the `.venv-wired` (Python 3.14) environment active. A failure in any
phase blocks task completion — either fix in this session or flip the task
to `blocked` with a reason.

### Phase 1 — Syntax and lint

For any Python files touched in this task:

```bash
cd C:\Users\muto\claude\4DApp\4DLab
ruff check registry/ --fix
```

For any JSON files touched in this task:

```bash
python -c "import json, sys, pathlib; [json.loads(p.read_text()) for p in pathlib.Path('registry').rglob('*.json')]"
```

Pass condition: exit 0; no remaining violations; every JSON parses.

### Phase 2 — Type checking

```bash
pyright registry/
```

Pass condition: 0 errors. Warnings are allowed (document them if surprising).

### Phase 3 — Unit tests

```bash
pytest registry/tests/ -x -q
```

Pass condition: all green, no failures, no errors. If the `registry/tests/`
folder is empty for a given task (audit-only tasks emit data, not code),
record this as PASS with note `no tests in scope`.

### Phase 4 — Task-specific verification

Run the commands in the task file's `### Verification ###` section verbatim.
Pass condition: every command exits 0 and produces the expected output.

### Phase 5 — Rule-set integrity (module-specific gate)

This phase is the registry's standing gate. It replaces 4DLabWired's
harness-regression gate. Three sub-checks; all three must PASS.

**5a. Schema validity** — every JSON rule file in `registry/rules/`
validates against `registry/schema_v2.py` (once schema_v2.py exists; for
audit-only tasks before v2 schema, record N/A with reason).

```bash
python -c "import registry.schema_v2 as s, json, pathlib; \
  [s.Rule.model_validate_json(p.read_text()) for p in pathlib.Path('registry/rules').glob('*.json')]" \
  && echo "schema-ok"
```

**5b. Case-ID resolution** — every `passes_cases:` entry in every rule
file resolves to a row in `registry/corpus_curated.csv` (once
corpus_curated.csv exists).

```bash
python -m registry.tools.resolve_cases --strict
```

**5c. Harness side-by-side (REG-V2-INTEGRATE onward only)** — when the v2
registry is wired into COMLab behind a flag, run the harness against both
v1 and v2 and confirm:

```bash
python 4DLabWired/harness/run_cases.py --registry v2 > harness_v2.txt
python 4DLabWired/harness/run_cases.py --registry v1 > harness_v1.txt
```

Pass condition: **v2 PASS count ≥ v1 PASS count on the curated corpus**.
Any regression on a v1-passing case is blocking — no exceptions.

For tasks before the schema, the rules, or the integration shim exist,
record N/A on the corresponding sub-check with a one-line reason.

### Phase 6 — Scope check

Manually verify:
- Every changed line traces to a Deliverable in the task file.
- No files outside the task's `### Files to touch ###` list were modified
  (unless documented as an unplanned follow-up in `REGISTRY_PROGRESS.md`).
- No imports from any lab, COMLab, or 4DLabWired (registry is self-contained).
- No rule edited without an updated `passes_cases:` list.
- No numeric threshold added or changed without a `// wiki:` citation.

Pass condition: all clean.

---

## VERIFICATION GATE block (paste into progress_notes/<task-id>.md)

```
## VERIFICATION GATE — <TASK_ID>

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS / FAIL | (violations count or "0 violations"; JSON files validated count) |
| 2 | pyright | PASS / FAIL | (errors count or "0 errors") |
| 3 | unit tests | PASS / FAIL | (N passed / M failed, or "no tests in scope") |
| 4 | task verification | PASS / FAIL | (commands from task file) |
| 5a | rule schema validity | PASS / FAIL / N/A | (N rules validated, or reason for N/A) |
| 5b | case-ID resolution | PASS / FAIL / N/A | (orphan refs count, or reason for N/A) |
| 5c | harness side-by-side | PASS / FAIL / N/A | (v1 PASS vs v2 PASS, or reason for N/A) |
| 6 | scope check | PASS / FAIL | (any out-of-scope edits?) |

**Overall: PASS / FAIL**

If FAIL: reason and next action.
```

Fill in the table, replace PASS/FAIL, add details. If any row is FAIL, do
not flip the task to `done` — fix first or escalate.

---

## Gate failure protocol

1. **Fix in this session** if the fix is < 30 min and < 3 files.
2. **Create a follow-up row** in `REGISTRY_PROGRESS.md` "Unplanned
   follow-ups" if the fix is larger — flip the task to `done` with a note,
   record the follow-up.
3. **Flip to `blocked`** if the fix requires architect input or a design
   decision — write the blocking question explicitly.

---

## Cross-references

- `registry-python` — the per-file inner loop that precedes this outer gate
- `registry-code-review` — the CODE REVIEW block; both must be clean to flip `done`
