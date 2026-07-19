# T-COMV2-NOSTART-1 progress note

Status: done
Date: 2026-06-21

## Plan / Scope Confirm

Mirror two DTCLab-emitted no-start discriminator signals that COMLab currently lacks:
(1) `Mode06MonitorState.MONITOR_ABORTED` in the `Mode06Status` enum and
(2) `ff_fuel_spark_cut_at_crank: bool = False` in `FreezeFrameRecord`.
Then wire a named reader in `FaultAtlasRouter.execute_triage_loop()` Phase 5
behind a default-off `enable_nostart` flag. The reader classifies no-start as
**security-lockout** (both signals present → promote `ERR-NS-005`) vs
**mechanical** (monitor aborted without cut → promote `ERR-NS-001/2/3/4`).
Keep flag-off, `dtc_lab_output`-absent, and no-`MONITOR_ABORTED` paths
byte-identical. Closes DEP-8 anti-orphan on both signals. CAN-era is already
gated at the emitter; COMLab does not re-gate.

Files: `vocabulary.py`, `ingestion.py`, `fault_atlas_router.py`,
`test_fault_atlas_router.py`, `test_vocabulary.py` (wiki drift guard),
`PROGRESS.md`, `progress_notes/T-COMV2-NOSTART-1.md`.

## Changed Files

- `comlab/schemas/vocabulary.py` — added `MONITOR_ABORTED = "MONITOR_ABORTED"` to
  `Mode06Status` enum (was tri-state, now 4 values); updated `Mode06MonitorState`
  alias comment.
- `comlab/schemas/ingestion.py` — added `ff_fuel_spark_cut_at_crank: bool = False`
  to `FreezeFrameRecord` §12.3 derived-flags block.
- `comlab/core/fault_atlas_router.py` — added `_NOSTART_CONFIDENCE`,
  `_NOSTART_SECURITY_NODES`, `_NOSTART_MECHANICAL_NODES` constants; `_NoStartVerdict`
  frozen dataclass; `_no_start_branch()` pure helper; `enable_nostart: bool = False`
  constructor param; Phase-5 promote block (DTC-keyed, after VE gate, before misfire).
- `tests/unit/test_fault_atlas_router.py` — `_nostart_request()` /
  `_nostart_router()` helpers; 7 tests: inert-when-off, no-aborted-inert,
  security-lockout activation, mechanical activation, helper-unavailable,
  helper-states, schema-roundtrip.
- `tests/unit/test_vocabulary.py` — updated `Mode06Status` + `Mode06MonitorState`
  drift-guard expected count 3→4; added `MONITOR_ABORTED` to `_WIKI_PENDING`.

VERIFICATION GATE — T-COMV2-NOSTART-1
=======================================
Phase 1 Syntax/import:  PASS (ruff: all checks passed)
Phase 2 Type check:     PASS (pyright: 0 new errors; all 15 pre-existing)
Phase 3 Lint:           PASS (`ruff check .`: all checks passed)
Phase 4 pytest:         PASS (500 passed, 4 skipped; nostart target 7 passed)
Phase 5 Wiki/orphan:    PASS (0.80 confidence cited per wiki/09 §CONCEPT_CONF_TIER;
                              node sets cited per wiki/06 §CONCEPT_FAM_NONSTART;
                              `ff_fuel_spark_cut_at_crank`/`MONITOR_ABORTED` read at
                              fault_atlas_router.py:442/:447/:1383/:1405;
                              `enable_nostart` branch at :561/:590/:1380)
Phase 6 Diff review:    PASS (vocabulary, ingestion, router, tests, note, ledger row only)

Fusion-consumer checklist:
  - Field mirrored at emitter's exact type ✓
  - Wiki cites on every literal ✓
  - Default-off flag, byte-identical single-point ✓
  - Evidence, not override (max(score, confidence)) ✓
  - Two greps prove orphaned signals read in reachable path ✓

CODE REVIEW — T-COMV2-NOSTART-1
================================
All changes are additive and default-off. No existing behaviour is altered.
The Phase-5 promote block follows the exact BANK-FUSE pattern (guard → helper →
node-set → iterate scoped → promote → span event), keyed on `request.dtc_lab_output`
instead of `request.obd_live_data`. The helper function is pure, module-level,
and independently tested. Schema changes are exact mirrors of the DTCLab emitter
types. Tests cover all 5 spec-named scenarios plus 2 helper-unit tests and the
schema round-trip. No cross-lab imports. No graphify. No new fault nodes.
