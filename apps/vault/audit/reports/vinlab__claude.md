# Graph-Trust Audit — vinlab (claude)

## Plan
Auditing row **T-GTA-VIN·claude** (first `pending` row owned by claude; no `reports/vinlab__claude.md`
existed — ledger consistent). Target map: `_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml`
(7 framed notes, 72 edges). Read-only: I classify every `implements`/`drift_guards`/`consumers`
edge as LIVE / MISLABEL / ORPHAN / PENDING with `file:line` evidence and write only this report —
no map/note/code/graph edits. vinlab has **no seeded case**; per `T-GTA-METHOD.md` I watch the
`vin_confidence` semantics on the comlab `fault_atlas_router` edge (a 1/3 catch in comlab).
Independence: did not read the other agents' vinlab reports.

## Method notes
- `implements` / `drift_guards`: `test -f` the path. All 9 source + 9 test paths + 3 doc pointers exist.
- `consumers` naming `file.py SYMBOL/field`: opened the file, confirmed the symbol exists **and**
  that it reads the named vinlab field/type. A reader of a *different* field = MISLABEL.
- Doc-pointer consumers (`hld:`/`lld:`/`dld:` → another vinlab design doc) classified LIVE iff the
  target doc exists (the downstream "reader" is that doc).

## Classification table

| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| PRD_VINLab.md | consumer `hld: docs/HLD_VINLab.md` | LIVE | `labs/vinlab/docs/HLD_VINLab.md` exists | — |
| PRD_VINLab.md | consumer `dnalab: assembly.py build_vehicle_dna (VehicleDNA Part-A producer contract)` | LIVE | `labs/dnalab/dnalab/assembly.py:9` `from vinlab import decode`, `:40` `physical=_decode_vin(vin)`, `:48` `VehicleDNA.new(vin_dna=physical,...)` | — |
| HLD_VINLab.md | consumer `lld: docs/LLD_VINLab.md` | LIVE | file exists | — |
| HLD_VINLab.md | consumer `dld: docs/DLD_VINLab.md` | LIVE | file exists | — |
| HLD_VINLab.md | consumer `dnalab: assembly.py build_vehicle_dna (vinlab.decode → VehicleDNA.vin_dna, Part A)` | LIVE | `assembly.py:40,48` | — |
| HLD_VINLab.md | consumer `comlab: projection.py project() (VehicleDNA → LabDnaView, reads vin_dna)` | LIVE | `labs/comlab/comlab/projection.py:53` `vin = vehicle_dna_json["vin_dna"]` | — |
| LLD_VINLab.md | implements ×9 (`__init__`, `decoder`, `models`, `db/tecdoc_query`, `overlay/{air_metering,cylinder_heuristic,horizon,stress_rpm,switches}`) | LIVE | all 9 `test -f` OK | — |
| LLD_VINLab.md | consumer `dld: docs/DLD_VINLab.md` | LIVE | file exists | — |
| LLD_VINLab.md | consumer `dnalab: assembly.py build_vehicle_dna ...` | LIVE | `assembly.py:40,48` | — |
| LLD_VINLab.md | consumer `comlab: projection.py project() reads vin_dna` | LIVE | `projection.py:53` | — |
| **LLD_VINLab.md** | **consumer `comlab: fault_atlas_router.py (FuelSystemStatus.CL comparison, :294)`** | **MISLABEL** | `fault_atlas_router.py:294` `if fuel_system_status == FuelSystemStatus.CL:` reads **FuelSystemStatus** — an **OBD** live fuel-system enum (`labs/comlab/comlab/schemas/vocabulary.py:412 class FuelSystemStatus`), **not** any vinlab field. The router's *real* vinlab read is `vin_confidence` at `:2239`. | Repoint edge → `comlab: fault_atlas_router.py vin_confidence (ExecutionMeta.vin_confidence, :2239)` |
| LLD_VINLab.md | drift_guards ×9 (test_decoder, test_models, test_horizon, test_stress_rpm, test_switches, test_cylinder_heuristic, test_air_metering, test_contract_conformance, test_vindna_from_json) | LIVE | all 9 `test -f` OK | — |
| DLD_VINLab.md | implements ×9 (same set as LLD) | LIVE | all 9 `test -f` OK | — |
| DLD_VINLab.md | consumer `dnalab: assembly.py build_vehicle_dna ...` | LIVE | `assembly.py:40,48` | — |
| DLD_VINLab.md | consumer `dnalab: models.py VinDNA.from_json -> VehicleDNA.vin_dna` | LIVE | `labs/dnalab/dnalab/models.py:106` `vin_dna=VinDNA.from_json(payload["vin_dna"])` | — |
| DLD_VINLab.md | consumer `comlab: projection.py project() reads vin_dna` | LIVE | `projection.py:53` | — |
| **DLD_VINLab.md** | **consumer `comlab: fault_atlas_router.py (FuelSystemStatus.CL comparison, :294)`** | **MISLABEL** | same as LLD: `:294` reads OBD `FuelSystemStatus`, no vinlab field; real vinlab read is `vin_confidence` `:2239` | Repoint edge → `comlab: fault_atlas_router.py vin_confidence (:2239)` |
| DLD_VINLab.md | drift_guards ×9 (same set as LLD) | LIVE | all 9 `test -f` OK | — |
| 10_decode_scope_rules.md | implements `decoder.py` | LIVE | `test -f` OK | — |
| 10_decode_scope_rules.md | consumer `vinlab: decoder.py decode_vin_payload` | LIVE | `labs/vinlab/vinlab/decoder.py:520 def decode_vin_payload` | — |
| 10_decode_scope_rules.md | consumer `vinlab: decoder.py _is_non_petrol` | LIVE | `decoder.py:142 def _is_non_petrol` | — |
| 10_decode_scope_rules.md | consumer `vinlab: decoder.py validate_vin_checksum` | LIVE | `decoder.py:693 def validate_vin_checksum` | — |
| 10_decode_scope_rules.md | drift_guards `test_decoder.py` | LIVE | `test -f` OK | — |
| 11_engine_resolution.md | implements ×5 (`decoder`, `models`, `overlay/{horizon,stress_rpm,switches}`) | LIVE | all 5 `test -f` OK | — |
| 11_engine_resolution.md | consumer `vinlab: decoder.py _resolve_wmi` | LIVE | `decoder.py:773 def _resolve_wmi` | — |
| 11_engine_resolution.md | consumer `vinlab: decoder.py _resolve_year` | LIVE | `decoder.py:793 def _resolve_year` | — |
| 11_engine_resolution.md | consumer `vinlab: decoder.py _resolve_engine` | LIVE | `decoder.py:735 def _resolve_engine` | — |
| 11_engine_resolution.md | consumer `vinlab: overlay/horizon.py euro_to_horizon` | LIVE | `labs/vinlab/vinlab/overlay/horizon.py:10 def euro_to_horizon` | — |
| 11_engine_resolution.md | consumer `comlab: projection.py project() vin.get("rated_rpm") → LabDnaView.rated_rpm` | LIVE | `projection.py:93` `rated_rpm=vin.get("rated_rpm")` (ObdLabDnaView branch) | — |
| 11_engine_resolution.md | consumer `obdlab: ObdLabDnaView.rated_rpm RPM ceiling (rated_rpm)` | LIVE | `labs/obdlab/obdlab/core/pid_ingestion_validator.py:268` `rated_rpm = dna_view.rated_rpm`, `:272` `limit = rated_rpm * _DNA_RPM_HEADROOM` (unwired pre-T-WIRE-1; reader+test exist → LIVE) | — |
| 11_engine_resolution.md | drift_guards ×3 (test_horizon, test_models, test_decoder) | LIVE | all 3 `test -f` OK | — |
| 12_brand_cylinder_rules.md | implements `overlay/cylinder_heuristic.py` | LIVE | `test -f` OK | — |
| 12_brand_cylinder_rules.md | consumer `vinlab: overlay/cylinder_heuristic.py infer_cylinder` | LIVE | `labs/vinlab/vinlab/overlay/cylinder_heuristic.py:365 def infer_cylinder` | — |
| 12_brand_cylinder_rules.md | drift_guards `test_cylinder_heuristic.py` | LIVE | `test -f` OK | — |

