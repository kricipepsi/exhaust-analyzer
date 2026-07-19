# T-OIL-R3b — Shim high-idle PID resolver + rule-schema high-idle evidence

### Goal ###

Teach the registry shim to read the high-idle gas fields added in R3a and to let a
rule express high-idle evidence. Add `high_idle_hc`, `high_idle_co`,
`high_idle_lambda` (and the others as needed) to the shim PID resolver, and confirm
the rule-schema `obd_evidence`/`chemistry_evidence` path can carry a high-idle gated
row. Done when a synthetic rule gating on `high_idle_hc` fires correctly through
`route_case_with_diagnostics` under test.

### Success criteria ###

- `registry/tests/test_shim_high_idle_pids.py::test_resolves_high_idle_hc` passes —
  `_build_observation` on a payload with `high_idle_hc=130` resolves the PID to 130.0.
- `::test_rule_with_high_idle_gate_fires` passes — a fixture rule with an
  `obd_evidence` row `{pid: high_idle_hc, operator: lt, value: 200}` fires for a
  turbo-shaped payload and is pruned for a rings-shaped one.
- Missing high-idle (legacy single-snapshot payload) → resolver returns `None` and
  any high-idle-gated rule is pruned, not crashed.
- Existing `registry/tests` suite stays green.

### Context ###

`registry/integration_shim.py` resolves single-point gas PIDs via `_PID_SOURCES`
(`"hc": (("gas","gas_hc"),)`, etc., ~line 51) into `_Observation`
(~line 180). This row adds the high-idle sources (`"high_idle_hc":
(("gas","high_idle_hc"),)`, …) and ensures `evaluate`/`_check_obd_evidence`
(~line 452) treats a `None` high-idle value as "constraint not satisfied" (mirrors
the v1 `evaluate_operator` None→False contract, `fault_atlas_router.py:416`). No
verdict-shape change. This unblocks R4/R5, whose rules gate on the delta.

STRICT-ONLY: Load skills: none.

### Consumer (signal/noise) ###

- **Consumer:** R4 (`MW-008` PCV) and R5 (`MW-009` turbo) rules — they read the
  `high_idle_*` PIDs this row resolves. Reader ships in the same pack.
- **Code path:** `integration_shim._PID_SOURCES` + `_build_observation` →
  `_check_obd_evidence` → `_score_rule`. Each new PID source has a one-line wiki
  citation comment.

### Deliverables ###

1. `registry/integration_shim.py` — add high-idle PID sources + None-safe handling.
2. `registry/tests/test_shim_high_idle_pids.py` (CREATE) — the tests above.

### Files to touch ###

- `registry/integration_shim.py` (MODIFY)
- `registry/tests/test_shim_high_idle_pids.py` (CREATE)

### Out of scope ###

No new live rules (R4/R5 add those). No `GasLabPayload` change (R3a owns the
contract). Do not change the verdict dict shape or the v1 inline path. Resolve only
the high-idle PIDs the PCV/turbo rules will actually use — do not pre-add resolvers
with no R4/R5 consumer (that would be a fresh orphan). GRAPH GUARDRAIL: no graphify.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab
ruff check registry/integration_shim.py registry/tests/test_shim_high_idle_pids.py
pyright registry/integration_shim.py
python3.14 -m pytest -x -q registry/tests/test_shim_high_idle_pids.py
python3.14 -m pytest -q registry/tests
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-OIL-R3b`: Status=done, Files changed=2, Verification="shim resolves high_idle_* PIDs None-safely; high-idle-gated fixture rule fires/prunes correctly; registry suite green"
