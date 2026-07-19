---
node_type: prd
lab: vinlab
module: vinlab
subsystem: requirements
implements: []
consumers:
  - "hld: labs/vinlab/docs/HLD_VINLab.md"
  - "dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (VehicleDNA Part-A producer contract)"
drift_guards: []
tags: [vinlab, prd, requirements]
source: "labs/vinlab/docs/PRD_VINLab.md"
---

# PRD — VINLab
**Status:** Approved
**Version:** 2.1
**Date:** 2026-06-12
**Scope:** Petrol-only, v2 — VIN-decode module (Part A physical DNA producer)

---

## Section 1 — Summary

VINLab is the **vehicle-identity channel** of the 4D petrol diagnostic pipeline. It
accepts a 17-character VIN and decodes it — fully offline, with zero network and zero
MySQL at runtime — into a typed `VinDNA` dataclass: the **physical DNA** of the
vehicle (make, displacement, cylinder count, banks, induction, fuel delivery, air
metering, emissions equipment, era, plus per-engine-code CoC emission targets). The
single public entry point is `vinlab.decode(vin) → VinDNA`.

VINLab is one of the three sibling labs of the **DNA family** (`vinlab` + `symptomlab`
→ `dnalab`). Its `VinDNA` is Part A; SymptomLab supplies Part B; DNALab composes both
into `VehicleDNA`. `VinDNA`'s shape is governed by `SEMANTIC_CONTRACT.md §4.1` — that
contract wins over all other documents.

VINLab is a **producer, not a judge.** It emits a decoded profile; it does not rank
faults or render verdicts. Its consumers live downstream in **COMLab** (which projects
`VinDNA` into per-lab DNA views) and through them in **OBDLab** and **GASLab**. The
symptom/identity channel is the cheapest independent prior, and the identity half of
that prior is what VINLab produces.

---

## Section 2 — Contacts

| Name | Role | Responsibility |
|------|------|----------------|
| VINLab Owner | Module Owner | VIN structural validation, WMI/year/engine resolution, overlay rules, CoC overlay, confidence grading |
| COMLab Team | Integration Consumer | Mirrors `VinDNA` locally; projects it into `ObdLabDnaView` / `DtcLabDnaView` / `lab_dna_views`; reads `rated_rpm`, `air_metering_strategy`, `stress_idle_rpm_target`, `confidence`, CoC targets |
| OBDLab Owner | Indirect Consumer | Reads the projected DNA view: `rated_rpm` (RPM ceiling), `air_metering_strategy` (VE routing), `upstream_o2_type`, `induction_type`, `confidence` |
| GASLab Owner | Indirect Consumer | Reads CoC emission targets (lambda/CO/HC thresholds) via the projector |
| 4DApp Engineering Lead | Architecture | Signal/noise rule; cross-lab JSON contract; offline-runtime constraint; SQL-isolation (H8) |

---

## Section 3 — Background

**Context.** The 17-character VIN (ISO 3779 / SAE J853 / NHTSA 49 CFR Part 565) encodes
the World Manufacturer Identifier (positions 1–3), the Vehicle Descriptor Section
(positions 4–9), and the Vehicle Identifier Section (positions 10–17, with the model
year at position 10). Decoding a VIN to a usable engine profile is not a pure
character lookup: European-market VINs frequently omit the NHTSA check digit, the
year code `L` collides between 1990 and 2020, low-volume manufacturers (SAE J853,
`vin[2] == '9'`) place their identifier at positions 12–13, and many engine attributes
must be resolved from a reference database keyed by engine code rather than from the
VIN string itself.

**Why now.** The 4D engine needs a vehicle profile to *filter* the diagnosis — to hide
bank-2 inputs on an inline engine, suppress turbo-boost fields on a naturally-aspirated
car, and pin the per-engine-code emission targets that GASLab compares chemistry
against. The decode must run on the technician's device with no connectivity, so all
reference data (`wmi.csv`, `years.csv`, `vds_engine_map.csv`, `vref.db`) is baked into
`vinlab/data/` at build time and the runtime is network-free and MySQL-free.

