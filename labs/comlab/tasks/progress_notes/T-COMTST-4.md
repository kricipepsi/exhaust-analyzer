# T-COMTST-4 — Progress Notes

## Plan

Add a test-only `tests/regression/` golden-master suite using fully assembled
COMLab request payloads captured from the 24-row characterization corpus. Pin the
current top fault, family, degradation mode, and processing-confidence rating for
5–7 canonical scenarios, plus the current ingestion rejection for malformed
input. Do not change production code, schemas, graph artifacts, or existing
harness tests. Signal/noise consumer: N/A; no production field, enum, or fault is
added.

## Capture finding

The 24-row capture passed on 2026-06-21. `COM-013` is rejected by
`OrchestratorInboundRequest.model_validate()` with `ERR-CONTRACT-001`; it never
reaches `LabPipelineAggregator.process()`. The rows labeled `fatal_incomplete`
currently emit non-fatal verdicts, and `process()` does not invoke
`run_fatal_gates_and_routing()`. Per task scope, production behavior was not
changed. The regression suite pins the actual contract rejection and records the
missing reachable `FATAL_INCOMPLETE` UI output as a follow-up.

## Negative control

Changed `case_001_no_fault.json` from `NF-001` to `NF-999` temporarily. The
regression run produced exactly one failure,
`test_comlab_regression[case_001_no_fault]`, with the other seven tests passing.
The fixture was restored and the suite returned to green.

VERIFICATION GATE — T-COMTST-4
=============================
Phase 1 Syntax/import:  PASS (`py_compile`; imports exercised by pytest)
Phase 2 Type check:     PASS (0 errors, 0 warnings; venv Python passed explicitly)
Phase 3 Lint:           PASS (ruff: all checks passed)
Phase 4 pytest:         PASS (regression 8 passed; full suite 431 passed, 4 skipped)
Phase 5 Wiki/orphan:    PASS (test-only; no production numerics, enums, fields, or consumers added)
Phase 6 Diff review:    PASS (9 regression deliverables; progress note + ledger only; no production scope creep)

comlab-python checklist items applied:
  type hints; module/function docstrings; no mutable defaults; no bare except;
  no string-formatting issue; pathlib/context-managed file reads; sorted imports.

Status: DONE — flipping PROGRESS.md to done

CODE REVIEW — T-COMTST-4
=======================
1. Design rules:        PASS (test-only; no cross-lab imports, graph work, raw-sensor derivation, or production surface)
2. Scope compliance:    PASS (`tests/regression/`, this note, and the ledger row only)
3. Contracts:           PASS (no public contract changed)
4. Docstrings:          PASS (module and helper/test functions documented)
5. Wiki provenance:     PASS (no production numerics or enums introduced)
6. Immediate Checklist: PASS (0 warnings)
7. Test coverage:       PASS (7 fixtures, manifest/coverage assertions, negative control verified)
8. Structural craft:    PASS (fixture loader and one parametrized execution path; no duplication in test logic)

Verdict: CLEAN
Blockers: none
