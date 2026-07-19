# T-GV2-2 — progress note

## Plan
Bring COMLab's local `ChemicalSignature` mirror to GASLab's 34-value surface:
drop `WRONG_VALVE_TIMING`, add the 3 `CAM_TIMING_*` members (verbatim per
GAS_VOCABULARY §3, same order), fix the 31/28 count docstrings to 34, migrate the
WVT test fixtures to `CAM_TIMING_RETARDED_MAP`, and add a GASLab-parity assertion
to the consistency guard. Executed by Cowork architect on explicit owner
authorization (2026-06-28), not delegated. Files: `comlab/schemas/vocabulary.py`,
`comlab/schemas/ingestion.py`, `comlab/config/global_fault_registry.json`,
`tests/unit/test_vocabulary.py`, `tests/e2e/test_kg_registry_consistency.py`,
`tests/e2e/test_diagnostic_engine.py`, `tests/fixtures/mock_gas_lab.py`,
`tests/fixtures/descriptor.py`, `tests/fixtures/comlab_cases.csv`,
`tests/regression/fixtures/case_022_legacy_cam_signal.json`.

**Coupled registry decision (owner-approved 2026-06-28).** The spec's
"do not edit registry; STOP and coordinate" note fired: COMLab's own
`global_fault_registry.json` still keyed two cam-timing rules (ERR-CT-001
chain-stretch, MAP-discriminated; ERR-CT-003 VVT full-retard) on the retired
`WRONG_VALVE_TIMING`, so the guard would fail the moment the enum dropped it.
Owner chose the **minimal re-point**: both → `CAM_TIMING_RETARDED_MAP`, with the
`_MAF`-variant coverage for MAF-equipped vehicles forward-registered as
`T-COM-CAMTIMING-MAF-1` on the comlab ledger.

## VERIFICATION GATE — T-GV2-2
1. Compile : PASS  (all edited .py compile)
2. Lint    : PASS  (ruff: All checks passed! on the 7 edited .py)
3. Types   : PASS  (pyright --pythonpath .venv-wired/bin/python on vocabulary.py + ingestion.py → 0 errors; the bare-invocation "pydantic unresolved" was a venvpath artifact, not a code error — same class as wiredV2 U-WV2-3)
4. Tests   : PASS  (full COMLab suite: 510 passed, 4 skipped — +1 vs 509 baseline = the new parity test; the 2 cam_timing CSV cases COM-011/COM-022 migrated and green)
5. Contract: PASS  (ChemicalSignature == 34 members; WRONG_VALVE_TIMING absent; {CAM_TIMING_RETARDED_MAP, CAM_TIMING_RETARDED_MAF, CAM_TIMING_ADVANCED} ⊆ values; global_fault_registry.json valid JSON, 0 live WRONG_VALVE_TIMING refs outside the intentional parity assertion)
6. Orphan  : PASS  (the 3 CAM_TIMING_* values are read by: the registry consistency guard `valid = {m.value for m in ChemicalSignature}`, and fault-atlas routing via ERR-CT-001/003 `gas_lab_state == CAM_TIMING_RETARDED_MAP` in global_fault_registry.json — grep-confirmed in a live path)
Result: CLEAN

## CODE REVIEW — T-GV2-2
Scope         : PASS — every changed line traces to the deliverable (enum mirror + docstrings + fixtures + parity guard) or to the owner-approved coupled registry re-point. No unrelated edits.
Composition   : N/A — this is a lab/consumer change, not wired composition. No cross-lab Python import added (mirror declared locally; names copied verbatim, not imported).
Consumers     : PASS — the 3 new values name their reader (cam_timing family route, ERR-CT-001) in inline comments; signal/noise satisfied (value re-point, not net-new field).
Literals      : N/A — no new numeric thresholds; the registry map_kpa<30 discriminator is unchanged.
Docstrings    : PASS — count docstrings corrected 31→34 (vocabulary) and 28→34 (ingestion).
Craft (WARN)  : Scope expanded beyond the spec's literal deliverable list to include global_fault_registry.json (2 rules), descriptor.py, comlab_cases.csv, and case_022 fixture — all *necessary* consequences of retiring the enum value (otherwise guard/regression/CSV nets break), and the registry edit was the owner-approved coupled decision. case_022's golden verdict was re-verified UNCHANGED after migration (MF-001/misfire/FULL_FUSION/LOW_CERTAINTY) — input-only migration, no snapshot rewrite, so no behaviour was silently re-baselined.
Result: CLEAN

## Follow-ups registered
- `T-COM-CAMTIMING-MAF-1` (comlab ledger, deferred) — add `_MAF`-variant cam-timing rules (ERR-CT-001b/003b keyed on `CAM_TIMING_RETARDED_MAF`) so MAF-equipped vehicles route; also covers `CAM_TIMING_ADVANCED` if a rule is wanted.
- `FU-2` (existing) — `OBD_VOCABULARY §17` doc-sync 32→34 (doc-only; the 3 values are parked in `test_vocabulary._WIKI_PENDING` until then).
