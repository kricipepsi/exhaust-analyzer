# T-WTEST-3 — Native-Linux Jaeger backend + `.sh` env profile + sanity span

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `deferred` (→ `pending` when T-WTEST-1 is `done`) · **Blocked by:** T-WTEST-1
**Mode:** STRICT — adds local trace tooling under `apps/wired/trace/`; **no wired/lab/COMLab source edits**. · **Scope owner:** wired-test / tracing.
**Load skills:** wired-python, wired-verification-loop, wired-code-review, wired-jaeger-tracing (read as reference; **clone** scaffold, do not import `ARCHIVE/`).

## Objective
Stand up a span backend on **this Linux host with no docker** (owner decision
2026-06-30) and a reusable env profile, so T-WTEST-4 can run the wired pipeline
with spans landing in Jaeger. Two deliverables: a **native linux/amd64 Jaeger v2
binary** brought online, and a `.sh` env profile that is a faithful port of the
Windows `setup_env_wired.ps1`. Prove the path with a single sanity span visible in
the Jaeger UI/REST API.

## Signal/noise
Adds no domain field or fault. The **named consumer** is **T-WTEST-4**, which
sources this profile and needs a live collector to receive spans; and the architect
verifying the trace path is real. Without a reachable collector + correct env, the
live `wired/tracing.py` spans are emitted and silently dropped.

## Pinned facts (verified at authoring)
- `OTLPSpanExporter` (gRPC) imports cleanly from `.venv-wired`:
  `from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter` → exit 0.
- **The Windows scaffold does not apply.** `ARCHIVE/wired/_jaeger/setup_env_wired.ps1`
  points at `C:\Users\muto\jaeger\...jaeger.exe`; `apps/wired/_jaeger/` and
  `apps/wired/harness/` are **symlinks into `ARCHIVE/`** — reference/clone, never
  import (AGENTS: no `ARCHIVE/` imports).
- Jaeger v2 single-binary ports (from the wired-jaeger skill): **OTLP gRPC 4317**,
  **OTLP HTTP 4318**, **UI + REST API 16686**.
- Env the `.ps1` sets (port the **non-Windows** ones): `OTEL_SERVICE_NAME=4dlab-wired-harness`,
  `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`, `OTEL_EXPORTER_OTLP_PROTOCOL=grpc`,
  `OTEL_TRACES_EXPORTER=otlp`, `OTEL_RESOURCE_ATTRIBUTES=deployment.environment=local,service.namespace=4dlab`.
- **Critical gate nuance:** the live `wired/tracing.py` gates spans on **`WIRED_OTEL`**
  (truthy) and uses the **globally-set** provider — it does **not** itself build an
  OTLP exporter. So the profile must **also** export `WIRED_OTEL=1`, and T-WTEST-4
  must register an OTLP `TracerProvider` (cloned from the `_sanity_emit_span.py`
  pattern). `OTEL_TRACES_EXPORTER=otlp` alone only drives the *archived* tracer.

## Scope
**IN:**
- Fetch the **current Jaeger v2 linux/amd64 release** binary (jaegertracing/jaeger
  GitHub releases) into a host-local location **outside the repo** (e.g. `~/jaeger/`).
  **Do not commit the binary** — the explicit-path commit below already excludes it,
  so no `.gitignore` edit is needed; if you place it inside the repo, prefer `~/`
  instead rather than editing shared `.gitignore`. Pin the exact version + sha256 in
  the progress note.
- Start it (default OTLP receiver config) and confirm: UI returns 200 at
  `http://localhost:16686/`, OTLP gRPC listening on 4317.
- Create `apps/wired/trace/setup_env_wired.sh` — a dot-sourceable profile exporting
  the env above **plus `WIRED_OTEL=1`** and a Linux `PYTHONPATH` (workspace root +
  the seven lab paths, mirroring `apps/wired/pyproject.toml`'s `pythonpath`). Print
  a status banner with a Jaeger-online/offline health check (port the `.ps1`
  banner). Confirm whether the live wired path still reads `USE_V2_REGISTRY`; add it
  **only** if a live consumer reads it — otherwise drop it (signal/noise).
- Clone (do **not** import) the `_sanity_emit_span.py` pattern into
  `apps/wired/trace/sanity_emit_span.py`: standalone `TracerProvider` + OTLP
  BatchSpanProcessor + `provider.shutdown()` flush, service `4dlab-wired-harness`.
  Run it and confirm the span is queryable at
  `http://localhost:16686/api/traces?service=4dlab-wired-harness` (or visible in UI).
- Record start/stop instructions for the binary in
  `apps/wired/trace/README.md` (how T-WTEST-4 brings it up).

**OUT:** docker / `jaeger-all-in-one`; any edit to `wired/`, a lab, or COMLab;
importing `ARCHIVE/_jaeger`; instrumenting code (already done in T-WIRE-3);
committing the Jaeger binary, any span JSON, or any secret; `graphify`; `Vault/`.

## Steps
1. Source nothing yet. Download + checksum the Jaeger v2 linux/amd64 binary to a
   git-ignored path; pin version + sha256 in the note.
2. Start Jaeger; health-check UI (16686) + gRPC (4317).
3. Write `apps/wired/trace/setup_env_wired.sh`; dot-source it; confirm the banner
   shows Jaeger ONLINE and the env vars (incl. `WIRED_OTEL=1`) are set.
4. Write + run `apps/wired/trace/sanity_emit_span.py`; confirm 1 span lands
   (REST API query returns the trace).
5. Write `apps/wired/trace/README.md` (bring-up/teardown).
6. Fill the gate blocks in `test_tasks/progress_notes/T-WTEST-3.md`; STOP.

## Success criteria
- Jaeger v2 (pinned version) runs natively (no docker); UI 200 + gRPC 4317 open.
- `setup_env_wired.sh` dot-sources cleanly, exports all listed vars **including
  `WIRED_OTEL=1`**, and its health check correctly reports ONLINE.
- The sanity span is retrievable via the REST API for service `4dlab-wired-harness`.
- Only the files in the commit block below are staged (explicit paths); the Jaeger
  binary + any span JSON remain **untracked** (not staged, not committed); no
  `wired/`/lab/COMLab diffs; no secrets.

## VERIFICATION GATE — T-WTEST-3
Complete in `test_tasks/progress_notes/T-WTEST-3.md`: Jaeger version + sha256 +
launch command; UI/gRPC health-check output; `setup_env_wired.sh` banner; the REST
API JSON proving the sanity span landed.

## CODE REVIEW — T-WTEST-3
Complete in `test_tasks/progress_notes/T-WTEST-3.md`: no `ARCHIVE/` import (sanity
emitter is a clone); no `wired/`/lab/COMLab edits; binary + JSON not staged; profile
drops Windows-only lines and any env with no live consumer; `graphify` not run.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/trace/setup_env_wired.sh \
  apps/wired/trace/sanity_emit_span.py \
  apps/wired/trace/README.md \
  apps/wired/test_tasks/progress_notes/T-WTEST-3.md \
  apps/wired/test_tasks/TEST_PROGRESS.md
git commit -m "T-WTEST-3: native-Linux Jaeger backend + .sh env profile + sanity span"
```
