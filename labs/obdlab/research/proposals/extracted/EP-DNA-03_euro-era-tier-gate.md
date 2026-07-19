---
proposal_id: EP-DNA-03
title: Euro-era emissions-tier gate + make/era fault priors
target_lab: DNALab (tier resolution) → COMLab fault_atlas
source: various/Vol6.md (Euro 1–6 eras); various/Vol4.md + Vol8.md (make/era cases); chunks/taxonomy/01-02
type: analytics_module + schema
status: PROPOSAL (named consumer)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
DNALab resolves the Euro emissions tier + era (1990–2000 / 2000–2010 / 2010–2020) from
VIN/year, gating which monitors/aftertreatment exist (wideband, GPF, e-thermostat) and which
fault families are plausible. Plus a make/era prior layer (Ford FPDM, Chrysler TIPM, BMW HPFP…).

## Diagnostic rationale
Prevents proposing an era-impossible fault (GPF-clog only Era 3; distributor PIP only Era 1)
and lets fault_atlas weight candidates by manufacturer known-failure patterns.

## Proposed consumer + code path
DNALab emits `euro_tier` + `era` in the slim DNA views; COMLab fault_atlas enables/disables
family branches and applies make/era priors. Extends [[EP-DNA-01_dynamic-graph-pruning]].

## Dependencies / related
[[EP-DNA-01_dynamic-graph-pruning]] · [[EP-DNA-02_slim-dna-views]] · chunks/taxonomy/01 · chunks/taxonomy/02.
