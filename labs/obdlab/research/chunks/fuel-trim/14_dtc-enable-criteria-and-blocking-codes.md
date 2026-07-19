---
chunk: fuel-trim/14_dtc-enable-criteria-and-blocking-codes
topic: fuel-trim
sources:
  - Fuel Trim Diagnostics.txt §"DTC P0171/P0174 run conditions" + §"DTC's not to be present"
  - FuelTrimFamilies.md §"control theory" (±20–25% adaptive limit, WOT lock)
consumer: obdlab/obdlab/core/analytics_preconditions.py + TrimAnalyticsGate (ENGINE_COLD/OPEN_LOOP/WOT_ACTIVE/DFCO_ACTIVE/CODES_RECENTLY_CLEARED) — the live trim-validity gate. The numeric P0171/4 enable envelope sharpens those gates. The "blocking-codes-clear-first" precondition is a forward-progress PROPOSAL (a prerequisite-DTC gate) — register in comlab/config/proposals/.
consumer_status: MIXED (active precondition gate + 1 proposal)
provenance: sources/fuel-trim/Fuel Trim Diagnostics.txt + FuelTrimFamilies.md
related: [[08_validity-preconditions]], [[06_trim-rails-and-sentinels]], [[03_normal-ranges-and-dtc-thresholds]]
---

# DTC enable-criteria envelope + blocking-codes (extends validity, chunk 08)

Chunk 08 lists *which* preconditions gate trim. This chunk pins the **numeric
envelope** a real PCM requires before it even evaluates a lean code, and adds the
**prerequisite-codes** rule.

## P0171/P0174 run-condition envelope (GMH VT Gen III, representative)

All must hold continuously for ~6 s, AND average LTFT cells above threshold,
before the lean code sets:

| Parameter | Window |
|---|---|
| Engine coolant temp | 50–115 °C |
| Barometric pressure | > 74 kPa |
| Mass air flow | 5–90 g/s |
| Manifold pressure | 26–90 kPa |
| Intake air temp | −20 … 90 °C |
| Engine RPM | 400–3000 |
| TPS angle | < 90 % |
| Vehicle speed | < 137 km/h |

Outside this envelope the PCM does not judge trims — so the 4D engine should not
either. This maps directly onto `analytics_preconditions` / `TrimAnalyticsGate`:
out-of-window → gate the trim findings (ENGINE_COLD, WOT_ACTIVE, etc.). The
envelope gives concrete bounds to pin rather than invent.

## WOT / power-enrichment lock

Under WOT the PCM **suspends closed loop and locks STFT at 0 %** to keep learned
trims from lean-skewing enrichment. Live `TrimAnalyticsGate.WOT_ACTIVE` already
covers this; the source confirms the threshold behaviour and that LTFT is frozen,
not zeroed, during WOT.

## Blocking-codes-clear-first (PROPOSAL)

A real PCM will **not** run the P0171/4 monitor if certain upstream codes are
present, and a technician must clear those first: P0101/2/3 (MAF), P0107/8 (MAP),
P0112/3/7/8 (IAT/ECT), P0121/2/3 (TPS), P0335/6 (CKP), P0351–0358 (coils),
P1111/2, P1258. Diagnostic rule: **if any sensor/ignition prerequisite DTC is
active, do not route on lean/rich trim — resolve the prerequisite first** (those
faults corrupt the very inputs trim is computed from).

No live precondition encodes a *prerequisite-DTC* gate today (the gates are
condition-based, not code-dependency-based). Propose `prerequisite_dtc_gate`:
consumer = `analytics_preconditions` reading `dtc_lab_output` active codes and
suppressing trim routing when a listed prerequisite is active. Register in
`comlab/config/proposals/`. This is forward progress — it kills a whole class of
mis-routes where a bad MAF/ECT makes trims lie.

Citation: Fuel Trim Diagnostics.txt P0171/4 run conditions (ECT 50–115 °C, baro
>74 kPa, MAF 5–90 g/s, MAP 26–90 kPa, IAT −20…90 °C, RPM 400–3000, TPS <90 %, VSS
<137 km/h, 6 s + avg-LTFT-threshold) and the prerequisite-DTC list; FuelTrimFamilies.md
WOT STFT-lock and ±20–25 % adaptive limit.


## Core Entities

- P0171, P0174, TrimAnalyticsGate.ENGINE_COLD, TrimAnalyticsGate.WOT_ACTIVE
- prerequisite_dtc_gate (PROPOSAL), dtc_lab_output
- analytics_preconditions (consumer, active)

## Graph relations (explicit)

**P0171** and **P0174** monitor REQUIRES run-condition envelope (ECT 50-115C, MAF 5-90 g/s)
out-of-envelope GATES trim via **TrimAnalyticsGate.ENGINE_COLD** and **TrimAnalyticsGate.WOT_ACTIVE**
**TrimAnalyticsGate.WOT_ACTIVE** LOCKS **STFT** at 0%
**prerequisite_dtc_gate** SUPPRESSES trim routing when MAF/MAP/IAT/ECT/TPS/CKP/coil DTC active
**prerequisite_dtc_gate** READS **dtc_lab_output**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
