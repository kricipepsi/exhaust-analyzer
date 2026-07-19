# Graph-Trust Audit — dnalab (claude)

## Plan
Picked the first `pending` row owned by `claude`: **T-GTA-DNA·claude** (no blockers).
Audited `_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml` (8 framed notes,
38 edges across `implements` / `consumers` / `drift_guards` / `mirrors_contract_in`),
classifying each LIVE / MISLABEL / ORPHAN / PENDING with `file:line` evidence against
dnalab + comlab code, and cross-checked the live `labs/dnalab/wiki/*.md` frontmatter
against the map. Reproduced the dnalab seeded case (`VehicleDNA` readers
`horizon_context_injector.from_vehicle_dna` + `projection.project` = **LIVE**,
unwired-but-tested ≠ ORPHAN). Read-only — wrote only this report.

## Summary (counts)
**38 edges classified: 38 LIVE / 0 MISLABEL / 0 ORPHAN / 0 PENDING. Seeded case OK.**

- `implements` (path-exists): 13 — all OK
- `drift_guards` (path-exists): 12 — all OK
- `mirrors_contract_in`: 1 — LIVE (target type exists)
- `consumers`: 12 — all read the named field/symbol (LIVE)
  - of which doc→doc (`hld`/`lld`/`dld` pointers): 5 — all target docs exist

Map ⇄ live-note frontmatter agree for all four framed wiki notes (10/11/12/13).

## Seeded case (must reproduce — `GRAPH_TRUST_AUDIT.md`)
> dnalab · `VehicleDNA` readers (`horizon_context_injector.from_vehicle_dna`,
> `projection.project`) → **LIVE** ("no live caller" expected pre-wire — must NOT be ORPHAN).

Confirmed **LIVE**:
- `horizon_context_injector.from_vehicle_dna` reads `vehicle_dna.vin_dna` and its sub-fields
  (`resolved_horizon`, `cylinder_count`, `number_of_banks`) —
  `labs/comlab/comlab/core/horizon_context_injector.py:70,75,77-79`.
- `projection.project` reads `vehicle_dna_json["vin_dna"]` —
  `labs/comlab/comlab/projection.py:53`.
- Both readers exist in code and are exercised by dnalab/comlab unit tests; the calling
  pipeline is `T-WIRE-1` (not yet built). Per the taxonomy, unwired-but-present reader = **LIVE**.

---

## Edge table

