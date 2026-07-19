# Graph-Trust Audit — obdlab (claude)

## Plan
Picked row **T-GTA-OBD·claude** (pending, owner=claude, no blockers) from
`GRAPH_TRUST_PROGRESS.md`. I audit `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml`
read-only: classify every framed `implements` / `consumers` / `drift_guards` edge as
LIVE / MISLABEL / ORPHAN / PENDING per `GRAPH_TRUST_AUDIT.md`, with `file:line` evidence,
resolving each comlab consumer against the actual reader in `labs/comlab/comlab/`. obdlab
has no obdlab-specific seeded case, but I carry the cross-lab nuance (a reader exercised
only by unit tests pre-wire is LIVE, not ORPHAN). I write only this file
(`reports/obdlab__claude.md`) and touch no map, note, code, or graph.

---

## Counts (62 edges)
**56 LIVE · 4 MISLABEL · 2 ORPHAN · 0 PENDING**

- LIVE: 35 doc-note edges + 21 wiki-note edges (7 implements + 7 drift_guards + 7 consumer).
- MISLABEL: 4 wiki consumer edges (delta-relations→power_loss, delta-relations→perception,
  taxonomy→symptom_router, truth-perception→symptom_router).
- ORPHAN: 2 wiki consumer edges (pids-protocol→fault_atlas_kg, taxonomy→fault_atlas_kg).
- PENDING: none (no `(pending …)` markers in this map).

