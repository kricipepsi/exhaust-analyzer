---
node_type: "hld"
lab: "vinlab"
module: "vinlab"
subsystem: "architecture"
implements: []
consumers:
  - "lld: labs/vinlab/docs/LLD_VINLab.md"
  - "dld: labs/vinlab/docs/DLD_VINLab.md"
  - "dnalab: labs/dnalab/dnalab/assembly.py decode_vin_payload() integration"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py (VinDNA integration)"
drift_guards: []
tags: [vinlab, finished, hld]
source: "labs/vinlab/docs/HLD_VINLab.md"
---
# HLD — VINLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_VINLab v2.0
**Version:** 2.1
**Date:** 2026-06-12

> **Audit note (2026-06-11; refreshed 2026-06-12):** this document is grounded in the
> live `vinlab/` package after the sibling split (T-RM-2-DNA), the enum-field cut-over
> (T-FX-5), the air-metering single-module rework (T-FX-2), and the cylinder-heuristic
> fallback (T-VL-7). Every field, enum, threshold, and code path below is transcribed
> from the shipped source, not from design intent. The DNA-pack data-flow tasks
> (T-DNA-3 `rated_rpm`, T-DNA-4 CoC/emissions, T-DNA-5 `model`, T-DNA-6 `fuel_type`) have
> landed; their dispositions are recorded in §9.

---

## 1. Responsibility

VINLab is the **vehicle-identity channel** of the 4D petrol diagnostic pipeline. It
transforms a 17-character VIN into a typed `VinDNA` dataclass — the **physical DNA**
(Part A) of the vehicle. It is a **producer, not a judge**: it decodes and grades
confidence; it does not rank faults. `VinDNA`'s schema is governed by
`SEMANTIC_CONTRACT.md §4.1`.

Runtime is **offline**: zero network, zero MySQL. All reference data is baked into
`vinlab/data/` at build time. VINLab is one of three sibling labs in the DNA family;
`dnalab` imports it (one-directional), but VINLab imports no other lab.

---

## 2. Architecture Position

```
caller (DNALab assembly / COMLab projector / tooling)
  │  vinlab.decode(vin, *, data_dir=None)
  ▼
vinlab.__init__.decode
  │  _get_decoder(data_dir)  ── lru_cache per data_dir
  ▼
RobustVINDecoder.decode_vin_payload(raw_vin)
  │   [1] pre_clean_vin          I→1, O→0, strip, upper (SAE J853)
  │   [2] length guard           len != 17 → ChassisNumberError
  │   [3] charset pattern        [A-HJ-NPR-Z0-9]{17} → VINDecodeError
  │   [4] validate_vin_checksum  NHTSA mod-11 + 3 bypass paths
  │   [5] _resolve_wmi           positions 1-3 (+ J853 low-volume rule)
  │   [6] _resolve_year          vin[9]; passthrough → None; L-disambiguation
  │   [H2] year ∈ [1990, 2020]   else VINDecodeError
  │   [7] _resolve_engine        Path A vds_full / Path B pos_8_only
  │   [H1] petrol guard          keyword scan (CSV + vref.db) → VINDecodeError
  │   [8] lookup_engine_ref      vref.db tech-mask + CoC overlay (read-only)
  │   [9] overlays               air metering, horizon, stress RPM, O2, cylinder
  │   [10] confidence grade      NONE / PARTIAL / HIGH
  ▼
VinDNA  (frozen dataclass, 16 core + 13 CoC fields)
  │
  ▼
COMLab mirrors VinDNA and projects it into per-lab DNA views (separate codebase).
```

Zero cross-lab Python imports. All SQL is confined to `db/tecdoc_query.py` (H8).

---

## 3. Internal Pipeline (decode_vin_payload)

