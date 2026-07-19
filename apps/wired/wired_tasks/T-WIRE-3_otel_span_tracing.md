# T-WIRE-3 — env-gated OpenTelemetry span tracing

### Goal ###
Instrument the wired pipeline with env-gated OpenTelemetry spans: a root span on
`diagnose()`/`run_case`, a child span per lab call (DNA/GAS/OBD/DTC), and a span
around COMLab's `process()`. Tracing must be **off by default** and the verdict
must be **byte-identical whether tracing is on or off**. Done when spans emit
only when the trace env var is set, and a verdict-equality test passes with the
var unset vs set.

### Success criteria ###
- `apps/wired/tests/test_tracing.py::test_verdict_identical_traced_vs_untraced`
  passes: `diagnose()` on the same input yields an equal verdict object with the
  trace env var unset and set.
- `apps/wired/tests/test_tracing.py::test_spans_emitted_when_enabled` passes: with
  the env var set and an in-memory span exporter, the expected span names appear;
  with it unset, none do.

### Context ###
**Blocked by T-WIRE-1.** Adapt the prior tracing approach from
`ARCHIVE/wiredV2/_wiredv2_skills/wiredv2-jaeger-tracing/SKILL.md` and
`ARCHIVE/wiredV2/wiredv2/_jaeger/` (READ-NARROW — reference, never import from
`ARCHIVE/`). The non-obvious invariant (this is why tracing is inlined here, not
a separate skill): **tracing is observability only — it must never change the
verdict or control flow.** Gate every span behind the env var (e.g.
`WIRED_OTEL=1`); when unset, the tracer is a no-op and no OpenTelemetry import
side-effects touch the result. Verify `opentelemetry-sdk` is installed in
`.venv-wired` before importing it; if absent, the env-gated path stays a no-op
and the test for "enabled" is skipped with a recorded reason (do not add a hard
dependency that breaks the default run).

Load skills: wired-composition-contract.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Spans are telemetry, not schema; they do not enter
any COMLab payload.

### Deliverables ###
1. `apps/wired/wired/tracing.py` — env-gated tracer factory; no-op when unset.
2. `apps/wired/wired/composition.py` — wrap `diagnose()` + the 4 lab calls +
   `process()` in spans via the factory (MODIFY).
3. `apps/wired/tests/test_tracing.py` — the two success-criteria tests.

### Files to touch ###
- `apps/wired/wired/tracing.py` (CREATE)
- `apps/wired/wired/composition.py` (MODIFY)
- `apps/wired/tests/test_tracing.py` (CREATE)

### Out of scope ###
No Jaeger backend/collector deployment, no dashboards. No change to mapping logic
or the verdict. No FATAL gate. Do not edit any lab. Do not rebuild a graph.
Surgical: the only composition.py change is wrapping calls in spans — no mapper
behaviour changes.

### Verification ###
```bash
cd /agent_workspace
PY=.venv-wired/bin/python
$PY -m py_compile apps/wired/wired/tracing.py apps/wired/wired/composition.py
$PY -m ruff check apps/wired/wired/tracing.py
( cd apps/wired && /agent_workspace/.venv-wired/bin/pyright . )
# verdict identical traced vs untraced + spans gate on the env var
$PY -m pytest -x -q apps/wired/tests/test_tracing.py
```
All steps must pass.

### Progress hook ###
PROGRESS.md `T-WIRE-3`: Status=done, Files changed={COUNT}, Verification="env-gated spans; verdict byte-identical OTEL unset vs set"
