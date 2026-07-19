---
node_type: task
task_id: T-COM-CODEPREP
status: pending
pack: VAULT
lab: comlab
mode: graph-tooling + coder lane
blocked_by:
- T-COM-CODE-CLEAN-A
- T-COM-CODE-CLEAN-B
- T-COM-CODE-CLEAN-C
- T-COM-CODE-CLEAN-D
consumers:
- modules.base — module map view
- graph/v2_code — AST code graph
- design→code→test spine (.base views)
tags:
- task
- vault
- comlab
---

# T-COM-CODEPREP — AST-legibility audit of the COMLab package (`4dlab-code-prep`)

**Status:** `pending` · **Pack:** VAULT (COMLab) · **Mode:** GRAPH-TOOLING + coder lane (audit, then coder applies fixes under inner loop)
**Origin:** pipeline guide §4 (code prep) · **Blocked by:** T-COM-CODE-CLEAN-A/B/C/D
**Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`4dlab-code-prep`**,
**`comlab-vault-prep`**.
**Consumer (signal/noise):** **Adds no schema field.** Produces a `file:line → rule → fix` audit so the
`graph/v2_code/` graph (built in `T-COM-GRAPH-AST`) has clean seams + accurate node labels; that graph's
consumer is the vault frontmatter derivation (`implements`/`module`/`source` → `modules.base`, the spine).

### Role note ###

`4dlab-code-prep` **probes what your local graphify build extracts**, then **reports** violations — it does
**not** auto-rewrite source (a blanket auto-rewrite is an unreviewable diff and is forbidden). The coder
applies the reported fixes under the COMLab inner loop. The skill never writes `graph.json` / runs graphify.
`comlab-vault-prep` Rule 5 governs the scope and audit-not-rewrite discipline here.

### Scope ###

- **Package only:** `labs/comlab/comlab/` — `core/`, `schemas/`, `analytics/`, `observability/`,
  `projection.py`, `__init__.py` (~6,200 LOC).
- **Excludes** `tests/` (its own run = `T-COM-TESTPREP`), `wiki/` (prose), **and `registry/`** (separate
  package, out of pack scope), `research/`.

### AST-legibility levers the audit checks (guide §3·1A) ###

Explicit named imports (no `from x import *`); a `__all__` public surface (today only `schemas/vocabulary.py`
+ `schemas/__init__.py` declare one — **the top-level `comlab/__init__.py` and `core/`/`analytics/` lack
`__all__`**; the audit reports whether the Wired-facing surface `LabPipelineAggregator` and the routing
classes should be exported); type hints on public signatures; domain states as real `StrEnum`s (graphify
reads these as nodes); `# WHY:` on non-obvious fusion gates; **every numeric literal carries a `# wiki: §…`
cite**.

### Known starting signal (post CODE-CLEAN A–D) ###

The four code-clean tasks should have applied the hygiene + AST-legibility fixes already, so the audit
should be light. Report — do not silently fix — any residual: a public symbol the Wired adapter imports
(`from comlab import LabPipelineAggregator`; `comlab.core.fault_atlas_router.FaultAtlasRouter`) absent from
an `__all__`; a continuation-line literal lacking an inline wiki cite; an untyped public signature.

### Success criteria ###

1. `4dlab-code-prep probe → audit → report` run against `labs/comlab/comlab/`; report lists every violation
   as `file:line → rule → fix`; zero false positives spot-checked; **`tests/`/`registry/` excluded**.
2. Coder applies in-scope fixes; inner loop (`ruff` / `pyright comlab/` / `pytest -x -q`) stays green;
   509 passed / 4 skipped preserved.
3. Report confirms: no `import *`; public surface has `__all__` or a stated reason; signatures typed;
   domain enums real `StrEnum`s.
4. No behaviour change; no graphify run; no schema field added/removed; no cross-lab import.

### Out of scope ###

- `tests/` (→ `T-COM-TESTPREP`) · `registry/` (out of pack) · running graphify (→ `T-COM-GRAPH-AST`) ·
  any schema change. **GRAPH GUARDRAIL:** no graphify / graph rebuild.

### Files to touch ###

- `labs/comlab/comlab/**/*.py` — only audit-reported legibility fixes.
- The audit report appended to the progress note (skill output convention).

### Verification ###

```bash
cd <repo>/labs/comlab && PY=../../.sandbox-py/bin/python3.14
ruff check . && "$PY" -m pyright --pythonpath "$PY" comlab/ && "$PY" -m pytest -x -q
grep -rn 'import \*' comlab/ && echo "FAIL star-import" || echo "OK"
grep -rn '__all__' comlab/__init__.py comlab/core/__init__.py comlab/schemas/__init__.py | head
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-CODEPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean / fixes applied / inner loop green / tests+registry excluded / counts
preserved) + `CODE REVIEW` (violations found vs fixed, no behaviour change). Ledger row → `done` only when
both blocks are clean.
