# DNALab → Vault — PIPELINE PACK · START HERE

Read this first, every session, before any other action in the DNA vault pack.

**Pack:** VAULT (DNALab tier) · **Lab:** `labs/dnalab` · **Authored:** 2026-06-13 (architect)
**Pipeline spec:** `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md`
**Vault plan:** `Vault/VAULT_IMPLEMENTATION_PLAN.md`
**Driving skill:** `_skills/graph/4dlab-vault/`
**Template pack:** VINLab (`VIN_VAULT_TASKS_START_HERE.md`) — DNALab is its direct sibling (same
DNA-family code, same trimmed state) and mirrors its decisions. GASLab/DTCLab are the wider model.

> **One rule above all (signal/noise):** nothing — no schema field, no graph edge, no vault
> frontmatter key — ships unless a **named, existing consumer** reads it on a real code path.
> "Future use" is not a consumer. A note with an empty `consumers` list is not ready to ship.

---

## 0. DNALab-specific facts — read before copying VIN/OBD blindly

### 0.1 Task-ID prefix is `T-DNAV-`, NOT `T-DNA-` (collision guard)

The `T-DNA-*` IDs are **already taken** by the DNA-family content pack (`T-DNA-1..13`, `T-DNA-TH-1..3`)
tracked in `labs/dnalab/tasks/PROGRESS.md`. This vault pack is a **different pack**, so every ID here uses
the prefix **`T-DNAV-`** (DNA-Vault) to avoid silently overwriting a content-pack row. Do not "tidy" these
back to `T-DNA-*`.

### 0.2 DNALab is the composition layer — tiny package, sibling-fed payloads

DNALab is the umbrella lab that composes `VinDNA` (from VINLab) + `SymptomDNA` (from SymptomLab) into the
`VehicleDNA` envelope. Its own package is small:

| File | Lines | Public surface |
|---|---|---|
| `dnalab/__init__.py` | 13 | `__all__ = ["build_vehicle_dna", "VehicleDNA"]` (already explicit ✓) |
| `dnalab/assembly.py` | 46 | `build_vehicle_dna(vin, triage) -> VehicleDNA` |
| `dnalab/models.py` | 92 | `VehicleDNA` dataclass · `.new()` · `.to_json_payload()` · `.to_json()` · `.from_json_payload()` · `SCHEMA_VERSION = "1.2"` |

> **No domain `StrEnum`s live in dnalab.** DNALab composes sibling dicts/views; the enums
> (`EngineState`, `Horizon`, …) are owned by VINLab/SymptomLab. The CODEPREP "domain states as real
> enums" lever therefore does **not** apply here — its absence is expected, **not** a violation to fix.

### 0.3 Paths — DNALab shares the GASLab/DTCLab layout (wiki at `wiki/`)

`build_lab_vault.py` defaults any **unregistered** lab to OBDLab's layout, which is WRONG for DNALab:

| Corpus | OBD default (WRONG for DNA) | **DNALab actual path** |
|---|---|---|
| code | `labs/<lab>/<lab>/` | `labs/dnalab/dnalab/` ✓ (`__init__.py`, `assembly.py`, `models.py`) |
| tests | `labs/<lab>/tests/` | `labs/dnalab/tests/` ✓ (4 modules under `tests/unit/`, 27 tests; `conftest.py` + `fixtures/`) |
| wiki | `labs/<lab>/research/chunks/` | **`labs/dnalab/wiki/`** (10 notes — see §0.4) |
| docs | `labs/<lab>/docs/` | `labs/dnalab/docs/` ✓ — **6 design docs** (HLD/DLD/LLD/ADR/BDD/PRD) + `DNA_VOCABULARY.md` |
| graph | single `graphify-out/graph.json` | **four-tier** `labs/dnalab/graph/v2_code|v2_tests/` (to build; today only `graph/v2_current/`, `graph/v1_baseline/`, `DIFF_REPORT.md` exist — **frozen**) |

`LAB_SRC_PATHS` in `build_lab_vault.py` has `obdlab`, `gaslab`, `dtclab`, `symptomlab` — **no `dnalab`**
(and no `vinlab`). A DNA build falls through to OBD's `research/chunks` default and aborts on the missing
dir + missing `v2_wiki`/`v2_docs` graphs. **T-DNAV-PATHS-1** adds the one-entry override (mirroring
`gaslab`/`dtclab`) and is a hard blocker on **T-DNAV-VAULT**.

