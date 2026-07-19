---
chunk: delta-relations/01_delta-method-and-formula
topic: delta-relations
sources:
  - FuelTrimW.md — "Dynamic Delta Analysis (ΔTrim): Low Idle vs. Stress Idle"
consumer: PENDING (COMLab delta-calculation script — SWEEP_MANIFEST FU-2). Until that script exists and reads ΔTrim in a live code path, this chunk is staging only.
consumer_status: PENDING
provenance: sources/fuel-trim/FuelTrimW.md (readable copy of the "Fuel Trim Diagnostics Wiki Preparation" HTML report; Gemini share https://gemini.google.com/share/23ff406a7345)
dedup: complements fuel-trim/04_trim-pattern-decision-tree (static idle pattern at 2500–3000 RPM); THIS defines the quantified ΔTrim at the 3500–4500 RPM stress band
---

# Delta method and formula

The primary diagnostic value of fuel trims (1990–2010 petrol) is the **difference**
between trims at two engine speeds, not the value at one speed.

## Idle bands

- **Low idle:** 600–800 RPM, zero external load.
- **Stress idle:** steady-state throttle hold at 3500–4500 RPM, park/neutral.

## Formulas

```
Total Trim = STFT + LTFT
ΔTrim      = Total Trim(stress idle) − Total Trim(low idle)
```

## Read axis

The discriminating question is whether trim **improves** or **worsens** under load:

- ΔTrim toward 0 / negative (trim improves as RPM rises) → leak-type faults that
  dilute out at higher airflow (vacuum leak; see `02_profile-vacuum-leak`).
- ΔTrim positive (trim worsens as RPM rises) → supply/metering faults that scale
  with demand (fuel starvation `03`, MAF under-report `04`).
- ΔTrim strongly negative with a rich shift → flow-restriction faults
  (exhaust backpressure `05`).

**Consumer note (signal/noise).** ΔTrim has **no live consumer yet**. The named
consumer is the proposed COMLab delta-calculation script (FU-2); per
SWEEP_MANIFEST §7 every delta field stays `PENDING` until that script reads it in
a code path. This chunk preserves the formula + bands so the script can be specced
against ground-truth, but nothing here ships into the engine until FU-2 closes.

Citation: ΔTrim formula, Total Trim = STFT+LTFT, and idle bands (600–800 /
3500–4500 RPM) per FuelTrimW.md ("Dynamic Delta Analysis").


## Core Entities

- DELTA_TRIM, TOTAL_TRIM, STFT, LTFT
- LOW_IDLE, STRESS_IDLE
- VACUUM_LEAK, FUEL_STARVATION, MAF_UNDERREPORT, EXHAUST_BACKPRESSURE
- COMLab delta-calculation script (consumer, PENDING FU-2)

## Graph relations (explicit)

**TOTAL_TRIM** EQUALS **STFT** plus **LTFT**
**DELTA_TRIM** EQUALS **TOTAL_TRIM** at **STRESS_IDLE** minus **TOTAL_TRIM** at **LOW_IDLE**
**VACUUM_LEAK** PRODUCES_NEGATIVE **DELTA_TRIM**
**FUEL_STARVATION** PRODUCES_POSITIVE **DELTA_TRIM**
**MAF_UNDERREPORT** PRODUCES_POSITIVE **DELTA_TRIM**
**EXHAUST_BACKPRESSURE** PRODUCES_NEGATIVE **DELTA_TRIM**
**DELTA_TRIM** CONSUMED_BY **COMLab delta-calculation script**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
