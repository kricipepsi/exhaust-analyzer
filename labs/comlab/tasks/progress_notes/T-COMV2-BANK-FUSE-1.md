# T-COMV2-BANK-FUSE-1 progress note

Status: done
Date: 2026-06-21

## Plan

Mirror OBDLab's exact `per_bank_trim_delta: float | None = None` contract into
`OBDLiveDataPayload`, then add a default-off bank-asymmetry evidence path in
`FaultAtlasRouter.execute_triage_loop()` Phase 5. Keep flag-off, absent-field,
and symmetric inputs byte-identical; add focused router tests; prove the live
read with the task's two grep gates. Touch only the schema, router, tests,
progress note, and ledger named by the task.

## Blocker

The task requires
`_bank_asymmetry_verdict(per_bank_trim_delta: float | None, model_year: int)`
and a `model_year < 2001` confidence-cap path. The live
`OrchestratorInboundRequest` and the aggregator's sanitized router payload do
not carry `model_year`; they expose only `SessionMetadata.resolved_horizon`.

The cited source, `wiki/04_horizon_eras.md §line44`, states that standard trim
thresholds apply in `HORIZON_ADAPTIVE`; it does not define a pre-CAN
confidence cap or authorize replacing model year with horizon.

Implementation needs an architect choice between:

1. adding `model_year` to the inbound/session metadata contract and its callers;
2. explicitly changing the helper contract to use `resolved_horizon`;
3. naming another existing, reachable source of model year.

No production code, tests, or ledger status were changed.

## Architect resolution — 2026-06-21 (Cowork)

**Decision: coder option 2 — use `resolved_horizon`, do not add `model_year`.** The router
already carries `request.metadata.resolved_horizon` (`fault_atlas_router.py:588`, `:1239`);
widening the inbound contract with `model_year` is unnecessary and violates "consume the
verdict, mirror minimally."

- Helper signature is now `_bank_asymmetry_verdict(per_bank_trim_delta, resolved_horizon: str)`.
- The pre-2001 confidence caveat maps to **`resolved_horizon == "HORIZON_LEGACY"`** — wiki/04
  defines LEGACY as Euro 1–2, era mask `model_year_range: 1980–2001`, where "fuel trims
  unreliable/absent" (`04_horizon_eras.md §CONCEPT_LEGACY` + era-mask line 63). That is the
  correct, reachable, wiki-grounded source — the prior `§line44` cite (ADAPTIVE thresholds)
  was wrong and has been removed.
- Enum: `comlab/schemas/vocabulary.py::Horizon.LEGACY` (`:85`).

The task spec `tasks/T-COMV2-BANK-FUSE-1_per_bank_asymmetry_verdict.md` has been patched
(Deliverable 2 + the `test_bank_fuse_legacy_caps_confidence` test). **Unblocked — re-pick and
proceed.** Ledger row stays `pending`.

## Changed Files

- `comlab/schemas/ingestion.py` — exact optional
  `per_bank_trim_delta: float | None = None` OBD mirror.
- `comlab/core/fault_atlas_router.py` — pure bank-asymmetry classifier,
  default-off constructor flag, LEGACY confidence cap, Phase-5 evidence rerank,
  and `bank_asymmetry_applied` telemetry.
- `tests/unit/test_fault_atlas_router.py` — three focused inertness, rank/event,
  and LEGACY-cap tests.
- `tasks/PROGRESS.md` — task row closed.
- `tasks/progress_notes/T-COMV2-BANK-FUSE-1.md` — gate and review evidence.

VERIFICATION GATE — T-COMV2-BANK-FUSE-1
=======================================
Phase 1 Syntax/import:  PASS (`py_compile` on both production files and test file)
Phase 2 Type check:     PASS (Pyright: 0 errors, 0 warnings)
Phase 3 Lint:           PASS (`ruff check .`: all checks passed)
Phase 4 pytest:         PASS (434 passed, 4 skipped; bank-fuse target 3 passed)
Phase 5 Wiki/orphan:    PASS (±5 %, 0.80 evidence, and 0.50 LEGACY cap cited;
                              `per_bank_trim_delta` read at router lines 821–848;
                              `enable_bank_fuse` branch at lines 300/318/820)
Phase 6 Diff review:    PASS (schema, router, focused tests, note, and ledger row only;
                              unrelated pre-existing worktree changes preserved)

comlab-python checklist items applied:
  type hints; private-symbol docstrings; no mutable defaults; no bare except;
  wiki-cited constants; no string-format/path/file changes; `is None`; sorted imports.

Status: DONE — PROGRESS.md flipped to done

CODE REVIEW — T-COMV2-BANK-FUSE-1
=================================
1. Design rules:        PASS (verdict mirror only; no cross-lab import, raw-sensor
                              derivation, graph work, override, or default-on behavior)
2. Scope compliance:    PASS (only task-declared implementation/test/note/ledger areas)
3. Contracts:           PASS (additive default-None Pydantic field; trailing default-off
                              router argument; existing callers remain compatible)
4. Docstrings:          PASS (private result/helper and test support symbols documented)
5. Wiki provenance:     PASS (threshold, family set, evidence score, and LEGACY cap sourced)
6. Immediate Checklist: PASS (0 warnings)
7. Test coverage:       PASS (flag-off/None/symmetric inertness, rank promotion + span
                              event, and LEGACY vs ADAPTIVE/MODERN cap)
8. Structural craft:    PASS (one pure classifier plus one contained Phase-5 consumer;
                              no duplicated production policy or shallow module)

Verdict: CLEAN
Blockers: none
