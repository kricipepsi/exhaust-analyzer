## Plan

For `T-GTA-DNA·agy`, I will audit `dnalab`. The map is at `/agent_workspace/_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml`. I will verify that every framed `consumers`, `drift_guards`, and `implements` edge resolves to a real code read or test file. I will write the report to `/agent_workspace/apps/vault/audit/reports/dnalab__agy.md` and touch nothing else. I will also reproduce the `dnalab` seeded case (VehicleDNA readers `horizon_context_injector.from_vehicle_dna`, `projection.project` classified as LIVE).

## Summary

- **Lab**: `dnalab`
- **Map audited**: `/agent_workspace/_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml`
- **Total edges**: 38
- **LIVE**: 36
- **MISLABEL**: 2
- **ORPHAN**: 0
- **PENDING**: 0
- **Seeded case validation**: Confirmed. VehicleDNA readers (`horizon_context_injector.from_vehicle_dna` and `projection.project`) are verified as **LIVE** (code readers exist and are covered by unit tests, "no live pipeline caller" is expected pre-wiring).

## Edge classifications

| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| **PRD_DNALab.md** | consumers: `hld: labs/dnalab/docs/HLD_DNALab.md` | LIVE | `labs/dnalab/docs/HLD_DNALab.md:18` | — |
| PRD_DNALab.md | consumers: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read) (T-DNA-7)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:75` | — |
| **HLD_DNALab.md** | consumers: `lld: labs/dnalab/docs/LLD_DNALab.md` | LIVE | `labs/dnalab/docs/LLD_DNALab.md:23` | — |
| HLD_DNALab.md | consumers: `dld: labs/dnalab/docs/DLD_DNALab.md` | LIVE | `labs/dnalab/docs/DLD_DNALab.md:24` | — |
| HLD_DNALab.md | consumers: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:75` | — |
| **LLD_DNALab.md** | implements: `labs/dnalab/dnalab/__init__.py` | LIVE | `labs/dnalab/dnalab/__init__.py:10-11` | — |
| LLD_DNALab.md | implements: `labs/dnalab/dnalab/assembly.py` | LIVE | `labs/dnalab/dnalab/assembly.py:14` | — |
| LLD_DNALab.md | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:22` | — |
| LLD_DNALab.md | consumers: `dld: labs/dnalab/docs/DLD_DNALab.md` | LIVE | `labs/dnalab/docs/DLD_DNALab.md:1` (doc exists) | — |
| LLD_DNALab.md | consumers: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:75` | — |
| LLD_DNALab.md | drift_guards: `labs/dnalab/tests/unit/test_assembly.py` | LIVE | `labs/dnalab/tests/unit/test_assembly.py:43` | — |
| LLD_DNALab.md | drift_guards: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:13` | — |
| **DLD_DNALab.md** | implements: `labs/dnalab/dnalab/__init__.py` | LIVE | `labs/dnalab/dnalab/__init__.py:10-11` | — |
| DLD_DNALab.md | implements: `labs/dnalab/dnalab/assembly.py` | LIVE | `labs/dnalab/dnalab/assembly.py:14` | — |
| DLD_DNALab.md | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:22` | — |
| DLD_DNALab.md | consumers: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:75` | — |
| DLD_DNALab.md | consumers: `comlab: labs/comlab/comlab/schemas/ingestion.py SessionMetadata.schema_version (MIN_SUPPORTED_SCHEMA_VERSION gate)` | MISLABEL | `labs/comlab/comlab/schemas/ingestion.py:161` | Repoint file to `labs/comlab/comlab/core/lab_pipeline_aggregator.py` and symbol to `check_schema_version()`. |
| DLD_DNALab.md | drift_guards: `labs/dnalab/tests/unit/test_assembly.py` | LIVE | `labs/dnalab/tests/unit/test_assembly.py:43` | — |
| DLD_DNALab.md | drift_guards: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:13` | — |
| DLD_DNALab.md | drift_guards: `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py` | LIVE | `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py:16` | — |
| **10_vehicle_dna_envelope.md** | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:21-33` | — |
| 10_vehicle_dna_envelope.md | mirrors_contract_in: `labs/comlab/comlab/schemas/ingestion.py VehicleDNA` | LIVE | `labs/comlab/comlab/schemas/ingestion.py:138` | — |
| 10_vehicle_dna_envelope.md | consumers: `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)` | LIVE | `labs/comlab/comlab/core/horizon_context_injector.py:75` | — |
| 10_vehicle_dna_envelope.md | consumers: `comlab: labs/comlab/comlab/projection.py project() vehicle_dna_json['vin_dna']` | LIVE | `labs/comlab/comlab/projection.py:53` | — |
| 10_vehicle_dna_envelope.md | drift_guards: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:13` | — |
| 10_vehicle_dna_envelope.md | drift_guards: `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py` | LIVE | `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py:16` | — |
| **11_schema_versioning.md** | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:18` | — |
| 11_schema_versioning.md | consumers: `comlab: labs/comlab/comlab/schemas/ingestion.py SessionMetadata.schema_version (MIN_SUPPORTED_SCHEMA_VERSION gate)` | MISLABEL | `labs/comlab/comlab/schemas/ingestion.py:161` | Repoint file to `labs/comlab/comlab/core/lab_pipeline_aggregator.py` and symbol to `check_schema_version()`. |
| 11_schema_versioning.md | drift_guards: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:13` | — |
| **12_assembly_contract.md** | implements: `labs/dnalab/dnalab/assembly.py` | LIVE | `labs/dnalab/dnalab/assembly.py:14` | — |
| 12_assembly_contract.md | consumers: `comlab: labs/comlab/comlab/schemas/ingestion.py OrchestratorInboundRequest (inbound assembly)` | LIVE | `labs/comlab/comlab/schemas/ingestion.py:488` | — |
| 12_assembly_contract.md | consumers: `comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (engine_state triage)` | LIVE | `labs/comlab/comlab/core/symptom_router.py:60` | — |
| 12_assembly_contract.md | drift_guards: `labs/dnalab/tests/unit/test_assembly.py` | LIVE | `labs/dnalab/tests/unit/test_assembly.py:43` | — |
| 12_assembly_contract.md | drift_guards: `labs/dnalab/tests/unit/test_assembly_integration.py` | LIVE | `labs/dnalab/tests/unit/test_assembly_integration.py:14` | — |
| **13_session_identity.md** | implements: `labs/dnalab/dnalab/models.py` | LIVE | `labs/dnalab/dnalab/models.py:41-52` | — |
| 13_session_identity.md | consumers: `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py metadata.session_id → OrchestratorFinalUIOutput.session_id correlation` | LIVE | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:309` | — |
| 13_session_identity.md | drift_guards: `labs/dnalab/tests/unit/test_assembly.py` | LIVE | `labs/dnalab/tests/unit/test_assembly.py:43` | — |
| 13_session_identity.md | drift_guards: `labs/dnalab/tests/unit/test_models.py` | LIVE | `labs/dnalab/tests/unit/test_models.py:13` | — |
