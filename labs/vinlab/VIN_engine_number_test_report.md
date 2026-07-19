# VINLab — Engine-number-from-VIN test report

**Date:** 2026-07-07  ·  **Lab:** `labs/vinlab`  ·  **Source:** `docs/Nio_vozila_3.csv`
**Sample:** 200 random VINs, `random.seed(42)`, filtered to petrol (`P13-Vrsta goriva (oznaka) == "P"`), 17-char VIN, non-empty `P15-Oznaka motorja`.
**Population after filter:** 167,778 rows.

## What "engine number" means here
The CSV field `P15-Oznaka motorja` is the engine code. VINLab does **not** expose an
engine number in its public output (`VinDNA`); the code is computed only inside the
decoder by `_resolve_engine`, keyed on brand + VDS = `vin[3:8]` against
`vinlab/data/vds_engine_map.csv` (a frozen lookup table the decoder reads).
This test therefore reads that private method, not the official `decode()` result.

## Results
| Metric | Count |
|---|---|
| `decode()` succeeded | 198 (99.0%) |
| `decode()` rejected (out-of-scope) | 2 (1.0%) |
| Engine code resolved (non-empty) | 199 (99.5%) |
| No engine code resolved | 1 (0.5%) |
| **Exact match to P15** (normalized) | 161 (80.5%) |
| **Near match** (one code contained in other) | 6 (3.0%) |
| Resolved but wrong | 32 (16.0%) |

Exact + near = **167 / 200 = 83.5%** of the sample.
Match rate among *resolved* codes only: exact 161/199, near 6/199.

## Two root causes
**1. Structural — VDS does not encode the engine variant.** `vin[3:8]` maps to at most
one code per brand, so distinct engines sharing a VDS collapse to a single guess:
- `ZFA18800004809939` — P15 `188A5000` → resolved `188A4000`
- `W0L000025T1080979` — P15 `X20SE` → resolved `X20XEV`
- `WVWZZZ9NZ6D040769` — P15 `BME` → resolved `AZQ`
- `VF1B560KE16320202` — P15 `F3PB670` → resolved `F3PB674`
- `WF05XXGCC5HB42474` — P15 `YVDA` → resolved `M1DD`
- `ZFA16900000176572` — P15 `187A1000` → resolved `188A4000`

**2. Data quality — `vds_engine_map.csv` holds corrupted codes.** 0 of the
199 resolved codes in this sample are mojibake or carry junk prefixes
(`TIP`/`TRI`/`TUP`/`UNK-`):

## Conclusion
On held-out data, engine numbers are **not** reliably recovered from VIN by VINLab:
~84% of petrol VINs yield a matching P15 code. The route is limited
by design (VDS granularity) and further degraded by corrupted rows in the frozen
`vds_engine_map.csv`. Fixing the map's mojibake/junk entries would lift the ceiling but
cannot overcome the structural VDS-granularity limit.

## Reproduce
`python3 tools/vin_engine_number_report.py` (petrol filter, seed 42, N=200).
