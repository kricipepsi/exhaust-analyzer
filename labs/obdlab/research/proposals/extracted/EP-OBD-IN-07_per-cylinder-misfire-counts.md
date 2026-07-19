---
proposal_id: EP-OBD-IN-07
title: Add per-cylinder misfire counts (Mode 06 / 200- & 1000-rev) as input fields
target_lab: OBDLab (input) → COMLab (fault_atlas misfire localiser)
source: proposals/AddObdFields.md §Part 2.5; chunks/fuel-trim/11
type: input_field
status: PROPOSAL (consumer proposed, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Ingest **per-cylinder misfire counts** (`misfire_count[cyl]`) over 200 and 1000 engine
revolutions (Mode 06 / enhanced stream). A misfiring cylinder pumps fresh O₂ past the
sensor and creates a **false-lean** trim indication.

## Diagnostic rationale
- Positive trims (>15 %) + single-cylinder count escalating ⇒ localised cylinder fault
  (coil, plug, leaking injector).
- High positive trims + misfires spread randomly across all cylinders ⇒ global fuel
  starvation (weak pump).
- Δ-signature: misfires that clear at 2500 RPM ⇒ vacuum leak / dirty injector; misfires
  that spike at 2500 RPM ⇒ ignition breakdown or fuel-volume starvation.
- **Catalyst protection:** sustained misfire >1 % of events is the meltdown boundary
  (see [[EP-CAT-04_catalyst-field-tests]]).

## Proposed consumer + code path
`comlab/core/fault_atlas_router.py` misfire localiser + the misfire-vs-fuelling pre-route
gate ([[EP-COM-07_misfire-vs-fuelling-gate]]).

## Dependencies / related
[[EP-COM-07_misfire-vs-fuelling-gate]] · [[EP-ECU-03_coil-driver-failure]] ·
[[EP-FA-04_fuel-water-contamination]].
