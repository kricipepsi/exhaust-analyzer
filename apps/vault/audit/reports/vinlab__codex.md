## Plan
Scope: `T-GTA-VIN·codex` audits `vinlab` from `_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml`, writes only `apps/vault/audit/reports/vinlab__codex.md`, and touches no maps, notes, code, or graph outputs. I will enumerate every `implements`, `consumers`, and `drift_guards` edge, cross-check the live-note frontmatter mirrors the map, classify each edge as LIVE / MISLABEL / ORPHAN / PENDING with exact file:line evidence, watch `vin_confidence` semantics, and record the no-seed self-check for VINLab.

## Summary
- Lab: `vinlab` · agent: `codex` · task: `T-GTA-VIN·codex`.
- Map audited: `_skills/graph/4dlab-vault/assets/vault-map.vinlab.yaml`.
- Report-only write: `apps/vault/audit/reports/vinlab__codex.md`.
- Live frontmatter parity: PASS for all 7 framed notes (`PRD_VINLab.md`, `HLD_VINLab.md`, `LLD_VINLab.md`, `DLD_VINLab.md`, `10_decode_scope_rules.md`, `11_engine_resolution.md`, `12_brand_cylinder_rules.md`).
- Edge counts: 72 total — 70 LIVE / 2 MISLABEL / 0 ORPHAN / 0 PENDING.
- Seeded case: none for VINLab in `GRAPH_TRUST_AUDIT.md`; dnalab VehicleDNA seeded nuance is not applicable to this row.
- `vin_confidence` check: COMLab projection reads `vin.get("confidence")` and normalises it (`projection.py:63-65`); OBDLab separately gates `rated_rpm` enforcement on `dna_view.confidence` (`pid_ingestion_validator.py:258-268`). No `vin_confidence` orphan found.

