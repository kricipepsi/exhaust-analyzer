---
title: "VINLab Decode Scope Rules — Length, Charset, Checksum Gate, Petrol Guard, Year Bound"
lab: vinlab
node_type: wiki
module: vinlab
subsystem: decode-scope-rules
implements:
  - "labs/vinlab/vinlab/decoder.py"
consumers:
  - "vinlab: labs/vinlab/vinlab/decoder.py RobustVINDecoder.decode_vin_payload"
  - "vinlab: labs/vinlab/vinlab/decoder.py _is_non_petrol"
  - "vinlab: labs/vinlab/vinlab/decoder.py validate_vin_checksum"
drift_guards:
  - "labs/vinlab/tests/unit/test_decoder.py"
tags: [vinlab, wiki, decode-scope-rules]
source: "labs/vinlab/wiki/10_decode_scope_rules.md"
role: citation-target
status: authoritative
date: 2026-06-12
companion_docset: "docs/ (HLD, DLD, VIN_VOCABULARY); VINlookup.md"
kg_ingestion: none
mirrors_code:
  - "vinlab/decoder.py:RobustVINDecoder.decode_vin_payload"
  - "vinlab/decoder.py:validate_vin_checksum"
  - "vinlab/decoder.py:_is_non_petrol / _NON_PETROL_KEYWORDS"
owns_citations:
  - "decoder.py — _NON_PETROL_KEYWORDS (H1 petrol-only guard)"
  - "decoder.py — model-year scope [1990, 2020] (H2)"
  - "decoder.py — _YEAR_PASSTHROUGH {0, U, Z}"
related_pages: [00_index, 11_engine_resolution, 12_brand_cylinder_rules]
---

# 10. Decode Scope Rules

> **What this page owns.** The gates that decide whether an input is *in scope* for
> VINLab at all — length, character set, checksum validity (and its documented
> bypasses), petrol-only fuel, and the supported model-year window. These are the
> rules that were previously scattered across `VINlookup.md`, task records, and
> inline comments; this page is their durable canonical home. Where a rule rests on
> an **external standard** (SAE J853, NHTSA 49 CFR Part 565, ISO 3780) this page
> *references* it and does **not** restate its number — per the index's
> no-duplication rule.

The gates run in a fixed order inside `decode_vin_payload`. Any gate that fails
raises an exception; the caller never receives a partially-decoded `VinDNA` from a
rejected VIN.

```
raw input
  │
  ▼
[1] pre-clean         strip().upper();  I→1, O→0          (SAE J853 §4.1.2 — referenced)
[2] length gate       len != 17        → ChassisNumberError
[3] charset gate      _VIN_PATTERN fail → VINDecodeError
[4] checksum gate     invalid          → VINDecodeError   (3 bypass paths below)
      … WMI / year / engine resolution (page 11) …
[H1] petrol gate      non-petrol fuel  → VINDecodeError
[H2] year gate        year ∉ [1990,2020] → VINDecodeError
  ▼
VinDNA (only if every gate passes)
```

## 10.1 Length gate — exactly 17 characters {#RULE_LENGTH}

A valid VIN is exactly 17 characters. A wrong-length input is treated as a likely
**pre-VIN chassis / frame number**, not as a malformed VIN, so it raises the
dedicated `ChassisNumberError` (a subclass of `VINDecodeError`) rather than the
generic error. This lets a caller distinguish "this looks like an older chassis
number" from "this is a corrupt VIN".

```
len(vin) != 17  →  ChassisNumberError("Input is not a 17-character VIN …")
```

`# source: decoder.py — len(vin) != 17 guard; ChassisNumberError docstring`

## 10.2 Character-set gate {#RULE_CHARSET}

After pre-cleaning (which substitutes the visually ambiguous `I → 1` and `O → 0`
per SAE J853), the VIN must match the canonical VIN alphabet — uppercase letters
and digits **excluding `I`, `O`, `Q`**:

```
_VIN_PATTERN = ^[A-HJ-NPR-Z0-9]{17}$        # decoder.py
```

A mismatch raises `VINDecodeError` (invalid characters). The pattern is the
machine-checkable form of the SAE J853 exclusion rule; the standard is the external
authority, this page only records the regex VINLab actually enforces.

`# source: decoder.py — _VIN_PATTERN; SAE J853 character-exclusion rule (referenced)`

