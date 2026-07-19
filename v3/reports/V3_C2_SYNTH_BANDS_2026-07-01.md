# V3_C2_SYNTH_BANDS_2026-07-01

**Task:** `T-V3-P4-C2-SYNTH`  **Mode:** provisional-synthetic seed (side file)
**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, tolerance-wide, web-corroborated, `synthetic=true`, correctable.
**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** `/agent_workspace/.venv-wired/bin/python v3/gen_c2_synth_seed.py`.
**Data + manifest:** `v3/data/c2_synthetic_seed_2026-07-01.{csv,json}`.

Seeds the 22 C2 cases' fuel-trim + Mode $06 catalyst columns with values derived from each case's **oracle fault family** (corpus `expected_fault_family`) through the `cluster2.md` signature, each band widened to the real-world spread found via web research. Consumed by `T-V3-P4-C2A` (dry-run) and `C2B` (commit).

## 1. No-back-solve statement

The generator's **only** inputs are (a) each case's `expected_fault_family` from the corpus oracle column and (b) the band table below. It does **not** read `rich_mixture.json` / `catalyst_failure.json` consumer thresholds, nor any case's current rank or predicted family. The `-10%` rich trim limit and `0.20` catalyst index pass limit used to *verify* the seed are the **research/producer** bands from `cluster2.md` (Quantitative Signatures), not consumer rules. Values are sampled uniformly across a tolerance-wide band (spread reported as σ), seeded deterministically per `case_id` (SHA-256; no wall-clock randomness).

## 2. Per-column bands — cluster2.md vs web-real vs band used

| Column / signal | `cluster2.md` band | Web-real range (cited) | Band used (tolerance-wide) |
| --- | --- | --- | --- |
| Total fuel trim — **rich** | `<= -10%` (TRUE_RICH) | −10%..−20%+ rich; ~−20% clearly rich, P0172 | idle STFT+LTFT ∈ **[−25%, −12%]**, 2500 ∈ [−21%, −10%] |
| Total fuel trim — **normal/catalyst** | ±10% normal | −10%..+10% balanced | idle STFT+LTFT ∈ **[−7%, +7%]** (near zero) |
| Total fuel trim — **lean** | +ve (mirror) | +10%..+25% (case +20/+22); corrects at rpm | idle ∈ **[+12%, +26%]**, 2500 ∈ [+1%, +10%] (corrects) |
| Total fuel trim — **sensor skew** | n/a (confounder) | erratic; O2/ground skew | idle ∈ **[−8%, +16%]** wide/ambiguous (no clean fire) |
| `catalyst_index_ratio` — healthy | `<= 0.20` pass | low ratio, downstream flatlines | **[0.05, 0.18]** |
| `catalyst_index_ratio` — failed | `> 0.20` fail | approaches 1:1 (0.76 set P0430) | **[0.55, 0.90]** |
| `catalyst_index_ratio` — sensor skew | borderline | falsely elevated by bad O2 | **[0.28, 0.55]** (mimics cat) |
| `decel_co_pct` — healthy / failed | `> 0.8%` fail | healthy <0.5%; dead cat several % | healthy **[0.05, 0.60]** / failed **[0.90, 2.20]** |
| `mode06_catalyst_margin_pct` | derived | — | `(0.20 − index)/0.20 × 100` (+ve = pass headroom) |
| `pre_post_cat_hc_delta_ppm` | — | healthy reduces HC 70–90% | healthy **[300, 900]** / failed **[10, 120]** |
| `pre_post_cat_co_delta_pct` | — | healthy reduces CO 70–90% | healthy **[0.5, 2.0]** / failed **[0.0, 0.25]** |

Where the web shows a **wider or shifted** range than `cluster2.md`, the wider field-realistic band is used (policy step 3). Rich vs catalyst_failure bands are stated separately above.

### Citations

