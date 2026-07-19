---
proposal_id: EP-GAS-01
title: GASLab 5-gas physical schema + Brettschneider λ for digital-vs-physical divergence
target_lab: GASLab (schema + chem) → COMLab fusion
source: proposals/wikiResearch.md §4; proposals/OBD_ImplProp.md §1 (FiveGasSnapshot)
type: schema + analytics_module
status: PROPOSAL (named consumer; ground-truth channel)
date_extracted: 2026-06-07
---

## What it proposes
A physical 5-gas snapshot schema (`co2_pct, o2_pct, co_pct, hc_ppm, nox_ppm`) and the
Brettschneider λ calculation, so the engine has a **chemical ground-truth λ_chem** to set
against the ECU's perceived λ_obd:

    λ = ([CO2] + CO/2 + [O2] + NOx + (Hcv/4 − Ocv/2)·([CO2]+[CO]))
        / ((1 + Hcv/4 − Ocv/2)·([CO2] + [CO] + K·[HC]))

## Diagnostic rationale
wikiResearch flags the absence of a physical-gas channel as the gap that makes
internal-ECU detection impossible — without λ_chem there is nothing to expose the ECU's
"digital lie." This is the truth half of truth-vs-perception (PRD §5).

## Proposed consumer + code path
GASLab emits `lambda_chem`; consumed by COMLab `perception_contradiction.py` and the
cross-delta engine ([[EP-COM-03_lambda-cross-delta-engine]]) and the ECU checker. Numeric
constants (Hcv, Ocv, K) carry wiki citations per CLAUDE.md.

## Related
[[EP-COM-03_lambda-cross-delta-engine]] · [[EP-COM-04_ecu-hardware-fault-checker]] ·
[[EP-GAS-02_misfire-chemistry-resolver]].
