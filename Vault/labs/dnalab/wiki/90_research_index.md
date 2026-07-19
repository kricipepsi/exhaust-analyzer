---
chunk_id: DNAWIKI-90
title: "DNA-prior research — index, status & sources"
lab: dnalab
doc: DNA_WIKI
role: research-evidence
status: authoritative
date: 2026-06-12
kg_ingestion: none
consumer: "COMLab proposals registry (every number below routes-to a named COMLab entry)"
raw_inputs: "../answersDNA.md ; ../DNA10.md"
related_chunks: [DNAWIKI-00, DNAWIKI-91, DNAWIKI-92, DNAWIKI-93, DNAWIKI-94]
---

# DNA-prior research — index, status & sources

**Disposition: research-evidence (routes out to COMLab).** This half of the wiki documents
*how far the operator-symptom + VIN-identity channel can be trusted*. Its numbers are
COMLab-owned: every figure on pages 91–94 carries a `# source:` and a `routes-to: COMLab-…`
tag. A finding with no nameable COMLab consumer is left as an open question, not written as
a finding. Raw inputs: `../answersDNA.md`, `../DNA10.md`.

## Headline (the reason this research exists)

The operator-symptom + VIN channel is the **cheapest independent input** into COMLab, but it
is **weak and must stay a prior, never an override**. Reported symptoms are noisy
(expert-rule baseline ≈ 50% accuracy; 30–70% of warranty returns are No-Trouble-Found), and
VIN decode is *region-dependent* — precise in North America, frequently **blind to engine
spec in Europe/RoW** (the `ZZZ` VDS placeholder) and corrupted by aftermarket mods a VIN
cannot see. The numbers below are the evidence for setting COMLab's report-trust cap,
symptom-prior weight, and identity-channel trust honestly.

## The DNA10 questions → where each is answered

| # | DNA10 question | Page | Status |
|---|---|---|---|
| Q1 | Operator-symptom predictiveness | `91` | answered (web) |
| Q9 | False / misleading report rate (NTF) | `91` | answered (web) |
| Q5 | Structured symptom vocabulary techs use | `92` | answered (web) |
| Q6 | Symptom × context → fault | `92` | answered (web) |
| Q2 | VIN-decode resolution 1990–2010 | `93` | answered (web) |
| Q3 | Per-engine reference-data (CoC) availability | `94` | answered (web) |
| Q7 | Aftermarket-mod prevalence | `94` | answered (web) |
| Q10 | Labeled symptom→fault datasets exist? | below + `91` | answered (web) |
| Q4 | Which identity attributes change the diagnosis | `93`, `94` | partial — feeds full/basic decision |
| Q8 | Does finer identity (`model`) matter | `93` | partial — `model` can stay empty |

## routes-to map (the consumer for each research theme)

```
91 predictiveness + NTF ─▶ COMLab-B  report-trust cap        (how hard to lean on the symptom prior)
                        ─▶ COMLab-F  symptom-prior weighting  (prior strength bands)
92 vocabulary           ─▶ COMLab-A  (tier_1,tier_2) routing  (+ SymptomLab catalog mapping)
92 context              ─▶ COMLab-B  context modifiers
93 VIN-decode resolution─▶ VINLab    decode-confidence field  (+ deferred full/basic tier)
                        ─▶ COMLab    identity-channel trust
94 reference-data (CoC) ─▶ VINLab    CoC / rated_rpm fields
94 aftermarket mods     ─▶ COMLab    identity-trust cap       (known-unknown that lowers confidence)
```

Where a `routes-to:` target is a **proposed** (not yet existing) COMLab entry, that is
allowed under the v2-rework rule: the finding and the COMLab consumer that reads it ship
**together as a proposal**. What is not allowed is a number with no nameable consumer at all.

## Consolidated source table