- **fuel_trim_normal_pm10** — LTFT normally -10%..+10%; approaching -20% indicates rich (P0172 'System Too Rich'). ricksfreeautorepairadvice.com/what-does-negative-fuel-trim-mean-expert-diagnosis-guide/; engineerfix.com/what-should-long-term-and-short-term-fuel-trim-be/
- **rich_negative_trim** — Negative trim = ECU pulling fuel because engine runs rich; both STFT+LTFT negative = sustained rich; fuel-delivery cause is consistent across RPM. foxwelldiag.com/blogs/car-diagnostic/understanding-long-term-fuel-trim-bank-1-and-how-to-diagnose-issues
- **catalyst_index_ratio** — Mode $06 rear/front O2 switch ratio: healthy cat = low ratio (downstream flatlines); failed cat = ratio approaches 1:1 (documented 0.76 set P0430). brakeandfrontend.com/obd-ii-diagnostics-checking-into-mode-06/
- **decel_co** — Healthy cat reduces CO 70-90% (near-zero tailpipe CO, often <0.5% at idle); dead cat / rich engine pushes idle CO into several-percent range. aa1car.com/library/converter.htm; ipdusa.com/Articles/770/Diagnosing-Faulty-Catalytic-Converters
- **lean_positive_trim** — Positive trim = ECU adding fuel for a lean condition; +20% documented (case +22/+20), ECU compensates up to ~+25%; vacuum-leak signature is high-at-idle / corrects at 1500-2500 rpm. vehicleservicepros.com/.../fuel-trim-finding-a-vacuum-leak...; xerodrive.com/auto-guides/long-term-fuel-trim-high-at-idle/
- **sensor_skew** — A bad O2 sensor / ground-voltage drop skews the Mode $06 ratio and fuel trim, causing false catalyst codes (P0420/P0430) — replace O2 before condemning the cat. brakeandfrontend.com/obd-ii-diagnostics-checking-into-mode-06/

## 3. Tolerance width (σ) — passes across the WHOLE spread, not a knife-edge

Worst-case corners clear the research limit with margin: rich total trim high corner = −4 + −8 = **−12% ≤ -10%**; lean total low corner = +3 + +9 = **+12% ≥ 10%**; failed catalyst index low corner = **0.55 > 0.2**. Reported σ per band (uniform std-dev = (hi−lo)/√12):

| Family | band_id | idle-STFT σ | idle-LTFT σ | index σ | C2-separable |
| --- | --- | --- | --- | --- | --- |
| rich_mixture | C2-RICH | 1.73 | 2.02 | 0.04 | yes |
| catalyst_failure | C2-CAT | 1.73 | 2.31 | 0.1 | yes |
| lean_condition | C2-LEAN | 1.44 | 2.6 | 0.04 | NO |
| sensor_fault | C2-SENSOR | 3.46 | 3.46 | 0.08 | NO |

## 4. Seeded cases (22/22) — value sits in its own oracle band

