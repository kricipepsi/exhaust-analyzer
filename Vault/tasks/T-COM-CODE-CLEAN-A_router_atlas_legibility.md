---
node_type: task
task_id: T-COM-CODE-CLEAN-A
status: done
pack: VAULT
lab: comlab
mode: coder lane
blocked_by: []
consumers:
- modules.base — module map view
- graph/v2_code — AST code graph
- design→code→test spine (.base views)
tags:
- task
- vault
- comlab
---

# T-COM-CODE-CLEAN-A — codingskills audit + AST-legible: the atlas routing spine

**Status:** `done` · **Pack:** VAULT (COMLab) · **Mode:** coder lane (inner loop after every edit)
**Origin:** pipeline guide §3·1A (code-clean **before** graph work) · **Blocked by:** —
**Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review` (mandatory 3) + run the
codingskills passes below. **Do NOT** load `comlab-vault-prep` (that gates Phase-2 prep, not code-clean).
**Consumer (signal/noise):** **Adds no schema field.** Cleaner seams + accurate names feed the
`graph/v2_code/` graph (built in `T-COM-GRAPH-AST`); its consumer is the **vault build's frontmatter
derivation** (`module`/`implements`/`source` → `modules.base`, the design→code→test spine). The name *is*
the future graph node label — structural quality, not new behaviour.

### Why this task exists (and why it is split) ###

COMLab has **no prior code audit**, so code-clean is real Phase-1 work, run **before** any graphify so a
later refactor cannot force a re-extraction. The package is ~6,200 LOC, so CODE-CLEAN is split by
subpackage. **This sub-task (A) takes the heaviest, highest-decision surface: the atlas routing spine.**

### Scope ###

- **`labs/comlab/comlab/core/fault_atlas_router.py`** (~2,204 LOC — `FaultAtlasRouter` + the registry
  models `OBDConstraint`/`DTCLabStatusRule`/`CrossDomainMatrix`/`ConfidenceScoring`/`RegistryRow`/
  `RegistryFile`, the `TriageVerdict` TypedDict, and the `_BankAsymmetryVerdict`/`_EcuFaultVerdict`/
  `_NoStartVerdict` evidence dataclasses) and **`core/fault_atlas_kg.py`** (`FaultAtlasKG`, ~144 LOC).
- **Excludes** the rest of `core/` (→ `T-COM-CODE-CLEAN-C`), `tests/`, `registry/`, `research/`, `wiki/`.

### codingskills passes to run (from `_skills/codingskills/`, coder lane) ###

`improve-codebase-architecture` (deepen shallow modules; a 2,204-LOC router is a prime depth/seam target —
report, don't force a rewrite), `uncle-bob-craft` (SOLID / dependency-rule), `code-simplifier` (reduce
nesting; clearer names — no behaviour change), `code-review-excellence` (defect sweep before the graph
freezes it), `pythonskill` (PEP 8, modern 3.14). Read each before applying; the structural-craft axis is
also folded into `comlab-code-review §8`.

### AST-legibility levers to confirm (guide §3·1A — what CODEPREP will audit) ###

No `from x import *`; the public surface stated (`__all__` or a recorded reason — **note `core/` has no
`__all__` today**; decide the intended export surface, e.g. `FaultAtlasRouter`/`FaultAtlasKG`, or record
why not); type hints on public signatures; domain states are real `StrEnum`s (not bare strings); `# WHY:`
rationale on the non-obvious triage gates; **every numeric literal carries its `# wiki: §…` cite** (the
±5 % bank bound, stoich band, confidence caps — confirm each).

### Success criteria ###

1. codingskills passes run; in-scope fixes applied; **no behaviour change** (legibility, not logic).
2. Inner loop green after every edit: `ruff check .` clean, `pyright comlab/` clean, `"$PY" -m pytest -x -q`
   green (`$PY=../../.sandbox-py/bin/python3.14`); test counts preserved (509 passed / 4 skipped).
3. Confirm: no `import *`; public surface stated; public signatures typed; domain enums real `StrEnum`s;
   numeric literals in the two files carry wiki cites.
4. No cross-lab import introduced (`gaslab`/`obdlab`/`dtclab`/`dnalab`); fusion-spine boundary intact
   (no raw-sensor/DTC/chemistry logic added — COMLab consumes verdicts).

### Out of scope ###

- The rest of `core/` (→ C) · `schemas/` (→ B) · `analytics/`/`projection`/`observability` (→ D).
- `tests/`, `registry/` · running graphify (→ GRAPH-AST) · any schema field add/remove · scoring/ranker
  rework. Surgical-change rule: every changed line traces to a legibility fix; unrelated finds go to the
  ledger "Unplanned follow-ups", not this diff. **GRAPH GUARDRAIL:** never run graphify / rebuild a graph.

### Files to touch ###

- `labs/comlab/comlab/core/fault_atlas_router.py`, `labs/comlab/comlab/core/fault_atlas_kg.py` — only audit-reported legibility fixes.
- Optionally create `labs/comlab/docs/audits/AUDIT_2026-06-26_comlab_router.md` (audit record; `.md` only).

### Verification ###

```bash
cd <repo>/labs/comlab && PY=../../.sandbox-py/bin/python3.14
ruff check . && "$PY" -m pyright --pythonpath "$PY" comlab/ && "$PY" -m pytest -x -q
grep -rn 'import \*' comlab/core/fault_atlas_router.py comlab/core/fault_atlas_kg.py && echo "FAIL star-import" || echo "OK no star-import"
grep -rn 'from gaslab\|from obdlab\|from dtclab\|from dnalab' comlab/core/fault_atlas_router.py comlab/core/fault_atlas_kg.py && echo "FAIL cross-lab" || echo "OK isolated"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-CODE-CLEAN-A.md` opens with the confirmed `## Plan` (passes run + target
symbols); the run session fills `VERIFICATION GATE` (audit clean / fixes applied / inner loop green /
counts preserved / isolated) + `CODE REVIEW` (violations found vs fixed, no behaviour change). Ledger row →
`done` only when both blocks are clean.
