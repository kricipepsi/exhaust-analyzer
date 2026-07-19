---
chunk: fuel-trim/17_per-cylinder-misfire-counts
topic: fuel-trim
sources:
  - proposals/AddObdFields.md §Part 2.5 — per-cylinder misfire counts (Mode 06 / 200- & 1000-rev)
  - chunks/fuel-trim/11_ignition-misfire-cases-and-trim-discriminator — misfire↔false-lean trim link
  - proposals/extracted/EP-OBD-IN-07_per-cylinder-misfire-counts.md
consumer: COMLab `fault_atlas_router` misfire localiser + the misfire-vs-fuelling pre-route gate (EP-COM-07). Per-cylinder counts localise single-cylinder vs global causes and guard against a misfire-driven false-lean trim mis-route.
consumer_status: PROPOSAL (EP-OBD-IN-07 — OBDLab-owned input field; consumer named)
availability: Mode-06 / enhanced stream. Per-cylinder counts are **portable on CAN (≈2008+)**; pre-CAN MID/TID are per-OEM. OBDLab carries its **own** field — a DTC is not always set and DTCLab may not be in use, so loop state / counts cannot depend on DTCLab (audit RQ-D).
dedup: fuel-trim/11 carries the misfire↔trim *discriminator logic*; this chunk adds the per-cylinder *count fields* that feed localisation. pids-protocol/01 carries the Mode-06 *no-start* monitor-state branch (different consumer).
---

# Per-cylinder misfire counts (Mode 06, 200- & 1000-rev)

`misfire_count[cyl]` over 200 and 1000 engine revolutions. A misfiring cylinder pumps fresh O₂ past
the upstream sensor and creates a **false-lean** trim reading — so misfire counts must be read
alongside trims, not after them.

## Discriminators

| Pattern | Reading |
|---|---|
| Positive trim (`> 15 %`) + **one** cylinder's count escalating | **localised** cylinder fault (coil, plug, leaking injector) |
| High positive trim + counts **spread randomly** across all cylinders | **global** fuel starvation (weak pump) |
| Δ-signature: counts **clear** at 2500 RPM | vacuum leak / dirty injector |
| Δ-signature: counts **spike** at 2500 RPM | ignition breakdown or fuel-volume starvation |

## Catalyst-protection boundary

Sustained misfire **> 1 % of events** is the catalyst-meltdown threshold — a hard escalation flag
the localiser raises independently of the fuelling diagnosis (cross-ref catalyst field tests).

## Why OBDLab-owned (RQ-D)

The misfire-vs-fuelling discriminator must run even when no DTC is stored and even when DTCLab is
not in the session, so the per-cylinder counts are an **OBDLab input field**, not a DTCLab-only
artefact. On pre-CAN vehicles the counts may be unavailable/per-OEM → the field is optional and the
localiser degrades gracefully to the scalar misfire-vs-trim logic in `11`.

Citation: per-cylinder false-lean mechanism + 200/1000-rev counts and the >1 % catalyst boundary per
AddObdFields §Part 2.5; misfire↔trim discriminator per `fuel-trim/11`. Consumer PROPOSAL —
EP-OBD-IN-07 (`fault_atlas` misfire localiser + EP-COM-07 gate); field + consumer ship together.


## Core Entities

- misfire_count, MISFIRE_FALSE_LEAN
- fault_atlas misfire localiser + EP-COM-07 gate (EP-OBD-IN-07 PROPOSAL)

## Graph relations (explicit)

**misfire_count** READ_ALONGSIDE trims as false-lean guard
single-cylinder count escalation INDICATES localised cylinder fault
random-spread counts INDICATES global **FUEL_STARVATION**
**misfire_count** above 1% of events RAISES catalyst-meltdown flag
**misfire_count** EMITTED_BY OBDLab and CONSUMED_BY **fault_atlas misfire localiser**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
