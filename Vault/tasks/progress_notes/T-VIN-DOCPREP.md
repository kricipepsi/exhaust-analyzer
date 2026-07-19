# T-VIN-DOCPREP — progress note

**Status:** `pending` · **Pack:** VAULT (VINLab)
Task spec: `Vault/tasks/T-VIN-DOCPREP_*.md` · Pack ledger: `Vault/tasks/VIN_VAULT_TASKS_START_HERE.md`

## Plan

Run `4dlab-doc-prep` (explode -> tables -> anchor -> relations -> verify) on exactly six VINLab v2
design docs: `HLD_VINLab.md`, `DLD_VINLab.md`, `LLD_VINLab.md`, `ADR_VINLab.md`,
`BDD_VINLab.md`, and `PRD_VINLab.md`. Emit one hierarchy-preserving subtree per doc under
`labs/vinlab/graph/v2_docs/ingest_ready/<doc>/...`. Use the explicit six-file list, not a
`docs/*.md` glob, so `docs/VIN_VOCABULARY.md` remains excluded for the later `_vocabulary/` vault
home and moved/handoff/superseded docs are not ingested. Copy source section bodies without editing
the source docs; convert non-BDD markdown tables to entity blocks; anchor every chunk with module,
section, and parent-doc lineage; append `## Graph relations (explicit)` lines whose
`CONSUMES`/`VERIFIES` paths are backed by real VINLab/COMLab/OBDLab/GASLab code or unit tests.
No graphify run, no `graph.json`, and no writes to the frozen `v2_current` / `v1_baseline` dirs.

## VERIFICATION GATE

- [x] **Exactly six subtrees** — `ADR_VINLab BDD_VINLab DLD_VINLab HLD_VINLab LLD_VINLab PRD_VINLab`.
- [x] **No excluded file ingested** — `VIN_VOCABULARY` is absent from `ingest_ready/`.
- [x] **Every chunk has an anchor** — 68/68 files start with `> **Context:**`.
- [x] **Every chunk has exactly one relation block** — 68/68 files have one non-empty `## Graph relations (explicit)` block.
- [x] **No prose graph built** — `labs/vinlab/graph/v2_docs/graph.json` does not exist.
- [x] **CONSUMES/VERIFIES grep-backed** — relation lines name shipped code/test paths, including `vinlab.decoder`, `vinlab.models`, `overlay/*`, `comlab.projection`, `lab_dna_views`, and `tests/unit/test_*.py`.
- [x] **Source/frozen discipline** — generated files are under `graph/v2_docs/ingest_ready/**`; `v1_baseline` and `v2_current` are clean in targeted git status. The VIN docs had pre-existing uncommitted changes before this run and were not edited by the generator.

### Coverage report

| Source doc | `##` sections | Chunks written | Tables converted | Relation lines |
|---|---:|---:|---:|---:|
| HLD_VINLab.md | 9 | 10 | 5 | 33 |
| DLD_VINLab.md | 11 | 12 | 8 | 37 |
| LLD_VINLab.md | 13 | 14 | 1 | 40 |
| ADR_VINLab.md | 11 | 12 | 1 | 32 |
| BDD_VINLab.md | 10 | 11 | 0 | 23 |
| PRD_VINLab.md | 8 | 9 | 3 | 20 |
| **Total** | **62** | **68** | **18** | **185** |

Includes 6 preambles (`00_Preamble.md`), one per source doc.

**Relation lines by predicate:**
DESCRIBES 68 · VERIFIES 59 · OWNED_BY 24 · CONSUMES 17 · IMPLEMENTS 10 · MIRRORS_CONTRACT_IN 3 ·
PROPOSAL 2 · DERIVED_FROM 1 · ENUMERATES 1

## CODE REVIEW

### Per-doc chunk counts

| Doc | Chunks | Sections covered | Notable |
|---|---:|---|---|
| HLD_VINLab | 10 | Preamble + S1-S9 | Pipeline, checksum, WMI/year, engine overlays, downstream consumers |
| DLD_VINLab | 12 | Preamble + S1-S11 | Module map, enums, nested dataclasses, VinDNA, decoder, overlays, SQL isolation, tests |
| LLD_VINLab | 14 | Preamble + S1-S13 | Exact helper-level rules for checksum, WMI/year/engine, stress RPM, horizon, O2, cylinder fallback |
| ADR_VINLab | 12 | Preamble + ADR-0001..0010 + references | ADR index table converted; each ADR ties to implementer/test where live |
| BDD_VINLab | 11 | Preamble + 9 features + traceability | BDD examples left intact; features map to named unit-test files |
| PRD_VINLab | 9 | Preamble + S1-S8 | PRD field/assumption tables converted; proposal-only `fuel_type` remains labelled as proposal |

### Exclusions honoured

- `docs/VIN_VOCABULARY.md` — excluded; later vault step owns `_vocabulary/VIN_VOCABULARY.md`.
- Non-design docs and moved VIN research/inventory files — excluded by explicit six-file list.
- Frozen `graph/v2_current/` and `graph/v1_baseline/` — not written.

### Run artifact

`scratch/doc_prep_vin.py` records the deterministic generation used for this run and can be rerun
without graphify or API calls.
