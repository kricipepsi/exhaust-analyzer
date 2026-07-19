# T-V7-4 — Fresh driver + multi-dimension scorer

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `deferred` (→ `pending` when T-V7-3 is `done`) · **Blocked by:** T-V7-3
**Mode:** STRICT — adds a driver under `apps/wired/v7/`; **no `wired/`/lab/COMLab source edits**. · **Scope owner:** wired-v7.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Objective
Write a fresh driver that runs every v7 case through the **live** `wired.diagnose()`
and scores the verdict across **multiple dimensions** so the suite catches every error
class — not just a wrong top fault. Imports **nothing** from `ARCHIVE/`.

## Signal/noise
Adds no domain field or fault. The **named consumer** is the report T-V7-5. The driver
holds **no diagnostic logic** — it maps inputs, calls the public engine, compares to
the oracle.

## Pinned facts (verified at authoring)
- Engine: `from wired import diagnose` → `diagnose(raw_inputs, *,
  enable_fatal_gates=False) -> OrchestratorFinalUIOutput`; verdict on
  `.diagnostic_verdict`. **No `use_v2_registry`.**
- Corpus loader `apps/wired/v7/load_corpus.py` (T-V7-2); oracle in
  `apps/wired/v7/data/cases_petrol_v7.csv` `expected_*` columns + tags (T-V7-3).
- Optional tracing reuses `apps/wired/trace/setup_env_wired.sh` + the OTLP-provider
  bootstrap pattern in `apps/wired/trace/run_traced_case.py` (clone, do not import
  `ARCHIVE/`); span gate `WIRED_OTEL=1`.

## Scope
**IN:**
- `apps/wired/v7/run_suite.py`:
  - load corpus + oracle; per case call `diagnose()`; capture the full verdict.
  - **multi-dimension scoring** per the row tag:
    - `accuracy` case → score each pinned dimension independently: `fault_family`,
      `fault_code` (where pinned), `state` (where pinned), `confidence` in
      `[min,max]` (where pinned), `perception_gap` (where pinned),
      `demotion_note_contains` (substring, where pinned). Each dimension yields
      PASS/FAIL/NA; the case PASSES only if every **pinned** dimension passes.
    - `characterization` → RAN/ERROR only (no-crash), excluded from the %.
    - negative/edge → assert the expected HANDLED/abort outcome.
    - any exception from `diagnose()` on a well-formed case → `CRASH` (an error class).
  - emit a typed per-case result (case_id, category, tag, per-dimension outcomes,
    overall) + aggregates: per-family pass rate over `accuracy` cases, **per-dimension
    failure counts**, crash count, characterization no-crash rate. Write machine
    output to `apps/wired/v7/runs/<timestamp>/results.json` (**not** committed).
  - flags: `--case <id>`, `--family <name>`, `--category <name>`, `--trace` (OTLP
    provider + `WIRED_OTEL=1`; tag each span with `case_id` + outcome — reuse the
    `apps/wired/trace` bootstrap, no ARCHIVE import).
- `apps/wired/v7/tests/test_run_suite.py`: lock the scoring contract — feed 3–4
  synthetic (verdict, oracle-row) pairs and assert each dimension classifies
  correctly (a family match, a confidence-band miss, a demotion-substring miss, a
  crash). This is the scorer's own regression guard.

**OUT:** any `ARCHIVE/` import; any edit to `wired/`/labs/COMLab; diagnostic logic in
the driver; recomputing expectations at runtime (read the oracle); committing run
JSON; `graphify`; `Vault/`.

## Steps
1. Implement `run_suite.py` (load → diagnose → multi-dim score → aggregate); inner
   loop after each meaningful edit.
2. Implement each scoring dimension exactly per the oracle tags.
3. Write `tests/test_run_suite.py`; run it.
4. Smoke-run the full corpus (no `--trace`); confirm it completes + writes
   `results.json`.
5. Optional: one `--trace` case to confirm the Jaeger path (reuse T-WTEST-3 Jaeger).
6. Fill `v7_tasks/progress_notes/T-V7-4.md` gates; STOP.

## Success criteria
- `run_suite.py` runs the full corpus through the **live** `diagnose()` (no `ARCHIVE/`
  import), scores all six dimensions per the tags, writes typed per-case + aggregate
  results (incl. per-dimension failure counts + crash count) to a run dir (not
  committed), and never crashes on a well-formed case.
- `tests/test_run_suite.py` passes (each scoring dimension verified, incl. a crash
  case); `py_compile`/`ruff`/`pyright` clean.
- `git status` shows only new files under `apps/wired/v7/` + `apps/wired/v7_tasks/`; no
  run JSON staged; no source edits.

## VERIFICATION GATE — T-V7-4
Complete in `v7_tasks/progress_notes/T-V7-4.md`: inner-loop results; `test_run_suite.py`
output; full-corpus smoke-run summary (cases run, per-family tally, per-dimension
failure counts) + run-dir path; trace id if `--trace` exercised.

## CODE REVIEW — T-V7-4
Complete in `v7_tasks/progress_notes/T-V7-4.md`: no `ARCHIVE/` import (trace bootstrap
cloned); no diagnostic logic; expectations read from the oracle; no `use_v2_registry`;
run JSON not staged; `graphify` not run.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/v7/run_suite.py \
  apps/wired/v7/tests/test_run_suite.py \
  apps/wired/v7_tasks/progress_notes/T-V7-4.md \
  apps/wired/v7_tasks/V7_PROGRESS.md
git commit -m "T-V7-4: fresh v7 driver + multi-dimension scorer vs live diagnose()"
```
