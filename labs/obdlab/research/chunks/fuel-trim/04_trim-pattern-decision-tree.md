---
chunk: fuel-trim/04_trim-pattern-decision-tree
topic: fuel-trim
sources:
  - master_fuel_trim_guide.md §4
  - Research10.md §1 (per-fault-family magnitude/sign confirmation)
consumer: fault-atlas routing — maps the idle-vs-RPM trim pattern to a root-cause family (vacuum leak / fuel delivery / MAF / EVAP / injector / EGR / exhaust leak)
consumer_status: active
consumer_note: >
  The RPM-dependence discriminator (idle vs 2500–3000 RPM, the "Three-Speed Test")
  is a low-idle-vs-stress-idle DELTA. Per SWEEP_MANIFEST §7, delta data is staged
  in chunks/delta-relations/ and its consumer (COMLab delta-calculation script)
  does not exist yet → that portion is PENDING. The static single-point routing
  (this chunk) is active now.
consumer_status_delta: PENDING (COMLab delta script — see SWEEP_MANIFEST FU-2)
dedup: canonical decision tree; supersedes overlapping pattern tables in Short Term Long Term Fuel Trim Explained.md, Ross-Tech_ VAG-COM_ Fuel Trim Info.md, Eastern-Manufacturing.md
---

# Trim-pattern decision tree

The single most diagnostic rule in the fuel-trim domain: the **RPM-dependence**
of the trim discriminates root cause; the absolute values are secondary.

| Pattern | LTFT at idle | LTFT at 2500–3000 RPM | Root cause | Why |
|---|---|---|---|---|
| **Vacuum leak** | High positive (+15 … +25 %) | Drops toward normal | Unmetered air leak post-MAF | At idle the leak is a large % of total airflow; at cruise it is small, so trim normalises |
| **Fuel delivery** | Moderate positive | **Worsens** (more positive) | Weak pump, clogged filter, low pressure | Fuel demand rises with RPM; pump cannot keep up |
| **MAF under-reading (contaminated)** | Positive at idle | Negative under load | Dirty hot-wire MAF | At high airflow, contamination insulates the wire → reads low → ECU enriches |
| **MAF over-reading** | Negative at idle | More negative under load | Faulty MAF, water in airbox | ECU sees inflated airflow → injects excess fuel |
| **Leaking injector** | Negative on **one bank** | Negative persists | Dripping injector on that bank | One-bank only; raw fuel enters regardless of airflow |
| **Stuck-open EVAP purge** | Negative at idle | Normalises at cruise | Purge valve stuck open | At idle vapour is a large % of total fuel; at cruise it dilutes |
| **High fuel pressure** | Negative at idle and cruise | Negative persists | Pinched return line, faulty FPR | Constant excess fuel delivery |
| **Stuck-open EGR** | High positive | Normalises at cruise | EGR valve stuck open | EGR dilution mimics a vacuum leak |
| **Exhaust leak before pre-cat O₂** | Positive (false-lean) | Persists | Manifold gasket, broken weld | False O₂ feedback drives ECU to add fuel |
| **Worn engine (low compression)** | Slight positive, noisy | Slightly positive | Compression loss → leaner effective burn | Trims drift positive but not far |

## Per-family magnitude confirmation (Research10 §1)

- Vacuum leak / unmetered air: STFT low/normal, **LTFT high positive (+15…+25 %)**;
  LTFT absorbs the correction (real example: BMW 330i intake leak → LTFT +24/+25 %,
  STFT ≈ 0 %).
- MAF under-reporting: LTFT high positive (same sign as vacuum leak — RPM behaviour
  separates them, per the table above).
- Fuel delivery: LTFT high positive.
- Rich / over-fuelling (leaking injector, high pressure): **LTFT high negative
  (−10…−25 %)**.
- O₂/AFR sensor biased: moderate positive *or* negative, may be erratic (cross-ref
  `07_trim-vs-gas-chemistry-crosscheck`).

## The Three-Speed Test (RPM-delta discriminator — staged)

Measure trims at idle, 2500 RPM, and 3000 RPM (or under load via decel). The
RPM-dependence is the discriminator. **This is delta data** (low-idle vs
stress-idle) — extracted into `chunks/delta-relations/` and **PENDING** a named
COMLab delta-calculation consumer (SWEEP_MANIFEST §7, FU-2). Routing on the
*static idle pattern* above is active now; routing on the *delta* ships only when
that consumer exists.

Cross-refs: stuck-open EGR mimics vacuum leak (`master_gas_guide.md §3 rule 6`);
worn-engine drift (`master_mechanical_guide.md §6`); single-bank cases →
`05_bank-to-bank-comparison`.

Citation: pattern table per master_fuel_trim_guide.md §4 (synthesised from
Ross-Tech VAG-COM, Short Term Long Term Fuel Trim Explained, Eastern Manufacturing);
per-family magnitudes (+15…+25 % / −10…−25 %, BMW 330i example) per Research10.md §1.


## Core Entities

- VACUUM_LEAK, FUEL_STARVATION, MAF_UNDERREPORT, MAF_OVERREPORT, LEAKING_INJECTOR
- EVAP_PURGE_STUCK_OPEN, HIGH_FUEL_PRESSURE, EGR_STUCK_OPEN, EXHAUST_LEAK_PRECAT, WORN_RINGS
- STFT, LTFT; fault-atlas routing (consumer, active)

## Graph relations (explicit)

**VACUUM_LEAK** RAISES **LTFT** at idle and normalises at RPM
**FUEL_STARVATION** WORSENS **LTFT** at RPM
**MAF_UNDERREPORT** PRODUCES_POSITIVE **LTFT** at idle and negative under load
**LEAKING_INJECTOR** PRODUCES_NEGATIVE single-bank **LTFT**
**EVAP_PURGE_STUCK_OPEN** PRODUCES_NEGATIVE **LTFT** at idle
**EGR_STUCK_OPEN** MIMICS **VACUUM_LEAK**
**EXHAUST_LEAK_PRECAT** PRODUCES false-lean **POSITIVE_TRIM**
**trim-pattern-decision-tree** DISCRIMINATES by RPM-dependence of trim

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
