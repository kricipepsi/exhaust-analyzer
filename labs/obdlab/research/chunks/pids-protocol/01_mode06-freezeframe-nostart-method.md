---
chunk: pids-protocol/01_mode06-freezeframe-nostart-method
topic: pids-protocol
sources:
  - various/Vol4.md — Mode $06 (On-Board Monitor Test Results) + Mode $02 (Freeze Frame) for no-start isolation; 30 era cases
consumer: DTCLab freeze-frame / Mode-06 parser → COMLab fault_atlas (no-start branch). FF+Mode06 let the engine isolate crank-no-start vs no-crank-no-start without guessing.
consumer_status: PROPOSAL (no-start branch + Mode-06 MID/TID parse not yet in v2; names DTCLab producer + COMLab reader)
provenance: sources/various/Vol4.md — READABLE; real LaTeX survives ($<40×Disp$, $λ≈1.000$); Mode/MID/TID hex intact
dedup: new — pids-protocol pack was empty
---

# Mode 06 + Freeze Frame method for no-start isolation

A DTC says *where*; **Mode $06** (component monitor test values) and **Mode $02**
(freeze frame) say *why* — critical when the engine cranks but will not start and no
running PIDs exist.

## The diagnostic signatures (Vol4)

- **Immobilizer lock-out** (GM Passlock/Passkey, Ford PATS): Mode $06 Misfire Monitor
  (MID $A1 / TID $53) reads **"Incomplete"/all-zero CIDs** — the monitor aborted
  because no ignition was authorised. FF shows fuel/spark cut at key-on. → security,
  not mechanical.
- **CKP/CMP signal loss** (thermal VR failure, solder defect): Misfire monitor cannot
  run (no engine-speed profile); FF RPM = 0 with sync DTC.
- **Fuel system**: Mode $06 Fuel System Monitor (MID $81 / TID $01/$02) value vs
  Max/Min limit, e.g. +28 %/+32 % over a +20/+25 % limit = Failed (lean), or −25 %
  over a −15 % limit (rich).
- **EGR**: Mode $06 EGR Monitor (TID $41) value 65,227 vs max 896 = stuck/failed.
- **MAF rationality** (mechanical proxy): MAF "Fails to reach Peak ($< 40 \times
  \text{Disp.}$ g/s at WOT)".

## Logic
The "Incomplete/aborted" monitor state is itself diagnostic: it distinguishes a
**security lock-out** (engine forbidden to fire) from a **mechanical no-start**
(engine tried, failed). A pure DTC list cannot make that split.

## Consumer / code path
DTCLab parses Mode $06 MID/TID test-value-vs-limit + Mode $02 FF; COMLab fault_atlas
adds a no-start branch keyed on monitor-aborted + FF cut state. New input fields
(Mode-06 test value/limit pairs, FF cut flags) earn their place only via this consumer.


## Core Entities

- Mode06, Mode02, MID, TID, CKP_SENSOR_DROPOUT, immobilizer_lockout
- DTCLab FF/Mode06 parser -> COMLab fault_atlas no-start branch (PROPOSAL)

## Graph relations (explicit)

**Mode06** misfire-monitor Incomplete INDICATES **immobilizer_lockout**
**CKP_SENSOR_DROPOUT** PREVENTS misfire monitor (FF RPM=0)
**Mode06** fuel-system monitor value-vs-limit FLAGS lean or rich
**Mode06** PARSED_BY DTCLab and CONSUMED_BY **COMLab fault_atlas** no-start branch

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
