---
chunk: pids-protocol/08_dtc-state-machine-and-confidence-weighting
topic: pids-protocol
sources:
  - Advanced Automotive Fault Diagnosis (Tom Denton, 2nd ed., Elsevier 2006) §5.4.4 "MIL activation logic / healing / pending codes / freeze frame"
  - cardiagnosis (Marić 2013) — Pending codes P0xxxx* (../../cardiagnosis_prepped.md §Pending codes)
consumer: DTCLab DTC-state weighting (assign each ingested DTC a state → a confidence weight) → COMLab fault-atlas routing, which must route a CONFIRMED code harder than an unconfirmed PENDING one and treat a MIL-off HISTORY code as a possible-intermittent, not "fixed". The `dtc_state` field (per code) + its DTCLab/fault-atlas reader ship together (v2 forward-progress).
consumer_status: PROPOSAL
provenance: AdvAutomotiveFaultDiagnosis.txt §5.4.4 + cardiagnosis pending-codes section — readable prose; cycle counts intact
related: [[../fuel-trim/15_pcm-memory-freezeframe-verification]], [[06_readiness-monitors-and-absence-of-dtc-trust]], [[01_mode06-freezeframe-nostart-method]]
dedup: fuel-trim/15 already pins the temporal numbers (3-trip MIL-off, ≥40 warm-up auto-erase) but uses them ONLY for the trim `CODES_RECENTLY_CLEARED` gate and freeze-frame ferry. THIS chunk is the canonical DTC-state→**confidence** model consumed by DTCLab/COMLab routing, and it adds the **pending** stage (which 15 omits). Numbers are cross-referenced, not re-derived.
---

# DTC state machine → confidence weight

## Why state, not just presence

A DTC is not a boolean. The same P-code carries very different evidential weight
depending on its **lifecycle state**: an unconfirmed *pending* code may be a
one-off glitch, a *confirmed* code (MIL on) is a repeated, verified fault, and a
*history* code (MIL healed) may be a still-present intermittent. The fault-atlas
must weight these differently or it chases ghosts and trusts false "all-clear"s.

## The lifecycle (cite, do not invent)

```text
PENDING   → failure stored immediately on first detection; MIL NOT lit.
            (shown with '*' / 'PD' on scan tools)            [LOW confidence]
CONFIRMED → same failure recurs on the 3rd consecutive driving cycle
            → MIL illuminated; freeze-frame captured at failure  [HIGH confidence]
HISTORY   → MIL de-activated after 3 subsequent fault-free driving
            cycles; code remains stored                 [MEDIUM — possible intermittent]
ERASED    → code + distance + freeze-frame auto-clear after ≥ 40
            warm-up cycles with no re-failure                    [n/a]
```

- A **driving cycle** = start-up → a drive mode that would detect the fault →
  shut-off. A **warm-up cycle** = coolant +22 °C and ≥ 70 °C (see `06`).
- Some codes are **two-trip** (need 2 cycles to confirm), some **one-trip**
  (catalyst-damaging / safety-critical confirm in 1) — per fuel-trim/15.
- *Scope edge:* MY~2010+ adds **permanent DTCs** (Mode $0A) that a scan-tool
  clear cannot remove — only a clean monitor re-run clears them. At the very top
  of the 1990–2010 window; flag as a forward-note, not a 2006-era guarantee.

## State → confidence weight (the consumer contract)

| `dtc_state` | Meaning | Routing weight |
|---|---|---|
| `PENDING` | unconfirmed, MIL off | **low** — corroborate before routing; never sole basis for a definitive verdict |
| `CONFIRMED` | recurred, MIL on, freeze-frame present | **high** — full routing weight; freeze-frame conditions usable |
| `HISTORY` | MIL healed but stored | **medium** — treat as possible intermittent; do NOT read as "fixed" |
| `PERMANENT` | clear-resistant (MY2010+) | **high** — independent of clear state |

Reader = DTCLab DTC-state weighting → COMLab `fault_atlas_router`:

- ingest `dtc_state` per code (manual-entry / scan field, mirroring the
  `fuel_system_status` dropdown pattern — 4DApp has no live comms);
- a `PENDING` code must not, alone, justify a definitive fault-family verdict
  (pairs with cardiagnosis book-1's "pending = take into account, don't act
  blindly"); a `CONFIRMED` code routes at full weight; a `HISTORY`/MIL-off code
  is flagged possible-intermittent, never "clear".

Per signal/noise, `dtc_state` ships **only** with the DTCLab/fault-atlas reader
that weights it; register in `comlab/config/proposals/`.

Citation: pending→3-cycle-confirm→3-cycle-heal→≥40-warm-up-erase per Denton
§5.4.4; one-/two-trip + auto-erase numbers cross-referenced from
fuel-trim/15 (FuelTrimFamilies.md / Fuel Trim Diagnostics.txt); pending-code
diagnostic stance per cardiagnosis (Marić) Pending-codes section.


## Core Entities

- dtc_state, PENDING, CONFIRMED, HISTORY, PERMANENT
- DTCLab DTC-state weighting -> COMLab fault_atlas_router (PROPOSAL)

## Graph relations (explicit)

**dtc_state** PENDING CARRIES low routing weight
**dtc_state** CONFIRMED CARRIES high routing weight
**dtc_state** HISTORY INDICATES possible intermittent, not fixed
**dtc_state** PERMANENT IS clear-resistant
**dtc_state** EMITTED_BY DTCLab and CONSUMED_BY **fault_atlas_router**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
