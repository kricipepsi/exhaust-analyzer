# T-WTEST-5 — Extract the trace from Jaeger + write the trace report

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `deferred` (→ `pending` when T-WTEST-4 is `done`) · **Blocked by:** T-WTEST-4
**Mode:** STRICT — adds an extractor under `apps/wired/trace/` + one report; **no wired/lab/COMLab source edits**. · **Scope owner:** wired-test / tracing.
**Load skills:** wired-python, wired-verification-loop, wired-code-review, wired-jaeger-tracing (reference; clone, don't import `ARCHIVE/`).

## Objective
Pull the traced run (T-WTEST-4) out of Jaeger via its REST API into a raw JSON
artefact + a human-readable **trace report**: the span tree, per-phase durations,
and span status for the single oil case. This closes the loop — the run is now
inspectable offline, the way the archived `extract_blueprint` step did, but scoped
to one case on Linux.

## Signal/noise
Adds no domain field or fault. The **named consumer** is the **architect's review of
where time/▒errors sit in the wired pipeline** for the oil case (phase-of-failure
visibility) — the report at
`apps/wired/test_tasks/reports/WTEST5_TRACE_<date>.md` is the artifact that consumer
reads. Multi-case failure-mode aggregation has **no consumer in this single-case
pack** → deferred to the future accuracy-harness pack.

## Pinned facts (verified at authoring)
- Jaeger REST: `GET http://localhost:16686/api/traces?service=4dlab-wired-harness`
  returns trace JSON (the archived `extract_blueprint.py` queries exactly this and
  writes `traces-raw.json` / `services.json` / `operations.json`).
- **Do not import `ARCHIVE/`.** `extract_blueprint.py` is **reference** for the ~50-line
  REST-query + dump logic — clone it into `apps/wired/trace/`, do not import it.
  `analyse_failure_modes.py` is a **multi-case** tool that `from _jaeger.extract_blueprint
  import …` (an ARCHIVE import chain) and aggregates by `case_id` — **out of scope**
  here (single case; no consumer). List it as deferred, do not run/import it.
- Canonical span names to expect in the trace: see
  `apps/wired/tests/test_tracing.py::EXPECTED_SPANS` and the T-WTEST-4 progress note
  (recorded trace id).

## Scope
**IN:**
- Write `apps/wired/trace/extract_traces.py`: query the Jaeger REST API for service
  `4dlab-wired-harness` (optionally by the trace id recorded in T-WTEST-4), write
  `traces-raw.json` (+ a small `services.json`/`operations.json`) into a run dir
  (`apps/wired/trace/runs/<timestamp>/`). **Do not commit the JSON** — the
  explicit-path commit below excludes the run dir, so no `.gitignore` edit is needed.
  Clone the query/dump logic from `extract_blueprint.py`.
- Write the report `apps/wired/test_tasks/reports/WTEST5_TRACE_<date>.md`: the span
  tree (parent/child) for the oil case, each span's duration + status, the total
  trace duration, and a one-line "phase-of-failure readable: yes/no" verdict. Confirm
  the six `EXPECTED_SPANS` are present and correctly nested (OBD per case).
- Cross-link the report to the T-WTEST-1 baseline (suite green) and the T-WTEST-4
  verdict-invariance result so the trace is anchored to a passing, unchanged run.

**OUT:** running/importing `analyse_failure_modes.py` or any `ARCHIVE/_jaeger`
module; multi-case aggregation; any edit to `wired/`, a lab, or COMLab; committing
the raw trace JSON or the Jaeger binary; `graphify`; `Vault/`; secrets.

## Steps
1. Ensure Jaeger still holds the T-WTEST-4 trace (re-run T-WTEST-4 if the collector
   was restarted — spans are not persisted across a fresh binary start unless
   configured).
2. Write + run `apps/wired/trace/extract_traces.py`; dump `traces-raw.json` to the
   git-ignored run dir.
3. Parse the JSON; build the span tree + durations; write
   `WTEST5_TRACE_<date>.md`.
4. Confirm the six `EXPECTED_SPANS` + nesting; write the phase-of-failure verdict.
5. Fill the gate blocks in `test_tasks/progress_notes/T-WTEST-5.md`; STOP.

## Success criteria
- `extract_traces.py` retrieves the run's trace and writes `traces-raw.json` to the
  run dir (not staged/committed — explicit-path commit excludes it).
- Report exists, `.md`, with: span tree + per-span duration/status + total duration;
  confirmation the six `EXPECTED_SPANS` are present + nested under `wired.diagnose`;
  a one-line phase-of-failure-readable verdict; cross-links to T-WTEST-1 / T-WTEST-4.
- `git status` shows only new files under `apps/wired/trace/` (code) +
  `apps/wired/test_tasks/` (report/note); raw JSON + binary untracked; no
  `wired/`/lab/COMLab diffs; no secrets.

## VERIFICATION GATE — T-WTEST-5
Complete in `test_tasks/progress_notes/T-WTEST-5.md`: `extract_traces.py` output +
the run-dir path (ignored); a paste of the parsed span tree + durations; the
`EXPECTED_SPANS`-present check; report path.

## CODE REVIEW — T-WTEST-5
Complete in `test_tasks/progress_notes/T-WTEST-5.md`: no `ARCHIVE/` import (extractor
is a clone; `analyse_failure_modes.py` neither run nor imported); no `wired/`/lab/
COMLab edits; raw JSON + binary not staged; `graphify` not run.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/trace/extract_traces.py \
  apps/wired/test_tasks/reports/WTEST5_TRACE_<date>.md \
  apps/wired/test_tasks/progress_notes/T-WTEST-5.md \
  apps/wired/test_tasks/TEST_PROGRESS.md
git commit -m "T-WTEST-5: extract wired oil-case trace from Jaeger + trace report"
```
