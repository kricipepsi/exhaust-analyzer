---
node_type: "wiki"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "fuel-trim-reasoning"
implements:
  - "labs/obdlab/code/core/trim_vector_aggregator.py"
consumers:
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py — Total Fuel Trim evaluation"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py — OBD payload intake"
drift_guards:
  - "labs/obdlab/tests/unit/test_trim_vector_aggregator.py"
tags: [obdlab, finished, wiki]
source: "labs/obdlab/research/chunks/fuel-trim/README.md"
---
# chunks/fuel-trim/ — index & disposition ledger


**Date:** 2026-06-07 · **Step:** Phase 2 (chunking), folder 1 of 6 per
SWEEP_MANIFEST §4.5 order. **Updated 2026-06-07 (pass 2):** expanded from 8
fundamentals chunks to **15** after the owner flagged that the original set did
not cover the diagnostic possibilities of fuel trim. The previously-deferred
"Across Fault Families" report is now readable (`FuelTrimFamilies.md`, gate
passed) and `Fuel Trim Diagnostics.txt` is now properly chunked (was only
dedup-folded). Forward-progress ideas are marked **PROPOSAL** per root
`CLAUDE.md` → "Progress the app forward".

## Chunk set

### Fundamentals (pass 1 — how to read trims)

| Chunk | Concept | Primary consumer | Status |
|---|---|---|---|
| `01_stft-ltft-fundamentals` | STFT/LTFT, `total_trim = STFT+LTFT` | COMLab trim analytics → fault-atlas A&F-metering | active |
| `02_sign-convention` | +lean / −rich, J1979 sign | COMLab truth-vs-perception (sign = compare key) | active |
| `03_normal-ranges-and-dtc-thresholds` | healthy bands, ±18/±25 DTC, ±127 sentinel | fault-atlas P0171/2/4/5 routing | active |
| `04_trim-pattern-decision-tree` | idle-vs-RPM pattern → root cause | fault-atlas routing (static); delta part PENDING | active + PENDING |
| `05_bank-to-bank-comparison` | common-mode vs bank-specific | T-OBDV2-BANK-ASYM-1 → COMLab T-COMV2-BANK-FUSE-1 | active (gated T-OBDV2-0=revive) |
| `06_trim-rails-and-sentinels` | ±25/±127, frozen, reset | COMLab trim-validity gating | active |
| `07_trim-vs-gas-chemistry-crosscheck` | λ vs trim contradiction table | COMLab truth-vs-perception override (PRD §5) | active |
| `08_validity-preconditions` | ECT/CL/DFCO/WOT gate, `fuel_trim_invalid` | COMLab `fuel_trim_invalid` gate | active |

### Diagnostic evidence base + extensions (pass 2 — the missing coverage)

| Chunk | Concept | Primary consumer | Status |
|---|---|---|---|
| `09_fault-family-case-matrix` | 20 real cases, idle/2500RPM discriminator matrix | fault_atlas_router + global_fault_registry cross_domain_matrix | MIXED (14 active, 6 proposal) |
| `10_air-fuel-metering-injector-cases` | P01xx/P02xx mechanisms (cases 1–9) | lean/rich/sensor/misfire families | MIXED (+3 proposals) |
| `11_ignition-misfire-cases-and-trim-discriminator` | P03xx (cases 10–14) + misfire-vs-fuelling split | misfire/ignition families + pre-route discriminator | MIXED (+3 proposals) |
| `12_emissions-egr-evap-catalyst-idle-module-cases` | P04xx/05xx/06xx (cases 15–20) | catalyst/rich/lean/ecu families | MIXED (+1 proposal) |
| `13_ltft-load-cell-matrix` | per-cell LTFT (MAF×RPM) localisation | **PROPOSAL** — COMLab load-cell trim analyzer | PROPOSAL |
| `14_dtc-enable-criteria-and-blocking-codes` | P0171/4 run envelope + prerequisite-DTC gate | analytics_preconditions / TrimAnalyticsGate | MIXED (+1 proposal) |
| `15_pcm-memory-freezeframe-verification` | KAM persistence, Active/History/auto-erase, freeze-frame | TrimAnalyticsGate.CODES_RECENTLY_CLEARED + freeze_frame_pids | active + method |

