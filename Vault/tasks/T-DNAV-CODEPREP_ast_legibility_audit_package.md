---
node_type: task
task_id: T-DNAV-CODEPREP
status: pending
pack: VAULT
lab: dnalab
mode: graph-tooling + coder lane
blocked_by:
- T-DNAV-CODE-CLEAN
consumers:
- modules.base — module map view
- graph/v2_code — AST code graph
- design→code→test spine (.base views)
tags:
- task
- vault
- dnalab
---

# T-DNAV-CODEPREP — AST-legibility audit of the DNALab package (`4dlab-code-prep`)

**Status:** `pending` · **Pack:** VAULT (DNALab) · **Mode:** GRAPH-TOOLING + coder lane (audit, then coder applies fixes under inner loop)
**Origin:** pipeline guide §4 (code prep) · **Blocked by:** T-DNAV-CODE-CLEAN (done — DNA-family)
**Consumer (signal/noise):** **Adds no schema field.** Produces a `file:line → rule → fix` audit report
against graphify's AST-legibility rules so the `graph/v2_code/` graph (built in `T-DNAV-GRAPH-AST`) has
clean module seams and accurate node labels. That code graph's consumer is the **vault build's
frontmatter derivation** (`implements`/`module`/`source`) feeding `modules.base` and the
design→code→test spine. No new fields; this is a structural audit of existing code.

### Role note ###

`4dlab-code-prep` **probes what your local graphify build actually extracts**, then **reports**
violations — it does **not** auto-rewrite source (a blanket auto-rewrite is forbidden: unreviewable
diff). The coder applies the reported fixes under the normal inner loop (`ruff`→`pyright`→`pytest -x -q`
after every edit). The skill never writes `graph.json` and never runs graphify.

### Pre-check (code track was waived, not re-verified) ###

CODE-CLEAN/TESTS-GREEN ship `done` from the DNA-family work (`T-DNA-7` schema bump, `T-DNA-13` clarity,
`T-DNA-TH-1` isolation harness). **Before auditing, run `pytest -q` once** on `labs/dnalab/` to confirm
the suite is still green on the current checkout. Baseline is ~27 dnalab tests. The
`test_assembly_integration.py::test_real_pipeline_smoke` case may **skip** when the sibling labs
(vinlab/symptomlab) are not installed in the sandbox — that skip is **environment-gated and expected; a
skip is NOT a gate failure.** Only a test *failure* is a STOP — do not prep on a red suite.

### Composition-layer note (read before treating the missing-enum lever as a violation) ###

DNALab is the **umbrella/composition layer** — it composes `VinDNA` + `SymptomDNA` (sibling-lab payloads)
into `VehicleDNA`. It owns **no domain `StrEnum`s** of its own (those belong to VINLab/SymptomLab). So the
guide's "domain states as real enums" AST-legibility lever **does not apply here** — its absence is
expected, not a violation to manufacture. The audit's real surface is imports / `__all__` / type hints /
`# WHY:` rationale on the schema-version gate.

### Scope ###

- **Package only:** `labs/dnalab/dnalab/` — `__init__.py`, `assembly.py`, `models.py`.
- **Excludes** `tests/` (its own run = `T-DNAV-TESTPREP`), `wiki/` (prose, not AST), and `docs/`.

### AST-legibility levers the audit checks (guide §3·1A) ###

Explicit named imports (no `from x import *`); a `__all__` public surface (`__init__.py` already exports
`["build_vehicle_dna", "VehicleDNA"]` ✓ — confirm it still matches the shipped symbols); type hints on
public signatures (`build_vehicle_dna(vin: str, triage: dict[str, Any]) -> VehicleDNA` ✓; the `VehicleDNA`
methods `.new`/`.to_json_payload`/`.to_json`/`.from_json_payload`); `# WHY:` rationale on the non-obvious
gate (the `from_json_payload` `schema_version` mismatch raise at `models.py`); every numeric/string
literal that encodes a contract value (e.g. `SCHEMA_VERSION = "1.2"`) carrying an inline rationale/cite.

### Known starting signal (post DNA-family code work) ###

`T-DNA-13` already cleaned naming (the `to_json` rename) and `T-DNA-7` landed the schema bump, so the
audit should be **light** (3-file package). Report — do not silently fix — any residual: a public symbol
that `assembly.py`/`__init__.py` re-exports but is missing from `__all__`; an untyped public method
signature on `VehicleDNA`; or the `SCHEMA_VERSION` literal / the `from_json_payload` raise lacking a
`# WHY:` rationale comment.

### Success criteria ###

1. `4dlab-code-prep probe → audit → report` run against `labs/dnalab/dnalab/`; report lists every
   violation as `file:line → rule → fix`, zero false positives spot-checked.
2. Coder applies the in-scope fixes; inner loop stays green — `ruff check .` clean, `pyright dnalab tests`
   clean, `pytest -x -q` with **zero failures** (env-gated `test_real_pipeline_smoke` skip expected); no
   test regressions.
3. Report explicitly confirms: no `import *`; public surface has `__all__` matching shipped symbols;
   public signatures typed; **no domain-enum lever expected** (composition layer — noted, not flagged).
4. No behaviour change (prep is legibility, not logic); no graphify run; no schema field added/removed;
   `VehicleDNA` wire shape byte-identical (`to_json_payload` keys unchanged).

### Out of scope ###

- `tests/` (→ `T-DNAV-TESTPREP`) · running graphify (→ `T-DNAV-GRAPH-AST`) · the docs/wiki tiers.
- Any behaviour or schema change to `assembly.py`/`models.py` (DNA-family closed that track).

### Files to touch ###

- `labs/dnalab/dnalab/*.py` — only the audit-reported legibility fixes.
- The audit report appended to the progress note (skill output convention).

### Verification (inner loop + audit) ###

```bash
cd <repo>/labs/dnalab
pytest -q                              # confirm green BEFORE prep (real_pipeline_smoke skip expected, not a failure)
ruff check . && pyright dnalab tests && pytest -x -q
grep -rn 'import \*' dnalab/ && echo "FAIL star-import" || echo "OK no star-import"
grep -n '__all__' dnalab/__init__.py
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DNAV-CODEPREP.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (suite green pre-prep / audit clean / fixes applied / inner loop green / counts
preserved) + `CODE REVIEW` (violations found vs fixed, no behaviour change). Ledger row → `done` only when
both are clean.
