# T-LRC-4 — wiredV2: PowerShell env script → bash

**Pack:** Linux Residue Cleanup · **Area:** apps/wiredV2 · **Blocked by:** — · **Status:** pending
**Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`.
**Independent of wiredV2 feature work** — this only converts the local OTel/Jaeger env helper; safe to run anytime.

### Goal ###
Replace the Windows-only `apps/wiredV2/wiredv2/_jaeger/setup_env_wired.ps1` with a source-able
`setup_env_wired.sh` that exports the same OpenTelemetry profile on Linux (service name, OTLP
endpoint/protocol, traces exporter, resource attributes, `USE_V2_REGISTRY=1`) with `PYTHONPATH` and the
wired Python pointing at this host (`/agent_workspace/apps/wiredV2`, `/agent_workspace/.venv-wired/bin/python`),
and provides the `run-tests` / `run-case` / `open-jaeger` helpers as shell functions. Update the one
docstring that names the old script, and archive the `.ps1`. Done when `setup_env_wired.sh` sources clean,
sets the env vars, carries no Windows residue, and the `.ps1` is gone from the active path.

### Success criteria ###
- `bash -n apps/wiredV2/wiredv2/_jaeger/setup_env_wired.sh` exits 0.
- Sourcing it sets `OTEL_SERVICE_NAME=wiredv2-oil-case` and a `PYTHONPATH` containing `/agent_workspace/apps/wiredV2` (asserted in Verification).
- `grep -niE 'powershell|\.ps1|C:\\' setup_env_wired.sh` returns zero.
- `apps/wiredV2/wiredv2/_jaeger/setup_env_wired.ps1` no longer exists in the tree (moved to `ARCHIVE/`).
- `_sanity_emit_span.py` no longer references `setup_env_wired.ps1`.

### Context ###
`WINDOWS_RESIDUE_FOLLOWUPS.md` §"Needs a REWRITE" flags this script. The current `.ps1` (read it for the
exact values) sets: `OTEL_SERVICE_NAME=wiredv2-oil-case`, `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`,
`OTEL_EXPORTER_OTLP_PROTOCOL=grpc`, `OTEL_TRACES_EXPORTER=otlp`,
`OTEL_RESOURCE_ATTRIBUTES=deployment.environment=local,service.namespace=4dlab`,
`CLAUDE_CODE_ENABLE_TELEMETRY=1`, `USE_V2_REGISTRY=1`, and `PYTHONPATH=C:\Workspace\apps\wiredV2` (→ Linux
`/agent_workspace/apps/wiredV2`). Its helpers run pytest/`run_case.py` via the wired Python
(`C:\Workspace\.venv-wired\Scripts\python.exe` → `/agent_workspace/.venv-wired/bin/python`). The Jaeger
health banner used `Invoke-WebRequest` → use `curl -s -m 3 http://localhost:16686/` (non-fatal if offline).
The docstring at `apps/wiredV2/wiredv2/_jaeger/_sanity_emit_span.py:2` says "Run AFTER sourcing
setup_env_wired.ps1" — repoint to `.sh`.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Dev-env script conversion only.

### Deliverables ###
1. `apps/wiredV2/wiredv2/_jaeger/setup_env_wired.sh` — CREATE; bash equivalent of the OTel profile + `run-tests`/`run-case`/`open-jaeger` shell functions, Linux paths, `curl` health check.
2. `apps/wiredV2/wiredv2/_jaeger/_sanity_emit_span.py` — MODIFY; docstring `setup_env_wired.ps1` → `setup_env_wired.sh`.
3. `apps/wiredV2/wiredv2/_jaeger/setup_env_wired.ps1` — ARCHIVE (move to `ARCHIVE/2026-06-27_linux_residue/apps/wiredV2/wiredv2/_jaeger/`), do not `rm`.

### Files to touch ###
- `apps/wiredV2/wiredv2/_jaeger/setup_env_wired.sh` (CREATE)
- `apps/wiredV2/wiredv2/_jaeger/_sanity_emit_span.py` (MODIFY)
- `apps/wiredV2/wiredv2/_jaeger/setup_env_wired.ps1` (MOVE → ARCHIVE)

### Out of scope ###
No changes to the OTel/tracer runtime code, the Jaeger config, or the tests themselves — only the env
helper + the one docstring. Do not "improve" `run_case.py` or the tracer. The sibling
`apps/4DLabWired/_jaeger/setup_env_wired.ps1` (a separate app) is **not** in scope. Surgical: each changed
line traces to a Deliverable. GRAPH GUARDRAIL: no graphify.

### Verification ###
```bash
cd /agent_workspace
F=apps/wiredV2/wiredv2/_jaeger/setup_env_wired.sh
bash -n "$F"
( . "$F" >/dev/null 2>&1; [ "$OTEL_SERVICE_NAME" = "wiredv2-oil-case" ] && echo "OTEL ok" || exit 1
  case ":$PYTHONPATH:" in *":/agent_workspace/apps/wiredV2:"*) echo "PYTHONPATH ok";; *) echo "PYTHONPATH BAD"; exit 1;; esac )
! grep -niE 'powershell|\.ps1|C:\\' "$F"
! test -f apps/wiredV2/wiredv2/_jaeger/setup_env_wired.ps1
! grep -nF 'setup_env_wired.ps1' apps/wiredV2/wiredv2/_jaeger/_sanity_emit_span.py
```
All steps must pass.

### Progress hook ###
`LINUX_RESIDUE_CLEANUP_PROGRESS.md` T-LRC-4: Status=done, Verification="setup_env_wired.sh sources clean; .ps1 archived; docstring repointed".
