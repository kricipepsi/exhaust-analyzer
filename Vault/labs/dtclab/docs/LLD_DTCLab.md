---
node_type: "lld"
lab: "dtclab"
module: "dtclab"
subsystem: "low-level-design"
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
  - "dld: labs/dtclab/docs/DLD_DTCLab.md"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py DTCRoutingTag routing"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py DTCLabPayload integration"
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py HistoricalFaultContext / FuelSystemStatus comparison"
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py DTC_CONFIDENCE_WEIGHTS / Mode06MonitorState scoring"
  - "wired: labs/wired/wired/adapters/dtw.py T-DTW-1 adapter"
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
tags: [dtclab, finished, lld]
source: "labs/dtclab/docs/LLD_DTCLab.md"
---
# LLD — DTCLab
**Status:** Approved
**PRD Baseline:** PRD_DTCLab v2.0
**HLD / DLD Reference:** HLD_DTCLab v2.0 / DLD_DTCLab v2.0
**Version:** 2.0
**Date:** 2026-06-11

Convention: every numeric literal carries a `# wiki: <source> §<section>` comment in code.

> **v2.0 reconciliation note.** Reconciled to shipped `dtclab/`. Material changes from v1.0:
> the DNA gate dispatch is `_check_high_confidence_gate` with three named gates (no
> `secondary_air_equipped`, §7); `RoutingTagMapper.map` returns enum-definition order via a
> comprehension (§8); the Phase-2 scorer boundaries are added (§16).

---

## 1. DTC Format Regex — Exact String

Source: `DTC_VOCABULARY.md §2.3, §10`.

```python
DTC_REGEX: Final[str] = r"^[BCPU][0-3][0-9A-F]{3}$"
```

| Position | Pattern | Meaning |
|----------|---------|---------|
| 1 | `[BCPU]` | System: Body, Chassis, Powertrain, Network/Unknown |
| 2 | `[0-3]` | Sub-category: 0=SAE/generic, 1=mfr-specific, 2=SAE reserved, 3=mfr-specific |
| 3–5 | `[0-9A-F]{3}` | Hex fault code (uppercase only) |

Anchored `^...$` — partial matches rejected. Invalid forms (per `test_dtc_ingestion_gate.py`):
lowercase (`p0171`), too short (`P017`), too long (`P01711`), wrong system byte (`X0171`),
lowercase hex (`P0a71`).

---

## 2. Historical Context Classifier — Exact Boundary Values

Source: `DTC_VOCABULARY.md §9`. All comparisons are **strict inequalities**.

| Condition | Value | Result |
|-----------|-------|--------|
| `ECT == 60.0` | boundary | NOT COLD (exclusive) |
| `ECT == 59.9` | | COLD_START_TRANSIT_FAULT |
| `RPM == 1000` | boundary | NOT HISTORICAL_IDLE |
| `RPM == 999 AND load == 24.9` | | HISTORICAL_IDLE_FAULT |
| `RPM == 2000` | boundary | NOT HISTORICAL_LOAD |
| `RPM == 2001 AND load == 45.1` | | HISTORICAL_LOAD_FAULT |

Priority 1 (cold) always dominates: `ECT < 60` returns `COLD_START_TRANSIT_FAULT` before idle/load
are even evaluated.

---

## 3. Mode $06 Margin Tri-State — Exact Boundaries

Source: `DTC_VOCABULARY.md §7`.

```python
def classify_margin(margin_pct: float) -> Mode06MonitorState:
    if margin_pct <= 0:    return Mode06MonitorState.CRITICAL_FAIL
    if margin_pct <= 15:   return Mode06MonitorState.PENDING_FAIL_MARGINAL
    return Mode06MonitorState.PASSED
```

| Value | Result |
|-------|--------|
| `margin == 0.0` | CRITICAL_FAIL (boundary owned by fail side) |
| `margin == 0.001` | PENDING_FAIL_MARGINAL |
| `margin == 15.0` | PENDING_FAIL_MARGINAL (inclusive) |
| `margin == 15.001` | PASSED |
| `margin < 0` | CRITICAL_FAIL |

---

## 4. Freeze-Frame Symptom Flags — Exact Thresholds

Source: `DTC_VOCABULARY.md §12.3`.

```python
ff_open_loop_at_fault        = fuel_system_status in (OL, OL_FAULT, OL_DRIVE)
ff_load_high_at_low_rpm      = (calculated_load_pct > 70) and (engine_rpm < 1500)
ff_ect_warmup                = coolant_temp_c < 60
ff_iat_ect_biased            = (abs(intake_air_temp_c - coolant_temp_c) > 30) and (engine_rpm == 0)
ff_timing_retard_severe      = ignition_advance_deg < -10
ff_codes_cleared_invalidated = bool(codes_cleared)
```

