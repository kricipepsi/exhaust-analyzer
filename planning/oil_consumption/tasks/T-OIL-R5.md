# T-OIL-R5 — Turbo turbine-seal registry rule MW-009 (stoich-λ perception trigger)

### Goal ###

Add a new `mechanical_wear` registry rule `MW-009` for worn turbo turbine seals
(P_NEW_13). The tell is **extreme tailpipe HC at low idle with in-cylinder
combustion still stoichiometric** (oil cracks post-cylinder in the hot exhaust),
clearing at high idle. The rule must fire on the gas signature alone (a λ/CO band
match would miss it) and must not collide with PCV (`MW-008`, which is rich at idle).
Done when a turbo-shaped payload routes to `MW-009` and a PCV-shaped payload still
routes to `MW-008`.

### Success criteria ###

- `registry/tests/test_turbo_rule.py::test_turbo_routes_to_mw009` passes — payload
  `chemical_state=POA_SIGNATURE`, `gas_hc=720`, `gas_co=0.07`, `lambda_chem=1.00`,
  `high_idle_hc=130` → `fault_code=MW-009`. Write failing first.
- `::test_pcv_not_stolen_by_turbo` passes — the R4 PCV payload (`lambda_chem=0.93`)
  still routes to `MW-008`, not `MW-009` (rich-λ excludes turbo).
- `::test_turbo_needs_high_idle` passes — legacy payload without `high_idle_hc` does
  not fire `MW-009`.
- `registry/tests` suite stays green.

### Context ###

P_NEW_13 maps to live `POA_SIGNATURE` (proposal `TURBO_SEAL_OIL_LEAK`, T-OIL-2 pin).
Dossier logic (`OilburnCases.md` P_NEW_13, pinned in `PROGRESS.md §2`):
`low_idle.λ ∈ [0.99, 1.01]`, `low_idle.HC > 500 && low_idle.CO < 0.15`,
`high_idle.HC < 200`. Encode gating chemistry `POA_SIGNATURE` (GATING) +
`obd_evidence`: `hc ge 500` (DEFINITIVE), `co lt 0.15` (DEFINITIVE — clean burn),
`lambda_chem ge 0.99` AND `lambda_chem le 1.01` (stoich window — the perception
tell), `high_idle_hc lt 200` (DEFINITIVE — exhaust-flow dilution). The stoich-λ +
low-CO pair is what separates turbo from PCV (rich, λ<0.94). `forced_induction`
(VIN DNA) is **corroborating only** — do NOT make it a hard precondition (the gas
signature is the trigger; a hard VIN guard is deferred to `U-OIL-FI-1`). Cite each
literal with `OilburnCases.md P_NEW_13` + `GAS_VOCABULARY`.

STRICT-ONLY: Load skills: none.

### Consumer (signal/noise) ###

- **Consumer:** `route()` verdict — `MW-009` is the live turbo-seal diagnosis. Self
  consumer (ships live in this diff).
- **Code path:** `integration_shim._score_rule` → `_translate_to_output`
  (`fault_code=MW-009`). Consumes `high_idle_hc` (R3b) — a second justified reader
  for the R3a/R3b proposal pair.

### Deliverables ###

1. `registry/rules/mechanical_wear.json` — append `MW-009` with the gates above +
   citations.
2. `registry/tests/test_turbo_rule.py` (CREATE) — the four tests above.

### Files to touch ###

- `registry/rules/mechanical_wear.json` (MODIFY)
- `registry/tests/test_turbo_rule.py` (CREATE)

### Out of scope ###

No PCV rule (R4). No hard `forced_induction` precondition (→ `U-OIL-FI-1`). No
contract/resolver changes (R3a/R3b). Do not retune neighbours to force separation —
log a finding instead. No KG/display-family edits. GRAPH GUARDRAIL: no graphify.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab
ruff check registry/tests/test_turbo_rule.py
pyright registry/tests/test_turbo_rule.py
python3.14 -m pytest -x -q registry/tests/test_turbo_rule.py
python3.14 -m pytest -q registry/tests
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-OIL-R5`: Status=done, Files changed=2, Verification="MW-009 fires for turbo (stoich λ + low CO + HC drop), does not steal PCV MW-008, prunes without high-idle; registry suite green"
