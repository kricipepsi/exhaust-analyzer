---
node_type: task
task_id: T-COM-CODE-CLEAN-C
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

# T-COM-CODE-CLEAN-C — codingskills audit + AST-legible: the rest of the core pipeline

**Status:** `done` · **Pack:** VAULT (COMLab) · **Mode:** coder lane (inner loop after every edit)
**Origin:** pipeline guide §3·1A · **Blocked by:** —
**Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review` + the codingskills passes.
**Consumer (signal/noise):** **Adds no schema field.** Cleaner seams on the aggregation/perception
pipeline feed `graph/v2_code/`; consumer = the vault frontmatter derivation (`modules.base`, the spine).

### Scope ###

The non-router `core/` modules (~1,255 LOC):

- `lab_pipeline_aggregator.py` (634) — `LabPipelineAggregator` (the `.process()` spine the Wired app
  calls) + `AggregatorAbort`.
- `perception_contradiction.py` (285) — `PerceptionContradictionResult`, `CompensatedRichResult`, `detect`.
- `horizon_context_injector.py` (112) — `HorizonContext`, `HorizonContextInjector`.
- `symptom_router.py` (87) — symptom-prior routing.
- `ecu_hardware_checker.py` — `ECUHardwareChecker`, `ECUHardwareVerdict`.

**Excludes** `fault_atlas_router.py`/`fault_atlas_kg.py` (→ `T-COM-CODE-CLEAN-A`), `schemas/` (→ B),
`analytics/`/`projection`/`observability` (→ D), `tests/`, `registry/`.

### codingskills passes ###

Same five as A. The aggregator is the integration seam (consumes the four labs' verdicts, routes to atlas)
— `improve-codebase-architecture` (seam/depth) and `uncle-bob-craft` (dependency direction) are the
high-value passes. Confirm the default-off flag pattern (`enable_delta`, `enable_fatal_gates`) reads cleanly.

### AST-legibility levers to confirm (guide §3·1A) ###

No `import *`; public surface stated (no `__all__` in `core/` today — decide the export surface, e.g.
`LabPipelineAggregator`, or record why); typed public signatures; `# WHY:` on the non-obvious fusion gates
(perception-contradiction divergence; fatal-gate wiring); numeric literals carry `# wiki: §…` cites; flags
default-off.

### Success criteria ###

1. codingskills passes run; in-scope fixes applied; **no behaviour change**.
2. Inner loop green (`ruff` / `pyright comlab/` / `pytest -x -q`); 509 passed / 4 skipped preserved.
3. Confirm: no `import *`; public surface stated; signatures typed; literals cite wiki; flags default-off.
4. No cross-lab import; fusion-spine boundary intact (consumes verdicts, no raw-sensor logic added).

### Out of scope ###

- `fault_atlas_router.py`/`fault_atlas_kg.py` (→ A) · `schemas/` (→ B) · `analytics/`/`projection`/
  `observability` (→ D) · `tests/`, `registry/` · graphify · any schema/flag-default change.
- Surgical-change rule applies. **GRAPH GUARDRAIL:** no graphify / graph rebuild.

### Files to touch ###

- `labs/comlab/comlab/core/{lab_pipeline_aggregator,perception_contradiction,horizon_context_injector,symptom_router,ecu_hardware_checker}.py` — only audit-reported legibility fixes.

### Verification ###

```bash
cd <repo>/labs/comlab && PY=../../.sandbox-py/bin/python3.14
ruff check . && "$PY" -m pyright --pythonpath "$PY" comlab/ && "$PY" -m pytest -x -q
grep -rn 'import \*' comlab/core/lab_pipeline_aggregator.py comlab/core/perception_contradiction.py && echo FAIL || echo OK
grep -rn 'from gaslab\|from obdlab\|from dtclab\|from dnalab' comlab/core/*.py && echo "FAIL cross-lab" || echo "OK isolated"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-CODE-CLEAN-C.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean / inner loop green / counts preserved / isolated) + `CODE REVIEW`
(violations vs fixed, no behaviour change). Ledger row → `done` only when both clean.