Thresholds are strict (`<`, `>`) except `engine_rpm == 0` (equality). `ff_ect_warmup` and the
historical-context cold gate share the `< 60` boundary.

---

## 5. DTC Confidence Weights — Exact Values

Source: `DTC_VOCABULARY.md §16`. Consumed by COMLab aggregator **and** by `ranking.py`
(Phase-2 scorer). Not read by any `core/` module.

```python
DTC_CONFIDENCE_WEIGHTS: Final[Mapping[str, float]] = {
    "confirmed": 1.0, "permanent": 1.0, "pending": 0.5,
    "mode06_critical_fail": 0.7, "mode06_marginal": 0.4, "mode06_passed": 0.0,
}
```

Note: no drift-guard test for these values yet (open issue).

---

## 6. MID Key Pattern — Exact Regex

Source: `DTC_VOCABULARY.md §13.1`.

```python
MID_KEY_PATTERN: str = r"^MID_[0-9A-F]{2}_TID_[0-9A-F]{2}$"
```

Valid: `"MID_A2_TID_0B"`, `"MID_21_TID_81"`. Invalid: lowercase, missing TID, TID too long, extra
chars. MID hex is extracted by `mid_key.split("_")[1]`.

---

## 7. DNA-Gate Dispatch — `_check_high_confidence_gate`

Source: `DTC_VOCABULARY.md §4.1`. Reached only on `confidence == HIGH`.

```python
def _check_high_confidence_gate(self, gate_name: str) -> bool:
    emissions = self._dna_view.emissions
    if gate_name == "has_catalyst":
        return emissions.has_catalyst                 # wiki: §4.1
    if gate_name == "egr_equipped":
        return emissions.egr_equipped                 # wiki: §4.1
    logger.warning("unknown_dna_gate: gate=%s", gate_name)
    return True                                        # fail-open
```

**Exactly two named gates.** There is no `secondary_air_equipped` branch (SAI dropped — see DLD
§3). Unknown gate names fail **open** (emit) and log a warning.

---

## 8. RoutingTagMapper — Output Ordering

```python
def map(self, confirmed_dtcs: list[str]) -> list[DTCRoutingTag]:
    tags: set[DTCRoutingTag] = set()
    for dtc in confirmed_dtcs:
        for rule in self._rules:
            if _matches_any(dtc, rule.patterns) and self._gate_allows(rule.tag, rule.dna_gate):
                tags.add(rule.tag)
    return [t for t in list(DTCRoutingTag) if t in tags]   # enum-definition order
```

Deterministic regardless of DTC input order — `StrEnum` preserves definition order. Step 5b
(`evaluate_coolant_dtc_context`) may append `COOLANT_SYSTEM_MALFUNCTION` / `CYLINDER_FLUID_MISFIRE`
after this returns, so those two can appear out of enum order at the tail.

---

## 9. LRU Cache — Mode $06 Dictionary

```python
@functools.lru_cache(maxsize=4)
def _load_dictionary(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
```

`maxsize=4` = at most 4 distinct paths cached. In practice one path
(`mode_06_hex_dictionary.json`). `_lookup_component` returns `"UNKNOWN"` when the MID hex is
absent or its entry is not a dict; metadata keys (`_source_wiki`, `_description`) are never valid
2-hex MIDs so they never collide.

---

## 10. Config Path Resolution

```python
_CONFIG_DIR = Path(__file__).parent.parent / "config"
```

Resolved at module import. Missing config files surface as `FileNotFoundError` on first load —
fail-at-startup rather than fail-at-runtime.

---

## 11. Error Contracts

```python
class DTCFormatError(ValueError):
    def __init__(self, code: str, mode: str) -> None:
        self.code = code; self.mode = mode
        super().__init__(f"DTC {code!r} does not match {DTC_REGEX} (mode {mode})")

class FreezeFrameIncompleteError(ValueError):
    def __init__(self, missing: list[str]) -> None:
        self.missing = missing   # exact list of missing mandatory PID names
        super().__init__(f"Freeze frame incomplete — missing mandatory PIDs: {missing}")
```

COMLab must retry with a complete snapshot or mark the DTCLab output degraded when
`FreezeFrameIncompleteError` is raised.

---

## 12. POA_HISTORY Injection — Exact Contract (COMLab side)

Source: T-FX-3. `POA_HISTORY` is **never** produced inside DTCLab.

