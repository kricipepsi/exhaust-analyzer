## Plan

For `T-GTA-VIN·agy`, I will audit `vinlab`. The map is at `/agent_workspace/_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml`. I will verify that every framed `consumers`, `drift_guards`, and `implements` edge resolves to a real code read or test file. I will write the report to `/agent_workspace/apps/vault/audit/reports/vinlab__agy.md` and touch nothing else. There is no seeded case defined for `vinlab` in `GRAPH_TRUST_AUDIT.md` (which names only dtclab, comlab, and dnalab), but I will pay special attention to the `vin_confidence` semantics which was a 1/3 catch in comlab.

## Summary

- **Lab**: `vinlab`
- **Map audited**: `/agent_workspace/_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml`
- **Total edges**: 72
- **LIVE**: 70
- **MISLABEL**: 2
- **ORPHAN**: 0
- **PENDING**: 0
- **Seeded case validation**: N/A (no seeded case for `vinlab` in `GRAPH_TRUST_AUDIT.md`).

## Edge classifications

| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| **PRD_VINLab.md** | consumers: `hld: labs/vinlab/docs/HLD_VINLab.md` | LIVE | `labs/vinlab/docs/HLD_VINLab.md:19` | — |
| PRD_VINLab.md | consumers: `dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (VehicleDNA Part-A producer contract)` | LIVE | `labs/dnalab/dnalab/assembly.py:9,40` | — |
| **HLD_VINLab.md** | consumers: `lld: labs/vinlab/docs/LLD_VINLab.md` | LIVE | `labs/vinlab/docs/LLD_VINLab.md:38` | — |
| HLD_VINLab.md | consumers: `dld: labs/vinlab/docs/DLD_VINLab.md` | LIVE | `labs/vinlab/docs/DLD_VINLab.md:38` | — |
| HLD_VINLab.md | consumers: `dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (vinlab.decode → VehicleDNA.vin_dna, Part A)` | LIVE | `labs/dnalab/dnalab/assembly.py:40` | — |
| HLD_VINLab.md | consumers: `comlab: labs/comlab/comlab/projection.py project() (VehicleDNA → LabDnaView, reads vin_dna)` | LIVE | `labs/comlab/comlab/projection.py:53` | — |
| **LLD_VINLab.md** | implements: `labs/vinlab/vinlab/__init__.py` | LIVE | `labs/vinlab/vinlab/__init__.py` exists | — |
| LLD_VINLab.md | implements: `labs/vinlab/vinlab/decoder.py` | LIVE | `labs/vinlab/vinlab/decoder.py` exists | — |
| LLD_VINLab.md | implements: `labs/vinlab/vinlab/models.py` | LIVE | `labs/vinlab/vinlab/models.py:29` (`VinDNA`) | — |
| LLD_VINLab.md | implements: `labs/vinlab/vinlab/db/tecdoc_query.py` | LIVE | `labs/vinlab/vinlab/db/tecdoc_query.py` exists | — |
| LLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/air_metering.py` | LIVE | `labs/vinlab/vinlab/overlay/air_metering.py` exists | — |
| LLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/cylinder_heuristic.py` | LIVE | `labs/vinlab/vinlab/overlay/cylinder_heuristic.py` exists | — |
| LLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/horizon.py` | LIVE | `labs/vinlab/vinlab/overlay/horizon.py` exists | — |
| LLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/stress_rpm.py` | LIVE | `labs/vinlab/vinlab/overlay/stress_rpm.py` exists | — |
| LLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/switches.py` | LIVE | `labs/vinlab/vinlab/overlay/switches.py` exists | — |
| LLD_VINLab.md | consumers: `dld: labs/vinlab/docs/DLD_VINLab.md` | LIVE | `labs/vinlab/docs/DLD_VINLab.md:44` | — |
| LLD_VINLab.md | consumers: `dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (vinlab.decode → VehicleDNA.vin_dna, Part A)` | LIVE | `labs/dnalab/dnalab/assembly.py:40` | — |
| LLD_VINLab.md | consumers: `comlab: labs/comlab/comlab/projection.py project() (VehicleDNA → LabDnaView, reads vin_dna)` | LIVE | `labs/comlab/comlab/projection.py:53` | — |
| LLD_VINLab.md | consumers: `comlab: labs/comlab/comlab/core/fault_atlas_router.py (FuelSystemStatus.CL comparison, :294)` | MISLABEL | `labs/comlab/comlab/core/fault_atlas_router.py:294` | Repoint file to `labs/comlab/comlab/core/fault_atlas_router.py` and symbol to `vin_confidence` read (line 2239). |
| LLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_decoder.py` | LIVE | `labs/vinlab/tests/unit/test_decoder.py` exists | — |
| LLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_models.py` | LIVE | `labs/vinlab/tests/unit/test_models.py` exists | — |
| LLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_horizon.py` | LIVE | `labs/vinlab/tests/unit/test_horizon.py` exists | — |
| LLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_stress_rpm.py` | LIVE | `labs/vinlab/tests/unit/test_stress_rpm.py` exists | — |
| LLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_switches.py` | LIVE | `labs/vinlab/tests/unit/test_switches.py` exists | — |
| LLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_cylinder_heuristic.py` | LIVE | `labs/vinlab/tests/unit/test_cylinder_heuristic.py` exists | — |
| LLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_air_metering.py` | LIVE | `labs/vinlab/tests/unit/test_air_metering.py` exists | — |
| LLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_contract_conformance.py` | LIVE | `labs/vinlab/tests/unit/test_contract_conformance.py` exists | — |
| LLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_vindna_from_json.py` | LIVE | `labs/vinlab/tests/unit/test_vindna_from_json.py` exists | — |
| **DLD_VINLab.md** | implements: `labs/vinlab/vinlab/__init__.py` | LIVE | `labs/vinlab/vinlab/__init__.py` exists | — |
| DLD_VINLab.md | implements: `labs/vinlab/vinlab/decoder.py` | LIVE | `labs/vinlab/vinlab/decoder.py` exists | — |
| DLD_VINLab.md | implements: `labs/vinlab/vinlab/models.py` | LIVE | `labs/vinlab/vinlab/models.py:29` (`VinDNA`) | — |
| DLD_VINLab.md | implements: `labs/vinlab/vinlab/db/tecdoc_query.py` | LIVE | `labs/vinlab/vinlab/db/tecdoc_query.py` exists | — |
| DLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/air_metering.py` | LIVE | `labs/vinlab/vinlab/overlay/air_metering.py` exists | — |
| DLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/cylinder_heuristic.py` | LIVE | `labs/vinlab/vinlab/overlay/cylinder_heuristic.py` exists | — |
| DLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/horizon.py` | LIVE | `labs/vinlab/vinlab/overlay/horizon.py` exists | — |
| DLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/stress_rpm.py` | LIVE | `labs/vinlab/vinlab/overlay/stress_rpm.py` exists | — |
| DLD_VINLab.md | implements: `labs/vinlab/vinlab/overlay/switches.py` | LIVE | `labs/vinlab/vinlab/overlay/switches.py` exists | — |
| DLD_VINLab.md | consumers: `dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (vinlab.decode → VehicleDNA.vin_dna, Part A)` | LIVE | `labs/dnalab/dnalab/assembly.py:40` | — |
| DLD_VINLab.md | consumers: `dnalab: labs/dnalab/dnalab/models.py VinDNA.from_json -> VehicleDNA.vin_dna` | LIVE | `labs/dnalab/dnalab/models.py:106` | — |
| DLD_VINLab.md | consumers: `comlab: labs/comlab/comlab/projection.py project() (VehicleDNA → LabDnaView, reads vin_dna)` | LIVE | `labs/comlab/comlab/projection.py:53` | — |
| DLD_VINLab.md | consumers: `comlab: labs/comlab/comlab/core/fault_atlas_router.py (FuelSystemStatus.CL comparison, :294)` | MISLABEL | `labs/comlab/comlab/core/fault_atlas_router.py:294` | Repoint file to `labs/comlab/comlab/core/fault_atlas_router.py` and symbol to `vin_confidence` read (line 2239). |
| DLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_decoder.py` | LIVE | `labs/vinlab/tests/unit/test_decoder.py` exists | — |
| DLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_models.py` | LIVE | `labs/vinlab/tests/unit/test_models.py` exists | — |
| DLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_horizon.py` | LIVE | `labs/vinlab/tests/unit/test_horizon.py` exists | — |
| DLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_stress_rpm.py` | LIVE | `labs/vinlab/tests/unit/test_stress_rpm.py` exists | — |
| DLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_switches.py` | LIVE | `labs/vinlab/tests/unit/test_switches.py` exists | — |
| DLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_cylinder_heuristic.py` | LIVE | `labs/vinlab/tests/unit/test_cylinder_heuristic.py` exists | — |
| DLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_air_metering.py` | LIVE | `labs/vinlab/tests/unit/test_air_metering.py` exists | — |
| DLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_contract_conformance.py` | LIVE | `labs/vinlab/tests/unit/test_contract_conformance.py` exists | — |
| DLD_VINLab.md | drift_guards: `labs/vinlab/tests/unit/test_vindna_from_json.py` | LIVE | `labs/vinlab/tests/unit/test_vindna_from_json.py` exists | — |
| **10_decode_scope_rules.md** | implements: `labs/vinlab/vinlab/decoder.py` | LIVE | `labs/vinlab/vinlab/decoder.py` exists | — |
| 10_decode_scope_rules.md | consumers: `vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder.decode_vin_payload` | LIVE | `labs/vinlab/vinlab/decoder.py:520` | — |
| 10_decode_scope_rules.md | consumers: `vinlab: labs/vinlab/vinlab/decoder.py _is_non_petrol` | LIVE | `labs/vinlab/vinlab/decoder.py:142` | — |
| 10_decode_scope_rules.md | consumers: `vinlab: labs/vinlab/vinlab/decoder.py validate_vin_checksum` | LIVE | `labs/vinlab/vinlab/decoder.py:693` | — |
| 10_decode_scope_rules.md | drift_guards: `labs/vinlab/tests/unit/test_decoder.py` | LIVE | `labs/vinlab/tests/unit/test_decoder.py` exists | — |
| **11_engine_resolution.md** | implements: `labs/vinlab/vinlab/decoder.py` | LIVE | `labs/vinlab/vinlab/decoder.py` exists | — |
| 11_engine_resolution.md | implements: `labs/vinlab/vinlab/models.py` | LIVE | `labs/vinlab/vinlab/models.py:29` (`VinDNA`) | — |
| 11_engine_resolution.md | implements: `labs/vinlab/vinlab/overlay/horizon.py` | LIVE | `labs/vinlab/vinlab/overlay/horizon.py` exists | — |
| 11_engine_resolution.md | implements: `labs/vinlab/vinlab/overlay/stress_rpm.py` | LIVE | `labs/vinlab/vinlab/overlay/stress_rpm.py` exists | — |
| 11_engine_resolution.md | implements: `labs/vinlab/vinlab/overlay/switches.py` | LIVE | `labs/vinlab/vinlab/overlay/switches.py` exists | — |
| 11_engine_resolution.md | consumers: `vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder._resolve_wmi` | LIVE | `labs/vinlab/vinlab/decoder.py:773` | — |
| 11_engine_resolution.md | consumers: `vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder._resolve_year` | LIVE | `labs/vinlab/vinlab/decoder.py:793` | — |
| 11_engine_resolution.md | consumers: `vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder._resolve_engine` | LIVE | `labs/vinlab/vinlab/decoder.py:735` | — |
| 11_engine_resolution.md | consumers: `vinlab: labs/vinlab/vinlab/overlay/horizon.py euro_to_horizon` | LIVE | `labs/vinlab/vinlab/overlay/horizon.py:10` | — |
| 11_engine_resolution.md | consumers: `comlab: labs/comlab/comlab/projection.py project() vin.get("rated_rpm") → LabDnaView.rated_rpm` | LIVE | `labs/comlab/comlab/projection.py:93` | — |
| 11_engine_resolution.md | consumers: `obdlab: ObdLabDnaView.rated_rpm RPM ceiling (rated_rpm)` | LIVE | `labs/obdlab/obdlab/core/pid_ingestion_validator.py:268` | — |
| 11_engine_resolution.md | drift_guards: `labs/vinlab/tests/unit/test_horizon.py` | LIVE | `labs/vinlab/tests/unit/test_horizon.py` exists | — |
| 11_engine_resolution.md | drift_guards: `labs/vinlab/tests/unit/test_models.py` | LIVE | `labs/vinlab/tests/unit/test_models.py` exists | — |
| 11_engine_resolution.md | drift_guards: `labs/vinlab/tests/unit/test_decoder.py` | LIVE | `labs/vinlab/tests/unit/test_decoder.py` exists | — |
| **12_brand_cylinder_rules.md** | implements: `labs/vinlab/vinlab/overlay/cylinder_heuristic.py` | LIVE | `labs/vinlab/vinlab/overlay/cylinder_heuristic.py` exists | — |
| 12_brand_cylinder_rules.md | consumers: `vinlab: labs/vinlab/vinlab/overlay/cylinder_heuristic.py infer_cylinder` | LIVE | `labs/vinlab/vinlab/overlay/cylinder_heuristic.py:365` | — |
| 12_brand_cylinder_rules.md | drift_guards: `labs/vinlab/tests/unit/test_cylinder_heuristic.py` | LIVE | `labs/vinlab/tests/unit/test_cylinder_heuristic.py` exists | — |
