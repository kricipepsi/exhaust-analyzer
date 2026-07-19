# VINLab → Vault — PIPELINE PACK · START HERE

Read this first, every session, before any other action in the VIN vault pack.

**Pack:** VAULT (VINLab tier) · **Lab:** `labs/vinlab` · **Authored:** 2026-06-12 (architect)
**Pipeline spec:** `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md`
**Vault plan:** `Vault/VAULT_IMPLEMENTATION_PLAN.md`
**Driving skill:** `_skills/graph/4dlab-vault/`
**Template pack:** DTCLab (`DTC_VAULT_TASKS_START_HERE.md`) / GASLab — VINLab mirrors their decisions.

> **One rule above all (signal/noise):** nothing — no schema field, no graph edge, no vault
> frontmatter key — ships unless a **named, existing consumer** reads it on a real code path.
> "Future use" is not a consumer. A note with an empty `consumers` list is not ready to ship.

---

## 0. VINLab-specific paths — DO NOT copy OBDLab's paths blindly

VINLab shares GASLab/DTCLab's layout (wiki at `wiki/`, not `research/chunks/`), so the same path trap
applies. `build_lab_vault.py` defaults to OBDLab's layout for any **unregistered** lab:

| Corpus | OBD default (WRONG for VIN) | **VINLab actual path** |
|---|---|---|
| code | `labs/<lab>/<lab>/` | `labs/vinlab/vinlab/` ✓ (`decoder.py`, `models.py`, `db/`, `overlay/` ×5, `data/`) |
| tests | `labs/<lab>/tests/` | `labs/vinlab/tests/` ✓ (15 `test_*.py` under `tests/unit/`, fixtures + conftest) |
| wiki | `labs/<lab>/research/chunks/` | **`labs/vinlab/wiki/`** (4 files: `00_index.md`, `10_decode_scope_rules.md`, `11_engine_resolution.md`, `12_brand_cylinder_rules.md`) |
| docs | `labs/<lab>/docs/` | `labs/vinlab/docs/` ✓ — **6 design docs** (HLD/DLD/LLD/ADR/BDD/PRD) + `VIN_VOCABULARY.md` |
| graph | `labs/<lab>/graphify-out/graph.json` (single) | **four-tier** `labs/vinlab/graph/v2_code|v2_tests/` (to be built; today only `graph/v2_current/`, `graph/v1_baseline/`, `DIFF_REPORT.md` exist — **frozen**) |

`build_lab_vault.py` has **no `vinlab` entry** in `LAB_SRC_PATHS` (only `obdlab`, `gaslab`, `dtclab`,
`symptomlab`), so a VIN build falls through to OBD's `research/chunks` default and aborts on the missing
dir and the missing `v2_wiki`/`v2_docs` graphs. **T-VIN-PATHS-1** adds the one-entry override (mirroring
the `gaslab`/`dtclab` entries) and is a hard blocker on **T-VIN-VAULT**.

**Frozen canonical graphs:** `graph/v2_current/` and `graph/v1_baseline/` are the existing single
graphs (with `DIFF_REPORT.md`). They are **canonical — never re-extracted.** Phase-3 builds the **new**
`v2_code` / `v2_tests` tier dirs only and leaves the frozen dirs byte-unchanged.

## 1. Scope trims applied to this pack (owner direction 2026-06-12)

- **Code-clean + tests-green are DONE (owner: "code was checked so skip").** VINLab's code track was
  finished under the DNA-family tri-module work and its audit record
  `labs/dnalab/docs/audits/AUDIT_2026-06-12_trimodule_dna_vin_symptom.md`:
  - `T-DNA-12` decomposed `decoder.py::decode_vin_payload()` into named private helper seams
    (behaviour-preserving) — clean module seams ⇒ clean code graph communities;
  - `T-DNA-13` applied the audit clarity fixes (`to_json` naming, checksum comment, magic strings);
  - `T-DNA-TH-2` added the isolation harness — per-module unit tests for `overlay/horizon.py`,
    `stress_rpm.py`, `switches.py` plus a mini-fixture `data_dir`, removing the test `skip`s.

  All three are `done` in `labs/dnalab/tasks/PROGRESS.md` (173 vin tests green, no test edits). So the
  Phase-1 **CODE-CLEAN** and **TESTS-GREEN** rows ship `done` here as pointers — **not** re-authored as
  fresh work. This is GASLab's trimmed path (guide §7.3 swing factor), not DTCLab's full fresh-lab path.
  > **Re-confirm at run time, do not re-do:** the CODEPREP/TESTPREP sessions should `pytest -q` once to
  > confirm the suite is still green on the current checkout before auditing; if it is not, STOP and
  > surface it — do not start the prep on a red suite.
- **DOCS-V2 is DONE.** All six design docs are already v2 and self-describe as "reflects shipped code":
  `HLD/DLD/LLD` v2.0, `BDD` v2 (scenarios grounded in decoder + fixtures), `ADR` v2 (back-filled from
  the sibling-split rework), `PRD` **v2.1 dated 2026-06-12**. No reconcile task is needed; the **DOCS-V2**
  row ships `done` and unblocks **DOCPREP**. `VIN_VOCABULARY.md` has its own `_vocabulary/` vault home and
  is **excluded** from the docs tier (see `T-VIN-DOCPREP`).