## Forward-progress PROPOSALS (register in comlab/config/proposals/)

New diagnostic expressions found in the docs that v2 does not yet have. Each names
its consumer; field + consumer ship together (root `CLAUDE.md`). To be landed via
task spec **FT-FU-B**.

| Proposal | From | Consumer / code path |
|---|---|---|
| `maf_circuit_ground_open_failsafe` | case 3 | fault_atlas sensor_fault, keyed (P0102 + negative both-bank trim → speed-density failsafe rich) |
| `thermostat_stuck_open_closedloop_delay` | case 6 | analytics_preconditions (ENGINE_COLD persistence) + fault_atlas |
| `injector_thermal_intermittent` | case 9 | fault_atlas (cold-only single-bank +STFT that normalises warm) |
| `fuel_water_contamination` | case 10 | fault_atlas (P0300 + positive trim + random multi-misfire, normal compression/spark) |
| `alternator_ac_ripple_sensor_corruption` | case 14 | fault_atlas charging_system + CMP/CKP-noise route |
| `egr_insufficient_flow` | case 15 | fault_atlas EGR (commanded-EGR vs observed-STFT-response; inverse of ERR-LC-005) |
| `misfire_vs_fuelling` pre-route gate | Fuel Trim Diagnostics.txt | fault_atlas candidate-pruning (P030x + single-bank trim ≤ +15 % → misfire family first) |
| `ltft_cell_vector` + load-cell analyzer | chunk 13 | COMLab load-cell trim analyzer (idle-only / part-throttle-only / global localisation) |
| `prerequisite_dtc_gate` | chunk 14 | analytics_preconditions reading dtc_lab_output; suppress trim routing when a listed MAF/MAP/IAT/ECT/TPS/CKP/coil DTC is active |
| `fuel_delivery_restriction` split | case 2 | refine ERR-LC-003: current-normal + pressure-drop-under-load discriminates filter restriction from pump |

## Source disposition (current 5 sources)

| Source | Disposition | Where |
|---|---|---|
| `master_fuel_trim_guide.md` | **Spine — fully chunked** (pass 1) | §1→01, §2→02, §3→03, §4→04, §5→05, §6→06, §7→07, §8–9→08 |
| `FuelTrimFamilies.md` (42 KB, gate passed) | **Fully chunked (pass 2)** — 20 cases + control theory + memory logic | →09 (matrix), →10/11/12 (family detail), →15 (memory). OBD-I/II scale-conversion paragraph routes to **pids-protocol** (DR-FU-1). 8-step protocol + sensor bench-benchmark table = guided-pinpoint-test PROPOSAL candidate (FT-FU-C), not chunked. |
| `Fuel Trim Diagnostics.txt` (4.5 KW) | **Chunked (pass 2)** — was only dedup-folded in pass 1 | →11 (misfire-vs-fuelling, false-lean), →13 (LTFT cell matrix), →14 (DTC run envelope, prerequisite codes), →15 (KAM persistence, Field Service Mode) |
| `Research10.md` | **Partially folded** — §1 magnitudes + §2 sentinel are fuel-trim | →03, →04, →06. §3–§7 (O₂/VE/λ) belong to o2-logic & pids-protocol |
| `FuelTrimW.md` | **Deferred to delta-relations** — primary ΔTrim feeder | → `chunks/delta-relations/` (already extracted, consumer PENDING FU-2) |

