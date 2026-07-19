---
name: comlab-code-review
description: >
  Mandatory always-loaded COMLab session skill — runs a per-diff self-review at
  session end before any task flips to done. Produces the CODE REVIEW block for
  tasks/progress_notes/<task-id>.md. Catches COMLab design-rule violations, contract
  changes, signal/noise orphans, and structural-craft issues that slip past the
  6-phase verification gate.
origin: adapted from _obdlab_skills/obdlab-code-review/SKILL.md
updated: 2026-06-21 (initial build — COMLab Stage-4 bundle; includes structural-craft axis)
---

# comlab-code-review — Per-Diff Self-Review Before Commit

This skill defines the `CODE REVIEW` block. It is the second of two mandatory
blocks (alongside `VERIFICATION GATE` from `comlab-verification-loop`) that gate a
task from `in_progress` to `done`. A clean block is required before commit.

The 6-phase outer gate catches syntax/type/lint/pytest/drift/scope failures. This
skill catches what those phases miss: COMLab design-rule violations, semantic
contract drift, signal/noise orphans, and structural rot.

---

## When to run

After `comlab-verification-loop`'s 6 phases pass, diff staged, before `git commit`.

---

## The review checklist

### 1. COMLab design rule compliance (BLOCKING)

**Cross-lab boundary violations:**

- Any `comlab/` module importing from `gaslab`, `obdlab`, `dtclab`, `vinlab`,
  `symptomlab`, `dnalab` → **BLOCKING**. COMLab mirrors lab types locally; cross-lab
  traffic is JSON-contract-only per `wiki/SEMANTIC_CONTRACT.md`.

**Fusion-spine boundary violations:**

- Raw-sensor logic (PID validation, unit normalization, VE computation) inside
  `comlab/` → **BLOCKING**. That is OBDLab's job; COMLab consumes its *verdict*.
