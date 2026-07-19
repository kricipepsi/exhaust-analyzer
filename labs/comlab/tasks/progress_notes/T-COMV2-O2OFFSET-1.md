# T-COMV2-O2OFFSET-1 progress note

Status: done
Date: 2026-06-21

## Plan

Consume the already-mirrored OBD `o2_failure_mode` together with GAS
`lambda_chem` in a module-level wideband-offset classifier. Add a default-off
Phase-5 router reader that promotes only existing `sensor_fault` rows when the
OBD candidate conflicts with stoichiometric gas truth, leaving real lean/rich
mixtures and every absent/false guard inert. Reconcile proposal `EP-OBD-17` to
the shipped symbol and touch only the router, proposal entry, focused tests,
this note, and the ledger row; no schema, emitter, registry/KG, perception-axis,
aggregator, or UI changes.

## Changed Files

- `comlab/core/fault_atlas_router.py` — added the pure
  `_resolve_o2_sensor_fault` helper, COMLab-wiki-cited stoichiometric/confidence
  constants, trailing `enable_o2_offset=False` constructor flag, and Phase-5
  `sensor_fault` evidence promotion with `o2_offset_confirmed` tracing.
- `comlab/config/proposals/proposals.yaml` — reconciled `EP-OBD-17` to the
  module-level helper symbol actually shipped.
- `tests/unit/test_fault_atlas_router.py` — added a controlled two-family
  router and focused flag-off, absent-OBD, unavailable-helper, promotion,
  real-lean rejection, non-candidate, and trace-event tests.
- `tasks/PROGRESS.md` — closed the task.

VERIFICATION GATE — T-COMV2-O2OFFSET-1
======================================
Phase 1 Syntax/import:  PASS — Python 3.14.6 via the supplied
                        `.venv-comlab`; changed Python files compile and import
                        through focused/full pytest.
Phase 2 Type check:     PASS — Pyright `comlab/` with the venv interpreter:
                        0 errors, 0 warnings.
Phase 3 Lint:           PASS — `ruff check .`: all checks passed.
Phase 4 pytest:         PASS — 493 passed, 4 skipped; focused O2-offset
                        selection 5 passed.
Phase 5 Wiki/orphan:    PASS — 0.97/1.03 and 0.80 constants cite the COMLab
                        wiki; no unsourced production numerics, cross-lab
                        imports, or graph changes; the contracted field is read
                        in the live default-off router branch.
Phase 6 Diff review:    PASS — router, proposal string, focused tests, this
                        note, and one ledger-row edit only; unrelated
                        pre-existing worktree changes preserved.

Consumer-read greps:

- `rg -n "o2_failure_mode" comlab/core/fault_atlas_router.py`
  → helper input/guards at lines 314/327/329 and reachable live read at line
  1191.
- `rg -n "enable_o2_offset" comlab/core/fault_atlas_router.py`
  → default-off constructor at line 513, stored flag at line 541, and live
  branch at line 1190.

`comlab-python` checklist applied: typed signatures; docstring on the new
helper; no mutable defaults; no bare exceptions; named/wiki-cited constants; no
new string-formatting or filesystem code; explicit `is None`; imports sorted.

Status: DONE — `PROGRESS.md` flipped to done.

CODE REVIEW — T-COMV2-O2OFFSET-1
================================
1. Design rules:        PASS — consumes mirrored verdict fields only; no
                        cross-lab import, raw-sensor derivation, KG mutation,
                        additive bump, forced override, or default activation.
2. Scope compliance:    PASS — only task-declared implementation, proposal,
                        test, note, and ledger areas changed.
3. Contracts:           PASS — no schema change; the router constructor gains
                        one trailing default-off argument, so existing callers
                        remain compatible.
4. Docstrings:          PASS — the new pure helper documents purpose,
                        abstention, output states, and wiki sources.
5. Wiki provenance:     PASS — stoichiometric bounds and evidence confidence
                        have pinpoint COMLab-wiki citations.
6. Immediate Checklist: PASS — no warnings.
7. Test coverage:       PASS — flag-off identity, absent OBD, both `None`
                        helper guards, confirmed promotion/event, real-lean
                        rejection/no-event, and two non-candidate/no-event
                        cases are covered.
8. Structural craft:    PASS — one pure classifier and one contained Phase-5
                        reader follow the existing router seam; the controlled
                        test registry follows established helpers without
                        adding a shallow production module.

Verdict: CLEAN
Blockers: none
