# V3_C6_SYNTH_BANDS_2026-07-05

**Task:** `T-V3-P4-C6-SYNTH`  **Mode:** provisional-synthetic seed (side file)
**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, tolerance-wide, web-corroborated, `synthetic=true`, correctable.
**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** `/agent_workspace/.venv-wired/bin/python v3/gen_c6_synth_seed.py`.
**Data + manifest:** `v3/data/c6_synthetic_seed_2026-07-05.{csv,json}`.
**Baseline pin (from C6-PRE):** `V3_YARDSTICK_2026-07-05-C3B` (csv `9f530695…`, oracle `3088a7c3…`), run `POST_T_V3_P4_C3B`.

Seeds the 14 C6 cases' sensor-dynamics columns (`mode06_o2_response_margin_pct`, rich↔lean O2 timing, and two-point MAF actual-vs-calculated airflow) with values derived from each case's **oracle fault code** through the `cluster6.md` signature and C6-PRE contract. Consumed by `T-V3-P4-C6A` (dry-run) and `C6B` (commit).

## 1. No-back-solve statement

The generator's only data inputs are the pinned 14 C6 case IDs, each case's corpus oracle `expected_fault_family` / `expected_fault_code`, and the band table below. It does **not** read `sensor_fault.json`, `no_fault.json`, current ranks, predicted families, run traces, or any C6A/C6B consumer thresholds. The limits used in assertions are the **producer/research** limits from `cluster6.md` and `V3_C6_REVEAL_CONTRACT_2026-07-05.md`: Mode $06 margin relative to the vehicle limit, O2 response direction/slow timing, and MAF sustained >10–15% under-read at both points. Floats are sampled uniformly with a deterministic SHA-256-per-case seed; MAF g/s values are derived from modeled airflow and the sampled delta.

## 2. Per-column bands — cluster6 research vs web-real vs band used

| Column / signal | cluster6 producer threshold | Web-real range (cited) | Band used (tolerance-wide) | Grounding |
| --- | --- | --- | --- | --- |
| `mode06_o2_response_margin_pct` | Use vehicle Mode $06 result vs stored min/max; low margin or exceeded limit emits O2_LAZY_OR_BIASED | monitor framework standardized; numeric limit vehicle-specific | O2-fault ∈ **[2, 9]%** margin (fires); healthy/MAF/misfire ∈ **[35, 80]%** | **standardized-transport / manufacturer-specific numeric limit** |
| `o2_rich_to_lean_ms` | Longer-than-expected rich→lean response is positive evidence; not a universal ms line | CARB response-rate direction strong; example thresholds are OEM-specific | O2-fault ∈ **[650, 1200] ms**; healthy/MAF/misfire ∈ **[80, 220] ms** | **manufacturer-typical** |
| `o2_lean_to_rich_ms` | Longer-than-expected lean→rich response is positive evidence; not a universal ms line | public evidence supports slow transition direction, not fleet threshold | O2-fault ∈ **[620, 1150] ms**; healthy/MAF/misfire ∈ **[80, 230] ms** | **manufacturer-typical** |
| `maf_actual_calc_delta_pct_idle` | Sustained measured-MAF shortfall >10–15% vs modeled airflow at warm idle | Bosch HFM accuracy ±4%; vehicle-level screen widened beyond model/VE uncertainty | MAF-underread ∈ **[-28, -18]%** (fires); others ∈ **[-5, +5]%** | **empirical-inferred** |
| `maf_actual_calc_delta_pct_2500` | Sustained measured-MAF shortfall >10–15% vs modeled airflow at 2500 rpm | same; must persist at both points | MAF-underread ∈ **[-27, -18]%** (fires); others ∈ **[-5, +5]%** | **empirical-inferred** |
| `maf_gps_idle`, `maf_gps_2500` | source g/s supporting the delta | MAF is fast/accurate when healthy but contamination can bias reading | derived from `calc_airflow * (1 + delta/100)`; None only when MAF not applicable | **derived / correctable** |
| `calc_airflow_gps_idle`, `calc_airflow_gps_2500` | modeled-airflow reference path | alternate MAP/RPM/IAT/BARO path corroborates MAF rationality | idle modeled **[2.2, 3.9] g/s**; 2500 modeled **[8.0, 14.5] g/s** | **empirical-inferred support** |

### Citations

