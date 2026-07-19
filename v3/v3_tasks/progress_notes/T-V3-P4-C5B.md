# Progress note — T-V3-P4-C5B

**Task:** [[T-V3-P4-C5B_c5_signal_commit]]  
**Date:** 2026-07-06  
**Mode:** STRICT C5 signal-pack COMMIT

## Scope confirmation

Implemented the C5 lean-root-cause commit: pre-flighted `s_commit` (5 WOULD_BANK vacuum leak cases: `EXP-N011, EXP-N022, EXP-N029, case_003, case_016`), added 5 new C5 columns to the petrol corpus (`stft_load_pct, ltft_load_pct, calc_load_wot_pct, fuel_rail_pressure_load_kpa, wideband_lambda_wot`), populated all 11 columns for the 10 C5 rows from the seed JSON (including EGR healthy lookalike cases and correct None-value handling), mapped fields through the wired OBD payload chain, added `LeanRootCauseState` StrEnum + producer helper `_lean_root_cause_state` in the registry shim, applied LC/VL rule boosts under the C3 precedence and C5/C6 MAF-collision rules, added focused v7 shim tests, minted `[[V3_YARDSTICK_2026-07-06-C5B]]`, and rebound the active scorer to it. Out of scope remained untouched: no NF prunes, registry JSON, `run_suite.py`, C3 thresholds, abstain margin, `Vault/`, and graphify.

## Implementation notes

- `apps/wired/v7/data/cases_petrol_v7.csv`: added 5 columns and populated exactly 10 C5 rows across all 11 contract columns from `v3/data/c5_synthetic_seed_2026-07-06.json`; all non-C5 rows remain blank on new columns and preserved on existing columns.
- `labs/comlab/comlab/schemas/ingestion.py`, `apps/wired/wired/composition.py`, `apps/wired/v7/load_corpus.py`: added/mapped the 5 new C5 columns with named `LeanRootCauseState` consumers.
- `labs/comlab/registry/integration_shim.py`: added `LeanRootCauseState` StrEnum; decisive states are `VACUUM_LEAK_TRIM_PATTERN` (idle TFT >= 15 AND 2500 TFT <= 10 AND recovery delta >= 15), `FUEL_DELIVERY_SHORTFALL` (WOT lambda > 1.05 and rail pressure drop < 280 for port / < 12000 for DI), and `MAF_UNDERREAD` (WOT calc load < 80 and total load trim > 0). Decisive C5 boosts `LC-001/LC-002/LC-003/VL-001/VL-002/VL-003` by `+0.10`.
- **Precedence & Collision guards:** 
  - C3 control reference fault wins first (C5 boosts are bypassed if C3 is active).
  - C5 takes precedence over C6 when both are decisive (collision check: C6 block is skipped if C5 is decisive and C3 is inactive).
- `apps/wired/v7/tests/test_c5_lean_root_cause.py`: covers C5 emit paths, static/idle-only abstain no-op, None-column paths, EGR healthy lookalike no-op, C3 precedence, and C6 MAF-collision precedence.
- `apps/wired/fl_tasks/score_v3_yardstick.py`: active yardstick rebound to `V3_YARDSTICK_2026-07-06-C5B` with CSV hash `c49c17af1182a3eb07056a3fbf27c101378a32f35e375b18b3104d3928d8c7fd`; oracle hash remains `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127`; scorer hash unchanged.

## Pre-flight result

Command:

```bash
/agent_workspace/.venv-wired/bin/python v3/c5_signal_sim.py --scenario s_commit
```

Observed:

- Zero-overlay self-check: `OK (all 294 cases matched, drift = 0)`
- `S-COMMIT` WOULD_BANK = **5**
- `S-COMMIT` bank set equals S3 = **True**
- regressions = **0**
- no_fault-neighbour regressions = **0**
- EGR/Stay-abstained cases banked alarm = `[]`

## Score result

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json
```

Observed:

- Yardstick: `V3_YARDSTICK_2026-07-06-C5B`
- Hash lock: `ok`
- `top3_family` = **250/294 = 85.03 %** (expected **246/294**; see delta explanation below)
- coverage = **208/294 = 0.71**
- `top3_on_covered` = **179/208 = 86.06 %**
- total abstained = **86**
- single-verdict family+state = **147/294 = 50.00 %**

Diff command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json
```

