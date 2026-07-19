---
node_type: task
task_id: T-GAS-CODEPREP
status: pending
pack: VAULT
lab: gaslab
mode: graph-tooling + coder lane
blocked_by: []
consumers:
- modules.base — module map view
- graph/v2_code — AST code graph
- design→code→test spine (.base views)
tags:
- task
- vault
- gaslab
---


# T-GAS-CODEPREP — AST-legibility audit of the GASLab package (`4dlab-code-prep`)

**Status:** `pending` · **Pack:** VAULT (GASLab) · **Mode:** GRAPH-TOOLING + coder lane (audit, then coder applies fixes under inner loop)
**Origin:** pipeline guide §4 (code prep) · **Blocked by:** —
**Consumer (signal/noise):** **Adds no schema field.** Produces a `file:line → rule → fix` audit
report against graphify's AST-legibility rules so the `graph/v2_code/` graph (built in T-GAS-GRAPH-AST)
has clean module seams and accurate node labels. That code graph's consumer is the **vault build's
frontmatter derivation** (`implements`/`module`/`source`) feeding `modules.base` and the design→code→test
spine (plan §4). No new fields; this is a structural audit of existing code.

### Role note ###

`4dlab-code-prep` **probes what your local graphify build actually extracts**, then **reports**
violations — it does **not** auto-rewrite source (a blanket auto-rewrite is forbidden: unreviewable
diff). The coder applies the reported fixes under the normal inner loop (`ruff`→`pyright`→`pytest -x -q`
after every edit). The skill never writes `graph.json` and never runs graphify.

### Scope ###

- **Package only:** `labs/gaslab/gaslab/` (11 modules, ~1,992 lines).
- **Excludes** `tests/` (its own run = T-GAS-TESTPREP) and any `research/`/`wiki/` (prose, not AST).

### AST-legibility levers the audit checks (guide §3·1A) ###

Explicit named imports (no `from x import *`); a `__all__` public surface; type hints on public
signatures; domain states as real `Enum`/`StrEnum`s (a fixed set of named values — graphify reads
these as nodes); `# WHY:` rationale comments on non-obvious gates/formulas; and every numeric literal
in `gaslab/` carrying its wiki-citation comment.

### Known starting signal (from AUDIT_2026-06-10) ###

Hygiene is already strong — no cross-lab imports, no legacy imports, no bare `except`/`print`/mutable
defaults. The audit's one open code smell relevant here: numeric-literal citations are applied at the
**rule-block level**, so a few continuation lines (`rule_engine.py` L310–313, L325–328) lack their own
inline cite (AUD / GW-ENH-3). Code-prep should **report** these per the per-line rule; the citation
cleanup is already tracked by `GW-ENH-3` — coordinate, do not duplicate.

### Success criteria ###

1. `4dlab-code-prep probe → audit → report` run against `labs/gaslab/gaslab/`; report lists every
   violation as `file:line → rule → fix`, zero false positives spot-checked.
2. Coder applies the in-scope fixes; inner loop (`ruff`→`pyright`→`pytest -x -q`) stays green; **core
   207 tests preserved**.
3. Report explicitly confirms: no `import *`, public surface has `__all__` or a stated reason, public
   signatures typed, domain enums are real `Enum`/`StrEnum`.
4. No behaviour change (prep is legibility, not logic); no graphify run; no schema field added/removed.

### Out of scope ###

- `tests/` (→ T-GAS-TESTPREP) · running graphify (→ T-GAS-GRAPH-AST).
- AUD-3/4/6 schema-orphan/rename work (separate GASLab tasks) — report-only if surfaced, don't fix here.

### Files to touch ###

- `labs/gaslab/gaslab/*.py` — only the audit-reported legibility fixes.
- The audit report appended to the progress note (skill output convention).

### Verification (inner loop + audit) ###

```bash
cd <repo>/labs/gaslab
ruff check . && pyright && pytest -x -q -m "not slow"
grep -rn 'import \*' gaslab/ && echo "FAIL star-import" || echo "OK no star-import"
grep -rn '__all__' gaslab/__init__.py | head    # public surface present
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-CODEPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (audit clean / fixes applied / inner loop green / 207 preserved) + `CODE REVIEW`
(violations found vs fixed, no behaviour change). Ledger row flips to `done` only when both are clean.
