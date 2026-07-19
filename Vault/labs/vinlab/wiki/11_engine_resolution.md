---
node_type: "wiki"
lab: "vinlab"
module: "vinlab"
subsystem: "identity-resolution"
implements:
  - "labs/vinlab/vinlab/decoder.py"
  - "labs/vinlab/vinlab/models.py"
  - "labs/vinlab/vinlab/overlay/horizon.py"
  - "labs/vinlab/vinlab/overlay/stress_rpm.py"
  - "labs/vinlab/vinlab/overlay/switches.py"
consumers:
  - "vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder._resolve_wmi"
  - "vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder._resolve_year"
  - "vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder._resolve_engine"
  - "vinlab: labs/vinlab/vinlab/overlay/horizon.py euro_to_horizon"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py (VinDNA.rated_rpm)"
  - "obdlab: ObdLabDnaView.rated_rpm RPM ceiling (rated_rpm)"
drift_guards:
  - "labs/vinlab/tests/unit/test_horizon.py"
  - "labs/vinlab/tests/unit/test_models.py"
  - "labs/vinlab/tests/unit/test_decoder.py"
tags: [vinlab, finished, wiki]
source: "labs/vinlab/wiki/11_engine_resolution.md"
---

# 11. Identity Resolution — WMI, Year, Engine, Cylinder Fallback

> **What this page owns.** *How* VINLab turns the three identity slices of a VIN —
> manufacturer (WMI), model year, and engine — into resolved values, plus the two
> real-world data corrections that make this work on the Slovenian DMV corpus: the
> **OPSI corrupt-prefix finding** (T-FX-5) and the **cylinder-count fallback**
> (T-VL-7). The `make`/displacement *values* come from baked reference data
> (`wmi.csv`, `vds_engine_map.csv`, `vref.db`); this page owns the **resolution
> logic and the VINLab-specific numbers** (the displacement bands), not the data
> rows.

## 11.1 WMI resolution (`_resolve_wmi`) {#RULE_WMI}

The World Manufacturer Identifier normally occupies VIN positions 1–3. SAE J853's
**low-volume rule** — manufacturers building fewer than 500 units/year, signalled
by `vin[2] == '9'` — relocates the manufacturer code to positions 12–13. So the
resolver builds the extended 6-character key **first**, then falls back to the
standard 3-character key:

```
if vin[2] == '9':  try  vin[0:3] + vin[11:14]   (6-char extended key)
else / on miss:    try  vin[0:3]                (3-char standard key)
miss on both       →    VINDecodeError ("WMI not found")
```

A hit returns the `wmi.csv` row, which carries `brand`, `country`, and the
`era_hint` column used for year disambiguation (§11.2). The `country` value also
feeds the non-NHTSA checksum bypass (page 10, §10.3 path 1).

`# source: decoder.py — _resolve_wmi; SAE J853 low-volume rule (vin[2]=='9')`

## 11.2 Year resolution and the `L` collision (`_resolve_year`) {#RULE_YEAR}

Position 10 (`vin[9]`) encodes the model year via `years.csv`
(`year_code → calendar_year`, with an `era_bucket` of `ERA_1` / `ERA_3`). Three
characters are passthrough placeholders returning `None` — owned by page 10
(`#RULE_YEAR_PASSTHROUGH`).

Within the supported 1990–2020 window the **only** colliding code is `L`, which
maps to *both* 1990 and 2020. It is disambiguated by the WMI `era_hint`:

```
era_hint == "legacy"  AND row.era_bucket == "ERA_1"  → 1990
era_hint != "legacy"  AND row.era_bucket == "ERA_3"  → 2020
unrecognised era_hint → first candidate + confidence flag "era_hint_unrecognised"
```

So a legacy-era manufacturer's `L` resolves to 1990; a modern one's resolves to
2020. When the era hint matches neither bucket, the decoder returns the first
candidate year and raises the `era_hint_unrecognised` confidence flag (a PARTIAL
downgrade — see VIN_VOCABULARY §4), never an exception. The resolved year is then
subject to the H2 scope guard on page 10 (§10.5).

`# source: decoder.py — _resolve_year; L-disambiguation via wmi era_hint`

## 11.3 OPSI corrupt-prefix finding (T-FX-5) {#RULE_OPSI}

