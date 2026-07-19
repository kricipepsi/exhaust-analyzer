---
chunk: o2-logic/01_sensor-types-and-physics
topic: o2-logic
sources:
  - master_o2_sensor_guide.md §1
  - master_o2_sensor_guide.md §2 (narrowband voltage)
  - master_o2_sensor_guide.md §3 (wideband UEGO)
consumer: OBDLab composition.py — sensor-type mapping to WIDEBAND_LINEAR / NARROWBAND_0_TO_1V (driven by DNALab ObdLabDnaView sensor topology); selects the translation rule that produces normalized_obd_lambda (o2_normalizer.py)
consumer_status: active
dedup: physics primer also appears in O2NBvsWB.md (upstream/downstream scale-vs-anchor framing) — folded here; O2sensorLogic.md dropped as subset of O2NBvsWB.md
---

# O₂ sensor types and physics

Two sensor families, two interpretation rule-sets. The 4D engine reads
`o2_upstream_classification` (narrowband / wideband) from the DNALab
`ObdLabDnaView` sensor topology; `composition.py` maps it to
`WIDEBAND_LINEAR` or `NARROWBAND_0_TO_1V`, which selects the translation
algorithm in `04_normalized-lambda-translation`. Choosing the wrong rule-set
fabricates faults — running narrowband switching/cross-count checks on a
wideband signal triggers a false "lazy/stuck" verdict (see
`03_failure-modes-taxonomy`).

## Narrowband (zirconia, ~1980s–2000s)

A zirconia sensor generates a voltage by comparing exhaust O₂ to ambient air
across its solid electrolyte. It is accurate only near λ = 1.0 (± 0.05) and
behaves as a switch, not a meter.

- Output: 0–1 V switching voltage.
- Stoichiometric centre: **~0.45 V (450 mV)**. Below 0.45 V = lean; above = rich.
- Rich signal: ~0.8–0.9 V (low exhaust O₂). Lean signal: ~0.1–0.2 V (high O₂).
- Healthy upstream switching: ~1–2 Hz at idle, crossing 0.45 V cleanly each
  cycle; **cross-counts ≥ 8 in a 10 s sample at 2500 RPM**; switching frequency
  at 2500 RPM **2–5 Hz (multi-port) / 2–3 Hz (TBI)**. A sensor reading
  **< 0.5 Hz at 2500 RPM is slow regardless of voltage amplitude** — a static
  voltage test alone cannot detect this.
- Wiring: 1–4 wires (signal, ground, +12 V heater, heater ground).

## Wideband (UEGO/AFR, 2000s–present)

A dual-cell sensor: a Nernst sensing cell held at exactly 450 mV by a pump
cell. The ECU varies pump current (Ip), typically −2 mA to +2 mA, to keep the
Nernst cell at setpoint — **that pump current is the diagnostic parameter**,
and it is linear across λ 0.65–1.30+.

- λ = 1.0 (stoich): Ip ≈ 0 mA, reported λ = 1.000.
- Rich (λ < 1.0): negative Ip — ECU pumps O₂ *into* the chamber.
- Lean (λ > 1.0): positive Ip — ECU pumps O₂ *out* of the chamber.
- WOT power enrichment: Ip −0.5 to −1.5 mA, λ 0.85–0.92.
- DFCO (fuel cut, mostly air): Ip +1.5 to +2.0 mA, λ 1.30+.
- Wiring: 5–6 wires (signal, pump current, calibration resistor, reference,
  +12 V heater, heater ground).

**Raw wideband voltage is meaningless without the calibration-resistor value.**
The engine must read the reported λ PID (`obd_lambda`), not raw voltage.

## Heater circuits (both families)

O₂ sensors require ≥ ~350 °C to function; built-in heaters bring them online
within 20–60 s of cold start, enabling earlier closed-loop entry.

- Heater current: 0.5–2.0 A (older NB), up to 8 A (some WB).
- Heater resistance (cold): **4–14 Ω narrowband; 2.5–10 Ω wideband.**
- If closed loop is never reached, suspect heater open or sensor cold-stuck
  (failure mode `HEATER_FAULT`, see `03_failure-modes-taxonomy`).

Citation: SAE J1979 PIDs `$14`–`$1B` (O₂ sensor voltages), `$24`–`$2B`
(wideband sensor data); Bosch Technical Information — LSU 4.2 / 4.9 wideband
datasheet (pump-current calibration).


## Core Entities

- NARROWBAND_0_TO_1V, WIDEBAND_LINEAR, o2_upstream_classification, normalized_obd_lambda, HEATER_FAULT
- composition.py, o2_normalizer.py (consumer, active)

## Graph relations (explicit)

**o2_upstream_classification** MAPS_TO **WIDEBAND_LINEAR** or **NARROWBAND_0_TO_1V**
**composition.py** SELECTS translation rule by sensor type
**WIDEBAND_LINEAR** USES pump-current Ip as diagnostic parameter
**NARROWBAND_0_TO_1V** SWITCHES around 0.45V
heater open or cold-stuck PRODUCES **HEATER_FAULT**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