**Frozen canonical graphs:** `graph/v2_current/` and `graph/v1_baseline/` (with `DIFF_REPORT.md`) are
**canonical — never re-extracted.** Phase-3 builds the **new** `v2_code` / `v2_tests` tier dirs only and
leaves the frozen dirs byte-unchanged.

### 0.4 The wiki is **mixed type** — this is why prose graphs are waived (see §1)

The 10 wiki notes split cleanly into two kinds:

```
10–13  CONTRACT SPEC   10_vehicle_dna_envelope · 11_schema_versioning ·       overlaps the code+docs
                       12_assembly_contract · 13_session_identity             graphs (low new signal)
90–94  RESEARCH PROSE  90_research_index · 91_operator_symptom_predictiveness one consumer = COMLab-A/B
                       92_symptom_vocabulary_and_context · 93_vin_decode_     symptom prior, still a
                       resolution · 94_reference_data_and_aftermarket         PROPOSAL (not live yet)
```

The contract half re-derives what AST already extracts; the research half points almost entirely at
**proposal** consumers (COMLab-A/B), which signal/noise forbids framing as live. So WIKIPREP still makes
the relations explicit (and keeps proposals labelled proposals), but the LLM prose graph is **waived**.

## 1. Scope trims applied to this pack (mirrors VINLab, owner direction)

