### Goal ###
Commit the C3 **signal pack** (ECU/control-system fault). Write the **4 electrical C3 columns** into
the live corpus for the 22 C3 cases, wire the `ControlPlausibilityState` producer and the EF/SF
consumer gating into the shim, run the full corpus, verify `top3_family` rises to **228/294** with
**0 regressions**, and mint the new yardstick **`V3_YARDSTICK_2026-07-05-C3B`** (same-day second
mint — suffix avoids overwriting the C2B ruler; both stay immutable).
### Progressive-disclosure role — the COMMIT step (ships ONLY what C3A simulated) ###
C3A sized this commit; nothing unsimulated ships:
1. **Scenario 1 config committed (Δλ DROPPED):** Scenario 1 (electrical-only) banks the same 16 as
   Scenario 2 with 0 regressions, so the two Δλ columns (`gas_obd_lambda_delta`,
   `lambda_perception_delta`) — the expensive two-point 5-gas ask and the weakest-grounded
   (empirical-anecdotal) threshold — are **deferred, not committed**.
2. **The +0.10 boost ships as simulated.** The 2 separable-but-short cases (`CSV-125`, `CSV-126`)
   stay short — a stronger lift was NOT simulated and belongs to `T-V3-P4-C3C` (forward-registered),
   never folded into this diff.
3. **Abstain dial untouched:** 12 of the 16 flips stay masked at MARGIN=0.02 — they still bank
   `top3_family` (the pack metric); surfacing them is an abstain-cal decision, not this commit's.
### Data gate (provisional synthetic seed) ###
Consumes `v3/data/c3_synthetic_seed_2026-07-05.{csv,json}` (`synthetic=true`; grounding tags carried
into provenance). The 4 stay-abstained cases' seed values (below every gate) are written too — they
are honest data and must keep emitting producer `ABSTAIN`. Non-C3 cases (272) stay empty (None).
### Success criteria ###
1. **Corpus updated:** `cases_petrol_v7.csv` gains 4 columns — `koeo_map_baro_delta_kpa`,
   `module_voltage_loaded_v`, `dlc_signal_ground_drop_v`, `bidirectional_fuel_response_ok_bool` —
   populated for the 22 C3 cases from the seed; all other rows empty.
2. **Schemas & ingestion:** fields added to the OBD payload model (`comlab/schemas/ingestion.py`),
   mapped through `wired/composition.py` and `v7/load_corpus.py` (mirror the C2B pattern).
3. **Producer & consumer in the shim:** `integration_shim.py` registers the 4 columns and computes
   `ControlPlausibilityState` with the **Scenario 1 gates exactly as simulated** —
   lean-bias `dlc_signal_ground_drop_v > 0.20`; rich-bias `koeo_map_baro_delta_kpa >= 5.0`;
   processor `bidirectional_fuel_response_ok_bool == False AND module_voltage_loaded_v < 12.0`;
   any → `CONTROL_REFERENCE_FAULT`, none → no state. On the state: boost EF-001/EF-002/EF-003
   (+0.10 DEFINITIVE), prune SF-001/SF-002. **No registry JSON edits** (shim logic only, like C2B).
4. **Rescore & verification:** scorer on the new corpus reports `top3_family` **228/294 (77.55%)**,
   abstained **84**, coverage **210/294 (71.43%)**, `top3_on_covered` **168/210 (80.00%)**, and
   `diff` vs `POST_T_V3_P4_C2B` shows **16 newly_pass / 0 newly_fail / REGRESSIONS: (empty)**.
   Any deviation from the C3A-simulated numbers is surfaced, not reconciled away.
5. **Yardstick minted:** `V3_YARDSTICK_2026-07-05-C3B` bound in `score_v3_yardstick.py` (new csv
   hash; oracle unchanged `3088a7c3…`; `run_suite.py` untouched); record written to
   `v3/reports/V3_YARDSTICK_2026-07-05-C3B.md`; `Hash lock: ok` with no overrides. Prior yardsticks
   untouched.
