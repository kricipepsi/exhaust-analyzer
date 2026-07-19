---
name: comlab-vault-prep
description: >
  COMLab-specific companion for the four Phase-2 ingestion-prep tasks of the
  COMLab → Vault pipeline pack (T-COM-CODEPREP, T-COM-TESTPREP, T-COM-WIKIPREP,
  T-COM-DOCPREP). Load it ALONGSIDE the matching generic prep skill
  (`_skills/graph/4dlab-code-prep` for code/tests, `_skills/graph/4dlab-wiki-prep`
  for the wiki, `_skills/graph/4dlab-doc-prep` for the design docs). It does not
  replace those skills — it pins the COMLab invariants the generic procedure does
  not know: the docs exclusion file-list, the terminal-fusion-spine consumer
  framing (COMLab is CONSUMED-BY the app layer, it CONSUMES the four labs'
  verdicts), the proposal-stays-proposal edge rule, and the vocab→_vocabulary
  split. Do NOT load for code-clean, graphify, or the vault build — those have
  their own skill loadouts.
allowed-tools: [Read, Grep, Glob, Bash]
metadata:
  version: "1.0"
  pack: VAULT (COMLab)
  authored: 2026-06-26
---

# comlab-vault-prep — COMLab invariants for the four ingestion-prep tasks

This skill is the thin COMLab-specific layer over the generic prep skills. The
generic skill owns the *procedure*; this skill owns the *COMLab judgment calls*
the procedure cannot make for you. Read it after the matching generic skill,
before you touch a corpus.

## When to load (and the matching generic skill)

| Task | Generic skill (load first) | Corpus |
|---|---|---|
| `T-COM-CODEPREP` | `_skills/graph/4dlab-code-prep` | `labs/comlab/comlab/` package |
| `T-COM-TESTPREP` | `_skills/graph/4dlab-code-prep` | `labs/comlab/tests/` |
| `T-COM-WIKIPREP` | `_skills/graph/4dlab-wiki-prep` | `labs/comlab/wiki/` (15 chunks) |
| `T-COM-DOCPREP` | `_skills/graph/4dlab-doc-prep` | the 6 design docs (see exclusion list) |

Do **not** load this for `T-COM-CODE-CLEAN-*` (codingskills lane), `T-COM-GRAPH-AST`
(`4dlab-graphify-run`), or `T-COM-VAULT` (`4dlab-vault`).

## Rule 0 — do not cross the streams

Code/test prep, wiki prep, and doc prep are three different operations with three
different generic skills. One task runs exactly one of them. Crossing them (running
`4dlab-doc-prep` on the wiki, or `4dlab-code-prep` on docs) is the single most common
mistake the pipeline guide names. None of the prep skills ever writes `graph.json`
or runs graphify — that is `T-COM-GRAPH-AST` only.

## Rule 1 — COMLab is the TERMINAL fusion spine: frame consumers downstream

COMLab is built LAST. It **consumes** the four upstream labs' *verdicts*
(`schemas/ingestion.py::OrchestratorInboundRequest`), and it **is consumed by** the
application layer. So when you append a `CONSUMES`/`VERIFIES` relation line (wiki/doc
prep) or confirm a public symbol's reader (code prep), the *downstream* consumer of a
COMLab note is one of:

- **COMLab-internal** — `comlab/analytics/*` (scoring) or `comlab/core/fault_atlas_router.py`
  (family routing) or `comlab/core/lab_pipeline_aggregator.py` (the `.process()` spine).
- **The Wired app** — `apps/4DLabWired/` imports `from comlab import LabPipelineAggregator`
  → `.process(OrchestratorInboundRequest)` → `OrchestratorFinalUIOutput`
  (`apps/4DLabWired/wired/composition.py`, `harness/diagnostic_classify.py`; tests import
  `comlab.core.fault_atlas_router.FaultAtlasRouter` and `...lab_pipeline_aggregator.LabPipelineAggregator`).
- **The UI app** — `apps/ui/` rendering `OrchestratorFinalUIOutput`.

