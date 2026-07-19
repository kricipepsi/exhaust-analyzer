# wired — Progress Ledger

**Pack goal:** wire the CURRENT labs into COMLab's full pipeline and run **one
single case end-to-end — the oil-burning case** — returning its verdict. No UI,
no multi-case CSV harness in this pack; OpenTelemetry tracing is in scope.
**Tasks dir:** `apps/wired/wired_tasks/`
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW)
**Pre-prep gate:** `apps/wired/WIRING_PREP.md` — `T-WIRE-1` is blocked until
gaslab `T-GV2-2` (COMLab chem-mirror 28/32->34) is `done`.
**Last updated:** 2026-06-28 (architect, Cowork — pack authored)

This is the only file `WIRED_START_HERE.md` reads to find the next task. Keep it
under ~120 lines. Bulk notes (verification + code-review blocks) go in
`wired_tasks/progress_notes/<task-id>.md`, not here.

---

## Pre-prep tasks (gate — must clear before T-WIRE-1)
| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| T-GV2-2 | `labs/gaslab/tasks/T-GV2-2_chemsig_consumer_mirror_reconcile.md` | **done** | — | 2026-06-28 | (owner commit pending) | COMLab mirror 34-value; CT-001/003 re-pointed to CAM_TIMING_RETARDED_MAP; 510 passed | **DONE 2026-06-28 (Cowork, owner-authorized).** Unblocks T-WIRE-1. MAF-variant coverage → `T-COM-CAMTIMING-MAF-1` (comlab ledger). |
| T-PREP-WIRE-1 | `wiring_prep_tasks/T-PREP-WIRE-1_rings_pcv_chemistry_triage.md` | **done** | — | 2026-06-28 | (owner commit pending) | Ruling authored (`RINGS_PCV_TRIAGE_RULING.md`); both ACCEPT-KNOWN-BLOCKED + cross-lab reconciles forward-registered | DONE 2026-06-28 (Cowork). Rings/PCV expectations pinned for T-WIRE-2. |

## Task log
| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| T-WIRE-1 | `T-WIRE-1_compose_labs_comlab.md` | done | T-GV2-2 (**done**) | 2026-06-29 | 52210e1 | diagnose() returns `OrchestratorFinalUIOutput`; high-idle forwarded; no deferred path; guard=73; pytest 2 passed | Files changed=7; composition.py: DNA+GAS(+high-idle)+OBD+DTC -> COMLab; `diagnose()` returns `OrchestratorFinalUIOutput`; registry_guard expects 73 rules. |
| T-WIRE-2 | `T-WIRE-2_oil_case_runner.md` | done | T-WIRE-1 (**done**) | 2026-06-29 | (owner commit pending) | oil cases route per T-PREP-WIRE-1 ruling; run_case --case MW-002 exits 0; pytest 4 passed | Files changed=9; runner + five fixtures + tests + progress note + ledger. MW-002/MW-003/MW-009 route; MW-001→CF-001 and MW-008→SF-001 asserted as known-blocked per ruling; PCV emitted `INCOMPLETE_OXIDATION`. |
| T-WIRE-3 | `T-WIRE-3_otel_span_tracing.md` | done | T-WIRE-1 (**done**) | 2026-06-29 | e378781 | env-gated spans; verdict byte-identical OTEL unset vs set; pytest 2 passed | Files changed=5; `tracing.py` gates OTel behind `WIRED_OTEL`; `composition.py` wraps diagnose + DNA/GAS/OBD/DTC + COMLab spans; no payload or verdict mapping changes. |
| T-WIRE-4 | `T-WIRE-4_fatal_gate_passthrough.md` | done | T-WIRE-2 (**done**) | 2026-06-30 | (owner commit pending) | enable_fatal_gates threaded; default-off unchanged; INVALID -> FATAL_INCOMPLETE; pytest 3 passed | Files changed=6; `diagnose(..., enable_fatal_gates=False)` default-off; `run_case --fatal-gates` prints `degradation=FATAL_INCOMPLETE`; INVALID fixture triggers ERR-ABORT-001. |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred`
**Blocked by:** comma-separated task IDs that must reach `done` first, or `—`.
**Runnability convention.** `pending` = runnable now (spec authored, every
`Blocked by` is `done`). A forward-registered/unauthored placeholder stays
`deferred`, never `pending`. The guard takes the **first `pending` row
top-to-bottom**; `deferred`/`blocked` rows are skipped. T-WIRE-1 through T-WIRE-4
are `done`; this pack has no remaining pending runnable task.

> Promote a row to `pending` only when every `Blocked by` is `done`.

---

## Unplanned follow-ups
Bugs/refactors discovered mid-task. Logged here, not fixed in the session that
found them.

| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| — | — | — | — |

---

## Carried-in known issues (from the prior wiring / registry ledger)
Pre-known at authoring; the named task handles each.
| Ref | Item | Handled by |
|---|---|---|
| registry `wired-registry-guard-rule-count-drift` | `registry_guard.py` must expect 73 rules (not 68) or harness raises `RegistryActivationError` | T-WIRE-1 |
| `U-WV2-1` / `U-WV2-2` | rings MW-001 / PCV MW-008 GASLab<->registry chemistry contradictions | T-PREP-WIRE-1 (ruling) -> T-WIRE-2 (assert) |
| `U-WV2-3` | `pyright apps/wired/` from root may not discover `pyproject.toml`; use `cd apps/wired; pyright .` | T-WIRE-1 verification |

---

## Deferred (out of this pack — named for the next pack)
| ID | Item | Why deferred |
|---|---|---|
| T-WIRE-UI-* | Streamlit/React UI over `diagnose()` | UI not reworked yet; render `OrchestratorFinalUIOutput` once it is. |
| T-WIRE-HARNESS-* | Multi-case CSV accuracy harness + baseline | Single-case proves the wiring first; harness is a separate pack with its own `wired-harness-accuracy` skill. |

---

## Architect-level out-of-band patches
| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-28 | `apps/wired/**` + root `CLAUDE.md` | Authored the wired pack (5-piece infra + pre-prep gate) and inserted the `## Session bootstrap` row for wired into root `CLAUDE.md`. | Stand up `apps/wired` wiring from the verified lab surfaces. |
