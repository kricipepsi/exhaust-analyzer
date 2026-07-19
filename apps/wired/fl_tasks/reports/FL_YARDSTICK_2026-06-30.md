# FL_YARDSTICK_2026-06-30 — frozen v3 yardstick

**Task:** [[T-FL-1_lock_true_baseline]]  
**Date:** 2026-06-30  
**Mode:** read-only measurement; no engine/oracle/CSV/wiki/scorer edits.  
**Consumer:** [[T-FL-4_v3_scoreboard]] and v3 rebuild coders.  
**Baseline source:** existing run `apps/wired/v7/runs/20260630_163900/results.json`; re-scored from that JSON joined to `apps/wired/v7/data/cases_petrol_v7.csv`. I did **not** rerun the suite, to avoid minting a new run artefact when the task only needs a frozen yardstick.

## Frozen artefacts

| Artefact | Frozen value |
|---|---|
| Workspace commit at measurement | `fe3b827cfa4c80b099873a6c3c4b17833b50ae98` |
| Corpus + oracle CSV | `apps/wired/v7/data/cases_petrol_v7.csv` |
| CSV SHA-256 | `a94a7731bcc55a1ab826bdc46d5c9658d47dd86984902e3c93d7bab3be02a2ae` |
| Oracle subset SHA-256 | `a4de411098eb3c08d23d4881f4863fa1bd0a204cbb4041acb595474a1cecad7d` (`case_id`, `tag`, all `expected_*`, `accuracy_excluded`) |
| Scorer | `apps/wired/v7/run_suite.py` |
| Scorer SHA-256 | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |
| Source run JSON | `apps/wired/v7/runs/20260630_163900/results.json` |
| Run JSON SHA-256 | `d9069f8dea738de91654320b4f431b4345364ff27571f39cce2fd5b7fb210ee3` |
| Run command to reproduce v2 default | `cd /agent_workspace && /agent_workspace/.venv-wired/bin/python apps/wired/v7/run_suite.py` |
| Python | `/agent_workspace/.venv-wired/bin/python` = `Python 3.14.6` |
| `USE_V2_REGISTRY` | unset in measurement shell; COMLab default is v2 because `lab_pipeline_aggregator.py` resolves unset to `"1"` (`labs/comlab/comlab/core/lab_pipeline_aggregator.py:116-121`) |
| Trace | off; `--trace` not passed; `WIRED_OTEL` unset |
| Row count | 314 total = 294 accuracy (`tag=viable`) + 20 invalid; 20 rows have `accuracy_excluded=true` and are excluded from accuracy ratios |

**Yardstick rule:** v3 before/after scoring must use the exact CSV hash and scorer hash above. Any corpus/oracle edit creates a new yardstick file; this one is immutable historical baseline.

## Primary metric: family + state routing

Primary routing excludes the two surface dimensions from [[V7_ACCURACY_2026-06-30]] §4: `fault_code` namespace and `confidence` calibration. A case counts as routing-correct only when both independent routing dimensions pass:

- `fault_family == PASS`
- `state == PASS`

| Metric | As-pinned value |
|---|---:|
| Accuracy denominator | 294 |
| `fault_family` only | 141 / 294 = 47.96 % |
| `state` only | 275 / 294 = 93.54 % |
| **primary family+state routing** | **133 / 294 = 45.24 %** |
| Overall 6-dim conjunctive score | 0 / 294 = 0.00 % |

Why family+state is lower than the prior 48.0 % family-only number: 8 `no_fault` rows pass `fault_family` but fail `state` because the verdict still reports `is_fault_detected=true`; the primary yardstick treats that as a routing miss, not a healthy verdict.

## Surface dimensions reported separately

These are excluded from primary routing, but frozen because T-FL-4 must show their movement separately.

| Dimension | PASS | FAIL | Meaning |
|---|---:|---:|---|
| `fault_code` | 0 / 294 | 294 / 294 | namespace mismatch: engine emits short code (`MF-001`), oracle expects canonical KG id (`ERR-MF-001`) |
| `confidence` | 21 / 294 | 273 / 294 | engine confidence saturates above oracle mid-band windows |
| `perception_gap` | 194 / 294 | 100 / 294 | real mixed signal; not part of primary family+state yardstick |
| `demotion_note_contains` | 289 / 294 | 5 / 294 | text drift; not part of primary family+state yardstick |

## Per-family as-pinned family+state routing

| Family | Cases | family ✓ | state ✓ | family+state ✓ | family+state % |
|---|---:|---:|---:|---:|---:|
| `cam_timing` | 11 | 7 | 11 | 7 | 63.6 % |
| `catalyst_failure` | 23 | 9 | 22 | 9 | 39.1 % |
| `ecu_fault` | 31 | 4 | 31 | 4 | 12.9 % |
| `exhaust_leak` | 10 | 0 | 10 | 0 | 0.0 % |
| `ignition_fault` | 4 | 1 | 4 | 1 | 25.0 % |
| `lean_condition` | 62 | 37 | 62 | 37 | 59.7 % |
| `mechanical_wear` | 14 | 0 | 14 | 0 | 0.0 % |
| `misfire` | 54 | 46 | 54 | 46 | 85.2 % |
| `no_fault` | 18 | 8 | 0 | 0 | 0.0 % |
| `non_starter` | 5 | 0 | 5 | 0 | 0.0 % |
| `rich_mixture` | 37 | 23 | 37 | 23 | 62.2 % |
| `sensor_fault` | 25 | 6 | 25 | 6 | 24.0 % |
| **TOTAL** | **294** | **141** | **275** | **133** | **45.24 %** |

