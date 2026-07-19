---
proposal_id: EP-GAS-03
title: Combustion-integrity + oxygen-usage chemical metrics
target_lab: GASLab (chemical resolver) → COMLab
source: various/Vol1.md "Combustion Integrity Truth"; chunks/truth-perception/04
type: analytics_module + schema
status: PROPOSAL (named consumer)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Two derived GAS metrics, computable from 5-gas alone:
- `chemical_efficiency = CO2 / (CO2 + CO)` — fraction of carbon fully oxidised; <~0.95 ⇒
  fundamental combustion failure.
- `oxygen_usage_factor` (O₂ vs CO) — high O₂+high HC/CO ⇒ misfire; high CO+~0 O₂ ⇒ rich.

## Diagnostic rationale
Discriminates combustion failure from fuelling error without OBD data; the chemical basis
of the misfire-vs-fuelling gate. Distinct from [[EP-GAS-02_misfire-chemistry-resolver]]
(which emits the categorical state) — these are the quantified ratios behind it.

## Proposed consumer + code path
GASLab emits both ratios; COMLab fault_atlas misfire family + the misfire-vs-fuelling gate
read them. Display forms stated in Vol1 prose (CO2/(CO2+CO) standard); flagged readable-
prose-derived, not reconstructed.

## Dependencies / related
[[EP-GAS-02_misfire-chemistry-resolver]] · [[EP-COM-07_misfire-vs-fuelling-gate]] · chunks/truth-perception/04.
