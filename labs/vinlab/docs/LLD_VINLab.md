---
node_type: lld
lab: vinlab
module: vinlab
subsystem: low-level-design
implements:
  - "labs/vinlab/vinlab/__init__.py"
  - "labs/vinlab/vinlab/decoder.py"
  - "labs/vinlab/vinlab/models.py"
  - "labs/vinlab/vinlab/db/tecdoc_query.py"
  - "labs/vinlab/vinlab/overlay/air_metering.py"
  - "labs/vinlab/vinlab/overlay/cylinder_heuristic.py"
  - "labs/vinlab/vinlab/overlay/horizon.py"
  - "labs/vinlab/vinlab/overlay/stress_rpm.py"
  - "labs/vinlab/vinlab/overlay/switches.py"
consumers:
  - "dld: labs/vinlab/docs/DLD_VINLab.md"
  - "dnalab: labs/dnalab/dnalab/assembly.py build_vehicle_dna (vinlab.decode → VehicleDNA.vin_dna, Part A)"
  - "comlab: labs/comlab/comlab/projection.py project() (VehicleDNA → LabDnaView, reads vin_dna)"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py vin_confidence (request.metadata.vin_confidence, :2239)"
drift_guards:
  - "labs/vinlab/tests/unit/test_decoder.py"
  - "labs/vinlab/tests/unit/test_models.py"
  - "labs/vinlab/tests/unit/test_horizon.py"
  - "labs/vinlab/tests/unit/test_stress_rpm.py"
  - "labs/vinlab/tests/unit/test_switches.py"
  - "labs/vinlab/tests/unit/test_cylinder_heuristic.py"
  - "labs/vinlab/tests/unit/test_air_metering.py"
  - "labs/vinlab/tests/unit/test_contract_conformance.py"
  - "labs/vinlab/tests/unit/test_vindna_from_json.py"
tags: [vinlab, lld, low-level-design]
source: "labs/vinlab/docs/LLD_VINLab.md"
---

# LLD — VINLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_VINLab v2.0
**HLD / DLD Reference:** HLD_VINLab v2.0 / DLD_VINLab v2.0
**Version:** 2.0
**Date:** 2026-06-11

Convention: every numeric literal in `vinlab/` carries a `# source:`/`# wiki:` comment
(code-review gate). The literals below are transcribed from the live modules with their
cited source shown alongside.

---

## 1. Checksum Tables (`decoder.py`)

Source: NHTSA 49 CFR Part 565 — VIN checksum transliteration + position weights.

```python
_TRANSLITERATION = {            # letter → numeric value (I, O, Q excluded)
    A:1 B:2 C:3 D:4 E:5 F:6 G:7 H:8
    J:1 K:2 L:3 M:4 N:5 P:7 R:9
    S:2 T:3 U:4 V:5 W:6 X:7 Y:8 Z:9
}
_WEIGHTS = (8,7,6,5,4,3,2,10,0,9,8,7,6,5,4,3,2)   # pos 9 (check digit) weight = 0
```

```python
remainder = sum(value_i * _WEIGHTS[i] for i in 0..16) % 11   # modulo 11
expected  = "X" if remainder == 10 else str(remainder)
return expected == vin[8]
```

---

## 2. Character & Charset Constants (`decoder.py`)

```python
_CHAR_SUBSTITUTIONS = {"I": "1", "O": "0"}     # source: SAE J853 §4.1.2 (OCR recovery)
_VIN_PATTERN = r"^[A-HJ-NPR-Z0-9]{17}$"        # source: VINlookup.md §1 (excludes I,O,Q)
_YEAR_PASSTHROUGH = frozenset({"0", "U", "Z"}) # SAE J853 — non-year-coded placeholders
```

`pre_clean_vin`: `strip().upper()`, then `I→1`, `O→0`.

---

## 3. Checksum Bypass Sets (`decoder.py`)

```python
_EUROPEAN_COUNTRIES = frozenset({28 ISO-3166 European states})
    # source: Wikipedia European states + EC member/EEA — skip NHTSA check digit
_NON_NHTSA_COUNTRIES = frozenset({"JAPAN", "SOUTH KOREA", "INDIA"})
    # source: ISO 3780 — check digit mandatory only for US/CA/MX market
_OPSI_CHECKSUM_CORRUPT_PREFIXES = frozenset({"3MZ", "3MD", "3MV"})
    # source: T-FX-5 full-run — 1,866 Mexican Mazda VINs, corrupt pos-9 in Slovenian DMV data
```

Bypass order: non-NHTSA WMI → OPSI corrupt prefix → `vin[8] ∉ "123456789X"`.

---

## 4. Euro Normalisation (`decoder.py`)

```python
_EURO_MAP = {"euroN", "euro N" → "EURO_N"  for N in 1..7}   # source: SEMANTIC_CONTRACT §6.4
_normalise_euro(raw): None → "EURO_1"; else _EURO_MAP.get(key.strip().lower(), "EURO_1")
```

---

## 5. WMI Low-Volume Rule (`decoder.py::_resolve_wmi`)

```python
if vin[2] == "9":                       # source: SAE J853 low-volume (<500 units/yr)
    extended = vin[0:3] + vin[11:14]    # manufacturer code at positions 12-13
    if extended in wmi_index: return it
wmi_key = vin[0:3]                       # standard positions 1-3
```

---

## 6. Year Disambiguation (`decoder.py::_resolve_year`)

```python
year_char = vin[9]
if year_char in _YEAR_PASSTHROUGH: return (None, None)     # unknown, not an error
if len(candidates) == 1: return (int(calendar_year), None)
# L-collision (1990 vs 2020):
era_hint == "legacy" and era_bucket == "ERA_1" → 1990
era_hint != "legacy" and era_bucket == "ERA_3" → 2020
else → (first candidate, "era_hint_unrecognised")
```

