---
node_type: task
task_id: T-VIN-CODEPREP
status: pending
pack: VAULT
lab: vinlab
mode: graph-tooling + coder lane
blocked_by:
- T-VIN-CODE-CLEAN
consumers:
- modules.base — module map view
- graph/v2_code — AST code graph
- design→code→test spine (.base views)
tags:
- task
- vault
- vinlab
---

# T-VIN-CODEPREP — AST-legibility audit of the VINLab package (`4dlab-code-prep`)

**Status:** `pending` · **Pack:** VAULT (VINLab) · **Mode:** GRAPH-TOOLING + coder lane (audit, then coder applies fixes under inner loop)
**Origin:** pipeline guide §4 (code prep) · **Blocked by:** T-VIN-CODE-CLEAN (done — DNA-family)
**Consumer (signal/noise):** **Adds no schema field.** Produces a `file:line → rule → fix` audit report
against graphify's AST-legibility rules so the `graph/v2_code/` graph (built in `T-VIN-GRAPH-AST`) has
clean module seams and accurate node labels. That code graph's consumer is the **vault build's
frontmatter derivation** (`implements`/`module`/`source`) feeding `modules.base` and the
design→code→test spine. No new fields; this is a structural audit of existing code.

### Role note ###

`4dlab-code-prep` **probes what your local graphify build actually extracts**, then **reports**
violations — it does **not** auto-rewrite source (a blanket auto-rewrite is forbidden: unreviewable
diff). The coder applies the reported fixes under the normal inner loop (`ruff`→`pyright`→`pytest -x -q`
after every edit). The skill never writes `graph.json` and never runs graphify.

### Pre-check (code track was waived, not re-verified) ###

CODE-CLEAN/TESTS-GREEN ship `done` from the DNA-family work (`T-DNA-12/13/TH-2` + the tri-module audit).
**Before auditing, run `pytest -q` once** on `labs/vinlab/` to confirm the suite is still green on the
current checkout. Baseline is ~177 passed / ~11 skipped — the skips are **environment-gated** (external
corpus CSVs / MySQL dataset absent in the sandbox) and **are expected; a skip is NOT a gate failure.**
Only a test *failure* is a STOP — do not prep on a red suite.

### Gate scoping (read before treating anything as a blocker) ###

Two conditions are **explicitly out of this gate** — record them, do not block on them:

1. **Env-gated skips** (~11) — expected, per the pre-check above. The gate is *zero failures*, not *zero
   skips*.
2. **`pyright` on the out-of-package scripts.** This task's scope is the **`labs/vinlab/vinlab/` package**
   (the vault code tier). The top-level data-loading scripts (`dump_schema.py`, `load_tecdoc.py`,
   `mysql_bridge.py`, `setup_tecdoc_db.py`) and `tools/*.py` import optional deps (MySQL / pyngrok) and
   are **never copied into the vault** — a bare/default `pyright` that sweeps them in will fail on missing
   imports, which is a **pre-existing repo condition unrelated to this task** (logged as a follow-up in
   START_HERE §6). Scope the type-check to the package + tests: **`pyright vinlab tests`** — that passing
   is the gate.

### Scope ###

- **Package only:** `labs/vinlab/vinlab/` — `__init__.py`, `decoder.py`, `models.py`, `db/` (`tecdoc_query.py`,
  `__init__.py`), `overlay/` (`air_metering.py`, `cylinder_heuristic.py`, `horizon.py`, `stress_rpm.py`,
  `switches.py`, `__init__.py`).
- **Excludes** `tests/` (its own run = `T-VIN-TESTPREP`), `wiki/` (prose, not AST), and the bundled
  `vinlab/data/` CSV dataset (data, not code).

### AST-legibility levers the audit checks (guide §3·1A) ###

Explicit named imports (no `from x import *`); a `__all__` public surface; type hints on public
signatures; domain states as real `StrEnum`s (graphify reads these as nodes — already true for `Horizon`,
`EuroEmissionCategory`, `InductionType`, `AirMeteringStrategy`, `PrimaryLoadCalculation`,
`FuelDeliveryType`, `UpstreamO2Type`, `VinConfidence`, `DownstreamTrimRole`); `# WHY:` rationale on
non-obvious gates (the `_is_non_petrol` reject, the euro→horizon derivation, the cylinder-heuristic
fallback chain); every numeric literal in `vinlab/` carrying its wiki-citation comment.

### Known starting signal (post DNA-family code work) ###

`T-DNA-12` already split `decode_vin_payload()` into named private helpers and `T-DNA-13` cleaned naming,
so the audit should be light. Report — do not silently fix — any residual: a public symbol the decoder
or DNA assembly imports (`RobustVINDecoder`, `pre_clean_vin`, `classify_air_metering`, `infer_cylinder`,
`euro_to_horizon`, `stress_idle_rpm`, `derive_upstream_o2_type`) that is not in a `__all__`; a public
`overlay/` helper with an untyped signature; or a brand-rule numeric literal in `cylinder_heuristic.py`
lacking an inline cite.

### Success criteria ###

1. `4dlab-code-prep probe → audit → report` run against `labs/vinlab/vinlab/`; report lists every
   violation as `file:line → rule → fix`, zero false positives spot-checked.
2. Coder applies the in-scope fixes; inner loop stays green — `ruff check .` clean, `pyright vinlab tests`
   clean (package scope, not the out-of-package MySQL/pyngrok scripts), `pytest -x -q` with **zero
   failures** (env-gated skips expected, ~177 passed / ~11 skipped); no test regressions.
3. Report explicitly confirms: no `import *`; public surface has `__all__` or a stated reason; public
   signatures typed; domain enums are real `StrEnum`s.
4. No behaviour change (prep is legibility, not logic); no graphify run; no schema field added/removed;
   `VinDNA`/`VehicleDNA` wire shape byte-identical.

### Out of scope ###

- `tests/` (→ `T-VIN-TESTPREP`) · running graphify (→ `T-VIN-GRAPH-AST`) · touching `vinlab/data/` CSVs.
- Any behaviour or schema change to the decoder/overlay (DNA-family closed that track).

### Files to touch ###

- `labs/vinlab/vinlab/**/*.py` — only the audit-reported legibility fixes.
- The audit report appended to the progress note (skill output convention).

### Verification (inner loop + audit) ###

```bash
cd <repo>/labs/vinlab
pytest -q                              # confirm green BEFORE prep (skips expected, not a failure)
ruff check . && pyright vinlab tests && pytest -x -q   # pyright scoped to package+tests, NOT top-level scripts
grep -rn 'import \*' vinlab/ && echo "FAIL star-import" || echo "OK no star-import"
grep -rn '__all__' vinlab/__init__.py vinlab/decoder.py vinlab/models.py | head
```

### Progress hook ###

`Vault/tasks/progress_notes/T-VIN-CODEPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (suite green pre-prep / audit clean / fixes applied / inner loop green / counts
preserved) + `CODE REVIEW` (violations found vs fixed, no behaviour change). Ledger row → `done` only when
both are clean.
