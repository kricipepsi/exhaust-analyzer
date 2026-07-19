---
chunk: o2-logic/02_upstream-vs-downstream-roles
topic: o2-logic
sources:
  - master_o2_sensor_guide.md §4 (upstream vs downstream roles)
  - O2NBvsWB.md §1–2 (sensor configurations; downstream as "anchor"/secondary loop)
consumer: DownstreamTrimRole {NONE, CATALYST_MONITOR_ONLY, SECONDARY_FUEL_TRIM} — COMLab vocabulary.py / VINLab models.py, constructed in composition.py; read by COMLab perception-contradiction detector to qualify O2-health verdicts
consumer_status: active
dedup: O2sensorLogic.md (subset of O2NBvsWB.md) dropped; downstream-role detail extends here, suppression logic lives in 06_downstream-trim-suppression
related: [[06_downstream-trim-suppression]]
---

# Upstream vs downstream — different roles, different rules

Sensor *position* in the exhaust changes its job and the rules that apply to
its signal. Position is described as bank/sensor: B1S1 = Bank 1, pre-cat;
B1S2 = Bank 1, post-cat; likewise B2S1 / B2S2.

| Position | Role | Expected behaviour | Drives |
|---|---|---|---|
| **S1 (pre-cat)** | Fuel-control feedback | Rapid switching (NB) or live λ (WB) | STFT/LTFT |
| **S2 (post-cat)** | Catalyst-efficiency monitor | Slow, mostly stable ~0.5–0.7 V | P0420/P0430 monitor; trim only if the platform supports a rear loop |

## The hard rule

**A failing post-cat sensor does not affect fuel trim** on platforms where the
rear sensor is monitor-only. If the operator sees fuel-trim drift with only a
rear-sensor DTC (P0136/P0156), the rear sensor is *not* the cause of the drift
— keep looking. This rule is why the engine must know the downstream sensor's
role before attributing trim faults.

## Downstream role drives the consumer enum

Whether the rear sensor has trim authority is a per-vehicle fact supplied by
DNALab/VINLab and carried as `DownstreamTrimRole`:

- `NONE` — no downstream sensor, or role not assigned.
- `CATALYST_MONITOR_ONLY` — rear sensor only watches catalyst efficiency; has
  **no authority** to adjust fuel trim. Most pre-2005 petrol platforms.
- `SECONDARY_FUEL_TRIM` — rear sensor actively biases the upstream target (a
  secondary correction loop). Newer platforms; the rear loop can mask upstream
  drift, so an in-tolerance λ-agreement is *weak* evidence of a healthy
  upstream sensor (consumed by the perception-contradiction detector — see
  `05_bias-vs-real-truth-perception`).

The downstream secondary loop, when present, works as a guard: because the
catalyst stores oxygen the post-cat gas is stable, so the ECU uses the steady
downstream reading (target ~0.65–0.75 V) to detect upstream drift and bias the
main fuel calculation back to centre. How that role gates COMLab's post-cat
trim analytics is in `06_downstream-trim-suppression`.

Citation: SAE J1979 rear-sensor PIDs (B1S2/B2S2); narrowband post-cat target
0.5–0.7 V steady (master_o2_sensor_guide.md §4). Enum source:
O2_MODEL_STRATEGY.md §3 (mirrored in COMLab vocabulary.py / VINLab models.py).


## Core Entities

- DownstreamTrimRole.NONE, DownstreamTrimRole.CATALYST_MONITOR_ONLY, DownstreamTrimRole.SECONDARY_FUEL_TRIM
- B1S1, B1S2, STFT, LTFT, P0420
- composition.py / COMLab perception-contradiction detector (consumer, active)

## Graph relations (explicit)

**S1-pre-cat** DRIVES **STFT** and **LTFT**
**S2-post-cat** MONITORS catalyst efficiency (**P0420**)
**DownstreamTrimRole.CATALYST_MONITOR_ONLY** HAS_NO trim authority
**DownstreamTrimRole.SECONDARY_FUEL_TRIM** CAN_MASK upstream drift
**DownstreamTrimRole** SUPPLIED_BY DNALab/VINLab
**DownstreamTrimRole.SECONDARY_FUEL_TRIM** CONSUMED_BY **perception-contradiction detector**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
