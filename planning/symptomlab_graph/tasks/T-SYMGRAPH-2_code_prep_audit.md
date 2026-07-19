# T-SYMGRAPH-2 — `4dlab-code-prep` audit + apply on the production package

**Status:** pending · **Pack:** symptomlab_graph · **Mode:** LITE · **Blocked by:** —
(code-clean already DONE)

### Goal ###

Run `4dlab-code-prep` (`probe` → `audit` → `report`) on the **production package only**,
`labs/symptomlab/symptomlab/`, to produce a fix-plan against the AST-legibility rules, then
apply the listed `file:line → rule → fix` items. Proof of done: the `4dlab-code-prep` report
shows zero outstanding AST-legibility violations (or each remaining one is justified), and
the inner loop is green after the applied fixes. **No graph is built in this task.**

### Success criteria ###

- `4dlab-code-prep` final report: 0 outstanding AST-legibility violations on
  `labs/symptomlab/symptomlab/` (justify any deliberate exception in the note).
- `ruff check labs/symptomlab/symptomlab` + `pyright labs/symptomlab/symptomlab` clean.
- `cd labs/symptomlab && pytest` still green (fixes changed no behaviour).

### Context ###

Pass-1 graphify reads the package with tree-sitter (a static read of code structure — no
language model, offline, free); its node/edge quality depends only on what is *statically
visible*. `4dlab-code-prep` probes what the local graphify build actually extracts and
reports violations — it **audits, it does not auto-rewrite source** (a blanket rewrite is a
forbidden, unreviewable diff). The AST-legibility levers to confirm (pipeline guide §1A/§4):
explicit named imports (no `from x import *`), a `__all__` public surface, type hints on
public signatures, fixed domain value-sets as real `Enum`/`StrEnum` (a named-value set, not
bare strings) where the set is fixed, `# WHY:` comments on non-obvious gates, and
wiki-citation comments on numeric literals. Package is small —
`models.py`, `validator.py`, `data/`.

**Load skills:** `_skills\graph\4dlab-code-prep\SKILL.md` (read end-to-end before running;
follow its `probe`/`audit`/`report` operations). Read-narrow everything else.

### Consumer (signal/noise) ###

N/A — no new field/enum/fault. This is an AST-legibility audit + mechanical fixes, not a
schema change. (If the audit *suggests* a new `Enum`, that enum's value set must already
exist as the validator's allowed strings — it is a representation change of an existing
surface, not a new field; confirm a live reader before promoting, else leave as-is and note.)

### Deliverables ###

1. `labs/symptomlab/symptomlab/*.py` — only the fixes the report lists (imports, `__all__`,
   type hints, enums-of-existing-values, `# WHY:`/citation comments).
2. The `4dlab-code-prep` report artefact at the path the skill writes it.
3. `planning/symptomlab_graph/tasks/progress_notes/T-SYMGRAPH-2.md` — `## Plan` + the report
   summary + before/after violation count.

### Files to touch ###

- `labs/symptomlab/symptomlab/models.py` (MODIFY — as report dictates)
- `labs/symptomlab/symptomlab/validator.py` (MODIFY — as report dictates)
- `labs/symptomlab/symptomlab/data/*` (MODIFY only if report flags a literal/citation)
- progress note (CREATE)

### Out of scope ###

**Exclude `tests/` and any `research/`** — the test corpus is prepped separately in
T-SYMGRAPH-3. No wiki/docs. No behaviour change, no refactor beyond the report's listed
fixes, no blanket auto-rewrite. **GRAPH GUARDRAIL:** do not run `graphify` or touch any
`graph/` dir — this is not a KG-lane task; `4dlab-code-prep` itself never writes `graph.json`.

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2
# run the prep skill's probe/audit/report on the package (see its SKILL.md for exact CLI)
#   scope = labs/symptomlab/symptomlab   (NOT tests/, NOT research/)
ruff check labs/symptomlab/symptomlab
pyright labs/symptomlab/symptomlab
cd labs/symptomlab && pytest -q
```

All steps pass; attach the final report and confirm 0 outstanding violations.

### Progress hook ###

PROGRESS `T-SYMGRAPH-2`: Status=done, Files changed=<count>, Verification="code-prep 0 violations; inner loop green".
