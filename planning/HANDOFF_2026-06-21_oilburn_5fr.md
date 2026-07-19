# HANDOFF — Oil-Burn 5FR Presentation (2026-06-21)

**Goal:** present the wiredV2 diagnostic on one vehicle across 5 oil-burn cases, traced in Jaeger.

## The vehicle (settled)
- VIN **`VF7SA5FR8AW511081`** → Citroën, engine **5FR / EP6CDT**, 1.6 L I4, **turbo + GDI**, EURO 5.
- Sensors: **wideband upstream (λ) + narrowband downstream (voltage + post-cat B1S2 fuel trim)**, Bosch MED17.4.

## What's DONE
- VIN data-quality audit (4 defects): `planning/AUDIT_2026-06-21_vin_engine_resolution.md`.
- Coder specs: `labs/vinlab/tasks/T-VIN-FIX-1/2/3` (brand-join + vref equip + decoder integrity).
- 5-case signatures (gas + OBD incl. B1S2): `planning/OIL_CASE_SIGNATURES_5FR.md`.
- Standalone simulation (5/5 green) + OTLP→Jaeger tracing: `planning/sim/oil_burn_5fr_sim.py`,
  runner `run_sim_traced.ps1`, runbook `JAEGER_DEMO_README.md`, results `OIL_BURN_5FR_SIM_RESULTS.md`.
- Post-cat-trim real-build roadmap (10 tasks): `planning/post_cat_trim/POST_CAT_TRIM_START_HERE.md` + `PROGRESS.md`.
- Run task: `planning/sim/T-SIM-1_run_oil_cases.md` (full sequence; assign to coder).
- Jaeger v2 installed & running (native, no Docker), UI http://localhost:16686, OTLP 4317.

## Demand ranking (pick the presentation case)
1= **PCV MW-008** (4.0) — divergent split trim · 1= **Turbo MW-009** (4.0) — DFCO-decoupled trim
3 Rings MW-001 (3.5) · 4 Valve seals MW-002 (2.0) · 5 Head gasket MW-003 (1.0).
Lean: **Turbo MW-009** (looks healthy on gas, only post-cat trim reveals it).

## PENDING / blockers
- **T-VIN-FIX-3** (decoder) must land before the REAL `run_case.py` decodes the VIN end-to-end.
  (Simulation needs none of this — it runs today.)
- Confirm 5FR upstream is wideband (it is, per research) → `vref.db o2_type='NB'` fix is in T-VIN-FIX-2/PCT-4.

## NEXT SESSION — to do
1. Run **T-SIM-1** (coder): start Jaeger → run sim traced → capture `RUN_RESULTS_<date>.md` → confirm 5 traces.
2. **Analyse** the run + traces; **pick one case** (turbo or PCV).
3. Write the **final report**: vehicle/engine ID → per-case signatures → chosen-case trace walkthrough → verdict, + status of T-VIN-FIX-3 and the PCT roadmap. (Destined for Claude design.)

## Run commands
```powershell
cd C:\Workspace
.\planning\sim\run_sim_traced.ps1     # sim → Jaeger, opens UI (service: wiredv2-oil-case)
```
