---
proposal_id: EP-OBD-15
title: Broad physical-sensor-bounds config to survive ECU-fault float values
target_lab: OBDLab (config/physical_sensor_bounds.json)
source: proposals/OBD_ImplProp.md §1.A
type: config
status: PROPOSAL (consumer = ingestion validator, exists)
date_extracted: 2026-06-07
---

## What it proposes
Configure `PIDIngestionValidator` bounds wide enough that ECU-fault float readings reach
the analyser instead of being rejected at ingestion:
- `engine_rpm` 0–8000 · `coolant_temp_c` −40…130 °C · `throttle_pos_pct` 0–100 ·
  `map_kpa` 10–120 · `maf_gps` 0–300 · trims −100…+100 % (clamp ±127 in checker).

## Diagnostic rationale
If bounds are too tight, a −40 °C floated ECT (blown ground) fails validation and the
pattern is never analysed — the diagnostic engine would discard exactly the data that
proves the ECU fault.

## Proposed consumer + code path
OBDLab `core` ingestion validator reads this file at startup. Pairs with the
semantic-consistency gates that interpret the out-of-range-but-valid values.

## Dependencies / related
[[EP-OBD-14_semantic-consistency-gates]] · [[EP-OBD-16_state-translation-rules]].
