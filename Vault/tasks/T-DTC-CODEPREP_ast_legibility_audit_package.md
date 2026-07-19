---
node_type: task
task_id: T-DTC-CODEPREP
status: pending
pack: VAULT
lab: dtclab
mode: graph-tooling + coder lane
blocked_by:
- T-DTC-CODE-CLEAN
- T-DTC-COMMENT-FIX
consumers:
- modules.base — module map view
- graph/v2_code — AST code graph
- design→code→test spine (.base views)
tags:
- task
- vault
- dtclab
---

# T-DTC-CODEPREP — AST-legibility audit of the DTCLab package (`4dlab-code-prep`)

**Status:** `pending` · **Pack:** VAULT (DTCLab) · **Mode:** GRAPH-TOOLING + coder lane (audit, then coder applies fixes under inner loop)
**Origin:** pipeline guide §4 (code prep) · **Blocked by:** T-DTC-CODE-CLEAN, T-DTC-COMMENT-FIX
**Consumer (signal/noise):** **Adds no schema field.** Produces a `file:line → rule → fix` audit report
against graphify's AST-legibility rules so the `graph/v2_code/` graph (built in `T-DTC-GRAPH-AST`) has
clean module seams and accurate node labels. That code graph's consumer is the **vault build's
frontmatter derivation** (`implements`/`module`/`source`) feeding `modules.base` and the
design→code→test spine. No new fields; this is a structural audit of existing code.

### Role note ###

`4dlab-code-prep` **probes what your local graphify build actually extracts**, then **reports**
violations — it does **not** auto-rewrite source (a blanket auto-rewrite is forbidden: unreviewable
diff). The coder applies the reported fixes under the normal inner loop (`ruff`→`pyright`→`pytest -x -q`
after every edit). The skill never writes `graph.json` and never runs graphify.

### Scope ###

- **Package only:** `labs/dtclab/dtclab/` — `__init__.py`, `family_map.py`, `ranking.py`, `core/` (6),
  `schemas/` (5). ~1,582 lines.
- **Excludes** `tests/` (its own run = `T-DTC-TESTPREP`) and `wiki/` (prose, not AST).

### AST-legibility levers the audit checks (guide §3·1A) ###

Explicit named imports (no `from x import *`); a `__all__` public surface; type hints on public
signatures; domain states as real `StrEnum`s (graphify reads these as nodes — already true for
`DTCRoutingTag`, `Mode06MonitorState`, `MatchType`, `FuelSystemStatus`, `HistoricalFaultContext`);
`# WHY:` rationale on non-obvious gates (cross-field coolant rule; gpf_combined compound gate; the
scorer's max-weight selection); every numeric literal in `dtclab/` carrying its wiki-citation comment.

### Known starting signal (post CODE-CLEAN + COMMENT-FIX) ###

`T-DTC-CODE-CLEAN` should have already cleaned hygiene and `T-DTC-COMMENT-FIX` corrected the two stale
enum-count docstrings, so the audit should be light. Report — do not silently fix — any residual:
continuation-line numeric literals lacking an inline cite; a public symbol the Wired adapter imports
(`ranking.classify_top3`) that is not in a `__all__`; or a `core/` helper with an untyped public signature.

### Success criteria ###

1. `4dlab-code-prep probe → audit → report` run against `labs/dtclab/dtclab/`; report lists every
   violation as `file:line → rule → fix`, zero false positives spot-checked.
2. Coder applies the in-scope fixes; inner loop (`ruff`→`pyright`→`pytest -x -q`) stays green; test
   counts preserved.
3. Report explicitly confirms: no `import *`; public surface has `__all__` or a stated reason; public
   signatures typed; domain enums are real `StrEnum`s.
4. No behaviour change (prep is legibility, not logic); no graphify run; no schema field added/removed.

### Out of scope ###

- `tests/` (→ `T-DTC-TESTPREP`) · running graphify (→ `T-DTC-GRAPH-AST`).
- The stale-comment fix (owned by `T-DTC-COMMENT-FIX`) · the GPF out-of-era decision (START_HERE §5).

### Files to touch ###

- `labs/dtclab/dtclab/**/*.py` — only the audit-reported legibility fixes.
- The audit report appended to the progress note (skill output convention).

### Verification (inner loop + audit) ###

```bash
cd <repo>/labs/dtclab
ruff check . && pyright && pytest -x -q
grep -rn 'import \*' dtclab/ && echo "FAIL star-import" || echo "OK no star-import"
grep -rn '__all__' dtclab/__init__.py dtclab/ranking.py | head
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-CODEPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean / fixes applied / inner loop green / counts preserved) + `CODE REVIEW`
(violations found vs fixed, no behaviour change). Ledger row → `done` only when both are clean.
