# T-OIL-R2 — Verify + lock the three live single-snapshot oil verdicts

### Goal ###

Prove and pin that the three oil cases already expressible on the live path resolve
to their intended registry rules: worn rings → `MW-001`, valve-stem seals →
`MW-002`, head-gasket oil/coolant breach → `MW-003`. Add registry tests that feed
each case's low-idle gas signature through the live shim and assert the winning
`fault_code`. Tweak the three rules **only** if a test exposes a real miss. Done when
`registry/tests/test_oil_live_verdicts.py` is green.

### Success criteria ###

- `registry/tests/test_oil_live_verdicts.py::test_rings_routes_to_mw001` passes —
  payload with `chemical_state=WORN_PISTON_RINGS`, `gas_hc=380` → `fault_code=MW-001`.
- `::test_valve_seals_routes_to_mw002` passes — `WORN_VALVE_SEALS`, transient HC →
  `fault_code=MW-002`.
- `::test_head_gasket_routes_to_mw003` passes — `COOLANT_LEAK_INTERNAL`, `ect_c>95`,
  elevated O₂ → `fault_code=MW-003`.
- Existing `registry/tests` suite stays green (no regression in the 16 rulesets).

### Context ###

These three cases work today because their existing `mechanical_wear` rules match on
a single-point chemistry + HC/ECT gate (the only data the current `GasLabPayload`
carries). This row does not add capability; it **locks** the current live behaviour
with explicit oil-case tests so R4/R5 (which add PCV/turbo on the same
`mechanical_wear` family) cannot silently steal these verdicts later. Pinned rule
anchors: `registry/rules/mechanical_wear.json` — `MW-001` (`WORN_PISTON_RINGS` +
`hc ge 200`, line 6), `MW-002` (`WORN_VALVE_SEALS`, line 56), `MW-003`
(`COOLANT_LEAK_INTERNAL` + `ect_c gt 95.0`, line 96). Dossier signatures pinned in
`PROGRESS.md §2`.

STRICT-ONLY: Load skills: none.

### Consumer (signal/noise) ###

- **Consumer:** `route()` verdict via the shim — the live diagnostic output the UI
  renders. No new schema field.
- **Code path:** `integration_shim.route_case_with_diagnostics` →
  `_translate_to_output` → `fault_code = rule.rule_id`. Tests assert the value.
- N/A — no new field/enum/fault (verification + test lock only).

### Deliverables ###

1. `registry/tests/test_oil_live_verdicts.py` — three routing tests above.
2. `registry/rules/mechanical_wear.json` — **only if** a test fails: minimal,
   cited tweak to the failing rule's gate (record the reason in the progress note).

### Files to touch ###

- `registry/tests/test_oil_live_verdicts.py` (CREATE)
- `registry/rules/mechanical_wear.json` (MODIFY — conditional, minimal)

### Out of scope ###

No PCV/turbo rules (R4/R5). No high-idle fields (R3a/R3b). No KG/proposals edits
(R1). Do not "improve" adjacent `mechanical_wear` rules (`MW-004…007`) — if a test
surfaces an issue there, log it as an Unplanned follow-up, do not fix it here.
GRAPH GUARDRAIL: no graphify / graph rebuild.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab
ruff check registry/tests/test_oil_live_verdicts.py
pyright registry/tests/test_oil_live_verdicts.py
python3.14 -m pytest -x -q registry/tests/test_oil_live_verdicts.py
python3.14 -m pytest -q registry/tests
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-OIL-R2`: Status=done, Files changed={1 or 2}, Verification="rings/valve-seals/head-gasket route to MW-001/002/003 on live shim path; registry suite green"