## Count summary
**72 edges classified: 70 LIVE / 2 MISLABEL / 0 ORPHAN / 0 PENDING.**

Per-note edge counts (implements + consumers + drift_guards):
PRD 2 · HLD 4 · LLD 22 · DLD 22 · note10 5 · note11 14 · note12 3 = **72**.

## Seeded case
vinlab has **no seeded case** in `GRAPH_TRUST_AUDIT.md` — none to reproduce. The method's
flagged watch-item (`vin_confidence` semantics) was the one real finding: the two
`fault_atlas_router.py (FuelSystemStatus.CL, :294)` edges name an **OBD** enum read, while the
router's genuine vinlab consumption is `vin_confidence` at `:2239` (vinlab `VinConfidence`,
`decoder.py:507-514`, mirrored comlab-side in `schemas/{ingestion,response}.py`). Both ruled
**MISLABEL** (real reader, wrong field) — repoint to `vin_confidence :2239`, do not demote.

## Out-of-scope notes (not chased)
- `FuelSystemStatus` / `VinConfidence` are each defined **twice** — once vinlab-native
  (`vinlab/models.py:106 VinConfidence`) and once comlab-mirrored (`vocabulary.py:545 VinConfidence`,
  `:412 FuelSystemStatus`). Consistent with the rule-5 "mirror types over JSON boundaries" pattern;
  noted, not a defect.