- **mode06_monitor_framework** — Mode $06 / J1979-style monitor reporting exposes recent monitor results and limits; the transport is standardized, but the numeric O2 response limit is manufacturer-specific. [standardized-transport / manufacturer-specific numeric limit] cluster6.md lines 114-115, 155, 171; CARB OBD II final regulation: https://www.arb.ca.gov/regact/2015/obdii2015/finalregorder2.pdf
- **o2_response_direction** — O2 deterioration is defined by delayed/slow response and activity loss; public sources support direction strongly but not a universal ms fail line. Seed uses wide slow bands (620-1200 ms) only as provisional synthetic evidence. [manufacturer-typical] cluster6.md lines 147-157; CARB OBD II final regulation: https://www.arb.ca.gov/regact/2015/obdii2015/finalregorder2.pdf
- **maf_component_accuracy** — Bosch HFM public data gives component-level accuracy/time response anchors; C6 widens the vehicle-level separator beyond component error and model uncertainty. [empirical-inferred] cluster6.md line 161; Bosch HFM2 datasheet mirror: https://www.farnell.com/datasheets/69647.pdf
- **maf_contamination_rationality** — DENSO describes MAF contamination/electronics effects that corrupt ECU load input, and trade diagnostic sources corroborate comparing measured MAF against an alternate modeled air path. [empirical-inferred / professional trade corroboration] https://www.denso-am.eu/products/engine-management-systems/mass-air-flow-sensors#textContent-33196; https://gearsmagazine.com/magazine/a-breath-of-fresh-air-8-pin-mass-airflow-sensors/
- **static_rejected** — Single static O2 voltage, AFR, or MAF magnitude is rejected; dynamic inconsistency or monitor/rationality evidence is required. [physics/regulatory rationale] cluster6.md lines 126-129, 188-193; V3_C6_REVEAL_CONTRACT_2026-07-05 §9

## 3. Tolerance width (σ) — fires/clears across the WHOLE spread, not a knife-edge

Worst-case corners: O2-fault Mode $06 high corner = **9% ≤ 10%** and O2 response low corner = **620 ms ≥ 600 ms**; MAF-underread high corner = **-18% ≤ -15%** at both points; healthy/lookalike O2 response high corner = **230 ms < 600 ms**, Mode $06 low corner = **35% > 10%**, and healthy MAF deltas stay within ±5%. Reported σ uses uniform std-dev `(hi−lo)/√12`.

| oracle code | band_id | emit path | separable | MAF applicable | Mode06 σ | R→L σ | L→R σ | MAF idle σ | MAF 2500 σ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | yes | True | 1.732 | 129.904 | 124.13 | 2.309 | 2.309 |
| ERR-SF-005 | C6-O2-IMPLAUSIBLE-NORMAL-CHEM | O2_LAZY_OR_BIASED | yes | True | 1.732 | 144.338 | 135.677 | 2.887 | 2.887 |
| ERR-SF-004 | C6-MAF-UNDERREAD | MAF_UNDERREAD | yes | True | 11.547 | 37.528 | 40.415 | 2.887 | 2.598 |
| ERR-MF-005 | C6-HEALTHY-LOOKALIKE-MISFIRE | SENSOR_HEALTH_UNPROVEN_ABSTAIN | **NO** | True | 11.547 | 37.528 | 40.415 | 1.732 | 1.732 |

## 4. Seeded cases (14/14) — value sits in its own oracle-code band

