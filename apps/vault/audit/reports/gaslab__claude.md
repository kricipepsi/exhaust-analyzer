# Graph-Trust Audit — gaslab (auditor: claude)

## Plan
Row picked: **T-GTA-GAS·claude** (gaslab, read-only) from `GRAPH_TRUST_PROGRESS.md` — first
`pending` row whose Owner=claude. I audit `_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml`
(156 framed edges across 15 framed notes: PRD, HLD, LLD, DLD, and wiki 01–10). For each
`implements`/`drift_guards` edge I `test -f` the path; for each `consumers` edge I open the named
comlab/gaslab file and confirm the symbol **reads the named field/type** (MISLABEL if it reads a
different field; ORPHAN if no reader at all). Evidence is `file:line`. I write **only** this report —
no edits to maps, notes, code, or graph. Seeded cases: gaslab has **no** seeded case in
`GRAPH_TRUST_AUDIT.md` (the three seeds are dtclab×2 + dnalab×1); I still cross-apply the
`power_loss_analytics` orphan lesson to the gaslab edges that name it. Independence: I have not read
the codex/agy gaslab reports.

Path convention note: `implements`/`drift_guards` cite `labs/gaslab/code/*.py`; the live package is
`labs/gaslab/gaslab/*.py` and the Vault mirror is `Vault/labs/gaslab/code/*.py`. Both exist, so
`code/` resolves — classified LIVE, with the alias recorded once here rather than per-row.

---
## Summary counts
**156 edges total: 155 LIVE / 0 MISLABEL / 1 ORPHAN / 0 PENDING.**
- Per category: `implements` 59 (all LIVE, file exists), `drift_guards` 50 (all LIVE, test file
  exists), `consumers` 47 (46 LIVE / 1 ORPHAN).
- **Seeded case:** gaslab has no seeded case in `GRAPH_TRUST_AUDIT.md`. Cross-applied the
  `power_loss_analytics` lesson: in **dtclab** it was ORPHAN (0 DTC refs); in **gaslab** it is **LIVE**
  — `power_loss_analytics.compute(...)` genuinely reads `gas_co/gas_hc/gas_o2/lambda_chem`
  (`comlab/analytics/power_loss_analytics.py:68-71, 215-218`). The contrast confirms the method.

### The one ORPHAN (→ reconcile list)
| note | edge | class | evidence | proposed fix |
|---|---|---|---|---|
| 10_limited_scope_confidence | `comlab: lab_pipeline_aggregator.py chemistry confidence input` | **ORPHAN** | `comlab/core/lab_pipeline_aggregator.py` derives confidence **only** from horizon/VIN: `_confidence_from_horizon(horizon)` (203, 479, 550), `vin_confidence` (270, 350, 480), `confidence_score=0.0`/override (286, 537); **no** read of any gas/chem confidence — `grep -niE confidence … | grep gas\|chem\|lambda` → nothing (only docstring line 324). `GasLabPayload` (`comlab/schemas/ingestion.py:165-205`) carries **no** confidence field. The aggregator reads gaslab `sample_validity`/`lambda_chem`/`lambda_measured` but **not** a chemistry confidence. | Repoint to the real reader of gaslab confidence — the gaslab-internal ranking ceiling `labs/gaslab/gaslab/ranking.py` `_clamped_confidence` (note-10 already frames this correctly as a gaslab self-consumer). If no COMLab module consumes gaslab confidence, **demote this one comlab edge**; the note stays framed via its two LIVE gaslab self-consumers + comlab `sample_validity`/`lambda` edges elsewhere. |