## Edge classification
| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| `PRD_VINLab.md` | `consumers: hld: labs/vinlab/docs/HLD_VINLab.md` | LIVE | labs/vinlab/docs/HLD_VINLab.md:1-8 frontmatter exists and consumes LLD | — |
| `PRD_VINLab.md` | `consumers: dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (VehicleDNA Part-A producer contract)` | LIVE | labs/dnalab/dnalab/assembly.py:9 imports vinlab.decode; :40 decodes VIN; :48 passes vin_dna into VehicleDNA.new; labs/dnalab/dnalab/models.py:56-61 stores vin_dna | — |
| `HLD_VINLab.md` | `consumers: lld: labs/vinlab/docs/LLD_VINLab.md` | LIVE | labs/vinlab/docs/LLD_VINLab.md:1-8 frontmatter exists and implements VIN code | — |
| `HLD_VINLab.md` | `consumers: dld: labs/vinlab/docs/DLD_VINLab.md` | LIVE | labs/vinlab/docs/DLD_VINLab.md:1-8 frontmatter exists and implements VIN code | — |
| `HLD_VINLab.md` | `consumers: dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (vinlab.decode → VehicleDNA.vin_dna, Part A)` | LIVE | labs/dnalab/dnalab/assembly.py:40 decodes VIN; :48 VehicleDNA.new(vin_dna=physical); labs/dnalab/dnalab/models.py:56-61 stores vin_dna | — |
| `HLD_VINLab.md` | `consumers: comlab: labs/comlab/comlab/projection.py project() (VehicleDNA → LabDnaView, reads vin_dna)` | LIVE | labs/comlab/comlab/projection.py:42-53 project() reads vehicle_dna_json['vin_dna']; :63-65 reads confidence; :70-112 projects VIN fields into lab views | — |
| `LLD_VINLab.md` | `implements: labs/vinlab/vinlab/__init__.py` | LIVE | labs/vinlab/vinlab/__init__.py:1 exists | — |
| `LLD_VINLab.md` | `implements: labs/vinlab/vinlab/decoder.py` | LIVE | labs/vinlab/vinlab/decoder.py:1 exists | — |
| `LLD_VINLab.md` | `implements: labs/vinlab/vinlab/models.py` | LIVE | labs/vinlab/vinlab/models.py:1 exists | — |
| `LLD_VINLab.md` | `implements: labs/vinlab/vinlab/db/tecdoc_query.py` | LIVE | labs/vinlab/vinlab/db/tecdoc_query.py:1 exists | — |
| `LLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/air_metering.py` | LIVE | labs/vinlab/vinlab/overlay/air_metering.py:1 exists | — |
| `LLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/cylinder_heuristic.py` | LIVE | labs/vinlab/vinlab/overlay/cylinder_heuristic.py:1 exists | — |
| `LLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/horizon.py` | LIVE | labs/vinlab/vinlab/overlay/horizon.py:1 exists | — |
| `LLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/stress_rpm.py` | LIVE | labs/vinlab/vinlab/overlay/stress_rpm.py:1 exists | — |
| `LLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/switches.py` | LIVE | labs/vinlab/vinlab/overlay/switches.py:1 exists | — |
| `LLD_VINLab.md` | `consumers: dld: labs/vinlab/docs/DLD_VINLab.md` | LIVE | labs/vinlab/docs/DLD_VINLab.md:1-8 frontmatter exists and implements VIN code | — |
| `LLD_VINLab.md` | `consumers: dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (vinlab.decode → VehicleDNA.vin_dna, Part A)` | LIVE | labs/dnalab/dnalab/assembly.py:40 decodes VIN; :48 VehicleDNA.new(vin_dna=physical); labs/dnalab/dnalab/models.py:56-61 stores vin_dna | — |
| `LLD_VINLab.md` | `consumers: comlab: labs/comlab/comlab/projection.py project() (VehicleDNA → LabDnaView, reads vin_dna)` | LIVE | labs/comlab/comlab/projection.py:42-53 project() reads vehicle_dna_json['vin_dna']; :63-65 reads confidence; :70-112 projects VIN fields into lab views | — |
| `LLD_VINLab.md` | `consumers: comlab: labs/comlab/comlab/core/fault_atlas_router.py (FuelSystemStatus.CL comparison, :294)` | MISLABEL | labs/comlab/comlab/core/fault_atlas_router.py:283-295 defines _fuel_system_gate over FuelSystemStatus; :1188-1194 reads obd_live_data.fuel_system_status, not VinDNA/VINLab output | Remove from vinlab map or repoint to the OBD/comlab fuel-system note; this is not a VINLab consumer. |
| `LLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_decoder.py` | LIVE | labs/vinlab/tests/unit/test_decoder.py:1 exists | — |
| `LLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_models.py` | LIVE | labs/vinlab/tests/unit/test_models.py:1 exists | — |
| `LLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_horizon.py` | LIVE | labs/vinlab/tests/unit/test_horizon.py:1 exists | — |
| `LLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_stress_rpm.py` | LIVE | labs/vinlab/tests/unit/test_stress_rpm.py:1 exists | — |
| `LLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_switches.py` | LIVE | labs/vinlab/tests/unit/test_switches.py:1 exists | — |
| `LLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_cylinder_heuristic.py` | LIVE | labs/vinlab/tests/unit/test_cylinder_heuristic.py:1 exists | — |
| `LLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_air_metering.py` | LIVE | labs/vinlab/tests/unit/test_air_metering.py:1 exists | — |
| `LLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_contract_conformance.py` | LIVE | labs/vinlab/tests/unit/test_contract_conformance.py:1 exists | — |
| `LLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_vindna_from_json.py` | LIVE | labs/vinlab/tests/unit/test_vindna_from_json.py:1 exists | — |
| `DLD_VINLab.md` | `implements: labs/vinlab/vinlab/__init__.py` | LIVE | labs/vinlab/vinlab/__init__.py:1 exists | — |
| `DLD_VINLab.md` | `implements: labs/vinlab/vinlab/decoder.py` | LIVE | labs/vinlab/vinlab/decoder.py:1 exists | — |
| `DLD_VINLab.md` | `implements: labs/vinlab/vinlab/models.py` | LIVE | labs/vinlab/vinlab/models.py:1 exists | — |
| `DLD_VINLab.md` | `implements: labs/vinlab/vinlab/db/tecdoc_query.py` | LIVE | labs/vinlab/vinlab/db/tecdoc_query.py:1 exists | — |
| `DLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/air_metering.py` | LIVE | labs/vinlab/vinlab/overlay/air_metering.py:1 exists | — |
| `DLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/cylinder_heuristic.py` | LIVE | labs/vinlab/vinlab/overlay/cylinder_heuristic.py:1 exists | — |
| `DLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/horizon.py` | LIVE | labs/vinlab/vinlab/overlay/horizon.py:1 exists | — |
| `DLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/stress_rpm.py` | LIVE | labs/vinlab/vinlab/overlay/stress_rpm.py:1 exists | — |
| `DLD_VINLab.md` | `implements: labs/vinlab/vinlab/overlay/switches.py` | LIVE | labs/vinlab/vinlab/overlay/switches.py:1 exists | — |
| `DLD_VINLab.md` | `consumers: dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (vinlab.decode → VehicleDNA.vin_dna, Part A)` | LIVE | labs/dnalab/dnalab/assembly.py:40 decodes VIN; :48 VehicleDNA.new(vin_dna=physical); labs/dnalab/dnalab/models.py:56-61 stores vin_dna | — |
| `DLD_VINLab.md` | `consumers: dnalab: labs/dnalab/dnalab/models.py VinDNA.from_json -> VehicleDNA.vin_dna` | LIVE | labs/dnalab/dnalab/models.py:16 imports VinDNA; :86-107 VehicleDNA.from_json_payload calls VinDNA.from_json(payload['vin_dna']) and stores vin_dna | — |
| `DLD_VINLab.md` | `consumers: comlab: labs/comlab/comlab/projection.py project() (VehicleDNA → LabDnaView, reads vin_dna)` | LIVE | labs/comlab/comlab/projection.py:42-53 project() reads vehicle_dna_json['vin_dna']; :63-65 reads confidence; :70-112 projects VIN fields into lab views | — |
| `DLD_VINLab.md` | `consumers: comlab: labs/comlab/comlab/core/fault_atlas_router.py (FuelSystemStatus.CL comparison, :294)` | MISLABEL | labs/comlab/comlab/core/fault_atlas_router.py:283-295 defines _fuel_system_gate over FuelSystemStatus; :1188-1194 reads obd_live_data.fuel_system_status, not VinDNA/VINLab output | Remove from vinlab map or repoint to the OBD/comlab fuel-system note; this is not a VINLab consumer. |
| `DLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_decoder.py` | LIVE | labs/vinlab/tests/unit/test_decoder.py:1 exists | — |
| `DLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_models.py` | LIVE | labs/vinlab/tests/unit/test_models.py:1 exists | — |
| `DLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_horizon.py` | LIVE | labs/vinlab/tests/unit/test_horizon.py:1 exists | — |
| `DLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_stress_rpm.py` | LIVE | labs/vinlab/tests/unit/test_stress_rpm.py:1 exists | — |
| `DLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_switches.py` | LIVE | labs/vinlab/tests/unit/test_switches.py:1 exists | — |
| `DLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_cylinder_heuristic.py` | LIVE | labs/vinlab/tests/unit/test_cylinder_heuristic.py:1 exists | — |
| `DLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_air_metering.py` | LIVE | labs/vinlab/tests/unit/test_air_metering.py:1 exists | — |
| `DLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_contract_conformance.py` | LIVE | labs/vinlab/tests/unit/test_contract_conformance.py:1 exists | — |
| `DLD_VINLab.md` | `drift_guards: labs/vinlab/tests/unit/test_vindna_from_json.py` | LIVE | labs/vinlab/tests/unit/test_vindna_from_json.py:1 exists | — |
| `10_decode_scope_rules.md` | `implements: labs/vinlab/vinlab/decoder.py` | LIVE | labs/vinlab/vinlab/decoder.py:1 exists | — |
| `10_decode_scope_rules.md` | `consumers: vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder.decode_vin_payload` | LIVE | labs/vinlab/vinlab/decoder.py:520-543 defines decode_vin_payload and validates VIN; :645-673 computes horizon/stress/confidence and returns VinDNA | — |
| `10_decode_scope_rules.md` | `consumers: vinlab: labs/vinlab/vinlab/decoder.py _is_non_petrol` | LIVE | labs/vinlab/vinlab/decoder.py:142-151 scans non-petrol keywords; :564-568 and :584-588 use it for H1 fuel-scope guards | — |
| `10_decode_scope_rules.md` | `consumers: vinlab: labs/vinlab/vinlab/decoder.py validate_vin_checksum` | LIVE | labs/vinlab/vinlab/decoder.py:542-544 calls validate_vin_checksum; :693-729 implements NHTSA/bypass validation | — |
| `10_decode_scope_rules.md` | `drift_guards: labs/vinlab/tests/unit/test_decoder.py` | LIVE | labs/vinlab/tests/unit/test_decoder.py:1 exists | — |
| `11_engine_resolution.md` | `implements: labs/vinlab/vinlab/decoder.py` | LIVE | labs/vinlab/vinlab/decoder.py:1 exists | — |
| `11_engine_resolution.md` | `implements: labs/vinlab/vinlab/models.py` | LIVE | labs/vinlab/vinlab/models.py:1 exists | — |
| `11_engine_resolution.md` | `implements: labs/vinlab/vinlab/overlay/horizon.py` | LIVE | labs/vinlab/vinlab/overlay/horizon.py:1 exists | — |
| `11_engine_resolution.md` | `implements: labs/vinlab/vinlab/overlay/stress_rpm.py` | LIVE | labs/vinlab/vinlab/overlay/stress_rpm.py:1 exists | — |
| `11_engine_resolution.md` | `implements: labs/vinlab/vinlab/overlay/switches.py` | LIVE | labs/vinlab/vinlab/overlay/switches.py:1 exists | — |
| `11_engine_resolution.md` | `consumers: vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder._resolve_wmi` | LIVE | labs/vinlab/vinlab/decoder.py:546-548 calls _resolve_wmi; :773-791 resolves standard/low-volume WMI | — |
| `11_engine_resolution.md` | `consumers: vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder._resolve_year` | LIVE | labs/vinlab/vinlab/decoder.py:550-555 calls _resolve_year and gates 1990-2020; :793-827 implements year resolution | — |
| `11_engine_resolution.md` | `consumers: vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder._resolve_engine` | LIVE | labs/vinlab/vinlab/decoder.py:561-562 calls _resolve_engine; :735-771 resolves VDS/pos-8 engine rows | — |
| `11_engine_resolution.md` | `consumers: vinlab: labs/vinlab/vinlab/overlay/horizon.py euro_to_horizon` | LIVE | labs/vinlab/vinlab/overlay/horizon.py:10-25 maps Euro category to Horizon; labs/vinlab/vinlab/decoder.py:645-653 calls it for resolved_horizon and stress RPM | — |
| `11_engine_resolution.md` | `consumers: comlab: labs/comlab/comlab/projection.py project() vin.get("rated_rpm") → LabDnaView.rated_rpm` | LIVE | labs/comlab/comlab/projection.py:89-100 builds ObdLabDnaView; :93 reads vin.get('rated_rpm') into rated_rpm | — |
| `11_engine_resolution.md` | `consumers: obdlab: ObdLabDnaView.rated_rpm RPM ceiling (rated_rpm)` | LIVE | labs/obdlab/obdlab/core/pid_ingestion_validator.py:258-268 gates on DNA confidence then reads dna_view.rated_rpm; :272-276 applies rated_rpm × 1.05 ceiling | — |
| `11_engine_resolution.md` | `drift_guards: labs/vinlab/tests/unit/test_horizon.py` | LIVE | labs/vinlab/tests/unit/test_horizon.py:1 exists | — |
| `11_engine_resolution.md` | `drift_guards: labs/vinlab/tests/unit/test_models.py` | LIVE | labs/vinlab/tests/unit/test_models.py:1 exists | — |
| `11_engine_resolution.md` | `drift_guards: labs/vinlab/tests/unit/test_decoder.py` | LIVE | labs/vinlab/tests/unit/test_decoder.py:1 exists | — |
| `12_brand_cylinder_rules.md` | `implements: labs/vinlab/vinlab/overlay/cylinder_heuristic.py` | LIVE | labs/vinlab/vinlab/overlay/cylinder_heuristic.py:1 exists | — |
| `12_brand_cylinder_rules.md` | `consumers: vinlab: labs/vinlab/vinlab/overlay/cylinder_heuristic.py infer_cylinder` | LIVE | labs/vinlab/vinlab/overlay/cylinder_heuristic.py:365-391 infers CylinderHint; labs/vinlab/vinlab/decoder.py:629-636 calls _cylinder_fallback before emitting VinDNA | — |
| `12_brand_cylinder_rules.md` | `drift_guards: labs/vinlab/tests/unit/test_cylinder_heuristic.py` | LIVE | labs/vinlab/tests/unit/test_cylinder_heuristic.py:1 exists | — |

## Self-check
- Zero unclassified edges: PASS (`72` map edges emitted into the table above).
- Map⇄frontmatter parity: PASS; parsed frontmatter for each framed live note matched `implements`, `consumers`, and `drift_guards` exactly.
- ORPHAN/MISLABEL proof: the two MISLABEL rows both cite `fault_atlas_router.py:1188-1194`, which reads `obd_live_data.fuel_system_status` rather than any VINLab/VinDNA field.
- Seeded validation: PASS by absence; VINLab has no explicit seeded case in `GRAPH_TRUST_AUDIT.md`.

