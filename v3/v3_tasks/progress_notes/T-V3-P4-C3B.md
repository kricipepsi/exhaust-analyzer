# T-V3-P4-C3B — progress note

**Task:** C3 ECU/control-system signal-pack commit.  
**Date:** 2026-07-05 · **Coder:** Codex · **Mode:** STRICT (dual-gate)

## What shipped

- `apps/wired/v7/data/cases_petrol_v7.csv` — Added 4 C3 electrical columns (`koeo_map_baro_delta_kpa`, `module_voltage_loaded_v`, `dlc_signal_ground_drop_v`, `bidirectional_fuel_response_ok_bool`) and populated the 22 C3 cases from `v3/data/c3_synthetic_seed_2026-07-05.csv`; all non-C3 rows remain blank for those columns.
- `labs/comlab/comlab/schemas/ingestion.py` — Added the 4 fields to `OBDLiveDataPayload` with named `CONTROL_REFERENCE_FAULT` consumer comments.
- `apps/wired/wired/composition.py` — Mapped C3 raw OBD inputs into the COMLab OBD payload mirror.
- `apps/wired/v7/load_corpus.py` — Mapped the 4 C3 CSV columns into `raw_inputs["obd"]` and made them activate the OBD payload for C3 rows.
- `labs/comlab/registry/integration_shim.py` — Added `_PID_DISPATCH` entries, `ControlPlausibilityState`, Scenario-1 producer gates, EF-001/002/003 `+0.10` boost, and SF-001/SF-002 prune.
- `apps/wired/fl_tasks/score_v3_yardstick.py` — Minted/rebound active yardstick to `V3_YARDSTICK_2026-07-05-C3B` with CSV SHA-256 `9f530695dc3cf5586c9248a2b9de2f474950170326dcf5f62c1aefc36683e283`.
- `apps/wired/v7/tests/test_c3_control_plausibility.py` — Added a shim unit test covering the lean-bias, rich-bias, processor, and stay-abstained/quiet paths plus EF boost/SF prune.
- `v3/reports/V3_YARDSTICK_2026-07-05-C3B.md` — New active C3B yardstick record.

## Findings surfaced

- **Score movement:** `top3_family` rose from **212/294** to **228/294** (`+16`) with `REGRESSIONS: (empty)`.
- **Coverage delta versus task estimate:** task expected `coverage=210/294`, `top3_on_covered=168/210`, `total_abstained=84`; live run measured `coverage=209/294`, `top3_on_covered=167/209`, `total_abstained=85`. This is surfaced in `v3/reports/V3_YARDSTICK_2026-07-05-C3B.md`, not reconciled away.
- **Observed abstain change:** five cases became margin-abstained versus `POST_T_V3_P4_C2B`: `CSV-123`, `CSV-124`, `EXP-N002`, `EXP-N004`, `case_013`. The C3 pack metric still lands exactly (`top3_family +16`, zero regressions).
- **Deferred fields:** `gas_obd_lambda_delta` and `lambda_perception_delta` were not added to the corpus header; Δλ remains deferred per C3A Scenario-1 sizing.

---

## VERIFICATION GATE — T-V3-P4-C3B
1. Compile : PASS  (`py_compile` clean on `score_v3_yardstick.py`, `composition.py`, `load_corpus.py`, `ingestion.py`, `integration_shim.py`, `test_c3_control_plausibility.py`)
2. Lint    : PASS  (`ruff check` clean on the touched code paths and new test)
3. Types   : PASS  (`pyright` clean on touched paths under `apps/wired` config; root invocation has the known import-discovery gotcha)
4. Tests   : PASS  (`pytest apps/wired/v7/tests/` -> 26 passed; C3 shim test -> 5 passed)
5. Contract: PASS  (`score` reports `top3_family=228/294`, `Hash lock: ok`; `diff` vs `POST_T_V3_P4_C2B` reports `newly_pass=16`, `newly_fail=0`, `REGRESSIONS: (empty)`; measured coverage delta surfaced: `209/294`, not expected `210/294`)
6. Orphan  : PASS  (`CONTROL_REFERENCE_FAULT` grep confirms the 4 fields flow through `load_corpus.py` -> `composition.py` -> `ingestion.py` -> `_PID_DISPATCH` and are read by `_control_plausibility_state` / `_score_rule` EF boost + SF prune branch)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C3B
Scope         : PASS  (changes trace to the C3B deliverables; no Δλ columns, no stronger CSV-125/126 lift, no registry JSON edits, no abstain dial edit)
Composition   : PASS  (wired remains a mapper; diagnostic scoring stays in COMLab registry shim; no lab-to-lab imports)
Consumers     : PASS  (all 4 mapped fields name and feed the `CONTROL_REFERENCE_FAULT` consumer branch)
Literals      : PASS  (Scenario-1 gate literals are the task-pinned C3A simulation values: `0.20`, `5.0`, `12.0`, `+0.10`)
Docstrings    : PASS  (`ControlPlausibilityState`, `_control_plausibility_state`, and the new test helpers are documented)
Craft (WARN)  : Depth — C3 logic is isolated to one small shim producer plus the existing `_score_rule` override seam. Deletion — no leftover corpus-edit scaffold; `v3/apply_c3b_corpus.py` removed after the CSV was updated. Seam — mapping remains in `load_corpus.py`/`composition.py`; scoring remains in `integration_shim.py`. Interface — tests exercise the shim seam directly and the full corpus through the public scoreboard.
Result: CLEAN

## Guardrails honoured

`run_suite.py` frozen/untouched · `V3_YARDSTICK_2026-07-05-C3B` minted without overwriting prior yardsticks · `Vault/` untouched · no `graphify`/graph rebuild · no secrets · run JSON stays under ignored `apps/wired/v7/runs/` · owner commits by explicit path.
