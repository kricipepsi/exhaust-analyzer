### Goal ###

Produce the **explicit docs file list** that becomes the registry's vault `docs/`
tier, and reconcile each listed doc to the **shipped** `schema_v2.py` ground truth
(16 rule families, 34-value `ChemistryState`, the curated 252-case corpus). This is
the registry's Phase-1D equivalent — a *reconcile-and-pin*, NOT authoring a 6-doc
HLD/DLD/LLD/ADR/BDD/PRD pack (see Context for why that is out of scope). Done when
`registry/docs/VAULT_DOCS_MANIFEST.md` exists, names the included files + the
excluded files with one-line reasons, and every included file's figures match the
AST/corpus ground truth.

### Success criteria ###

- `registry/docs/VAULT_DOCS_MANIFEST.md` exists with two tables: **INCLUDE** (the
  docs tier) and **EXCLUDE** (with reason), no `docs/*.md` glob anywhere.
- For every INCLUDE doc, a `grep`-level reconciliation check passes: family count
  = 16, `ChemistryState` value count = 34, curated case count = 252 — any figure
  that disagrees with `schema_v2.py` / `corpus_meta.json` is corrected in-doc, and
  the correction is listed in the manifest's "Reconciled" column.
- `python -c "import json,glob; ..."` style check (in Verification) confirms the
  three ground-truth numbers the docs are reconciled against.

### Context ###

This task replaces Phase 1D of `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md §3` for the
registry. Per the pipeline's **exclusion discipline** ("Phase 2 doc-prep must ingest
an explicit file list, never a `docs/*.md` glob") the architect pins the list here so
the downstream doc-prep (T-RVAULT-3) has a clean, deglobbed input.

**Why no full 6-doc pack (settled by web research, architect 2026-06-28):** design
docs (HLD/LLD/PRD) are a *pre-implementation* feedback artefact and a historical
record; authoring them retroactively for already-shipped, green, self-contained code
is the exact case the literature says to skip (Google eng-practices: for small
components a full design doc "may not be justified"; ADRs are skipped when a decision
is "limited in scope … or already covered elsewhere"). The registry is a rule-data
package whose **rules ARE the spec** ("rules so readable they serve as documentation").
Its one architecturally-significant decision is already captured at
`labs/comlab/docs/adr/ADR-0006_separate_rule_registry_from_fault_atlas_kg.md`.

**Ground truth to reconcile against (read these, narrow):**
- `labs/comlab/registry/schema_v2.py` — `class FaultFamily` (16 values), `class
  ChemistryState` (34 values; the `REG-V2-CHEMSIG-34` parity, ledger 2026-06-21).
- `labs/comlab/registry/corpus_meta.json` — curated case totals (252; 241 kept + 11
  new per `AUDIT-CORPUS`).
- `labs/comlab/registry/rules/` — 16 family JSON files (the live rule set).

**Candidate INCLUDE (confirm/curate, do not assume):** `SCHEMA_V2_SPEC.md`,
`REGISTRY_AUDIT.md`, `CHEMISTRY_COVERAGE.md`, `CORPUS_AUDIT.md`, `case_library.html`.
**Candidate EXCLUDE:** `cvsgaps.md` (curation-driver scratch), `Vol5.md` (source
extract), `REGISTRY_START_HERE.md` + `REGISTRY_START_HERE_AUDIT_RESPONSE.md` +
`REGISTRY_PROGRESS.md` (workstream infra), `registry_tasks/**` (task pack),
`_registry_skills/**` (skill bundle). Confirm each by opening its head, not by name.

Load skills: none (architect/author-lane reconcile; no inner loop).

### Consumer (signal/noise) ###

N/A — no new field/enum/fault. This task pins a file list and corrects stale figures;
it adds no schema surface. (The docs' downstream consumer is the vault build's
frontmatter derivation in T-RVAULT-6, named there.)

### Deliverables ###

1. `labs/comlab/registry/docs/VAULT_DOCS_MANIFEST.md` — INCLUDE/EXCLUDE tables +
   "Reconciled" column.
2. In-place figure corrections to any INCLUDE doc whose family/chemistry/case counts
   are stale (each correction logged in the manifest).

### Files to touch ###

- `labs/comlab/registry/docs/VAULT_DOCS_MANIFEST.md` (CREATE)
- `labs/comlab/registry/docs/SCHEMA_V2_SPEC.md` (MODIFY — only if a figure is stale)
- `labs/comlab/registry/docs/REGISTRY_AUDIT.md` (MODIFY — only if stale)
- `labs/comlab/registry/docs/CHEMISTRY_COVERAGE.md` (MODIFY — only if stale)
- `labs/comlab/registry/docs/CORPUS_AUDIT.md` (MODIFY — only if stale)

### Out of scope ###

Do NOT author HLD/DLD/LLD/ADR/BDD/PRD for the registry. Do NOT rewrite prose for
style — only correct figures that disagree with the AST/corpus ground truth. Do NOT
touch `rules/*.json`, code, or tests. Do NOT build any graph. If a doc is so stale it
needs a structural rewrite, STOP and log it as a follow-up row — do not rewrite it in
this task.

GRAPH GUARDRAIL (standing, every task): do NOT run `graphify` or rebuild any graph.

### Verification ###

```bash
cd /agent_workspace/labs/comlab/registry

# Ground-truth numbers the docs must match
python3 - <<'PY'
import json, re, pathlib
sv = pathlib.Path("schema_v2.py").read_text()
fam = len(re.findall(r'^\s+[A-Z_]+\s*=\s*"', sv.split("class FaultFamily")[1].split("class ")[1] if False else sv))  # sanity only
meta = json.load(open("corpus_meta.json"))
rules = list(pathlib.Path("rules").glob("*.json"))
print("rule-family files:", len(rules))           # expect 16
print("corpus cases (meta):", meta.get("total") or meta.get("case_count") or "INSPECT")
PY

# Manifest exists and has no glob
test -f docs/VAULT_DOCS_MANIFEST.md && ! grep -q 'docs/\*\.md' docs/VAULT_DOCS_MANIFEST.md && echo "manifest OK"
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-RVAULT-1`: Status=done, Files changed={COUNT}, Verification="docs tier list pinned + reconciled to 16/34/252"
