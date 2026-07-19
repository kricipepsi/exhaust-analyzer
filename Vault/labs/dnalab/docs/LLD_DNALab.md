---
node_type: "lld"
lab: "dnalab"
module: "dnalab"
subsystem: "low-level-design"
implements:
  - "labs/dnalab/dnalab/__init__.py"
  - "labs/dnalab/dnalab/assembly.py"
  - "labs/dnalab/dnalab/models.py"
consumers:
  - "dld: labs/dnalab/docs/DLD_DNALab.md"
  - "comlab: OrchestratorInboundRequest.vehicle_dna ingestion"
drift_guards:
  - "labs/dnalab/tests/unit/test_assembly.py"
  - "labs/dnalab/tests/unit/test_models.py"
tags: [dnalab, finished, lld]
source: "labs/dnalab/docs/LLD_DNALab.md"
---
# LLD — DNALab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_DNALab v2.0
**HLD / DLD Reference:** HLD_DNALab v2.1 / DLD_DNALab v2.1
**Version:** 2.1
**Date:** 2026-06-12

DNALab carries no physics and no numeric thresholds. Its only "literals" are the schema
version, the session-id format, and the timestamp format.

---

## 1. Schema Version (`models.py`)

```python
SCHEMA_VERSION = "1.2"          # source: SEMANTIC_CONTRACT.md §4.3
```

The single coordinating constant. `from_json_payload` rejects any payload whose
`schema_version` differs (`ValueError`). T-DNA-7 bumped this `1.0 → 1.1` once upstream
field tasks landed; T-DNA-10 bumped it `1.1 → 1.2` for the `engine_state` wire-value
rename (`won_not_start` → `will_not_start`).

---

## 2. Session-ID Format (`models.py::VehicleDNA.new`)

```python
session_id = session_id or f"DNA_TX_{uuid.uuid4().hex[:10].upper()}"
```

`DNA_TX_` prefix + the first 10 hex characters of a UUID4, upper-cased. A caller-supplied
`session_id` is used verbatim. Tested by `test_assembly.py` (`startswith("DNA_TX_")`).

---

## 3. Timestamp Format (`models.py::VehicleDNA.new`)

```python
ts = (timestamp or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
```

ISO-8601 UTC, second precision, literal `Z` suffix. Tested against
`^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`.

---

## 4. Top-Level Key Set (`models.py::to_json_payload`)

```python
{"session_id", "timestamp", "schema_version", "vin_dna", "symptom_dna"}
```

Exactly five snake_case keys (`§4.3`). `vin_dna` / `symptom_dna` are produced by each
model's `to_json()` — DNALab never enumerates their inner fields.

---

## 5. Required Triage Keys (`assembly.py`)

```python
required = ("tier_1", "tier_2", "occurs_during", "engine_state", "load_state")
```

Checked before the VIN decode. `load_state` joined the required set in T-DNA-7 (and is
passed through to `resolve()`). `free_text_notes` is **not** required (optional on
`SymptomDNA`) and is not forwarded by the assembly.

---

## 6. Enum-Coercion Path (delegated)

DNALab performs no enum coercion of its own. `VinDNA.from_json` /`SymptomDNA.from_json`
coerce their respective enums; `VehicleDNA.from_json_payload` only routes the nested
dicts to them. This keeps the umbrella free of vocabulary knowledge.

---

## 7. Forbidden Patterns (DNALab-specific)

| Pattern | Enforcement |
|---------|-------------|
| `from comlab/gaslab/obdlab/dtclab import …` | only in-family imports allowed (`dnalab → vinlab + symptomlab`) |
| Duplicating `VinDNA` / `SymptomDNA` field knowledge in the umbrella | delegate to each model's `to_json`/`from_json` |
| Silent cross-`schema_version` load | `from_json_payload` must raise on mismatch |
| Defining validation that belongs to a producer | DNALab pre-checks triage-key presence only |
| Numeric/physics literals in `dnalab/` | none should exist — DNALab is composition, not computation |
