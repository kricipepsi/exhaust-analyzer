---
chunk_id: COMWIKI-00-INDEX
title: "COMLab Wiki v2 — Index & Ingestion Manifest"
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
scope: "petrol 1990–2010 (Euro 1–5), manually-entered 5-gas + OBD-II PIDs + DTCs + VIN/symptom DNA; the prune→rank→fuse decision spine"
entities_defined: []
related_chunks: [COMWIKI-01, COMWIKI-02, COMWIKI-03, COMWIKI-04, COMWIKI-05, COMWIKI-06, COMWIKI-07, COMWIKI-08, COMWIKI-09, COMWIKI-10, COMWIKI-11, COMWIKI-12, COMWIKI-13, COMWIKI-14]
companion: "global_fault_registry.json + comlab/config/kg/*.json (frozen) + OBD_VOCABULARY.md"
sources: [COMLab v1 wiki (ARCHIVE 2026-06-20), REWORK_PLAN_COMLab.md, AUDIT_ANSWERS_COMLab.md, AUDIT_PART1_CEILING_RESEARCH.md, OPEN_LEVERS_COMLab.md, "research packs A/B/C/D/E", tasks/PROGRESS.md]
---

# COMLab Wiki v2 — Index & Ingestion Manifest

This is the **authoritative reasoning grammar** for COMLab: the **prune→rank→fuse decision
spine** of 4DLab. Where GASLab, OBDLab, DTCLab, and DNALab each emit one validated
channel, COMLab is the only module that **consumes all of them and produces a verdict**. This
wiki defines how those channels are pruned, scored, fused, calibrated, and presented — and
what the 2026-06 research rework changes about that.

> **COMLab is built LAST** (`ROADMAP.md` Stage 4). The emitter labs and the research gates are
> settled first so the spine is not tuned against a moving target. This wiki is therefore
> authored at the *start* of the Stage-4 rework and encodes its target architecture, not a
> shipped state — implementation rows live in `tasks/PROGRESS.md`.

## How v2 differs from v1

v2 (2026-06-20) supersedes the v1 wiki (the 80 loose `COMLab_*.md` / `ERR-*.md` / `*_Family.md`
files retired to `ARCHIVE/2026-06-20_comlab_wiki_v1/`). The reasoning grammar and every numeric
threshold from v1 are carried forward; v2 restructures the document into **self-contained,
KG-ingestible chunks** (matching the GASLab and DTCLab v2 wikis) and folds in the research
rework. When this wiki contradicts the archived v1 notes, **this wiki wins**.

The three reframes the research forced (full detail in `COMWIKI-08`/`12`):

- **R1 — Data is the binding constraint, not the logic.** The ~50 % plateau is a corpus
  problem (small, imbalanced, partly synthetic, ambiguous sentinels), not a ranker problem.
  The measured achievable ceiling is **70–80 %, not 85 %** on the current four single-point
  channels (provable ~9.6 % floor from 27 `ecu_fault` STOP cases). [v2: AUDIT Q2, pack C]
- **R2 — The additive prune-then-rank paradigm has hit its ceiling.** Bounded-additive nudges
  moved **0 pp** repeatedly; the intended DTC tie-breaker is starved (64/90 OUTRANKED cases
  carry no DTC). The fix is **calibrated, conflict-aware late fusion**, not more weight-tuning.
  [v2: AUDIT Part 1 §1.1, pack A]
- **R3 — The missing discriminator is a two-point delta.** The hardest collisions separate on
  the *sign of change across an RPM step* — a discriminator that needs **no DTC**. The contract
  already supports two operating points; the gap is a *populated* second frame. [v2: packs D/E]

## Knowledge-graph ingestion conventions

Every chunk is an independently retrievable unit. To make extraction deterministic:

1. **Front-matter (YAML)** on every file carries `chunk_id`, `title`, `version`,
   `entities_defined`, `related_chunks`, `sources`. KG ingestion treats `entities_defined` as
   the node list the chunk is authoritative for.
2. **Stable anchor IDs.** Every concept, gate, rule, stage, fault, and test has an explicit
   anchor of the form `{#CONCEPT_<NAME>}`, `{#GATE_<NAME>}`, `{#RULE_<NAME>}`,
   `{#STAGE_<NAME>}`, `{#FAULT_<NAME>}`, `{#FUSE_<NAME>}`, `{#TEST_<NAME>}`. Cross-references use
   these IDs (e.g. `→ FUSE_CONFLICT_AWARE`) rather than fragile section numbers.
