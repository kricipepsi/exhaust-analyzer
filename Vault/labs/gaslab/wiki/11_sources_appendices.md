---
chunk_id: GASWIKI-11
title: "Sources & Appendices"
doc: GAS_WIKI
version: v2.0
summary: "Source-file provenance (incl. the v2 research dossiers q1–q10), reference appendix tables (idle reference, pre/post-cat, UK MOT limits), the proposed v2.x enum-additions appendix for the new oil-burn cases, and the glossary."
covers_v1_sections: [13]
entities_defined: [CONCEPT_REFERENCE_TABLES, CONCEPT_PROPOSED_ENUM_ADDITIONS, CONCEPT_GLOSSARY, CONCEPT_SOURCES]
related_chunks: [GASWIKI-06A, GASWIKI-06B, GASWIKI-10]
sources: ["GAS_WIKI.md v1.0 §13", "research q1–q10"]
---

# 11. Sources & Appendices

> **Chunk summary.** Provenance, reference tables, the proposed-enum-additions appendix, and the glossary. Every claim in the atlas traces to a source listed here.

## 11.1 Sources {#CONCEPT_SOURCES}

### Spine (v1 sources, carried forward)

| Source file | Used for |
|---|---|
| `gas_lab_wiki.md` (v1.2) | Combustion foundations, five gases, grammar, fault atlas, catalyst, tactics |
| `master_gas_guide.md` | Per-gas behaviour bands, four-canonical-rows summary, AFR chart |
| `gas_lab_dataset.yaml` (v2.3) | Numeric thresholds, enum values, edge-rule priorities |
| `gasrules1.md` (Crypton) | AFR/λ relationship, EGR idle-vs-load, lean/rich tables, O₂ post-cat reliability |
| `gasinteraction.md` | NO/HC/CO/CO₂/O₂ interaction matrices |
| `diagnoseecu.md` | Truth-vs-perception framework, λ tie-breakers, ghost misfire vs ECU blindness |
| `CommonFaults.md` | Era-specific fault patterns (Era 1, Era 2) |
| `knowledge_base.py` | High-idle ranges, UK MOT limits |
| MOTOR Magazine 1998 files | CO-to-NOₓ transition, cat NOₓ capacity, rejuvenation, cold-converter test, mass-vs-concentration |
| `plini3.txt` (Toyota) | Dilution screen, misfire-induced NOₓ via cat O₂, O₂ as best post-cat indicator |
| `understanding5gas_*.txt` | NOₓ causes, EGR idle mechanism, timing effects, O₂ sensor bias, worn engine + flat cam |

### v2 research dossiers (new)

| Source | Integrated into | Topic |
|---|---|---|
| `q1&7/Advanced Engineering Analysis of Petrol Engine Timings (1990–2010).md` | GASWIKI-02 §2.4, GASWIKI-05 (timing), GASWIKI-06B (WVT), GASWIKI-08 §8.9 | Brettschneider reliability per fault (q1); timing thermodynamic signatures + RPM-differential family separation (q7) |
| `q2/bretsscheider.md` | GASWIKI-02 §2.4 | Brettschneider robustness, "sample not engine", uncertainty band |
| `q3/PreCatAirLeak.md` | GASWIKI-04 §4.4, GASWIKI-08 §8.10 | Pre-cat leak vs sampling-error; OBD STFT correlation; probe-occlusion test |
| `q4/OilburnCases.md` | GASWIKI-06A (oil-burn sub-modes), GASWIKI-06B (head-gasket), GASWIKI-08 §8.9 | Five oil-ingestion failure modes + RPM-delta deltas |
| `q6/Diverg.md` | GASWIKI-04 §4.12 | ECU-vs-tailpipe divergence magnitudes per fault |
| `q9/ethanolblend.md` | GASWIKI-02 §2.9, GASWIKI-04 §4.1 | E5/E10 + altitude shifts; do-not-relax-the-gate rule |
| `q10/catalystFault.md` | GASWIKI-07 §7.6 | Dual-idle catalyst efficiency test |
| `EP-GAS-03 / formula-wiki F-GAS-04, F-GAS-05` | GASWIKI-02 §2.10 | Combustion-integrity derived metrics: chemical efficiency and O₂-vs-CO oxygen usage |
| `EP-CAT-02 / EP-CAT-05; Vol1 N-008; Denton §5` | GASWIKI-07 §7.8 | Healthy-catalyst masking limit, pre-cat O₂/LTFT and ΔT hand-off, cat-masked oil-burn precedent, and thermal-urgency figure |

