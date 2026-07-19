# T-DNAV-VAULT — progress note

**Status:** `done` · **Date:** 2026-06-13 · **Pack:** VAULT (DNALab) · **Lane:** author (architect session)
Task spec: `Vault/tasks/T-DNAV-VAULT_build_dnalab_vault.md` · Pack ledger: `Vault/tasks/DNA_VAULT_TASKS_START_HERE.md`

## Plan

1. Author `assets/vault-map.dnalab.yaml` mapping the four design documents (`PRD_DNALab.md`, `HLD_DNALab.md`, `LLD_DNALab.md`, `DLD_DNALab.md`) and the four wiki notes (`10_vehicle_dna_envelope.md`, `11_schema_versioning.md`, `12_assembly_contract.md`, `13_session_identity.md`) to their explicit `implements`, `consumers`, and `drift_guards`, and placing `ADR_DNALab.md`, `BDD_DNALab.md`, `DNA_VOCABULARY.md`, `00_index.md`, and the research notes (`90–94`) in the `plain` category.
2. Update `vault-map.vocabulary.yaml` to include `DNA_VOCABULARY.md` with its implements, consumers, and drift guards.
3. Run the dry-runs and execute the vault building scripts to copy and frame the notes, and build the standalone vocabulary note `Vault/_vocabulary/DNA_VOCABULARY.md`.
4. Update `Vault/System-Map.md` and `Vault/_meta/PROVENANCE.md` with the new DNALab entries.

## VERIFICATION GATE

- [x] **Vault directories populated**: `Vault/labs/dnalab/` correctly contains `code/`, `tests/`, `wiki/`, and `docs/`.
- [x] **Vocabulary area built**: `Vault/_vocabulary/DNA_VOCABULARY.md` successfully created with §-anchored frontmatter.
- [x] **Signal/noise gate held**: Every single framed note in `vault-map.dnalab.yaml` has at least one named, grep-confirmed downstream consumer on a real code path (COMLab ingestion / OrchestratorInboundRequest).
- [x] **No graph re-extraction**: Sourced code graphs under `labs/dnalab/graph` are completely untouched (zero diff).
- [x] **Bases render cleanly**: Obsidian bases and views copied/installed, System-Map refreshed, and PROVENANCE updated with correct MD5 hashes.
- [x] **Idempotency**: Re-running the scripts updates vault files in-place without duplication.

## CODE REVIEW

- **Map validation**: Map authored based on Phase-2 prep plus code/test graphs.
- **Consumer confirmation**: Every consumer in the map is backed by live symbols (e.g. `OrchestratorInboundRequest.vehicle_dna`, `SCHEMA_VERSION`, `build_vehicle_dna`, `session correlation`).
- **Proposals preserved**: `fuel_type` is kept as a proposal and not mapped to live consumers; research index and notes (`90-94`) are placed under the `plain` list (not framed) since their only consumer is the COMLab-A/B proposal.
- **No out-of-scope files**: `DNA_VOCABULARY.md` and indexes correctly excluded from the framed docs and mapped under vocabulary/plain lists.
