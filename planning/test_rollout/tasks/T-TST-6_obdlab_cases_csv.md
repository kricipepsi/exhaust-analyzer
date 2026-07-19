# T-TST-6 — Derive obdlab_cases.csv from the reconciled master

**Status:** `authored` · impl blocked · **Blocked by:** `T-MASTER-RECON`, `T-TST-2` (done) ·
**Pack:** `planning/test_rollout/` · **Mode:** STRICT
**Load skills (session start):** read `TEST_ROLLOUT_START_HERE.md`; sandbox Python 3.14; mandatory pair +
`_skills/codingskills/ecc-subset/python-testing`.

## Goal

Project the reconciled `cases_petrol_master_v6.csv` into `labs/obdlab/tests/fixtures/obdlab_cases.csv`:
**OBD-consumed columns × OBD-decidable rows**, per `PROJECTION_CONTRACT.md` (OBDLab section). This is the
data fixture the bounce harness (`T-TST-8`) consumes; without it `T-TST-8` cannot run.

## Files

- **Create:** `labs/obdlab/tests/fixtures/obdlab_cases.csv`.
- **Read-only inputs:** the reconciled master (post `T-MASTER-RECON`) + `PROJECTION_CONTRACT.md` OBDLab rules.

## Scope (from PROJECTION_CONTRACT — OBDLab)

- **Consumed input columns:** `engine_rpm`, `coolant_temp_c`, `calculated_engine_load_pct`,
  `mass_airflow_gps`, `manifold_vacuum_kpa`, `shrtft1/2`, `longft1/2`, `number_of_banks`, `has_maf`, `has_map`.
- **Consumed expected columns:** `expected_obd_lambda`, `expected_ve_pct`, `expected_ve_validity`,
  `expected_trim_analytics_gate`, `expected_maf_status`, `expected_map_status`, `expected_o2_failure_mode`.
- **Row predicate:** OBD-decidable rows only (warmed engine, valid telemetry; OBD anomaly set or normal-with-
  telemetry). Use the `lab_decidability`/`perception_gap` column from `T-MASTER-RECON` — do not re-derive.

## Success criteria

1. Every row is OBD-decidable per the reconciled master's classification (no perception-gap/fusion-only rows).
2. Expected cells trace to a live `obdlab` source + wiki section in `gt_source`; uncited → `gt_method=characterization`.
3. Shared input columns are byte-consistent with the master (projection, not re-authoring).
4. The CSV loads in `conftest.py` and `test_cases.py` collects over it without error.

## Out of scope

The relabel itself (`T-MASTER-RECON`). The descriptor/generators/bounce gate (`T-TST-8`). Any obdlab code change.

## Signal/noise consumer

`obdlab_cases.csv` is consumed by `T-TST-8` Mode A1 (decision-rate floor on signal-bearing rows) and
`test_cases.py`. Columns with no consumer in those do not ship.

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-TST-6.md`, opening with `## Plan`.)