It is **not** another diagnostic lab. A COMLab note never names GASLab/OBDLab/DTCLab as
its *consumer* — those are its *inputs*. **Grep-confirm the reader before you frame it**
(`grep -rn "from comlab" apps/`), and remember the Wired app is still evolving: if the
named reader does not resolve today, flag it as a prep gap — do not invent it.

## Rule 2 — proposals stay proposals at the edge

COMLab carries a live proposals slate. These tokens must stay labelled `PROPOSAL` and
must **never** be promoted to a live `CONSUMES`/`VERIFIES` edge:

- `wiki/13_proposals_register.md` — the wiki proposal register.
- `comlab/config/proposals/` — the same-change proposal registry (`COMLab-DELTA`,
  `COMLab-DELTA-V2`, `EP-OBD-17`, `EP-DTC-NOSTART-1`, `EP-OBD-IN-*`, `EP-FA-05`, `COMLab-B`).

A capability shipped behind a **default-off flag** (`enable_delta`, `enable_delta_v2`,
`enable_fatal_gates`) whose live value is still Gate-gated is *also* a proposal-grade edge:
note it as flag-gated, not as an always-live consumer. Signal/noise governs the edge.

## Rule 3 — DOCPREP exclusion file-list (never a `docs/*.md` glob)

`labs/comlab/docs/` holds non-design-doc files. Ingest exactly these **six design docs**
by explicit path:

```
labs/comlab/docs/COMLab_HLD.md
labs/comlab/docs/COMLab_DLD.md
labs/comlab/docs/COMLab_LLD.md
labs/comlab/docs/COMLab_BDD.md
labs/comlab/docs/COMLab_PRD.md
labs/comlab/docs/adr/        ← the 11 ADR records ADR-0001 … ADR-0011 (the "ADR" of HLD/DLD/LLD/ADR/BDD/PRD)
```

**Exclude** (do NOT ingest into the docs tier):

- `docs/Vocabulary/DTC_VOCABULARY.md`, `OBD_VOCABULARY.md`, `SEMANTIC_CONTRACT.md` —
  the vocabulary surface → the shared `Vault/_vocabulary/` tier (built in `T-COM-VAULT`
  step 0), exactly like OBDLab's `OBD_VOCABULARY.md`. `DTC_VOCABULARY`/`OBD_VOCABULARY`
  already have `_vocabulary/` homes from the DTC/OBD packs — COMLab's copies are mirrors.
- `docs/CROSS_LAB_DEPENDENCIES.md` — the cross-lab forward-dependency registry, not a
  COMLab design doc; it has no single-lab vault home.
- `docs/ARCHIVE/` — the superseded v1.0 docs (`COMLab_{HLD,DLD,LLD,PRD}_v1.0_2026-05-21.md`).
- `docs/adr/README.md` — the ADR index, not a record (the 11 records are the docs).

## Rule 4 — wiki is lab-only, graph-canonical at source

`labs/comlab/wiki/` is the 15-chunk lab wiki (`00_index.md … 14_sources_appendices.md`).
`4dlab-wiki-prep` is **append-only** (relation/label trailer blocks) — never move or
rename a chunk. Vocabulary/contract docs live under `docs/Vocabulary/`, design docs under
`docs/`; do not relocate anything between these folders during prep.

## Rule 5 — code/test prep is an AUDIT, not a rewrite

`4dlab-code-prep` probes what your local graphify build extracts, then **reports**
violations as `file:line → rule → fix`. It does not auto-edit source. The coder applies
the reported fixes under the COMLab inner loop (`ruff` → `pyright comlab/` →
`"$PY" -m pytest -x -q`, Python 3.14 via the shared venv `/agent_workspace/.venv-wired`). Scope the
package run to `comlab/` (exclude `tests/`, `registry/`, `research/`); the test corpus is
its own run (`T-COM-TESTPREP`). The registry sub-package is **out of this pack's scope**.

## Anti-orphan close (every prep task)

Every `CONSUMES`/`VERIFIES` line you append (or public reader you confirm) must name a
**real, existing** code path or test — grep-confirm it. An orphan is **flagged and routed
back as a prep gap**, never patched into the graph and never shipped with a fabricated
consumer. This is the Stage-4 signal/noise gate applied at the graph edge.