---
## Consumer edges — full classification (the discriminating edges)
| note | edge (consumer) | class | evidence (file:line) |
|---|---|---|---|
| PRD_GASLab | `hld: docs/HLD_GASLab.md` | LIVE | doc exists `labs/gaslab/docs/HLD_GASLab.md` |
| PRD_GASLab | `comlab: lab_pipeline_aggregator.py GasLabPayload boundary` | LIVE | `GasLabPayload` typed boundary def `comlab/schemas/ingestion.py:165`; aggregator reads `request.gas_lab_output.*` (`lab_pipeline_aggregator.py:331,402,405,436,611`) |
| HLD_GASLab | `lld: docs/LLD_GASLab.md` | LIVE | doc exists |
| HLD_GASLab | `dld: docs/DLD_GASLab.md` | LIVE | doc exists |
| HLD_GASLab | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | `chemical_state = request.gas_lab_output.chemical_state` `fault_atlas_router.py:949`; matched at 884,1663 (`gas_lab_state == chemical_state`) |
| LLD_GASLab | `dld: docs/DLD_GASLab.md` | LIVE | doc exists |
| LLD_GASLab | `comlab: power_loss_analytics.py lambda/gas analytics` | LIVE | reads `gas_hc,gas_o2,gas_co,lambda_chem` `power_loss_analytics.py:68-71`; bound from payload 215-218 |
| LLD_GASLab | `comlab: lab_pipeline_aggregator.py sample_validity/lambda aggregation` | LIVE | `sample_validity` 331; `lambda_measured` 402; `lambda_chem` 405,436 |
| LLD_GASLab | `comlab: perception_contradiction.py lambda_measured fallback` | LIVE | `select_perception_lambda(... lambda_measured ...)` `perception_contradiction.py:101-124` |
| LLD_GASLab | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | as HLD row (`fault_atlas_router.py:949,884`) |
| DLD_GASLab | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | `fault_atlas_router.py:949,884` |
| DLD_GASLab | `comlab: power_loss_analytics.py gas_co/gas_hc/gas_o2/lambda_chem` | LIVE | `power_loss_analytics.py:68-71,215-218` |
| DLD_GASLab | `comlab: lab_pipeline_aggregator.py lambda_chem/lambda_measured/sample_validity` | LIVE | `lab_pipeline_aggregator.py:331,402,405,436` |
| DLD_GASLab | `comlab: perception_contradiction.py lambda_measured` | LIVE | `perception_contradiction.py:103,115,124` |
| DLD_GASLab | `comlab: schemas/vocabulary.py sample_validity mirror` | LIVE | `SampleValidity` StrEnum "emitted by GASLab in GasLabPayload.sample_validity" `vocabulary.py:289-290` |
| 01_role_boundaries | `comlab: lab_pipeline_aggregator.py GasLabPayload ingestion` | LIVE | `gas_lab_output.model_dump()` 611; field reads 331/405 |
| 01_role_boundaries | `comlab: schemas/vocabulary.py sample_validity/ChemicalSignature mirror` | LIVE | `ChemicalSignature` `vocabulary.py:241`; `SampleValidity` 289 |
| 01_role_boundaries | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | `fault_atlas_router.py:949` |
| 02_combustion_foundations | `comlab: power_loss_analytics.py lambda_chem` | LIVE | `lambda_chem` param 71; payload 218 |
| 02_combustion_foundations | `comlab: lab_pipeline_aggregator.py lambda_chem aggregation` | LIVE | `lambda_chem=request.gas_lab_output.lambda_chem` 405,436 |
| 02_combustion_foundations | `comlab: perception_contradiction.py lambda_measured comparison` | LIVE | `perception_contradiction.py:124,140` (lambda_chem vs obd) |
| 03_five_gases_reference | `comlab: power_loss_analytics.py gas_co/gas_hc/gas_o2` | LIVE | `power_loss_analytics.py:68-70,215-217` |
| 03_five_gases_reference | `comlab: lab_pipeline_aggregator.py GasLabPayload forwarding` | LIVE | `gas_lab_output.model_dump()` 611 |
| 04_inter_gas_grammar | `comlab: lab_pipeline_aggregator.py sample_validity` | LIVE | `validity = request.gas_lab_output.sample_validity` 331 |
| 04_inter_gas_grammar | `comlab: schemas/vocabulary.py sample_validity mirror` | LIVE | `vocabulary.py:289-290` |
| 04_inter_gas_grammar | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | `fault_atlas_router.py:949,884` |
| 05_fault_atlas_part_a | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | `fault_atlas_router.py:949,884` |
| 05_fault_atlas_part_a | `comlab: power_loss_analytics.py gas_co/gas_hc/gas_o2` | LIVE | `power_loss_analytics.py:68-70` |
| 06a_oil_mechanical | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | `fault_atlas_router.py:949,884` |
| 06a_oil_mechanical | `comlab: power_loss_analytics.py gas_co/gas_hc/gas_o2` | LIVE | `power_loss_analytics.py:68-70` |
| 06b_valvetrain_egr | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | `fault_atlas_router.py:949,884` |
| 06b_valvetrain_egr | `comlab: power_loss_analytics.py gas_co/gas_hc/gas_o2` | LIVE | `power_loss_analytics.py:68-70` |
| 07_catalyst_postcat | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | `fault_atlas_router.py:949,884` |
| 07_catalyst_postcat | `comlab: power_loss_analytics.py lambda_chem/gas_o2` | LIVE | `lambda_chem` 71/218, `gas_o2` 69/216 |
| 08_diagnostic_tactics | `gaslab: rule_engine.py dual-reading and block-test path` | LIVE | `block_test_passed` gate `gaslab/rule_engine.py:248,278,386,399`; wiki §8.7 |
| 08_diagnostic_tactics | `comlab: fault_atlas_router.py chemical_state routing` | LIVE | `fault_atlas_router.py:949,884` |
| 08_diagnostic_tactics | `comlab: perception_contradiction.py lambda mismatch comparison` | LIVE | `detect(lambda_chem, normalized_obd_lambda, ...)` `perception_contradiction.py:128-180` |
| 09_era_specific | `gaslab: rule_engine.py _coc_adjust_normal_bounds` | LIVE | `gaslab/rule_engine.py:115` def, called 206 |
| 09_era_specific | `gaslab: resolution.py _euro_thresholds` | LIVE | `gaslab/resolution.py:47` def, called 107,399 |
| 10_limited_scope | `gaslab: ranking.py top-3 confidence ceiling` | LIVE | `_TOP3_LIMIT=3` 29; `_clamped_confidence` ceiling clamp `gaslab/ranking.py:98-101` |
| 10_limited_scope | `gaslab: rule_engine.py DNA-scoped candidate suppression` | LIVE | `GasLabDnaView` scoping `gaslab/rule_engine.py:117,134-156` (DNA bounds adjust/suppress) |
| 10_limited_scope | `comlab: lab_pipeline_aggregator.py chemistry confidence input` | **ORPHAN** | see ORPHAN table above — no chemistry-confidence reader in the aggregator |

