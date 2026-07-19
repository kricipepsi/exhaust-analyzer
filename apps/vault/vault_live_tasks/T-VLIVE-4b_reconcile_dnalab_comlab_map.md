# T-VLIVE-4b — Reconcile dnalab COMLab consumers in `vault-map.dnalab.yaml`
**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring (map asset) · **Mode:** STRICT
**Blocks:** T-VLIVE-4 (dnalab framing cannot pass the anti-orphan gate until this lands)
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md` (Step 4/5 orphan rule).

## Goal
Repoint every dnalab COMLab consumer edge that names a **non-existent symbol**
(`OrchestratorInboundRequest.vehicle_dna`) or vague prose (`session correlation`,
`schema-version gate`) to the **real live reader** in comlab, so T-VLIVE-4 frames
dnalab with zero `MISSING` consumers. This is a naming fix only — no path was
deleted (unlike the dtclab/comlab wired edges); the DNA envelope **is** consumed
live, just under different symbols.

## Context (why the edges are stale)
`OrchestratorInboundRequest` (live `labs/comlab/comlab/schemas/ingestion.py:488`)
has **no `vehicle_dna` field** — its fields are `metadata, gas_lab_output,
obd_live_data, dtc_lab_output, symptom_dna, downstream_trim_role, has_catalyst,
user_input_echo_audit, second_operating_point`. The DNA envelope reaches comlab as
the **`VehicleDNA`** mirror class (`ingestion.py:138`, holds `vin_dna: VinDNA`) and
the 17-char `SessionMetadata.vin_dna_string`. Verified live readers of it:
- `labs/comlab/comlab/core/horizon_context_injector.py` →
  `HorizonContextInjector.from_vehicle_dna(vehicle_dna: VehicleDNA)` reads
  `vehicle_dna.vin_dna.{resolved_horizon, cylinder_count, number_of_banks}`.
- `labs/comlab/comlab/projection.py` → `project()` reads
  `vehicle_dna_json["vin_dna"]` to build a `LabDnaView`.
- `labs/comlab/comlab/schemas/lab_dna_views.py` — read-only views of `VehicleDNA`.

## Decision (architect-pinned — do not redesign)
Replace each edge as below; **grep-verify each target resolves before writing**.

| Note(s) (map line) | Stale edge | Repoint to (live read) |
|---|---|---|
| design docs + `10_vehicle_dna_envelope.md` (17, 27, 39, 52, 65) | `comlab: OrchestratorInboundRequest.vehicle_dna ingestion` | `comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)` — and on the envelope note also `comlab: labs/comlab/comlab/projection.py project() vehicle_dna_json["vin_dna"]` |
| `10_vehicle_dna_envelope.md` (implements `models.py`) | (mirror not stated) | add `mirrors_contract_in: labs/comlab/comlab/schemas/ingestion.py VehicleDNA` (comlab-local mirror of the dnalab envelope) |
| design-doc note (53) + `11_schema_versioning.md` (76) | `schema-version gate` / `OrchestratorInboundRequest schema compatibility gate` | `comlab: labs/comlab/comlab/schemas/ingestion.py SessionMetadata.schema_version (MIN_SUPPORTED_SCHEMA_VERSION gate)` (ingestion.py:161) |
| `12_assembly_contract.md` (86) | `OrchestratorInboundRequest ingestion call` | `comlab: labs/comlab/comlab/schemas/ingestion.py OrchestratorInboundRequest (inbound assembly)` |
| `12_assembly_contract.md` (87) | `symptom_router.route_symptom (engine_state triage value)` | add path: `comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (engine_state triage)` — already resolves, just unqualified |
| `13_session_identity.md` (98) | `comlab: session correlation` | `comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py metadata.session_id → OrchestratorFinalUIOutput.session_id correlation` (aggregator lines 309/505/576/606; response.py:135) |

Preserve provenance tags already on edges (e.g. the `(T-DNA-7)` suffix on line 17)
— fix the symbol, keep the tag. **No note is demoted to `plain`**: every dnalab
note retains ≥1 live consumer after the repoint (`session_id` is read live, so
`13_session_identity` stays framed).

## Files to touch
- edit (consumer edges only): `_skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml`
  — the 5 `vehicle_dna` edges + lines 53, 76, 86, 87, 98 per the table; add the one
  `mirrors_contract_in` line on `10_vehicle_dna_envelope.md`.
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md` (flip T-VLIVE-4 `blocked` → `pending`).

## Out of scope
- Any other map asset; dnalab note bodies/frontmatter (that is T-VLIVE-4); any
  Python; any graph; the dnalab→comlab schema itself; `Vault/`.

## Verification
1. `grep -n 'OrchestratorInboundRequest.vehicle_dna\|session correlation' _skills/graph/4dlab-vault/assets/vault-map.dnalab.yaml`
   → no matches.
2. Every repointed target resolves to a live read:
   - `grep -n 'def from_vehicle_dna' labs/comlab/comlab/core/horizon_context_injector.py`
   - `grep -n 'vehicle_dna_json\["vin_dna"\]' labs/comlab/comlab/projection.py`
   - `grep -n 'class VehicleDNA\|MIN_SUPPORTED_SCHEMA_VERSION\|class OrchestratorInboundRequest' labs/comlab/comlab/schemas/ingestion.py`
   - `grep -n 'def route_symptom' labs/comlab/comlab/core/symptom_router.py`
   - `grep -n 'session_id=meta.session_id\|metadata.session_id' labs/comlab/comlab/core/lab_pipeline_aggregator.py`
3. Re-run the T-VLIVE-4 anti-orphan gate (dry-run dnalab framing): every named
   consumer + `implements`/`drift_guards` path resolves; zero unresolved. No note
   bodies written by this task.
4. `git --no-pager diff --stat` shows only the two files above touched.

## Success criteria
`vault-map.dnalab.yaml` names a live comlab reader for every consumer edge; T-VLIVE-4
row is `pending` (runnable) and its anti-orphan gate passes on re-run.

## Progress hook
`VAULT_LIVE_PROGRESS.md` T-VLIVE-4b: Status=done, Files changed=2,
Verification="vehicle_dna edges → horizon_context_injector/projection; schema-version → SessionMetadata.schema_version; session correlation → aggregator session_id; T-VLIVE-4 unblocked".
