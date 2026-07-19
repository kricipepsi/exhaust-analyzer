# V3_C9_SYNTH_BANDS_2026-07-06

**Task:** `T-V3-P4-C9-SYNTH`  **Mode:** provisional-synthetic seed (side file)
**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, tolerance-wide, web-corroborated, `synthetic=true`, correctable.
**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** `/agent_workspace/.venv-wired/bin/python v3/gen_c9_synth_seed.py`.
**Data + manifest:** `v3/data/c9_synthetic_seed_2026-07-06.{csv,json}`.
**Baseline pin (from C9-PRE):** `V3_YARDSTICK_2026-07-06-C5B` (csv `c49c17af…`, oracle `3088a7c3…`), run `POST_T_V3_P4_C5B`.

Seeds the 11 C9 cases' health confirmation and emissions columns (`readiness_supported_complete_bool, stored_dtc_count, pending_dtc_count, permanent_dtc_count, mode06_min_margin_pct, warmup_cycles_since_clear, miles_since_clear, stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, gas_delta_hc_ppm, gas_delta_co_pct, gas_delta_co2_pct, gas_delta_o2_pct`) with values derived from each case's **oracle fault code** through the `cluster9.1.md` / `value9.md` signature, each band widened to the real-world spread found via web research. Consumed by `T-V3-P4-C9A` (dry-run).

## 1. No-back-solve statement

C9 cases are split by `expected_fault_family`: `no_fault` (10 cases) and `misfire` (1 case). The band group is keyed on the finer **`expected_fault_code`** — the corpus **answer key** — resolved to `OPTIMAL_HEALTH` or `ERR-MF-008`. The generator's **only** inputs are (a) each case's `expected_fault_code` and (b) the band table below. It does **not** read `no_fault.json` consumer thresholds, nor any case's current rank or predicted family. The gates used to *verify* the seed are the **research/producer** bands from `cluster9.1.md` / `value9.md`, not consumer rules. Floats are sampled uniformly across a tolerance-wide band (σ reported), seeded deterministically per `case_id` (SHA-256; no wall-clock randomness).

## 2. Per-column bands — cluster9 research vs web-real vs band used

| Column / signal | cluster9 producer threshold | Web-real range (cited) | Band used (tolerance-wide) | Grounding |
| --- | --- | --- | --- | --- |
| `readiness_supported_complete_bool` | all non-continuous = COMPLETE | complete monitors | **True** (healthy) / **True** (misfire) | **standardized** |
| `stored/pending/permanent_dtc_count` | all DTC counts = 0 | no codes present | healthy: **0**; misfire: `pending` = **1** | **standardized** |
| `mode06_min_margin_pct` | margin `>= 10%` | margin 15-95% of limit range | healthy: **[15.0, 95.0]%**; misfire: **[1.0, 5.0]%** | **standardized** |
| `warmup_cycles_since_clear` | cycles `>= 5` | typical reset maturity | healthy: **[5, 40]** cycles | **standardized** |
| `miles_since_clear` | distance `>= 200` miles | typical reset maturity | healthy: **[200, 800]** miles | **standardized** |
| `stft_idle_pct` | STFT within `+/-5%` | normal idle STFT | healthy: **[-4.0, 4.0]%**; misfire: **[6.0, 12.0]%** | **standardized** |
| `ltft_idle_pct` | LTFT within `+/-7%` | normal idle LTFT | healthy: **[-6.0, 6.0]%**; misfire: **[8.0, 15.0]%** | **standardized** |
| `stft_2500_pct` | STFT within `+/-5%` | normal 2500 STFT | healthy: **[-4.0, 4.0]%**; misfire: **[2.0, 6.0]%** | **standardized** |
| `ltft_2500_pct` | LTFT within `+/-7%` | normal 2500 LTFT | healthy: **[-6.0, 6.0]%**; misfire: **[4.0, 8.0]%** | **standardized** |
| `gas_delta_hc_ppm` | delta HC `-10` to `+15` ppm | combustion delta | healthy: **[-10, 15]** ppm; misfire: **[25, 60]** ppm | **anecdotal** |
| `gas_delta_co_pct` | delta CO `-0.15` to `+0.15` % | combustion delta | healthy: **[-0.150, 0.150]%**; misfire: **[0.200, 0.500]%** | **anecdotal** |
| `gas_delta_co2_pct` | delta CO2 `+0.3` to `+0.8` % | combustion delta | healthy: **[0.30, 0.80]%**; misfire: **[-1.50, -0.50]%** | **anecdotal** |
| `gas_delta_o2_pct` | delta O2 `-0.5` to `+0.4` % | combustion delta | healthy: **[-0.50, 0.40]%**; misfire: **[0.50, 1.50]%** | **anecdotal** |

Where the web shows a **wider or typical** range, the band is set to fire the producer gate robustly while staying field-realistic (policy step 3).

### Citations

- **obd_readiness_completeness** — All supported readiness monitors must complete to verify emission-control functionality before confirming health. California BAR OBD Test Reference; CARB/EPA regulations. Corroborated: https://www.bar.ca.gov/pdf/obd_test_reference.pdf
- **obd_dtc_count** — Stored, pending, and permanent DTCs must all be zero to exclude active or intermittent faults. SAE J1979 / CARB regulations. Corroborated: https://www.bar.ca.gov/pdf/obd_test_reference.pdf
- **mode06_margin** — Mode $06 monitor margins >= 10% ensures the emission systems are operating comfortably inside limits, not on the edge of failure. value9.md §1; SAE J1979. Corroborated: https://www.arb.ca.gov/regact/2015/obdii2015/finalregorder2.pdf
- **obd_reset_age** — Warm-up cycles since clear >= 5 and distance >= 200 miles prevent the fresh-reset blind spot where DTCs are cleared but monitors haven't run. CARB/EPA. Corroborated: https://www.bar.ca.gov/pdf/obd_test_reference.pdf
- **fuel_trims** — Healthy vehicles operate with trims within +/-5% (STFT) and +/-7% (LTFT), with minimal shift (<=5%) between idle and 2500 RPM. value9.md §1; SAE J1979. Corroborated: https://thegrouptrainingacademy.com/fuel-trim-diagnosis-o2-sensor-performance/
- **five_gas_deltas** — Two-speed idle-to-RPM gas deltas (HC, CO, CO2, O2) stay within tight combustion limits (e.g. ΔCO2 positive, ΔHC near 0) indicating stable, efficient combustion. value9.md §1; EPA/BAR. Corroborated: https://www.motor.com/magazine-summary/service-tips-for-gdi-engines/