## Path-resolution note (NOT a defect)
The map's `implements`/`drift_guards` use **vault-relative** paths
(`labs/obdlab/code/core/X.py`, `labs/obdlab/tests/...`). Per the map header and
`build_lab_vault.py`, `code/` is the in-vault copy of the repo's `<lab>/<lab>/` tree, so
`labs/obdlab/code/core/ve_engine.py` resolves to repo `labs/obdlab/obdlab/core/ve_engine.py`.
All 12 implements code files and all test files exist in the repo under that mapping —
classified LIVE. (Tests aren't renamed by the build, so they `test -f` directly.)

## Seeded-case fidelity
obdlab has no lab-specific seeded case. The cross-lab crux **is** respected: every LIVE
consumer here (perception_contradiction, ecu_hardware_checker, lab_pipeline_aggregator) is
exercised by a unit test and not yet called by a built pipeline — correctly LIVE, **not**
ORPHAN (unwired ≠ orphan). My 2 ORPHANs are ORPHAN because the **named file reads zero of
the field** (fault_atlas_kg is a pure KG JSON loader), exactly parallel to the seeded
`power_loss_analytics` 0-DTC-refs case — not because they are unwired.

---

## Classification table

### Doc notes (35 edges — all LIVE)
| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| PRD_OBDLab.md | consumer → HLD_OBDLab.md | LIVE | `labs/obdlab/docs/HLD_OBDLab.md` exists | — |
| HLD_OBDLab.md | consumer → LLD_OBDLab.md | LIVE | `labs/obdlab/docs/LLD_OBDLab.md` exists | — |
| HLD_OBDLab.md | consumer → DLD_OBDLab.md | LIVE | `labs/obdlab/docs/DLD_OBDLab.md` exists | — |
| LLD_OBDLab.md | implements ve_engine / o2_normalizer / trim_vector_aggregator (×3) | LIVE | `labs/obdlab/obdlab/core/{ve_engine,o2_normalizer,trim_vector_aggregator}.py` exist | — |
| LLD_OBDLab.md | consumer → DLD_OBDLab.md | LIVE | DLD exists | — |
| LLD_OBDLab.md | drift_guards test_{ve_engine,o2_normalizer,trim_vector_aggregator} (×3) | LIVE | `labs/obdlab/tests/unit/test_*.py` exist | — |
| DLD_OBDLab.md | implements (×12 core+schemas) | LIVE | all 12 resolve under `labs/obdlab/obdlab/{core,schemas}/` | — |
| DLD_OBDLab.md | consumer → comlab fault_atlas fusion (perception channel) | LIVE | perception channel real: `perception_contradiction.py:127` + `fault_atlas_router.py` | — (coarse doc edge) |
| DLD_OBDLab.md | drift_guards (×12 unit + integration smoke) | LIVE | all 12 test files exist incl. `tests/integration/test_pipeline_smoke.py` | — |

### Wiki notes — implements + drift_guards (14 edges — all LIVE)
| note | edge | class | evidence (file:line) |
|---|---|---|---|
| o2-logic | implements o2_normalizer.py | LIVE | `labs/obdlab/obdlab/core/o2_normalizer.py` exists |
| o2-logic | drift_guard test_o2_normalizer.py | LIVE | exists |
| fuel-trim | implements trim_vector_aggregator.py | LIVE | exists |
| fuel-trim | drift_guard test_trim_vector_aggregator.py | LIVE | exists |
| delta-relations | implements ve_engine.py | LIVE | exists |
| delta-relations | drift_guard test_ve_engine.py | LIVE | exists |
| ecu-diagnosis | implements semantic_consistency_checker.py | LIVE | exists |
| ecu-diagnosis | drift_guard test_semantic_consistency_checker.py | LIVE | exists |
| pids-protocol | implements pid_ingestion_validator.py | LIVE | exists |
| pids-protocol | drift_guard test_pid_ingestion_validator.py | LIVE | exists |
| taxonomy | implements dna_view.py | LIVE | `labs/obdlab/obdlab/schemas/dna_view.py` exists |
| taxonomy | drift_guard test_dna_view.py | LIVE | exists |
| truth-perception | implements sensor_signal_translator.py | LIVE | exists |
| truth-perception | drift_guard test_sensor_signal_translator.py | LIVE | exists |

### Wiki notes — comlab consumer edges (13 edges — the substantive check)
| note | consumer edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| o2-logic | perception_contradiction.py — O2/lambda bias-vs-truth | **LIVE** | reads `normalized_obd_lambda`: `core/perception_contradiction.py:102,129,172,180` | — |
| o2-logic | power_loss_analytics.py — mixture scoring | **LIVE** | receives/forwards `lambda_perception_delta` (derived from `normalized_obd_lambda`): `analytics/power_loss_analytics.py:189,239` | note: passthrough only — power_loss's *scoring* uses GAS chem (`gas_o2/gas_co/lambda_chem`, :214-228); "mixture scoring" descriptor is imprecise |
| fuel-trim | perception_contradiction.py — Total Fuel Trim evaluation | **LIVE** | `detect_compensated_rich` reads `total_trim_correction_delta`: `core/perception_contradiction.py:251,267,288` | — |
| fuel-trim | lab_pipeline_aggregator.py — OBD payload intake | **LIVE** | reads `obd_live_data.total_trim_correction_delta`: `core/lab_pipeline_aggregator.py:430-432` | — |
| delta-relations | power_loss_analytics.py — lambda-delta-vector scoring | **MISLABEL** | power_loss does NOT read ve_engine output (`ve_pct`/`ve_validity`); reads gas chem + passes `lambda_perception_delta`. Real `ve_pct` consumer: `core/fault_atlas_router.py:258-274,1349-1355`; real delta-vector scoring: `analytics/delta_engine.py:199,235` | repoint to `fault_atlas_router` (ve evidence gate) / `delta_engine` |
| delta-relations | perception_contradiction.py | **MISLABEL** | perception reads `normalized_obd_lambda`/`total_trim_correction_delta`, NOT ve_engine's `ve_pct`/`ve_validity` (grep: 0 `ve_pct` refs in `perception_contradiction.py`) | repoint ve_engine consumer to `fault_atlas_router._ve_evidence_gate` |
| ecu-diagnosis | ecu_hardware_checker.py — ECU driver/rail fault checks | **LIVE** | `check()` reads rail fields `intake_air_temp_c/coolant_temp_c/throttle_pos_pct/total_trim_correction_delta/per_bank_trim_delta`: `core/ecu_hardware_checker.py:31-75` | — |
| pids-protocol | fault_atlas_kg.py — PID/Mode06/readiness fault-atlas keys | **ORPHAN** | `fault_atlas_kg.py` is a pure KG JSON loader — 0 OBD-field reads (imports only `json`,`KGNode`; whole file is `resolve`/`_load_*`): `core/fault_atlas_kg.py:1-146`. Real PID reader: `core/fault_atlas_router.py:369,1453` (`per_cylinder_misfire_counts`) | repoint to `fault_atlas_router` |
| pids-protocol | lab_pipeline_aggregator.py | **LIVE** | aggregator intakes `obd_live_data` and ferries full payload incl. PID fields via `model_dump()`: `core/lab_pipeline_aggregator.py:340,612` | note: field-level PID/Mode06/readiness *logic* reader is `fault_atlas_router`; aggregator only intakes/forwards |
| taxonomy | symptom_router.py — era/emission symptom-prior routing | **MISLABEL** | `symptom_router` reads only `environmental_conditions.engine_state`/`occurs_during`: `core/symptom_router.py:6,59,69` — NO era/emission/taxonomy field. dna_view era taxonomy (`euro_emission_category`/horizon) consumed by `core/horizon_context_injector.py:47,99` + `lab_pipeline_aggregator._lambda_tolerance_for_horizon:215,394` | repoint to `horizon_context_injector` / `lab_pipeline_aggregator` (horizon) |
| taxonomy | fault_atlas_kg.py | **ORPHAN** | `fault_atlas_kg.py` reads no era/emission field (0 refs; KG loader). Era reader: `fault_atlas_router.py:311` (`era_lambda_tolerance`), `horizon_context_injector.py:99` | repoint to `fault_atlas_router` / `horizon_context_injector` |
| truth-perception | perception_contradiction.py — truth-vs-perception override core | **LIVE** | perception is the truth-vs-perception comparator (`normalized_obd_lambda` vs `lambda_chem`): `core/perception_contradiction.py:137,218,227`; producer `sensor_signal_translator.translate→OBDLivePayload`: `labs/obdlab/obdlab/core/sensor_signal_translator.py:71,230` | — |
| truth-perception | symptom_router.py — symptom prior | **MISLABEL** | `symptom_router` reads only `engine_state`/`occurs_during` (`core/symptom_router.py:6,59,69`), NOT sensor_signal_translator output. Real consumer of that output: `perception_contradiction` | repoint / drop symptom_router from truth-perception consumers |

---

## Out-of-scope observations (tail — not chased)
1. **(Resolved during session)** Early in this session `reports/obdlab__codex.md` was on
   disk while `T-GTA-OBD·codex` still read `pending`; by the time I committed, the codex
   row had flipped to `done` (commit `5c7a636`). No action needed — noting the transient
   per the START_HERE stale-ledger guard. My own row was clean throughout.
2. **`fault_atlas_kg` is structurally never an OBD-field consumer** — it is a boot-time
   KG index loader. Both edges naming it (pids-protocol, taxonomy) are ORPHANs that should
   repoint to `fault_atlas_router` (the routing layer that actually reads PID/era fields).
   Recommend the reconcile pass treat these as a pair.
3. **`symptom_router` is named by 2 edges (taxonomy, truth-perception)** but reads only the
   symptom-DNA `engine_state`/`occurs_during` keys — it consumes no OBD payload field at
   all. Both → MISLABEL. The era/truth channels it is credited with live in
   `horizon_context_injector` / `lab_pipeline_aggregator` / `fault_atlas_router` /
   `perception_contradiction`.
