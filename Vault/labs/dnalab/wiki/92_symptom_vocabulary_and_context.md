---
chunk_id: DNAWIKI-92
title: "Structured symptom vocabulary & symptom × context"
lab: dnalab
doc: DNA_WIKI
role: research-evidence
status: authoritative
date: 2026-06-12
kg_ingestion: none
consumer: "COMLab-A (tier_1,tier_2) routing ; COMLab-B context modifiers ; SymptomLab catalog"
raw_inputs: "../answersDNA.md §3, §4"
related_chunks: [DNAWIKI-90, DNAWIKI-91]
---

# Structured symptom vocabulary & symptom × context

**Disposition: research-evidence.** Numbers `routes-to:` COMLab / SymptomLab consumers; the
real home is the COMLab proposals registry + the SymptomLab catalog. (DNA10 Q5, Q6.)

## Part A — what standard symptom vocabulary professionals actually use (Q5)

Professional diagnosis runs on **standardised taxonomies**, not free text — which validates
SymptomLab's closed-catalog design (page 91, Finding 2).

```
# source: SAE J1930 / J2012 (ISO 15031-6), standards
# finding: J2012 defines >11,000 DTCs in a fixed P/C/B/U structure; J1930 mandates terminology
routes-to: COMLab-A (tier_1,tier_2) → fault-family routing
routes-to: SymptomLab catalog mapping (the CLOSED pair vocabulary is the standardised intake)
```

| Standard | Focus | Top-level structure |
|---|---|---|
| **SAE J1930 / ISO** | mandated terminology (CARB/EPA) | fixed acronyms — MAF, EGR, TWC, etc. |
| **SAE J2012 / ISO 15031-6** | DTC architecture (>11,000 codes) | 1st char system: **P**owertrain / **C**hassis / **B**ody / **U** network · 2nd char: 0 generic / 1 manufacturer · 3rd char sub-system: 1–2 air-fuel, 3 ignition, 4 aux-emissions, 5 idle, 6 computer/outputs, 7–9 transmission |
| **OEM guided diagnostics** (Ford/DAF/Porsche) | Universal Symptom Surveys + guided trees | functional areas → component systems → symptom flowcharts mapping to DTCs/PIDs |

```
# scope-warning (carry verbatim): SAE J3016 is NOT a diagnostic/symptom standard — it defines
# driving-automation Levels 0–5 and is irrelevant to powertrain troubleshooting. Do not cite it.
```

**Read for COMLab/SymptomLab:** the SAE P/C/B/U + sub-system grid is the external anchor the
two-tier catalog maps onto; the standards confirm a *closed* vocabulary is industry practice,
not a project quirk. Proprietary scan-tool symptom trees are trade secrets (gap).

## Part B — how environmental context shifts the fault (Q6)

The core principle is **validated and universal**: co-occurring context shifts the posterior
fault probability. The specific failure modes the research cites come from **2019–2024
vehicles and are era-mismatched** to the 1990–2010 petrol scope — they are kept only as
*structural analogies*, never as 1990–2010 facts.

```
# source: GM TSBs 22-NA-224 / PIP5651G (industry, post-2012 — ERA MISMATCH, analogy only)
# finding: low-idle (P0506) + underboost (P0299) + MAF (P0101) → disconnected CAC tube, not throttle body
routes-to: COMLab-B context modifiers (PATTERN: co-occurring codes re-rank the family)
```

```
# source: GM TSB 21-NA-124 (industry, post-2012 — ERA MISMATCH, analogy only)
# finding: EVAP small leak (P0442) + "hard start after refuel" → stuck-open purge solenoid over filler-cap seal
routes-to: COMLab-B context modifiers (starting-context re-ranks the EVAP cause)
```

```
# source: GM TSB 24-NA-124 (industry, post-2012 — ERA MISMATCH, analogy only)
# finding: no-start/stall (P2534) + blown bay fuse → harness rub-through over ignition switch
routes-to: COMLab-B context modifiers (circuit-load context re-ranks)
```

```
# source: TRUE / ICCT remote-sensing report (peer-reviewed, 2020; 60M+ samples)
# finding: older petrol emissions deteriorate sharply with thermal context — NO can ~double near 30°F (-1.1°C)
routes-to: COMLab-B context modifiers (cold-start context raises catalyst / O2-performance fault priors)
```

**Read for COMLab:** the actionable, in-scope signal is the **thermal/cold-start** one (the
TRUE data is fleet-wide, not model-specific). The TSB examples justify the *mechanism*
("occurs-during" + co-occurring evidence changes the answer) that COMLab-B context modifiers
implement against the SymptomLab `occurs_during` / `engine_state` / `load_state` axes — but
their specific codes must **not** be hard-coded as 1990–2010 truth.

## Gap

No unified cross-manufacturer database maps (ambient temp × fuel trim × load) → specific
component failure. So context modifiers should stay **coarse, axis-level rules**, not
fine-grained lookup tables. Logged as a question, not a finding.



## Graph relations (explicit)

**SAE J2012 / ISO 15031-6** DEFINES **>11,000 DTCs in P/C/B/U structure** (PROPOSAL — COMLab-A routing anchor; COMLab-A not live)
**SAE J1930** MANDATES **standardized diagnostic terminology** (PROPOSAL — SymptomLab vocabulary external anchor)
**CLOSED symptom vocabulary** IS **industry practice, not a project quirk** (PROPOSAL — validates SymptomLab catalog design)
**P/C/B/U + sub-system grid** MAPS_ONTO **SymptomLab two-tier catalog** (PROPOSAL)
**co-occurring codes** RE_RANK **fault family probability** (PROPOSAL — COMLab-B context modifiers mechanism; COMLab-B not live)
**occurs_during / engine_state / load_state axes** ENABLE **context-sensitive re-ranking** (PROPOSAL — COMLab-B)
**thermal/cold-start context** RAISES **catalyst / O2-performance fault priors** (PROPOSAL — TRUE/ICCT fleet data; COMLab-B)
**TSB examples (GM 22-NA-224 etc.)** ARE **era-mismatched structural analogies** (PROPOSAL — must NOT be hard-coded as 1990–2010 facts)
**SAE J3016** IS_NOT a diagnostic/symptom standard (driving-automation Levels 0–5; irrelevant to powertrain — scope warning)
**cross-manufacturer context→fault database** IS_A **genuine gap** (QUESTION — context modifiers stay coarse, axis-level)

## Core Entities

- `COMLab-A (tier_1,tier_2) routing` — symptom→fault-family routing; STATUS: PROPOSAL
- `COMLab-B context modifiers` — co-occurring evidence re-ranking; STATUS: PROPOSAL
- `SymptomLab catalog` — CLOSED two-tier symptom vocabulary; consumer: COMLab-A (PROPOSAL)
- `SAE J2012 / ISO 15031-6` — DTC architecture standard; external anchor
- `occurs_during / engine_state / load_state` — context axes for re-ranking