**What recently became possible (v2 sibling split, T-RM-2-DNA, 2026-06-06).** VINLab
was forked from v1 `DNALab/VINLab/` into an **independent module** with its own
`pyproject.toml`, own folder, and the no-cross-lab-import boundary. Enum-typed fields
replaced bare `str` annotations (ADR-0004 / T-FX-5). The single-deep-module
air-metering classifier (T-FX-2) replaced two parallel switches. A last-resort
cylinder-count heuristic (T-VL-7) was added behind a `cylinder_count == 0` gate so it
can never overwrite real data. The CoC emission targets were overlaid from petrol CSV
medians keyed by engine code.

---

## Section 4 — Objective

**Business benefit.** Provide a typed, confidence-graded vehicle profile at decode time
so every downstream lab can tailor its analysis to the exact hardware on the car —
without embedded per-vehicle lookup tables in each lab.

**Customer benefit.** The technician scans or types a VIN once; the app instantly knows
the engine architecture and emission targets and shows only the inputs that matter for
that specific vehicle.

**Key Results:**

- **KR1:** `decode()` runs with zero network and zero MySQL on every call (offline
  constraint; data baked into `vinlab/data/`).
- **KR2:** Out-of-scope vehicles are rejected at decode: non-petrol (H1) and model year
  outside 1990–2020 (H2) raise `VINDecodeError`.
- **KR3:** Inputs that are not 17 characters raise `ChassisNumberError` (a
  `VINDecodeError` subclass) so callers can route legacy chassis numbers separately.
- **KR4:** Every decode returns a `VinConfidence` grade (`HIGH` / `PARTIAL` / `NONE`)
  reflecting how much of the profile was resolved from authoritative data.
- **KR5:** Zero cross-lab Python imports (DNA-family boundary; COMLab mirrors `VinDNA`).
- **KR6:** Every numeric literal in `vinlab/` carries a wiki/standard citation comment.
- **KR7:** All SQL lives in `db/tecdoc_query.py` (H8 SQL-isolation); no other module
  writes SQL.

---

## Section 5 — Market Segment

**Advanced workshop technician (petrol, 1990–2020 fleet):** Professionals diagnosing
European and Asian petrol vehicles where the VIN is the fastest route to engine
architecture and emission targets, and where connectivity on the shop floor is not
guaranteed. They need a decode that degrades gracefully (PARTIAL/NONE confidence)
rather than failing when reference data is incomplete.

---

## Section 6 — Value Proposition

- **Jobs addressed:** VIN structural validation (charset, length, checksum), WMI →
  brand/country resolution, model-year disambiguation, two-path engine resolution,
  emission-equipment derivation, air-metering classification, stress-idle-RPM
  targeting, cylinder-count inference (fallback), CoC emission-target overlay, and
  confidence grading.
- **Gains created:** one `decode()` call yields a fully typed `VinDNA`; downstream labs
  read enum fields, not raw strings. Air metering is classified once into both a
  developer label (`primary_load_calculation`) and the OBDLab-canonical
  `air_metering_strategy`. The CoC overlay attaches per-engine-code lambda/CO/HC
  targets so GASLab has a ground-truth reference without its own database.
- **Pains relieved:** European VINs without a check digit still decode (data-driven
  bypass via `wmi.csv` country). The `L`-year 1990/2020 collision is resolved by WMI
  `era_hint`. Pre-VIN chassis numbers are distinguished from decode failures. A missing
  reference row downgrades confidence instead of crashing.
- **Competitive advantage:** the decode is fully offline; the heuristics are
  brand-aware (per-manufacturer cylinder rules) yet gated so they never overwrite
  authoritative CSV/DB data; the output is a frozen, contract-governed dataclass that
  every other lab can rely on.

---

## Section 7 — Solution

### Key Features (all P0)

- P0: **Structural validation** — `pre_clean_vin` (I→1, O→0 per SAE J853), 17-char
  length guard (`ChassisNumberError`), charset pattern `[A-HJ-NPR-Z0-9]{17}`, and
  NHTSA modulo-11 checksum with three documented bypass paths.