This is the genuinely VINLab-owned piece behind checksum bypass path 2 (page 10,
§10.3). The Slovenian DMV registration export (OPSI open-data) contains **1,866
Mexican-built Mazda VINs whose position-9 check digit is corrupt** in the source
data — they are valid vehicles with an unreliable check character. Rejecting them
on checksum would silently drop a real, in-scope population. The fix is a narrow,
named prefix allow-list that skips checksum validation for exactly those WMIs:

```
_OPSI_CHECKSUM_CORRUPT_PREFIXES = frozenset({"3MZ", "3MD", "3MV"})   # decoder.py
```

The set is deliberately closed and tied to the registry finding — it is **not** a
general "skip checksum for Mazda" rule. Widening it requires a new finding and a
follow-up task; the displacement of the boundary is a code-review concern. This
page is the durable home for *why* those three prefixes bypass the checksum, so the
rationale no longer lives only in the T-FX-5 task record.

`# source: decoder.py — _OPSI_CHECKSUM_CORRUPT_PREFIXES; T-FX-5 full-run analysis (1,866 VINs)`

## 11.4 Two-path engine resolution (`_resolve_engine`) {#RULE_ENGINE}

The engine row is matched against `vds_engine_map.csv` (indexed at load) by two
keys in priority order, both prefixed with the resolved brand so the same VDS
slice can mean different engines for different manufacturers:

```
Path A (modern):  key = f"{BRAND}_{vin[3:8]}"   → vds_full_index   (5-char VDS)
Path B (legacy):  key = f"{BRAND}_{vin[7]}"      → vds_pos8_index   (single pos-8 char)
neither matches   → None  (engine not in CSV → confidence NONE, page 04)
```

Path A is the modern 5-character VDS (`vin[3:8]`); Path B is the legacy
single-character position-8 fallback (`vin[7]`) used by older vehicles whose VDS
does not carry a full engine pattern. A `None` result is **not** an exception — the
VIN is still decoded from WMI/year, but `confidence` collapses to `NONE` because
the engine — the spine of every CoC and overlay value — is unknown.

`# source: decoder.py — _resolve_engine; BRAND_VDS / BRAND_POS8 key construction`

## 11.5 Cylinder-count fallback (`infer_cylinder`, T-VL-7) {#RULE_CYLINDER_FALLBACK}

A **last-resort runtime fallback** that fires *only* when `cylinder_count == 0`
after both the CSV and `vref.db` lookups. Callers gate on `cylinder_count == 0`, so
it **never overwrites real data** — it only fills a gap. It returns a `CylinderHint`
(`count`, `config`, `induction`, `source`) where `source` records provenance:
`brand_rule`, `disp_fallback`, or `unresolved`.

Resolution is **brand-dispatched first** (the per-manufacturer engine-code tables
on page 12), then falls back to a displacement-only band table when the brand is
unknown or its rule does not fire. The displacement bands are the VINLab-owned
numbers (T-VL-7) and live here canonically:

| Displacement (L) | Inferred count | Config | Source tag |
|---|---|---|---|
| `disp <= 0` | 0 (unresolved) | — | `unresolved` |
| `0 < disp <= 1.2` | 3 | `I3` | `disp_fallback` |
| `1.2 < disp <= 2.5` | 4 | `I4` | `disp_fallback` |
| `2.5 < disp <= 3.5` | 6 | `V6` | `disp_fallback` |
| `3.5 < disp <= 5.0` | 8 | `V8` | `disp_fallback` |
| `disp > 5.0` | 12 | `V12` | `disp_fallback` |

The config vocabulary the hint may emit is a fixed set (`I3, I4, I5, I6, V6, V8,
V10, V12, BOXER_4, BOXER_6, ROTARY, W12`); it is carried as auxiliary data, not
stored directly on `VinDNA`. The induction default is `NATURALLY_ASPIRATED` unless
a brand rule promotes it to `TURBOCHARGED` (page 12).

```
infer_cylinder(code, disp, brand):
    code empty            → _displacement_fallback(disp)
    brand in dispatch     → brand rule (page 12), else _displacement_fallback(disp)
    brand unknown         → _displacement_fallback(disp)
```