```
raw_vin
  │
[1] pre_clean_vin           strip().upper(); I→1, O→0  (SAE J853 §4.1.2)
[2] len(vin) != 17          → ChassisNumberError (may be a pre-VIN chassis no.)
[3] _VIN_PATTERN mismatch   → VINDecodeError (invalid characters)
[4] validate_vin_checksum   False → VINDecodeError (checksum failed)
        bypass: non-NHTSA WMI (EU/JP/KR/IN) | OPSI corrupt prefix | non-standard pos-9
[5] _resolve_wmi            vin[2]=='9' → try vin[0:3]+vin[11:14]; else vin[0:3]
        miss → VINDecodeError (WMI not found)
[6] _resolve_year           vin[9]; {0,U,Z} → (None, None);
        single candidate → year; L-collision → era_hint (legacy=1990 / else=2020)
[H2] model_year ∉ [1990,2020] (when known) → VINDecodeError (year out of scope)
[7] _resolve_engine         Path A brand_vds_full (vin[3:8]); Path B brand_pos8 (vin[7])
        → engine_row dict | None
[H1] _is_non_petrol(CSV fuel_system_type) → VINDecodeError (fuel out of scope)
[8] lookup_engine_ref(vref.db, engine_code)  → db_row | None
        db None → conf flag; engine None → conf flag (NONE)
[H1] _is_non_petrol(db fuel_delivery_type) → VINDecodeError
[9] assemble VinDNA:
        basic attrs (CSV) → tech-mask (vref.db, authoritative for displacement) →
        cylinder heuristic (only if cylinder_count==0) → air metering classify →
        euro→horizon → stress RPM → CoC overlay
[10] confidence:  engine_not_in_csv → NONE | any conf_flags → PARTIAL | clean → HIGH
  ▼
VinDNA(...)   one constructor call
```

The decoder gathers every value into locals first, then makes **one** `VinDNA(...)`
constructor call (the dataclass is frozen/immutable).

---

## 4. Checksum Architecture (validate_vin_checksum)

NHTSA modulo-11 (49 CFR Part 565) with three documented bypass paths, in order:

| Bypass | Trigger | Rationale |
|--------|---------|-----------|
| Non-NHTSA WMI | `country ∈` European set ∪ {Japan, South Korea, India} | ISO 3780 — check digit never mandatory outside US/CA/MX market |
| OPSI corrupt prefix | `vin[:3] ∈ {3MZ, 3MD, 3MV}` | T-FX-5 finding: 1,866 Mexican Mazda VINs with corrupt pos-9 in Slovenian DMV data |
| Non-standard pos-9 | `vin[8] ∉ "123456789X"` | European 1990s vehicles used `Z`/`0` as a dummy check character |

When none of the bypasses apply, the standard transliteration + position-weights
computation runs: `remainder = Σ(value × weight) % 11`, expected `= "X"` if remainder
is 10 else `str(remainder)`, compared to `vin[8]`.

---

## 5. WMI & Year Resolution

**WMI (`_resolve_wmi`).** Standard manufacturers occupy VIN positions 1–3. SAE J853's
low-volume rule (manufacturers producing < 500 units/year, signalled by `vin[2] == '9'`)
places the manufacturer code at positions 12–13, so the resolver tries the 6-char
extended key `vin[0:3] + vin[11:14]` **first**, then falls back to the standard 3-char
key. A miss raises `VINDecodeError`.

**Year (`_resolve_year`).** SAE J853 excludes `I, O, Q, U, Z` from the year alphabet;
`0` is also unused. These passthrough characters (`{0, U, Z}`) return
`(model_year=None, flag=None)` — *unknown, not an error*. The only colliding code in
1990–2020 is `L` (1990 vs 2020), disambiguated by the WMI `era_hint` column
(`legacy → ERA_1 → 1990`; otherwise `ERA_3 → 2020`). An unrecognised era returns the
first candidate plus an `era_hint_unrecognised` confidence flag.

---

## 6. Engine Resolution & Overlays

**Two-path engine resolution (`_resolve_engine`).** Path A matches the modern 5-char
VDS (`vin[3:8]`) keyed `BRAND_VDS`; Path B falls back to the legacy single-character
position-8 (`vin[7]`) keyed `BRAND_POS8`. Returns the CSV row or `None`.

**Overlay modules** (applied after base decode, each a pure function of already-decoded
fields):

| Overlay | Module | Input → Output |
|---------|--------|----------------|
| Air metering | `overlay/air_metering.py` | `(has_maf, has_map)` → `(primary_load_calculation, air_metering_strategy)` |
| Horizon | `overlay/horizon.py` | `euro_emission_category` → `Horizon` |
| Stress RPM | `overlay/stress_rpm.py` | `(euro, induction, fuel, displacement, horizon)` → `int` |
| Upstream O2 | `overlay/switches.py` | `(year, fuel_delivery, o2_hint)` → `UpstreamO2Type` |
| Cylinder fallback | `overlay/cylinder_heuristic.py` | `(engine_code, displacement, brand)` → `CylinderHint` |

`has_maf` / `has_map` derive from `vref.db` flags when present, else from fuel-delivery
and induction heuristics (see DLD §6). The classifier (T-FX-2) is a single deep module
producing **both** the developer label and the OBDLab-canonical strategy from one
classification of `(has_maf, has_map)` — eliminating the "two views of one fact" defect.