- DTC regex (`re.match(r"^[BCPU]…")`) or routing-tag derivation → **BLOCKING**
  (DTCLab's job).
- NOx / CO / HC ppm chemistry, λ-from-ppm conversion, or catalyst-efficiency math
  → **BLOCKING** (GASLab's job).

**Signal/noise violations (COMLab's governing constraint):**

- A new field / enum / fault / signal whose `### Consumer (signal/noise) ###` is
  blank, vague ("future use", "for COMLab"), or names no `file.py::function` code
  path → **BLOCKING**.
- A contracted consumer field that is defined on a schema but **read nowhere** in a
  live COMLab path (analytics / fault-atlas routing) → **BLOCKING** (orphan).
- A new field/enum without a same-change proposal under `comlab/config/proposals/`
  when no existing consumer can be named → **BLOCKING**.

**Vocabulary / provenance violations:**

- A new enum value or numeric threshold with no `# wiki: §N` (or `wiki_ref`)
  citing `labs/comlab/wiki/NN_*.md` → **BLOCKING**. Vague `# from wiki` is BLOCKING.
- A v6-only enum name re-introduced (`MixtureClass`, `GasRuleFlag`, `OBDFlag`,
  4-value `DTCRoutingTag`, `HistoricalSignature`) → **BLOCKING**.

**Flag / regression violations:**

- A new fusion capability not shipped default-off behind an explicit flag →
  **BLOCKING**. A flag change that alters single-point / flag-off verdict values
  (not byte-identical) → **BLOCKING**.

**Folder / graph violations:**

- A new doc written into `wiki/` (reserved for the lab wiki) → **BLOCKING**;
  design docs go in `docs/`, vocabulary/contract in `docs/Vocabulary/`.
- Any `graphify` / KG rebuild step → **BLOCKING** (graph is frozen).

### 2. Scope compliance (BLOCKING on scope creep)

Check the task's `### Out of scope ###` section.

- Files changed outside the task's named set → **BLOCKING** unless a direct
  dependency.
- "While I was here" fixes → **BLOCKING**; log as unplanned follow-up in
  `PROGRESS.md`'s follow-ups table.

### 3. Contract changes (BLOCKING if callers unhandled)

Did a public function signature, Pydantic model, or enum shape change?

- List every caller in `comlab/` and `tests/`. Every caller updated in this diff —
  missing → **BLOCKING**.
- A change to the input contract (`schemas/ingestion.py`) or output contract
  (`schemas/response.py`) is cross-lab-visible — log it as an architect-level patch
  row in `PROGRESS.md` and surface to the user → **BLOCKING** if missing.

### 4. Docstrings on public symbols (BLOCKING)

Every public class, function, and module constant introduced or materially changed
must have a docstring: what it does, inputs/types, outputs/types, and which wiki
section it sources from.

### 5. Wiki provenance (BLOCKING)

All new enum values, score weights, fusion thresholds, and confidence caps cite
their wiki section inline (`# wiki: §08`, `# wiki: §10`). Vague citations are
**BLOCKING** — pinpoint the section.

### 6. Python Immediate Checklist (WARNING / BLOCKING)

Per `comlab-python §5`: type hints, no mutable defaults, no bare except, f-strings,
pathlib, `is None`, sorted imports. Three or more warnings in one file → WARNING.
**Mutable default or bare except → BLOCKING.**

### 7. Test coverage of the change (WARNING / BLOCKING)

- New enum class with no drift/coverage test → **BLOCKING**.
- New output-contract field with no test covering its constraint or emission path →
  **BLOCKING**.
- New fusion/routing branch with no parametrized test → **BLOCKING**.
- Bug fix without a prior failing test → WARNING.

### 8. Structural craft (WARNING — record, don't silently skip)

These are the high-signal structural checks the project's skill-eval found carry the
largest measured quality gain (uncle-bob / improve-architecture). They are a
**WARNING axis** here, not BLOCKING, so they never override the lab design rules —
but a session must run them and record findings, not skip the axis:

- **Smells:** rigidity (small change forces many edits), fragility (changes break
  unrelated areas), needless repetition (DRY violated), opacity (hard to follow).
  Name any you see with file/area.
- **Depth / deletion test:** is the new module deep (a lot of behaviour behind a
  small interface), or a shallow pass-through? If deleting it just pushes the same
  complexity onto callers, reconsider the seam.
- **Single responsibility + small functions** in the changed code; suggest one or
  two concrete refactors (extract-and-name, invert a dependency) rather than a
  rewrite.

Record findings in the block; convert to a follow-up row in `PROGRESS.md` if a
refactor is warranted but out of this task's scope.

---

## The CODE REVIEW block

Paste into `labs/comlab/tasks/progress_notes/<task-id>.md` under the current task,
alongside `VERIFICATION GATE`:

```
CODE REVIEW — <task-id>
=======================
1. Design rules:        PASS / FAIL <violations>
2. Scope compliance:    PASS / FAIL <out-of-scope files>
3. Contracts:           PASS / FAIL <callers updated: list>
4. Docstrings:          PASS / FAIL <missing symbols: list>
5. Wiki provenance:     PASS / FAIL <unsourced numerics/enums: list>
6. Immediate Checklist: PASS / N warnings <list>
7. Test coverage:       PASS / WARNING / FAIL <gap>
8. Structural craft:    PASS / N notes <smells / depth / SRP findings>

Verdict: CLEAN / BLOCKED
Blockers: <empty if CLEAN; otherwise itemised>
```

**CLEAN** = zero BLOCKING findings (axes 1–7). Axis 8 notes and other warnings are
recorded, not blocking. **BLOCKED** = at least one BLOCKING; commit does not happen;
task stays `in_progress`.

---

## Cross-references

- `_comlab_skills/comlab-verification-loop/SKILL.md` — 6-phase outer gate.
- `_comlab_skills/comlab-python/SKILL.md` — Immediate Checklist used in §6.
- `labs/comlab/wiki/NN_*.md` — invariants enforced (§01 boundaries, §06 atlas,
  §08 fusion, §09 confidence, §10 differential).
- `labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md` — anti-orphan gate for §1 signal/noise.
