# T-COMV2-MISFIRE-LOC-1 progress note

Status: done
Date: 2026-06-21

## Plan

Mirror OBDLab's exact `per_cylinder_misfire_counts: dict[int, int] | None = None` contract into `OBDLiveDataPayload`, then add a default-off misfire locality evidence path in `FaultAtlasRouter.execute_triage_loop()` Phase 5. Keep flag-off, absent-field, and unavailable inputs byte-identical; add focused router tests; prove the live read with the task's two grep gates. Touch only the schema, router, tests, progress note, and ledger named by the task.

## Changed Files

- `comlab/schemas/ingestion.py` — exact optional `per_cylinder_misfire_counts: dict[int, int] | None = None` OBD mirror.
- `comlab/core/fault_atlas_router.py` — pure misfire locality classifier `_misfire_locality`, default-off constructor flag, Phase-5 evidence rerank (boosting misfire/ignition_fault and demoting lean_condition for single cylinder; boosting lean_condition for global), and `misfire_localised` span tracing.
- `tests/unit/test_fault_atlas_router.py` — three focused tests covering inertness/flag-off, single-cylinder bias, and global misfire.
- `tasks/PROGRESS.md` — task row closed.
- `tasks/progress_notes/T-COMV2-MISFIRE-LOC-1.md` — gate and review evidence.

VERIFICATION GATE — T-COMV2-MISFIRE-LOC-1
========================================
Phase 1 Syntax/import:  PASS (`py_compile` on both production files and test file)
Phase 2 Type check:     PASS (Pyright: 0 errors, 0 warnings)
Phase 3 Lint:           PASS (`ruff check .`: all checks passed)
Phase 4 pytest:         PASS (442 passed, 4 skipped; misfire-loc target 3 passed)
Phase 5 Wiki/orphan:    PASS (misfire localisation and trim thresholds cited;
                              `per_cylinder_misfire_counts` read at router line 895;
                              `enable_misfire_loc` branch at line 894)
Phase 6 Diff review:    PASS (schema, router, focused tests, note, and ledger row only;
                              unrelated pre-existing worktree changes preserved)

comlab-python checklist items applied:
  type hints; private-symbol docstrings; no mutable defaults; no bare except;
  wiki-cited constants; no string-format/path/file changes; `is None`; sorted imports.

Status: DONE — PROGRESS.md flipped to done

CODE REVIEW — T-COMV2-MISFIRE-LOC-1
=================================
1. Design rules:        PASS (verdict mirror only; no cross-lab import, raw-sensor
                              derivation, graph work, override, or default-on behavior)
2. Scope compliance:    PASS (only task-declared implementation/test/note/ledger areas)
3. Contracts:           PASS (additive default-None Pydantic field; trailing default-off
                              router argument; existing callers remain compatible)
4. Docstrings:          PASS (private result/helper and test support symbols documented)
5. Wiki provenance:     PASS (threshold, family set, evidence score, and proposals register sourced)
6. Immediate Checklist: PASS (0 warnings)
7. Test coverage:       PASS (flag-off/None/unavailable inertness, rank promotion + span
                              event, and global misfire routing)
8. Structural craft:    PASS (one pure classifier plus one contained Phase-5 consumer;
                              no duplicated production policy or shallow module)

Verdict: CLEAN
Blockers: none