| note | edge | class | evidence (file:line) | proposed fix |
|---|---|---|---|---|
| PRD_DNALab.md | consumers: `hld: …/HLD_DNALab.md` | LIVE | `test -f labs/dnalab/docs/HLD_DNALab.md` → OK | — |
| PRD_DNALab.md | consumers: comlab injector `from_vehicle_dna` (VehicleDNA.vin_dna) (T-DNA-7) | LIVE | `horizon_context_injector.py:70,75` reads `vehicle_dna.vin_dna` | — |
| HLD_DNALab.md | consumers: `lld: …/LLD_DNALab.md` | LIVE | `test -f labs/dnalab/docs/LLD_DNALab.md` → OK | — |
| HLD_DNALab.md | consumers: `dld: …/DLD_DNALab.md` | LIVE | `test -f labs/dnalab/docs/DLD_DNALab.md` → OK | — |
| HLD_DNALab.md | consumers: comlab injector `from_vehicle_dna` (vin_dna) | LIVE | `horizon_context_injector.py:75` | — |
| LLD_DNALab.md | implements: `dnalab/__init__.py` | LIVE | `test -f` → OK | — |
| LLD_DNALab.md | implements: `dnalab/assembly.py` | LIVE | `test -f` → OK | — |
| LLD_DNALab.md | implements: `dnalab/models.py` | LIVE | `test -f` → OK | — |
| LLD_DNALab.md | consumers: `dld: …/DLD_DNALab.md` | LIVE | `test -f` → OK | — |
| LLD_DNALab.md | consumers: comlab injector `from_vehicle_dna` (vin_dna) | LIVE | `horizon_context_injector.py:75` | — |
| LLD_DNALab.md | drift_guards: `tests/unit/test_assembly.py` | LIVE | `test -f` → OK | — |
| LLD_DNALab.md | drift_guards: `tests/unit/test_models.py` | LIVE | `test -f` → OK | — |
| DLD_DNALab.md | implements: `dnalab/__init__.py` | LIVE | `test -f` → OK | — |
| DLD_DNALab.md | implements: `dnalab/assembly.py` | LIVE | `test -f` → OK | — |
| DLD_DNALab.md | implements: `dnalab/models.py` | LIVE | `test -f` → OK | — |
| DLD_DNALab.md | consumers: comlab injector `from_vehicle_dna` (vin_dna) | LIVE | `horizon_context_injector.py:75` | — |
| DLD_DNALab.md | consumers: comlab `ingestion.py SessionMetadata.schema_version` (MIN_SUPPORTED gate) | LIVE | gate `lab_pipeline_aggregator.py:233,240` reads `schema_version`; called at `:358` (`request.metadata.schema_version`); field def `ingestion.py:161` | — |
| DLD_DNALab.md | drift_guards: `tests/unit/test_assembly.py` | LIVE | `test -f` → OK | — |
| DLD_DNALab.md | drift_guards: `tests/unit/test_models.py` | LIVE | `test -f` → OK | — |
| DLD_DNALab.md | drift_guards: `tests/unit/test_vehicledna_roundtrip.py` | LIVE | `test -f` → OK | — |
| 10_vehicle_dna_envelope.md | implements: `dnalab/models.py` | LIVE | `test -f` → OK | — |
| 10_vehicle_dna_envelope.md | mirrors_contract_in: comlab `ingestion.py VehicleDNA` | LIVE | `class VehicleDNA` `ingestion.py:138` (fields `schema_version:146`, `vin_dna:147`) | — |
| 10_vehicle_dna_envelope.md | consumers: comlab injector `from_vehicle_dna` (vin_dna) | LIVE | `horizon_context_injector.py:70,75` | — |
| 10_vehicle_dna_envelope.md | consumers: comlab `projection.py project()` `vehicle_dna_json['vin_dna']` | LIVE | `projection.py:42,53` (`vin = vehicle_dna_json["vin_dna"]`) | — |
| 10_vehicle_dna_envelope.md | drift_guards: `tests/unit/test_models.py` | LIVE | `test -f` → OK | — |
| 10_vehicle_dna_envelope.md | drift_guards: `tests/unit/test_vehicledna_roundtrip.py` | LIVE | `test -f` → OK | — |
| 11_schema_versioning.md | implements: `dnalab/models.py` | LIVE | `test -f` → OK | — |
| 11_schema_versioning.md | consumers: comlab `ingestion.py SessionMetadata.schema_version` (MIN_SUPPORTED gate) | LIVE | gate reads + raises `lab_pipeline_aggregator.py:240`; called `:358`; field `ingestion.py:161` | — |
| 11_schema_versioning.md | drift_guards: `tests/unit/test_models.py` | LIVE | `test -f` → OK | — |
| 12_assembly_contract.md | implements: `dnalab/assembly.py` | LIVE | `test -f` → OK; `build_vehicle_dna` `assembly.py:14` | — |
| 12_assembly_contract.md | consumers: comlab `ingestion.py OrchestratorInboundRequest` (inbound assembly) | LIVE | `class OrchestratorInboundRequest` `ingestion.py:488`; consumes `VehicleDNA` whole (note body §85) | — |
| 12_assembly_contract.md | consumers: comlab `symptom_router.py route_symptom` (engine_state triage) | LIVE | `route_symptom` `symptom_router.py:38` reads `env["engine_state"]` `:60,68`; assembly stamps `engine_state` `assembly.py:45,53` | — |
| 12_assembly_contract.md | drift_guards: `tests/unit/test_assembly.py` | LIVE | `test -f` → OK | — |
| 12_assembly_contract.md | drift_guards: `tests/unit/test_assembly_integration.py` | LIVE | `test -f` → OK | — |
| 13_session_identity.md | implements: `dnalab/models.py` | LIVE | `test -f` → OK | — |
| 13_session_identity.md | consumers: comlab `lab_pipeline_aggregator.py metadata.session_id → OrchestratorFinalUIOutput.session_id correlation` | LIVE | aggregator reads `meta.session_id` `:309,505,576` and emits into `OrchestratorFinalUIOutput(session_id=…)` `:308-309` | — (see note 1) |
| 13_session_identity.md | drift_guards: `tests/unit/test_assembly.py` | LIVE | `test -f` → OK | — |
| 13_session_identity.md | drift_guards: `tests/unit/test_models.py` | LIVE | `test -f` → OK | — |

---

## Notes / out-of-scope observations (not chased — for the union/reconcile)
1. **Note 13 cross-boundary nuance (still LIVE).** The `session_id` correlation edge names a
   real reader: the aggregator reads `meta.session_id` and copies it into
   `OrchestratorFinalUIOutput.session_id`. The field is *carried* on comlab's `SessionMetadata`
   (`ingestion.py:155`+), while the note `implements: dnalab/models.py` (`VehicleDNA.new` stamps
   identity). The reader reads the named field, so this is LIVE — but the field's authoritative
   home is the comlab boundary schema, not dnalab models directly. Flagged only so the union is
   aware; no reclassification.
2. No PENDING edges in this map — the one forward-task reference (`T-DNA-7` on the PRD consumer)
   annotates an edge whose reader **already exists** in code, so it is LIVE, not PENDING.
3. The `plain:` notes (ADR/BDD/VOCAB/00/90-94) are unframed by design (no consumer) — out of scope.