3. **Provenance.** Content new in v2 (from the research rework) is tagged inline `[v2: <src>]`.
4. **Signal/noise tags.** A token COMLab does not yet read in a live path is tagged
   **[PROPOSAL]** inline and consolidated in `COMWIKI-13`. See §"Signal/noise discipline" below.
5. **Numeric literals carry a citation** (`# wiki: §…` or a named source), per house rule.

## Chunk manifest

| chunk_id | file | covers | primary entities |
|---|---|---|---|
| COMWIKI-00 | `00_index.md` | this manifest, conventions, sources, graph relations | — |
| COMWIKI-01 | `01_role_boundaries_fusion_spine.md` | COMLab's role; boundary & isolation invariants; the four input channels | CONCEPT_FUSION_SPINE, CONCEPT_ISOLATION, CONCEPT_CHANNELS |
| COMWIKI-02 | `02_lab_input_contract.md` | every field consumed from GAS/OBD/DTC/DNA + symptom; provenance flags | CONCEPT_GAS_INPUT, CONCEPT_OBD_INPUT, CONCEPT_DTC_INPUT, CONCEPT_DNA_INPUT, CONCEPT_PROVENANCE |
| COMWIKI-03 | `03_vehicle_dna_pruning.md` | VehicleDNA → 3 LabDnaViews; hardware-flag gating; polymorphic VE/O₂ math | CONCEPT_LABDNAVIEW, RULE_HW_PRUNE, CONCEPT_VE_POLYMORPH, CONCEPT_O2_POLYMORPH |
| COMWIKI-04 | `04_horizon_eras.md` | LEGACY/ADAPTIVE/MODERN profiles, masks, era assignment | CONCEPT_LEGACY, CONCEPT_ADAPTIVE, CONCEPT_MODERN, RULE_HORIZON_PRUNE |
| COMWIKI-05 | `05_fault_taxonomy.md` | 30 nodes / 12 families; gas-state routing; trim grammar | the 30 FAULT_* nodes + family concepts |
| COMWIKI-06 | `06_fault_atlas_families.md` | per-family diagnostic context, discriminators, the colliding-pair set | family CONCEPT_* + collision rules |
| COMWIKI-07 | `07_pipeline_stages.md` | Stage A→B→C→D pipeline; fatal gates; prune/score order; catalyst override | STAGE_A..D, GATE_*, RULE_SCORING, RULE_CAT_OVERRIDE |
| COMWIKI-08 | `08_scoring_to_fusion_rework.md` | R2: additive ceiling → conflict-aware late fusion; the 13 evidence consumers | FUSE_CONFLICT_AWARE, FUSE_INV_VARIANCE, FUSE_CONTRADICTION, the T-COMV2-* consumers |
| COMWIKI-09 | `09_calibration_confidence.md` | B.Q1: post-hoc calibration; posterior/LR tiers; ECE/Brier/reliability | CONCEPT_CALIBRATION, CONCEPT_CONF_TIER, CONCEPT_CONFORMAL |
| COMWIKI-10 | `10_differential_and_symptom_prior.md` | B.Q2 top-k differential as primary output; B.Q3 symptom prior cap | CONCEPT_DIFFERENTIAL, RULE_TOPK, RULE_SYMPTOM_PRIOR |
| COMWIKI-11 | `11_two_point_delta.md` | D+E: operating points, Δ signatures, abstain set, gates, gas↔OBD cross-reference | TEST_TWO_POINT, RULE_DELTA_GATE, RULE_CROSSREF, CONCEPT_NOISE_FLOOR |
| COMWIKI-12 | `12_corpus_eval_discipline.md` | C: data as constraint; provenance; label noise; ceiling; Phase-0 gates | CONCEPT_CEILING, GATE_DATA, GATE_CAPTURE, RULE_ABSTAIN_LOWSUPPORT |
| COMWIKI-13 | `13_proposals_register.md` | consolidated signal/noise register: fusion consumers + EP-* proposals | the proposal entities |
| COMWIKI-14 | `14_sources_appendices.md` | research packs, standards, target-architecture diagram, human gates, glossary | CONCEPT_TARGET_ARCH, CONCEPT_GLOSSARY |

## Reading order

Foundations (01 → 02 → 03 → 04) establish role, the input contract, and pruning. The lookup
surface (05 → 06) is the taxonomy and atlas. The operational spine (07) is today's pipeline.
The rework (08 → 09 → 10 → 11 → 12) is what Stage 4 changes: fusion, calibration, differential,
delta, and the data discipline that bounds all of it. The register (13) and sources (14) are
reference layers cited throughout.

## Signal/noise discipline in this wiki

