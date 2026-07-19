## Plan

Scope: `T-GTA-DNA·codex` audits `dnalab` using `_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml`. I will classify every framed `implements`, `consumers`, and `drift_guards` edge with file:line evidence, reproduce the seeded `VehicleDNA` reader case as LIVE when verified, write only `apps/vault/audit/reports/dnalab__codex.md`, and touch no maps, notes, code, or graph artifacts.

## Summary

- Lab: `dnalab`
- Map: `_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml`
- Report: `apps/vault/audit/reports/dnalab__codex.md`
- Framed notes audited: 8
- Edges classified: 37
- Counts: 35 LIVE / 2 MISLABEL / 0 ORPHAN / 0 PENDING
- Map/frontmatter parity: PASS — parsed frontmatter for all 8 framed live notes and found 0 mismatches against the map for `node_type`, `lab`, `module`, `subsystem`, `implements`, `consumers`, and `drift_guards`.
- Seeded case: PASS — `horizon_context_injector.from_vehicle_dna` reads `vehicle_dna.vin_dna` at `labs/comlab/comlab/core/horizon_context_injector.py:70-79`; `projection.project()` reads `vehicle_dna_json["vin_dna"]` at `labs/comlab/comlab/projection.py:46-56`; both are classified LIVE despite pre-wire status.

## Edge classifications

| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| `PRD_DNALab.md` | consumer: `hld: labs/dnalab/docs/HLD_DNALab.md` | LIVE | `labs/dnalab/docs/HLD_DNALab.md:16-20` exists as current HLD. | None. |
| `PRD_DNALab.md` | consumer: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read) (T-DNA-7)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:70-79` defines `from_vehicle_dna` and reads `vehicle_dna.vin_dna`; unit coverage at `labs/comlab/tests/unit/test_horizon_context_injector.py:95-103`. | None. |
| `HLD_DNALab.md` | consumer: `lld: labs/dnalab/docs/LLD_DNALab.md` | LIVE | `labs/dnalab/docs/LLD_DNALab.md:20-25` exists as current LLD and references HLD/DLD. | None. |
| `HLD_DNALab.md` | consumer: `dld: labs/dnalab/docs/DLD_DNALab.md` | LIVE | `labs/dnalab/docs/DLD_DNALab.md:21-26` exists as current DLD. | None. |
| `HLD_DNALab.md` | consumer: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:70-79` reads `vehicle_dna.vin_dna`; unit coverage at `labs/comlab/tests/unit/test_horizon_context_injector.py:95-103`. | None. |
| `LLD_DNALab.md` | implements: `labs/dnalab/dnalab/__init__.py` | LIVE | `labs/dnalab/dnalab/__init__.py:10-13` exports `build_vehicle_dna` and `VehicleDNA`. | None. |
| `LLD_DNALab.md` | implements: `labs/dnalab/dnalab/assembly.py` | LIVE | `labs/dnalab/dnalab/assembly.py:14-48` defines `build_vehicle_dna`, validates triage keys, resolves VIN/symptom inputs, and returns `VehicleDNA.new(...)`. | None. |
| `LLD_DNALab.md` | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:21-33` defines `VehicleDNA`; `models.py:64-76` serializes the contract payload. | None. |
| `LLD_DNALab.md` | consumer: `dld: labs/dnalab/docs/DLD_DNALab.md` | LIVE | `labs/dnalab/docs/DLD_DNALab.md:21-26` exists as current DLD. | None. |
| `LLD_DNALab.md` | consumer: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:70-79` reads `vehicle_dna.vin_dna`; unit coverage at `labs/comlab/tests/unit/test_horizon_context_injector.py:95-103`. | None. |
| `LLD_DNALab.md` | drift_guard: `labs/dnalab/tests/unit/test_assembly.py` | LIVE | `labs/dnalab/tests/unit/test_assembly.py:42-56` tests `build_vehicle_dna` returns a `VehicleDNA`; `test_assembly.py:70-76` checks payload keys/schema version. | None. |
| `LLD_DNALab.md` | drift_guard: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:12-18` constructs `VehicleDNA`; `test_models.py:42-51` tests payload keys/schema value. | None. |
| `DLD_DNALab.md` | implements: `labs/dnalab/dnalab/__init__.py` | LIVE | `labs/dnalab/dnalab/__init__.py:10-13` exports `build_vehicle_dna` and `VehicleDNA`. | None. |
| `DLD_DNALab.md` | implements: `labs/dnalab/dnalab/assembly.py` | LIVE | `labs/dnalab/dnalab/assembly.py:14-48` implements the assembly entry point. | None. |
| `DLD_DNALab.md` | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:21-33` defines the envelope; `models.py:86-103` validates inbound `schema_version` before reconstitution. | None. |
| `DLD_DNALab.md` | consumer: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:70-79` reads `vehicle_dna.vin_dna`; unit coverage at `labs/comlab/tests/unit/test_horizon_context_injector.py:95-103`. | None. |
| `DLD_DNALab.md` | consumer: `comlab: labs/comlab/comlab/schemas/ingestion.py SessionMetadata.schema_version (MIN_SUPPORTED_SCHEMA_VERSION gate)` | MISLABEL | `labs/comlab/comlab/schemas/ingestion.py:151-161` only defines `SessionMetadata.schema_version`; the real gate is `labs/comlab/comlab/core/lab_pipeline_aggregator.py:231-245` plus `lab_pipeline_aggregator.py:357-358`, which reads `request.metadata.schema_version`. | Relabel consumer to `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py _run_stage_a_fatal_gates/check_schema_version (request.metadata.schema_version MIN_SUPPORTED_SCHEMA_VERSION gate)`. |
| `DLD_DNALab.md` | drift_guard: `labs/dnalab/tests/unit/test_assembly.py` | LIVE | `labs/dnalab/tests/unit/test_assembly.py:42-56` covers assembly; `test_assembly.py:91-96` covers payload reconstitution. | None. |
| `DLD_DNALab.md` | drift_guard: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:12-18` covers construction; `test_models.py:34-39` rejects wrong schema versions. | None. |
| `DLD_DNALab.md` | drift_guard: `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py` | LIVE | `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py:15-22` round-trips envelope metadata; `test_vehicledna_roundtrip.py:24-30` round-trips nested `vin_dna`. | None. |
| `10_vehicle_dna_envelope.md` | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:21-33` defines `VehicleDNA`; `models.py:64-76` emits `session_id`, `timestamp`, `schema_version`, `vin_dna`, and `symptom_dna`. | None. |
| `10_vehicle_dna_envelope.md` | consumer: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:70-79` reads `vehicle_dna.vin_dna`; unit coverage at `labs/comlab/tests/unit/test_horizon_context_injector.py:95-103`. | None. |
| `10_vehicle_dna_envelope.md` | consumer: `comlab: labs/comlab/comlab/projection.py project() vehicle_dna_json['vin_dna']` | LIVE | `labs/comlab/comlab/projection.py:46-56` defines `project()` and reads `vehicle_dna_json["vin_dna"]`; unit coverage at `labs/comlab/tests/unit/test_projection.py:111-146`. | None. |
| `10_vehicle_dna_envelope.md` | drift_guard: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:42-51` checks exact payload keys/schema value. | None. |
| `10_vehicle_dna_envelope.md` | drift_guard: `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py` | LIVE | `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py:15-22` round-trips metadata; `test_vehicledna_roundtrip.py:81-88` round-trips JSON string payload. | None. |
| `11_schema_versioning.md` | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:41-59` defaults and stores `schema_version`; `models.py:93-100` rejects mismatched versions. | None. |
| `11_schema_versioning.md` | consumer: `comlab: labs/comlab/comlab/schemas/ingestion.py SessionMetadata.schema_version (MIN_SUPPORTED_SCHEMA_VERSION gate)` | MISLABEL | `labs/comlab/comlab/schemas/ingestion.py:151-161` only defines `SessionMetadata.schema_version`; the real gate is `labs/comlab/comlab/core/lab_pipeline_aggregator.py:231-245` plus `lab_pipeline_aggregator.py:357-358`, which reads `request.metadata.schema_version`. | Relabel consumer to `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py _run_stage_a_fatal_gates/check_schema_version (request.metadata.schema_version MIN_SUPPORTED_SCHEMA_VERSION gate)`. |
| `11_schema_versioning.md` | drift_guard: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:34-39` rejects wrong schema versions; `test_models.py:50-51` checks schema value. | None. |
| `12_assembly_contract.md` | implements: `labs/dnalab/dnalab/assembly.py` | LIVE | `labs/dnalab/dnalab/assembly.py:14-48` implements the assembly contract and passes `engine_state`/`load_state` into `symptomlab.resolve(...)`. | None. |
| `12_assembly_contract.md` | consumer: `comlab: labs/comlab/comlab/schemas/ingestion.py OrchestratorInboundRequest (inbound assembly)` | LIVE | `labs/comlab/comlab/schemas/ingestion.py:488-502` defines `OrchestratorInboundRequest`, the complete COMLab ingestion payload accepted from adapters/callers. | None. |
| `12_assembly_contract.md` | consumer: `comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (engine_state triage)` | LIVE | `labs/comlab/comlab/core/symptom_router.py:38-61` defines `route_symptom()` and reads `symptom_dna["environmental_conditions"]["engine_state"]`; routing branches at `symptom_router.py:68-84`. | None. |
| `12_assembly_contract.md` | drift_guard: `labs/dnalab/tests/unit/test_assembly.py` | LIVE | `labs/dnalab/tests/unit/test_assembly.py:42-56` covers happy-path assembly; `test_assembly.py:113-129` rejects missing triage keys before resolve. | None. |
| `12_assembly_contract.md` | drift_guard: `labs/dnalab/tests/unit/test_assembly_integration.py` | LIVE | `labs/dnalab/tests/unit/test_assembly_integration.py:15-22` runs real sibling-pipeline assembly when available and asserts returned `VehicleDNA`. | None. |
| `13_session_identity.md` | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:41-58` generates/stores `session_id`; `models.py:70-73` serializes it. | None. |
| `13_session_identity.md` | consumer: `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py metadata.session_id → OrchestratorFinalUIOutput.session_id correlation` | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:263-310` copies `meta.session_id` into fatal output; `lab_pipeline_aggregator.py:504-506` and `lab_pipeline_aggregator.py:575-577` copy `meta.session_id` into final outputs. | None. |
| `13_session_identity.md` | drift_guard: `labs/dnalab/tests/unit/test_assembly.py` | LIVE | `labs/dnalab/tests/unit/test_assembly.py:61-62` checks generated session id format; `test_assembly.py:91-96` preserves session id through reconstitution. | None. |
| `13_session_identity.md` | drift_guard: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:14-18` checks generated session id; `test_models.py:21-31` checks explicit session id preservation. | None. |

## Notes for union/reconcile

- D1: `DLD_DNALab.md` and `11_schema_versioning.md` both label the schema-version gate as `labs/comlab/comlab/schemas/ingestion.py SessionMetadata.schema_version`. That file defines the field, but the actual live gate/read is in `labs/comlab/comlab/core/lab_pipeline_aggregator.py` via `check_schema_version(request.metadata.schema_version)`. Repoint both consumer edges to the aggregator gate.
- No ORPHAN edges found.
- No PENDING edges found.
