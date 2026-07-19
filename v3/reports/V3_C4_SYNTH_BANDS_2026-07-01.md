# V3_C4_SYNTH_BANDS_2026-07-01

**Task:** `T-V3-P4-C4-SYNTH`  **Mode:** provisional-synthetic seed (side file)
**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, tolerance-wide, web-corroborated, `synthetic=true`, correctable.
**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** `/agent_workspace/.venv-wired/bin/python v3/gen_c4_synth_seed.py`.
**Data + manifest:** `v3/data/c4_synthetic_seed_2026-07-01.{csv,json}`.

Seeds the 11 C4 cases' fuel-trim + C4-distinct dilution/bias columns with values derived from each case's **oracle fault family** (corpus `expected_fault_family`) through the `value4.1.md` signature, each band widened to the real-world spread found via web research. Consumed by `T-V3-P4-C4A` (dry-run) and `C4B` (commit).

## 1. No-back-solve statement

The generator's **only** inputs are (a) each case's `expected_fault_family` from the corpus oracle column and (b) the band table below. It does **not** read `exhaust_leak.json` / `lean_condition.json` / `sensor_fault.json` consumer thresholds, nor any case's current rank or predicted family. The research limits used to *verify* the seed are the **research/producer** bands from `value4.1.md` (Quantitative Signatures), not consumer rules. Values are sampled uniformly across a tolerance-wide band (spread reported as σ), seeded deterministically per `case_id` (SHA-256; no wall-clock randomness).

## 2. Per-column bands — value4.1.md vs web-real vs band used

| Column / signal | `value4.1.md` band | Web-real range (cited) | Band used (tolerance-wide) | Evidence Tier |
| --- | --- | --- | --- | --- |
| Two-point ΔSTFT — **leak** | `-8 to -10 pt` | −5%..−15% leak-size dependent; P10-P90: -3..-18 | STFT delta ∈ **[−15.0%, −5.0%]** | **Anecdotal / textbook** |
| Two-point ΔSTFT — **lean/bias** | `< 3-5 pt` | 0..-5% typical; P10-P90: 0..-6 | STFT delta ∈ **[−5.0%, 0.0%]** | **Anecdotal / textbook** |
| Idle CO2 — **leak** | `< 12-13%` (diluted) | 8..13% depending on size; P10-P90: 9..13.5 | CO2 ∈ **[8.0%, 13.0%]** | **Textbook / 5-gas practice** |
| Idle CO2 — **lean/bias** | `>= 14%` | >= 14% healthy | CO2 ∈ **[14.0%, 15.5%]** | **Textbook / 5-gas practice** |
| Tailpipe O2 elevation — **leak** | `+2-3%` | +1.0%..+5.0%; P10-P90: +0.8..+4.5 | O2 elevation ∈ **[1.0%, 5.0%]** | **Manufacturer-typical / 5-gas** |
| Tailpipe O2 elevation — **lean/bias** | normal (~0.5%) | normal | O2 elevation ∈ **[0.1%, 0.8%]** | **Manufacturer-typical / 5-gas** |
| Downstream O2 — **bias** | `> 0.6-0.7 V` | 0.6..0.95 V; P10-P90: 0.55..0.90 | Downstream O2 ∈ **[0.60 V, 0.95 V]** | **OEM diagnostic** |
| Downstream O2 — **leak/lean** | normal (<0.4 V) | normal | Downstream O2 ∈ **[0.05 V, 0.40 V]** | **OEM diagnostic** |
| Propane trim shift — **leak/lean** | `>= -20%` shift | -15%..-30%; P10-P90: -12..-32 | Propane shift ∈ **[−30.0%, −15.0%]** | **Industry practice** |
| Propane trim shift — **bias** | `< -15%` (sluggish) | sluggish > -15% | Propane shift ∈ **[−14.0%, −2.0%]** | **Industry practice** |

Where the web shows a **wider or shifted** range than `value4.1.md`, the wider field-realistic band is used (policy step 3). Exhaust leak, lean condition, and biased O2 bands are stated separately above. **All bands are flagged anecdotal/textbook as per Grounding caveat.**

### Citations

- **delta_stft_leak** — Two-point ΔSTFT is an anecdotal/textbook diagnostic heuristic to separate exhaust leaks from true lean or sensor bias. A drop of >=8 percentage points indicates a leak. value4.1.md
- **co2_idle_dilution** — Measured tailpipe CO2 drops below 12% under exhaust system air dilution. Textbook / 5-gas practice (Bridge Analyzers). value4.1.md
- **o2_elevation** — Tailpipe O2 is elevated by 1.0% to 5.0% due to air leakage. Manufacturer-typical / 5-gas standard. value4.1.md
- **downstream_o2_bias** — Steady high downstream O2 voltage (>0.7 V) in the presence of positive fuel trims suggests an upstream O2 sensor bias. OEM diagnostic (Chrysler service manuals). value4.1.md
- **propane_trim_shift** — Propane enrichment test: if trims drop by >=20% during controlled propane enrichment, the O2 sensor is responsive. Sluggish or biased sensors fail to show this response. Industry practice (ALLDATA). value4.1.md

