# T-COMV2-FUELSYS-GATE-1 progress note

Status: done
Date: 2026-06-21

## Plan

Mirror OBDLab's live `fuel_system_status` field onto COMLab's
`OBDLiveDataPayload` as an optional local `FuelSystemStatus` enum. Add a pure
closed/open-loop classifier and a default-off Phase-5 router reader that caps
trim-driven `lean_condition` and `rich_mixture` evidence below the winner floor
when O2 feedback is unavailable. Preserve byte-identical output for flag-off,
field-absent, and `CL` inputs. Touch only ingestion, the fault-atlas router,
focused tests, this note, and the ledger row; no emitter, registry, UI, graph, or
live-activation changes.

## Changed Files

- `comlab/schemas/ingestion.py` — mirrored optional OBD-live
  `fuel_system_status` with its named consumer.
- `comlab/core/fault_atlas_router.py` — added `_fuel_system_gate`,
  `_OPEN_LOOP_TRIM_CONFIDENCE_CAP`, `enable_fuelsys_gate=False`, and the
  Phase-5 lean/rich evidence demotion with `fuel_system_gated` tracing.
- `tests/unit/test_fuel_system_gate.py` — covered JSON enum validation,
  flag-off/closed-loop/absent invariance, all three open-loop states, both
  trim-driven families, threshold suppression, and trace attributes.
- `tasks/PROGRESS.md` — closed the task.

VERIFICATION GATE — T-COMV2-FUELSYS-GATE-1
===========================================
Phase 1 Syntax/import:  PASS — Python 3.14.6 native adapted COMLab venv;
                        changed Python files compiled and imported through tests.
Phase 2 Type check:     PASS — pyright `comlab/`: 0 errors, 0 warnings.
Phase 3 Lint:           PASS — `ruff check .`: all checks passed.
Phase 4 pytest:         PASS — focused fuel-system suite 9 passed; full suite
                        472 passed, 4 skipped.
Phase 5 Wiki/orphan:    PASS — the 0.60 cap cites COMLab wiki §08; the optional
                        field is read in the reachable default-off Phase-5 branch.
Phase 6 Diff review:    PASS — 3 implementation/test files plus this note and
                        one ledger-row/status update; no scope creep.

Consumer-read greps:

- `rg -n "fuel_system_status" comlab/core/fault_atlas_router.py`
  → classifier input/guards at lines 247–257 and live read at line 1070.
- `rg -n "enable_fuelsys_gate" comlab/core/fault_atlas_router.py`
  → constructor at line 483, stored flag at line 509, reachable branch at line
  1069.

`comlab-python` checklist applied: typed signatures; docstrings on new symbols;
no mutable defaults; no bare exceptions; named/cited constant; no new string
formatting or filesystem code; explicit `is None`; imports ordered.

Status: DONE — `PROGRESS.md` flipped to done.

CODE REVIEW — T-COMV2-FUELSYS-GATE-1
=====================================
1. Design rules:        PASS — local JSON-boundary enum mirror only; no
                        cross-lab import, raw-sensor derivation, override,
                        additive bump, graph operation, or default activation.
2. Scope compliance:    PASS — only the task's named implementation, test,
                        note, and ledger files changed.
3. Contracts:           PASS — additive `FuelSystemStatus | None = None`
                        inbound field and trailing default-off constructor flag;
                        existing callers remain valid.
4. Docstrings:          PASS — the pure classifier documents purpose, return
                        states, and COMLab wiki/proposal sources.
5. Wiki provenance:     PASS — the 0.60 confidence cap has a pinpoint
                        `CONCEPT_EVIDENCE_INPUTS` citation.
6. Immediate Checklist: PASS — no warnings.
7. Test coverage:       PASS — enum parsing, all falsy guards, CL no-op, every
                        open-loop enum, lean/rich demotion, threshold behavior,
                        and trace payload are covered.
8. Structural craft:    PASS — policy is isolated in a pure classifier; the
                        router branch follows the existing evidence-reader seam
                        and introduces no shallow module or duplicated caller
                        wiring.

Verdict: CLEAN
Blockers: none