## 11.2 Reference appendix tables {#CONCEPT_REFERENCE_TABLES}

### 11.2.1 Idle reference (warm, working cat)

| Gas | Ideal | Marginal | Fault |
|---|---|---|---|
| HC | 0 – 35 ppm | 35 – 100 ppm | > 100 ppm |
| CO | 0.1 – 0.45 % | 0.45 – 1.0 % | > 1.0 % |
| CO₂ | 14.5 – 16 % | 13.5 – 14.5 % | < 13.5 % |
| O₂ | 0 – 0.35 % | 0.35 – 1.0 % | > 1.0 % |
| NOₓ | < 100 ppm | 100 – 500 ppm | > 500 ppm |
| λ | 0.995 – 1.005 | 0.97 – 1.03 | < 0.97 or > 1.03 |

### 11.2.2 Pre- and post-cat reference

| Condition | CO | CO₂ | HC | O₂ | λ | AFR |
|---|---|---|---|---|---|---|
| Before cat (efficient) | 0.6 % | 14.7 % | 100 ppm | 0.7 % | 1.0 | 14.7 |
| After cat (efficient) | 0.1 % | 15.2 % | 15 ppm | 0.1 % | 1.0 | 14.7 |

### 11.2.3 UK MOT test limits (concentration-based)

| Parameter | Test condition | Limit |
|---|---|---|
| CO | At idle | ≤ 0.30 % |
| CO | At raised idle (~2500 RPM) | ≤ 0.20 % |
| HC | At raised idle (~2500 RPM) | ≤ 200 ppm |
| Lambda | At raised idle | 0.97 – 1.03 |

## 11.3 Proposed v2.x enum additions (not yet in the contract) {#CONCEPT_PROPOSED_ENUM_ADDITIONS}

Per the v2 decision, the new oil-burn field cases (q4) are **mapped onto existing enum values now** so they require no contract change and COMLab needs no schema change. The candidate values below are recorded for a **future coordinated contract revision** (`SEMANTIC_CONTRACT.md` + `OBD_VOCABULARY.md §17` + COMLab schema). They are **not** emittable today.

> **Distinct from the v2.1 cam-timing change.** The v2.1 timing-taxonomy revision (retired `WRONG_VALVE_TIMING`; added `CAM_TIMING_RETARDED_MAP` / `CAM_TIMING_RETARDED_MAF` / `CAM_TIMING_ADVANCED`, surface 32 → 34) *does* alter the GASLab contract surface and **is** live in this wiki. Its coordinated mirror into `OBD_VOCABULARY.md §17`, `SEMANTIC_CONTRACT.md`, the COMLab schema, and `resolution.py` rule bindings is the open cross-lab follow-up (→ GAS_VOCABULARY §21).

