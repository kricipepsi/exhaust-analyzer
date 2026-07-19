---
proposal_id: EP-CAT-01
title: Catalyst OSC damping-ratio monitor (post-cat/pre-cat switching ratio)
target_lab: catalyst (new chunks/catalyst) → COMLab
source: sources/o2-logic/master_catalyst_guide.md §2-3; O2logic.md (TI_cat)
type: analytics_module
status: PROPOSAL (named consumer; catalyst split pending SWEEP §4.3)
date_extracted: 2026-06-07
---

## What it proposes
Model oxygen-storage-capacity (OSC) as the damping the cat applies to O₂ swings. Compute
the post-cat-to-pre-cat switching ratio (healthy ≥ 2:1; approaching 1:1 ⇒ P0420/P0430).
Optionally the signal-transfer index `TI_cat = σ(V_down)/σ(V_up)`.

## Diagnostic rationale
The damping ratio is the principal evidence of the OBD catalyst monitor; encoding it lets
the engine reason about borderline vs failed cats rather than just echoing P0420.

## Proposed consumer + code path
A `chunks/catalyst/` model feeding COMLab `fault_atlas_router` catalyst family. Strict
enable conditions (ECT ≥ 70 °C, 2000–3000 RPM cruise, CL, no misfire/trim DTC) gate it.

## Related
[[EP-CAT-03_false-p0420-cluster]] · [[EP-OBD-17_wideband-offset-failure-mode]] ·
[[EP-CAT-04_catalyst-field-tests]].
