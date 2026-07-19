---
node_type: dld
lab: dtclab
module: dtclab
subsystem: detailed-design
implements:
  - "labs/dtclab/dtclab/core/dtc_ingestion_gate.py"
  - "labs/dtclab/dtclab/core/historical_context_classifier.py"
  - "labs/dtclab/dtclab/core/mode06_evaluator.py"
  - "labs/dtclab/dtclab/core/freeze_frame_extractor.py"
  - "labs/dtclab/dtclab/core/routing_tag_mapper.py"
  - "labs/dtclab/dtclab/core/data_fusion_sanitizer.py"
  - "labs/dtclab/dtclab/family_map.py"
  - "labs/dtclab/dtclab/ranking.py"
  - "labs/dtclab/dtclab/schemas/vocabulary.py"
  - "labs/dtclab/dtclab/schemas/dna_view.py"
  - "labs/dtclab/dtclab/schemas/payload.py"
  - "labs/dtclab/dtclab/schemas/freeze_frame.py"
  - "labs/dtclab/dtclab/schemas/mode06_result.py"
  - "labs/dtclab/dtclab/config/routing_tag_map.yaml"
  - "labs/dtclab/dtclab/config/mode_06_hex_dictionary.json"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py DTCRoutingTag routing"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py DTCLabPayload integration"
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py rich_dtc_present (P0172/P0175) gate"
  - "wired (pending T-WIRE-1): apps/wired/wired/composition.py DTCLabPayload mapping"
drift_guards:
  - "labs/dtclab/tests/unit/test_dtc_ingestion_gate.py"
  - "labs/dtclab/tests/unit/test_freeze_frame_extractor.py"
  - "labs/dtclab/tests/unit/test_historical_context_classifier.py"
  - "labs/dtclab/tests/unit/test_mode06_evaluator.py"
  - "labs/dtclab/tests/unit/test_routing_tag_mapper.py"
  - "labs/dtclab/tests/unit/test_classify_top3.py"
  - "labs/dtclab/tests/unit/test_rank_candidates.py"
  - "labs/dtclab/tests/unit/test_family_map.py"
  - "labs/dtclab/tests/unit/test_payload.py"
  - "labs/dtclab/tests/unit/test_vocabulary.py"
  - "labs/dtclab/tests/unit/test_dna_view.py"
  - "labs/dtclab/tests/integration/test_dtclab_pipeline.py"
tags: [dtclab, detailed-design, dld]
source: "labs/dtclab/docs/DLD_DTCLab.md"
---
# DLD — DTCLab
**Status:** Approved
**PRD Baseline:** PRD_DTCLab v2.0
**HLD Reference:** HLD_DTCLab v2.0
**Version:** 2.0
**Date:** 2026-06-11

> **v2.0 reconciliation note.** Reconciled to the shipped `dtclab/` package. Material
> changes from v1.0: `DTCRoutingTag` is **18** members (drop `SAI_HISTORY`; add
> `COOLANT_SYSTEM_MALFUNCTION`, `CYLINDER_FLUID_MISFIRE`); `DtcEmissionsView` has **3**
> fields; **5** DNA-gated YAML entries; new package-root modules `family_map.py` and
> `ranking.py` documented (§15–§16).

---

## 1. Module Map

```
dtclab/
├── __init__.py                          ← exports DataFusionSanitizer
├── family_map.py                        ← routing-tag → canonical-family map (Phase-2 input)
├── ranking.py                           ← Phase-2 scorer (rank_candidates / classify_top3)
├── core/
│   ├── data_fusion_sanitizer.py         ← public entry point (sanitize)
│   ├── dtc_ingestion_gate.py
│   ├── freeze_frame_extractor.py        ← incl. evaluate_coolant_dtc_context (step 5b)
│   ├── historical_context_classifier.py
│   ├── mode06_evaluator.py
│   └── routing_tag_mapper.py
├── schemas/
│   ├── dna_view.py
│   ├── freeze_frame.py
│   ├── mode06_result.py
│   ├── payload.py
│   └── vocabulary.py
└── config/
    ├── mode_06_hex_dictionary.json
    └── routing_tag_map.yaml
```

