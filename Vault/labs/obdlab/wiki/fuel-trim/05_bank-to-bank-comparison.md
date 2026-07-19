---
chunk: fuel-trim/05_bank-to-bank-comparison
topic: fuel-trim
sources:
  - master_fuel_trim_guide.md §5
consumer: T-OBDV2-BANK-ASYM-1 (per-bank STFT/LTFT emit) → COMLab T-COMV2-BANK-FUSE-1 (bank-asymmetry fusion); see CROSS_LAB_DEPENDENCIES DEP-3
consumer_status: active (inherited cross-lab consumer; coder-runnable gated on T-OBDV2-0 = revive)
dedup: canonical bank-comparison rule; no other source carries the opposite-direction harness-swap case
---

# Bank-to-bank comparison (V-engines / inline-six with two pre-cat O₂)

The single most powerful test on engines with two pre-cat O₂ sensors. Compares
per-bank trim (B1 = STFT `$06`/LTFT `$07`, B2 = STFT `$08`/LTFT `$09`).

- **Both banks deviate the same way (within ±5 % of each other):** **common-mode**
  cause — MAF, fuel pump, fuel pressure, EVAP, intake-plenum leak, or an exhaust
  manifold leak feeding both pre-cat O₂ sensors.
- **Only one bank deviates:** **bank-specific** cause — intake-port gasket on that
  bank, a single clogged/leaking injector, single-bank fuel-rail issue, or a
  single-bank O₂ sensor bias.
- **Banks deviate in *opposite* directions:** rare — usually a swapped O₂ harness
  or a single failing wideband. Raise `o2_sensor_swap_suspected` and cross-ref
  `master_o2_sensor_guide.md`.

**Consumer note (signal/noise).** Per-bank trim is the OBD-side emit re-homed from
the void GASLab task T-GV2-14 onto OBDLab T-OBDV2-BANK-ASYM-1. The bank-asymmetry
*verdict* is a COMLab fusion product (T-COMV2-BANK-FUSE-1) built last; OBDLab emits
the two banks' trims under a frozen contract and is never blocked on COMLab. This
chunk is coder-runnable only once the OBDLab scope gate T-OBDV2-0 resolves to
`revive`.

Citation: SAE J1979 per-bank PIDs `$06`/`$07` (B1), `$08`/`$09` (B2);
±5 % bank-match bound per master_fuel_trim_guide.md §5 (consensus practitioner value).


## Core Entities

- STFT, LTFT, per_bank_trim_delta, o2_sensor_swap_suspected
- T-OBDV2-BANK-ASYM-1 (producer), T-COMV2-BANK-FUSE-1 (consumer)

## Graph relations (explicit)

**both-banks-deviating-together** INDICATES common-mode cause
**single-bank-deviating** INDICATES bank-specific cause
**opposite-direction-banks** RAISES **o2_sensor_swap_suspected**
**per_bank_trim_delta** EMITTED_BY **T-OBDV2-BANK-ASYM-1**
**per_bank_trim_delta** CONSUMED_BY **T-COMV2-BANK-FUSE-1**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
