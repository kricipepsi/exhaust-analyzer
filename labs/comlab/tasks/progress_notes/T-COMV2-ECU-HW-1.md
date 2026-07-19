# T-COMV2-ECU-HW-1 progress note

Status: done
Date: 2026-06-21

## Plan

Mirror OBDLab's optional `intake_air_temp_c` and `throttle_pos_pct` fields onto
COMLab's local `OBDLiveDataPayload`, implement the pure coherent digital-lie
AND-gate in `ECUHardwareChecker`, and wire its named reader into Phase 5 behind
`enable_ecu_hw=False`. Promote only existing `ecu_fault` rows as conflict-aware
evidence. Preserve byte-identical output when the flag is off, a required input
is absent, the signature is not met, or bank trim is asymmetric. Touch only the
task's ingestion, checker, router, focused test, note, and ledger files.

## Changed Files

- `comlab/schemas/ingestion.py` — mirrored optional emitter-faithful IAT/TPS
  fields with bounds, wiki provenance, and named consumer comments.
- `comlab/core/ecu_hardware_checker.py` — replaced the empty stub with the
  immutable verdict and pure digital-lie checker.
- `comlab/core/fault_atlas_router.py` — added `enable_ecu_hw=False`, one
  stateless checker instance, Phase-5 ECU-family promotion, and the
  `ecu_hardware_fault_applied` event.
- `tests/unit/test_ecu_hardware_checker.py` — covered schema bounds, every
  AND-gate guard, single-bank symmetry, flag-off/absent/normal invariance,
  ECU-fault promotion/event emission, and asymmetric rejection.
- `tasks/PROGRESS.md` — closed the selected ledger row.

VERIFICATION GATE — T-COMV2-ECU-HW-1
=====================================
Phase 1 Syntax/import:  PASS — changed Python files compiled under the
                        sanctioned native Python 3.14.6 COMLab venv.
Phase 2 Type check:     PASS — pyright with explicit venv `--pythonpath`
                        reported 0 errors, 0 warnings.
Phase 3 Lint:           PASS — `ruff check .` reported all checks passed.
Phase 4 pytest:         PASS — focused ECU-hardware suite 16 passed; full suite
                        488 passed, 4 skipped.
Phase 5 Wiki/orphan:    PASS — all thresholds and confidence constants cite
                        COMLab-local wiki sections; both mirrored fields are
                        read by the pure checker from the reachable Phase-5
                        default-off branch.
Phase 6 Diff review:    PASS — four implementation/test files plus this note
                        and the selected ledger row/status; no scope creep.

Consumer-read greps:

- `rg -n "intake_air_temp_c|throttle_pos_pct" comlab/core/ecu_hardware_checker.py comlab/core/fault_atlas_router.py`
  → checker inputs/guards at lines 31–63 and live router reads at lines
  1163/1165.
- `rg -n "enable_ecu_hw|ECUHardwareChecker" comlab/core/fault_atlas_router.py`
  → import at line 24, constructor flag at line 485, stored checker/flag at
  lines 512–513, and reachable branch at line 1161.

`comlab-python` checklist applied: typed signatures; docstrings on public
symbols; no mutable defaults; no bare exceptions; named and cited constants; no
legacy formatting or filesystem additions; explicit `is None`; imports ordered.

Status: DONE — `PROGRESS.md` flipped to done.

CODE REVIEW — T-COMV2-ECU-HW-1
===============================
1. Design rules:        PASS — local JSON-boundary mirrors only; no cross-lab
                        import, raw-sensor derivation, override, additive bump,
                        graph operation, or default activation.
2. Scope compliance:    PASS — only task-named implementation, test, note, and
                        ledger files changed.
3. Contracts:           PASS — additive optional inbound fields and a trailing
                        default-off router flag preserve existing callers.
4. Docstrings:          PASS — verdict, checker, check method, and test helpers
                        document their responsibilities.
5. Wiki provenance:     PASS — temperature, TPS, trim, symmetry, confidence,
                        and no-evidence constants have pinpoint COMLab cites.
6. Immediate Checklist: PASS — no warnings.
7. Test coverage:       PASS — schema constraints, all falsy guards,
                        single-bank acceptance, flag-off/absent invariance,
                        promotion/event, and asymmetric rejection are covered.
8. Structural craft:    PASS — policy remains in one pure checker behind a
                        small typed interface; the router only adapts evidence
                        into the established conflict-aware ranking seam.

Verdict: CLEAN
Blockers: none