`__init__.py` re-exports only `DataFusionSanitizer` (`__all__ = ["DataFusionSanitizer"]`). The
Phase-2 scorer is imported directly from `dtclab.ranking` by the Wired adapter (`T-DTW-1`).

---

## 2. `schemas/vocabulary.py` — Enums and Constants

All enums are `StrEnum`. Source: `DTC_VOCABULARY.md` (drift-guarded by `test_vocabulary.py`).

| Enum | Members |
|------|---------|
| `DTCRoutingTag` | `LEAN_HISTORY`, `RICH_HISTORY`, `MISFIRE_HISTORY`, `CATALYST_HISTORY`, `EGR_HISTORY`, `O2_HISTORY`, `INJECTOR_HISTORY`, `VVT_HISTORY`, `EVAP_HISTORY`, `THERMAL_HISTORY`, `ECU_INTERNAL_HISTORY`, `POA_HISTORY`, `IDLE_CONTROL_HISTORY`, `BOOST_HISTORY`, `KNOCK_HISTORY`, `COOLANT_SYSTEM_MALFUNCTION`, `CYLINDER_FLUID_MISFIRE` (**17**) |
| `DTCSeverityClass` | `A`, `B`, `C`, `D` (SAE J2012) — enum only; no loader (reserved) |
| `DTCState` | `PENDING`, `CONFIRMED`, `PERMANENT` — reserved contract surface; not read by production code |
| `Mode06MonitorState` | `PASSED`, `PENDING_FAIL_MARGINAL`, `CRITICAL_FAIL` |
| `FuelSystemStatus` | `CL`, `OL`, `OL_DRIVE`, `OL_FAULT` |
| `HistoricalFaultContext` | `HISTORICAL_IDLE_FAULT`, `HISTORICAL_LOAD_FAULT`, `COLD_START_TRANSIT_FAULT`, `UNKNOWN` |

Constants:

```python
DTC_REGEX: Final[str] = r"^[BCPU][0-3][0-9A-F]{3}$"   # wiki: §2.3, §10

DTC_CONFIDENCE_WEIGHTS: Final[Mapping[str, float]] = {
    "confirmed":            1.0,   # wiki: §16
    "permanent":            1.0,   # wiki: §16
    "pending":              0.5,   # wiki: §16
    "mode06_critical_fail": 0.7,   # wiki: §16
    "mode06_marginal":      0.4,   # wiki: §16
    "mode06_passed":        0.0,   # wiki: §16
}
```

`DTC_CONFIDENCE_WEIGHTS` is consumed by COMLab's aggregator **and** by the Phase-2 scorer
(`ranking.py`). No `core/` module reads it.

---

## 3. `schemas/dna_view.py`

### Enums

| Enum | Members | Note |
|------|---------|------|
| `EuroEmissionCategory` | `EURO_1`–`EURO_7`, `UNKNOWN` | Local mirror (no `dnalab` import) |
| `AirMeteringStrategy` | `MAF`, `MAP_SPEED_DENSITY`, `HYBRID` | Different values from OBDLab — COMLab maps |
| `ResolvedHorizon` | `HORIZON_LEGACY`, `HORIZON_CLASSIC`, `HORIZON_MODERN` | `HORIZON_CLASSIC` ≠ OBDLab's `HORIZON_ADAPTIVE` |
| `VinConfidence` | `HIGH`, `PARTIAL`, `NONE` | Same as OBDLab |

### `DtcEmissionsView` (3 fields)

| Field | Type | Routing gate use |
|-------|------|----------------|
| `has_catalyst` | `bool` | `CATALYST_HISTORY` gate (`has_catalyst`) |
| `egr_equipped` | `bool` | `EGR_HISTORY` gate (`egr_equipped`) |

