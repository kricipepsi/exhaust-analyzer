# T-DNAV-WIKIPREP — Progress Notes

**Status:** done · **Date:** 2026-06-13 · **Lane:** author (architect session)
**Pack:** VAULT (DNALab) · **Task file:** `Vault/tasks/T-DNAV-WIKIPREP_explicit_relations_wiki.md`

## Plan

`4dlab-wiki-prep relations → labels → roster → verify` over 10 dnalab wiki notes. Mixed-type corpus: 5 contract-spec notes (00, 10–13) frame live COMLab consumers with `CONSUMED_BY`/`VERIFIES` lines; 5 research-prose notes (90–94) frame every prior as a COMLab-A/B/F PROPOSAL — none as live. Append-only trailers, no graphify, no file moves, no schema fields.

## VERIFICATION GATE

### Block coverage
- **10/10** chunks carry exactly one `## Graph relations (explicit)` block — zero missing, zero duplicates.
- **10/10** chunks carry exactly one `## Core Entities` block — zero missing, zero duplicates.
- Zero empty relation blocks.

### Relation lines
Total: **123** bold relation lines across the corpus.

| Chunk | Lines |
|---|---:|
| `00_index.md` | 9 |
| `10_vehicle_dna_envelope.md` | 11 |
| `11_schema_versioning.md` | 12 |
| `12_assembly_contract.md` | 13 |
| `13_session_identity.md` | 13 |
| `90_research_index.md` | 15 |
| `91_operator_symptom_predictiveness.md` | 12 |
| `92_symptom_vocabulary_and_context.md` | 13 |
| `93_vin_decode_resolution.md` | 10 |
| `94_reference_data_and_aftermarket.md` | 15 |

### Append-only confirmed
No sourced prose, numeric literals, tables, citations, or frontmatter were rewritten. Trailer sections appended at end of each file; body text before `## Graph relations (explicit)` remains the original sourced content.

### Consumer checks (contract notes — live)
- `VehicleDNA` CONSUMED_BY `COMLab OrchestratorInboundRequest.vehicle_dna` — grep-confirmed in `labs/comlab/comlab/schemas/ingestion.py`, `labs/comlab/comlab/core/lab_pipeline_aggregator.py` (live code).
- `SCHEMA_VERSION` CONSUMED_BY `COMLab schema-version gate` — grep-confirmed in COMLab HLD (`schema_version` gate step), `dnalab/models.py` (live constant).
- `engine_state` CONSUMED_BY `COMLab symptom_router.route_symptom()` — grep-confirmed in `labs/comlab/comlab/core/symptom_router.py:32` (live function, called from `lab_pipeline_aggregator.py`).
- `session_id` / `timestamp` CONSUMED_BY `COMLab session correlation` — confirmed via `VehicleDNA.new()` in `dnalab/models.py`; COMLab correlates via `OrchestratorInboundRequest`.
- `build_vehicle_dna()` VERIFIES triage required keys — grep-confirmed in `dnalab/assembly.py:32-37` (fail-fast check before decode).
- `VehicleDNA.from_json_payload()` VERIFIES schema_version match — grep-confirmed in `dnalab/models.py:93-101` (strict-match ValueError gate).
- `dnalab/tests/unit/` — 27 tests across 4 modules (test_assembly.py 11, test_models.py 10, test_vehicledna_roundtrip.py 5, test_assembly_integration.py 1). All test references in VERIFIED_BY lines resolve to real test functions.

### Proposal handling (research notes — 90–94)
- Every relation line in 90–94 labelled **PROPOSAL** — none framed as a live `CONSUMES`/`VERIFIES`.
- `COMLab-A` (tier_1,tier_2 routing), `COMLab-B` (report-trust cap + context modifiers), `COMLab-F` (symptom-prior weighting) all marked `STATUS: PROPOSAL (not live)`.
- `COMLab proposals registry` (`labs/comlab/comlab/config/proposals/`) named as the canonical home for all research findings.
- Genuine gaps (no open complaint→fix dataset, no ZZZ-dropoff table, no post-2020 remap survey for 1990–2010) recorded as `QUESTION`, not as findings.

### Orphan flags on research notes
The `verify` step would flag 90–94 lines as orphans (no live code path reads them). Per the task spec (START_HERE §0.4, §5), this is **expected** — COMLab-A/B/F are proposals, not live consumers. These orphan flags are recorded as expected, not as violations to fix.

## CODE REVIEW

- **Honesty gates held.** Relations stay within concepts already present in the wiki notes and the task's named consumer list. No fabricated live consumers for research notes.
- **Canonical labels assigned.** `DNAWIKI-00-INDEX`, `DNAWIKI-10-VEHICLE_DNA_ENVELOPE`, `DNAWIKI-11-SCHEMA_VERSIONING`, `DNAWIKI-12-ASSEMBLY_CONTRACT`, `DNAWIKI-13-SESSION_IDENTITY`, `DNAWIKI-90-RESEARCH_INDEX`, `DNAWIKI-91-OPERATOR_SYMPTOM_PREDICTIVENESS`, `DNAWIKI-92-SYMPTOM_VOCABULARY_CONTEXT`, `DNAWIKI-93-VIN_DECODE_RESOLUTION`, `DNAWIKI-94-REFERENCE_DATA_AFTERMARKET`. Also: `VehicleDNA`, `SCHEMA_VERSION`, `build_vehicle_dna()`, `COMLab OrchestratorInboundRequest`, `symptom_router.route_symptom()`, `COMLab-A/B/F`.
- **Proposal vs live preserved.** Contract notes frame only live consumers; research notes frame only proposals. `fuel_type` stays proposal-only (COMLab-E). No proposal promoted to live; no live consumer downgraded to proposal.
- **No graph side effects.** No graph build, graph update, schema field, or source-code change was made.
- **No file moves/renames.** All 10 wiki notes remain at their canonical `labs/dnalab/wiki/` paths.
