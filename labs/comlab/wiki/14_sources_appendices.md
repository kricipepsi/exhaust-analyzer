---
chunk_id: COMWIKI-14
title: "Sources, Target Architecture & Appendices"
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: "The target architecture diagram for the reworked spine, the rework-level success criteria and what-NOT-to-do, the human/manager gate decisions, the full source list (research packs A–E + standards), and a glossary."
entities_defined: [CONCEPT_TARGET_ARCH, CONCEPT_SUCCESS_CRITERIA, CONCEPT_HUMAN_GATES, CONCEPT_GLOSSARY]
related_chunks: [COMWIKI-00, COMWIKI-08, COMWIKI-09, COMWIKI-10, COMWIKI-11, COMWIKI-12]
sources: [REWORK_PLAN_COMLab.md §4/§6/§7, research README.md, "packs A–E", standards]
---

# Sources, Target Architecture & Appendices

## Target architecture (the reworked spine) {#CONCEPT_TARGET_ARCH}

```
ingest (+ provenance flags, optional 2nd frame)                 schemas/ingestion.py     COMWIKI-02
   │
Stage-A validity gates per modality (dilution, RPM, warm, CL)   → modality may ABSTAIN    COMWIKI-07/11
   │
per-lab per-channel DELTA (only when 2nd frame present)         analytics/delta_engine.py COMWIKI-11
   ├─ temporal align (gas ~10 s lag, last-5 s window)            E.Q1
   ├─ architecture gate FIRST (speed-density null / turbo inv.)  D.Q4  ← mandatory
   └─ normalise + uncertainty  z_c = Δ_c/σ_Δc                    E.Q2
   │
CONFLICT-AWARE LATE FUSION (evidence = 13 consumers + deltas)    new fusion stage          COMWIKI-08
   ├─ agreement → corroborate ; disagreement → conflict feature  A.Q2 / E.Q3
   ├─ inverse-variance weighting (anti-swamping)                 A.Q3
   └─ Bayesian log-odds first → DS/PCR5 where needed             E.Q4
   │
CALIBRATION  fused score → posterior (Platt/temp) → LR tiers     calibrator                COMWIKI-09
   │
RANKED DIFFERENTIAL  top-3 + per-candidate calibrated confidence response.py               COMWIKI-10
        (single lead verdict retained for back-compat)
   │
SINGLE_POINT degradation fallback = today's additive path (byte-identical when no 2nd frame) COMWIKI-07
```

The additive single-point ranker is **retained as a degradation mode**, not deleted. The rework
is **additive and default-off at the seams** — which is what makes it shippable under the
regression-lock rule.

## Success criteria (rework-level) {#CONCEPT_SUCCESS_CRITERIA}

Done means:

- The engine reports **top-1 and top-3** (+ any-correct-in-k) on a **measured-real,
  provenance-audited eval subset**, with **calibrated** confidence (reliability / ECE / Brier
  shown), per-family **recall CIs**, and abstention on low-support families and within-noise
  deltas.
- The fusion stage is **grep-confirmed read in a live path**; the single-point path is
  **byte-identical** when no second frame / no calibration data (regression-locked).
- Every new numeric literal (noise floors, lag, tiers, bands) carries a source citation; every
  new field has a named consumer in the same change (`COMWIKI-13`).

### Do NOT

- Chase **85 %** on the current corpus — below the measured ceiling (R1); set the target from
  Gate-Data (`COMWIKI-12`).
- **Weight-tune** the additive ranker (proven 0 pp; "scoring tightening is a smell") — skip F2
  unless M1 shows gaps < 0.10.
- Build the delta module **live** before Gate-Capture, or rebuild the corpus inside the delta
  task.
- Add cross-lab imports, emit verdicts from emitter labs, or rebuild any graph.
- Treat synthetic-corpus accuracy as real before the sim-to-real holdout test.

## Decisions for the human / manager {#CONCEPT_HUMAN_GATES}

1. **Gate-Capture (product, dominant):** can the field workflow capture a second operating-point
   frame (low idle + ~2500 RPM, optionally + ~3750 RPM stress)? The GAS/OBD schemas already
   support it — this is a corpus/workflow *population* decision, not a build. Yes → the delta
   rework is real; No → record DeltaLab deferred-pending-data.
2. **Target:** accept a **measured ceiling (~70–80 %) + decision-support differential** product,
   or fund real data collection to lift the ceiling?
