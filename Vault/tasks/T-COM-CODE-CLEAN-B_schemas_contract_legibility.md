---
node_type: task
task_id: T-COM-CODE-CLEAN-B
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

# T-COM-CODE-CLEAN-B — codingskills audit + AST-legible: the schemas / contract surface

**Status:** `done` · **Pack:** VAULT (COMLab) · **Mode:** coder lane (inner loop after every edit)
**Origin:** pipeline guide §3·1A · **Blocked by:** —
**Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review` + the codingskills passes.
**Consumer (signal/noise):** **Adds no schema field.** The schemas *are* COMLab's contract surface — the
input verdict envelope and the output UI envelope. Clean enums/labels here become the most-referenced
nodes in `graph/v2_code/`; consumer = the vault frontmatter derivation (`modules.base`, the spine).

### Scope ###

- **`labs/comlab/comlab/schemas/`** (~1,506 LOC, 6 files):
  - `ingestion.py` (505) — the inbound contract: `OrchestratorInboundRequest` (the spine input),
    `VehicleDNA`/`VinDNA`, the four lab payloads (`GasLabPayload`, `DTCLabPayload`, `OBDLiveDataPayload`,
    `FreezeFrameRecord`/`Mode06MonitorResult`), `SecondOperatingPointFrame`, the echo-audit models.
  - `vocabulary.py` (662) — the enums (`Horizon` `StrEnum` + family/chemistry vocab; **already has
    `__all__`** — confirm it is complete and accurate).
  - `response.py` (128) — the outbound contract: `OrchestratorFinalUIOutput` (spine output),
    `DiagnosticVerdict`, `DifferentialSiblingOut`, `LabRoutingDirectiveOut`, `PerformanceAnalytics`.
  - `lab_dna_views.py` (88) — `GasLabDnaView`/`ObdLabDnaView`/`DtcLabDnaView`/`ProjectedViews`.
  - `kg.py` — `KGNode`/`KGFile`. `__init__.py` (has `__all__`).
- **Excludes** `core/` (→ A/C), `analytics/`/`projection`/`observability` (→ D), `tests/`, `registry/`.

### codingskills passes ###

Same five as `T-COM-CODE-CLEAN-A`. Schemas are largely declarative (pydantic) — the high-value passes here
are `code-review-excellence` (enum completeness, validator correctness) and `uncle-bob-craft` (no logic
leaking into models). Names and enum values are the graph node labels.

### AST-legibility levers to confirm (guide §3·1A) ###

No `import *`; `__all__` present and accurate in `vocabulary.py` + `schemas/__init__.py` (widen/trim to the
real public surface); type hints on every public field/method; **domain states are real `StrEnum`s**, no
v6 enum names re-introduced (`MixtureClass`, `GasRuleFlag`, `OBDFlag`, 4-value `DTCRoutingTag`,
`HistoricalSignature`); every numeric bound/threshold literal carries its `# wiki: §…` cite.

### Success criteria ###

1. codingskills passes run; in-scope fixes applied; **no behaviour change**.
2. Inner loop green (`ruff` / `pyright comlab/` / `pytest -x -q`); 509 passed / 4 skipped preserved.
3. `__all__` in `vocabulary.py` + `schemas/__init__.py` matches the real public surface; all public fields
   typed; enums are `StrEnum`s; no v6 enum re-introduction; literals cite wiki.
4. No cross-lab import; the contract still mirrors each lab's types **locally** (no `from gaslab`/etc.).

### Out of scope ###

- Any field/enum **add, remove, or widen** — this is legibility only. A real contract change is a separate
  spec with a named consumer (signal/noise). · `core/`, `analytics/`, `tests/`, `registry/` · graphify.
- Surgical-change rule applies; unrelated finds → ledger follow-ups. **GRAPH GUARDRAIL:** no graphify.

### Files to touch ###

- `labs/comlab/comlab/schemas/*.py` — only audit-reported legibility fixes.

### Verification ###

```bash
cd <repo>/labs/comlab && PY=../../.sandbox-py/bin/python3.14
ruff check . && "$PY" -m pyright --pythonpath "$PY" comlab/ && "$PY" -m pytest -x -q
grep -rn 'import \*' comlab/schemas/ && echo "FAIL star-import" || echo "OK"
grep -rnE 'MixtureClass|GasRuleFlag|OBDFlag|HistoricalSignature' comlab/schemas/ && echo "FAIL v6 enum" || echo "OK no v6"
grep -rn '__all__' comlab/schemas/__init__.py comlab/schemas/vocabulary.py | head
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-CODE-CLEAN-B.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean / inner loop green / `__all__` accurate / no v6 enum / counts preserved) +
`CODE REVIEW` (violations vs fixed, no behaviour/contract change). Ledger row → `done` only when both clean.