## 10.3 Checksum gate and its three bypass paths {#RULE_CHECKSUM}

The North-American check-digit algorithm (NHTSA modulo-11, 49 CFR Part 565) is an
**external standard** — VINLab references it, it does not restate the weight table
or transliteration values here. What VINLab *owns* is the **bypass policy**: the
check digit is mandatory only for the North-American market, so three documented
conditions skip validation rather than rejecting a legitimate non-NA VIN. They are
tried in order:

| # | Bypass | Trigger | Why it exists | Home |
|---|--------|---------|---------------|------|
| 1 | Non-NHTSA WMI | manufacturer country ∈ European set ∪ {Japan, South Korea, India} | ISO 3780 — the check digit is never mandatory outside the US/CA/MX market; decision is **data-driven** from `wmi.csv` | `wmi.csv` + ISO 3780 (referenced) |
| 2 | OPSI corrupt prefix | `vin[:3] ∈ {3MZ, 3MD, 3MV}` | T-FX-5 finding — 1,866 Mexican-Mazda VINs in the Slovenian DMV data carry a corrupt position-9 digit | **page 11 (`#RULE_OPSI`)** — VINLab-owned |
| 3 | Legacy dummy pos-9 | `vin[8] ∉ "123456789X"` | 1990s European vehicles used `Z` / `0` as a dummy check character | `VINlookup.md §1` |

When **none** of the three apply, the standard modulo-11 computation runs and a
mismatch raises `VINDecodeError`. The OPSI corrupt-prefix detail (the `3MZ/3MD/3MV`
prefix set and the registry finding behind it) is the genuinely VINLab-owned piece
and is documented in full on page 11 so the data-source story lives next to the
WMI/registry resolution it belongs to.

`# source: decoder.py — validate_vin_checksum; _OPSI_CHECKSUM_CORRUPT_PREFIXES`

## 10.4 Petrol-only guard (H1) {#RULE_PETROL}

4DApp v2 is **petrol-only**. VINLab enforces this with a keyword scan against the
decoded fuel description from **both** data sources — the petrol CSV
`fuel_system_type` and the `vref.db` `fuel_delivery_type`. Any case-insensitive
substring match raises `VINDecodeError` (fuel out of scope). This is the canonical
home for the keyword set:

```
_NON_PETROL_KEYWORDS = (
    "DIESEL", "LPG", "CNG", "E85", "HYBRID", "ELECTRIC", "EV",
    "FLEX_FUEL", "FLEXFUEL", "METHANOL", "ETHANOL", "BIOFUEL",
)
```

The match is a plain `kw in value.upper()` test, so e.g. `FLEX_FUEL` and the
spaceless `FLEXFUEL` are both listed to catch either spelling. The guard runs
twice in the pipeline: once on the CSV fuel field (step H1, before the `vref.db`
read) and again on the `vref.db` fuel field (after it), so a non-petrol vehicle is
rejected whichever source first reveals it.

`# source: decoder.py — _NON_PETROL_KEYWORDS; _is_non_petrol() (H1 guard)`

## 10.5 Model-year scope guard (H2) — [1990, 2020] {#RULE_YEAR_BOUND}

VINLab supports model years **1990 through 2020 inclusive**. When a year is
resolved (see page 11 for *how*), a value outside that closed window raises
`VINDecodeError("Year out of supported scope 1990-2020")`.

```
if model_year is not None and (model_year < 1990 or model_year > 2020):
    raise VINDecodeError("Year out of supported scope 1990-2020")     # decoder.py
```

The window is the VINLab-owned scope decision (it bounds the reference data baked
at build time); the value lives here, not in a task file. Note the guard fires only
when the year is **known** — an unresolved year (next section) is *unknown, not
out of scope*, and is allowed through with reduced confidence.

`# source: decoder.py — H2 year-bound guard [1990, 2020]`

## 10.6 Year passthrough — unknown is not an error {#RULE_YEAR_PASSTHROUGH}

Three position-10 characters are treated as **placeholders, not years**: when
`vin[9]` is one of these, the decoder returns `model_year = None` (and no
confidence flag from this step) rather than rejecting the VIN:

```
_YEAR_PASSTHROUGH = frozenset({"0", "U", "Z"})        # decoder.py
```