---
## implements + drift_guards edges (file-existence class)
All 59 `implements` and 50 `drift_guards` paths resolve and are **LIVE** (`test -f` OK). Code paths
cite `labs/gaslab/code/*.py` (Vault-mirror alias) → live `labs/gaslab/gaslab/*.py`; both trees verified
present. Test paths under `labs/gaslab/tests/unit/` + `labs/gaslab/tests/test_cases.py` all exist.

`implements` files (each LIVE): `contracts.py, brettschneider.py, validity_gates.py, rule_engine.py,
resolution.py, ontology_loader.py, audits.py, dna_view.py, process.py, family_map.py, ranking.py,
data/gas_lab_ontology.yaml` (subset per note per the map).

`drift_guards` test files (each LIVE): `test_contracts, test_brettschneider, test_validity_gates,
test_rule_engine, test_rule_engine_reachability, test_resolution, test_ontology, test_validators,
test_dna_view, test_process, test_family_map, test_rank_candidates, test_classify_top3,
test_t_p8_7_hc_discriminator, tests/test_cases.py` (subset per note per the map).

> Pre-wire note (not a defect): all comlab consumers above are exercised by comlab unit tests but not
> yet by a live pipeline (the pipeline is `T-WIRE-1`). Per the taxonomy that is **LIVE**, not ORPHAN.

---
## Out-of-scope observations (noted, not chased)
- The note-10 ORPHAN is a **mislabeled-as-comlab** confidence edge whose true reader is the
  gaslab-internal ranking ceiling already framed in the same note — the cleanest reconcile is to drop
  the one comlab confidence edge, not to demote the note. (Reconcile pass decides; I do not edit.)
- `GasLabPayload` exposes `gas_co2/gas_nox` and a `high_idle_*` family (`ingestion.py:177-205`) whose
  comments name `R3b PID resolver` consumers — these are **not framed** in the gaslab map, so out of
  scope here; flagged only so the reconcile pass knows the payload surface is wider than the map frames.
