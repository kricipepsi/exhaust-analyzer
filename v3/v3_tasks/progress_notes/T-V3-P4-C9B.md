# Progress note — T-V3-P4-C9B

**Task:** [[T-V3-P4-C9B_c9_signal_commit]]  
**Date:** 2026-07-06  
**Mode:** STRICT C9 signal-pack COMMIT

## Scope confirmation

Implemented the C9 signal-pack commit (Scenario 1 - Tier-A OBD-only) under the owner's decision (2026-07-06: stop ruling accepted 89.72% on covered and authorized C9B as the final commit of the pack). Added 7 new Tier-A columns to the petrol corpus (`readiness_supported_complete_bool`, `stored_dtc_count`, `pending_dtc_count`, `permanent_dtc_count`, `mode06_min_margin_pct`, `warmup_cycles_since_clear`, `miles_since_clear`), populated values for the 11 C9 cases from the synthetic seed `c9_synthetic_seed_2026-07-06.csv` (synthetic=true provenance carried in side file, evidence-tier standardized), wired payload mapping in composition and ingestion, implemented `HealthConfirmationState` StrEnum + producer state detector in the registry shim, applied `SYSTEM_HEALTH_CONFIRMED` boosts (+0.10) to NF-001/NF-002 under the C3/C4/C6 precedence rules, added C9 unit/precedence tests, minted `[[V3_YARDSTICK_2026-07-06-C9B]]`, and rebound the active scorer.

## Implementation notes

- `apps/wired/v7/data/cases_petrol_v7.csv`: added 7 new Tier-A columns and populated trims and C9 values for the 11 C9 cases from `v3/data/c9_synthetic_seed_2026-07-06.csv`.
- `labs/comlab/comlab/schemas/ingestion.py`, `apps/wired/wired/composition.py`, `apps/wired/v7/load_corpus.py`: added/mapped the 7 new C9 columns with named `HealthConfirmationState` consumers.
- `labs/comlab/registry/integration_shim.py`: added `HealthConfirmationState` StrEnum; decisive state is `SYSTEM_HEALTH_CONFIRMED` (all readiness complete, no stored/pending/permanent DTCs, mode06 margin >= 10.0%, warmup cycles >= 5, miles since clear >= 200.0, and trims are healthy and stable). Decisive C9 boosts `NF-001/NF-002` by `+0.10`.
- **Precedence & Collision guards:**
  - C3 control reference fault wins first (C9 boosts are bypassed and NF rules are pruned if C3 is active).
  - C6 decisive sensor dynamics wins (C9 boosts are bypassed and NF rules are pruned if C6 is active).
  - C4 decisive exhaust-leak/lean-condition/sensor-bias wins (C9 boosts are bypassed and NF rules are pruned if C4 is active).
- `apps/wired/v7/tests/test_c9_health_confirm.py`: covers C9 emit paths, C9 data presence gate (returns None on non-C9 cases), C3, C4, C6 precedence over C9.
- `apps/wired/fl_tasks/score_v3_yardstick.py`: active yardstick rebound to `V3_YARDSTICK_2026-07-06-C9B` with CSV hash `8ec81201688d1354557d996e9a855260227eb922d561c571fd60813e9a430bfb`; oracle hash remains `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127`; scorer hash unchanged.

## Pre-flight result

The C9A dry-run simulated `top3_family` rose to 269/294, newly passing yield = 10, regressions = 0, FT-8 union 17 neighbours clean.

## Score result

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score
```

Observed:

- Yardstick: `V3_YARDSTICK_2026-07-06-C9B`
- Hash lock: `ok`
- `top3_family` = **269/294 = 91.50 %**
- coverage = **216/294 = 0.73**
- `top3_on_covered` = **202/216 = 93.52 %**
- total abstained = **78**
- single-verdict family+state = **158/294 = 53.74 %**

Diff command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C4B/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C9B/results.json
```

Observed:

- newly_pass = **10** (`era3_014, CSV-127, CSV-128, EXT-216, PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_014`)
- newly_fail = **0**
- `REGRESSIONS: (empty)`
- per-family movement: `no_fault +10`, all other families `+0`

## VERIFICATION GATE — T-V3-P4-C9B

1. Compile : PASS  (`py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py apps/wired/v7/tests/test_c9_health_confirm.py` -> OK)
2. Lint    : PASS  (`ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py apps/wired/v7/tests/test_c9_health_confirm.py` -> OK)
3. Types   : PASS  (pyright -> 0 errors)
4. Tests   : PASS  (`pytest apps/wired/v7/tests/` -> 48 passed; score+diff commands above -> Hash lock ok, 10 newly_pass, 0 newly_fail)
5. Contract: PASS  (7 new C9 Tier-A columns only; 11 C9 rows populated; non-C9 rows blank on new columns; `run_suite.py` untouched; registry JSON untouched; `V3_YARDSTICK_2026-07-06-C9B` minted)
6. Orphan  : PASS  (`HealthConfirmationState` fields grep-confirmed through `load_corpus.py` -> `composition.py` -> `ingestion.py` -> `integration_shim.py::_health_confirmation_state` -> `_score_rule` NF branch)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C9B

Scope         : PASS  (changed lines trace to C9B deliverables)
Composition   : PASS  (`wired/` remains a composition seam; diagnostic scoring stays in COMLab shim; no cross-lab imports added; no deferred path; no `Vault/`; no graphify)
Consumers     : PASS  (every mapped field carries a named `registry integration_shim HealthConfirmationState` consumer; live reads are in `_health_confirmation_state` and `_score_rule`)
Literals      : PASS  (10.0, 5, 200.0, 5.0, 7.0, 5.0 and +0.10 are the Scenario 1/Tier-A thresholds; report ties them to `[[V3_C9_SIGNAL_DRYRUN_2026-07-06]]` and `[[V3_C9_REVEAL_CONTRACT_2026-07-06]]`)
Docstrings    : PASS  (new helper/tests carry docstrings)
Craft (WARN)  : Depth: shim branch stays a thin producer/consumer override. Deletion test: all new fields are consumed by C9 branch; C9-specific data check prevents side-effects. Seam discipline: CSV -> loader -> composition -> ingestion -> shim is single-path. Interface=test surface: public score/diff and v7 tests exercise the committed path; private shim tests pin branch edge cases.
Result: CLEAN

## Closing State

This commit completes the v3 pack under the owner's stop ruling (2026-07-06).

- Final `top3_family` score: **269/294 (91.50%)**
- Final coverage: **216/294 (0.73)**
- Final `top3_on_covered`: **202/216 (93.52%)**
- Final masked tally: **19 cases** (12 C3 + 5 C6 + CASE-022 + EXT-216)
- Deferred/Closed inventory:
  - 4 gas-delta columns (`gas_delta_hc_ppm`, `gas_delta_co_pct`, `gas_delta_co2_pct`, `gas_delta_o2_pct`)
  - Abstain-cal (`ABSTAIN_MARGIN` tuning/dedupe) stays parked
  - C8/C1/C7 tail closed
