---
proposal_id: EP-ECU-03
title: ECU fault node — high-power ignition-coil driver (IGBT) shorted
target_lab: fault-atlas (new node) → COMLab ECU checker
source: chunks/ecu-diagnosis/04; proposals/OBD_ImplProp.md FAULT 5
type: fault_node
status: PROPOSAL (consumer = EP-COM-04)
date_extracted: 2026-06-07
---

## Signature
IGBT driver shorted closed melts the coil primary → permanent single-cylinder no-spark.
**Deceptive λ ≈ 1.01** (OBD looks fine) but raw **HC ≥ 1800–2200 ppm**, O₂ ≥ 4.5 %, CO
≤ 0.3 %, single-cylinder misfire count climbing. Under stress idle the raw fuel + air
exotherm threatens catalyst meltdown (>900 °C).

## Why deceptive λ matters
Stoichiometric-looking λ is exactly why the standard bias detector misses it; the checker
must route on the HC/O₂/misfire chemistry, not λ.

## Proposed consumer + code path
[[EP-COM-04_ecu-hardware-fault-checker]] (symptom → IGNITION_MISFIRE / CATALYST_OVERWHELMED).
Register in `comlab/config/proposals/`.

## Related
[[EP-OBD-IN-07_per-cylinder-misfire-counts]] · [[EP-CAT-04_catalyst-field-tests]] ·
[[EP-COM-07_misfire-vs-fuelling-gate]].