> `secondary_air_equipped` / `SAI_HISTORY` are **not** in shipped code. SAI was dropped from
> 4DLab (`wiki/11_proposals_register.md §11.4`): cold-start light-off (~260 °C) is unreadable at
> the ≥ 75 °C read-floor.

### `DtcLabDnaView` (8 fields)

`make`, `model`, `model_year`, `euro_emission_category`, `air_metering_strategy`,
`resolved_horizon`, `emissions` (`DtcEmissionsView`), `confidence` (`VinConfidence`).

---

## 4. `schemas/payload.py` — `DTCLabPayload` (9 fields)

| Field | Type | Validator | COMLab Consumer |
|-------|------|----------|----------------|
| `active_mil` | `bool` | | Severity context |
| `mil_flashing` | `bool` | | Severity context |
| `confirmed_dtcs` | `list[str]` | `DTC_REGEX` per item → `ERR-CONTRACT-001` | Routing; OBD analytics gating |
| `pending_dtcs` | `list[str]` | `DTC_REGEX` per item → `ERR-CONTRACT-001` | Stored |
| `permanent_dtcs` | `list[str]` | `DTC_REGEX` per item → `ERR-CONTRACT-001` | Stored |
| `routing_tags` | `list[DTCRoutingTag]` | Valid member → `ERR-CONTRACT-002` | Fault-atlas routing; Phase-2 scorer seed |
| `mode_06_monitors` | `dict[str, Mode06MonitorResult]` | Key matches `MID_KEY_PATTERN` | Confidence scoring |
| `historical_fault_context` | `HistoricalFaultContext` | | Temporal fault ranking |
| `freeze_frame` | `FreezeFrameRecord` | | Healing delta; OBDLab forwarding |

Validators: `_validate_dtc_list` (three DTC lists), `_validate_routing_tags` (mode="before"),
`_validate_monitor_keys` (Mode $06 keys).

---

## 5. `schemas/freeze_frame.py` — `FreezeFrameRecord`

12 mandatory PIDs:

| Field | Type | Constraints |
|-------|------|------------|
| `calculated_load_pct` | `float` | `[0, 100]` |
| `engine_rpm` | `int` | `≥ 0` |
| `coolant_temp_c` | `float` | any (negative legal) |
| `short_term_ft1` | `float` | |
| `long_term_ft1` | `float` | |
| `manifold_pressure_kpa` | `float` | `≥ 0` |
| `vehicle_speed_kmh` | `int` | `≥ 0` |
| `ignition_advance_deg` | `float` | any (negative = retard) |
| `intake_air_temp_c` | `float` | any (negative legal) |
| `maf_gps` | `float` | `≥ 0` |
| `throttle_pos_pct` | `float` | `[0, 100]` |
| `fuel_system_status` | `FuelSystemStatus` | |

7 optional extended PIDs: `short_term_ft2`, `long_term_ft2`, `o2_voltage_b1s1`,
`barometric_pressure_kpa`, `commanded_egr_pct`, `run_time_since_start_sec`, `fuel_level_pct`.

6 derived symptom flags (all `bool`, default `False`): `ff_open_loop_at_fault`,
`ff_load_high_at_low_rpm`, `ff_ect_warmup`, `ff_iat_ect_biased`, `ff_timing_retard_severe`,
`ff_codes_cleared_invalidated`.

---

## 6. `schemas/mode06_result.py`

```python
MID_KEY_PATTERN: str = r"^MID_[0-9A-F]{2}_TID_[0-9A-F]{2}$"
```

`Mode06MonitorResult` (4 fields): `monitor_id` (pattern-validated), `state`
(`Mode06MonitorState`), `margin_pct` (`float`), `target_component` (`str`).

---

## 7. `core/dtc_ingestion_gate.py`

### `validate_dtc_list(codes: list[str], mode: str) → list[str]`

```
1. If mode not in ("$03", "$07", "$0A"): raise ValueError
2. For each code in codes:
     if not _COMPILED_REGEX.match(code): raise DTCFormatError(code, mode)
3. Return codes unchanged (pass-through)
```

