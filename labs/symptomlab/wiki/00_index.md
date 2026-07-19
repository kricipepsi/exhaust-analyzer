---
chunk_id: SYMWIKI-00
title: "SymptomLab Wiki — Index"
lab: symptomlab
node_type: wiki
module: symptomlab
subsystem: wiki-index
implements: []
consumers:
  - "vault: Vault/_bases/modules.base (routing index over SYMWIKI-01..04 framed notes)"
drift_guards: []
tags: [symptomlab, wiki, wiki-index]
source: "labs/symptomlab/wiki/00_index.md"
doc: SYMPTOM_WIKI
version: v2.0
role: routing-index
status: authoritative
date: 2026-06-12
companion_docset: "docs/ (PRD, HLD, DLD, LLD, ADR, BDD, SYMPTOM_VOCABULARY)"
kg_ingestion: extract
related_chunks: [SYMWIKI-01, SYMWIKI-02, SYMWIKI-03, SYMWIKI-04]
---

# SymptomLab Wiki — Index

**Disposition: canonical, extraction-bearing.** This wiki is the citation-backed
corpus describing what SymptomLab owns: the driver-reported "Part B" symptom
vocabulary. The chunked notes below carry `kg_ingestion: extract` front-matter and
feed the `v2_wiki` graph tier. They mirror live code (`allowed_combinations.yaml`,
`models.py`, `validator.py`) and are the prose authority for the catalog and axes.

## Routing — the chunked notes

| Chunk | Note | Owns |
|---|---|---|
| SYMWIKI-01 | `01_symptom_catalog.md` | The two-tier symptom catalog — 7 Tier-1 × 3 Tier-2 = **21 allowed pairs** — and the candidate fault family each pair points at. Prose mirror of `allowed_combinations.yaml`. |
| SYMWIKI-02 | `02_environmental_axes.md` | The three context axes (`occurs_during`, `engine_state`, `load_state`) and the physical derivation of `load_state`. Prose mirror of the `models.py` `StrEnum`s. |
| SYMWIKI-03 | `03_symptom_dna_payload.md` | The four-field, routing-free `SymptomDNA` Part-B payload contract. |
| SYMWIKI-04 | `04_catalog_changelog.md` | The legacy→revised catalog changelog (KEEP/REWORD/DROP/ADD) — provenance for the catalog's shape. |

## Canonical surface (what SymptomLab actually owns)

- **21-pair symptom catalog** — `data/allowed_combinations.yaml`, 7 `tier_1` × 3
  `tier_2`. The `len == 21` invariant is enforced at validator construction
  (`validator.py:SymptomValidator`). `oil_consumption` is the seventh Tier-1
  category (live; oil-consumption build in progress).
- **Three environmental axes** (typed `StrEnum`): `OccursDuring`, `EngineState`
  (`will_not_start`), `LoadState`.
- **`SymptomDNA`** — the four-field Part B payload; routing-free by design.

Full field/enum tables also live in `docs/SYMPTOM_VOCABULARY.md`; behaviour in
`docs/HLD_SymptomLab.md` / `docs/BDD_SymptomLab.md`.

## Where the numbers live (deliberately not here)

The weighting bands, exhaust-chemistry footprints, context-modifier
promotions/demotions, and the report-trust cap are **COMLab-owned** and live in the
proposals registry `labs/comlab/comlab/config/proposals/entries.yaml`, never in
these live notes:

- **COMLab-A** — `(tier_1, tier_2)` → fault-family routing.
- **COMLab-B** — `load_state` context modifiers + the report-trust cap.
- **COMLab-F** — per-Tier-1 weighting bands and measured category frequencies.
- **COMLab-G** — per-fault-family exhaust-chemistry footprints.

This is the signal/noise boundary: SymptomLab supplies the vocabulary those numbers
key off; a number with no SymptomLab consumer (the validator reads only pairs and
axis enums) would be noise. A `grep` for any weighting band, chemistry %, or
trust-cap figure inside `labs/symptomlab/wiki/` must return zero hits.

## History

This index was previously marked `kg_ingestion: none` / "reference-only" on the
premise that SymptomLab "carries no empirical numeric literals." That premise was
incorrect: `labs/dnalab/research/DNAresearch.md` and
`labs/symptomlab/AnswerSymLab.md` carry sourced weighting bands, chemistry
footprints, and the report-trust figure — measured, citation-backed prose. Those
numbers are now correctly routed to the COMLab proposals registry (above), and the
vocabulary they key off is authored as the live corpus (SYMWIKI-01..04).
