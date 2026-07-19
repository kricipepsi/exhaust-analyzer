# V3_C3_SYNTH_BANDS_2026-07-05

**Task:** `T-V3-P4-C3-SYNTH`  **Mode:** provisional-synthetic seed (side file)
**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, tolerance-wide, web-corroborated, `synthetic=true`, correctable.
**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** `/agent_workspace/.venv-wired/bin/python v3/gen_c3_synth_seed.py`.
**Data + manifest:** `v3/data/c3_synthetic_seed_2026-07-05.{csv,json}`.
**Baseline pin (from C3-PRE):** `V3_YARDSTICK_2026-07-05` (csv `3df2e8cb…`, oracle `3088a7c3…`), run `POST_T_V3_P4_C2B`.

Seeds the 22 C3 cases' control-plausibility columns (`koeo_map_baro_delta_kpa, module_voltage_loaded_v, dlc_signal_ground_drop_v, gas_obd_lambda_delta, lambda_perception_delta, bidirectional_fuel_response_ok_bool`) with values derived from each case's **oracle fault code** through the `cluster3_prepped.md` signature (lines 183-188), each band widened to the real-world spread found via web research. Consumed by `T-V3-P4-C3A` (dry-run) and `C3B` (commit).

## 1. No-back-solve statement

All 22 C3 cases share `expected_fault_family = ecu_fault`, so the band group is keyed on the finer **`expected_fault_code`** — the corpus **answer key** — resolved to a registry `fault_name`. The generator's **only** inputs are (a) each case's `expected_fault_code` and (b) the band table below. It does **not** read `ecu_fault.json` / `sensor_fault.json` consumer thresholds, nor any case's current rank or predicted family. The Δλ≥0.05, |MAP−BARO|≥5 kPa, ΔV_gnd>0.20 V, Vmod<12.0 V and O2-swing<0.1 V limits used to *verify* the seed are the **research/producer** bands from `cluster3_prepped.md`, not consumer rules. Floats are sampled uniformly across a tolerance-wide band (σ reported), seeded deterministically per `case_id` (SHA-256; no wall-clock randomness). The bool is **deterministic** per fault (only P0606 → `False`), not sampled.

## 2. Per-column bands — cluster3 research vs web-real vs band used

| Column / signal | cluster3 producer threshold | Web-real range (cited) | Band used (tolerance-wide) | Grounding |
| --- | --- | --- | --- | --- |
| `dlc_signal_ground_drop_v` — bias/offset | `> 0.20 V` (signal ground) | computer-ground fault > 0.10 V; trouble at 0.30 V | lean-bias ∈ **[0.22, 0.45] V** (fires); others ≤ 0.16 V | **standardized** |
| `gas_obd_lambda_delta` (Δλ) | `>= 0.05` divergence | practitioner heuristic (no OEM constant) | separable ∈ **[0.06, 0.14]** (fires); abstain ≤ 0.04 | **empirical-anecdotal** |
| `lambda_perception_delta` | derived from divergence | ECU perceived-vs-actual λ gap | separable ∈ **[0.06, 0.15]**; abstain ≤ 0.04 | **empirical-anecdotal** |
| `koeo_map_baro_delta_kpa` | `>= 5 kPa` static split | KOEO MAP≈BARO ~98-102 kPa; split sets P0069 | rich-bias ∈ **[5.5, 12.0] kPa** (fires); others < 3.5 | **manufacturer-typical** |
| `module_voltage_loaded_v` | `< 12.0 V` supply suspect | P0606 triggered by weak battery < 12.4 V | processor ∈ **[9.5, 11.9] V** (low); others ≥ 11.8 | **manufacturer-typical** |
| `bidirectional_fuel_response_ok_bool` | O2 swing `< 0.1 V` → unresponsive | active-test/propane confirms responsiveness | **False** only for P0606; **True** otherwise (deterministic) | **manufacturer-typical** |

Where the web shows a **wider or stricter** range than the research answer (computer grounds fault below 0.10 V vs the 0.20 V signal-ground gate), the band is set to fire the producer gate robustly while staying field-realistic (policy step 3). Bands are stated separately per oracle sub-fault below.

### Citations

