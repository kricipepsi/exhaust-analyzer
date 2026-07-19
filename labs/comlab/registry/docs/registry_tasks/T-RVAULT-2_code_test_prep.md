### Goal ###

Make the registry **package** and its **test suite** AST-legible for graphify Pass-1,
by running `4dlab-code-prep` (probe → audit → report) over `labs/comlab/registry/`
(production package) and, as a second scoped run, over `labs/comlab/registry/tests/`,
then applying the fixes the report flags. Done when the code-prep report shows zero
outstanding AST-legibility violations and the inner loop is green on every edited file.

### Success criteria ###

- `4dlab-code-prep` report for the package and for `tests/` each end with **0
  must-fix violations** (explicit named imports, `__all__` public surface on modules,
  type hints on public signatures, domain states as real `StrEnum`/`Enum`,
  `# WHY:` on non-obvious gates — `schema_v2.py` enums already satisfy most of this).
- `ruff check` 0, `pyright` 0 on every edited file.
- `python3.14 -m pytest labs/comlab/registry/tests/ -q` stays green (baseline **471
  passed**, ledger 2026-06-21) — no test count regression.

### Context ###

Phase 2 code+test prep from `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md §4`, folded into
one task because Phase-1 code-clean and tests-green are **already met**: the registry
was revived clean under `T-REG-REVIVE-1` (ruff/pyright clean, 471 passed) and is
self-contained (no lab/COMLab imports — see `schema_v2.py` header). So this task is the
prep **audit**, not a refactor: `4dlab-code-prep` probes what the local graphify build
extracts and reports `file:line → rule → fix`; the coder applies only those fixes. A
blanket auto-rewrite is forbidden.

**Scope split (do not cross):** the package run **excludes** `tests/`; `tests/` is its
own second run. Package surface: `schema_v2.py`, `integration_shim.py`, `__init__.py`,
`shim/` (`payload_mirrors.py`), `tools/` (`build_corpus.py`, `render_case_library.py`).
The `rules/*.json` are **data**, not Python — they are not code-prep targets (they
enter the graph as data nodes via the AST run in T-RVAULT-4); do not "fix" them here.

**Python: 3.14 ONLY** — run every `python`/`pytest` via the shared host venv
(`/agent_workspace/.venv-wired` per `4DLab_CLAUDE.md` → "Python environment"); system
`python3` is 3.10 and breaks on `StrEnum`. Purge stale `__pycache__` before re-running
if a `.pyc` shadows an edit.

Load skills: `_skills/graph/4dlab-code-prep` (probe/audit/report), and the registry
inner-loop skill `labs/comlab/registry/docs/_registry_skills/registry-python`.

### Consumer (signal/noise) ###

N/A — no new field/enum/fault. AST-legibility prep does not add schema surface; it
makes existing surface statically visible to the Pass-1 extractor.

### Deliverables ###

1. `labs/comlab/registry/graph/CODE_PREP_REPORT.md` — the code-prep audit output
   (package + tests), violations resolved to 0.
2. Minimal AST-legibility fixes to flagged package files (imports/`__all__`/hints
   only — surgical).

### Files to touch ###

- `labs/comlab/registry/graph/CODE_PREP_REPORT.md` (CREATE)
- `labs/comlab/registry/*.py`, `shim/*.py`, `tools/*.py` (MODIFY — only flagged lines)

### Out of scope ###

No behaviour change — every edit must be import/typing/`__all__`/comment only and
trace to a report line. Do NOT touch `rules/*.json`. Do NOT run graphify (that is
T-RVAULT-4). Do NOT add fields, rules, or families. If the report flags a genuine
design smell beyond AST-legibility, log it as an Unplanned follow-up row — do not fix
it here.

GRAPH GUARDRAIL (standing): do NOT run `graphify` or rebuild any graph.

### Verification ###

```bash
cd /agent_workspace
PY=.venv-wired/bin/python   # 3.14 shared host venv (confirm path per 4DLab_CLAUDE.md)

# Inner loop on edited files
ruff check labs/comlab/registry
$PY -m pyright labs/comlab/registry 2>/dev/null || pyright labs/comlab/registry

# Suite still green (baseline 471)
$PY -m pytest labs/comlab/registry/tests/ -q

# Report exists and shows zero must-fix
test -f labs/comlab/registry/graph/CODE_PREP_REPORT.md && echo "report present"
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-RVAULT-2`: Status=done, Files changed={COUNT}, Verification="code+test prep clean; 471 green; ruff/pyright 0"