| Source / identifier | Type | Year | Claim it supports | Access |
|---|---|---|---|---|
| Deep-SBM diagnostic model (Cognitran Ltd data) | peer-reviewed | 2020 | hand-crafted RMI rule-bases peak ≈ 50% accuracy; Deep-SBM maps 2,093 inputs → ~3,000 fault classes | free |
| KG-LLM diagnostic framework (German OEM) | peer-reviewed | 2024 | dialogue-based framework reaches 77.3% accuracy (+46.1% over baseline LLM) | free |
| G-OBD diagnostic assistant | peer-reviewed | 2024 | 89.3% accuracy vs certified-mechanic verdicts across 450 DTC instances | free |
| Symestic / MES diagnostics | industry | 2026 | NTF/RTOK rates 30–70% of returns; €50–€500 per false claim | free |
| Text-mining diagnostic study | peer-reviewed | 2015 | customer symptom logs ill-structured; "engine" has >20 spellings | free |
| SAE J1930 / J2012 (ISO 15031-6) | standard | — | mandated terminology; >11,000 DTC definitions; P/C/B/U structure | standard |
| ISO 3779 / 4030 + NHTSA 49 CFR 565 | standard | — | 17-char VIN layout; modulo-11 check digit (NA) | standard |
| Grokipedia Porsche VIN | industry | 2024 | RoW Porsche used `ZZZ` placeholders in VDS positions 4–6 | free |
| EPA certification archives | dataset | 2026 | public CoC / test-result archives span MY 1979–2013 | free |
| EPA tampering surveys | government | 1984/1986/1989 | gasoline tampering 19–22% overall; catalyst removal 3–11%; O2 ~1% | free |
| Dataintelo tuning-market analysis | industry | 2025 | petrol = 41.2% of $9.8B remap market; Europe 32.7% ($3.2B) | paid |
| SciencePG ECU-tuning study | peer-reviewed | 2026 | remap power gains up to 25% (turbo) / 15% (NA) | free |
| TRUE / ICCT remote-sensing report | peer-reviewed | 2020 | oldest 11–14% of fleet emit ~50% of NO mass; cold-temp deterioration | free |
| Identifix / ALLDATA | industry | 2024 | leading commercial symptom→repair history datasets (paid) | paid |

## Could not be found (genuine gaps — no number shipped)

- No open-source, multi-brand lexicon translating **raw driver complaints → SAE DTCs**
  without a proprietary mapping engine (Identifix-class).
- No nationwide government survey isolating **tampering/remap rates for 1990–2010 petrol
  passenger cars within the current (2020–2026) fleet** — modern surveys focus on diesel
  pickups.
- No public confusion matrix mapping **raw driver-written text → physical fix** without an
  intermediate DTC.

These stay questions. They are the empirical inputs the deferred **full/basic** dataset
decision (`../research/DEFERRED_full_basic_dataset_decision.md`) will need before it can be
scoped.



## Graph relations (explicit)

**91 predictiveness + NTF** ROUTES_TO **COMLab-B report-trust cap** (PROPOSAL — COMLab-B not live)
**91 predictiveness + NTF** ROUTES_TO **COMLab-F symptom-prior weighting** (PROPOSAL — COMLab-F not live)
**92 symptom vocabulary** ROUTES_TO **COMLab-A (tier_1,tier_2) routing** (PROPOSAL — COMLab-A not live)
**92 symptom vocabulary** ROUTES_TO **SymptomLab catalog mapping** (PROPOSAL)
**92 context modifiers** ROUTES_TO **COMLab-B context modifiers** (PROPOSAL)
**93 VIN-decode resolution** ROUTES_TO **VINLab decode-confidence field** (PROPOSAL — deferred full/basic tier)
**93 VIN-decode resolution** ROUTES_TO **COMLab identity-channel trust** (PROPOSAL)
**94 reference-data (CoC)** ROUTES_TO **VINLab CoC / rated_rpm fields** (PROPOSAL)
**94 aftermarket mods** ROUTES_TO **COMLab identity-trust cap** (PROPOSAL)
**ALL research findings** ROUTES_TO **COMLab proposals registry** (labs/comlab/comlab/config/proposals/) — PROPOSAL, not live
**Deep-SBM / KG-LLM / G-OBD sources** SUPPORT **symptom-channel trust cap evidence** (PROPOSAL — validation constraint)
**Identifix / ALLDATA datasets** ARE **commercial/proprietary** (PROPOSAL — validation constraint, not a shippable literal)
**No open complaint→fix dataset** IS_A **genuine gap** (QUESTION, not a finding)

## Core Entities

- `COMLab-A` — (tier_1,tier_2) symptom routing; STATUS: PROPOSAL (not live)
- `COMLab-B` — report-trust cap + context modifiers; STATUS: PROPOSAL (not live)
- `COMLab-F` — symptom-prior weighting; STATUS: PROPOSAL (not live)
- `COMLab proposals registry` — labs/comlab/comlab/config/proposals/; home for all research findings
- `Deep-SBM / Cognitran (2020)` — source for ~50% symptom→fault accuracy ceiling
- `TRUE / ICCT remote-sensing (2020)` — source for fleet-wide emissions deterioration data
- `EPA certification archives` — source for CoC/test-result data MY 1979–2013