| Candidate value | Current v2 mapping | Distinct signature that would justify its own value | DNA gate if added |
|---|---|---|---|
| `PCV_STUCK_OPEN` | `POA_SIGNATURE` (clogged-PCV sub-mode) | Heavy rich at closed-throttle idle (CO ~1.9 %, λ ~0.925, HC ~610) that clears as manifold vacuum falls at 2500 RPM (CO ~0.45 %, HC ~170). Distinct from generic POA by the strong idle-only rich offset. | none |
| `TURBO_SEAL_OIL_LEAK` | `POA_SIGNATURE` (turbo-seal sub-mode) | Extreme tailpipe HC (~720 ppm) with **perfectly stoichiometric λ (1.000) and near-zero CO** — oil cracks in the hot exhaust, not the cylinder, so combustion is intact. | `induction_type = forced` |
| `HEAD_GASKET_OIL_BREACH` | `COOLANT_LEAK_INTERNAL` (oil-to-cylinder breach) | False-lean O₂ (> 2 %) with suppressed NOₓ (< 30 ppm) plus elevated CO and HC and a milky oil/coolant emulsion — an oil-passage breach (often alongside coolant). Distinct from pure coolant leak by oil-emulsion evidence. | none |

**Change protocol reminder:** adding these is a backwards-compatible enum extension (minor version bump) *only if* COMLab mirrors the new values in `comlab/schemas/vocabulary.py` in the same coordinated change. Until then, emit the mapped existing value and annotate the sub-mode in the warnings stream.

## 11.4 Glossary {#CONCEPT_GLOSSARY}

- **AFR** — Air-fuel ratio, mass-based; stoichiometric petrol = 14.71 : 1.
- **Brettschneider equation** — Chemistry-only lambda from HC/CO/CO₂/O₂/NOₓ and fuel H/C ratio; a *sample* mass-balance, not a direct engine measurement (→ CONCEPT_BRETTSCHNEIDER_RELIABILITY).
- **CE** — Combustion Efficiency; explicit carbon-oxidation ratio `CO₂/(CO₂+CO)`, with low values marking a combustion-quality deficit (→ CONCEPT_COMBUSTION_INTEGRITY).
- **Collision** — Physically impossible two-high pattern (CO + O₂, or NOₓ + CO) that names a specific failure mode.
- **Dual-idle test** — Idle vs 2500 RPM 5-gas comparison; separates weak from dead catalyst and routes RPM-differential faults (→ TEST_DUAL_IDLE_CATALYST, → TEST_RPM_SEPARATION_MATRIX).
- **Exhaust Gas Triangle** — CO + CO₂ + O₂ ≈ 14–16 % in valid samples.
- **GasLabDnaView** — Slim DNA projection consumed by GASLab.
- **Healthy-catalyst masking / "filter of truth"** — A lit, high-OSC catalyst can scrub a rich or HC-heavy feed so the downstream 5-gas sample looks clean; tailpipe gas cannot exonerate the engine alone (→ CONCEPT_HEALTHY_CAT_MASKING).
- **Light-off** — Catalyst surface reaching self-sustaining reaction temperature (~400 °C).
- **Masking rule** — Override naming ignition misfire when HC + O₂ are high but NOₓ is low.
- **Modified Brettschneider** — HC carbon-mass-corrected form (factor 12 vs 6); noted for future calibration.
- **NDIR** — Non-dispersive infrared sensing; used for HC, CO, CO₂.
- **OSC** — Oxygen Storage Capacity; ceria-zirconia property buffering ECU oscillations.
- **Oxygen-usage** — Qualitative O₂-vs-CO discriminator: high O₂ with high HC/CO routes to misfire, while high CO with near-zero O₂ routes to pure rich over-fuelling (→ CONCEPT_COMBUSTION_INTEGRITY).
- **POA signature** — Poisoning + Oil-ash + Abundant HC — the secondary effects of oil burning GASLab can detect.
- **Probe-occlusion test** — Blocking the probe tip to expose a sampling-apparatus leak (→ TEST_PROBE_OCCLUSION).
- **Quench** — Flame extinguished by a cool surface, leaving unburned HC.
- **Speed-Density vs MAF** — The two load-calc systems; they invert the rich/lean fingerprint of a retarded cam (→ FAULT_CAM_TIMING_RETARDED_MAP rich vs → FAULT_CAM_TIMING_RETARDED_MAF lean).
- **STRESS_IDLE** — Clinical diagnostic RPM bucket, 3500–4500, VIN-dependent.
- **Truth-vs-perception** — Chemistry λ (ground truth) vs ECU λ (perception); divergence magnitudes at → CONCEPT_DIVERGENCE_MAGNITUDE.
- **TWC** — Three-Way Catalyst.

