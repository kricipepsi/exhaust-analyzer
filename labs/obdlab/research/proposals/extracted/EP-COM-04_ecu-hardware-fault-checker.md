---
proposal_id: EP-COM-04
title: ECU-hardware-fault checker (the named consumer for all internal-ECU fault nodes)
target_lab: COMLab/OBDLab (new checker)
source: proposals/OBD_ImplProp.md §3; chunks/ecu-diagnosis/* ; SWEEP_MANIFEST ECU-FU-1
type: analytics_module
status: PROPOSAL (this is the consumer that unblocks EP-ECU-01..07)
date_extracted: 2026-06-07
---

## What it proposes
A dedicated checker that detects internal solid-state ECU failures the existing bias
detector deliberately suppresses (its Lambda-Truth guard 0.90/1.10 mutes the abnormal
λ 0.72–1.55 these modes produce). Defines ≥5 new fault-atlas node ids and the
discriminator logic from Tables 1–3 (symmetry, deceptive λ, digital-vs-physical).

## Diagnostic rationale
v1 cannot detect internal ECU hardware failure at all; this is precisely the class v2
exists to add. The checker reads the typed boundary inputs and routes to the new nodes.

## Proposed consumer + code path
New `comlab/core/ecu_hardware_checker.py` (or OBDLab forensic stage) reading
`calculated_engine_load_pct`, `shrtft*/longft*`, `total_trim_correction_delta(_b2)`,
`map_kpa`, `coolant_temp_c`, `mass_airflow_gps`, plus proposed TPS/IAT and the 5-gas λ.
Registers nodes in `comlab/config/proposals/` (ECU-FU-1).

## Dependencies / related
Consumes: [[EP-ECU-01_capacitor-leakage]] [[EP-ECU-02_injector-driver-fault]]
[[EP-ECU-03_coil-driver-failure]] [[EP-ECU-04_sensor-ground-trace-blown]]
[[EP-ECU-05_5v-regulator-collapse]] [[EP-ECU-06_adc-mux-failure]] [[EP-ECU-07_eprom-bitflip]].
Needs: [[EP-OBD-13_bank-asymmetry-audit]] · [[EP-GAS-01_5gas-brettschneider-schema]].