`DTCFormatError(ValueError)`: attributes `code`, `mode`. Fail-fast — stops on first invalid code.

---

## 8. `core/freeze_frame_extractor.py`

### `extract_freeze_frame(raw: dict, codes_cleared: bool = False) → FreezeFrameRecord`

```
1. Check all 12 mandatory keys — None or absent → FreezeFrameIncompleteError(missing=[...])
2. Pydantic construction with coercion: "800" → 800; "OL_FAULT" → FuelSystemStatus.OL_FAULT
3. Derive 6 symptom flags via model_copy(update={...}):
     ff_open_loop_at_fault        ← fuel_system_status in (OL, OL_FAULT, OL_DRIVE)
     ff_load_high_at_low_rpm      ← calculated_load_pct > 70 AND engine_rpm < 1500
     ff_ect_warmup                ← coolant_temp_c < 60
     ff_iat_ect_biased            ← abs(iat - ect) > 30 AND engine_rpm == 0
     ff_timing_retard_severe      ← ignition_advance_deg < -10
     ff_codes_cleared_invalidated ← bool(codes_cleared)
4. Return FreezeFrameRecord with flags populated
```

### `evaluate_coolant_dtc_context(dtc_code, fuel_status) → str | None`  *(step 5b)*

Cross-field coolant/fluid signature detector (CoolantLeakSig.md §4):

```
dtc_code in ("P0128","P0117") AND fuel_status == OL_FAULT → "COOLANT_SYSTEM_MALFUNCTION"
dtc_code.startswith("P030")   AND fuel_status == CL       → "CYLINDER_FLUID_MISFIRE"
otherwise                                                  → None
```

Returns the **string value** of a `DTCRoutingTag`; the sanitizer wraps it back into the enum
and appends if not already present.

---

## 9. `core/historical_context_classifier.py`

### `classify_historical_context(coolant_temp_c, engine_rpm, calculated_load_pct) → HistoricalFaultContext`

```
Priority 1: coolant_temp_c < 60                               → COLD_START_TRANSIT_FAULT
Priority 2: engine_rpm < 1000 AND calculated_load_pct < 25    → HISTORICAL_IDLE_FAULT
Priority 3: engine_rpm > 2000 AND calculated_load_pct > 45    → HISTORICAL_LOAD_FAULT
Default:                                                        → UNKNOWN
```

All comparisons are strict inequalities. Source: `DTC_VOCABULARY.md §9`.

---

## 10. `core/mode06_evaluator.py`

### `classify_margin(margin_pct: float) → Mode06MonitorState`

```
margin_pct ≤ 0    → CRITICAL_FAIL
0 < margin ≤ 15   → PENDING_FAIL_MARGINAL
margin > 15       → PASSED
```

### `evaluate_monitor(mid_key, margin_pct, dictionary_path) → Mode06MonitorResult`

```
1. Validate mid_key against MID_KEY_PATTERN → ValueError on miss
2. state = classify_margin(margin_pct)
3. mid_hex = mid_key.split("_")[1]            # "MID_21_TID_81" → "21"
4. dictionary = _load_dictionary(dictionary_path)   # @lru_cache(maxsize=4)
5. component = _lookup_component(mid_hex, dictionary)   # "UNKNOWN" if absent
6. Return Mode06MonitorResult(monitor_id, state, margin_pct, target_component)
```

`_load_dictionary` uses `@functools.lru_cache(maxsize=4)`. Metadata keys (`_source_wiki`,
`_description`) are absent from MID lookups because they are not valid 2-hex MIDs.

---

## 11. `core/routing_tag_mapper.py` — `RoutingTagMapper`

### Constructor: `__init__(map_path, dna_view)`

Loads `routing_tag_map.yaml` into `list[_RoutingRule(patterns, tag, dna_gate)]`.

### `map(confirmed_dtcs: list[str]) → list[DTCRoutingTag]`