**H2 scope guard:** `model_year is not None and (model_year < 1990 or > 2020)` →
`VINDecodeError`. (Years 1990–2020 inclusive.)

---

## 7. Engine Resolution Slices (`decoder.py::_resolve_engine`)

```python
vds_slice = vin[3:8]        # Path A — modern 5-char VDS
pos_8_char = vin[7]         # Path B — legacy single-char position-8
full_key = f"{BRAND}_{vds_slice}"   ; pos8_key = f"{BRAND}_{pos_8_char}"
```

---

## 8. Displacement & Tech-Mask Conversion (`decoder.py`)

```python
_engine_displacement_liters = disp_cc / 1000.0      # vref.db displacement_cc authoritative
_number_of_banks = 2 if db.is_v_engine else 1
downstream_o2_present = (model_year is not None and model_year >= 1996)  # source: OBD-II mandate
```

Bank inference from CSV `engine_configuration` (when `vref.db` absent): first char
`V`/`W` or `BOXER` prefix → `number_of_banks = 2`. W16/W12 are 4-bank in metal but the
contract caps at 2 for OBDLab routing (`# wiki: SEMANTIC_CONTRACT.md §4.1`).

---

## 9. Stress-Idle RPM Table (`overlay/stress_rpm.py`)

Source: `OBD_VOCABULARY.md §3.2` + T-VL-4 build rules. First match wins:

```python
EURO_1 & NATURALLY_ASPIRATED                         → 3000   # Euro 1 NA baseline
EURO_2/3 & NA & displacement < 2.0                   → 3500   # small-displacement
EURO_3/4 & NA & displacement >= 2.0                  → 4000   # large-displacement
EURO_4/5 & TURBOCHARGED                              → 4000   # boost ramps engage
EURO_5/6 & GDI                                       → 4500   # HPFP fully loaded
# horizon fallback when euro absent/unrecognised:
LEGACY → 3000 ; ADAPTIVE → 3500 ; MODERN/unknown → 4000
```

`VinDNA.stress_idle_rpm_target` default is `3000` (Euro 1 NA 1.0 L baseline, contract
§6.5).

---

## 10. Euro → Horizon Map (`overlay/horizon.py`)

Source: `SEMANTIC_CONTRACT §6.4`.

```python
EURO_1, EURO_2          → HORIZON_LEGACY
EURO_3, EURO_4          → HORIZON_ADAPTIVE
EURO_5, EURO_6, EURO_7  → HORIZON_MODERN
unknown                 → ValueError
# _year_to_horizon (used only when euro unknown):
1990-2000 → LEGACY ; 2001-2010 → ADAPTIVE ; else → MODERN
```

---

## 11. Upstream-O2 Derivation (`overlay/switches.py`)

Source: `OBD_VOCABULARY.md §4.3` + `SEMANTIC_CONTRACT §6.3`.

```python
o2_type_hint == "WB"                          → WIDEBAND_AFR
o2_type_hint == "NB"                          → NARROWBAND       # explicit hint wins
year >= 2001 and fuel ∈ {GDI, PORT_INJECTION} → WIDEBAND_AFR     # WB standard ~2001
fuel == CARBURETOR                            → NARROWBAND
default                                        → NARROWBAND
```

---

## 12. Cylinder Heuristic Constants (`overlay/cylinder_heuristic.py`)

Displacement-band fallback (`# source: T-VL-7 task spec`):

```python
disp <= 0    → (0,  unresolved)
disp <= 1.2  → (3,  "I3")
disp <= 2.5  → (4,  "I4")
disp <= 3.5  → (6,  "V6")
disp <= 5.0  → (8,  "V8")
disp >  5.0  → (12, "V12")
```

Brand family sets (transcribed verbatim from the task spec):

```python
_TOYOTA_I4 = {AZ,NR,NZ,ZZ,QR,AR} ; _TOYOTA_V6 = {GR,VZ,JZ,MZ} ; _TOYOTA_V8 = {UZ}
_NISSAN_I4 = {GA,CA,CR,QG,SR,HR,MR} ; _NISSAN_V6 = {VQ,VK} ; _NISSAN_TURBO_I4 = {TB}
_SUBARU_BOXER_4 = {EJ,FA,FB,EE} ; _SUBARU_BOXER_6 = {EZ}
_RENAULT_I4 = {K4M,H4M,K9K,F4R,F4P,K4J} ; _RENAULT_I3 = {H5F,D4F,H4Bt}
BMW turbo families = {N54,N55,B58,S55,S63}
_MERCEDES_TABLE = {M111/M271/M166→I4, M112/M272/M276→V6, M104→I6,
                   M113/M273/M278→V8, M275/M279/M137→V12}
```

The heuristic is a **last-resort fallback** — gated on `cylinder_count == 0`; it never
overwrites CSV or `vref.db` data, and the rule table must not be expanded without a
follow-up task.

---

## 13. Forbidden Patterns (VINLab-specific)

| Pattern | Enforcement |
|---------|-------------|
| `from gaslab/obdlab/dtclab/comlab/symptomlab import …` | DNA-family import boundary (one-way: `dnalab → vinlab`) |
| SQL string outside `db/tecdoc_query.py` | H8 SQL-isolation |
| Numeric literal without a `# source:`/`# wiki:` comment | code-review gate |
| Network or MySQL call at runtime | offline-runtime constraint (data baked into `vinlab/data/`) |
| New `VinDNA` field without a named consumer | signal/noise rule — field does not ship |
| Expanding `_BRAND_DISPATCH`/`_MERCEDES_TABLE` without a follow-up task | T-VL-7 scope lock |
| Re-running graphify against `graph/` | frozen verified artefact; not in the inner loop |