## ORACLE_SUSPECT adjudication

Only one V7_ACCURACY §5 cluster is tagged as possibly oracle-correct: `mechanical_wear → misfire` (10 cases). The wiki adjudication is **oracle-correct for primary family+state routing**: the engine's `misfire` family is defensible for these single-snapshot rows, and the v3 corpus should not count these 10 as engine family/state routing errors unless the input supplies the missing mechanical discriminator.

Evidence:

- COMWIKI-06 states `misfire` is combustion dropout and explicitly includes mechanical/compression causes; its discriminator is ignition vs fuelling vs mechanical plus localisation (`labs/comlab/wiki/06_fault_atlas_families.md:73-76`).
- COMWIKI-06 states `mechanical_wear` has **no distinct single-snapshot chemistry** and needs delta/freeze-frame levers (`labs/comlab/wiki/06_fault_atlas_families.md:101-104`).
- COMWIKI-05 maps `ERR-MF-006 low_compression_mechanical_misfire` to `misfire` on `IGNITION_MISFIRE / POA_SIGNATURE` (`labs/comlab/wiki/05_fault_taxonomy.md:82-88`).
- COMWIKI-05 defines `IGNITION_MISFIRE` as high HC, depressed CO2, elevated O2 (`labs/comlab/wiki/05_fault_taxonomy.md:109-114`), which matches the cluster's high-HC / depressed-CO2 / elevated-O2 rows.
- `mechanical_wear.json` says compression-loss mechanical wear can produce an ignition-misfire gas signature and that gas alone cannot distinguish compression loss from ignition failure (`labs/comlab/comlab/config/kg/mechanical_wear.json:155-171`).
- `misfire.json` has a canonical misfire node for low-compression mechanical misfire (`ERR-MF-006`) with ring/valve/bore impacted subsystems (`labs/comlab/comlab/config/kg/misfire.json:125-141`).

Caveat: the observed v2 winner is `MF-001` (classic ignition misfire), not `MF-006`; code-level specificity remains unresolved and is intentionally outside this primary routing yardstick because `fault_code` is a separately reported surface dimension.

| Cluster | Cases | Decision | Primary-yardstick effect | Wiki basis | Pending v3 corpus action |
|---|---:|---|---:|---|---|
| `mechanical_wear → misfire` | 10 | `oracle-correct` for family+state | +10 routed cases | COMWIKI-06 family collision + COMWIKI-05 `ERR-MF-006` + KG mechanical gas-alone ambiguity | `pending-for-v3`: repin these 10 rows to a misfire-family oracle or require a mechanical discriminator before scoring them as mechanical_wear |

Affected case IDs: `era1_002`, `era1_015`, `CSV-118`, `CSV-119`, `CSV-120`, `EXT-222`, `EXT-223`, `EXT-224`, `MECH-002`, `MECH-006`.

## As-pinned vs adjudicated routing

| Metric | Numerator / denominator | Percent |
|---|---:|---:|
| As-pinned primary family+state routing | 133 / 294 | 45.24 % |
| ORACLE_SUSPECT adjustment | +10 / 294 | +3.40 pp |
| **Adjudicated primary family+state routing** | **143 / 294** | **48.64 %** |

The adjudicated number is not a mutation of the CSV. It is a report-only correction for v3 planning and T-FL-4 delta reporting.

## Top as-pinned family misroute clusters

These remain engine/data failures for T-FL-3 unless later trace evidence marks a more specific failure mode.

| Expected | Predicted | Count |
|---|---|---:|
| `mechanical_wear` | `misfire` | 10 |
| `ecu_fault` | `lean_condition` | 10 |
| `catalyst_failure` | `lean_condition` | 8 |
| `lean_condition` | `misfire` | 7 |
| `rich_mixture` | `catalyst_failure` | 7 |
| `sensor_fault` | `no_fault` | 6 |
| `lean_condition` | `catalyst_failure` | 6 |
| `ecu_fault` | `rich_mixture` | 6 |
| `exhaust_leak` | `sensor_fault` | 6 |
| `lean_condition` | `sensor_fault` | 5 |
| `ecu_fault` | `sensor_fault` | 5 |
| `ecu_fault` | `catalyst_failure` | 5 |

## Pending-for-v3 oracle rows

| ID | Status | Action |
|---|---|---|
| `FL-V3-ORACLE-MW-MISFIRE` | `pending-for-v3` | Revisit the 10 `mechanical_wear → misfire` rows above. Either repin their family to `misfire` for a single-snapshot yardstick or enrich the corpus with compression/oil/coolant/delta evidence before scoring them as `mechanical_wear`. |
