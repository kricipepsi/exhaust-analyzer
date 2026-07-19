---
proposal_id: EP-OBD-14
title: Semantic-consistency physics gates (blown ground trace, trim saturation)
target_lab: OBDLab (core/semantic_consistency_checker.py)
source: proposals/OBD_ImplProp.md §2.C and §3 (Gates A–C)
type: analytics_module
status: PROPOSAL (consumer proposed, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Add physics gates that assert thermodynamic plausibility and separate digital lies from
real faults:
- **Blown-ground-trace gate:** engine physically warm but `fuel_status = Open_Loop_Cold`
  and `coolant_temp_c = −40 °C` (floating minimum) ⇒ raise `SemanticConsistencyError`
  mapped to vaporized internal sensor-ground trace.
- **Trim-saturation gate:** total trim beyond ±127 ⇒ `ValueError` (storage limit).
- **ADC-input gate:** OBD upstream-O₂ flatline <0.15 V + railed trims, but physical
  5-gas λ < 0.90 ⇒ ECU ADC port failure rather than a real lean condition.
- **Catalyst-vs-cap-leak gate:** downstream mimics upstream but trims balanced (±5 %) ⇒
  traditional catalyst failure, not capacitor-leak ripple.

## Diagnostic rationale
Operationalises "semantic coherence vs digital divergence" at the OBDLab boundary so
COMLab is never handed physically impossible state.

## Proposed consumer + code path
Producer OBDLab `core/semantic_consistency_checker.py`; the verdicts feed COMLab
[[EP-COM-04_ecu-hardware-fault-checker]] and [[EP-COM-05_semantic-coherence-paradigm]].

## Dependencies / related
[[EP-ECU-04_sensor-ground-trace-blown]] · [[EP-ECU-06_adc-mux-failure]] ·
[[EP-GAS-01_5gas-brettschneider-schema]].
