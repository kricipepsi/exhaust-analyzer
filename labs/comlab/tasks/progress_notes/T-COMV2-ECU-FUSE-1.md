# T-COMV2-ECU-FUSE-1 progress note

Status: done
Date: 2026-06-21

## Plan

Mirror OBDLab's optional `lambda_perception_delta` and
`total_trim_correction_delta_b2` fields into COMLab at their exact emitter
types. Add a pure ECU-fuse classifier and a default-off Phase-5 router reader
that treats symmetric railed trim plus era-tolerance gas↔OBD divergence as
conflict-aware evidence for existing `ecu_fault` rows. Thread the already
computed era tolerance into the sanitized router payload, preserve the existing
perception detector, and keep every absent/false guard byte-identical. Touch
only ingestion, router, the direct aggregator tolerance seam, focused tests,
this note, and the ledger row; no registry, emitter, graph, or UI changes.

## Changed Files

- `comlab/schemas/ingestion.py` — mirrored the two optional OBD fields with
  named consumer comments.
- `comlab/core/fault_atlas_router.py` — added `_EcuFaultVerdict`,
  `_ecu_fault_verdict`, `enable_ecu_fuse=False`, and Phase-5 `ecu_fault`
  evidence promotion with `ecu_fault_fused` tracing.
- `comlab/core/lab_pipeline_aggregator.py` — threads the existing active era
  lambda tolerance into the sanitized payload; no new threshold calculation.
- `tests/unit/test_fault_atlas_router.py` — controlled ECU-fuse registry,
  flag/guard regression tests, promotion/rejection tests, span assertion, and
  existing perception-axis reachability lock.
- `tasks/PROGRESS.md` — closed the task.

VERIFICATION GATE — T-COMV2-ECU-FUSE-1
=======================================
Phase 1 Syntax/import:  PASS — Python 3.14.6 native adapted COMLab venv;
                        changed Python files compile and import through tests.
Phase 2 Type check:     PASS — pyright `comlab/`: 0 errors, 0 warnings.
Phase 3 Lint:           PASS — `ruff check .`: all checks passed.
Phase 4 pytest:         PASS — 458 passed, 4 skipped; focused ECU/perception
                        selection 5 passed; router module 87 passed.
Phase 5 Wiki/orphan:    PASS — thresholds cite COMLab wiki sections; fields are
                        read in the live default-off router branch.
Phase 6 Diff review:    PASS — 4 implementation/test files plus this note and
                        one ledger-row edit; aggregator is the direct dependency
                        required to pass the existing era tolerance.

Consumer-read greps:

- `rg -n "total_trim_correction_delta_b2|lambda_perception_delta" comlab/core/fault_atlas_router.py`
  → helper inputs at lines 219/236/242 and reachable reads at lines 1009–1013.
- `rg -n "enable_ecu_fuse" comlab/core/fault_atlas_router.py`
  → default-off constructor at line 424, stored flag at line 448, live branch at
  line 1008.

`comlab-python` checklist applied: typed signatures; docstrings on new symbols;
no mutable defaults; no bare exceptions; named/cited constants; no new string
formatting or filesystem code; explicit `is None`; imports ordered.

Status: DONE — `PROGRESS.md` flipped to done.

CODE REVIEW — T-COMV2-ECU-FUSE-1
=================================
1. Design rules:        PASS — JSON-boundary mirrors only; no cross-lab import,
                        raw-sensor derivation, graph operation, additive bump,
                        forced override, or default activation.
2. Scope compliance:    PASS — aggregator edit is the direct dependency for
                        threading the same tolerance already used by
                        `perception_contradiction.detect`.
3. Contracts:           PASS — both fields are additive `float | None = None`
                        mirrors of the emitter; constructor flag is trailing and
                        default-off; existing callers remain valid.
4. Docstrings:          PASS — verdict type and pure helper document purpose,
                        inputs/abstention, output, and wiki sources.
5. Wiki provenance:     PASS — 25.0 saturation and 0.80 confidence literals
                        carry pinpoint COMLab wiki citations.
6. Immediate Checklist: PASS — no warnings.
7. Test coverage:       PASS — off/absent/tolerance/trim guards, ECU promotion,
                        real-mixture agreement, bank asymmetry, trace event, and
                        unchanged live perception axis are covered.
8. Structural craft:    PASS — pure classifier keeps policy separate from rank
                        mutation; router branch mirrors the established
                        bank-fuse seam; no new shallow module or duplication.

Verdict: CLEAN
Blockers: none
