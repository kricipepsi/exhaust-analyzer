# T-OIL-R1 — Demote orphaned KG/symptom artefacts to proposals + anti-orphan test

### Goal ###

Bring the first-pass oil artefacts into compliance with the signal/noise rule
without changing live behaviour. The `P_NEW_09…13` KG nodes, the three "Engine
Mechanical (Piston Rings / PCV-Crankcase / Turbo Oil Seal)" display families, and
the `oil_consumption.*` tier_2 symptom-prior mappings currently have **no live
reader** (the live shim path never loads the COMLab KG). This task records them in
the **proposals registry** (`comlab/comlab/config/proposals/`) with a named future
consumer, and adds a test proving they are NOT consulted on the live path. Done when
`registry/tests/test_oil_no_kg_on_live_path.py` is green and the proposals entries
carry a future-consumer line each.

### Success criteria ###

- `registry/tests/test_oil_no_kg_on_live_path.py::test_live_route_does_not_load_comlab_kg`
  passes — asserts a live `route_case` call resolves an oil case to a registry
  `MW-00x` verdict and that `comlab/config/kg/` is never opened (monkeypatch /
  import-guard). Write it failing first.
- `registry/tests/test_oil_no_kg_on_live_path.py::test_oil_proposals_have_future_consumer`
  passes — every oil proposal entry has a non-empty `future_consumer` field naming
  a task id (`T-OIL-R4`/`R5`/`U-OIL-KG-1`).
- Existing `comlab` + `registry` suites stay green before and after.

### Context ###

The drift, pinned in `OIL_CONSUMPTION_START_HERE.md §0`: `route()` defaults to the
v2 shim (`fault_atlas_router.py:249`, `:1017`), and the shim builds the verdict from
the registry rule only (`integration_shim.py::_translate_to_output`) — it never
calls `fault_atlas_kg.resolve`. So the first-pass KG nodes/families and the tier_2
symptom-prior rows (the live `symptom_prior.yaml` is keyed on `_csv_primary_symptom`
and lifts a whole family — it cannot separate rings/valve-seals/PCV, all
`mechanical_wear`) are orphans. This task does not try to make them live; it records
them honestly as proposals so the ledger stops claiming a consumer that the engine
does not run. The future consumer that will graduate them is `U-OIL-KG-1` (wire KG
enrichment into the v2 path).

Pinned anchors: `comlab/comlab/config/kg/mechanical_wear.json:205` (the five
`P_NEW_*` nodes, all `fault_family: mechanical_wear`); `comlab/comlab/config/
proposals/entries.yaml` (existing oil symptom-prior rows, lines ~98-120);
`comlab/comlab/config/symptom_prior.yaml` (live, CSV-keyed — leave unchanged).

STRICT-ONLY: Load skills: none.

### Consumer (signal/noise) ###

- **Consumer:** the **proposals registry** itself (documented future consumer), not
  a live decision. The future live consumer is `U-OIL-KG-1` (KG enrichment in v2
  `route()`), named in `PROGRESS.md §4`.
- **Code path:** `comlab/comlab/config/proposals/entries.yaml` +
  `proposals.yaml` — read by the proposals tooling/tests, never by
  `integration_shim.route_case`. The anti-orphan test asserts that absence.

### Deliverables ###

1. `comlab/comlab/config/proposals/entries.yaml` — add/annotate the 3 display
   families + tier_2 oil markers with a `future_consumer:` line each.
2. `comlab/comlab/config/proposals/proposals.yaml` — register `P_NEW_09…13` KG nodes
   as proposal entries (mark proposal-only; not loaded live).
3. `registry/tests/test_oil_no_kg_on_live_path.py` — the two tests above.

### Files to touch ###

- `comlab/comlab/config/proposals/entries.yaml` (MODIFY)
- `comlab/comlab/config/proposals/proposals.yaml` (MODIFY)
- `registry/tests/test_oil_no_kg_on_live_path.py` (CREATE)

### Out of scope ###

Do NOT wire KG enrichment into `route()` (that is the future `U-OIL-KG-1`). Do NOT
edit `symptom_prior.yaml`, the live registry rules, or `config/kg/*.json` content
(the nodes stay where they are; this task only *registers* them as proposals and
proves they are not live). No new oil rules — those are R2/R4/R5. GRAPH GUARDRAIL:
do not run graphify or rebuild any graph.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab   # Windows: C:\Users\muto\claude\4DApp\4DLab
# Inner loop
ruff check registry/tests/test_oil_no_kg_on_live_path.py
pyright registry/tests/test_oil_no_kg_on_live_path.py
# Structural
python3.14 -c "import yaml,sys; d=yaml.safe_load(open('labs/comlab/comlab/config/proposals/proposals.yaml')); print('P_NEW_09' in str(d))"
# Functional
python3.14 -m pytest -x -q registry/tests/test_oil_no_kg_on_live_path.py
python3.14 -m pytest -q labs/comlab registry/tests
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-OIL-R1`: Status=done, Files changed=3, Verification="anti-orphan test green; oil KG/families/symptom rows registered as proposals with future_consumer"
