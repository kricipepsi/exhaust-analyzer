---
proposal_id: EP-CAT-03
title: false_P0420 cluster (demote catalyst-failure when feed-gas is clean)
target_lab: catalyst → COMLab
source: sources/o2-logic/master_catalyst_guide.md §3, §8
type: routing_gate + fault_node
status: PROPOSAL (named consumer, not yet wired)
date_extracted: 2026-06-07
---

## What it proposes
Surface `false_P0420_suspected` when active P0420/P0430 co-occurs with: no misfire DTC,
trims within ±10 %, IR-temp test pass, tailpipe gases within with-cat reference, no
exhaust leak. Also `dtc_set_outside_enable_window` when the freeze-frame shows the monitor
ran outside its strict enable conditions (ECT < 70 °C, OL, RPM not steady).

## Diagnostic rationale
The catalyst is fine and the monitor is glitching (aged rear sensor, ECU calibration
drift, tight threshold). Prevents needless converter replacement.

## Proposed consumer + code path
COMLab catalyst routing reads DTCLab freeze-frame + trims + GASLab tailpipe values to
demote the candidate. Register in `comlab/config/proposals/`.

## Related
[[EP-CAT-01_osc-damping-monitor]] · [[EP-DTC-03_dtc-enable-window-gate]] ·
[[EP-CAT-04_catalyst-field-tests]].
