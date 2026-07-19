---
chunk: pids-protocol/04_gdi-highpressure-fuel-pids
topic: pids-protocol
sources:
  - various/Vol2.md — Master Document 5 (GDI High-Pressure Fuel); various/Vol4.md GDI cases (FRP drift, HPFP)
consumer: COMLab fault_atlas fuel-delivery (GDI branch) — desired-vs-actual rail pressure + VCV duty isolate HPFP/lift-pump faults (P0087/P0088) the trim logic alone mis-attributes.
consumer_status: PROPOSAL (GDI rail-pressure PIDs + VCV duty not yet input fields; names producer OBDLab + reader COMLab)
provenance: sources/various/Vol2.md MD5 + Vol4 — concepts READABLE; pressure spec numbers partly stripped in MD5 table (flagged in formula wiki)
dedup: new; relates to EP-CAT/EP-FA fuel-restriction split (proposals/extracted EP-FA-07)
---

# GDI high-pressure fuel diagnostics

GDI uses dual-stage delivery: in-tank lift pump → cam-driven HPFP → rail (>2000 psi).
Diagnosis centres on two PIDs and one actuator duty.

## Parameters (Vol2 MD5 / Vol4, readable)

- **Fuel Rail Pressure Desired vs Actual:** a large desired-minus-actual delta =
  HPFP or control-solenoid failure (P0087 too-low). Pressure that drops only at high
  RPM = worn cam drive lobe.
- **VCV (Volume Control Valve) duty cycle:** jumps from idle baseline to high %
  when actual struggles to meet desired → over-compensating for internal pump leak or
  weak lift pump.
- **Leak-down (hot shutdown):** rapid pressure drop = leaking GDI injectors or pump
  seals.
- **GDI HPFP internal seal failure (Vol4 N-013):** fuel enters crankcase oil; trims
  −30 %, λ_chem≈0.88 rich — fuel arrives via PCV vapour, not injector pulse (an L4
  source-attribution case, truth-perception/03).

## Consumer / code path
OBDLab emits `frp_desired`, `frp_actual`, `vcv_duty`; COMLab fault_atlas GDI fuel
branch reads the desired-vs-actual delta + VCV duty. Fields earn their place via this
named consumer only.


## Core Entities

- frp_desired, frp_actual, vcv_duty, P0087, HPFP
- fault_atlas GDI fuel branch (PROPOSAL)

## Graph relations (explicit)

large **frp_desired** minus **frp_actual** INDICATES HPFP fault (**P0087**)
**vcv_duty** high INDICATES internal pump leak or weak lift pump
**frp_desired**, **frp_actual**, **vcv_duty** EMITTED_BY OBDLab and CONSUMED_BY **fault_atlas GDI fuel branch**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