`# source: cylinder_heuristic.py — _displacement_fallback bands; _CONFIG_VOCAB; T-VL-7 task spec`

## 11.6 Why these three corrections live together

WMI resolution, the OPSI checksum finding, and the engine/cylinder fallbacks all
exist for one reason: VINLab decodes a **real, messy registry corpus**, not
textbook VINs. The standards (page 10) define the ideal; this page records the
empirically-grounded adjustments that keep legitimate Slovenian-DMV vehicles in
scope. Each adjustment is bounded and named (a closed prefix set, a gated
`count == 0` fallback) so it can never silently expand into a general override of
authoritative data.

## Graph relations (explicit)

**VINWIKI-11-IDENTITY_RESOLUTION** DESCRIBES **WMI resolution**
**VINWIKI-11-IDENTITY_RESOLUTION** DESCRIBES **year resolution**
**VINWIKI-11-IDENTITY_RESOLUTION** DESCRIBES **OPSI corrupt-prefix finding**
**VINWIKI-11-IDENTITY_RESOLUTION** DESCRIBES **two-path engine resolution**
**VINWIKI-11-IDENTITY_RESOLUTION** DESCRIBES **cylinder-count fallback**
**vinlab.decoder.RobustVINDecoder._resolve_wmi** CONSUMES **WMI resolution**
**vinlab.decoder.RobustVINDecoder._resolve_year** CONSUMES **year resolution**
**vinlab.decoder.validate_vin_checksum** CONSUMES **_OPSI_CHECKSUM_CORRUPT_PREFIXES**
**vinlab.decoder.RobustVINDecoder._resolve_engine** CONSUMES **two-path engine resolution**
**vinlab.overlay.cylinder_heuristic.infer_cylinder** CONSUMES **cylinder-count fallback**
**vinlab.overlay.horizon.euro_to_horizon** CONSUMES **EuroEmissionCategory**
**vinlab.models.VinDNA.resolved_horizon** MAPS_TO **vinlab.models.Horizon**
**vinlab.models.VinDNA.rated_rpm** MAPS_TO **comlab.schemas.lab_dna_views.ObdLabDnaView.rated_rpm**
**comlab.projection.project** CONSUMES **vinlab.models.VinDNA.rated_rpm**
**obdlab.core.pid_ingestion_validator.PIDIngestionValidator._check_dna_rpm** CONSUMES **comlab.schemas.lab_dna_views.ObdLabDnaView.rated_rpm**
**labs/vinlab/tests/unit/test_horizon.py::test_euro_to_horizon_matches_contract** VERIFIES **vinlab.overlay.horizon.euro_to_horizon**
**labs/vinlab/tests/unit/test_models.py::test_decode_known_engine_code_yields_rated_rpm** VERIFIES **vinlab.models.VinDNA.rated_rpm**
**labs/obdlab/tests/unit/test_pid_ingestion_validator.py DNA-RPM tests** VERIFIES **PIDIngestionValidator._check_dna_rpm**

## Core Entities

- **WMI resolution** - Standard and low-volume WMI lookup. Consumer: `vinlab.decoder.RobustVINDecoder._resolve_wmi`.
- **year resolution** - Position-10 model-year decoding, `L` disambiguation, and unknown passthrough. Consumer: `vinlab.decoder.RobustVINDecoder._resolve_year`.
- **OPSI corrupt-prefix finding** - Closed `{3MZ, 3MD, 3MV}` checksum-bypass finding. Consumer: `vinlab.decoder.validate_vin_checksum`.
- **two-path engine resolution** - `BRAND_VDS` first, legacy `BRAND_POS8` fallback. Consumer: `vinlab.decoder.RobustVINDecoder._resolve_engine`.
- **cylinder-count fallback** - Brand rule then displacement-band last-resort inference. Consumer: `vinlab.overlay.cylinder_heuristic.infer_cylinder`.
- **euro_to_horizon** - Euro category to VIN horizon overlay. Consumer: `vinlab.overlay.horizon.euro_to_horizon`; tests in `labs/vinlab/tests/unit/test_horizon.py`.
- **VinDNA.rated_rpm** - DBS P14 rated-RPM output. Consumer: `comlab.projection.project` -> `ObdLabDnaView.rated_rpm` -> `PIDIngestionValidator._check_dna_rpm`.