## 3. Tolerance width (σ) — fires/clears across the WHOLE spread, not a knife-edge

Reported σ per band (uniform std-dev = (hi−lo)/√12):

| oracle code | band_id | separable | margin σ | warmup σ | miles σ | idle STFT/LTFT σ | 2500 STFT/LTFT σ | HC σ | CO σ | CO2 σ | O2 σ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OPTIMAL_HEALTH | C9-HEALTHY | yes | 23.094 | 10.104 | 173.205 | 2.309/3.464 | 2.309/3.464 | 7.217 | 0.087 | 0.144 | 0.26 |
| ERR-MF-008 | C9-MISFIRE-LOOKALIKE | **NO** | 1.155 | 10.104 | 173.205 | 1.732/2.021 | 1.155/1.155 | 10.104 | 0.087 | 0.289 | 0.289 |

## 4. Seeded cases (11/11) — value sits in its own oracle-code band

| case_id | oracle code | fault_name | band | sep | readiness | DTC (st/pe/pm) | margin | wuc | miles | STFT/LTFT idle | STFT/LTFT 2500 | ΔHC | ΔCO | ΔCO2 | ΔO2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CSV-127 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 93.2% | 26 | 636 | 0.4/-5.8% | -0.8/-2.0% | 9 ppm | 0.066% | 0.34% | 0.31% |
| CSV-128 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 65.4% | 8 | 660 | -0.8/-0.3% | -3.5/-0.5% | 5 ppm | -0.081% | 0.38% | -0.2% |
| EXT-216 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 58.1% | 25 | 568 | -0.7/3.9% | -1.0/-0.4% | 6 ppm | -0.138% | 0.8% | -0.41% |
| PDF-HI-005 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 76.1% | 21 | 722 | -2.8/1.9% | 0.5/-5.0% | 9 ppm | -0.112% | 0.57% | -0.45% |
| PDF-HI-010 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 67.4% | 12 | 234 | 3.9/-4.2% | -0.1/4.4% | -5 ppm | 0.018% | 0.63% | 0.2% |
| YAML-PDF_HI_005 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 82.6% | 9 | 609 | 3.9/0.1% | -2.0/1.8% | 8 ppm | -0.029% | 0.31% | 0.23% |
| YAML-PDF_HI_010 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 84.7% | 11 | 681 | -3.5/-5.9% | -3.6/-5.4% | -2 ppm | 0.08% | 0.54% | -0.05% |
| YAML-TC1 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 29.0% | 25 | 714 | 3.8/1.6% | -1.4/4.9% | -3 ppm | -0.032% | 0.63% | 0.18% |
| case_014 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 72.9% | 36 | 696 | -2.8/0.7% | 3.4/-4.4% | -9 ppm | -0.051% | 0.44% | -0.28% |
| era2_016 | ERR-MF-008 | misfire_lookalike | C9-MISFIRE-LOOKALIKE | abst | True | 0/1/0 | 1.9% | 28 | 282 | 8.5/11.5% | 3.5/6.1% | 40 ppm | 0.495% | -0.81% | 0.77% |
| era3_014 | OPTIMAL_HEALTH | no_fault | C9-HEALTHY | Y | True | 0/0/0 | 91.8% | 13 | 737 | -1.5/-6.0% | 0.2/-5.7% | 2 ppm | 0.144% | 0.72% | -0.18% |

## 5. Separability split — which cases the C9 signal can and cannot separate

Across the 11 C9 cases, we have a clear **10 separable vs 1 stay-abstained** split:

- **C9-Separable (10 cases):** `CSV-127, CSV-128, EXT-216, PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_014, era3_014`. These are genuine no_fault cases that pass all OBD and combustion metrics. They will successfully confirm health on paper.
- **Stay-Abstained (1 case):** `era2_016`. This is the crankshaft position sensor sync drop fault (expected misfire, currently winning no_fault). It is seeded with misfire-consistent values that fail multiple OBD and combustion checks (e.g. pending DTC, low Mode $06 margin, elevated trims and gas deltas). It will fail the health confirmation gate and return `SENSOR_HEALTH_UNPROVEN_ABSTAIN` to prevent false-healthy diagnostic leakage.

## 6. Collision checks verification

All C9 rows have C5-only columns (`calc_load_wot_pct`, `fuel_rail_pressure_load_kpa`, `wideband_lambda_wot`) and C6-only columns (`mode06_o2_response_margin_pct`, `o2_rich_to_lean_ms`, `o2_lean_to_rich_ms`, `maf_actual_calc_delta_pct_idle`, `maf_actual_calc_delta_pct_2500`) left as absent. This ensures that C9 does not interfere with the active states of C5/C6.

## 7. Paper-separability caveat

While these 10 healthy cases pass all confirmation criteria on paper, their actual top3_family movement depends on the C9A dry-run and C9B commit. Paper-separability represents the logical limit, whereas active simulation and scoring will evaluate the live effect of the boosts and prunes.
