# REG-WIKI — render the per-fault-family HTML case library

### Goal ###

Render a static, browsable HTML case library from the curated corpus so a human
can review, per fault family, exactly which cases the registry is built against —
their inputs (gas / OBD / DTC), the expected verdict, and the reasoning. Consumes
`corpus_curated.csv` + `corpus_meta.json` (both already produced by AUDIT-CORPUS);
produces one self-contained HTML file grouped by `expected_top_fault_family`. This
is a read-only documentation/tooling deliverable — no rule or schema change. Done
when the page renders every curated case, grouped by family, and opens standalone.

### Success criteria ###

- A script reads `corpus_curated.csv` + `corpus_meta.json` and writes one
  self-contained HTML file (inline CSS; no external assets) under `registry/docs/`.
- Every row in `corpus_curated.csv` appears exactly once; the case count in the
  page matches `len(corpus_curated.csv)` and the family counts match
  `corpus_meta.json`.
- Cases are grouped under a heading per `expected_top_fault_family`, with a
  family index / jump-links at the top.
- Each case card shows: `case_id`, `description`, the gas block (`hc, co, co2, o2,
  nox, lambda_analyser`), the trim/OBD block (`stft_b1/ltft_b1/…, obd_lambda, map,
  maf, rpm, ect`), `dtcs`, and the expected columns (`expected_top_fault`,
  `expected_top_fault_family`, `expected_state`, `expected_confidence_min/max`,
  `reasoning`).
- Re-running the script is deterministic (same input → byte-identical output).
- Document readability gate passes (per `4DLab/CLAUDE.md`); the script is lint/type clean.

### Context ###

`registry/corpus_curated.csv` is the curated 252-case corpus (header columns
include `case_id, description, hc, co, co2, o2, nox, lambda_analyser, stft_b1,
ltft_b1, stft_b2, ltft_b2, obd_lambda, …, dtcs, …, expected_top_fault,
expected_top_fault_family, expected_state, expected_confidence_min,
expected_confidence_max, reasoning, …`); `registry/corpus_meta.json` carries the
per-family counts and corpus metadata. AUDIT-CORPUS produced both; this task only
**reads** them. The original reference layout (`TestSuite/cases_petrol.html`) is
not in-tree — specify the structure from the columns above rather than chasing it.
The library is a review aid for rule authoring/audit; it has no runtime consumer
and adds no field, so it carries no signal/noise obligation.

Load skills: the registry bundle (`registry/docs/_registry_skills/_INDEX.md` —
`registry-python`, `registry-verification-loop`, `registry-code-review`); env per
`REGISTRY_START_HERE.md`.

### Deliverables ###

1. `registry/tools/render_case_library.py` — reads `corpus_curated.csv` +
   `corpus_meta.json`, emits the HTML. Pure stdlib (`csv`, `json`, `html`); no new
   dependency. Deterministic ordering (family name, then `case_id`).
2. `registry/docs/case_library.html` — the rendered output (committed artefact).
3. `registry/tests/test_render_case_library.py` — asserts: every CSV row rendered
   once; family counts == `corpus_meta.json`; output is deterministic on re-run;
   no unescaped user text (HTML-escape all cell values).

### Files to touch ###

- `registry/tools/render_case_library.py` (CREATE)
- `registry/docs/case_library.html` (CREATE — generated artefact)
- `registry/tests/test_render_case_library.py` (CREATE)
- `registry/docs/REGISTRY_PROGRESS.md` (flip row)
- `registry/docs/registry_tasks/progress_notes/REG-WIKI.md` (gates)

### Out of scope ###

No edits to `corpus_curated.csv` / `corpus_meta.json` (read-only; data fixes are
AUDIT-CORPUS follow-ups). No rule/schema changes. No live-server / interactivity
(static HTML only). No re-running the diagnostic engine to compute verdicts — the
page shows the **expected** columns from the curated CSV, not freshly-scored
output. Surgical-change rule: adjacent data issues → Unplanned follow-ups.

### Verification ###

```bash
cd labs/comlab/registry   # env per REGISTRY_START_HERE.md
python tools/render_case_library.py            # writes docs/case_library.html
python -m pytest registry/tests/test_render_case_library.py -q
# determinism: re-render and diff
python tools/render_case_library.py && git diff --quiet registry/docs/case_library.html && echo "deterministic OK"
# count parity
python -c "import csv; n=sum(1 for _ in csv.DictReader(open('corpus_curated.csv'))); print('csv rows', n)"
```

### Progress hook ###

`REGISTRY_PROGRESS.md` `REG-WIKI`: Status=done, Files changed={COUNT},
Verification="case_library.html renders N curated cases grouped by family; counts match corpus_meta.json; deterministic; tests green".