- **ground_drop_standard** — Ground-circuit voltage drop max 0.1 V (0.2 V for a wire/cable run); computer/sensor grounds are the strictest — Fluke: any reading > 0.10 V on a computer ground is a fault, and as little as 0.30 V on a computer ground causes trouble; CARDONE ECM bulletin: allowable drop 0.1 V, > 0.3 V unacceptable. [STANDARDIZED] fluke.com/en-us/learn/blog/automotive/electrical-automotive-troubleshooting; aa1car.com/library/voltage_drop_testing.htm; cardone.com PT77-0008
- **ground_offset_lean_mechanism** — A positive ground offset raises the O2 voltage the ECU sees; the ECU reads a genuinely stoichiometric/lean mixture as RICH and commands negative fuel trim, driving the engine physically lean — the tell is the contradiction between sensor/OBD command and actual chemistry. [empirical/field] vehicleservicepros.com fuel-trims-downstream-o2; fordfiesta.org O2-sensors-reading-rich-fuel-trims-adding-more-fuel
- **koeo_map_baro** — With the key on, engine off, manifold pressure equals ambient barometric pressure (~98-102 kPa at sea level); MAP and BARO should read equal/very-similar at KOEO, and a significant MAP-vs-BARO difference sets a plausibility DTC (e.g. P0069). [manufacturer-typical] aa1car.com/library/map_sensors.htm; engineerfix.com/how-to-test-a-map-sensor-with-a-scan-tool; underhoodservice.com/follow-the-map-sensor
- **lambda_divergence** — Gas-to-OBD divergence Δλ = |λ_OBD − λ_tailpipe| ≥ 0.05 flags a control-reference fault (exhaust analyzer reads lean while OBD trims command rich, or vice-versa). [EMPIRICAL-ANECDOTAL — practitioner heuristic, not an OEM/SAE constant] cluster3_prepped.md §Quantitative Diagnostic Signature Mapping line 183
- **processor_p0606** — P0606 = ECM internal CPU/RAM/ROM self-test failure; the module cannot correctly interpret its 50+ sensor inputs so ALL ECU-reported data is untrustworthy — yet the engine frequently runs normally (MIL only). Weak battery (< 12.4 V) / poor grounds are common triggers. [manufacturer-typical] obd-codes.com/p0606; fixdapp.com/blog/p0606-code; skanyx.com/codes/p0606
- **bidirectional_response** — Active bidirectional fuel-override (±25% / −12.5% steps) with an O2 swing < 0.1 V indicates the loop is unresponsive to command; a healthy loop swings and the propane/override test confirms sensor responsiveness. [manufacturer-typical] cluster3_prepped.md §Quantitative Diagnostic Signature Mapping line 188

## 3. Tolerance width (σ) — fires/clears across the WHOLE spread, not a knife-edge

Worst-case corners: lean-bias ground drop low corner = **0.22 V > 0.20**; rich-bias MAP-BARO low corner = **5.5 kPa ≥ 5.0**; processor Vmod high corner = **11.9 V < 12.0**; every separable Δλ low corner = **0.06 ≥ 0.05**. Every abstain-group high corner sits BELOW every gate (Δλ ≤ 0.04, ground ≤ 0.09 V, MAP-BARO ≤ 3.5 kPa). Reported σ per band (uniform std-dev = (hi−lo)/√12):

| oracle code | band_id | separable | map-baro σ | Vmod σ | gnd-drop σ | Δλ σ | perception σ | bidir_ok |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ERR-EF-006 | C3-LEAN-BIAS | yes | 1.01 | 0.52 | 0.066 | 0.023 | 0.026 | True |
| ERR-EF-007 | C3-RICH-BIAS | yes | 1.876 | 0.462 | 0.02 | 0.023 | 0.026 | True |
| ERR-ECU-001 | C3-PROCESSOR | yes | 1.01 | 0.693 | 0.035 | 0.02 | 0.023 | False |
| ERR-EF-002 | C3-POA-CONFOUNDER | **NO** | 1.01 | 0.577 | 0.02 | 0.012 | 0.012 | True |
| ERR-EF-008 | C3-INTERMITTENT | **NO** | 0.866 | 0.577 | 0.017 | 0.009 | 0.009 | True |

## 4. Seeded cases (22/22) — value sits in its own oracle-code band

