---
proposal_id: EP-COM-15
title: 30-case truth-vs-perception test corpus (validation asset)
target_lab: COMLab (test/validation) + fault_atlas pattern set
source: various/Vol1.md N-001..N-030; chunks/truth-perception/03
type: test_corpus
status: PROPOSAL (named consumer; labelled fixtures)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Register the 30 Vol1 cases (N-001..N-030) as labelled test fixtures: each carries λ_obd,
λ_chem, Δλ, 5-gas values, DTC, and the expected L3/L4/L5 verdict — a ready-made corpus to
validate perception_contradiction + fault_atlas against ground truth.

## Diagnostic rationale
The engine's truth-vs-perception logic needs labelled discrepancy scenarios to test
against; these span 1990–2020 and cover blindness / inversion / masking / hallucination
classes the unit suites do not.

## Proposed consumer + code path
COMLab test harness loads the corpus; novel cases (ghost-misfire hallucination, double-liar
cancellation, model-shift) also seed new fault_atlas PROPOSAL patterns.

## Dependencies / related
[[EP-COM-05_semantic-coherence-paradigm]] · [[EP-COM-11_tcg-root-source-attribution]] · chunks/truth-perception/03.
