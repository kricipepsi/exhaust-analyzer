---
name: verification-loop
description: Comprehensive verification system for Claude Code sessions — build, type-check, lint, test, security scan, diff review before declaring any task done.
origin: ECC
---

# Verification Loop Skill

A comprehensive verification system for Claude Code sessions.

## When to Use

Invoke this skill:
- After completing any T## task before flipping status to `done` in PROGRESS.md
- Before declaring a refactor complete
- After any change that touches model output (T05–T09, T12, T13)

## Verification Phases (Python / pytest adaptation)

### Phase 1: Syntax & Import-Existence Check
```bash
python -m py_compile <changed_file>.py && echo "PASS" || echo "FAIL"
# Import-existence guard — actually import the module so every `import` line resolves:
python -c "import importlib; importlib.import_module('<module.path>')" && echo "IMPORTS OK" || echo "IMPORT FAIL"
```

`py_compile` only proves the file *parses* — it does not prove the imports point at
anything real. A plausible-looking `from fast_fetch import get` or `import disk_cache`
compiles fine and then explodes at runtime, because a model under pressure will invent a
library that *sounds* like it should exist. Actually importing the module is the cheapest
way to catch a hallucinated dependency before it reaches a test or a user. If an import
names a third-party package, confirm it is a real, installed distribution — not just a
name that reads convincingly.
<!-- Rework basis: skill_eval T-SE-5 (cohort_gateoverlap_report.md §2.3). On the trap-API
     task this skill recovered 0 escaped defects — it hallucinated `fast_fetch`/`disk_cache`
     identically to the no-skill control because it had no library-existence guard. Phase 1
     now imports the module so invented dependencies fail here instead of at runtime. -->

### Phase 2: Type Check
```bash
cd exhaust-analyzer-main
pyright . 2>&1 | head -30
# OR if pyright not installed:
python -m mypy . --ignore-missing-imports 2>&1 | head -30
```

Report all type errors. Fix before continuing.

### Phase 3: Lint Check
```bash
cd exhaust-analyzer-main
ruff check . 2>&1 | head -30
# OR:
flake8 . --max-line-length=120 2>&1 | head -30
```

### Phase 4: pytest Suite (Layer-1) — MANDATORY
```bash
cd exhaust-analyzer-main
python -m pytest tests/ -x --tb=short
```

**This must be green before any task is declared done.** If a previously-passing test now fails, stop and log a blocker in PROGRESS.md.

### Phase 5: Fast Accuracy Benchmark (Layer-1 accuracy sniff)
```bash
cd exhaust-analyzer-main
python tests/run_accuracy_benchmark.py
```

Run after any change that touches the model (T05–T09, T12). Record result in PROGRESS.md Notes.

### Phase 6: Diff Review
```bash
git diff --stat
git diff HEAD -- <changed_files>
```

Review each changed file for:
- Unintended changes outside task scope
- Missing error handling — and specifically the **boundary/failure paths**, since these
  are what slip through a green happy-path suite. For every collection or numeric operation
  in the diff, ask: what happens on an empty input, a single element (`len == 1`
  aggregations like `stdev`), a zero denominator, and the first/last index (off-by-one)?
  If the diff added a code path but no test exercises its empty/single/zero case, that path
  is unverified — flag it before declaring done.
- Petrol-only constraint — no diesel/LPG/hybrid paths re-introduced
- No magic numbers, no mutable defaults, no print statements (pythonskill checklist)
<!-- Rework basis: skill_eval T-SE-5 (cohort_gateoverlap_report.md §2). Recovery was 0 on
     the csv-stats task, where the escaped defects were boundary cases (single-value stdev,
     empty/zero handling). The diff review now names those boundaries explicitly so the gate
     catches them instead of trusting a happy-path-only suite. -->

## Output Format

After running all phases, record in PROGRESS.md Notes:

```
VERIFICATION GATE — T##
========================
Syntax:         PASS
Imports:        PASS (module imported; no hallucinated deps)
Type check:     PASS / SKIP (no pyright)
Lint:           PASS (X warnings noted)
pytest Layer-1: PASS (X tests, X passed)
Fast benchmark: X% accuracy (baseline: Y%)
Diff review:    X files changed, no scope creep

Pythonskill checklist items applied:
  [list which of the 10 items were checked]

Status: DONE — flipping PROGRESS.md
```

## Hard Stops

Do **not** flip a task to `done` if:
- pytest Layer-1 has any failure
- Layer-2 accuracy regressed vs. last checkpoint (for model-touching tasks)
- Diff shows changes outside the task's stated scope
- Any petrol-only violation is present

Log as a blocker in PROGRESS.md instead.
