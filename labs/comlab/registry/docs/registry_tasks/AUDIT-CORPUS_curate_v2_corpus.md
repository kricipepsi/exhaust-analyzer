# AUDIT-CORPUS — Curate the v2 ground-truth corpus from the 281-case master

### Goal ###

Produce the single curated corpus the v2 registry will be authored
against: a verified keep / drop / add disposition for every case in
`TestSuite/cases_petrol_master_v6.csv`, plus the specs for any new cases
the audit decides are needed. Outputs land in `registry/` as three
artefacts that downstream tasks (AUDIT-REG, AUDIT-CHEM, REG-V2-SCHEMA,
all REG-V2-AUTHOR-*, REG-WIKI) consume: a human narrative
(`CORPUS_AUDIT.md`), the curated CSV (`corpus_curated.csv`), and a
structured per-case metadata file (`corpus_meta.json`).

This task **measures and curates**. It does not author any rule, does not
modify the original `cases_petrol_master_v6.csv`, and does not write the
HTML wiki.

### Success criteria ###

The task is done when all of the following are true:

1. `registry/CORPUS_AUDIT.md` exists and contains:
   - A keep / drop / add summary table (counts by fault family).
   - A per-case disposition table for every case in
     `cases_petrol_master_v6.csv` with columns:
     `case_id | expected_top_fault_family | disposition (keep | drop | relabel) | rationale | source (cvsgaps | jaeger | csv | new)`.
   - A separate table for **new cases proposed by this audit** (beyond
     `cvsgaps.md`'s vacuum_leak / overheating / charging_system list) —
     each with `proposed_case_id | family | rationale | source_evidence`.
   - A bottom-line: total kept, total dropped, total new, projected
     curated-corpus PASS-rate floor against the current v1 router.
2. `registry/corpus_curated.csv` exists and contains:
   - All KEEP rows from `cases_petrol_master_v6.csv` (same columns,
     verbatim).
   - All ADD rows (the new cases) with synthesized values matching the
     master_v6 schema. A new-case row uses `case_id` prefix `NEW-` to
     distinguish.
3. `registry/corpus_meta.json` exists and validates against the inline
   schema below (Pydantic `CorpusMeta`). Every row in
   `corpus_curated.csv` has a matching entry in `corpus_meta.json`.
4. The discovery clause: if the Jaeger trace data reveals a chemistry /
   evidence pattern that the existing CSV cases do not characterize,
   propose a new case in the **ADD** table with the source flagged
   `jaeger`. Do not propose new cases without trace evidence; do not
   skip proposing them when the evidence is there.
5. Every `cvsgaps.md` keep/drop disposition is either accepted or
   overruled in `CORPUS_AUDIT.md`, with the rationale recorded.
   `cvsgaps.md` is a proposal, not truth — the audit verifies each row
   against the actual CSV + traces before adopting.
6. The wired test suite stays green (no harness or wired code changed):
   `pytest 4DLabWired/tests/ -x -q` exits 0.
7. No file under `4DLabWired/`, `COMLab/`, `GASLab/`, `OBDLab/`,
   `DTCLab/`, `DNALab/`, `TestSuite/` is modified by this task.

### Context ###

The 281-case `cases_petrol_master_v6.csv` is contaminated with
analyser-hardware faults, leaded-fuel scenarios, hybrid edges, contrived
multi-fault combinations, and duplicate baselines. The current 16.0 %
accuracy figure is measured against this noisy ground truth. Curating
the corpus is the prerequisite for the v2 rule rebuild — you cannot
author rules against noise.

Inputs (read-only):
- `TestSuite/cases_petrol_master_v6.csv` — 281 rows, 66 columns. Schema
  documented implicitly by `4DLabWired/harness/run_cases.py` (read the
  `_NON_CONSUMER_COLUMNS` list at line 35–50 — those columns exist for
  metadata, not consumption).
- `registry/cvsgaps.md` — corpus-curation proposal. Recommends keeping
  high-frequency families (lean, rich, misfire, catalyst), adding three
  new families (vacuum_leak, overheating, charging_system), and dropping
  ~30–40 noise cases. Treat as a proposal; verify each disposition.
- `4DLabWired/_jaeger/runs/20260527-044325/DIAGNOSTIC_CAPABILITY_ANALYSIS.md`
  — the trace-based failure analysis. The "Expected × Predicted pivot"
  table (§1.2) and the per-phase breakdowns are where to look for the
  evidence behind the discovery clause.
- `4DLabWired/_jaeger/runs/20260527-044325/FAILURE_BLUEPRINT.md` —
  per-case verdict + phase, deduped to 281 rows. Cross-reference when a
  disposition decision turns on what actually happened in the trace.
- `4DLabWired/_jaeger/runs/20260527-044325/traces-raw.json` — full trace
  data (~14 MB). Sample programmatically when a per-case decision needs
  the actual span tags.

`Load skills:` (none on-demand — audit-only, no rule schema yet)

The `corpus_meta.json` schema (Pydantic, written inline in the
verification script — do **not** add `pydantic` to a registry package
just for this task; use a one-file script with a local model):

```python
from typing import Literal
from pydantic import BaseModel, Field

Disposition = Literal["keep", "drop", "relabel", "new"]
Source = Literal["cvsgaps", "jaeger", "csv", "new"]

class CaseMeta(BaseModel):
    case_id: str
    expected_top_fault_family: str
    disposition: Disposition
    relabel_to: str | None = None              # only when disposition == "relabel"
    rationale: str
    source: Source                              # which input drove the decision
    chemistry_signature: str | None = None      # GASLab chemistry_state observed in traces, if known
    dtcs: list[str] = Field(default_factory=list)
    notes: str | None = None

class CorpusMeta(BaseModel):
    generated_at: str                           # ISO 8601 UTC
    master_csv_total: int                       # 281
    curated_count: int                          # kept + new
    dropped_count: int
    relabel_count: int
    new_count: int
    cases: list[CaseMeta]
```

### Deliverables ###

1. `registry/CORPUS_AUDIT.md` — human-narrative audit with the four
   tables described in success criteria #1.
2. `registry/corpus_curated.csv` — curated CSV; KEEP rows + ADD rows;
   same column schema as `cases_petrol_master_v6.csv`.
3. `registry/corpus_meta.json` — structured per-case metadata, conforming
   to the `CorpusMeta` Pydantic model inlined in the verification script.
4. `registry/tools/build_corpus.py` — one-shot script that (a) reads the
   master CSV + `cvsgaps.md` + the Jaeger trace data, (b) emits the
   three artefacts above, (c) validates `corpus_meta.json` against
   `CorpusMeta`. Idempotent (re-running on the same inputs produces the
   same outputs).

### Files to touch ###

- `registry/CORPUS_AUDIT.md` (CREATE)
- `registry/corpus_curated.csv` (CREATE)
- `registry/corpus_meta.json` (CREATE)
- `registry/tools/__init__.py` (CREATE — empty)
- `registry/tools/build_corpus.py` (CREATE)
- `registry/tests/test_build_corpus.py` (CREATE — fixture test covering
  CorpusMeta schema validation + a sample keep/drop/add scenario)
- `registry/REGISTRY_PROGRESS.md` (MODIFY — flip AUDIT-CORPUS row to
  done at session end)
- `registry/registry_tasks/progress_notes/AUDIT-CORPUS.md` (CREATE —
  VERIFICATION GATE + CODE REVIEW blocks)

### Out of scope ###

- **Do not author any rule.** No JSON files under `registry/rules/` — that
  is REG-V2-AUTHOR-* territory.
- **Do not write `schema_v2.py`.** That is REG-V2-SCHEMA. The Pydantic
  `CorpusMeta` model above lives inside `build_corpus.py` only.
- **Do not modify `cases_petrol_master_v6.csv`.** The master CSV is
  preserved as the input of record; the curated CSV is a separate file
  under `registry/`.
- **Do not write the HTML wiki.** That is REG-WIKI.
- **Do not run the harness.** Curation is independent of pipeline state.
- **Do not touch any lab, COMLab, or 4DLabWired code.** The registry is
  self-contained.

Surgical-change rule: every changed line traces to a Deliverable. If you
spot a defect in `cases_petrol_master_v6.csv` (e.g., a typo in
`expected_top_fault_family`), log it as `T##b` under "Unplanned
follow-ups" in `REGISTRY_PROGRESS.md` — do not fix it in this diff.

### Verification ###

Run from the workspace root with `.venv-wired` active.

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop on touched Python files
ruff check registry/ --fix
pyright registry/
pytest registry/tests/ -x -q

# Structural checks
python -c "import csv; rows = list(csv.DictReader(open('registry/corpus_curated.csv'))); print(f'curated rows: {len(rows)}')"
python -c "import json; d = json.load(open('registry/corpus_meta.json')); print(f'meta entries: {len(d[\"cases\"])}, curated_count: {d[\"curated_count\"]}, dropped: {d[\"dropped_count\"]}, new: {d[\"new_count\"]}')"

# Contract: every corpus_curated.csv row has a meta entry, and vice versa
python -c "import csv, json; \
  csv_ids = {r['case_id'] for r in csv.DictReader(open('registry/corpus_curated.csv'))}; \
  meta = json.load(open('registry/corpus_meta.json')); \
  meta_ids = {c['case_id'] for c in meta['cases'] if c['disposition'] in ('keep','new','relabel')}; \
  missing_in_meta = csv_ids - meta_ids; \
  missing_in_csv = meta_ids - csv_ids; \
  assert not missing_in_meta, f'CSV rows lack meta: {missing_in_meta}'; \
  assert not missing_in_csv, f'meta references missing CSV rows: {missing_in_csv}'; \
  print('contract OK')"

# Contract: every cvsgaps.md disposition is addressed in CORPUS_AUDIT.md
python -c "import re, pathlib; \
  cvs = pathlib.Path('registry/cvsgaps.md').read_text(); \
  audit = pathlib.Path('registry/CORPUS_AUDIT.md').read_text(); \
  cvs_ids = set(re.findall(r'\b([A-Z]+-?N?\d+|case_\d+|CSV-\d+|EXT-\d+|EXP-N\d+|TC\d+|YAML-[A-Z0-9]+|PDF-HI-\d+)\b', cvs)); \
  missing = [cid for cid in cvs_ids if cid not in audit]; \
  assert not missing, f'cvsgaps cases not addressed in audit: {missing[:10]}'; \
  print(f'all {len(cvs_ids)} cvsgaps cases addressed')"

# Regression: no wired or harness file touched
python -c "import subprocess; out = subprocess.check_output(['git','status','--porcelain']).decode(); \
  bad = [l for l in out.splitlines() if any(l[3:].startswith(p) for p in ['4DLabWired/', 'COMLab/', 'GASLab/', 'OBDLab/', 'DTCLab/', 'DNALab/', 'TestSuite/'])]; \
  assert not bad, f'out-of-scope edits: {bad}'; print('scope OK')"

# Regression: wired tests still green
pytest 4DLabWired/tests/ -x -q
```

All steps must pass.

### Progress hook ###

REGISTRY_PROGRESS.md `AUDIT-CORPUS`: Status=done, Files changed=8,
Verification="curated <N> cases (kept <K>, dropped <D>, new <A>); meta+csv
contract OK; <C> cvsgaps cases addressed; wired suite green"
