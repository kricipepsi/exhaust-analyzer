---
chunk: fuel-trim/01_stft-ltft-fundamentals
topic: fuel-trim
sources:
  - master_fuel_trim_guide.md §1
consumer: COMLab trim analytics — total-trim (STFT+LTFT) symptom generation feeding fault-atlas Air-&-Fuel-Metering routing (P0171/P0172/P0174/P0175)
consumer_status: active
dedup: supersedes the STFT/LTFT primer in fuel-trim.md, fuel-trim-analysis.md, "What are fuel trims all about.md"
---

# STFT / LTFT fundamentals

Fuel trim is the ECU's percentage adjustment to the base injector pulse width,
compensating for deviations from the stoichiometric 14.7:1 AFR target. It is the
ECU *learning* that the physical fuel-air system does not match its base map.

- **STFT — Short-Term Fuel Trim.** Moment-to-moment correction from the upstream
  O₂ sensor feedback. Reacts in milliseconds; oscillates rapidly positive/negative
  as the ECU fine-tunes around stoichiometric. Analogy: *acceleration*.
- **LTFT — Long-Term Fuel Trim.** Learned, averaged correction stored in
  non-volatile memory. Represents how far the fuel system deviates from base-map
  over time. Analogy: *speed*. Persistent STFT corrections transfer gradually
  into LTFT.

**Combination rule (the value the engine evaluates):**

```
total_trim = STFT + LTFT
```

The 4D engine evaluates **total trim**, not STFT or LTFT in isolation. This is
the quantity the decision tree (`04_trim-pattern-decision-tree`) and the
DTC-threshold logic (`03_normal-ranges-and-dtc-thresholds`) consume.

**Why both are needed.** STFT alone shows the instantaneous correction but hides
a settled bias the ECU has already absorbed into LTFT; LTFT alone hides whether
the system is still actively chasing. A vacuum leak, for example, can present as
STFT ≈ 0 % with LTFT +24 % once the long-term correction has fully absorbed the
offset (see `04_trim-pattern-decision-tree`). Reading total trim avoids that
masking.

Citation: SAE J1979 PIDs `$06` (STFT B1), `$07` (LTFT B1), `$08` (STFT B2),
`$09` (LTFT B2).


## Core Entities

- STFT, LTFT, TOTAL_TRIM
- P0171, P0172, P0174, P0175
- COMLab trim analytics (consumer, active)

## Graph relations (explicit)

**TOTAL_TRIM** EQUALS **STFT** plus **LTFT**
**STFT** TRANSFERS_INTO **LTFT** over time
**TOTAL_TRIM** CONSUMED_BY **COMLab trim analytics**
**TOTAL_TRIM** ROUTES_TO **P0171**, **P0172**, **P0174**, **P0175**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
