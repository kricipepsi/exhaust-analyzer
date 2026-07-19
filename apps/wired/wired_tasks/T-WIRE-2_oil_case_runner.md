# T-WIRE-2 — oil-burning single-case CLI runner

### Goal ###
Build a single-case CLI runner `apps/wired/wired/run_case.py` that loads an
oil-burning case fixture, calls `diagnose()`, and prints/returns the verdict
(`diagnostic_verdict.fault_code` + confidence). Ship the oil-case fixtures and
assert each case routes to the expected verdict **per the T-PREP-WIRE-1 ruling**
(cases ruled FIX-NOW assert their corrected route; cases ruled
ACCEPT-KNOWN-BLOCKED assert the documented non-route). Done when the runner
exits 0 on a routed case and the fixture suite asserts the ruling's expectations.

### Success criteria ###
- `apps/wired/tests/test_oil_cases.py` passes: each oil fixture (`MW-002`,
  `MW-003`, `MW-009`, plus `MW-001`/`MW-008` per the ruling) reaches its expected
  verdict (routed) or expected documented non-route (known-blocked).
- Smoke: `/agent_workspace/.venv-wired/bin/python -m wired.run_case --case MW-002`
  exits 0 and prints a `fault_code` (run from `/agent_workspace`).

### Context ###
T-WIRE-1 proves the wiring returns a verdict; this proves it returns the
**right** verdict on the corpus this pack targets. **Blocked by T-WIRE-1 and
T-PREP-WIRE-1.** The prior wiring routed 3/5 oil cases (`MW-002/003/009`) and was
blocked on `MW-001` (rings) and `MW-008` (PCV) by GASLab<->registry chemistry
contradictions — the T-PREP-WIRE-1 ruling
(`wiring_prep_tasks/RINGS_PCV_TRIAGE_RULING.md`) decides the expectation for each.

Pin the case numerics from the dossier (READ-NARROW, grep the case IDs):
`planning/oil_consumption/PROGRESS.md` (the MW-00x map + per-case dossier) and
`planning/OIL_CASE_SIGNATURES_5FR.md`. The runner reads its verdict from
`OrchestratorFinalUIOutput.diagnostic_verdict.fault_code`
(`labs/comlab/comlab/schemas/response.py:132`).

Load skills: wired-composition-contract.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. The runner consumes `diagnose()`'s existing
output; fixtures are test data, not schema.

### Deliverables ###
1. `apps/wired/wired/run_case.py` — `argparse` CLI: `--case <ID>` -> load fixture
   -> `diagnose()` -> print verdict; `main()` returns exit 0/1.
2. `apps/wired/tests/fixtures/oil_cases/` — one JSON per oil case (raw inputs).
3. `apps/wired/tests/test_oil_cases.py` — parametrized assertions per the ruling.

### Files to touch ###
- `apps/wired/wired/run_case.py` (CREATE)
- `apps/wired/tests/fixtures/oil_cases/*.json` (CREATE)
- `apps/wired/tests/test_oil_cases.py` (CREATE)

### Out of scope ###
No multi-case CSV harness or accuracy scoring (separate pack). No OTel (T-WIRE-3).
No FATAL gate (T-WIRE-4). Do not edit any lab or COMLab code — if a case cannot
route because of a lab/registry bug not covered by the ruling, log a `T##b`
follow-up and mark that case `blocked`, do not patch a lab. Do not rebuild a graph.

### Verification ###
```bash
cd /agent_workspace
PY=.venv-wired/bin/python
$PY -m py_compile apps/wired/wired/run_case.py
$PY -m ruff check apps/wired/wired/run_case.py apps/wired/tests/test_oil_cases.py
( cd apps/wired && /agent_workspace/.venv-wired/bin/pyright . )
$PY -m wired.run_case --case MW-002
$PY -m pytest -x -q apps/wired/tests/test_oil_cases.py
```
All steps must pass.

### Progress hook ###
PROGRESS.md `T-WIRE-2`: Status=done, Files changed={COUNT}, Verification="oil cases route per T-PREP-WIRE-1 ruling; run_case --case MW-002 exits 0"
