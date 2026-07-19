# T-DNAV-DOCPREP — Progress Notes

**Status:** done · **Date:** 2026-06-13 · **Lane:** author (architect session)
**Pack:** VAULT (DNALab) · **Task file:** `Vault/tasks/T-DNAV-DOCPREP_doc_prep_design_docs.md`

## Plan

`4dlab-doc-prep explode → tables → anchor → relations → verify` on the six DNALab design docs in `labs/dnalab/docs/`. Explicit file list: HLD_DNALab.md, DLD_DNALab.md, LLD_DNALab.md, ADR_DNALab.md, BDD_DNALab.md, PRD_DNALab.md. DNA_VOCABULARY.md excluded (vocab tier, → T-DNAV-VAULT step 0). Output under `labs/dnalab/graph/v2_docs/ingest_ready/`. No graphify, no source doc edits, no schema fields.

## VERIFICATION GATE

### Explode
- **51 chunks** across 6 doc subtrees (HLD: 9, DLD: 8, LLD: 8, ADR: 9, BDD: 8, PRD: 9)
- Every `##` section produced exactly one chunk; zero lost, zero double-explode
- Six doc dirs confirmed; DNA_VOCABULARY excluded

### Tables (logic tables → entity blocks)
Tables converted in 4 chunks:
- **DLD §2** (`2_modelspy_VehicleDNA_frozen_dataclass.md`): VehicleDNA 5-field grid → 5 entity blocks per field; Classmethods grid → 4 method entity blocks
- **DLD §3** (`3_modelspy_fromjsonpayload_contract.md`): Failure/Exception grid → 3 failure entity blocks
- **DLD §5** (`5_Exceptions_propagated_not_defined_here.md`): Exception grid → 4 exception entity blocks
- **PRD §7** (`Section_7_Solution.md`): VehicleDNA 5-field grid → 5 entity blocks per field; Assumptions grid → 3 assumption entity blocks

Narrative tables (HLD §6 consumer table, HLD §7 NFR table, ADR roster, BDD traceability) left as-is per skill rule.

### Anchors
- **51/51** chunks carry a `> **Context:**` anchor header naming module (DNALab) + parent document
- Zero missing anchors

### Relations
- **266** bold relation lines across all 51 chunks, zero empty blocks
- Every chunk carries exactly one `## Graph relations (explicit)` block

| Doc | Relation lines |
|---|---:|
| HLD_DNALab | 48 |
| DLD_DNALab | 55 |
| LLD_DNALab | 36 |
| ADR_DNALab | 49 |
| BDD_DNALab | 32 |
| PRD_DNALab | 46 |
| **Total** | **266** |

### Consumer checks (CONSUMES/VERIFIES grep-backed)
- `VehicleDNA` — confirmed in `dnalab/models.py` (class VehicleDNA, line 1 match)
- `build_vehicle_dna` — confirmed in `dnalab/assembly.py` (def build_vehicle_dna, line 1 match)
- `SCHEMA_VERSION` — confirmed in `dnalab/models.py` (6 references)
- All BDD VERIFIES lines name real test modules (`test_assembly.py`, `test_models.py`, `test_vehicledna_roundtrip.py`)
- All CONSUMES targets reference real code paths (COMLab OrchestratorInboundRequest, vinlab.decode, symptomlab.resolve)

### Proposal discipline
- `symptom_dna` → COMLab `fault_atlas_router` symptom prior: labelled **PROPOSAL — COMLab-A, not live** (in DLD §2)
- `fuel_type` → COMLab-E: labelled **proposal** (in ADR-0007, PRD §8)
- Zero proposals framed as live consumers; zero live consumers downgraded to proposals
- Zero unflagged orphans

### Source docs + frozen graphs untouched
- Zero edits to `labs/dnalab/docs/*.md` (source docs read-only; pre-existing git modifications are from prior sessions, not this task)
- Frozen `graph/v2_current/` and `graph/v1_baseline/` byte-unchanged
- No graphify, no graph.json written, no schema field added

### Exclusions honoured
- `DNA_VOCABULARY.md` excluded from doc-prep (vocab tier, belongs to `--vocab` in T-DNAV-VAULT)
- No `docs/*.md` glob used — explicit six-doc list only

## CODE REVIEW

- **Honesty gates held.** Every CONSUMES/VERIFIES line references a real, existing code path or test, grep-confirmed. No fabricated consumers. Proposals labelled as proposals.
- **Table conversion consistent.** All logic-bearing tables (fields, failures, exceptions) converted to entity blocks following the skill's `### Field:` / `### Exception:` / `### Failure:` pattern. Narrative tables left as markdown grids.
- **Anchors consistent.** Every chunk's `> **Context:**` header names DNALab module + parent document + boundary contract `SEMANTIC_CONTRACT.md §4.3`.
- **Relations canonical.** Entities use canonical labels (VehicleDNA, build_vehicle_dna(), SCHEMA_VERSION, COMLab OrchestratorInboundRequest) matching the shipped code. Predicate vocabulary follows the skill's table (CONSUMES, VERIFIES, GATED_BY, DELEGATES_TO, OWNED_BY, DESCRIBES, SUPERSEDES, MIRRORS_CONTRACT_IN, DERIVED_FROM, PROPAGATED_FROM, ROUTES_TO, EXPORTS, ENUMERATES, CONSOLIDATES).
- **No graph side effects.** No graph build, graph update, or graphify run. No source doc edits. Output isolated to `graph/v2_docs/ingest_ready/`.