- P0: **WMI resolution** — standard positions 1–3, plus the SAE J853 low-volume rule
  (`vin[2] == '9'` → try the 6-char extended WMI `vin[0:3]+vin[11:14]` first).
- P0: **Year resolution** — `vin[9]` lookup, passthrough characters (`0`, `U`, `Z`) →
  `model_year = None`, and `L`-year disambiguation (1990 vs 2020) via WMI `era_hint`.
- P0: **Scope guards** — H1 petrol-only (keyword scan of CSV `fuel_system_type` and
  `vref.db` `fuel_delivery_type`), H2 model year ∈ [1990, 2020].
- P0: **Two-path engine resolution** — Path A `vds_full` (`vin[3:8]`), Path B
  `pos_8_only` (`vin[7]`) fallback, keyed by brand.
- P0: **vref.db tech-mask + CoC overlay** — `lookup_engine_ref()` (read-only SQLite)
  fetches induction, fuel delivery, MAF/MAP presence, euro norm, O2 type, EGR, and the
  13 CoC/type-approval/noise measurements.
- P0: **Overlay rules** — air-metering classification, euro→horizon mapping,
  stress-idle-RPM targeting, upstream-O2 derivation, cylinder-count fallback.
- P0: **Confidence grading** — `NONE` (engine not in CSV), `PARTIAL` (any downgrade
  flag), `HIGH` (clean resolve).
- P0: **`VinDNA` output dataclass** (frozen) with `to_json()` / `from_json()`.

### Technology

- Python 3.14. Standard library only at runtime (`csv`, `re`, `sqlite3`, `pathlib`) plus
  PyYAML for tooling; no network, no MySQL. Package `vinlab`, standalone
  `pyproject.toml`.
- Entry point: `vinlab.decode(vin, *, data_dir=None) → VinDNA`. The decoder is
  `lru_cache`d per `data_dir`, loading `wmi.csv`, `years.csv`, `vds_engine_map.csv`
  into memory once and opening `vref.db` read-only.
- Exceptions: `VINDecodeError(ValueError)` and `ChassisNumberError(VINDecodeError)`.
- No cross-lab imports — COMLab mirrors `VinDNA` locally.

### `VinDNA` fields (16 core + 13 CoC overlay)

| # | Field | Type | Source | contract cite |
|---|-------|------|--------|---------------|
| 1 | `vin` | `str` | caller (cleaned) | §4.1 |
| 2 | `make` | `str` | `wmi.csv` brand | §4.1 |
| 3 | `model_year` | `int \| None` | `vin[9]` + `years.csv` | §4.1 |
| 4 | `engine_displacement_liters` | `float` | `vref.db displacement_cc` / CSV | §4.1 |
| 5 | `cylinder_count` | `int` | CSV / `vref.db` / heuristic fallback | §4.1 |
| 6 | `number_of_banks` | `int` | `is_v_engine` / config prefix | §4.1 |
| 7 | `induction_type` | `InductionType` | `vref.db` / heuristic | §4.1, §6.1 |
| 8 | `fuel_delivery_type` | `FuelDeliveryType` | `vref.db` / CSV | §4.1 |
| 9 | `air_metering_architecture` | `AirMeteringArchitecture` | classifier | §4.1, §6.2 |
| 10 | `emissions` | `Emissions` | `vref.db` + year rule | §4.1 |
| 11 | `euro_emission_category` | `EuroEmissionCategory` | `vref.db euro_norm` | §4.1, §6.4 |
| 12 | `resolved_horizon` | `Horizon` | `euro_to_horizon()` | §4.1, §6.4 |
| 13 | `stress_idle_rpm_target` | `int` | `stress_idle_rpm()` | §4.1, §6.5 |
| 14 | `rated_rpm` | `int \| None` | `vehicles_petrol_specimens.csv` `P14_rated_rpm` (T-DNA-3) | §4.1, §6.5 |
| 15 | `confidence` | `VinConfidence` | decode flags | §4.1 |
| 16 | `air_metering_strategy` | `AirMeteringStrategy` | classifier | §6.2 |
| 17–29 | CoC overlay (13 fields) | `float\|int \| None` | `vref.db` per engine code | (see §8 note) |

