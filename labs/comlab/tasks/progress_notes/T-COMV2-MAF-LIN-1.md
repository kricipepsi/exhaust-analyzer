# T-COMV2-MAF-LIN-1 progress note

Status: done
Date: 2026-06-21

## Plan

Mirror OBDLab's exact `w_theo: float | None = None` and `sensor_error_delta: float | None = None` contract into `OBDLiveDataPayload`, then add a default-off MAF linearity ladder evidence path in `FaultAtlasRouter.execute_triage_loop()` Phase 5. Keep flag-off, absent-field, and within-spec inputs byte-identical; add focused router tests; prove the live read with the task's two grep gates. Touch only the schema, router, tests, progress note, and ledger named by the task.

## Changed Files

- `comlab/schemas/ingestion.py` — additive optional `w_theo` and `sensor_error_delta` schema fields.
- `comlab/core/fault_atlas_router.py` — pure MAF linearity band classifier `_maf_linearity_band`, default-off constructor flag, Phase-5 evidence rerank (boosting `ERR-LC-002` or `P0101` to at least 0.80, and demoting `P0102` to 0.60), and `maf_linearity_applied` span tracing.
- `tests/unit/test_fault_atlas_router.py` — `_RecordingSpan` updated to store attributes; three focused unit tests covering inertness/flag-off, calibration drift (`ERR-LC-002` promotion), and component fault (`P0101` promotion).
- `tasks/PROGRESS.md` — task row closed.
- `tasks/progress_notes/T-COMV2-MAF-LIN-1.md` — gate and review evidence.

VERIFICATION GATE — T-COMV2-MAF-LIN-1
=======================================
Phase 1 Syntax/import:  PASS (`py_compile` on both production files and test file)
Phase 2 Type check:     PASS (Pyright: 0 errors, 0 warnings in activated venv-comlab environment)
Phase 3 Lint:           PASS (`ruff check .`: all checks passed)
Phase 4 pytest:         PASS (445 passed, 4 skipped; maf_lin target 3 passed)
Phase 5 Wiki/orphan:    PASS (5–12 % calibration drift, >12 % component fault, and P0102 open-circuit cited;
                              `sensor_error_delta` read at router line 966;
                              `enable_maf_lin` branch at line 965)
Phase 6 Diff review:    PASS (schema, router, focused tests, note, and ledger row only;
                              unrelated pre-existing worktree changes preserved)

comlab-python checklist items applied:
  type hints; private-symbol docstrings; no mutable defaults; no bare except;
  wiki-cited constants; no string-format/path/file changes; `is None`; sorted imports.

Status: DONE — PROGRESS.md flipped to done

CODE REVIEW — T-COMV2-MAF-LIN-1
=================================
1. Design rules:        PASS (verdict mirror only; no cross-lab import, raw-sensor
                              derivation, graph work, override, or default-on behavior)
2. Scope compliance:    PASS (only task-declared implementation/test/note/ledger areas)
3. Contracts:           PASS (additive default-None Pydantic fields; trailing default-off
                              router argument; existing callers remain compatible)
4. Docstrings:          PASS (private result/helper and test support symbols documented)
5. Wiki provenance:     PASS (threshold, family set, evidence score, and proposals register sourced)
6. Immediate Checklist: PASS (0 warnings)
7. Test coverage:       PASS (flag-off/None/within-spec inertness, rank promotion + span
                              event attributes, and component fault routing)
8. Structural craft:    PASS (one pure classifier plus one contained Phase-5 consumer;
                              no duplicated production policy or shallow module)

Verdict: CLEAN
Blockers: none
