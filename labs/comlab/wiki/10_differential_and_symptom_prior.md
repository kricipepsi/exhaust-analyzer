---
chunk_id: COMWIKI-10
title: Ranked Differential Output & the Symptom Prior
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: 'B.Q2: make the ranked top-k differential (with per-candidate calibrated
  confidence) the primary product output, score the engine on top-1 AND top-3, and
  abstain/flag low-support families. B.Q3: keep the operator-symptom prior as a bounded
  tie-breaker capped at a moderate likelihood ratio.'
entities_defined:
- CONCEPT_DIFFERENTIAL
- RULE_TOPK
- RULE_LOWSUPPORT_FLAG
- RULE_SYMPTOM_PRIOR
related_chunks:
- COMWIKI-06
- COMWIKI-08
- COMWIKI-09
- COMWIKI-12
sources:
- REWORK_PLAN_COMLab.md §3.B
- AUDIT_ANSWERS_COMLab.md Q8/Q10
- research pack B
- response.py
- symptom_router.py
- config/symptom_prior.yaml
node_type: wiki
lab: comlab
module: comlab
subsystem: differential-output
implements:
- labs/comlab/comlab/core/lab_pipeline_aggregator.py
- labs/comlab/comlab/core/symptom_router.py
- labs/comlab/comlab/schemas/response.py
consumers:
- 'comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py CONCEPT_DIFFERENTIAL
  / RULE_TOPK'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py RULE_SYMPTOM_PRIOR (capped
  0.65)'
- 'wired (pending T-WIRE-1): apps/wired/wired/composition.py OrchestratorFinalUIOutput
  rendering'
drift_guards:
- labs/comlab/tests/unit/test_symptom_router.py
- labs/comlab/tests/unit/test_symptom_prior.py
- labs/comlab/tests/unit/test_lab_pipeline_aggregator.py
tags:
- comlab
- differential-output
- wiki
source: labs/comlab/wiki/10_differential_and_symptom_prior.md
---

# Ranked Differential Output & the Symptom Prior

## Why a differential, not a forced top-1

The taxonomy is **not mutually exclusive** — ≥4 colliding pairs (`COMWIKI-06` `RULE_COLLISION_SET`),
so a forced top-1 must mislabel a fraction no matter the tuning (`AUDIT Q10`). On comparable
diagnostic tasks, the **top-1 → top-3 gap is +17–33 pp** (pack B §2). The honest, higher-yield
product is a **ranked differential**.

The mechanism already exists: `DifferentialSiblingOut` (max 5) is populated from
`runner_ups = scored[1:4]` in `response.py`; `fault_atlas_router` already emits siblings. The
rework **promotes** this from a back-compat extra to the primary output. Low code cost, high
honesty payoff.

## The differential as primary output {#CONCEPT_DIFFERENTIAL}

1. **Score the engine on top-1 AND top-3** (and "any-correct-in-k") in the eval harness — this
   reframes the achievable target away from a single number (`COMWIKI-12`).
2. **Make the differential the primary product output**, each candidate carrying its **calibrated
   posterior** (`COMWIKI-09`) and, where available, a **conformal prediction set** with a coverage
   guarantee.
3. **Keep a single lead verdict for back-compat** (the calibrated top-1).

*Files:* eval harness/metrics, `core/fault_atlas_router.py` (emits siblings), `schemas/response.py`.

### top-k construction {#RULE_TOPK}

The differential is the calibrated-and-ranked candidate set from the fusion stage:
`lead = argmax(posterior)`; `differential = top-k by posterior` (k≤5, default 3). Within a
colliding family (`COMWIKI-06`), members appear together with their relative confidence rather
than one being forced to win.

### Low-support abstention {#RULE_LOWSUPPORT_FLAG}

Per-family recall is reported with **binomial confidence intervals**; families with **< 10 cases**
are **not certified** and are flagged **low-support / anecdotal** in the output — routed to the
differential, never a hard verdict (`AUDIT`/pack C, `COMWIKI-12`). Resampling cannot create
absent separation, so this is a labelling-of-uncertainty rule, not a model change. A within-noise
**delta** is likewise non-diagnostic and abstains (`COMWIKI-11`).

## The operator-symptom prior {#RULE_SYMPTOM_PRIOR}

Single self-reported symptoms are **weak-to-moderate** evidence — likelihood ratio ≈ 1–3, rarely
> 4 — and must be capped **below** strong objective evidence (LR > 10) (pack B §3). Today the
prior is `prior_weight 0.10`, bounded-additive, with ~0 false-positive delta but tiny lift
(`AUDIT Q8`).

**Decision:** keep the symptom as a **bounded prior that breaks ties only**; encode the cap as an
**LR ceiling at a "moderate" band**, discounted further when the symptom is vague or second-hand.
The symptom can never push a confidence tier on its own (`COMWIKI-09`). This folds into
`T-COMV2-CTXMOD-1`, which also consumes `SymptomDNA…load_state` as a **context modifier** and caps
symptom-prior weighting at **65 % trust**. No expansion of symptom influence. *Files:*
`config/symptom_prior.yaml`, `core/symptom_router.py`. The tier_1/tier_2 → fault-family routing
keys are registered as proposal `COMLab-A` (`COMWIKI-13`). [v2: B.Q3]

## Graph relations (explicit)

**CONCEPT_DIFFERENTIAL** IS **the primary product output** (single lead retained for back-compat)
**RULE_TOPK** BUILT_FROM **calibrated posteriors (COMWIKI-09)** OVER **fusion output (COMWIKI-08)**
**DifferentialSiblingOut** POPULATED_FROM **runner_ups = scored[1:4]** (response.py)
**RULE_LOWSUPPORT_FLAG** ROUTES **<10-case families** TO **differential** (not a hard verdict)
**RULE_SYMPTOM_PRIOR** CAPPED_AT **moderate LR / 65 % trust** VIA **T-COMV2-CTXMOD-1**
**symptom routing keys** REGISTERED_AS **proposal COMLab-A (COMWIKI-13)**
**OrchestratorFinalUIOutput** RENDERED-BY **apps/4DLabWired/wired/composition.py**

## Core Entities

- **CONCEPT_DIFFERENTIAL** — Ranked differential of candidate faults. Consumer: `comlab/core/lab_pipeline_aggregator.py`.
- **RULE_TOPK** — Top-k (default 3, max 5) candidate selection by posterior. Consumer: `comlab/core/lab_pipeline_aggregator.py`.
- **RULE_LOWSUPPORT_FLAG** — Flagging of minority fault families with <10 cases as low-support. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
- **RULE_SYMPTOM_PRIOR** — Symptom prior weight capping to prevent symptom swamping. Consumer: `comlab/core/symptom_router.py`.
