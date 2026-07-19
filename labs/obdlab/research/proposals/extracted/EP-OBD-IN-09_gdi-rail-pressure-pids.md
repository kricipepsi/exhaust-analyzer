---
proposal_id: EP-OBD-IN-09
title: Add GDI high-pressure fuel PIDs (FRP desired/actual, VCV duty) as input fields
target_lab: OBDLab (input) → COMLab fault_atlas (GDI fuel branch)
source: various/Vol2.md MD5; various/Vol4.md GDI cases; chunks/pids-protocol/04
type: input_field
status: PROPOSAL (consumer proposed; field gap)
date_extracted: 2026-06-07
sweep: sources/various volume sweep
---

## What it proposes
Ingest `fuel_rail_pressure_desired`, `fuel_rail_pressure_actual`, and `vcv_duty_pct` for
GDI engines. Desired-minus-actual delta + VCV duty isolate HPFP / lift-pump faults
(P0087/P0088) the trim logic mis-attributes to mixture.

## Diagnostic rationale
Pressure that drops only at high RPM = worn cam drive lobe; VCV duty climbing from idle
baseline = compensation for internal pump leak. GDI HPFP seal failure (Vol4 N-013) leaks
fuel into oil → rich λ_chem via PCV, not injector pulse.

## Proposed consumer + code path
COMLab `fault_atlas_router` GDI fuel branch reads the FRP delta + VCV duty. Fields earn
their place via this named consumer only (signal/noise).

## Dependencies / related
[[EP-FA-07_fuel-restriction-split]] · chunks/pids-protocol/04 · DNALab GDI flag ([[EP-DNA-02_slim-dna-views]]).