6. **Inner loop clean:** `py_compile`+`ruff`+`pyright` on touched files; `pytest apps/wired/v7/tests/`
   green (add a shim unit test for the 3 sub-gates + the ABSTAIN path, incl. one stay-abstained case).
### Context ###
- Commit sizing (gates, boost, column decision, expected numbers): `v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.{md,json}` §2/§3/§6.
- Consumer/FT-8 map: `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.json`.
- Wiring pattern to mirror (READ-NARROW): the C2B diff — `integration_shim.py` C2 state/dispatch,
  `ingestion.py` C2 fields, `composition.py`/`load_corpus.py` C2 mappings, and
  `v3/reports/V3_YARDSTICK_2026-07-05.md` (mint format).
- Baseline: `POST_T_V3_P4_C2B` / `V3_YARDSTICK_2026-07-05` (csv `3df2e8cb…`). **If anything committed
  after C3A, STOP and re-run the C3A sim on the new baseline before this diff** (stale-baseline rule).
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** `CONTROL_REFERENCE_FAULT` is read by the EF-001/EF-002/EF-003 boost + SF-001/SF-002
  prune branch this task adds.
- **Code path:** `labs/comlab/registry/integration_shim.py::_score_rule` (state emit + gate), fed by
  the 4 columns via `load_corpus.py` → `composition.py` → `ingestion.py` payload. Each mapped field
  carries a `# consumer:` comment naming this branch. No orphan: all 4 columns feed the state; the
  deferred Δλ columns are NOT added anywhere.
### Deliverables ###
1. `apps/wired/v7/data/cases_petrol_v7.csv` — MODIFY. 4 C3 columns, 22 cases filled.
2. `labs/comlab/comlab/schemas/ingestion.py` — MODIFY. Payload fields.
3. `apps/wired/wired/composition.py` — MODIFY. Map inputs → payload.
4. `apps/wired/v7/load_corpus.py` — MODIFY. CSV → raw inputs.
5. `labs/comlab/registry/integration_shim.py` — MODIFY. State emit + EF boost / SF prune + dispatch.
6. `apps/wired/fl_tasks/score_v3_yardstick.py` + `v3/reports/V3_YARDSTICK_2026-07-05-C3B.md` —
   MODIFY/CREATE. Mint + rebind.
### Files to touch ###
The six above, plus `apps/wired/v7/tests/` (ADD shim unit test) and
`v3/v3_tasks/progress_notes/T-V3-P4-C3B.md` (CREATE).
### Out of scope ###
**No Δλ columns** (deferred — the C3A-disclosed decision). **No stronger lift for CSV-125/126**
(that is `T-V3-P4-C3C`, sim-first). **No registry JSON edits. No abstain-dial change (MARGIN=0.02).
No oracle/scorer(`run_suite.py`) edit.** The 4 stay-abstained cases must not be nudged into passing.
Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph rebuild. Run JSON stays untracked. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m pytest apps/wired/v7/tests/
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C2B/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json
```
Gate: `top3_family = 228/294`, coverage `210/294`, `top3_on_covered = 80.00%`, `Hash lock: ok`
(on `V3_YARDSTICK_2026-07-05-C3B`), `16 newly_pass / 0 newly_fail`, `REGRESSIONS: (empty)`.
### Progress hook ###
PROGRESS.md `T-V3-P4-C3B`: Status=done, Files changed=~8, Verification="C3 commit: 4 electrical
columns + ControlPlausibilityState + EF boost/SF prune; top3_family 212→228 (+16); REGRESSIONS
empty; V3_YARDSTICK_2026-07-05-C3B minted; Δλ deferred; CSV-125/126 + 4 stay-abstained honest".
### Depends on ###
`T-V3-P4-C3A` done ✓ (sized this commit; FT-8 clean ✓). Owner go given. **Unblocks the C6 pack**
(next in the pinned sequence) and forward-registers `T-V3-P4-C3C` (CSV-125/126 lift, sim-first).
