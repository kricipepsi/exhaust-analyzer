---
name: comlab-verification-loop
description: >
  Comprehensive verification system for COMLab coding sessions — syntax, type-check,
  lint, pytest, wiki-drift / anti-orphan guard, and diff review before declaring any
  task done. Owns the VERIFICATION GATE block written into
  tasks/progress_notes/<task-id>.md. Python 3.14-only.
origin: adapted from _obdlab_skills/obdlab-verification-loop/SKILL.md
updated: 2026-06-21 (initial build — COMLab Stage-4 bundle)
---

# comlab-verification-loop — Outer Gate for COMLab Tasks

A comprehensive verification system for COMLab coding sessions. This is the
task-completion gate; the per-file inner loop is owned by `comlab-python`.

---

## When to invoke

- After completing any COMLab task before flipping its status to `done` in
  `tasks/PROGRESS.md`.
- Before declaring a refactor complete.
- After any change that touches `comlab/schemas/`, `comlab/core/`,
  `comlab/analytics/`, or `comlab/config/`.

---

## The interpreter (every command)

```bash
cd labs/comlab
PY=/agent_workspace/.venv-wired/bin/python   # shared venv (Py 3.14); or: source /agent_workspace/.venv-wired/bin/activate
"$PY" --version            # must print Python 3.14.x — stop if not
```

Python 3.14 ONLY. Never system `python3` or any 3.11/3.12/3.13. Purge stale
`__pycache__` if a `.pyc` shadows an edit.

---

## Verification Phases

### Phase 1 — Syntax & import check

```bash
"$PY" -m py_compile comlab/<changed_file>.py && echo "PASS" || echo "FAIL"
"$PY" -c "import comlab.<module>" && echo "IMPORT_PASS" || echo "IMPORT_FAIL"
```

Every `.py` under `comlab/` must import cleanly with no side effects.

### Phase 2 — Type check

```bash
pyright comlab/ 2>&1 | head -30
```

`pyrightconfig` must pin `pythonVersion` 3.14. Report all type errors; fix before
continuing.

### Phase 3 — Lint check

```bash
ruff check comlab/ 2>&1 | head -30
```

Zero warnings on changed files. Pre-existing warnings on untouched files: OK, but
note in `progress_notes/<task-id>.md`.

### Phase 4 — pytest suite — MANDATORY

```bash
"$PY" -m pytest -x -q
```

**This must be green before any task is declared done.** If a previously-passing
test now fails, stop and log a blocker in the progress notes. If the task touches
`registry/`, also run `"$PY" -m pytest registry/tests/ -q` (separate package).

### Phase 5 — Wiki drift / anti-orphan guard (COMLab-specific)

This phase replaces the emitter labs' sensor-bounds drift guard with COMLab's two
governing checks:

```bash
# (a) Wiki provenance — every numeric literal / enum added in the diff cites a wiki §
git diff HEAD -- comlab/ | grep -nE '^\+' | grep -nE '[0-9]' | grep -vE '# wiki:|wiki_ref|version|line [0-9]' || echo "NO_UNSOURCED_NUMERICS"

# (b) Anti-orphan — any field the task contracts to consume is grep-confirmed read in a live path
grep -rn "<consumed_field_name>" comlab/ --include=*.py | grep -vE 'schemas/|test'   # must show a real read site, not just the schema definition
```

The guard verifies:

- Every enum value / numeric threshold added in `comlab/` carries a
  `# wiki: §N` (or `wiki_ref`) provenance comment citing `labs/comlab/wiki/NN_*.md`.
  No `# from wiki` / `# from BP` vagueness.
- Every field the task's `### Consumer (signal/noise) ###` names is **read** in a
  live COMLab path (analytics or fault-atlas routing), not merely defined on a
  schema. A field defined but unread is an **orphan** → FAIL.
- The fusion-spine boundary holds: no raw-sensor / DTC-parse / chemistry logic was
  introduced (that belongs upstream).
- For flag work: single-point / flag-off behaviour is byte-identical
  (regression-locked) — the flag does not silently change a verdict.

### Phase 6 — Diff review

```bash
git diff --stat
git diff HEAD -- <changed_files>
```

Review each changed file for:

- Unintended changes outside task scope.
- Missing error handling / silent defaults (COMLab is fail-closed).
- No cross-lab Python imports (`from gaslab`, `from obdlab`, `from dtclab`,
  `from vinlab`, `from dnalab`, `from symptomlab`) — mirror types locally.
- No v6 / v1 imports or v6-only enum names (`MixtureClass`, `GasRuleFlag`,
  `OBDFlag`, the 4-value `DTCRoutingTag`, `HistoricalSignature`).
- No magic numbers without a `# wiki:` source comment.
- No bare `except:`, no mutable defaults, no `print` statements
  (`comlab-python §5` checklist).
- No new doc written into `wiki/` (reserved for the lab wiki; design docs → `docs/`).
- `graphify` / KG rebuild absent (graph is frozen — never rebuilt in a COMLab task).

---

## Output format

After running all phases, write this block into
`labs/comlab/tasks/progress_notes/<task-id>.md` under the current task:

```
VERIFICATION GATE — <task-id>
=============================
Phase 1 Syntax/import:  PASS / FAIL <reason>
Phase 2 Type check:     PASS / FAIL <count> errors
Phase 3 Lint:           PASS (<N> warnings noted)
Phase 4 pytest:         PASS (<X> passed, <Y> skipped) [+ registry <X> passed]
Phase 5 Wiki/orphan:    PASS / FAIL <unsourced numerics / orphaned consumer field>
Phase 6 Diff review:    <N> files changed, no scope creep / SCOPE_CREEP <list>

comlab-python checklist items applied:
  [list which of the 10 items were checked]

Status: DONE — flipping PROGRESS.md to done / BLOCKED
```

**Do NOT paste this block into `PROGRESS.md`** — the ledger stays small. The
progress-notes file is where the gate evidence lives. The progress note must
**open with the confirmed `## Plan`** (written at task start) and gain this block
plus the `CODE REVIEW` block at task end.

---

## Hard stops

Do **not** flip a task to `done` if:

- Phase 4 (pytest) has any failure on COMLab tests (or `registry/tests/` when touched).
- Phase 5 fails: an unsourced numeric/enum, or a contracted consumer field that is
  read nowhere in a live path (orphan).
- Phase 6 shows changes outside the task's stated scope.
- Any cross-lab Python import, or any v6/v1 import or v6-only enum name, is present.
- Raw-sensor / DTC-parse / chemistry logic was introduced into `comlab/`.
- A flag-introduction change altered a verdict value instead of staying default-off
  and byte-identical.
- Any `graphify` / KG rebuild step was run.

Log as a blocker in the progress-notes file instead.

---

## Cross-references

- `_comlab_skills/comlab-python/SKILL.md` — inner loop + Immediate Checklist.
- `_comlab_skills/comlab-code-review/SKILL.md` — per-diff `CODE REVIEW` block.
- `labs/comlab/wiki/NN_*.md` — invariants the gate enforces (§03 prune, §08 fusion,
  §09 confidence, §10 differential, §11 delta).
- `labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md` — anti-orphan gate definition.