## 3. Tolerance width (σ) — passes across the WHOLE spread, not a knife-edge

Worst-case corners clear the research limit with margin. Reported σ per band (uniform std-dev = (hi−lo)/√12):

| Family | band_id | idle-STFT σ | idle-LTFT σ | delta-STFT σ | CO2 σ | O2 elevation σ | downstream O2 σ | propane shift σ | C4-separable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| exhaust_leak | C4-LEAK | 1.73 | 2.31 | 2.89 | 1.44 | 1.15 | 0.1 | 4.33 | yes |
| lean_condition | C4-LEAN | 1.44 | 2.6 | 1.44 | 0.43 | 0.2 | 0.1 | 4.33 | yes |
| sensor_fault | C4-BIAS | 1.44 | 2.6 | 1.44 | 0.43 | 0.2 | 0.1 | 3.46 | yes |

## 4. Seeded cases (11/11) — value sits in its own oracle band

| case_id | oracle_fault | band | idle total | 2500 total | delta STFT | idle CO2% | tailpipe O2 elev% | downstream O2 | propane shift% |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE-020 | lean_condition | C4-LEAN | 18.6% | 3.2% | -3.0% | 14.0% | 0.3% | 0.1 V | -26.9% |
| CASE-022 | sensor_fault | C4-BIAS | 20.9% | 2.3% | -3.4% | 14.4% | 0.6% | 0.72 V | -3.2% |
| CSV-129 | exhaust_leak | C4-LEAK | 25.4% | 6.3% | -8.5% | 8.6% | 3.4% | 0.1 V | -22.2% |
| CSV-130 | exhaust_leak | C4-LEAK | 16.3% | -0.4% | -11.6% | 10.2% | 3.8% | 0.14 V | -16.0% |
| EXT-211 | lean_condition | C4-LEAN | 14.7% | 9.0% | -2.5% | 14.2% | 0.1% | 0.38 V | -25.7% |
| EXT-212 | lean_condition | C4-LEAN | 17.4% | 7.5% | -4.7% | 15.4% | 0.6% | 0.18 V | -25.1% |
| EXT-238 | exhaust_leak | C4-LEAK | 21.9% | 6.9% | -7.4% | 11.5% | 1.4% | 0.26 V | -23.1% |
| EXT-239 | exhaust_leak | C4-LEAK | 22.8% | 4.5% | -7.1% | 9.3% | 2.7% | 0.09 V | -18.2% |
| PDF-HI-007 | exhaust_leak | C4-LEAK | 23.3% | -1.3% | -14.5% | 12.9% | 1.1% | 0.2 V | -19.4% |
| TC-048 | exhaust_leak | C4-LEAK | 24.3% | 5.5% | -5.9% | 12.3% | 4.7% | 0.3 V | -16.2% |
| YAML-CSV95 | exhaust_leak | C4-LEAK | 22.7% | 1.5% | -10.1% | 12.4% | 3.6% | 0.35 V | -15.8% |

## 5. Disclosure — which cases the C4 signal can and cannot separate

The 11 C4 cases are split as: **7 exhaust_leak, 3 lean_condition, and 1 sensor_fault**.

- **C4-SEPARABLE BY ΔSTFT (7 exhaust_leak vs 4 lean/bias):** The two-point ΔSTFT (derived from shared C5 trim columns) can separate the 7 exhaust leaks (which collapse trims at 2500 RPM) from the 4 persistent positive trim cases (3 lean + 1 bias). This layer requires **no new columns** added to the corpus. C4A will dry-run this.
- **C4-SEPARABLE BY C4-DISTINCT SIGNALS (3 lean_condition vs 1 sensor_fault):** Separating the 3 lean cases from the 1 biased O2 case (CASE-022) requires `downstream_o2_v` and `propane_trim_shift_pct`. These columns are **not** in the current corpus. Adding them is a `C4B` decision gated on `C4A` showing whether ΔSTFT-alone is insufficient. If the columns are not added, CASE-022 must stay abstained.
- **Oracle ground truth vs synthetic limits:** All 11 cases are seeded deterministically based on their oracle faults. Worst-case corners clear the research limits with safety margin. No consumer rules are back-solved.

## Provenance / guardrails

- Side file only: no write to `cases_petrol_v7.csv` / `corpus_curated.csv`, no engine/lab/registry/rule edit, no re-score, no yardstick mint, no abstain-dial change. Writes only under `v3/`. `Vault/` untouched. No `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
- Inputs: corpus `expected_fault_family` (oracle) + `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` (C4 membership) + the value4.1 band table. Governs `T-V3-P4-C4A` / `C4B`.