- **CODE-CLEAN + TESTS-GREEN are DONE.** DNALab's code track was finished under the DNA-family work:
  `T-DNA-7` (bump `VehicleDNA` `schema_version` → 1.2, round-trip the new fields), `T-DNA-13` (audit
  clarity fixes incl. `to_json` naming), and `T-DNA-TH-1` (assembly **isolation harness** — fake
  decode/resolve via monkeypatch, builders `make_vin_dna`/`make_symptom_dna`). All are `done` in
  `labs/dnalab/tasks/PROGRESS.md`. So **CODE-CLEAN** and **TESTS-GREEN** ship `done` here as pointer rows
  — **not** re-authored as fresh work (GASLab's trimmed path, guide §7.3).
  > **Re-confirm at run time, do not re-do:** the CODEPREP/TESTPREP sessions `pytest -q` once to confirm
  > the suite is still green on the current checkout before auditing. Baseline ~27 dnalab tests; the
  > `test_assembly_integration::test_real_pipeline_smoke` may **skip** if sibling labs (vinlab/symptomlab)
  > are not installed in the sandbox — a **skip is expected, not a gate failure**. Only a *failure* is a STOP.
- **DOCS-V2 is DONE.** All six design docs already self-describe as v2 reflecting shipped code: `HLD/DLD/LLD`
  v2.1, `BDD` v2 (scenarios grounded in the live suite), `ADR` v2 (refreshed 2026-06-12, `SCHEMA_VERSION =
  "1.2"` landed), `PRD` **v2.1 dated 2026-06-12**. No reconcile needed; **DOCS-V2** ships `done` and
  unblocks **DOCPREP**. `DNA_VOCABULARY.md` has its own `_vocabulary/` vault home and is **excluded** from
  the docs tier (see `T-DNAV-DOCPREP`).
- **"Skip graph testing" → mirror VIN/GAS/DTC.** The Pass-3 LLM prose graphs (`v2_wiki`, `v2_docs`) are
  **waived**, and the graph-review cross-check tier (the OBDLab `DOCGRAPH-2 / WIKIGRAPH-1 / CODEGRAPH-1`
  equivalents) is **not authored**. Phase-3 still runs the cheap, no-token, no-re-extraction
  **health-check** (`eval-*-graph` Part-A only) inline as build verification. The vault copies wiki/docs
  as raw `.md` + injected frontmatter (no prose graph), exactly as GAS/DTC/VIN were built. See §6 for the
  documented trigger that would lift this later.

## 2. The chain (run in dependency order — one task per session)

```
PHASE 1  T-DNAV-CODE-CLEAN     DONE — covered by T-DNA-7/13/TH-1                          coder
         T-DNAV-TESTS-GREEN    DONE — 27 dnalab tests green (T-DNA-TH-1 isolation harness) coder
         T-DNAV-DOCS-V2        DONE — 6 docs already v2 (PRD v2.1, ADR refreshed 2026-06-12) author
              │ (wiki: confirm wiki/ current — no task)
PHASE 2  T-DNAV-CODEPREP       4dlab-code-prep on labs/dnalab/dnalab/   ← (code-clean done)  coder
         T-DNAV-TESTPREP       4dlab-code-prep on labs/dnalab/tests/    ← (tests-green done) coder
         T-DNAV-WIKIPREP       4dlab-wiki-prep on labs/dnalab/wiki/     ← (wiki current)     author
         T-DNAV-DOCPREP        4dlab-doc-prep on the 6 design docs      ← T-DNAV-DOCS-V2     author
              │ (prep done per corpus)
PHASE 3  T-DNAV-GRAPH-AST      graphify code+tests → graph/v2_code, v2_tests ← CODEPREP+TESTPREP coder
         (T-DNAV-GRAPH-LLM     waived — "skip graph testing"; prose graphs not built, mirror VIN)
              │
PHASE 4  T-DNAV-PATHS-1        add dnalab entry to LAB_SRC_PATHS (wiki/, code+tests tiers)  ← (none) coder
         T-DNAV-VAULT          vault-map.dnalab.yaml + dry-run + build + bases ← GRAPH-AST + PATHS-1 author
```

The four corpora are independent until they converge at the vault, so within a phase the sessions run in
any order. **PATHS-1 has no corpus dependency** and can run any time before VAULT.

## 3. Pack ledger (source of truth — the next task is the first `pending` row whose Blocked-by are all `done`)

| ID | Task file | Status | Blocked by | Lane | Notes |
|---|---|---|---|---|---|
| T-DNAV-CODE-CLEAN | — (no file; DNA-family) | done | — | coder | Covered by `T-DNA-7` (schema bump 1.2) + `T-DNA-13` (clarity fixes) + `T-DNA-TH-1` (assembly isolation harness). Package is 3 files, already clean. |
| T-DNAV-TESTS-GREEN | — (no file; DNA-family) | done | — | coder | `T-DNA-TH-1` isolation harness: fake decode/resolve via monkeypatch, builders `make_vin_dna`/`make_symptom_dna`; 27 dnalab tests (4 modules). |
| T-DNAV-DOCS-V2 | — (no file; pre-reconciled) | done | — | author | All 6 design docs already v2 reflecting shipped code (HLD/DLD/LLD v2.1, BDD v2, ADR v2 2026-06-12, PRD v2.1 2026-06-12). No reconcile; unblocks DOCPREP. |
| T-DNAV-CODEPREP | `T-DNAV-CODEPREP_ast_legibility_audit_package.md` | done | T-DNAV-CODE-CLEAN | coder | `4dlab-code-prep` probe→audit→report on `dnalab/dnalab/`; 5 fixes applied (3 rationale + 2 docstrings), inner loop green. |
| T-DNAV-TESTPREP | `T-DNAV-TESTPREP_ast_legibility_audit_tests.md` | done | T-DNAV-TESTS-GREEN | coder | Zero violations — folded into CODEPREP (mirrors DTC). |
| T-DNAV-WIKIPREP | `T-DNAV-WIKIPREP_explicit_relations_wiki.md` | done | — | author | `4dlab-wiki-prep` over the 10 mixed-type notes; contract notes → code symbols (live), research notes → COMLab-A/B (kept **labelled proposals**). |
| T-DNAV-DOCPREP | `T-DNAV-DOCPREP_doc_prep_design_docs.md` | done | T-DNAV-DOCS-V2 | author | `4dlab-doc-prep` on the 6 docs (explicit file list; `DNA_VOCABULARY.md` excluded). |
| T-DNAV-GRAPH-AST | `T-DNAV-GRAPH-AST_graphify_code_and_tests.md` | done | T-DNAV-CODEPREP, T-DNAV-TESTPREP | coder | build `v2_code`/`v2_tests`; health-check Part-A only; never touch `v2_current`/`v1_baseline`. |
| T-DNAV-GRAPH-LLM | — (no file) | waived | T-DNAV-WIKIPREP, T-DNAV-DOCPREP | — | "skip graph testing": prose Pass-3 graphs not built; Phase-2 wiki/doc prep is sufficient. Lift trigger in §6. |
| T-DNAV-PATHS-1 | `T-DNAV-PATHS-1_register_dnalab_source_paths.md` | done | — | coder | add `dnalab` entry to `LAB_SRC_PATHS` mirroring `gaslab`/`dtclab` (wiki/, two AST tiers). |
| T-DNAV-VAULT | `T-DNAV-VAULT_build_dnalab_vault.md` | done | T-DNAV-GRAPH-AST, T-DNAV-PATHS-1 | author | vault-map.dnalab.yaml + dry-run + build + bases; `_vocabulary/DNA_VOCABULARY.md`; prose graphs waived. |

## 4. Non-negotiables (carry from DNALab + Vault rules)

- **graphify is a SANCTIONED step only inside T-DNAV-GRAPH-AST**, scoped to a specific package/dir,
  building the **new** tier dirs. It is **still forbidden** as a side-effect of any other task, and never
  re-extracts the frozen `graph/v2_current/` or `graph/v1_baseline/`.
- **`consumers` is architect-named, never auto-derived from the graph.** Empty list = not ready.
- **No cross-lab Python imports.** DNALab emits `VehicleDNA`; downstream COMLab reads it through its own
  local mirror types (`OrchestratorInboundRequest.vehicle_dna`) — never `import dnalab` from another lab.
  DNALab itself composes `VinDNA`/`SymptomDNA` from sibling labs as **payloads**, not via live imports of
  their logic (the isolation harness fakes them).
- **Signal/noise at the edge:** every `CONSUMES`/`VERIFIES` line a prep skill appends must name a real,
  existing code path or test. The research-wiki prior (COMLab-A/B) is a **proposal** — it stays labelled a
  proposal and is **never** framed as a live consumer (§0.4, §5).
- **One task per session.** Fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/<id>.md`, flip the
  ledger row to `done`, then STOP. Coder lane runs the inner loop (`ruff`→`pyright`→`pytest -x -q`) after
  every edit; the prep/graph/vault lanes are graph-tooling (no lab inner-loop) per each task's role note.

## 5. Named downstream consumers (use these, grep-confirm before framing — VAULT step)

DNALab's contract surface is the `VehicleDNA` envelope. Confirm each by grep before framing a note on it:

- `VehicleDNA` envelope → COMLab `OrchestratorInboundRequest.vehicle_dna` ingestion (`T-DNA-7`).
- `SCHEMA_VERSION` / `from_json_payload` mismatch raise → COMLab ingestion compatibility gate (the
  `schema_version` round-trip in `models.py`).
- `load_state` / `engine_state` triage required keys → `assembly.build_vehicle_dna` triage validation
  (`T-DNA-2`); `engine_state` → COMLab `symptom_router.route_symptom` (`T-DNA-10`, live).
- Composed `VinDNA` sub-payload → VINLab `DnaView` mirrors (rated_rpm/CoC/model — see VIN pack §5).
- Composed `SymptomDNA` sub-payload → COMLab `fault_atlas_router` symptom prior (COMLab-A — **proposal**).

> **Do NOT frame** a note whose only "consumer" would be the COMLab-A/B symptom-prior **proposal** — a
> proposal is not a live consumer. Leave such a note `plain:` or keep the field labelled a proposal. This
> is exactly why the research-prose half of the wiki (§0.4) is copied raw, not framed as live nodes.

## 6. Follow-ups for the owner (not authored as pack tasks)

- A DNALab-vault-pack row should be added to the bootstrap table in `4DLab/CLAUDE.md` pointing here.
- **Prose-graph lift trigger.** If/when COMLab-A/B (the symptom-prior readers) ship **live** (no longer
  proposals), the research-prose wiki half (`90–94`) gains real consumers — at that point the owner can
  lift "skip graph testing" for DNALab and author the `v2_wiki`/`v2_docs` Pass-3 graphs + cross-check tier
  in a dedicated session, the same way SymptomLab's skip was lifted when its wiki became canonical. Out of
  scope now.
- **DNA family doc/wiki refresh.** `labs/dnalab/tasks/PROGRESS.md` notes a deferred final-cleanup refresh
  of the per-lab doc sets (and `T-DNA-8`/`T-OIL-1` symptom-catalog work). If that lands after this pack is
  authored and materially changes `assembly.py`/`models.py` or the wiki, re-confirm DOCS-V2/wiki currency
  before the prep sessions run — it does not change the chain, only the freshness pre-check.
