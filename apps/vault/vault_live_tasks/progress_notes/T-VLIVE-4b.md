# T-VLIVE-4b — Reconcile dnalab COMLab consumers in `vault-map.dnalab.yaml`

## Plan

Scope: `T-VLIVE-4b` reconciles the stale `OrchestratorInboundRequest.vehicle_dna` and other vague comlab consumer edges in `vault-map.dnalab.yaml`. I will repoint the vehicle_dna edges to the live readers `horizon_context_injector.py` and `projection.py`, map schema-version gates to `ingestion.py`, map assembly contract to `ingestion.py` and `symptom_router.py`, and map session correlation to `lab_pipeline_aggregator.py`. I will add the `mirrors_contract_in` field to `10_vehicle_dna_envelope.md`. I will verify that every target resolves and flip `T-VLIVE-4` from `blocked` to `pending` in the progress ledger.

## Verification results

- Eligibility: `T-VLIVE-4b` is the first runnable `pending` row (no blockers).
- Consumer edges updated in `_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml`:
  - `vehicle_dna` ingestion edges repointed to `horizon_context_injector.py` and `projection.py`.
  - `10_vehicle_dna_envelope.md` carries `mirrors_contract_in: labs/comlab/comlab/schemas/ingestion.py VehicleDNA`.
  - schema-version and assembly contract edges mapped to `ingestion.py` and `symptom_router.py`.
  - session correlation edge mapped to `lab_pipeline_aggregator.py`.
- Anti-orphan check: Checked all other consumer paths in `vault-map.dnalab.yaml`. All resolve perfectly to live files and symbols. Symbol verification confirms `from_vehicle_dna`, `vehicle_dna_json["vin_dna"]`, `VehicleDNA`, `MIN_SUPPORTED_SCHEMA_VERSION`, `OrchestratorInboundRequest`, `route_symptom`, and `session_id` exist in the respective comlab files.
- Test suites:
  - `labs/dnalab/tests` -> 27 passed.
  - `labs/comlab/tests` -> 510 passed.
- Graph untouched: `labs/dnalab/graph/` remains completely clean/untouched.
- Progress Ledger: Flipped `T-VLIVE-4b` status to `done` and updated details; flipped `T-VLIVE-4` status to `pending`.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-4b` had no blockers and was runnable.
- [x] Framed notes: N/A (this task is map-only, no notes framed/edited).
- [x] No empty consumers: All updated mapped notes have valid, non-empty consumers.
- [x] Bases render: N/A (dry-run/mechanical check of the map passes).
- [x] Tests green: both dnalab (27 passed) and comlab (510 passed) are green.
- [x] Graph untouched: git status shows no changes to `labs/dnalab/graph/` or other graph dirs.
- [x] Anti-orphan confirmed: every remaining consumer path in `vault-map.dnalab.yaml` resolves to a live file on disk.

## CODE REVIEW

- [x] Schema conformance: N/A (map change conforms to the schema).
- [x] Live path remap: Live remapped paths in the updated consumers are correctly documented (e.g. `labs/comlab/comlab/...`).
- [x] Signal/noise: Every mapped note has at least one live named consumer.
- [x] No duplicate frontmatter: N/A (no notes written/edited).
- [x] Scope guard: Checked that no other files/notes were modified.

