# V3_C5_SYNTH_BANDS_2026-07-06

**Task:** `T-V3-P4-C5-SYNTH`  **Mode:** provisional-synthetic seed (side file)
**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, tolerance-wide, web-corroborated, `synthetic=true`, correctable.
**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** `/agent_workspace/.venv-wired/bin/python v3/gen_c5_synth_seed.py`.
**Data + manifest:** `v3/data/c5_synthetic_seed_2026-07-06.{csv,json}`.
**Baseline pin (from C5-PRE):** `V3_YARDSTICK_2026-07-05-C6B` (csv `bf739368…`, oracle `3088a7c3…`), run `POST_T_V3_P4_C6B`.

Seeds the 10 C5 cases' lean-condition and airflow columns (`stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, stft_load_pct, ltft_load_pct, calc_load_wot_pct, maf_gps_idle, maf_gps_2500, fuel_rail_pressure_load_kpa, wideband_lambda_wot`) with values derived from each case's **oracle fault code** through the `cluster5.md` signature, each band widened to the real-world spread found via web research. Consumed by `T-V3-P4-C5A` (dry-run) and `C5B` (commit).

## 1. No-back-solve statement

All 10 C5 cases share `expected_fault_family = lean_condition`, so the band group is keyed on the finer **`expected_fault_code`** — the corpus **answer key** — resolved to a registry `fault_name`. The generator's **only** inputs are (a) each case's `expected_fault_code` and (b) the band table below. It does **not** read `lean_condition.json` / `vacuum_leak.json` consumer thresholds, nor any case's current rank or predicted family. The TFT>=15% idle, TFT recovery>=15%, pressure drop>35 kPa, load<80% and lambda>1.05 limits used to *verify* the seed are the **research/producer** bands from `cluster5.md`, not consumer rules. Floats are sampled uniformly across a tolerance-wide band (σ reported), seeded deterministically per `case_id` (SHA-256; no wall-clock randomness).

## 2. Per-column bands — cluster5 research vs web-real vs band used

| Column / signal | cluster5 producer threshold | Web-real range (cited) | Band used (tolerance-wide) | Grounding |
| --- | --- | --- | --- | --- |
| `stft/ltft_idle_pct` | Total idle trim (TFT) `>= 15%` | Idle vacuum leak TFT elevated | idle: STFT ∈ **[5.0, 10.0]%**, LTFT ∈ **[15.0, 20.0]%** | **empirical** |
| `stft/ltft_2500_pct` | Recovery delta `>= 15%` | trims recover at 2500 to normal | 2500: STFT ∈ **[-3.0, 2.0]%**, LTFT ∈ **[0.0, 3.0]%** | **empirical** |
| `calc_load_wot_pct` | Peak WOT load `< 80%` | normal load 90-100%; contaminated MAF < 85% | normal ∈ **[85.0, 95.0]%**; MAF underread ∈ **[62.0, 75.0]%** | **manufacturer-typical / empirical-inferred** |
| `fuel_rail_pressure_load_kpa` | drop `> 35 kPa` below spec | normal port 3.2-3.8 bar; starvation drops pressure | normal ∈ **[320.0, 380.0] kPa**; DI ∈ **[150.0, 250.0] bar** | **manufacturer-typical** |
| `wideband_lambda_wot` | WOT lambda `> 1.05` | normal PE lambda ~0.85; lean starvation > 1.05 | normal ∈ **[0.820, 0.880]**; lean ∈ **[1.060, 1.150]** | **standardized** |

Where the web shows a **wider or typical** range, the band is set to fire the producer gate robustly while staying field-realistic (policy step 3).

### Citations

- **vacuum_leak_trim_recovery** — Comparing fuel trims at idle vs 2500 RPM is a standard diagnostic technique. Unmetered air represents a large percentage of total air at idle (low volume), raising trims (TFT >= 15%). At higher RPM, total air volume increases, reducing the unmetered air percentage, so trims recover to normal (TFT drops toward 0%). Under-reported MAF or fuel delivery faults remain high or worsen at 2500 RPM. [empirical/practitioner] motor.com; gearsmagazine.com. Corroborated: https://thegrouptrainingacademy.com/fuel-trim-diagnosis-o2-sensor-performance/
- **egr_stuck_open_idle_trims** — An EGR valve stuck open at idle recirculates inert exhaust gas, diluting the intake charge. This causes combustion instability/rough idle/misfires without introducing excess unmetered oxygen. The O2 sensor does not read a classic lean mixture at idle so trims do not swing highly positive; they stay normal or negative (false rich) unless severe misfires dump unburned oxygen. [empirical/field] scannerdanner.com; s2ki.com; mri-auto-diagnostics.com. Corroborated: https://scannerdanner.com
- **wot_calculated_engine_load** — Calculated Engine Load PID 04 represents current airflow relative to peak. Under WOT, Calculated Load should reach 90-100%. If Calculated Load is low (e.g. < 80%) at WOT while fuel trims are positive, it indicates a contaminated MAF sensor under-reporting air mass, causing the PCM to under-fuel. [manufacturer-typical] gearsmagazine.com; ls1tech.com. Corroborated: https://gearsmagazine.com/magazine/mass-air-flow-misconceptions/
- **wot_fuel_pressure_drop** — Fuel rail pressure drop under demand (WOT) indicates a physical fuel supply restriction. A drop of > 35 kPa (5 psi) below OEM specifications (normally 320-380 kPa for port injection, GDI operates higher at 150-200 bar) causes fuel starvation and a lean mixture at high RPM. [manufacturer-typical] motor.com; hpacademy.com. Corroborated: https://www.motor.com/magazine-summary/service-tips-for-gdi-engines/
- **wot_wideband_lambda_enrichment** — Under WOT, the ECU enters open-loop power enrichment, targeting a rich mixture (lambda ~0.85). If fuel starvation is present, lambda remains lean (> 1.05) under WOT due to insufficient fuel volume. [standardized] motor.com; miataturbo.net. Corroborated: https://www.hpacademy.com/forum/practical-dyno-tuning/show/set-up-lambda-target/

