# Formula wiki — index

**Date:** 2026-06-07 · **Scope:** formulas extracted from the **readable** parts of the
whole `sources/` tree (fuel-trim, o2-logic/catalyst, ecu-diagnosis, taxonomy, pids-protocol)
plus `sources/various/` (Vol1–8) and the already-readable proposal/wiki docs.

## How to read an entry
Each formula card states: **Formula** (ASCII/code block) · **ASCII plot** where it aids
intuition · **Logic** (why it exists) · **Connected case** (a fault it diagnoses) ·
**Lab** (owning module) · **Source**.

## Readability-gate note (important)
The `sources/various/` volume docs are Google-Docs→md exports; **display equations and
inline math symbols were image-stripped in Vol1/2/3/6 and the two Vol7 display formulas**.
Per the CLAUDE.md gate, those are **NOT reconstructed**. Where the same formula survives
in another readable source it is carried here with that source cited; otherwise it is
listed in `PENDING_STRIPPED_FORMULAS.md` for a readable re-export. **No formula in the
cards below is fabricated.**

## Files

| File | Domain | Lab(s) |
|---|---|---|
| `01_gas-chemistry-lambda.md` | Brettschneider λ, stoich, vsum validity, chemical efficiency, oxygen-usage | GASLab |
| `02_fuel-trim.md` | total trim, bank divergence, ΔTrim, OBD-I↔II conversion | OBDLab / COMLab |
| `03_airflow-ve-load.md` | VE, theoretical airflow, sensor-error Δ, calculated/absolute load, MAF rules | OBDLab |
| `04_o2-lambda-translation.md` | wideband Ip→λ, Δλ vector, catalyst OSC ratio, cat field tests | OBDLab / GASLab |
| `05_delta-divergence.md` | δ, cross-delta Δδ, state deltas, two-speed gas deltas | COMLab |
| `PENDING_STRIPPED_FORMULAS.md` | 12 formulas referenced-but-stripped in source exports | — |

## Card index

| ID | Formula | File |
|---|---|---|
| F-GAS-01 | Brettschneider λ | 01 |
| F-GAS-02 | Stoichiometric AFR ↔ λ | 01 |
| F-GAS-03 | vsum + dilution validity | 01 |
| F-GAS-04 | Chemical efficiency CO₂/(CO₂+CO) | 01 |
| F-GAS-05 | Oxygen-usage factor O₂/CO | 01 |
| F-FT-01 | total_trim = STFT+LTFT | 02 |
| F-FT-02 | per-bank trim + B1/B2 divergence | 02 |
| F-FT-03 | ΔTrim low→stress idle | 02 |
| F-FT-04 | OBD-I↔II trim conversion | 02 |
| F-AIR-01 | Volumetric efficiency | 03 |
| F-AIR-02 | Theoretical airflow (speed-density) | 03 |
| F-AIR-03 | Sensor calibration-error delta | 03 |
| F-AIR-04 | Calculated/absolute load | 03 |
| F-AIR-05 | MAF idle/peak rules | 03 |
| F-O2-01 | Wideband Ip sign → λ | 04 |
| F-O2-02 | Lambda-delta vector | 04 |
| F-O2-03 | Catalyst OSC switching ratio | 04 |
| F-O2-04 | Catalyst field-test thresholds | 04 |
| F-DLT-01 | Single-speed divergence δ | 05 |
| F-DLT-02 | Cross-delta Δδ | 05 |
| F-DLT-03 | State deltas (trim/λ/airflow) | 05 |
| F-DLT-04 | Two-speed gas deltas | 05 |

**22 formula cards + 12 pending.**