```
tags = set()
For each dtc in confirmed_dtcs:
  For each rule in rules:
    if any(p.match(dtc) for p in rule.patterns):
      if _gate_allows(rule.tag, rule.dna_gate):
        tags.add(rule.tag)
Return [t for t in list(DTCRoutingTag) if t in tags]   # enum-definition order
```

### `_gate_allows(tag, gate_name) → bool`

```
gate_name is None     → True (ungated)
dna_view is None      → True (None ≡ NONE)
confidence == NONE    → True
confidence == PARTIAL → True + logger.info("dna_gate_downgraded")
confidence == HIGH    → _check_high_confidence_gate(gate_name)
```

### `_check_high_confidence_gate(gate_name) → bool`

```
"has_catalyst"  → dna_view.emissions.has_catalyst
"egr_equipped"  → dna_view.emissions.egr_equipped
unknown         → True + logger.warning("unknown_dna_gate")   # fail-open
```

Exactly three named gates. `POA_HISTORY` is never produced here.

---

## 12. `core/data_fusion_sanitizer.py` — `DataFusionSanitizer`

Config paths resolved at module load:

```python
_CONFIG_DIR             = Path(__file__).parent.parent / "config"
_ROUTING_TAG_MAP_PATH   = _CONFIG_DIR / "routing_tag_map.yaml"
_MODE06_DICTIONARY_PATH = _CONFIG_DIR / "mode_06_hex_dictionary.json"
```

### `sanitize(raw_dtcs, raw_freeze_frame, raw_mode06, *, codes_cleared=False, active_mil=False, mil_flashing=False) → DTCLabPayload`

Executes the pipeline (HLD §3), including **step 5b** (`evaluate_coolant_dtc_context` over each
confirmed DTC, appending coolant/fluid tags), then calls `DTCLabPayload.model_validate(...)` and
logs `dtclab_payload_emitted`.

---

## 13. `family_map.py` — Routing-tag → canonical-family map  *(Phase-2 input)*

`CANONICAL_FAMILIES` is the 16-family set mirrored from COMLabSimple (no cross-lab import):
`lean_condition`, `rich_mixture`, `misfire`, `sensor_fault`, `ecu_fault`, `catalyst_failure`,
`exhaust_leak`, `ignition_fault`, `mechanical_wear`, `cam_timing`, `non_starter`, `no_fault`,
`invalid_input`, `vacuum_leak`, `overheating`, `charging_system`.

`ROUTING_TAG_TO_FAMILY: dict[DTCRoutingTag, str | None]` maps each tag to one canonical family
or `None` (context-only / not voted on):

| Routing tag | Canonical family |
|---|---|
| `LEAN_HISTORY` | `lean_condition` |
| `RICH_HISTORY` | `rich_mixture` |
| `MISFIRE_HISTORY` | `misfire` |
| `CATALYST_HISTORY` | `catalyst_failure` |
| `O2_HISTORY` | `sensor_fault` |
| `VVT_HISTORY` | `cam_timing` |
| `ECU_INTERNAL_HISTORY` | `ecu_fault` |
| `KNOCK_HISTORY` | `ignition_fault` |
| `INJECTOR_HISTORY` | `mechanical_wear` |
| `POA_HISTORY` | `None` — COMLab injects from GASLab |
| `EGR_HISTORY`, `EVAP_HISTORY`, `THERMAL_HISTORY`, `IDLE_CONTROL_HISTORY`, `BOOST_HISTORY`, `COOLANT_SYSTEM_MALFUNCTION`, `CYLINDER_FLUID_MISFIRE` | `None` — context-only |

`families_for_tags(tags) → list[str]` strips `None`, dedups, preserves insertion order.

---

## 14. `ranking.py` — Phase-2 scorer

### `MatchType(StrEnum)`

`DEFINITIVE` (weight 1.0 — CONFIRMED/PERMANENT), `INDICATIVE` (0.5 — PENDING),
`MONITOR_WEAK` (0.7/0.4 — Mode $06 CRITICAL_FAIL/MARGINAL), `MONITOR_PASS` (0.0 — Mode $06 PASSED).

### `CandidateScore` (frozen dataclass)