- **"Skip graph testing" → mirror GAS/DTC.** The Pass-3 LLM prose graphs (`v2_wiki`, `v2_docs`) are
  **waived**, and the graph-review cross-check tier (the OBDLab `T-VAULT-DOCGRAPH-2 / WIKIGRAPH-1 /
  CODEGRAPH-1` equivalents) is **not authored**. Phase-3 still runs the cheap, no-token,
  no-re-extraction **health-check** (`eval-*-graph` Part-A only) inline as build verification. The vault
  copies wiki/docs as raw `.md` + injected frontmatter (no prose graph), exactly as GAS/DTC were built.

## 2. The chain (run in dependency order — one task per session)

```
PHASE 1  T-VIN-CODE-CLEAN     DONE — covered by T-DNA-12/13/TH-2 + tri-module audit   coder
         T-VIN-TESTS-GREEN    DONE — 173 vin tests green (T-DNA-TH-2, no skips)        coder
         T-VIN-DOCS-V2        DONE — 6 docs already v2 (PRD v2.1, 2026-06-12)          author
              │ (wiki: confirm wiki/ current — no task)
PHASE 2  T-VIN-CODEPREP       4dlab-code-prep on labs/vinlab/vinlab/   ← (code-clean done)  coder
         T-VIN-TESTPREP       4dlab-code-prep on labs/vinlab/tests/    ← (tests-green done) coder
         T-VIN-WIKIPREP       4dlab-wiki-prep on labs/vinlab/wiki/     ← (wiki current)     author
         T-VIN-DOCPREP        DONE — 6 docs exploded/anchored under graph/v2_docs/ingest_ready  author
              │ (prep done per corpus)
PHASE 3  T-VIN-GRAPH-AST      graphify code+tests → graph/v2_code, v2_tests ← CODEPREP+TESTPREP  coder
         (T-VIN-GRAPH-LLM     waived — "skip graph testing"; prose graphs not built, mirror GAS/DTC)
              │
PHASE 4  T-VIN-PATHS-1        DONE — vinlab entry added to LAB_SRC_PATHS (wiki/, code+tests tiers)  coder
         T-VIN-VAULT          vault-map.vinlab.yaml + dry-run + build + bases ← GRAPH-AST + PATHS-1 author
```

The four corpora are independent until they converge at the vault, so within a phase the sessions run in
any order. **PATHS-1 has no corpus dependency** and can run any time before VAULT.

## 3. Pack ledger (source of truth — the next task is the first `pending` row whose Blocked-by are all `done`)

| ID | Task file | Status | Blocked by | Lane | Notes |
|---|---|---|---|---|---|
| T-VIN-CODE-CLEAN | — (no file; DNA-family) | done | — | coder | Covered by `T-DNA-12` (decoder seams) + `T-DNA-13` (clarity) + tri-module audit `labs/dnalab/docs/audits/AUDIT_2026-06-12_trimodule_dna_vin_symptom.md`. Owner: "code was checked so skip". |
| T-VIN-TESTS-GREEN | — (no file; DNA-family) | done | — | coder | `T-DNA-TH-2` isolation harness: per-module tests for horizon/stress_rpm/switches + mini `data_dir`; 173 vin tests green, skips removed. |
| T-VIN-DOCS-V2 | — (no file; pre-reconciled) | done | — | author | All 6 design docs already v2 reflecting shipped code (HLD/DLD/LLD v2.0, BDD v2, ADR v2, PRD v2.1 2026-06-12). No reconcile needed; unblocks DOCPREP. |
| T-VIN-CODEPREP | `T-VIN-CODEPREP_ast_legibility_audit_package.md` | done | T-VIN-CODE-CLEAN | coder | 4dlab-code-prep probe→audit→report on `vinlab/vinlab/`; explicit package export surfaces added; gate recorded in `progress_notes/T-VIN-CODEPREP.md`. |
| T-VIN-TESTPREP | `T-VIN-TESTPREP_ast_legibility_audit_tests.md` | done | T-VIN-TESTS-GREEN | coder | 4dlab-code-prep scoped to `tests/`; static import + two fixture/data path legibility fixes applied; gate recorded in `progress_notes/T-VIN-TESTPREP.md`. |
| T-VIN-WIKIPREP | `T-VIN-WIKIPREP_explicit_relations_wiki.md` | done | — | author | 2026-06-13: 4dlab-wiki-prep run over 4 chunks completed, 58 relation lines, proposals kept as proposals. |
| T-VIN-DOCPREP | `T-VIN-DOCPREP_doc_prep_design_docs.md` | done | T-VIN-DOCS-V2 | author | 2026-06-13: 4dlab-doc-prep run on the explicit 6 design docs; 68 chunks under `graph/v2_docs/ingest_ready/`; `VIN_VOCABULARY.md` excluded; no graphify/graph.json. |
| T-VIN-GRAPH-AST | `T-VIN-GRAPH-AST_graphify_code_and_tests.md` | done | T-VIN-CODEPREP, T-VIN-TESTPREP | coder | 2026-06-13: built `v2_code` (150n/255e) + `v2_tests` (542n/567e), offline AST; dangling=0 both; CHECK only from isolated nodes, all explained as tree-sitter docstring/empty-`__init__` artifacts (owners present+wired); frozen graphs byte-identical; no source edit. |
| T-VIN-GRAPH-LLM | — (no file) | waived | T-VIN-WIKIPREP, T-VIN-DOCPREP | — | "skip graph testing": prose Pass-3 graphs not built; Phase-2 wiki/doc prep is sufficient. |
| T-VIN-PATHS-1 | `T-VIN-PATHS-1_register_vinlab_source_paths.md` | done | — | coder | 2026-06-13: added `vinlab` entry to `LAB_SRC_PATHS` (wiki/, `v2_code`+`v2_tests`). 4 existing labs' dry-runs byte-identical; VIN dry-run resolves all 6 disk paths, stops only at missing `vault-map.vinlab.yaml` (T-VIN-VAULT). One-entry diff; no graphify/edit. Follow-up flagged: add `vinlab` to the line-345 PROVENANCE cosmetic tuple at T-VIN-VAULT. |
| T-VIN-VAULT | `T-VIN-VAULT_build_vinlab_vault.md` | done | T-VIN-GRAPH-AST, T-VIN-PATHS-1 | author | 2026-06-13: built vault-map.vinlab.yaml + built vocabulary + built vinlab vault tier + updated System-Map.md and PROVENANCE.md; prose graphs waived. |

