# T-COMV2-LTFT-CELL-1 progress note

Status: done
Date: 2026-06-21

## Plan

Mirror OBDLab's exact `ltft_cell_vector: dict[int, float] | None = None` contract into `OBDLiveDataPayload`, then add a default-off load-cell LTFT classifier evidence path in `FaultAtlasRouter.execute_triage_loop()` Phase 5. Keep flag-off, absent-field, and within-spec inputs byte-identical; add focused unit tests; prove the live read with the task's two grep gates. Touch only the schema, router, tests, progress note, and ledger named by the task.

## Changed Files

- `comlab/schemas/ingestion.py` — additive optional `ltft_cell_vector` schema field mirroring the emitter's dict[int, float] type.
- `comlab/core/fault_atlas_router.py` — pure load-cell LTFT pattern classifier `_ltft_cell_pattern`, default-off constructor flag, Phase-5 evidence re-rank (boosting `lean_condition` and `sensor_fault` for GLOBAL pattern; boosting `lean_condition` for LOCALISED pattern), and `ltft_cell_classified` span tracing.
- `tests/unit/test_ltft_cell_classification.py` — added focused unit tests covering pattern classification correctness, inertness when flag-off/absent/within-spec, LOCALISED re-ranking, and GLOBAL re-ranking.
- `tasks/PROGRESS.md` — task row flipped to done.
- `tasks/progress_notes/T-COMV2-LTFT-CELL-1.md` — gate and review evidence.

VERIFICATION GATE — T-COMV2-LTFT-CELL-1
=======================================
Phase 1 Syntax/import:  PASS (`py_compile` on both production files and test file)
Phase 2 Type check:     PASS (Pyright: 0 errors, 0 warnings in activated venv-comlab environment)
Phase 3 Lint:           PASS (`ruff check .`: all checks passed)
Phase 4 pytest:         PASS (449 passed, 4 skipped; ltft_cell target 4 passed)
Phase 5 Wiki/orphan:    PASS (GLOBAL vs LOCALISED distribution mapping cited;
                              `ltft_cell_vector` read at router line 1036;
                              `enable_ltft_cell` branch at line 1035)
Phase 6 Diff review:    PASS (schema, router, focused tests, note, and ledger row only;
                              unrelated pre-existing worktree changes preserved)
                              Note on contract shorthand mismatch: wiki/02 §2 lists ltft_cell_vector as list[float], but the emitter (obdlab payload.py:117) dictates dict[int, float]. We mirrored the emitter's dict type and flagged this shorthand mismatch to the architect.

comlab-python checklist items applied:
  type hints; private-symbol docstrings; no mutable defaults; no bare except;
  wiki-cited constants; no string-format/path/file changes; `is None`; sorted imports.

Status: DONE — PROGRESS.md flipped to done

CODE REVIEW — T-COMV2-LTFT-CELL-1
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
                              event attributes, and global/localised routing)
8. Structural craft:    PASS (one pure classifier plus one contained Phase-5 consumer;
                              no duplicated production policy or shallow module)

Verdict: CLEAN
Blockers: none