`U` and `Z` are excluded from the SAE J853 year alphabet, and `0` is unused;
manufacturers assign them to non-year-coded market variants. Distinguishing
*unknown* (`None`, allowed) from *out-of-scope* (a real year outside 1990–2020,
rejected by §10.5) is deliberate — it keeps a decodable VIN with an unstamped year
in scope at `PARTIAL`/`HIGH` rather than throwing it away. The downstream
confidence grade is page-04 / VIN_VOCABULARY territory; this page only owns the
passthrough set itself.

`# source: decoder.py — _YEAR_PASSTHROUGH {0, U, Z}`

## 10.7 Exception taxonomy (what each gate raises) {#RULE_EXCEPTIONS}

| Gate | Raises | Meaning to the caller |
|------|--------|-----------------------|
| Length ≠ 17 | `ChassisNumberError` | Probably a pre-VIN chassis/frame number, not a VIN |
| Charset mismatch | `VINDecodeError` | Malformed — illegal VIN characters |
| Checksum fail (no bypass) | `VINDecodeError` | Check digit does not validate |
| WMI miss | `VINDecodeError` | Manufacturer prefix not in `wmi.csv` (page 11) |
| Non-petrol fuel | `VINDecodeError` | Fuel out of scope (H1) |
| Year out of [1990, 2020] | `VINDecodeError` | Model year out of supported scope (H2) |

`ChassisNumberError` subclasses `VINDecodeError`, so a caller that only catches the
base class still handles wrong-length input; one that wants the distinction catches
the subclass first.

`# source: decoder.py — ChassisNumberError(VINDecodeError); decode_vin_payload raise sites`

## Graph relations (explicit)

**VINWIKI-10-DECODE_SCOPE_RULES** DESCRIBES **VIN length gate**
**VINWIKI-10-DECODE_SCOPE_RULES** DESCRIBES **VIN charset gate**
**VINWIKI-10-DECODE_SCOPE_RULES** DESCRIBES **VIN checksum gate**
**VINWIKI-10-DECODE_SCOPE_RULES** DESCRIBES **H1 petrol-only guard**
**VINWIKI-10-DECODE_SCOPE_RULES** DESCRIBES **H2 model-year scope guard**
**vinlab.decoder.RobustVINDecoder.decode_vin_payload** CONSUMES **VIN length gate**
**vinlab.decoder.RobustVINDecoder.decode_vin_payload** CONSUMES **VIN charset gate**
**vinlab.decoder.validate_vin_checksum** CONSUMES **VIN checksum gate**
**vinlab.decoder._is_non_petrol** CONSUMES **_NON_PETROL_KEYWORDS**
**vinlab.decoder.RobustVINDecoder.decode_vin_payload** CONSUMES **H1 petrol-only guard**
**vinlab.decoder.RobustVINDecoder.decode_vin_payload** CONSUMES **H2 model-year scope guard**
**labs/vinlab/tests/unit/test_decoder.py::TestH1PetrolOnly.test_is_non_petrol_detects_diesel** VERIFIES **vinlab.decoder._is_non_petrol**
**labs/vinlab/tests/unit/test_decoder.py::TestH2YearBounds.test_year_below_1990_raises** VERIFIES **H2 model-year scope guard**

## Core Entities

- **VIN length gate** - Exactly-17-character VIN requirement. Consumer: `vinlab.decoder.RobustVINDecoder.decode_vin_payload`.
- **VIN charset gate** - `_VIN_PATTERN` and SAE J853 character exclusion enforcement. Consumer: `vinlab.decoder.RobustVINDecoder.decode_vin_payload`.
- **VIN checksum gate** - NHTSA modulo-11 validation plus the three documented bypass paths. Consumer: `vinlab.decoder.validate_vin_checksum`.
- **H1 petrol-only guard** - Non-petrol keyword rejection across CSV and `vref.db` fuel fields. Consumer: `vinlab.decoder._is_non_petrol`.
- **_NON_PETROL_KEYWORDS** - Canonical VINLab-owned non-petrol keyword tuple. Consumer: `vinlab.decoder._is_non_petrol`.
- **H2 model-year scope guard** - Inclusive 1990-2020 model-year bound. Consumer: `vinlab.decoder.RobustVINDecoder.decode_vin_payload`.
- **_YEAR_PASSTHROUGH** - `{0, U, Z}` unknown-year passthrough set. Consumer: `vinlab.decoder.RobustVINDecoder._resolve_year`.