| case_id | oracle_fault | band | idle total | 2500 total | index | margin% | decel CO% |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CASE-015 | catalyst_failure | C2-CAT | 5.4 | 6.2 | 0.71 | -255.0 | 1.07 |
| CASE-023 | rich_mixture | C2-RICH | -15.3 | -18.6 | 0.145 | 27.5 | 0.14 |
| CASE-029 | rich_mixture | C2-RICH | -15.7 | -15.1 | 0.059 | 70.5 | 0.26 |
| CASE-040 | rich_mixture | C2-RICH | -23.5 | -15.5 | 0.096 | 52.0 | 0.06 |
| CSV-100 | lean_condition | C2-LEAN | 14.9 | 8.1 | 0.155 | 22.5 | 0.4 |
| CSV-121 | catalyst_failure | C2-CAT | 5.0 | 0.5 | 0.801 | -300.5 | 0.93 |
| CSV-122 | catalyst_failure | C2-CAT | 4.5 | 5.3 | 0.701 | -250.5 | 1.91 |
| EXP-N017 | lean_condition | C2-LEAN | 18.2 | 7.7 | 0.144 | 28.0 | 0.16 |
| EXT-217 | rich_mixture | C2-RICH | -14.3 | -15.2 | 0.117 | 41.5 | 0.2 |
| EXT-232 | catalyst_failure | C2-CAT | -4.3 | -5.7 | 0.831 | -315.5 | 1.1 |
| EXT-233 | catalyst_failure | C2-CAT | -3.2 | 2.4 | 0.809 | -304.5 | 0.99 |
| PDF-HI-001 | rich_mixture | C2-RICH | -21.1 | -13.1 | 0.15 | 25.0 | 0.21 |
| PDF-HI-006 | catalyst_failure | C2-CAT | 0.7 | 1.8 | 0.792 | -296.0 | 1.91 |
| RULE-CO-1 | rich_mixture | C2-RICH | -15.8 | -11.0 | 0.125 | 37.5 | 0.47 |
| YAML-PDF_HI_001 | rich_mixture | C2-RICH | -17.3 | -13.9 | 0.178 | 11.0 | 0.23 |
| case_002 | rich_mixture | C2-RICH | -22.6 | -17.5 | 0.1 | 50.0 | 0.4 |
| case_004 | sensor_fault | C2-SENSOR | 2.6 | 5.1 | 0.407 | -103.5 | 0.44 |
| case_015 | rich_mixture | C2-RICH | -13.8 | -13.5 | 0.139 | 30.5 | 0.59 |
| case_017 | rich_mixture | C2-RICH | -22.4 | -14.9 | 0.134 | 33.0 | 0.26 |
| era1_017 | sensor_fault | C2-SENSOR | 5.9 | 3.8 | 0.444 | -122.0 | 0.68 |
| era2_015 | lean_condition | C2-LEAN | 21.0 | 3.8 | 0.083 | 58.5 | 0.44 |
| era2_019 | rich_mixture | C2-RICH | -16.6 | -14.0 | 0.129 | 35.5 | 0.14 |

## 5. Disclosure — which cases the C2 signal can and cannot separate

The 22 C2 cases are **not** all cleanly rich-vs-catalyst. Oracle split: **11 rich_mixture, 6 catalyst_failure, 3 lean_condition, 2 sensor_fault**.

- **C2-SEPARABLE (17): rich_mixture + catalyst_failure.** The C2 producer (TRUE_RICH on trim ≤ −10% vs LOW_OSC/high-index on the catalyst monitor) cleanly separates these two — the seed puts rich cases in the negative-trim band and catalyst cases in the near-zero-trim + failed-index band. C2A should predict these flip toward top-3.
- **NOT C2-SEPARABLE by rich-vs-catalyst (3 lean_condition):** a lean case has **positive** trim, so it fires neither TRUE_RICH (needs ≤ −10%) nor a catalyst fail. Seeded honestly from lean ground truth (positive idle trim, corrects at 2500), these **stay abstained** under the C2 producer/consumer — they need a lean/vacuum discriminator (a later cluster), not C2. Flagged `c2_separable=false`.
- **CONFOUNDED (2 sensor_fault):** O2/ground skew produces a falsely-elevated index that *mimics* catalyst failure (both cases' current prediction is `catalyst_failure`). Seeded with the ambiguous skew signature (erratic trims, borderline index 0.28–0.55). The C2 catalyst monitor alone **cannot** distinguish sensor skew from real catalyst failure — the research fix is the OSC active test / sensor rationality (tier c), not the passive C2 index. Flagged `c2_separable=false`; likely stays mis-routed/abstained until a sensor-rationality signal lands. **Synthetic passes must never be read as real-world accuracy** — the manifest `synthetic=true` + scoreboard split keep them distinguishable.

## Provenance / guardrails

- Side file only: no write to `cases_petrol_v7.csv` / `corpus_curated.csv`, no engine/lab/registry/rule edit, no re-score, no yardstick mint, no abstain-dial change. Writes only under `v3/`. `Vault/` untouched. No `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
- Inputs: corpus `expected_fault_family` (oracle) + `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` (C2 membership) + the web-validated band table. Governs `T-V3-P4-C2A` / `C2B`.