| case_id | oracle code | fault_name | band | sep | MAP-BARO kPa | Vmod V | gnd V | Δλ | perc. | bidir_ok |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE-039 | ERR-EF-002 | ecu_fault_poa_context | C3-POA-CONFOUNDER | abst | 1.5 | 12.97 | 0.084 | 0.025 | 0.015 | True |
| CSV-041 | ERR-EF-006 | ecu_fault_lean_bias | C3-LEAN-BIAS | Y | 1.9 | 13.46 | 0.385 | 0.117 | 0.12 | True |
| CSV-045 | ERR-ECU-001 | ecu_internal_processor_fault | C3-PROCESSOR | Y | 2.7 | 10.2 | 0.063 | 0.116 | 0.116 | False |
| CSV-123 | ERR-EF-007 | ecu_fault_rich_bias | C3-RICH-BIAS | Y | 7.3 | 14.07 | 0.074 | 0.115 | 0.101 | True |
| CSV-124 | ERR-EF-007 | ecu_fault_rich_bias | C3-RICH-BIAS | Y | 7.5 | 13.48 | 0.062 | 0.134 | 0.143 | True |
| CSV-125 | ERR-ECU-001 | ecu_internal_processor_fault | C3-PROCESSOR | Y | 2.1 | 11.52 | 0.044 | 0.06 | 0.101 | False |
| CSV-126 | ERR-ECU-001 | ecu_internal_processor_fault | C3-PROCESSOR | Y | 2.4 | 10.97 | 0.07 | 0.113 | 0.107 | False |
| ECU-001 | ERR-EF-006 | ecu_fault_lean_bias | C3-LEAN-BIAS | Y | 1.9 | 13.49 | 0.32 | 0.119 | 0.072 | True |
| ECU-009 | ERR-EF-002 | ecu_fault_poa_context | C3-POA-CONFOUNDER | abst | 0.8 | 13.88 | 0.048 | 0.039 | 0.022 | True |
| EXP-N002 | ERR-EF-006 | ecu_fault_lean_bias | C3-LEAN-BIAS | Y | 3.1 | 11.96 | 0.234 | 0.089 | 0.082 | True |
| EXP-N004 | ERR-EF-006 | ecu_fault_lean_bias | C3-LEAN-BIAS | Y | 3.2 | 13.29 | 0.253 | 0.071 | 0.085 | True |
| EXP-N005 | ERR-EF-008 | ecu_fault_intermittent_normal_test | C3-INTERMITTENT | abst | 1.0 | 13.27 | 0.048 | 0.023 | 0.023 | True |
| EXP-N018 | ERR-EF-002 | ecu_fault_poa_context | C3-POA-CONFOUNDER | abst | 2.2 | 13.93 | 0.087 | 0.019 | 0.014 | True |
| EXP-N019 | ERR-ECU-001 | ecu_internal_processor_fault | C3-PROCESSOR | Y | 0.7 | 9.71 | 0.08 | 0.104 | 0.124 | False |
| EXT-221 | ERR-EF-006 | ecu_fault_lean_bias | C3-LEAN-BIAS | Y | 1.3 | 12.83 | 0.302 | 0.083 | 0.142 | True |
| TC-021 | ERR-EF-006 | ecu_fault_lean_bias | C3-LEAN-BIAS | Y | 1.2 | 12.25 | 0.25 | 0.105 | 0.107 | True |
| YAML-CSV41 | ERR-EF-006 | ecu_fault_lean_bias | C3-LEAN-BIAS | Y | 0.9 | 13.1 | 0.282 | 0.088 | 0.12 | True |
| YAML-CSV45 | ERR-ECU-001 | ecu_internal_processor_fault | C3-PROCESSOR | Y | 1.1 | 10.28 | 0.143 | 0.11 | 0.116 | False |
| YAML-RULE_NOx_1 | ERR-ECU-001 | ecu_internal_processor_fault | C3-PROCESSOR | Y | 1.8 | 9.61 | 0.131 | 0.082 | 0.114 | False |
| YAML-TC47 | ERR-ECU-001 | ecu_internal_processor_fault | C3-PROCESSOR | Y | 3.3 | 10.61 | 0.12 | 0.107 | 0.106 | False |
| case_001 | ERR-EF-006 | ecu_fault_lean_bias | C3-LEAN-BIAS | Y | 3.0 | 13.04 | 0.24 | 0.063 | 0.12 | True |
| case_013 | ERR-EF-007 | ecu_fault_rich_bias | C3-RICH-BIAS | Y | 11.6 | 13.35 | 0.082 | 0.101 | 0.136 | True |

## 5. Separability split — which cases the C3 signal can and cannot separate

The 22 C3 cases split by oracle code: **8 lean-bias (ERR-EF-006), 3 rich-bias (ERR-EF-007), 7 processor/P0606 (ERR-ECU-001), 3 POA-confounder (ERR-EF-002), 1 intermittent (ERR-EF-008)**.

- **C3-SEPARABLE (18):** ERR-EF-006 + ERR-EF-007 + ERR-ECU-001. The ControlPlausibilityState producer separates these three: lean-bias fires the ground-drop (>0.20 V) + Δλ divergence gates; rich-bias fires the KOEO MAP-BARO split (≥5 kPa) + Δλ; the P0606 processor fault fires the deterministic bidirectional-unresponsive gate (`bool=False`) with a low supply voltage. C3A should predict these flip toward top-3.
- **STAY-ABSTAINED (4):** the C3-PRE §6 confounders. **3 POA-context (ERR-EF-002)** — a co-existing PHYSICAL oil-burning fault shifts exhaust chemistry so gas and OBD AGREE; the Δλ test fails to trigger, so C3 cannot separate them. **1 intermittent (ERR-EF-008)** — the fault is not active in the single idle snapshot, so no control-plausibility signal exists to measure. Both are seeded **honestly below every producer gate** (never into a passing band) and flagged `stay_abstained=true`; they remain abstained under the C3 producer/consumer until a different discriminator (physical-fault isolation, or repeat sampling) lands. **18 + 4 = 22.** ✔

> **Never read synthetic-seeded passes as real-world accuracy.** The manifest `synthetic=true` + downstream scoreboard split keep them distinguishable; the Δλ discriminator is **empirical-anecdotal** (C3-PRE §7) and must be confirmed against real vehicle data before it is trusted as a live win.

## Provenance / guardrails

- Side file only: no write to `cases_petrol_v7.csv` / `corpus_curated.csv`, no engine/lab/registry/rule edit, no re-score, no yardstick mint, no abstain-dial change. Writes only under `v3/`. `Vault/` untouched. No `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
- Inputs: corpus `expected_fault_code` (oracle) for the pinned 22 `C3_CASES` + the web-validated band table. Producer thresholds cited to `v3/research/research_answers/cluster3_prepped.md` and `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.md`. Governs `T-V3-P4-C3A` / `C3B`.