The 13 CoC overlay fields are `target_lambda_v112`, `target_rpm_u2`, `idle_rpm_low`,
`co_low_idle`, `co_high_idle`, `co_type_approval`, `hc_type_approval`,
`nox_type_approval`, `hc_nox_type_approval`, `co2_type_approval`,
`noise_stationary_dba`, `noise_rpm`, `noise_driving_dba`.

### Assumptions

| Assumption | Validation |
|-----------|-----------|
| `vref.db` (small SQLite) is the runtime reference; `mysql_data/` (~484 MB) is build-time only | tests skip when `vref.db` absent; `mysql_data/` flagged for Track-2 removal |
| European / Japanese / Korean / Indian VINs may legitimately lack a NHTSA check digit | data-driven bypass via `wmi.csv` `country` |
| The cylinder-count heuristic is a last resort | gated on `cylinder_count == 0`; never overwrites CSV/DB data |
| `VinDNA` shape is contract-owned (`SEMANTIC_CONTRACT.md §4.1`) | enum-typed fields; `from_json` raises `KeyError` on missing required keys |

---

## Section 8 — Release

### v2 Scope

All P0 features above, as shipped after the sibling split (T-RM-2-DNA), the enum-field
cut-over (T-FX-5), the air-metering single-module rework (T-FX-2), and the
cylinder-heuristic fallback (T-VL-7). The CoC overlay is populated from per-engine-code
petrol CSV medians.

### Landed (DNA-family pack — see `labs/dnalab/tasks/PROGRESS.md`)

These tasks are **done**; their dispositions are now shipped behaviour:

- **T-DNA-3 — emit `rated_rpm` (done).** `VinDNA` now emits `rated_rpm` (`int | None`,
  source `DBS/docs/vehicles_petrol_specimens.csv` `P14_rated_rpm`). COMLab's projector
  (`projection.py` → `ObdLabDnaView.rated_rpm`) already reads it as the OBDLab RPM
  ceiling — producer and consumer are now matched.
- **T-DNA-4 — formalize CoC fields + reconcile emissions (VINLab side done).** The CoC
  fields are formalized **top-level** on `VinDNA`; the emissions block is formalized as
  `{upstream_o2_type, downstream_o2_present, downstream_trim_role, has_catalyst,
  egr_equipped}` with `secondary_air_equipped` dropped (no consumer). The projector
  still reads CoC under `emissions{}` → the remaining fix is the paired **COMLab-C** path
  change at Stage 4 (not a VINLab change).
- **T-DNA-5 — `model` disposition (DNA10 Q8) — kept-empty.** No `VinDNA.model` field:
  the DBS specimen file has no repeated engine-code groups, so there is no within-code
  CoC variance to justify the field. DTCLab's mirror relaxation is registered as
  COMLab-D.
- **T-DNA-6 — `fuel_type` proposal (+ `altitude_band` note) — proposal-only.**
  `fuel_type` is registered as **proposal** COMLab-E (future `GasLabDnaView`, E5/E10
  blend-correction context); it is **not** a live `VinDNA` field. `altitude_band` stays
  session/context metadata (lambda math is altitude-invariant), not a schema field.

### Explicitly Deferred

- `mysql_data/` (~484 MB) verbatim copy — Track-2 cleanup candidate; not used at runtime.
- `hc_nox_type_approval` and the three noise fields are not part of the confidence-flag
  CoC-null check (only nine CoC fields downgrade confidence).

### Success Criteria

1. KR1–KR7 all hold.
2. Offline decode produces a valid `VinDNA` for every in-scope fixture VIN.
3. Out-of-scope (non-petrol, year ∉ [1990, 2020], wrong length) raises the correct
   exception subclass.
4. No cross-lab Python imports.
5. Every numeric literal carries a citation; all SQL confined to `db/tecdoc_query.py`.