3. **Canonical operating-point pair:** confirm **curb idle + 2500 RPM** (stress idle 3750
   optional), closing band reconciliation before `T-COMV2-DELTA-1` builds.
4. **Fusion family:** approve the staged path (Bayesian log-odds + conflict feature → DS/PCR5
   where needed → stacking only if a paired dataset is funded).

## Sources {#CONCEPT_GLOSSARY}

**Rework synthesis:** `research/REWORK_PLAN_COMLab.md` (the authoring spine for chunks 08–14).

**Research packs (A–E):**

- A — scoring + evidence fusion: `Automotive Diagnostic Fusion Research.md`, `deep-research-report.md`.
- B — calibration + differential + symptom prior: `WEB_RESEARCH_PROMPT_B_*`, pack-B synthesis.
- C — corpus quality + label noise: `WEB_RESEARCH_PROMPT_C_*`, `deep-research-reportC.md`.
- D — two-point delta fixtures: `DeltaRes1.md`, `Two-Point Emissions Test Fixture Design.md`,
  `WEB_RESEARCH_PROMPT_D_*`.
- E — gas↔OBD cross-reference: `Multi-Sensor Fusion for Automotive Diagnostics.md`, `DeltaRes2.md`,
  `WEB_RESEARCH_PROMPT_E_*`.

**Audit & levers:** `AUDIT_ANSWERS_COMLab.md`, `AUDIT_PART1_CEILING_RESEARCH.md`,
`OPEN_LEVERS_COMLab.md`, `PROPOSAL_DeltaLab_cross_lab_delta_module.md`.

**Design docs:** `docs/COMLab_{PRD,HLD,DLD,LLD}.md`. **Ledger:** `tasks/PROGRESS.md`.

**Cross-lab wikis:** GASWIKI-00…11, DTCWIKI-00…12, `obdlab/wiki/OBDLab_KG_Wiki.md`, DNALab.

**Standards (cited inline at literals):** SAE J1979/J2012, ISO 15031-5/-6, ISO 14229 UDS,
EPA/BAR two-speed-idle, ECE R51 / ISO 5130 (stress idle), SAE J1635 (cold-start symptoms).

**Retired:** `ARCHIVE/2026-06-20_comlab_wiki_v1/` — the v1 wiki (provenance only; do not cite).

## Glossary

- **OUTRANKED bucket** — the ~82–90 cases where the correct rule scored but lost to a higher-
  `base_weight` generic; the whole accuracy game.
- **degradation mode** — FULL_FUSION / GAS_DOMINANT / FATAL_INCOMPLETE / SINGLE_POINT.
- **abstain** — a modality/channel declining to vote (validity gate failed, within-noise delta,
  or on the Δ abstain set); feeds the fusion graceful-degradation path.
- **provenance flag** — observed / derived / imputed / synthetic / manual-override / sentinel /
  out-of-range / saturated.
- **two-speed idle** — curb idle + 2500 RPM no-load; the canonical delta operating-point pair.
- **conflict-as-feature** — channel disagreement fed to fusion as evidence, never a forced override.

## Graph relations (explicit)

**CONCEPT_TARGET_ARCH** ASSEMBLES **COMWIKI-02 → 07 → 11 → 08 → 09 → 10** (+ SINGLE_POINT fallback)
**CONCEPT_SUCCESS_CRITERIA** REQUIRES **top-1+top-3 on GATE_DATA subset** WITH **calibration metrics**
**CONCEPT_HUMAN_GATES** GATE **target + Gate-Capture + operating-point pair + fusion family**
**research packs A–E** GROUND **COMWIKI-08…12**
**ARCHIVE/2026-06-20_comlab_wiki_v1** SUPERSEDED_BY **this corpus**

## Core Entities

- **CONCEPT_TARGET_ARCH** — Stage 4 fusion and calibration target architecture assembly. Consumer: `COMLab architecture`.
- **CONCEPT_SUCCESS_CRITERIA** — Top-1 and top-3 performance criteria on GATE_DATA. Consumer: `COMLab validation`.
- **CONCEPT_HUMAN_GATES** — Human manager gates for target and capture decisions. Consumer: `COMLab administration`.
- **CONCEPT_GLOSSARY** — Glossary of terms and cross-lab reference citations. Consumer: `COMLab glossary/documentation`.
