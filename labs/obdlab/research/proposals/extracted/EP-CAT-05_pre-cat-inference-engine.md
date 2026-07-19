---
proposal_id: EP-CAT-05
title: Pre-cat inference engine (model feed-gas from inlet/outlet temp differential)
target_lab: catalyst + COMLab (L5)
source: various/Vol1.md "Systemic Masking" / Pre-Cat Inference Engine
type: analytics_module
status: PROPOSAL (named consumer)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Model what the feed-gas (pre-cat) chemistry must have been, from the heat the catalyst
generates — inferred via the inlet/outlet temperature differential — so a highly efficient
catalyst cannot fully mask engine misbehaviour.

## Diagnostic rationale
Modern cats are "filters of truth": they hide rich-running / oil-burn until catastrophic
failure (Vol1 N-008 cat-masked oil burn). Inferring pre-cat gas from cat heat exposes the
masked fault before meltdown. Complements the post-cat masking rule.

## Proposed consumer + code path
COMLab L5 reads cat inlet/outlet ΔT (IR or modelled) + post-cat gas to infer pre-cat λ;
asserts `Catalyst_Masking_*` earlier. Builds on the catalyst field-test inputs.

## Dependencies / related
[[EP-CAT-02_cat-masking-detection]] · [[EP-CAT-04_catalyst-field-tests]] · [[EP-COM-10_l5-prognostic-scoring]].
