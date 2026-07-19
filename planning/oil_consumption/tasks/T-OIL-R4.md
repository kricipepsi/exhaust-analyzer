# T-OIL-R4 — PCV (stuck-open) registry rule MW-008

### Goal ###

Add a new `mechanical_wear` registry rule `MW-008` for a stuck-open PCV valve
(P_NEW_11) that fires on the rich-at-idle + HC-drops-at-high-idle signature and does
**not** collide with worn rings (`MW-001`). Done when a PCV-shaped payload routes to
`MW-008` and a rings-shaped payload still routes to `MW-001`, both under test.

### Success criteria ###

- `registry/tests/test_pcv_rule.py::test_pcv_routes_to_mw008` passes — payload
  `chemical_state=POA_SIGNATURE`, `gas_hc=610`, `lambda_chem=0.93`,
  `high_idle_hc=170` → `fault_code=MW-008`. Write failing first.
- `::test_rings_not_stolen_by_pcv` passes — the R2 rings payload (`gas_hc=380`,
  high-idle HC rising) still routes to `MW-001`, not `MW-008`.
- `::test_pcv_needs_high_idle` passes — a legacy payload without `high_idle_hc` does
  not fire `MW-008` (high-idle gate prunes it; falls back to prior POA behaviour).
- `registry/tests` suite stays green.

### Context ###

P_NEW_11 maps to live `POA_SIGNATURE` (proposal `PCV_STUCK_OPEN`, T-OIL-2 pin). The
discriminator vs rings is the **low→high-idle delta** plus **rich λ at idle**.
Dossier logic (`OilburnCases.md` P_NEW_11, pinned in `PROGRESS.md §2`):
`low_idle.λ < 0.94`, `low_idle.HC > 500 && high_idle.HC < 250`. Encode as a rule
gating chemistry `POA_SIGNATURE` (GATING) with `obd_evidence` rows: `hc ge 500`
(low-idle, DEFINITIVE), `high_idle_hc lt 250` (DEFINITIVE — the delta), `lambda_chem
lt 0.94` (SUGGESTIVE — rich-at-idle). Every literal carries an `OilburnCases.md
P_NEW_11` + `GAS_VOCABULARY` citation comment (house rule). `base_weight` ≈ 0.82
(above generic POA, below an exact-DTC match; pin against the existing
`mechanical_wear` weights so it out-scores `MW-001` only when the high-idle gate and
rich-λ both hold).

STRICT-ONLY: Load skills: none.

### Consumer (signal/noise) ###

- **Consumer:** `route()` verdict — `MW-008` is the live diagnosis the UI renders
  for a stuck-open PCV. This rule is its own consumer (ships live in this diff).
- **Code path:** `integration_shim._score_rule` scores `MW-008`;
  `_translate_to_output` sets `fault_code=MW-008`. The `high_idle_hc` PID consumed
  here is the reader that justifies R3a/R3b shipping.

### Deliverables ###

1. `registry/rules/mechanical_wear.json` — append `MW-008` with the gates above +
   citations.
2. `registry/tests/test_pcv_rule.py` (CREATE) — the four tests above.

### Files to touch ###

- `registry/rules/mechanical_wear.json` (MODIFY)
- `registry/tests/test_pcv_rule.py` (CREATE)

### Out of scope ###

No turbo rule (R5). No high-idle resolver/contract changes (R3a/R3b own those). Do
not retune `MW-001…007` to "make room" — if PCV vs rings can't separate with the
delta+λ gate, that is a finding for the progress note, not a silent reweight of
neighbours. No KG/display-family edits (R1 proposal). GRAPH GUARDRAIL: no graphify.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab
ruff check registry/tests/test_pcv_rule.py
pyright registry/tests/test_pcv_rule.py
python3.14 -m pytest -x -q registry/tests/test_pcv_rule.py
python3.14 -m pytest -q registry/tests
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-OIL-R4`: Status=done, Files changed=2, Verification="MW-008 fires for PCV (rich λ + HC drop), does not steal rings MW-001, prunes without high-idle; registry suite green"
