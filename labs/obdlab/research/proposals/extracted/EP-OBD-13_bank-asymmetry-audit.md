---
proposal_id: EP-OBD-13
title: Asymmetric bank trim audit (Total B1 vs Total B2 ≥ 20 % divergence)
target_lab: OBDLab (core/trim_vector_aggregator.py) → COMLab
source: proposals/OBD_ImplProp.md §2.B; chunks/ecu-diagnosis/07; chunks/fuel-trim/05
type: analytics_module
status: PROPOSAL (field exists, consumer missing — orphan to close)
date_extracted: 2026-06-07
---

## What it proposes
Aggregate Total Trim per bank (`STFT_Bn + LTFT_Bn`) and emit the B1–B2 divergence. On a
declared dual-bank engine (`number_of_banks == 2`), |Total B1 − Total B2| ≥ 20 %
isolates a bank-specific hardware fault:
- Injector driver failed **open** (B1): B1 ≈ +50 %, B2 normal.
- Injector driver **shorted** (B1): B1 ≈ −50 %, B2 normal.

## Diagnostic rationale
Bank symmetry vs asymmetry is the **strongest internal-vs-external ECU tell** (chunk 07
§2). `total_trim_correction_delta_b2` is **emitted by OBDLab but read nowhere in COMLab
non-test code** — an orphan field. This adds the consumer (do not add a field).

## Proposed consumer + code path
COMLab ECU-hardware-fault checker ([[EP-COM-04_ecu-hardware-fault-checker]]) or a shared
B1/B2-divergence helper reading `total_trim_correction_delta` / `_b2` in
`fault_atlas_router.py`. Closes ECU-FU-2.

## Dependencies / related
[[EP-ECU-02_injector-driver-fault]] · [[EP-COM-04_ecu-hardware-fault-checker]].
