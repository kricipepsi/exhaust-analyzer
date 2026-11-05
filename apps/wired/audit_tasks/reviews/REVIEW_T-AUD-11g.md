# REVIEW T-AUD-11g — ACCEPT, score 95 (Windows Cowork, 2026-11-05 22:42 CET)

Facts first: commit `e3d6a8f` on `fix/T-AUD-11g` (after spec `8a81707`) changes only
`audit/drift/2026-11-05_DRIFT_REPORT_comlab.md`. Cowork re-run of `check_report.py`: `sections 8/8, findings 73,
refs ok 126/126`, `REPORT OK` (exit 0). Porcelain: note and RESULT only. Headless run 21:23:35-21:37:17 UTC, exit 0.
Docs row: no second-model review.

## Findings re-derived (73; the behaviour claims checked directly, none rejected)
- **Fatal gates off in production** (PRD:228, HLD:233): `composition.py:108` `enable_fatal_gates: bool = False`; the
  public UI calls `diagnose(raw_inputs)` (`apps/ui/app.py:948`); only the yardstick and suite scripts pass `True`, and
  only for `invalid`-tagged cases. So ERR-ABORT-001/004/005 never fire for a user. `audit/FINDINGS.md` and
  `FIX_PLAN.md` do not mention it. **A product defect or an unrecorded decision: new row T-AUD-19.**
- ERR-ABORT-001 lets `BORDERLINE` through (`lab_pipeline_aggregator.py:370`); PRD:234 and HLD:234 say `!= VALID`.
- Catalyst-damage override `^P030[0-8]$` (`fault_atlas_router.py:72`); HLD:299 says `P030[0-9]`.
- `_map_degradation` (`:194-198`) returns only FULL_FUSION or GAS_DOMINANT; `SINGLE_POINT` is in `DegradationLit`
  (`response.py:26`) but never set (HLD:306, BDD:260).
- `run_fallback_tree` raises `NotImplementedError` past the non-starter and suppressed-GASLab paths (`:674-682`);
  HLD:553 and SEMANTIC_CONTRACT:301 describe it as the directive's consumer.
- Siblings get `fault_name=sibling_id` (`fault_atlas_router.py:1854`); HLD:426 says the sibling's name.
- The rest (LLD class and signature listings, DLD budgets and missing logging/orjson/exit-78 boot, CROSS_LAB "pending"
  rows already built, SEMANTIC_CONTRACT field shapes) rest on their quoted lines or ABSENT commands.

## Drift groups (for T-AUD-18)
1. Gate contract: order, input paths (`metadata.*` vs `vehicle_dna.*`), BORDERLINE, remediation texts, 70 vs 75 °C
   (same split as T-AUD-17), abort shape (`fault_code` in a full output vs an error union).
2. Degradation modes: SINGLE_POINT and GAS_DOMINANT rules; `run_fallback_tree` phase-3 stub.
3. LLD listings that no longer match: request/response models, `schema_version`, aggregator signature, KG loader API
   and errors, registry schema, routing-tag counts (17 vs 16/19), abstain fields.
4. DLD operations promised and absent: structured logging, orjson, exit 78, `run_orchestrator`, `build_validate.py`,
   size budgets.
5. CROSS_LAB_DEPENDENCIES: four consumers marked pending that exist; a stale line cite.
6. SEMANTIC_CONTRACT mirrors: `metadata` vs `vehicle_dna`, missing `secondary_air_equipped`, `reading_high`, Mode $06 shape.
7. Small: DTC regex hex, P0309, sibling `fault_name`, KG path name, HORIZON_MODERN window.

## Score
100 − 3 (`## Time` one phase) − 2 (two DLD size-budget findings judge a commitment document by `du`) = 95.

## Follow-up
- T-AUD-18: COMLab docs drift fixes (groups 1-7), rulings first on group 1 (BORDERLINE, 70/75) and group 2.
- T-AUD-19: the public app runs `diagnose()` with `enable_fatal_gates=False`. Rule whether users get the Stage A
  aborts (invalid sample, VIN NONE, schema), then fix the default or record the decision in the HLD.

Measured: COMLab core (263 KB docs, 6,674 code lines) → 73 findings in 14 min on Sonnet medium.