| case_id | oracle code | fault_name | band | emit | sep | Mode06 % | R→L ms | L→R ms | MAF Δ idle % | MAF Δ 2500 % | MAF g/s idle | calc g/s idle | MAF g/s 2500 | calc g/s 2500 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE-014 | ERR-SF-001 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | Y | 4.4 | 1010.0 | 805.0 | 3.8 | 2.3 | 3.31 | 3.19 | 10.95 | 10.7 |
| CASE-045 | ERR-SF-005 | sensor_fault_normal_operation | C6-O2-IMPLAUSIBLE-NORMAL-CHEM | O2_LAZY_OR_BIASED | Y | 8.6 | 1133.0 | 931.0 | -0.2 | -0.8 | 2.42 | 2.42 | 10.42 | 10.5 |
| CASE-048 | ERR-SF-005 | sensor_fault_normal_operation | C6-O2-IMPLAUSIBLE-NORMAL-CHEM | O2_LAZY_OR_BIASED | Y | 3.2 | 995.0 | 1029.0 | 0.5 | -3.2 | 2.9 | 2.89 | 12.45 | 12.86 |
| CSV-025 | ERR-SF-001 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | Y | 3.1 | 661.0 | 656.0 | -0.1 | -3.8 | 2.55 | 2.55 | 12.6 | 13.1 |
| EXP-N020 | ERR-SF-004 | sensor_fault_vvt_context | C6-MAF-UNDERREAD | MAF_UNDERREAD | Y | 45.7 | 122.0 | 155.0 | -22.0 | -22.5 | 2.85 | 3.65 | 10.71 | 13.82 |
| EXT-229 | ERR-SF-001 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | Y | 5.3 | 845.0 | 902.0 | 4.0 | 3.2 | 3.57 | 3.43 | 10.12 | 9.81 |
| EXT-230 | ERR-SF-001 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | Y | 4.1 | 1001.0 | 1016.0 | 0.9 | 3.0 | 2.94 | 2.91 | 11.6 | 11.26 |
| PDF-4G-05 | ERR-MF-005 | misfire_lookalike_pdf_4g_05 | C6-HEALTHY-LOOKALIKE-MISFIRE | SENSOR_HEALTH_UNPROVEN_ABSTAIN | abst | 69.1 | 171.0 | 130.0 | 2.4 | -0.4 | 3.21 | 3.13 | 9.07 | 9.11 |
| TC-046 | ERR-SF-001 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | Y | 4.1 | 668.0 | 1040.0 | -3.2 | -2.2 | 3.27 | 3.38 | 10.51 | 10.75 |
| YAML-CSV25 | ERR-SF-001 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | Y | 3.2 | 1097.0 | 629.0 | 1.1 | 0.9 | 2.99 | 2.96 | 13.24 | 13.12 |
| YAML-TC46 | ERR-SF-001 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | Y | 3.4 | 787.0 | 737.0 | 3.0 | -2.8 | 3.54 | 3.44 | 8.78 | 9.03 |
| case_046 | ERR-SF-001 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | Y | 7.6 | 812.0 | 807.0 | -1.0 | 1.5 | 2.93 | 2.96 | 11.2 | 11.03 |
| era1_006 | ERR-SF-001 | upstream_o2_sensor_lazy_response | C6-O2-LAZY | O2_LAZY_OR_BIASED | Y | 4.4 | 868.0 | 933.0 | 4.0 | 2.5 | 2.72 | 2.62 | 11.12 | 10.85 |
| era2_012 | ERR-SF-005 | sensor_fault_normal_operation | C6-O2-IMPLAUSIBLE-NORMAL-CHEM | O2_LAZY_OR_BIASED | Y | 5.1 | 874.0 | 893.0 | 2.3 | -1.8 | 3.61 | 3.53 | 13.41 | 13.66 |

## 5. Separability split — which cases the C6 signal can and cannot separate

Oracle-code split: **{'ERR-SF-001': 9, 'ERR-SF-005': 3, 'ERR-SF-004': 1, 'ERR-MF-005': 1}**. Emit-path split: **{'O2_LAZY_OR_BIASED': 12, 'MAF_UNDERREAD': 1, 'SENSOR_HEALTH_UNPROVEN_ABSTAIN': 1}**. MAF-less/speed-density modeled cases: **0**; if later vehicle identity marks any row speed-density, this generator already preserves the invariant by writing `None` to all MAF columns for `maf_applicable=false` bands.

- **C6-SEPARABLE (13):** `ERR-SF-001` + `ERR-SF-005` use the O2 dynamics path (`O2_LAZY_OR_BIASED`): low Mode $06 margin and slow rich↔lean response, with normal MAF plausibility. `ERR-SF-004` uses the MAF path (`MAF_UNDERREAD`): healthy O2 dynamics, but sustained >15% measured-MAF shortfall at both idle and 2500 rpm. These are synthetic C6A inputs only, not live accuracy wins.
- **STAY-ABSTAINED (1):** `PDF-4G-05` (`ERR-MF-005`) is the named lookalike from the task: oracle `misfire`, current engine `sensor_fault`. It is seeded below every C6 gate (healthy Mode $06 margin, healthy O2 timing, healthy MAF deltas) so C6 stops supporting the wrong sensor verdict; it remains for a misfire discriminator. **13 + 1 = 14.** ✔

> **Never read synthetic-seeded passes as real-world accuracy.** The manifest `synthetic=true` and downstream synthetic-vs-real split keep these correctable. Mode $06 numeric limits are manufacturer-specific, O2 ms bands are manufacturer-typical rather than universal, and MAF shortfall is empirical-inferred until validated on real vehicles.

## Provenance / guardrails

- Side file only: no write to `cases_petrol_v7.csv`, no engine/lab/registry/rule edit, no re-score, no yardstick mint, no abstain-dial change. Writes only under `v3/`. `Vault/` untouched. No `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
- Inputs: corpus oracle `expected_fault_family` / `expected_fault_code` for the pinned 14 `C6_CASES` + the band table above. Producer thresholds cited to `v3/research/research_answers/cluster6.md` and `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.md`. Governs `T-V3-P4-C6A` / `C6B`.
- Live web fetch note: the session attempted the mandated firecrawl path; CLI was not installed, then installed, but reported unauthenticated. This report therefore cites the already-landed, web-corroborated `cluster6.md` source set and its primary URLs rather than adding scratch `.firecrawl/` artifacts.