## 3. Tolerance width (σ) — fires/clears across the WHOLE spread, not a knife-edge

Worst-case corners: vacuum leak idle TFT low corner = **20.0% > 15%**; vacuum leak 2500 TFT high corner = **5.0% <= 10%**; trim recovery delta low corner = **20.0% - 5.0% = 15.0% >= 15%**; stay-abstained (EGR) idle TFT high corner = **6.0% < 15.0%**. Every stay-abstained high corner sits safely BELOW every active C5 gate. Reported σ per band (uniform std-dev = (hi−lo)/√12):

| oracle code | band_id | separable | idle STFT/LTFT σ | 2500 STFT/LTFT σ | load σ | pressure σ | lambda σ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ERR-LC-001 | C5-VACUUM-LEAK | yes | 1.443/1.443 | 1.443/0.866 | 2.887 | 17.321 | 0.017 |
| ERR-LC-005 | C5-EGR-STUCK-OPEN-LOOKALIKIE | **NO** | 1.732/1.732 | 1.732/1.732 | 2.887 | 17.321 | 0.017 |

## 4. Seeded cases (10/10) — value sits in its own oracle-code band

| case_id | oracle code | fault_name | band | sep | MAF eq | rail pres | is GDI | STFT/LTFT idle | STFT/LTFT 2500 | WOT load | WOT rail pressure | WOT lambda |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-N011 | ERR-LC-001 | vacuum_leak_post_maf | C5-VACUUM-LEAK | Y | True | True | False | 5.9/15.2% | 1.5/0.3% | 92.3% | 322.0 kPa | 0.86 |
| EXP-N022 | ERR-LC-001 | vacuum_leak_post_maf | C5-VACUUM-LEAK | Y | True | False | False | 7.8/17.1% | -0.2/2.7% | 92.5% | None | 0.841 |
| EXP-N029 | ERR-LC-001 | vacuum_leak_post_maf | C5-VACUUM-LEAK | Y | True | True | False | 6.0/15.6% | -2.0/2.9% | 86.4% | 350.6 kPa | 0.864 |
| case_003 | ERR-LC-001 | vacuum_leak_post_maf | C5-VACUUM-LEAK | Y | True | True | False | 5.5/18.2% | -0.0/2.8% | 89.7% | 369.4 kPa | 0.843 |
| case_016 | ERR-LC-001 | vacuum_leak_post_maf | C5-VACUUM-LEAK | Y | True | True | False | 6.5/18.8% | -0.9/0.6% | 88.5% | 342.7 kPa | 0.863 |
| CSV-113 | ERR-LC-005 | egr_stuck_open | C5-EGR-STUCK-OPEN-LOOKALIKIE | abst | True | True | False | 1.6/1.4% | 0.6/-3.0% | 90.3% | 343.1 kPa | 0.851 |
| CSV-114 | ERR-LC-005 | egr_stuck_open | C5-EGR-STUCK-OPEN-LOOKALIKIE | abst | True | True | False | -0.2/-0.5% | 2.7/-2.4% | 93.2% | 352.1 kPa | 0.879 |
| REAL-004 | ERR-LC-005 | egr_stuck_open | C5-EGR-STUCK-OPEN-LOOKALIKIE | abst | True | True | False | 2.4/1.8% | 2.9/1.3% | 86.4% | 371.1 kPa | 0.835 |
| era1_001 | ERR-LC-005 | egr_stuck_open | C5-EGR-STUCK-OPEN-LOOKALIKIE | abst | True | False | False | -0.3/-2.3% | -1.8/0.9% | 94.2% | None | 0.867 |
| era3_015 | ERR-LC-001 | vacuum_leak_post_maf | C5-VACUUM-LEAK | Y | True | True | True | 8.7/16.5% | -0.0/0.1% | 89.6% | 15745.4 kPa | 0.824 |

## 5. Separability split — which cases the C5 signal can and cannot separate

Across the 10 C5 cases, we have a clear **6 separable vs 4 stay-abstained** split:

- **C5-Separable (6 cases):** `EXP-N011, EXP-N022, EXP-N029, case_003, case_016, era3_015`. These are vacuum leaks post-MAF (`ERR-LC-001`), including the PCV drift `era3_015` and the MAF-equipped `EXP-N022` (modeled as MAF-equipped from its BMW VIN). They carry the dynamic trim pattern and will successfully bank.
- **Stay-Abstained (4 cases):** `CSV-113, CSV-114, REAL-004, era1_001`. These are stuck-open EGR valve lookalikes (`ERR-LC-005`). Research and combustion physics confirm that they do not exhibit vacuum leak trims at idle (they dilute with inert exhaust, not oxygen), so they are seeded with normal/healthy C5 signals. They remain abstained at `MARGIN=0.02` to prevent back-solving.

## 6. C6-MAF-collision guard verification

All C5 rows have C6-only columns (`mode06_o2_response_margin_pct`, `maf_actual_calc_delta_pct_idle`, `maf_actual_calc_delta_pct_2500`) left as `None` or absent. This ensures C6's `_sensor_dynamics_state` returns `SENSOR_HEALTH_UNPROVEN_ABSTAIN` (not c6_decisive), completely avoiding false sensor-fault triggers on C5 rows. C5's precedence rule in the shim will further enforce this when both are present.
