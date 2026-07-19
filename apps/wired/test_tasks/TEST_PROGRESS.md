# wired-test — Progress Ledger

**Pack goal:** test the **wired** 4DLab end-to-end through two lenses, anchored on
a green full-suite baseline: **(1)** a `pyscn` static-quality audit of the wiring
code, then **(2)** a native-Linux **Jaeger / OpenTelemetry** runtime trace pass
over the single oil-burning case. No new diagnostic logic, no UI, no multi-case
accuracy harness — this pack **verifies** the wiring the `T-WIRE-*` pack built; it
does not extend it.

**Tasks dir:** `apps/wired/test_tasks/`
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW)
**Reads on boot:** `apps/wired/test_tasks/WIRED_TEST_START_HERE.md`
**Last updated:** 2026-06-30 (architect, Cowork — pack authored)

This is the only file `WIRED_TEST_START_HERE.md` reads to find the next task. Keep
it under ~120 lines. Bulk notes (verification + code-review blocks) go in
`test_tasks/progress_notes/<task-id>.md`, not here.

---

## Pre-pack gate (must hold before T-WTEST-1)

| Item | State | Evidence |
|---|---|---|
| `T-WIRE-1..4` wiring done | **done** | `apps/wired/WIRED_PROGRESS.md` (T-WIRE-4 2026-06-30) |
| `pyscn` evaluated read-only | **done** | `planning/code_audit/reports/PYSCN_EVAL_2026-06-29.md` (T-PYSCN-1) |
| OTel SDK + OTLP exporter in `.venv-wired` | **present** | `python -c "from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter"` exits 0 |

## Task log

| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| T-WTEST-1 | `T-WTEST-1_full_suite_green_baseline.md` | done | — | 2026-06-30 | (owner commit pending) | GREEN: 1991 passed, 16 skipped, 0 failed/errors; `apps/wired` OTel test ran (`1 passed`) | Run-only baseline report: `reports/WTEST1_BASELINE_2026-06-30.md`. Unblocks T-WTEST-2. |
| T-WTEST-2 | `T-WTEST-2_pyscn_audit_wired.md` | done | T-WTEST-1 (**done**) | 2026-06-30 | (owner commit pending) | GREEN: `pyscn` check exit 0; analyze exit 0; 9 files parsed, 0 parse failures; health 71/C | Report: `reports/WTEST2_PYSCN_WIRED_2026-06-30.md`; clean vs pinned thresholds; advisory production clone/module-complexity debt recorded. |
| T-WTEST-3 | `T-WTEST-3_native_jaeger_env_profile.md` | done | T-WTEST-1 (**done**) | 2026-06-30 | (this commit) | CLEAN: Jaeger v2.19.0 native binary outside repo; UI 200; OTLP gRPC 4317 open; profile ONLINE; sanity span retrievable via REST | Added `apps/wired/trace/` profile, sanity emitter, README. Unblocks T-WTEST-4. |
| T-WTEST-4 | `T-WTEST-4_otel_run_spans_to_jaeger.md` | done | T-WTEST-3 (**done**) | 2026-06-30 | (owner commit pending) | GREEN: MW-002 traced run emitted Jaeger trace `e72961acd660e386ec9537bacc0fc4e9`; verdict bytes matched; `test_tracing.py` passed (`2 passed`) | Added `apps/wired/trace/run_traced_case.py`; REST span proof recorded in `progress_notes/T-WTEST-4.md`. Unblocks T-WTEST-5. |
| T-WTEST-5 | `T-WTEST-5_trace_extract_and_report.md` | done | T-WTEST-4 (**done**) | 2026-06-30 | (this commit) | CLEAN: extracted Jaeger trace `934b526f078a04b65521aeee8669b581`; report written; `test_tracing.py` passed (`2 passed`) | Report: `reports/WTEST5_TRACE_2026-06-30.md`; raw JSON in local `apps/wired/trace/runs/WTEST5_20260630/` excluded from commit. |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred`
**Blocked by:** comma-separated task IDs that must reach `done` first, or `—`.

**Runnability convention.** `pending` = runnable now (spec authored, every
`Blocked by` is `done`). A forward-registered/unauthored placeholder stays
`deferred`, never `pending`. The guard takes the **first `pending` row
top-to-bottom**; `deferred`/`blocked` rows are skipped. Promote a row
`deferred -> pending` only when every `Blocked by` is `done`.

---

## Unplanned follow-ups

Bugs/refactors discovered mid-task. Logged here, not fixed in the session that
found them.

| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| — | — | — | — |

---

## Carried-in known issues

Pre-known at authoring; the named task handles each.

| Ref | Item | Handled by |
|---|---|---|
| `setup_env_wired.ps1` is Windows PowerShell; host is Linux Mint | the `.ps1` profile + Windows Jaeger binary path do **not** apply; port to a `.sh` profile + native linux/amd64 Jaeger v2 binary | T-WTEST-3 |
| two tracing gates | live `wired/tracing.py` gates spans on `WIRED_OTEL` and uses the **globally-set** provider; it does **not** itself construct an OTLP exporter. Spans reach Jaeger only when **both** a provider with the OTLP exporter is registered **and** `WIRED_OTEL=1` | T-WTEST-4 |
| no ARCHIVE imports | `apps/wired/_jaeger/` and `apps/wired/harness/` are **symlinks into `ARCHIVE/`** — reference/clone the scaffold, **never import** it (AGENTS rule: no `ARCHIVE/` imports). New live trace tooling lands under `apps/wired/trace/` | T-WTEST-3/4/5 |
| docker absent | the Jaeger backend is a **native binary**, not `jaeger-all-in-one` in docker (owner decision 2026-06-30) | T-WTEST-3 |

---

## Deferred (out of this pack — named for the next pack)

| ID | Item | Why deferred |
|---|---|---|
| T-WTEST-HARNESS-* | multi-case CSV accuracy harness + trace fixture over many cases | single case proves the trace path first; the accuracy harness is its own pack |
| Stage-4 complexity debt | `fault_atlas_router` / VINLab clones flagged by pyscn | reworked at ROADMAP Stage 4, not against the current spine — see `planning/code_audit/STAGE4_COMPLEXITY_INPUTS.md` |

---

## Architect-level out-of-band patches

| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-30 | `apps/wired/test_tasks/**` | Authored the wired-test pack (ledger + START_HERE + 5 specs) and a SUGGESTED block in `.agent/assignments.md`. | Verify the composed wiring under pyscn + native-Linux Jaeger before any UI/accuracy pack. |
