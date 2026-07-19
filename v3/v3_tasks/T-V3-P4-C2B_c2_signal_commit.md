### Goal ###
Commit the C2 **signal pack** (rich_mixture vs catalyst_failure). Write the C2 columns into the live corpus, wire the producer logic into composition/registry, adjust the RM/CF consumer rules, run the full corpus, verify that `top3_family` rises to **212/294** (with 0 regressions), and mint the new **V3_YARDSTICK_2026-07-05** yardstick.

### Progressive-disclosure role — the COMMIT step ###
This task integrates the C2 logic simulated in `T-V3-P4-C2A` into the live engine and corpus:
1. **Corpus modification:** Append the C2 columns to the live CSV and fill them for the 22 target cases using the synthetic seed data from `T-V3-P4-C2-SYNTH`.
2. **Producer/Consumer wiring:** Map the new columns through the ingestion schemas and the composition layer into the integration shim. Implement the C2 state logic and rule boosts/pruning inside the registry shim's `_score_rule` function.
3. **Score movement:** This commit officially moves the yardstick score from 197/294 to 212/294 on the new schema. Since the corpus changes, a new yardstick must be minted and bound.

### Data gate (provisional synthetic seed) ###
Consumes the **synthetic C2 seed from `T-V3-P4-C2-SYNTH`** (grounded in `cluster2_values.md`, `synthetic=true`, evidence-tier `anecdotal`). Non-C2 cases in the corpus are filled with empty values (None).

### Success criteria ###
1. **Corpus updated:** `cases_petrol_v7.csv` has 9 new columns appended: `mode06_catalyst_margin_pct`, `catalyst_index_ratio`, `stft_idle_pct`, `ltft_idle_pct`, `stft_2500_pct`, `ltft_2500_pct`, `pre_post_cat_hc_delta_ppm`, `pre_post_cat_co_delta_pct`, and `decel_co_pct`. All 22 C2 cases are populated with their seed values, and the other 272 cases are left empty.
2. **Schemas & Ingestion:** `comlab/schemas/ingestion.py` has the fields added to `GasLabPayload` and `OBDLiveDataPayload`. `wired/composition.py` and `v7/load_corpus.py` map these fields from raw inputs to the payloads.
3. **Producer & Consumer implemented:** `integration_shim.py` has C2 columns registered in `_PID_DISPATCH` and the state emit + RM/CF boost/pruning logic fully integrated in `_score_rule`. RM-001/003/004 and CF-001/002/006/007 are gated and boosted when C2 data is present.
4. **Rescore & Verification:** Running the scorer on the new corpus reports:
   - `top3_family` rises to **212/294** (72.11%)
   - `coverage` is **72.79%** (214/294)
   - `top3_on_covered` is **76.64%** (164/214)
   - **0 regressions** on the full 294-case corpus compared to `POST_T_V3_3D`.
5. **Yardstick minted:** A new yardstick named **V3_YARDSTICK_2026-07-05** is minted in `score_v3_yardstick.py`, written to `v3/reports/V3_YARDSTICK_2026-07-05.md`, and bound to the scoreboard so runs pass with `Hash lock: ok` and no overrides.
6. **Inner loop clean:** `py_compile`, `ruff`, `pyright`, and `pytest apps/wired/v7/tests/` are clean across the touched code paths.

### Deliverables ###
1. `apps/wired/v7/data/cases_petrol_v7.csv` — MODIFY. Add C2 columns and values.
2. `labs/comlab/comlab/schemas/ingestion.py` — MODIFY. Add fields to payload models.
3. `apps/wired/wired/composition.py` — MODIFY. Map new inputs into payloads.
4. `apps/wired/v7/load_corpus.py` — MODIFY. Map CSV columns to raw inputs.
5. `labs/comlab/registry/integration_shim.py` — MODIFY. Integrate C2 columns and scoring logic.
6. `apps/wired/fl_tasks/score_v3_yardstick.py` — MODIFY. Mint and rebind V3_YARDSTICK_2026-07-05.
7. `v3/reports/V3_YARDSTICK_2026-07-05.md` — CREATE. New active yardstick record.
8. `v3/v3_tasks/progress_notes/T-V3-P4-C2B.md` — CREATE. Progress note.

### Out of scope ###
No engine change outside the integration shim. No registry JSON edits. No change to the scoring window (MARGIN=0.02). Writes only to files listed. No secrets.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m pytest apps/wired/v7/tests/
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_P4_C2B/results.json
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_3D/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C2B/results.json
```
Gate: Scorer reports `top3_family = 212/294`, `coverage = 72.79%`, `top3_on_covered = 76.64%`, `Hash lock: ok`, and `REGRESSIONS: (empty)`.
