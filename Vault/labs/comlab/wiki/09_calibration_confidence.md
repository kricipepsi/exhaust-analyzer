---
chunk_id: COMWIKI-09
title: "Confidence Calibration — making the number mean a likelihood"
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: "B.Q1 of the rework: replace evidence-completeness confidence tiers with a post-hoc calibration layer that maps the fused score to a real posterior, redefine tiers as likelihood-ratio/posterior bands, and verify with reliability diagrams / ECE / Brier. Under the small/imbalanced/noisy corpus, prefer Platt/temperature over isotonic and use conformal prediction for finite-sample coverage."
entities_defined: [CONCEPT_CALIBRATION, CONCEPT_CONF_TIER, CONCEPT_CONFORMAL, CONCEPT_CALIB_METRICS]
related_chunks: [COMWIKI-08, COMWIKI-10, COMWIKI-12]
sources: [REWORK_PLAN_COMLab.md §3.B/§8.4, AUDIT_ANSWERS_COMLab.md Q5, "research pack B", "research pack C"]
---

# Confidence Calibration — making the number mean a likelihood

## The problem

Today `ConfidenceRating ∈ {HIGH_ASSURANCE, DEGRADED_ASSURANCE, LOW_CERTAINTY}` reflects
**evidence-chain completeness, not calibrated correctness** (`AUDIT Q5`). A "HIGH_ASSURANCE"
verdict does not mean the diagnosis is probably right — only that the inputs were present. The
rework makes confidence a **real likelihood**.

## The calibration layer {#CONCEPT_CALIBRATION}

Add a **post-hoc calibration layer** after the fusion stage (`COMWIKI-08`) that maps the fused
score → a calibrated posterior, then to tiers re-defined as posterior / likelihood-ratio bands.

**Method choice under this corpus (small, imbalanced, noisy — pack C):**

- **Prefer Platt / sigmoid or temperature scaling over isotonic regression.** Isotonic overfits
  the single-digit minority-class bins here and is not validated for many-minority-class
  imbalance; sigmoid's extra intercept also helps under imbalance ("Better Classifier Calibration
  for Small Data Sets", REWORK_PLAN §8.4). [v2: B.Q1 + §8.4]
- **Fit on a minority-stratified calibration split**, using only `observed`-provenance rows
  (`COMWIKI-02` `CONCEPT_PROVENANCE`).
- **Calibrate before fuse, per modality** where modalities are first combined (REWORK_PLAN §8.4),
  then calibrate the fused score.

**Hard dependency:** calibration is **meaningless on noisy/synthetic labels**. It must be fit on
the **Gate-Data measured-real eval subset** (`COMWIKI-12`). Until that subset exists, the tiers
are **expert-set priors, flagged as such** in the output. *Files:* `schemas/vocabulary.py` (tier
definitions), fusion-stage calibrator.

## Conformal prediction for the differential {#CONCEPT_CONFORMAL}

Rather than trusting a calibrated top-1, use **conformal prediction** to give the ranked
differential (`COMWIKI-10`) a **finite-sample coverage guarantee** — the prediction set contains
the true fault with a chosen probability, which is exactly what a small, imbalanced corpus can
honestly support. [v2: B.Q1 + §8.4]

## Confidence tiers redefined {#CONCEPT_CONF_TIER}

Tiers become **posterior / likelihood-ratio bands** (the BI-RADS / O-RADS pattern), not
adjectives describing evidence completeness. Indicative banding (literals are expert priors until
Gate-Data calibration sets them):

| Tier | Meaning (post-calibration) | Provisional band |
|---|---|---|
| `HIGH_ASSURANCE` | calibrated posterior strongly favours the lead | posterior ≳ 0.80 |
| `DEGRADED_ASSURANCE` | lead favoured but within a plausible differential | 0.50–0.80 |
| `LOW_CERTAINTY` | no candidate dominates; differential is the product | < 0.50 |

The symptom prior is capped as a **moderate-LR ceiling** so it can never push a tier on its own
(`COMWIKI-10` `RULE_SYMPTOM_PRIOR`).

## Verification metrics {#CONCEPT_CALIB_METRICS}

A confidence claim ships only with the calibration evidence (`COMWIKI-12` success criteria):

- **Reliability diagram** — predicted vs observed frequency per bin.
- **ECE** (Expected Calibration Error) — aggregate miscalibration.
- **Brier score** — sharpness + calibration combined.

These are computed on the Gate-Data subset; "accuracy improved" claims are gated on the same
subset (`COMWIKI-12`).

## Graph relations (explicit)

**CONCEPT_CALIBRATION** MAPS **fused score (COMWIKI-08)** TO **calibrated posterior**
**CONCEPT_CALIBRATION** USES **Platt/temperature** (not isotonic) UNDER **small/imbalanced corpus**
**CONCEPT_CALIBRATION** DEPENDS_ON **GATE_DATA eval subset (COMWIKI-12)**
**CONCEPT_CONF_TIER** REDEFINED_AS **posterior/LR bands** (not evidence completeness)
**CONCEPT_CONFORMAL** GUARANTEES **finite-sample coverage** FOR **CONCEPT_DIFFERENTIAL (COMWIKI-10)**
**CONCEPT_CALIB_METRICS** (reliability/ECE/Brier) GATE **any accuracy claim**

## Core Entities

- **CONCEPT_CALIBRATION** — Platt/temperature scaling mapping scores to likelihood posteriors. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
- **CONCEPT_CONF_TIER** — Posterior/likelihood-ratio bands mapping diagnostic confidence. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
- **CONCEPT_CONFORMAL** — Conformal prediction sets guaranteeing finite-sample coverage. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
- **CONCEPT_CALIB_METRICS** — Expected calibration error and reliability verification metrics. Consumer: `COMLab validation`.