Every field, enum value, or flag this wiki introduces as **new** must name an **existing or
co-shipped consumer** — the COMLab analytics or fault-atlas code path that reads it — and the
code path. v2-new tokens are tagged **[PROPOSAL]** inline and consolidated in
`COMWIKI-13`. A **[PROPOSAL]** token is *not yet* in the live `global_fault_registry.json` /
config; it ships only when its task spec is authored and the consumer code path lands, and it
must be registered in `comlab/config/proposals/` — never silently in the live KG/registry.
"Future use" is not a consumer; but "not in v1" is **not** a reason to defer — default new
improvements to a proposal that ships its consumer in the same change (`AGENTS.md` rule 4).

## Frozen-graph note

The KG JSON under `comlab/config/kg/*.json` is **frozen**. This wiki is queried as domain
truth; it does **not** trigger a graph rebuild. Do not run `graphify` to "refresh" the KG from
these chunks — the KG pre-step is **SKIP** unless a task is an explicit `T-KG-*` lane
(root `CLAUDE.md` hard prohibition). The v1 per-fault source docs were archived, not deleted;
their machine-readable content survives in the frozen JSON and is summarised in `COMWIKI-05/06`.

## Sources

**Internal (this lab):**

- `labs/comlab/research/REWORK_PLAN_COMLab.md` — the architect's research synthesis driving v2.
- `labs/comlab/research/{AUDIT_ANSWERS_COMLab,AUDIT_PART1_CEILING_RESEARCH,OPEN_LEVERS_COMLab}.md`
- `labs/comlab/research/PROPOSAL_DeltaLab_cross_lab_delta_module.md`
- Research packs A–E: `Automotive Diagnostic Fusion Research.md`, `DeltaRes1.md`, `DeltaRes2.md`,
  `Two-Point Emissions Test Fixture Design.md`, `Multi-Sensor Fusion for Automotive Diagnostics.md`,
  `deep-research-report.md`, `deep-research-reportC.md`.
- `labs/comlab/docs/{COMLab_PRD,COMLab_HLD,COMLab_DLD,COMLab_LLD}.md` — design docs.
- `labs/comlab/tasks/PROGRESS.md` — the Stage-4 fusion-consumer ledger.
- `ARCHIVE/2026-06-20_comlab_wiki_v1/` — the retired v1 wiki (provenance only).

**Cross-lab (companion contracts):**

- `labs/gaslab/wiki/` (GASWIKI-00…11) — gas chemistry / `chemical_state`.
- `labs/obdlab/wiki/OBDLab_KG_Wiki.md` + `OBD_VOCABULARY.md` — live-PID channel.
- `labs/dtclab/wiki/` (DTCWIKI-00…12) — DTC / freeze-frame / Mode `$06` channel.
- `labs/dnalab/` — VehicleDNA + symptom prior.

**Standards (cited inline where literals appear):** SAE J1979/J2012, ISO 15031-5/-6,
EPA/BAR two-speed-idle test, ECE R51 / ISO 5130 (stress idle), SAE J1635 (cold-start symptoms).

## Graph relations (explicit)

**COMWIKI-00-INDEX** DESCRIBES **COMWIKI-01** through **COMWIKI-14**
**COMWIKI-00-INDEX** DESCRIBES reading order **01 → 02 → 03 → 04 → 05/06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14**
**COMLab v1 wiki (80 loose files)** SUPERSEDED_BY **COM_WIKI v2.0 chunk corpus**
**COMLab v1 wiki** RETIRED_TO **ARCHIVE/2026-06-20_comlab_wiki_v1**
**global_fault_registry.json** COMPANION_TO **COM_WIKI v2.0**
**comlab/config/kg/*.json** FROZEN_SOURCE_FOR **COM_WIKI v2.0 §05/§06**
**GASLabPayload / OBDLiveDataPayload / DTCLabPayload / VehicleDNA** CONSUMED_BY **COMLab.schemas.ingestion**

## Core Entities

- **COMWIKI-00-INDEX** — authoritative index & ingestion manifest for the COMLab v2 wiki corpus (15 chunks). Consumer: KG ingestion / human navigation.
- **global_fault_registry.json** — flat cross-domain fault registry (the rule surface). Consumer: `comlab/core/fault_atlas_router.py`.
- **comlab/config/kg/*.json** — frozen per-node KG enrichment (Stage C). Consumer: `comlab/core/fault_atlas_kg.py`.
- **COMLab v1 wiki (ARCHIVE)** — retired loose-file wiki. Do not cite; cite chunk + anchor.