```python
# In COMLab (NOT inside RoutingTagMapper):
if gas_payload.chemical_state == ChemicalSignature.POA_SIGNATURE:
    if DTCRoutingTag.POA_HISTORY not in dtc_payload.routing_tags:
        dtc_payload = dtc_payload.model_copy(
            update={"routing_tags": [*dtc_payload.routing_tags, DTCRoutingTag.POA_HISTORY]}
        )
```

If `POA_HISTORY` appears in `RoutingTagMapper`'s output, that is a DTCLab bug.

---

## 13. `AirMeteringStrategy` and `ResolvedHorizon` Divergence

DTCLab values differ from OBDLab values. COMLab maps explicitly (no cross-lab enum import):

```python
# AirMeteringStrategy (OBDLab → DTCLab):
#   DUAL_MAF_MAP_CROSSCHECK → HYBRID            (approximate)
#   MAP_ONLY_SPEED_DENSITY  → MAP_SPEED_DENSITY
#   MAF_ONLY                → MAF
# ResolvedHorizon (OBDLab → DTCLab):
#   HORIZON_LEGACY   → HORIZON_LEGACY           (safe)
#   HORIZON_ADAPTIVE → HORIZON_CLASSIC          (intentional divergence)
#   HORIZON_MODERN   → HORIZON_MODERN           (safe)
```

---

## 14. Cross-Field Coolant/Fluid Signatures (step 5b)

Source: `CoolantLeakSig.md §4` (`evaluate_coolant_dtc_context`).

```python
if dtc_code in ("P0128", "P0117") and fuel_status == FuelSystemStatus.OL_FAULT:
    return "COOLANT_SYSTEM_MALFUNCTION"   # heat lost to boiling coolant; logger.warning
if dtc_code.startswith("P030") and fuel_status == FuelSystemStatus.CL:
    return "CYLINDER_FLUID_MISFIRE"       # liquid quenching spark; logger.info
return None
```

Both require **two** conditions (DTC match AND fuel-system status). Returns a tag **string**; the
sanitizer re-wraps into `DTCRoutingTag` and de-dups against existing tags.

---

## 15. Phase-2 Scorer Boundaries (`ranking.py`)

### MatchType ← weight mapping

```python
weight == 1.0  (confirmed/permanent)     → DEFINITIVE
weight == 0.5  (pending)                  → INDICATIVE
weight ∈ {0.7, 0.4} (critical/marginal)   → MONITOR_WEAK
else (0.0, passed)                        → MONITOR_PASS
```

### DNA confidence factor (`§14.2`)

```python
_DNA_FACTOR_HIGH = 1.0    # gate holds; full confidence
_DNA_FACTOR_PARTIAL = 0.7 # logged downgrade
_DNA_FACTOR_NONE = 0.5    # pure DTC-pattern (dna_view None ≡ NONE)
```

Applied to DNA-gated families only; ungated families multiply by 1.0.

### Confidence assembly

```python
raw_confidence = max_family_weight * dna_factor          # rank_candidates — NO clamp
confidence     = min(max(raw_confidence, 0.0), 1.0)      # classify_top3 — unit-interval clamp only
```

No family-keyed or tier-keyed ceiling constant (DESIGN §6). No sum-1 normalisation — COMLab
`combine()` owns that (DESIGN §4). Sort key throughout: `(-confidence, family)`; `classify_top3`
returns at most 3 deduplicated families.

---

## 16. Error Types and Codes

| Error | Raised when |
|-------|-------------|
| `DTCFormatError(ValueError)` | DTC fails `DTC_REGEX`; attributes: `code`, `mode` |
| `FreezeFrameIncompleteError(ValueError)` | Mandatory PID absent; attribute: `missing: list[str]` |
| `ValueError` | Invalid mode string (`"$03"`, `"$07"`, `"$0A"` only); invalid MID key |
| Pydantic `ValidationError` | `DTCLabPayload` field constraint; error codes `ERR-CONTRACT-001`, `ERR-CONTRACT-002` |

---

## 17. Forbidden Patterns (DTCLab-specific)

| Pattern | Enforcement |
|---------|-------------|
| `from gaslab import ...` / `from obdlab import ...` / `from comlab import ...` | Import-isolation audit in `test_dna_view.py` |
| `POA_HISTORY` in `routing_tag_map.yaml` | Convention; no automated test |
| `dtc_severity_map.yaml` loader | File does not exist; `DTCSeverityClass` is enum-only (reserved) |
| `secondary_air_equipped` / `SAI_HISTORY` | Dropped from 4DLab (`wiki §11.4`); must not reappear |
| Diesel-specific DTC patterns | `PRD_4D_App.md §5` scope exclusion |
| Adding a `DTCLabPayload` field without a named COMLab consumer | Signal/noise rule — field does not ship |
