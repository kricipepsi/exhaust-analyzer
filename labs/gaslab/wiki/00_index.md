---
chunk_id: GASWIKI-00-INDEX
title: "GAS Lab Wiki v2 — Index & Knowledge-Graph Ingestion Manifest"
doc: GAS_WIKI
version: v2.0
date: 2026-06-03
status: authoritative
scope: "petrol 1990–2010 (Euro 1–5), manually-entered 5-gas analyser, warm-engine samples only"
entities_defined: []
related_chunks: [GASWIKI-01, GASWIKI-02, GASWIKI-03, GASWIKI-04, GASWIKI-05, GASWIKI-06A, GASWIKI-06B, GASWIKI-07, GASWIKI-08, GASWIKI-09, GASWIKI-10, GASWIKI-11]
companion: GAS_VOCABULARY.md (v2.0)
sources: [GAS_WIKI.md v1.0, GAS_VOCABULARY.md v1.1, ChunkProp.md, research q1–q10]
---

# GAS Lab Wiki v2 — Index & Ingestion Manifest

This is the **authoritative reasoning grammar** for GASLab: the "physical reality" module that turns five exhaust-gas readings (HC, CO, CO₂, O₂, NOₓ) plus DNA context into a single canonical `chemical_state` for COMLab.

v2 (2026-06-03) supersedes v1.0 (2026-05-19). It folds in field-research answers to the questions that pestered v1 (see `questions.md`) and restructures the document as **self-contained chunk files** designed for both human navigation and knowledge-graph / RAG ingestion. When this wiki contradicts older notes, this wiki wins for GASLab purposes.

> **Scope change (2026-06-03):** the operating envelope was narrowed from 1990–2020 to **petrol 1990–2010 (Euro 1–5)**. Chemistry tied to the post-2010 "modern" vehicle set (Euro 6/7, the 2010–2020 Era-3 fault patterns) is **out of scope** and is not carried into v2. GDI and early-turbo failure modes remain in scope only where the vehicles were sold within 1990–2010.

## How v2 differs from v1

The reasoning grammar and every numeric threshold are preserved. The `ChemicalSignature` contract is now **34-value** (v2.1 timing-taxonomy revision retired `WRONG_VALVE_TIMING` for three `CAM_TIMING_*` states — see GASWIKI-06B and GAS_VOCABULARY §21). v2 adds:

- **Brettschneider reliability model** — λ is a measure of the *sample*, not the *engine*; per-fault reliability and an explicit uncertainty band (research q1, q2).
- **Pre-cat leak vs sample-handling-error** resolution via OBD fuel-trim correlation and the probe-occlusion test (research q3).
- **ECU-vs-tailpipe divergence magnitudes** quantified per fault, feeding the truth-vs-perception detector (research q6).
- **Five oil-burn failure modes** (worn rings, valve-stem seals, stuck-open PCV, head-gasket oil breach, turbo turbine-seal leak) mapped onto existing enum values with RPM-delta sub-modes (research q4).
- **Dual-idle (idle vs 2500 RPM) catalyst test** distinguishing weak/lazy from dead/poisoned converters (research q10).
- **Timing-fault RPM-differential separation matrix** and Speed-Density-vs-MAF rich/lean behaviour (research q7).
- **Fuel-formulation (E5/E10) and altitude** shifts and why the triangle gate must *not* be relaxed (research q9).
- **Proposed v2.x enum additions** appendix — new oil-burn cases recorded for a future contract revision, still mapped onto existing values (distinct from the v2.1 cam-timing change, which does alter the contract surface).

OBD-II depth from research q7 (DTC tables, Mode `$06` MID/TID, freeze-frame, in-cylinder pressure) is summarised as **OBDLab / DTCLab territory** with cross-references, not reproduced in full — GASLab's emit boundary is tailpipe 5-gas only.

## Knowledge-graph ingestion conventions

Every chunk is an independently retrievable unit. To make extraction deterministic:

1. **Front-matter** (YAML) on every file carries: `chunk_id`, `title`, `summary`, `entities_defined`, `related_chunks`, `sources`. KG ingestion should treat `entities_defined` as the node list this chunk is authoritative for.
2. **Stable anchor IDs.** Every fault entity, rule, gate, and test has an explicit anchor of the form `{#FAULT_<NAME>}`, `{#RULE_<NAME>}`, `{#GATE_<NAME>}`, `{#TEST_<NAME>}`, `{#CONCEPT_<NAME>}`. Cross-references use these IDs (e.g. `→ RULE_MASKING`) rather than fragile section numbers. Legacy `§n.n` numbers are retained in parentheses for traceability to v1.
3. **Typed fault-entity records.** Each fault in the atlas (chunks 05, 06A, 06B) uses the same key list so relations extract uniformly: `chemical_state`, `dna_gate`, `match_class`, `gas_vector`, `discriminator`, `rpm_delta`, `related`, `sources`.
4. **One concept per section.** Sections are never split across chunks; cross-chunk links are expected and resolvable by `chunk_id` + anchor.
5. **Provenance.** Content new in v2 is tagged inline `[v2: qN]` so the graph can attribute each claim to its research source.

## Chunk manifest