---

*End of GAS Lab Wiki v2 chunk set. This document is the citation target for every rule in the GASLab rule engine and for every reasoning sentence rendered to the technician. Scope: petrol 1990–2010 (Euro 1–5), 5-gas warm-idle.*

## Graph relations (explicit)

**CONCEPT_SOURCES** ENUMERATES **GAS_WIKI.md v1.0**, **research q1–q10**, **cases_petrol**, **casesextra**, **Denton AdvAutomotiveFaultDiagnosis**, **Wikipedia — Brettschneider formula / Catalyst poisoning / Stoichiometry**
**CONCEPT_REFERENCE_TABLES** CONSUMED_BY **gaslab.rule_engine** — per-fault numeric thresholds are normative
**CONCEPT_REFERENCE_TABLES** DESCRIBES **warm-idle reference gas values**, **UK MOT fast-pass standards**, **Brettschneider worked examples**
**CONCEPT_PROPOSED_ENUM_ADDITIONS** ENUMERATES **PCV_STUCK_OPEN**, **TURBO_SEAL_OIL_LEAK**, **HEAD_GASKET_OIL_BREACH** — candidate v2.x values, not emittable today
**CONCEPT_PROPOSED_ENUM_ADDITIONS** GATED_BY **coordinated contract revision** — `SEMANTIC_CONTRACT.md` + `OBD_VOCABULARY.md §17` + COMLab schema
**PCV_STUCK_OPEN** (proposed) MAPS_TO **POA_SIGNATURE** — heavy rich at idle, clears at 2500 RPM
**TURBO_SEAL_OIL_LEAK** (proposed) MAPS_TO **POA_SIGNATURE** — high HC + stoich λ + ~0 CO
**HEAD_GASKET_OIL_BREACH** (proposed) MAPS_TO **COOLANT_LEAK_INTERNAL** — false-lean O₂ + suppressed NOₓ + oil emulsion
**CONCEPT_GLOSSARY** MAPS_TO **GAS_VOCABULARY.md** — canonical vocabulary definitions
**CONCEPT_GLOSSARY** DEFINES **AFR**, **Brettschneider equation**, **CE**, **Collision**, **Dual-idle test**, **Exhaust Gas Triangle**, **GasLabDnaView**, **Healthy-catalyst masking**, **Light-off**, **Masking rule**, **Modified Brettschneider**, **NDIR**, **OSC**, **Oxygen-usage**, **POA signature**, **Probe-occlusion test**, **Quench**, **Speed-Density vs MAF**, **STRESS_IDLE**, **Truth-vs-perception**, **TWC**

## Core Entities

- **CONCEPT_SOURCES** — research provenance: q1–q10, cases_petrol, casesextra, Denton, Wikipedia. Consumer: all wiki chunks via `sources` frontmatter.
- **CONCEPT_REFERENCE_TABLES** — normative numeric thresholds: warm-idle reference, UK MOT fast-pass, Brettschneider worked examples. Consumer: `gaslab.rule_engine` threshold dictionaries.
- **CONCEPT_PROPOSED_ENUM_ADDITIONS** — three candidate v2.x enum values (PCV_STUCK_OPEN, TURBO_SEAL_OIL_LEAK, HEAD_GASKET_OIL_BREACH). Not emittable; mapped onto existing values. Consumer: `CONCEPT_PROPOSED_ENUM_ADDITIONS` → `comlab/config/proposals/`.
- **CONCEPT_GLOSSARY** — 20-term definition list, canonical vocabulary cross-reference to `GAS_VOCABULARY.md`. Consumer: all wiki chunks, graphify entity resolution.
