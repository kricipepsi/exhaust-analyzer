---
chunk: ecu-diagnosis/05_sensor-ground-trace-open
topic: ecu-diagnosis
sources:
  - EcuSignatures.md §"4. Vaporized/Blown Internal Sensor Ground Trace (Reference Ground Open)"
consumer: PROPOSAL — consumer = COMLab ECU-hardware-fault checker (proposals/OBD_ImplProp.md, ECU-FU-1); register in comlab/config/proposals/. New v2 fault refining ecu_fault.json ERR-EF-006 (sensor-ground/5V-ref → lean-bias). Ships with TWO companion proposals (not blockers): new TPS + IAT input fields on OBDLivePayload (ECU-FU-3) that the checker reads — TPS=100 % and IAT=−40 °C carry this signature and neither field exists today (only coolant_temp_c/ECT). Per the v2 rule the fields + their consumer ship together as proposals, not deferred.
consumer_status: PROPOSAL (+ companion field proposals: TPS, IAT — ECU-FU-3)
provenance: sources/ecu-diagnosis/EcuSignatures.md
related: [[01_method-load-pct-and-idle-bands]], [[07_comparative-signature-tables]]
---

# Failure mode 4 — vaporized sensor ground trace (reference ground open)

A thin internal trace supplies the clean 0 V reference ground for ratiometric
sensors (ECT, IAT, TPS, MAP). If a high-current circuit (e.g. a shorted O₂-heater
12 V wire) contacts a sensor ground during service, the excess current vaporises
the trace. The sensor ground side then **floats up to 1.5–4.5 V**.

This is the **all-banks symmetric, locked-sensor** fault — the strongest
"internal ECU" tell in the document.

## Low idle (700–800 RPM)

Floating ground corrupts every ratiometric sensor at once:

- ECT and IAT thermistors read max resistance → **locked −40 °C** (extreme cold).
  *(ECT maps to live `coolant_temp_c`, range −40…140; IAT has no live field.)*
- TPS pin floats to max → OBD reports **100 % WOT** though throttle is closed.
  *(No live TPS field.)*
- False −40 °C + false 100 % WOT → ECU forces **max cold-start + acceleration
  enrichment** → massive over-fuel.
- Fuel status locks **open-loop (OL_FAULT)** → STFT/LTFT B1/B2 freeze 0 %; if it
  tries closed loop, trims peg **−25 %** but are overridden by enrichment maps.
- Physical: opaque black exhaust — CO 9.5 %, CO₂ 6.5 %, HC ≈ 1200 ppm, λ_chem ≈ 0.720.
- Both O₂ sensors lock high **> 0.9 V**.
- `calculated_engine_load_pct` spikes to a deceptive **80–90 %** (from high TPS+MAP).

## Stress idle (3500–4500 RPM)

Revving is hard (bogs, backfires). If reached: ECT/IAT stay **−40 °C**, TPS stays
**100 %**, `calculated_engine_load_pct` **pegs 100 %** (anomalous for a parked
vehicle). CO 8.8 %, HC 1400, λ_chem ≈ 0.740. O₂ sensors locked > 0.9 V,
unresponsive to RPM.

## Discriminator

The unmistakable combo: **−40 °C ECT + 100 % TPS + 100 % LOAD_PCT on a parked,
warmed engine**, all banks, frozen trims, severe rich tailpipe. The "all
ratiometric sensors locked together" pattern is what separates an internal ground
failure from a single external sensor fault (see chunk 07, symmetric-vs-asymmetric).

**Blocking gap:** two of the three locked signals (TPS, IAT) are not in the
payload, and `calculated_engine_load_pct = 100 %` at idle would be rejected/ignored
as implausible rather than read as a fault flag. Capturing this mode needs new
input fields — only added if the proposed checker names them as consumers.

Citation: EcuSignatures.md failure mode 4, both idle bands; Table 1 row 4, Table
2 row 4 (chunk 07). coolant_temp_c range OBDLab_KG_Wiki §3.1.


## Core Entities

- SENSOR_GROUND_TRACE_OPEN, ECT, IAT, TPS, LOAD_PCT
- TrimAnalyticsGate.OPEN_LOOP (OL_FAULT), ERR-EF-006
- ECU_HARDWARE_CHECKER (proposed consumer, ECU-FU-1); TPS/IAT fields (ECU-FU-3)

## Graph relations (explicit)

**SENSOR_GROUND_TRACE_OPEN** LOCKS **ECT** at -40C
**SENSOR_GROUND_TRACE_OPEN** LOCKS **TPS** at 100%
**SENSOR_GROUND_TRACE_OPEN** SPIKES **LOAD_PCT** to 80-100%
**SENSOR_GROUND_TRACE_OPEN** REQUIRES **TPS** and **IAT** input fields
**SENSOR_GROUND_TRACE_OPEN** REFINES **ERR-EF-006**
**SENSOR_GROUND_TRACE_OPEN** CONSUMED_BY **ECU_HARDWARE_CHECKER**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