| chunk_id | file | covers (v1 §) | primary entities |
|---|---|---|---|
| GASWIKI-01 | `01_role_boundaries_dna_ingestion.md` | 1, 2, 3 | CONCEPT_ROLE, CONCEPT_GASLABDNAVIEW, CONCEPT_DNA_GATED_INGESTION, CONCEPT_GASLABPAYLOAD |
| GASWIKI-02 | `02_combustion_foundations.md` | 4 | CONCEPT_LAMBDA, CONCEPT_BRETTSCHNEIDER, CONCEPT_CATALYST_WINDOW, CONCEPT_RPM_BUCKET, CONCEPT_EURO_SCALING, CONCEPT_FUEL_ALTITUDE |
| GASWIKI-03 | `03_five_gases_reference.md` | 5 | GAS_HC, GAS_CO, GAS_CO2, GAS_O2, GAS_NOX, CONCEPT_CROSS_SENSITIVITY |
| GASWIKI-04 | `04_inter_gas_grammar_validity_gates.md` | 6, 8 | GATE_TRIANGLE, GATE_DILUTION, RULE_SEESAW, RULE_MASKING, RULE_COLLISION, RULE_WVT, RULE_LAMBDA_MISMATCH, CONCEPT_DIVERGENCE_MAGNITUDE |
| GASWIKI-05 | `05_fault_atlas_part_a.md` | 7.1–7.16 | FAULT_NORMAL_OPERATION … FAULT_WORN_ENGINE (16 faults) |
| GASWIKI-06A | `06a_fault_atlas_oil_mechanical.md` | 7.17–7.23 | FAULT_FLAT_CAMSHAFT, FAULT_GDI_*, FAULT_VACUUM_REGULATOR_*, FAULT_WORN_VALVE_SEALS, FAULT_WORN_PISTON_RINGS, FAULT_POA_SIGNATURE + oil-burn sub-modes |
| GASWIKI-06B | `06b_fault_atlas_valvetrain_egr_combustion.md` | 7.24–7.32 | FAULT_CAM_TIMING_RETARDED_MAP, FAULT_CAM_TIMING_RETARDED_MAF, FAULT_CAM_TIMING_ADVANCED, FAULT_EGR_*, FAULT_VVT_FAILURE, FAULT_EVAP_*, FAULT_INCOMPLETE_*, FAULT_COOLANT_LEAK_INTERNAL |
| GASWIKI-07 | `07_catalyst_postcat_logic.md` | 9 | CONCEPT_TWC, TEST_DUAL_IDLE_CATALYST, CONCEPT_NOX_CAPACITY, CONCEPT_CO_TO_NOX_TRANSITION, TEST_REJUVENATION |
| GASWIKI-08 | `08_diagnostic_tactics.md` | 11 | TEST_PRECONDITIONS, TEST_LAMBDA_MISMATCH, TEST_WEIRD_GASES_TREE, TEST_RPM_SEPARATION_MATRIX, TEST_PROBE_OCCLUSION |
| GASWIKI-09 | `09_era_specific_patterns.md` | 12 | CONCEPT_ERA1, CONCEPT_ERA2 |
| GASWIKI-10 | `10_limited_scope_confidence.md` | 10 | CONCEPT_CONFIDENCE_LEVEL, CONCEPT_SCOPE_SHRINKAGE, CONCEPT_CONFIDENCE_CEILING |
| GASWIKI-11 | `11_sources_appendices.md` | 13 | CONCEPT_REFERENCE_TABLES, CONCEPT_PROPOSED_ENUM_ADDITIONS, CONCEPT_GLOSSARY |

## Reading order

Foundations (01 → 02 → 03) establish vocabulary and physics. Grammar (04) is the rule layer. The atlas (05, 06A, 06B) is the lookup surface. Catalyst (07), tactics (08), era (09), scope/confidence (10), and sources (11) are reference layers cited by the atlas.

*The chunk files (`00_index.md` … `11_sources_appendices.md`) are the **sole canonical** form of this wiki, for both human linear reading and KG ingestion. The former assembled single-file `GAS_WIKI.md` was retired to ARCHIVE on 2026-06-10 — do not edit or cite it; cite the chunk + section instead (e.g. `GASWIKI-02 §2.3`).*

## Graph relations (explicit)

**GASWIKI-00-INDEX** DESCRIBES **GASWIKI-01** through **GASWIKI-11**
**GASWIKI-00-INDEX** DESCRIBES reading order **01 → 02 → 03 → 04 → 05/06A/06B → 07 → 08 → 09 → 10 → 11**
**GASWIKI-00-INDEX** DESCRIBES **CHANGE_v2.1_timing_taxonomy**
**GAS_WIKI v1.0** SUPERSEDED_BY **GAS_WIKI v2.0 chunk corpus**
**GAS_WIKI.md (single-file)** RETIRED_TO **ARCHIVE**
**GAS_VOCABULARY.md** COMPANION_TO **GAS_WIKI v2.0**
**chunk_id** frontmatter CONSUMED_BY **graphify Pass-3 LLM extraction**
**entities_defined** frontmatter CONSUMED_BY **graphify Pass-3 LLM extraction**
**related_chunks** frontmatter CONSUMED_BY **graphify Pass-3 LLM extraction**
**anchor IDs** (`{#FAULT_*}`, `{#RULE_*}`, `{#GATE_*}`, `{#TEST_*}`, `{#CONCEPT_*}`) CONSUMED_BY **graphify Pass-3 LLM extraction**

## Core Entities

- **GASWIKI-00-INDEX** — authoritative index & ingestion manifest for the GASLab v2 wiki corpus (12 chunks + CHANGE). Consumer: `T-GAS-GRAPH-LLM` (graphify Pass-3).
- **GAS_VOCABULARY.md** — companion vocabulary file (v2.0), moved to `labs/gaslab/docs/GAS_VOCABULARY.md`. Consumer: `test_validators.py`, `gaslab/resolution.py`, wiki chunks.
- **GAS_WIKI.md (ARCHIVE)** — retired single-file v1.0 wiki. Do not cite; cite chunk + section.
- **CHANGE_v2.1_timing_taxonomy** — v2.1 changelog for the `CAM_TIMING_*` contract change. Consumer: `contracts.py` `ChemicalSignature` enum.