## 4. Non-negotiables (carry from VINLab + Vault rules)

- **graphify is a SANCTIONED step only inside T-VIN-GRAPH-AST**, scoped to a specific package/dir,
  building the **new** tier dirs. It is **still forbidden** as a side-effect of any other task, and never
  re-extracts the frozen `graph/v2_current/` or `graph/v1_baseline/`.
- **`consumers` is architect-named, never auto-derived from the graph.** Empty list = not ready.
- **No cross-lab Python imports.** VINLab emits `VinDNA`/`VehicleDNA`; downstream labs read it through
  their own local `DnaView` mirror types — never `import vinlab` from another lab.
- **Signal/noise at the edge:** every `CONSUMES`/`VERIFIES` line a prep skill appends must name a real,
  existing code path or test. The `fuel_type` E5/E10 item is a **proposal** (gaslab wiki §1.4, `T-DNA-6`)
  — it stays labelled a proposal and is **never** framed as a live consumer.
- **One task per session.** Fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/<id>.md`, flip
  the ledger row to `done`, then STOP. Coder lane runs the inner loop (`ruff`→`pyright`→`pytest -x -q`)
  after every edit; the prep/graph/vault lanes are graph-tooling (no lab inner-loop) per each task's role note.

## 5. Named downstream consumers (use these, grep-confirm before framing — VAULT step)

VINLab's contract surface is `VinDNA` / `VehicleDNA`; downstream labs read it via their local `DnaView`
mirrors. Confirm each by grep before framing a note on it:

- `rated_rpm` → `ObdLabDnaView.rated_rpm` → OBDLab RPM ceiling (`T-DNA-3`, source DBS P14).
- CoC / `Emissions` fields → GASLab CoC threshold tables via the projector (`T-DNA-4`).
- `model` → `DtcLabDnaView.model` (DBS variance check, `T-DNA-5`).
- `load_state` / `engine_state` → DNALab `assembly.py` triage required keys (`T-DNA-2`).
- `air_metering` (`AirMeteringArchitecture`), `upstream_o2_type`, `induction_type` → OBDLab/GASLab
  perception overlays (the `overlay/` classifiers).

> **Do NOT frame** a note whose only "consumer" would be the `fuel_type` E5/E10 **proposal** — a proposal
> is not a live consumer. Leave such a note `plain:` or keep the field labelled a proposal.

## 6. Follow-ups for the owner (not authored as pack tasks)

- A VINLab-vault-pack row should be added to the bootstrap table in `4DLab/CLAUDE.md` pointing here.
- If the owner later lifts "skip graph testing" for VINLab (as was done for SymptomLab), the prose Pass-3
  graphs (`v2_wiki`/`v2_docs`) + cross-check tier would be authored then — out of scope now.
- **Out-of-package `pyright` failures (surfaced by the T-VIN-CODEPREP run, 2026-06-12).** The top-level
  data-loading scripts `dump_schema.py`, `load_tecdoc.py`, `mysql_bridge.py`, `setup_tecdoc_db.py` and
  `tools/*.py` fail a default/full `pyright` on missing optional deps (MySQL / pyngrok). They live
  **outside** `labs/vinlab/vinlab/`, are **never copied into the vault** (the code tier is the package
  only), and are not in any pack task's scope — so this is a **pre-existing repo condition, not a pack
  gate blocker.** If the owner wants it cleaned (type-ignore stubs or an optional-dep guard), it needs its
  own task spec with the consumer named; it does **not** belong in any CODEPREP/GRAPH/VAULT diff.