> Note on pass-1 drops: the original sweep listed 11 fuel-trim sources and dropped/
> folded several REF docs (Ross-Tech, Eastern Manufacturing, `Short Term Long Term
> Fuel Trim Explained.md`, etc.). Those files are no longer in `sources/fuel-trim/`
> (folder was consolidated to the 5 above). The unique *routable* content the owner
> missed lived in the "Across Fault Families" report — now captured via
> `FuelTrimFamilies.md` (chunks 09–12, 15) — and in `Fuel Trim Diagnostics.txt`
> (chunks 11, 13, 14, 15).

## Anti-orphan verification (2026-06-07 pass 2)

- `fault_atlas_router` / `global_fault_registry.json` — 14 of 20 cases map to
  existing nodes (ERR-LC-001/003, ERR-SF-004/005, ERR-MF-004/005/006, ERR-IF-003,
  ERR-RM-004, ERR-CF-001, ERR-ECU-001); verified present in `comlab/config/kg/*`.
- `analytics_preconditions.py` / `TrimAnalyticsGate` — live trim-validity gate
  (ENGINE_COLD/OPEN_LOOP/WOT_ACTIVE/DFCO_ACTIVE/CODES_RECENTLY_CLEARED) consumes
  chunks 14/15.
- 6 case mechanisms + 4 concept ideas have **no** live node/consumer → marked
  PROPOSAL above (not orphans: each names a proposed consumer + code path), to land
  via FT-FU-B. No chunk ships an orphan field.

## Unplanned follow-ups

| ID | Item | Why deferred |
|---|---|---|
| FT-FU-B | **Author task spec(s) to land the 10 fuel-trim proposals** (table above) — register nodes/fields in `comlab/config/proposals/`, name each consumer + code path, pin thresholds. | Architect task next session; coder implements. One-task-per-session. |
| FT-FU-C | **Guided pinpoint-test feature** from FuelTrimFamilies.md sensor-calibration benchmarks (MAF/MAP/ECT/injector/coil/O₂-heater/alternator test values) + 8-step protocol. A forward-progress UX proposal — component bench specs, no current OBD/gas consumer. | Needs an owner call on whether guided component testing is in v2 scope. |
| FT-FU-A | (pass 1, still open) Whether long-form mechanics docs earn verbatim chunks — now moot: those REF files were removed from `sources/`; no unique routable fact was lost. | Superseded — close unless owner reinstates the docs. |

---

## Volume-sweep addition (2026-06-07 — sources/various/)

| Chunk | Concept | Consumer | Status |
|---|---|---|---|
| `16_three-speed-trim-test` | idle/2500/cruise trim sweep; MAF "double-whammy" rich-idle/lean-load signature | COMLab delta engine + fault_atlas | active (idle/2500) + PENDING (load axis, FU-2) |

## Proposal-audit addition (2026-06-08 — PROPOSAL_AUDIT_v2_boost.md)

| Chunk | Concept | Consumer | Status |
|---|---|---|---|
| `17_per-cylinder-misfire-counts` | per-cyl misfire counts (Mode 06, 200/1000-rev); single-cyl vs global; >1 % catalyst boundary | fault_atlas misfire localiser + EP-COM-07 gate (EP-OBD-IN-07, OBD-owned) | PROPOSAL (CAN-era) |

Source: Vol2 Master Document 3 + Vol3 PID-without-DTC profiling. Complements
fuel-trim/04 (static idle-vs-2500) and delta-relations (ΔTrim). Vol3 total-trim display
equation stripped — it is the standard `total=STFT+LTFT` already in fuel-trim/01.


## Core Entities

- fuel-trim (17 chunks; 10 forward-progress proposals)
- STFT, LTFT, TOTAL_TRIM, TrimAnalyticsGate, fault_atlas_router
- COMLab trim analytics + fault_atlas_router + global_fault_registry.json

## Graph relations (explicit)

**fuel-trim** FEEDS **COMLab trim analytics** and **fault_atlas_router**
**fuel-trim** CALIBRATES **global_fault_registry.json** cross_domain_matrix
**fuel-trim proposals** REGISTERED_IN **comlab/config/proposals/** (FT-FU-B)

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
