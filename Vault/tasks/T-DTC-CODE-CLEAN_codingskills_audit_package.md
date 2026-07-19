---
node_type: task
task_id: T-DTC-CODE-CLEAN
status: pending
pack: VAULT
lab: dtclab
mode: coder lane
blocked_by: []
consumers:
- modules.base — module map view
- graph/v2_code — AST code graph
- design→code→test spine (.base views)
tags:
- task
- vault
- dtclab
---


# T-DTC-CODE-CLEAN — codingskills audit + make `dtclab/` AST-legible

**Status:** `pending` · **Pack:** VAULT (DTCLab) · **Mode:** coder lane (inner loop after every edit)
**Origin:** pipeline guide §3·1A (code-clean **before** graph work) · **Blocked by:** —
**Consumer (signal/noise):** **Adds no schema field.** Cleaner module seams and accurate names feed the
`graph/v2_code/` graph (built in `T-DTC-GRAPH-AST`), whose consumer is the **vault build's frontmatter
derivation** (`module`/`implements`/`source` → `modules.base`, the design→code→test spine). The name
*is* the future graph node label, so this is a structural quality pass, not new behaviour.

### Why this task exists (unlike GASLab) ###

GASLab entered the vault pipeline with a completed code audit (`docs/audits/AUDIT_2026-06-10`). **DTCLab
has none** (`labs/dtclab/docs/audits/` does not exist), so the code-clean pass is real work here, run
**before** any graphify so a later refactor cannot force a graph re-extraction.

### Scope ###

- **Package only:** `labs/dtclab/dtclab/` — `__init__.py`, `family_map.py`, `ranking.py`, `core/` (6
  modules), `schemas/` (5 modules), `config/` (data, not audited as code). ~1,582 lines.
- **Excludes** `tests/` (→ `T-DTC-TESTPREP` / `T-DTC-TESTS-GREEN`) and `wiki/` (prose, not AST).

### codingskills passes to run (from `_skills/codingskills/`, coder lane) ###

`improve-codebase-architecture` (deepen shallow modules; clean seams), `uncle-bob-craft` (SOLID /
dependency-rule / boundaries), `code-simplifier` (reduce nesting/redundancy, clearer names — no
behaviour change), `code-review-excellence` (defect sweep before the graph freezes it),
`pythonskill` (PEP 8, modern 3.14 patterns, the generate-validate-fix loop).

### AST-legibility levers to confirm (guide §3·1A — what CODEPREP will audit) ###

Explicit named imports (no `from x import *`); a `__all__` public surface (today `__init__.py` exports
only `DataFusionSanitizer` — confirm that is the intended surface, or widen it if `ranking.classify_top3`
should be a package-level export for the Wired adapter); type hints on public signatures; domain states
as real `StrEnum`s (already true: `DTCRoutingTag`, `Mode06MonitorState`, etc.); `# WHY:` rationale on
non-obvious gates (the cross-field coolant rule, the gpf_combined compound gate); and every numeric
literal in `dtclab/` carrying its wiki-citation comment (already largely present — confirm `ranking.py`
DNA factors and `freeze_frame_extractor.py` thresholds each cite their `§`).

### Success criteria ###

1. codingskills passes run; reported in-scope fixes applied; **no behaviour change** (legibility, not logic).
2. Inner loop green after every edit: `ruff check .` clean, `pyright` clean, `pytest -x -q` green.
3. Confirm: no `import *`; public surface stated (`__all__` or a recorded reason); public signatures typed;
   domain enums are real `StrEnum`s; numeric literals in `dtclab/` carry wiki cites.
4. No cross-lab import introduced (`gaslab`/`obdlab`/`comlab`/`dnalab`); isolation audit still green.
5. The 18-member `DTCRoutingTag` is unchanged (coordinate with `T-DTC-COMMENT-FIX`, which owns the
   stale-docstring fix — do **not** duplicate it here).

### Out of scope ###

- `tests/` (→ TESTPREP/TESTS-GREEN) · running graphify (→ GRAPH-AST) · the stale-comment fix (→ COMMENT-FIX).
- Any schema field add/remove · the GPF out-of-era decision (START_HERE §5).

### Files to touch ###

- `labs/dtclab/dtclab/**/*.py` — only the audit-reported legibility fixes.
- Optionally create `labs/dtclab/docs/audits/AUDIT_<date>_dtclab_state.md` (the audit record, mirroring
  GASLab) — useful provenance for later prep tasks; report-style, `.md` only.

### Verification (inner loop + audit) ###

```bash
cd <repo>/labs/dtclab
ruff check . && pyright && pytest -x -q
grep -rn 'import \*' dtclab/ && echo "FAIL star-import" || echo "OK no star-import"
grep -rn '__all__' dtclab/__init__.py | head
grep -rn 'from gaslab\|from obdlab\|from comlab\|from dnalab' dtclab/ && echo "FAIL cross-lab" || echo "OK isolated"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-CODE-CLEAN.md` opens with the confirmed `## Plan` (which passes,
target modules); the run session fills `VERIFICATION GATE` (audit clean / fixes applied / inner loop
green / isolation green) + `CODE REVIEW` (violations found vs fixed, no behaviour change). Ledger row →
`done` only when both blocks are clean.
