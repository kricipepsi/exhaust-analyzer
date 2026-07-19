---
proposal_id: EP-CAT-02
title: Catalyst masking detection (Catalyst_Masking_Rich / _Lean)
target_lab: catalyst + GASLab → COMLab
source: sources/o2-logic/master_catalyst_guide.md §4
type: fault_node
status: PROPOSAL (named consumer; high-value safety rule)
date_extracted: 2026-06-07
---

## What it proposes
Surface `Catalyst_Masking_Rich` when a **healthy** cat scrubs the evidence of a
**rich-running engine**: negative LTFT at idle and cruise, tailpipe λ within the cat
window (0.97–1.03), tailpipe HC/CO normal, but **pre-cat O₂ stuck rich** (>0.7 V). The
rare mirror `Catalyst_Masking_Lean` also defined.

## Diagnostic rationale
Without this rule the engine returns `insufficient_evidence` for a serious rich condition
(leaking injector, high fuel pressure, GDI HPFP failure) and lets the user drive away with
a damaged engine temporarily saved by the cat — the guide calls this the single most
common misdiagnosis to defend against.

## Proposed consumer + code path
COMLab `fault_atlas_router` reads pre-cat O₂ + GASLab tailpipe λ + LTFT sign to assert the
masking node. Register in `comlab/config/proposals/`.

## Related
[[EP-GAS-01_5gas-brettschneider-schema]] · [[EP-CAT-01_osc-damping-monitor]].