**Cylinder heuristic (T-VL-7).** A last-resort fallback that fires **only** when
`cylinder_count == 0` after CSV and `vref.db`. Brand-dispatched (per-manufacturer
engine-code rules) with a displacement-band fallback; never overwrites real data.

---

## 7. Downstream Integration Points (consumers)

VINLab produces; COMLab mirrors `VinDNA` and **projects** it into per-lab DNA views.
The named consumers (signal/noise rule):

| `VinDNA` field | Consumer | Status |
|----------------|----------|--------|
| `air_metering_strategy` | OBDLab VE routing branch (via `ObdLabDnaView`) | live |
| `induction_type` | OBDLab `FAULT_VE_SENSOR_SKEW` classifier; cylinder/turbo logic | live |
| `upstream_o2_type` | OBDLab O2 normalisation path | live (enum-mirror realign pending, COMLab-D) |
| `stress_idle_rpm_target` | OBDLab `STRESS_IDLE` bucketing target | live |
| `confidence` | OBDLab three-branch DNA-RPM gate | live |
| `engine_displacement_liters` | OBDLab VE formula denominator | live |
| `number_of_banks` / `cylinder_count` | Bank-2 null contract; UI field gating | live |
| CoC targets (`target_lambda_v112`, `co_low_idle`, `co_high_idle`, …) | GASLab CoC threshold tables (via projector) | emitted (T-DNA-4 formalized the top-level CoC fields); projector path fix is COMLab-C (Stage 4) |
| `rated_rpm` | OBDLab RPM ceiling (projector reads it) | **live — emitted by `VinDNA` since T-DNA-3** |
| `model` | DTCLab mirror requires it | **kept-empty (no field), T-DNA-5** — DBS shows no within-engine-code variance; DTCLab mirror relaxed via COMLab-D |
| `euro_emission_category` / `resolved_horizon` | era-conditioned routing context | live |

> **Cross-lab note:** COMLab and DTCLab mirror `VinDNA`'s types locally and reconcile
> **up to** this contract. VINLab is never blocked on them. Where the projector and
> `VinDNA` disagree on nesting (CoC, emissions), the fix is the paired COMLab-C path
> change plus the T-DNA-4 contract amendment — not a VINLab change made unilaterally.

---

## 8. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Runtime network calls | 0 |
| Runtime MySQL calls | 0 (reference baked into `vinlab/data/`; `vref.db` read-only) |
| SQL isolation (H8) | all SQL in `db/tecdoc_query.py`; no other module writes SQL |
| Import isolation | 0 cross-lab Python imports (DNA-family one-way: `dnalab → vinlab`) |
| Numeric literals | every literal in `vinlab/` carries a `# source:`/`# wiki:` citation |
| Signal/noise | every `VinDNA` field has a named consumer (live or registered proposal) |
| Decode determinism | same VIN + same `data_dir` → identical `VinDNA` (decoder is `lru_cache`d) |

---

## 9. Known Gaps / Accepted Behaviour

| ID | Description | Status |
|----|-------------|--------|
| T-DNA-3 | `rated_rpm` now emitted by `VinDNA` (source `P14_rated_rpm`); consumed by the projector → `ObdLabDnaView.rated_rpm` | Done |
| T-DNA-4 | CoC fields formalized at top level on `VinDNA`; emissions block formalized (`has_catalyst`/`egr_equipped` nested, `secondary_air_equipped` dropped). The projector path bug (reads CoC under `emissions{}`) is the paired **COMLab-C** fix at Stage 4 | VINLab side done; COMLab-C pending in COMLab |
| T-DNA-5 | `model` kept-empty (no `VinDNA` field): DBS specimen file shows no repeated engine-code groups, so no within-code CoC variance evidence to justify the field. DTCLab mirror relaxation registered as COMLab-D | Done (keep-empty) |
| CoC-null check | Only 9 of 13 CoC fields drive the confidence downgrade; `hc_nox`/noise fields excluded | Accepted (documented) |
| `mysql_data/` | ~484 MB verbatim build-time copy; unused at runtime | Track-2 removal candidate |
| `secondary_air_equipped` | Present in `VehicleDNA.md` example payload, not on `VinDNA.Emissions` | Resolved (T-DNA-4): dropped — no named consumer; `emissions` keeps `has_catalyst`/`egr_equipped` |
