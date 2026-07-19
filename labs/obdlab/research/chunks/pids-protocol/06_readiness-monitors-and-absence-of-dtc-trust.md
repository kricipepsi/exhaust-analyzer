---
chunk: pids-protocol/06_readiness-monitors-and-absence-of-dtc-trust
topic: pids-protocol
sources:
  - Advanced Automotive Fault Diagnosis (Tom Denton, 2nd ed., Elsevier 2006) §5.4.6 "Monitors and readiness flags", §5.4.5 "OBD cycles", §5.3 monitor taxonomy
consumer: obdlab `analytics_preconditions` — a monitor-readiness precondition that demotes/qualifies any "no-fault" (absence-of-DTC) inference whose owning monitor is Not-Ready or whose readiness was reset by battery-disconnect / scan-tool clear, before fault-atlas routing. Also feeds truth-perception `Perception_Reliability_Index` / `ECU_Consistency_Score` (monitor-completeness as a trust input). The manual-entry readiness summary field + its reader ship together (v2 forward-progress).
consumer_status: PROPOSAL
provenance: AdvAutomotiveFaultDiagnosis.txt §5.4.5/5.4.6 — prose + readiness counts/cycle definitions intact (no image-strip)
related: [[../fuel-trim/08_validity-preconditions]], [[../fuel-trim/14_dtc-enable-criteria-and-blocking-codes]], [[../fuel-trim/15_pcm-memory-freezeframe-verification]], [[../truth-perception/02_lambda-delta-vector-and-scoring]]
dedup: the DTC-state machine (3 trips / ≥40 warm-up cycles) and trim relearn-after-clear are already in fuel-trim/15 and fuel-trim/08 — NOT repeated here. This chunk adds the cross-monitor "absence-of-DTC trust" gate (catalyst / EVAP / O2 / EGR / misfire / secondary-air), which no existing chunk covers.
---

# Monitor readiness & the trustworthiness of a *missing* DTC

## The reliability principle (why this gates KG ingestion)

Every other chunk reasons about the values that **are** present (trims, λ, gas).
This chunk reasons about a **silence**: when a DTC is *absent*, is that silence
trustworthy? In OBD-II it is trustworthy **only if the monitor responsible for
that fault has actually run to completion** since the last memory clear. A monitor
that has not completed reports **no fault because it never looked** — not because
the system is healthy. Encoding "no DTC ⇒ component OK" into the KG without this
qualifier is the single most dangerous false-truth the engine can ingest.

## Readiness flags (monitor status)

Each emissions monitor carries a **readiness flag**: `Ready` (a.k.a. "Complete")
or `Not-Ready` ("Incomplete"). The flag indicates whether the monitor has finished
its self-evaluation sequence since the fault memory was last cleared.

- **Continuous monitors** — **misfire** and **fuel-system** — run whenever their
  enable conditions hold and are essentially always Ready on a warm, driven car.
- **Non-continuous (conditional) monitors** — **catalyst, EVAP, O2 sensor, O2
  heater, EGR, secondary-air** — run only under specific preconditions and are
  frequently `Not-Ready` on a car that was recently serviced or only short-tripped.

```text
absence_of_dtc_trust(monitor):
  Ready      -> trust "no DTC for this monitor" as a real negative
  Not-Ready  -> DO NOT trust the silence; the monitor never evaluated
```

## What resets readiness to Not-Ready (the trap)

Readiness flags are reset to `Not-Ready` by:

- a **battery disconnect** (also wipes KAM / learned long-term fuel trim), and
- a **scan-tool fault-memory clear**.

So a freshly-cleared or battery-changed car shows **"no codes" with most monitors
`Not-Ready`** — a clean-looking scan that proves almost nothing. This is the same
hazard `fuel-trim/08` guards for trims (`codes_cleared ≥ 1 drive cycle`) and
`fuel-trim/15` guards for the relearn window — generalised here to **all**
emissions monitors and to the absence-of-DTC inference itself.

## When can a scan be trusted for a test? (era allowance)

A car is considered ready for a valid OBD test when at most a small number of
flags remain `Not-Ready`:

- **Model year 1996–2000:** up to **2** monitors may be `Not-Ready`.
- **2001 onward:** at most **1** monitor may be `Not-Ready`.

(Petrol 1990–2010 scope: pre-1996 cars predate standardised OBD-II readiness.)

## Cycle definitions that drive readiness (cite, do not invent)

- **Driving cycle** = engine start-up → a drive mode in which the malfunction
  would be detected if present → engine shut-off.
- **Warm-up cycle** = coolant rises **≥ 22 °C** from start **and** reaches a
  **minimum of 70 °C**. (4DApp captures at operating temperature **≥ 75 °C**,
  which sits safely above this warm-up floor — see truth-perception / CTS logic.)

## FMEM note (a *value* analogue of the same trap)

Readiness qualifies a missing **DTC**; **FMEM** (failure-mode effects management /
limp-home) qualifies a present **PID value**. On a sensor fault the PCM substitutes
a **safe default value** for that sensor and runs on it. A PID read while its
sensor's circuit DTC is active is therefore a *fabricated default, not a
measurement* and must be down-trusted. This is the mechanism behind the
prerequisite-DTC gate in [[../fuel-trim/14_dtc-enable-criteria-and-blocking-codes]]
and is given its own full treatment in [[07_fmem-limp-home-substituted-values]]:
**sensor-circuit DTC active ⇒ that sensor's PID is FMEM-default ⇒ demote any
candidate that reads it.**

## Consumer / code path (signal-noise)

Input (manual entry, mirroring the `fuel_system_status` dropdown pattern of
`fuel-trim/08`, since 4DApp ingests user-entered scan data — no live comms):

- `monitor_readiness` — a per-monitor or summarised Ready/Not-Ready map
  (catalyst, EVAP, O2, O2-heater, EGR, misfire, fuel-system, secondary-air).
- optional `recently_cleared` / `battery_reset` boolean (already partially carried
  as `codes_cleared`).

Reader = `obdlab/obdlab/core/analytics_preconditions.py`:

1. For any candidate justified by the **absence** of a monitor's DTC, if that
   monitor is `Not-Ready` (or readiness was reset) → **demote/suppress** the
   candidate (the negative is unproven), exactly as `fuel_trim_invalid` demotes
   trim candidates.
2. Pass `monitor_readiness` completeness to truth-perception
   `Perception_Reliability_Index` / `ECU_Consistency_Score` as a trust input — a
   scan with many `Not-Ready` flags yields a lower reliability index.

Per signal/noise, the `monitor_readiness` field ships **only** together with this
`analytics_preconditions` reader (forward-progress proposal — register the field
in `comlab/config/proposals/` alongside the gate).

Citation: readiness flags, continuous vs conditional monitors, battery-disconnect/
scan-clear reset, and the MY1996–2000 ≤2 / 2001+ ≤1 allowance per Denton §5.4.6;
driving-cycle and warm-up-cycle (+22 °C / ≥70 °C) definitions per Denton §5.4.5;
monitor taxonomy per Denton §5.3; FMEM per Denton §5.2.1.


## Core Entities

- monitor_readiness, Ready, Not-Ready, value_is_fmem
- analytics_preconditions -> Perception_Reliability_Index (PROPOSAL)

## Graph relations (explicit)

**monitor_readiness** Not-Ready INVALIDATES absence-of-DTC inference
battery disconnect RESETS **monitor_readiness** to Not-Ready
**monitor_readiness** CONSUMED_BY **analytics_preconditions** to demote unproven negatives
**monitor_readiness** completeness FEEDS **Perception_Reliability_Index**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
