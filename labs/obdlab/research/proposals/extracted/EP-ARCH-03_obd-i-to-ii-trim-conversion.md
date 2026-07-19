---
proposal_id: EP-ARCH-03
title: OBD-I ↔ OBD-II fuel-trim scale conversion (PID encoding)
target_lab: OBDLab / pids-protocol
source: chunks/delta-relations/README (unhomed); sources/fuel-trim/FuelTrimW.md
type: reference_formula
status: PROPOSAL (named consumer; unique image-locked formula)
date_extracted: 2026-06-07
---

## What it proposes
Capture the OBD-I→OBD-II trim conversion so legacy 0–255 trim values normalise to percent:

    Trim% = ((Value − 128) / 128) × 100%   (0–255 scale, 128 = baseline / 0 %)

## Diagnostic rationale
A unique, previously image-locked formula needed to ingest pre-OBD-II / raw-byte trim
data on the 1990–2010 fleet; without it legacy values are mis-scaled.

## Proposed consumer + code path
OBDLab PID-ingestion/normalisation when a raw 0–255 trim byte is supplied. Numeric
literals carry wiki citation. Routes to the pids-protocol chunk pass (DR-FU-1).

## Related
[[EP-OBD-15_physical-sensor-bounds-config]] · [[EP-OBD-16_state-translation-rules]].