`family: str`, `raw_confidence: float`, `match_type: MatchType`.

### DNA confidence factors (`§14.2`)

`_DNA_FACTOR_HIGH = 1.0`, `_DNA_FACTOR_PARTIAL = 0.7`, `_DNA_FACTOR_NONE = 0.5`.

### `rank_candidates(payload, *, dna_view=None) → list[CandidateScore]`

```
1. Seed each family reachable from payload.routing_tags (via ROUTING_TAG_TO_FAMILY)
   at the PASSED weight (0.0).
2. DTC evidence: for confirmed(1.0)/permanent(1.0)/pending(0.5), match each DTC
   against the routing rules; take per-family MAX weight; record MatchType.
3. Mode $06 evidence: global-max monitor weight across all monitors, applied to
   every active family if it raises the family's max.
4. raw_confidence = max_weight × DNA factor (gated families only); no clamp.
5. Sort by (-raw_confidence, family).
```

### `classify_top3(payload, *, dna_view=None) → list[tuple[str, float]]`

Clamps each `raw_confidence` to `[0,1]`, dedups families (keep max), re-sorts
`(-confidence, family)`, returns at most 3. **No sum-1 normalisation** — COMLab `combine()`
does fusion/normalisation (FU-1). No `LabResult` construction — that is the Wired adapter
(`T-DTW-1`).

---

## 15. `config/routing_tag_map.yaml` — Schema and DNA-Gated Entries

```yaml
entries:
  - patterns: ["<regex>", ...]
    tag: <DTCRoutingTag string value>
    source_wiki: "DTC_VOCABULARY.md §15"
    [dna_gate: <gate_name>]
```

**32 entries total — 27 ungated, 5 DNA-gated:**

| Patterns | Tag | Gate |
|---------|-----|------|
| `^P040[0-9]$` | `EGR_HISTORY` | `egr_equipped` |
| `^P0420$` | `CATALYST_HISTORY` | `has_catalyst` |
| `^P0430$` | `CATALYST_HISTORY` | `has_catalyst` |

`POA_HISTORY`, `COOLANT_SYSTEM_MALFUNCTION`, and `CYLINDER_FLUID_MISFIRE` have **no** YAML entry:
the first is injected by COMLab (T-FX-3); the latter two come from step 5b
(`evaluate_coolant_dtc_context`), not pattern matching.

---

## 16. Test Coverage

| File | Coverage |
|------|---------|
| `test_dtc_ingestion_gate.py` | valid/invalid codes, 3 modes, fail-on-first, empty list, unknown-mode `ValueError` |
| `test_freeze_frame_extractor.py` | 12-PID happy path, all 6 flags at boundary, missing PID error, extended PIDs, string coercion, Pydantic constraint failures |
| `test_historical_context_classifier.py` | Priority order, ECT=60 boundary, both-conditions-required |
| `test_mode06_evaluator.py` | margin boundaries, valid/invalid keys, component lookup, LRU-cache ≤ 1 open |
| `test_routing_tag_mapper.py` | fan-out, DNA gates (HIGH/PARTIAL/NONE), POA never emitted, `dna_view=None` |
| `test_classify_top3.py` / `test_rank_candidates.py` | Phase-2 scorer: weight selection, DNA factor, clamp, dedup, top-3 ordering |
| `test_family_map.py` | tag→family map, `None` handling, `families_for_tags` dedup/order |
| `test_payload.py` | Round-trip, JSON, malformed DTC, lowercase rejection, ERR-CONTRACT-001/002 |
| `test_vocabulary.py` | enum drift guards vs `DTC_VOCABULARY.md`, `DTC_REGEX` exact string |
| `test_dna_view.py` | field sets (8 + 2), enum counts, drift guard, round-trips, import isolation |
| `test_dtclab_pipeline.py` | integration: HIGH-with-catalyst, catalyst/EGR suppressed, no-DNA, historical context |
| `test_dtclab_regression.py` | named fixtures: routing tags, historical context, freeze-frame flags, structure validity |
