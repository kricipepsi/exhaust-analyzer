---
proposal_id: EP-DNA-02
title: Per-lab slim DNA views (e.g. ObdLabDnaView) for sensor topology context
target_lab: DNALab → translation labs
source: proposals/DataFlow.md §Phase 1; sources/o2-logic/O2logic.md (composition map)
type: schema
status: PROPOSAL (named consumer; cross-lab input dependency)
date_extracted: 2026-06-07
---

## What it proposes
DNALab resolves the VIN into a master `VehicleDNA` then projects **slim, targeted views**
(`ObdLabDnaView`, etc.) carrying only what each translator needs — e.g. O₂ sensor
topology (narrowband vs wideband, bank/sensor positions, downstream role), number of
banks, aspiration, fuel-system type, emissions tier.

## Diagnostic rationale
`composition.py` maps sensor type → `WIDEBAND_LINEAR` / `NARROWBAND_0_TO_1V` driven by the
view; bank count drives the asymmetry audit. Keeps the full DNA out of the translators
(typed JSON boundary, no cross-lab import).

## Proposed consumer + code path
`apps/wired/wired/composition.py` builds the views; OBDLab `o2_normalizer` / bank logic
consume them.

## Related
[[EP-OBD-13_bank-asymmetry-audit]] · [[EP-OBD-17_wideband-offset-failure-mode]] ·
[[EP-DNA-01_dynamic-graph-pruning]].
