---
proposal_id: EP-DTC-04
title: Mode-06 / Freeze-Frame no-start method + immobilizer/security branch
target_lab: DTCLab (FF/Mode06 parser) → COMLab fault_atlas (no-start)
source: various/Vol4.md (30 era no-start cases, Mode $06 MID/TID + Mode $02 FF); chunks/pids-protocol/01
type: analytics_module
status: PROPOSAL (named consumer)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
A no-start isolation method using Mode $06 monitor test-value-vs-limit + Mode $02 freeze
frame, with a dedicated **security/immobilizer branch**: a Misfire Monitor reading
"Incomplete"/all-zero CIDs (monitor aborted, no ignition authorised) flags a lock-out
(GM Passlock/Passkey, Ford PATS) — vs a mechanical no-start where the engine tried and failed.

## Diagnostic rationale
A pure DTC list cannot split "engine forbidden to fire" from "engine failed to fire." The
aborted-monitor state is itself the discriminator. Crank-no-start vs no-crank-no-start.

## Proposed consumer + code path
DTCLab parses Mode $06 MID/TID (Misfire $A1/$53, Fuel $81, EGR $41) + Mode $02 FF; COMLab
fault_atlas adds a no-start branch. New input fields (Mode-06 value/limit pairs, FF cut
flags) earn place via this consumer.

## Dependencies / related
[[EP-DTC-01_dtc-causal-hierarchy]] · [[EP-DNA-03_euro-era-tier-gate]] · chunks/pids-protocol/01.
