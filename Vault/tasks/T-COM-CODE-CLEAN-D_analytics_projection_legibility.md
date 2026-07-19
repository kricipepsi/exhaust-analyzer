---
node_type: task
task_id: T-COM-CODE-CLEAN-D
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

# T-COM-CODE-CLEAN-D — codingskills audit + AST-legible: analytics, projection, observability

**Status:** `done` · **Pack:** VAULT (COMLab) · **Mode:** coder lane (inner loop after every edit)
**Origin:** pipeline guide §3·1A · **Blocked by:** —
**Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review` + the codingskills passes.
**Consumer (signal/noise):** **Adds no schema field.** Cleaner analytics/projection seams feed
`graph/v2_code/`; consumer = the vault frontmatter derivation (`modules.base`, the spine).

### Scope ###

- `analytics/delta_engine.py` (622) — the two-point `DeltaEngine` (ΔTrim/Δgas/ΔO₂ bands; default-off).
- `analytics/power_loss_analytics.py` (207) — `PowerLossAnalytics` (scoring weights, `Mode06MonitorState`).
- `projection.py` (124) — `project()` (raw `vin_dna` dict → `ProjectedViews`; the FU-4 path).
- `observability/_tracer.py` (191) + `observability/__init__.py` — the span tracer.
- `comlab/__init__.py` (8) — the package surface (`from comlab import LabPipelineAggregator` is the Wired
  entrypoint — **confirm the top-level `__all__`/export is intentional**; it has none today).

**Excludes** `core/` (→ A/C), `schemas/` (→ B), `tests/`, `registry/`.

### codingskills passes ###

Same five as A. `delta_engine.py` carries ~30 `# wiki: delta-relations/NN` provenance comments now mirrored
COMLab-local at `wiki/11 §CONCEPT_DELTA_BANDS` — confirm each band literal cites a wiki §; the optional
comment-repoint (delta-relations → COMWIKI-11) is a **deferred** follow-up, not this task's diff.

### AST-legibility levers to confirm (guide §3·1A) ###

No `import *`; the **top-level `comlab/__init__.py` export surface** stated (this is the Wired app's import
target — decide `__all__ = ["LabPipelineAggregator", ...]` or record why not); typed public signatures;
`# WHY:` on the delta architecture/validity gates; every band/threshold literal carries `# wiki: §…`; the
delta flags default-off.

### Success criteria ###

1. codingskills passes run; in-scope fixes applied; **no behaviour change**.
2. Inner loop green (`ruff` / `pyright comlab/` / `pytest -x -q`); 509 passed / 4 skipped preserved.
3. Confirm: no `import *`; top-level export surface stated; signatures typed; delta literals cite wiki;
   flags default-off.
4. No cross-lab import; projection still reads the raw `vin_dna` dict (no `from vinlab` import).

### Out of scope ###

- `core/` (→ A/C) · `schemas/` (→ B) · `tests/`, `registry/` · graphify · the delta comment-repoint
  (deferred) · any band/flag/behaviour change. Surgical-change rule applies. **GRAPH GUARDRAIL:** no graphify.

### Files to touch ###

- `labs/comlab/comlab/analytics/*.py`, `labs/comlab/comlab/projection.py`,
  `labs/comlab/comlab/observability/*.py`, `labs/comlab/comlab/__init__.py` — only legibility fixes.

### Verification ###

```bash
cd <repo>/labs/comlab && PY=../../.sandbox-py/bin/python3.14
ruff check . && "$PY" -m pyright --pythonpath "$PY" comlab/ && "$PY" -m pytest -x -q
grep -rn 'import \*' comlab/analytics/ comlab/projection.py comlab/observability/ && echo FAIL || echo OK
grep -rn 'from vinlab\|from gaslab\|from obdlab\|from dtclab' comlab/analytics/ comlab/projection.py && echo "FAIL cross-lab" || echo "OK isolated"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-CODE-CLEAN-D.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean / inner loop green / counts preserved / isolated) + `CODE REVIEW`
(violations vs fixed, no behaviour change). Ledger row → `done` only when both clean.