Observed:

- newly_pass = **9** (expected **5**; see delta explanation below)
- newly_fail = **0**
- `REGRESSIONS: (empty)`
- per-family movement: `lean_condition +9`, all other families `+0`

### Delta Explanation (Scoreboard Disclosure)
The live run scored `top3_family 250/294` (9 newly_pass), whereas the task expected `246/294` (5 newly_pass). 
The additional +4 passes are: `era1_001, CSV-113, CSV-114, REAL-004`. These are the 4 EGR stuck open lookalike cases. In the baseline run (where C5 columns were empty), these 4 cases had empty trims, which allowed a false `CF-001` (catalyst failure) rule to outrank `lean_condition` in the top-3 window. Writing normal/healthy trims from the C5 seed caused the catalyst check in `integration_shim.py::_score_rule` to prune the false `CF-001` rule, allowing `lean_condition` to enter the top-3 window and pass, which is chemically and diagnostically correct.

## VERIFICATION GATE — T-V3-P4-C5B

1. Compile : PASS  (`py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py apps/wired/v7/tests/test_c5_lean_root_cause.py` -> OK)
2. Lint    : PASS  (`ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py apps/wired/v7/tests/test_c5_lean_root_cause.py` -> OK)
3. Types   : PASS  (temporary `pyrightconfig.json` extraPaths check -> 0 errors; registry local pyright -> 0 errors)
4. Tests   : PASS  (`/agent_workspace/.venv-wired/bin/python v3/c5_signal_sim.py --scenario s_commit` (pre-flight) -> 5 banked, set==S3, 0/0 regressions; `/agent_workspace/.venv-wired/bin/python -m pytest apps/wired/v7/tests/` -> 38 passed; score+diff commands above -> Hash lock ok, 9 newly_pass, 0 newly_fail)
5. Contract: PASS  (5 new C5 columns only; 10 C5 rows populated; non-C5 rows blank on new columns; `run_suite.py` untouched; registry JSON untouched; `V3_YARDSTICK_2026-07-06-C5B` minted)
6. Orphan  : PASS  (`LeanRootCauseState` fields grep-confirmed through `load_corpus.py` -> `composition.py` -> `ingestion.py` -> `integration_shim.py::_lean_root_cause_state` -> `_score_rule` LC/VL branch)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C5B

Scope         : PASS  (changed lines trace to C5B deliverables: pre-flight sim, CSV columns, payload mapping, shim producer/consumer, tests, yardstick, progress ledger)
Composition   : PASS  (`wired/` remains a composition seam; diagnostic scoring stays in COMLab shim; no cross-lab imports added; no deferred path; no `Vault/`; no graphify)
Consumers     : PASS  (every mapped field carries a named `registry integration_shim LeanRootCauseState` consumer; live reads are in `_lean_root_cause_state` and `_score_rule`)
Literals      : PASS  (`15.0`, `10.0`, `280.0`, `12000.0`, `80.0`, `1.05`, and `+0.10` are the task-pinned C5B/C5-PRE thresholds; the report ties them to `[[V3_C5_REVEAL_CONTRACT_2026-07-05]]` and `[[V3_C5_SIGNAL_DRYRUN_2026-07-06]]`)
Docstrings    : PASS  (new enum/helper/test helpers carry docstrings)
Craft (WARN)  : Depth: shim branch stays a thin producer/consumer override beside C2/C3/C6; no rule JSON mutation. Deletion test: all new fields are consumed today by the C5 branch; the five new columns also serve the live `LeanRootCauseState` branch and unblock later C4 reuse. Seam discipline: CSV -> loader -> composition -> ingestion -> shim is single-path; no duplicate mapping in runner/tests. Interface=test surface: public score/diff and v7 tests exercise the committed path; private shim tests pin branch edge cases.
Result: CLEAN

## Follow-on

C5B unblocks the C4 pack in the pinned sequence. The abstain-cal thread remains parked: C5B deliberately left `MARGIN=0.02` untouched, so all 5 of the C5 top-3 flips remain hidden by abstain behavior.
