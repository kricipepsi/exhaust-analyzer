# T-WTEST-4 — Run the wired oil case under OTel; spans land in Jaeger

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `deferred` (→ `pending` when T-WTEST-3 is `done`) · **Blocked by:** T-WTEST-3
**Mode:** STRICT — adds a run harness under `apps/wired/trace/`; **no wired/lab/COMLab source edits**. · **Scope owner:** wired-test / tracing.
**Load skills:** wired-python, wired-verification-loop, wired-code-review, wired-jaeger-tracing (reference; clone, don't import `ARCHIVE/`).

## Objective
Drive the **single oil-burning case** end-to-end through the live `diagnose()` with
tracing on, so the canonical wired span tree lands in the Jaeger backend stood up in
T-WTEST-3 — **without changing the verdict**. This is the runtime proof that the
T-WIRE-3 instrumentation works against a real collector, not just an in-memory
exporter.

## Signal/noise
Adds no domain field or fault; observability only. The **named consumer** is
**T-WTEST-5** (which extracts + analyses the traces this run produces) and the
architect verifying the trace path. The verdict-invariance check reuses the exact
contract T-WIRE-3 already pinned (`test_tracing.py::test_verdict_identical_traced_vs_untraced`).

## Pinned facts (verified at authoring)
- Live span gate: `wired/tracing.py` → `TRACE_ENV_VAR = "WIRED_OTEL"`; spans emit
  iff `WIRED_OTEL` is truthy **and** an OTel provider is registered. It calls
  `opentelemetry.trace.get_tracer("wired")` against the **global** provider — it does
  **not** build an exporter. So the run harness must **register an OTLP
  `TracerProvider`** (clone the `_sanity_emit_span.py` / `_tracer.py` pattern into
  `apps/wired/trace/`; do **not** import `ARCHIVE/`) **and** set `WIRED_OTEL=1`.
- Canonical span set (from `apps/wired/tests/test_tracing.py::EXPECTED_SPANS`):
  `wired.diagnose`, `lab.dnalab.build`, `lab.gaslab.process`, `lab.obdlab.translate`,
  `lab.dtclab.sanitize`, `comlab.process`. The OBD span only appears when the case
  carries an `obd` block (see that test's `_obd_inputs()`).
- Case + runner: `apps/wired/wired/run_case.py` (`load_case`, `main`); the end-to-end
  oil case used by T-WIRE-2 verification is **MW-002** (`run_case --case MW-002`
  exits 0). Fixtures live in `apps/wired/tests/fixtures/oil_cases/`.
- Verdict-invariance is already a test:
  `test_tracing.py::test_verdict_identical_traced_vs_untraced`.

## Scope
**IN:**
- With Jaeger running (T-WTEST-3) and `apps/wired/trace/setup_env_wired.sh` sourced,
  write `apps/wired/trace/run_traced_case.py`: register an OTLP `TracerProvider`
  (BatchSpanProcessor → `localhost:4317`, service `4dlab-wired-harness`), set/honour
  `WIRED_OTEL=1`, run the oil case (default **MW-002**; accept a `--case` arg) through
  `wired.diagnose()` (reuse `run_case.load_case`), then `provider.shutdown()` to flush.
  Print the returned verdict + the emitted trace/span id for cross-reference.
- Confirm in Jaeger (REST API `…/api/traces?service=4dlab-wired-harness`) that **one
  trace** for the run contains the canonical span tree — at minimum the six
  `EXPECTED_SPANS` (OBD present iff the case has an `obd` block) with correct
  parent/child nesting under `wired.diagnose`.
- **Verdict invariance:** run `pytest apps/wired/tests/test_tracing.py -q` from the
  neutral cwd and confirm `test_verdict_identical_traced_vs_untraced` and
  `test_spans_emitted_when_enabled` pass; additionally confirm the traced
  `diagnose()` verdict JSON byte-matches the untraced one for MW-002 (mirror the
  test's assertion in the run script's output).
- Record the run (case, verdict, trace id, span names + nesting) in the progress note.

**OUT:** any edit to `wired/`, a lab, or COMLab (instrumentation is T-WIRE-3, done —
if a span is missing, that is a `blocked` hand-back, **not** a fix here); adding new
spans/attributes; multi-case runs (single case this pack); committing span JSON or
the Jaeger binary; `graphify`; `Vault/`; secrets.

## Steps
1. Start Jaeger (T-WTEST-3 README); dot-source `setup_env_wired.sh`; confirm banner
   ONLINE and `WIRED_OTEL=1`.
2. Write `apps/wired/trace/run_traced_case.py`; run it for MW-002.
3. Query the REST API; confirm the canonical span tree + nesting for that trace id.
4. Run `pytest apps/wired/tests/test_tracing.py -q`; confirm both tracing tests pass;
   confirm traced vs untraced verdict bytes match for MW-002.
5. Fill the gate blocks in `test_tasks/progress_notes/T-WTEST-4.md`; STOP.

## Success criteria
- `run_traced_case.py` runs MW-002 to a verdict and flushes spans without error.
- Jaeger holds one trace for the run with the six `EXPECTED_SPANS` (OBD per case)
  nested under `wired.diagnose`; the trace id is recorded.
- `test_tracing.py` (both tests) passes; traced verdict JSON == untraced verdict JSON
  for MW-002 (byte-identical).
- `git status` shows only new files under `apps/wired/trace/` +
  `apps/wired/test_tasks/`; no `wired/`/lab/COMLab diffs; no span JSON / binary
  staged; no secrets.

## VERIFICATION GATE — T-WTEST-4
Complete in `test_tasks/progress_notes/T-WTEST-4.md`: `run_traced_case.py` output
(verdict + trace id); the REST API JSON span list + nesting; `pytest test_tracing.py`
tail; the traced==untraced byte-match evidence.

## CODE REVIEW — T-WTEST-4
Complete in `test_tasks/progress_notes/T-WTEST-4.md`: no `ARCHIVE/` import (provider
bootstrap is a clone); no instrumentation/source edits; span JSON + binary not staged;
`graphify` not run; verdict-invariance reused, not re-implemented divergently.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/trace/run_traced_case.py \
  apps/wired/test_tasks/progress_notes/T-WTEST-4.md \
  apps/wired/test_tasks/TEST_PROGRESS.md
git commit -m "T-WTEST-4: run wired oil case under OTel; canonical span tree lands in Jaeger"
```
