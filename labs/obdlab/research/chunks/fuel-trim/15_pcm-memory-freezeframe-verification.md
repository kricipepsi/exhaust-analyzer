---
chunk: fuel-trim/15_pcm-memory-freezeframe-verification
topic: fuel-trim
sources:
  - FuelTrimFamilies.md §"Strategic Synthesis of PCM Memory Logic"
  - Fuel Trim Diagnostics.txt §"Fuel Trim Data Storage" + §"3 trips / 40 warm-up cycles"
consumer: TrimAnalyticsGate.CODES_RECENTLY_CLEARED (active — demote trims within N cycles of a clear) + OBDLivePayload.freeze_frame_pids ferry from DTCLab (active — freeze-frame trims consumed at L4). The "verify under freeze-frame conditions" workflow and Field Service Mode are method/reference. STFT-volatile-vs-LTFT-KAM persistence informs the reset-handling gate.
consumer_status: ACTIVE (CODES_RECENTLY_CLEARED + freeze_frame_pids) + method notes
provenance: sources/fuel-trim/FuelTrimFamilies.md + Fuel Trim Diagnostics.txt
related: [[06_trim-rails-and-sentinels]], [[08_validity-preconditions]], [[09_fault-family-case-matrix]], [[../pids-protocol/08_dtc-state-machine-and-confidence-weighting]]
---

# PCM memory, freeze-frame & repair verification

## Trim persistence (why a reset invalidates trims)

- **STFT is volatile** — erased at key-off, restarts at 0 % each run.
- **LTFT lives in KAM** — persists across key cycles; reset only by PCM power
  loss, scan-tool reset, or DTC erase, then relearned over ~1 drive cycle.

Consequence (already gated): within < 1 drive cycle of `codes_cleared`, LTFT is
mid-relearn and meaningless → `TrimAnalyticsGate.CODES_RECENTLY_CLEARED` demotes
trim-derived candidates (cross-ref `06`, `08`). This chunk supplies the *why* and
the relearn window.

## DTC temporal memory (freeze-frame is the diagnostic context)

| State | Behaviour |
|---|---|
| **Active DTC** | Set on a failed monitor (1 cycle, or 2 for two-trip codes). Captures **freeze-frame** = engine snapshot at failure. |
| **History DTC** | MIL turns **off after 3 consecutive fault-free trips**, but the code stays in History. |
| **Auto-erase** | History + freeze frame auto-clear after **40 consecutive warm-up cycles** with no re-failure. |

Diagnostic rules that follow:

- **Never clear codes before reading freeze frame** — clearing destroys the
  snapshot (RPM, load, ECT, STFT/LTFT at the moment of failure) needed to
  reproduce an intermittent fault. The freeze-frame trims are consumed at the L4
  layer via `freeze_frame_pids`.
- A MIL that is **off** does not mean fixed — check History + freeze frame; the
  3-trip rule may have masked a still-present intermittent fault.
- For intermittents, drive the car to the freeze-frame conditions to re-provoke.

## Field Service Mode (method/reference)

Grounding the OBD-I test terminal (or 16-pin designated terminal) with the engine
running puts supported GM PCMs into Field Service Mode: observe real-time trim
response **without setting new DTCs** during testing. Reference only — no engine
consumer; useful guidance for a future guided-diagnostic feature.

Citation: FuelTrimFamilies.md PCM memory logic (Active/History DTC, 3-trip MIL-off,
40-warm-up-cycle auto-erase, freeze-frame); Fuel Trim Diagnostics.txt STFT-volatile
/ LTFT-KAM persistence and Field Service Mode.


## Core Entities

- STFT, LTFT, KAM, TrimAnalyticsGate.CODES_RECENTLY_CLEARED, freeze_frame_pids
- TrimAnalyticsGate.CODES_RECENTLY_CLEARED + freeze_frame_pids (consumer, active)

## Graph relations (explicit)

**STFT** IS_VOLATILE erased at key-off
**LTFT** PERSISTS_IN **KAM**
**codes_cleared** RESETS **LTFT** and TRIGGERS **TrimAnalyticsGate.CODES_RECENTLY_CLEARED**
**freeze_frame_pids** FERRIED_FROM DTCLab and CONSUMED at L4
History DTC CLEARS MIL after 3 trips and auto-erases after 40 warm-up cycles

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
