---
node_type: hld
lab: dtclab
module: dtclab
subsystem: architecture
implements:
consumers:
  - "lld: labs/dtclab/docs/LLD_DTCLab.md"
  - "dld: labs/dtclab/docs/DLD_DTCLab.md"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py DTCRoutingTag routing"
drift_guards:
tags: [dtclab, architecture, hld]
source: "labs/dtclab/docs/HLD_DTCLab.md"
---
# HLD — DTCLab
**Status:** Approved
**PRD Baseline:** PRD_DTCLab v2.0
**Version:** 2.0
**Date:** 2026-06-11

> **v2.0 reconciliation note.** This revision reconciles the HLD to the shipped
> `dtclab/` package (AST ground truth, June 2026). Changes from v1.0: the routing
> surface is **18** `DTCRoutingTag` values (not 17 — `SAI_HISTORY` was never shipped;
> `COOLANT_SYSTEM_MALFUNCTION` and `CYLINDER_FLUID_MISFIRE` are added); `DtcEmissionsView`
> carries **3** flags (no `secondary_air_equipped`); the routing map has **5** DNA-gated
> entries (not 6); and the **Phase-2 scorer** (`ranking.py`) and **family map**
> (`family_map.py`) are now documented.

---

## 1. Responsibility

DTCLab validates raw DTC lists, extracts and annotates freeze-frame data, classifies
historical fault context, evaluates Mode $06 monitor margins, and maps confirmed DTCs to
routing tags. It emits a typed `DTCLabPayload` consumed by COMLab. A second, optional
surface — the **Phase-2 scorer** — turns that payload into ranked `(fault_family, confidence)`
candidates for COMLab's Bayesian fusion.

DTCLab covers OBD-II layers L3 (stored DTCs), L4 (freeze-frame snapshot), and the Mode $06
on-board monitor data.

---

## 2. Architecture Position

```
COMLab
  │  constructs DtcLabDnaView from VIN record (COMLab.project(..., target='dtc'))
  │  supplies raw DTC dict, raw freeze-frame dict, raw Mode $06 dict
  ▼
dtclab.DataFusionSanitizer.sanitize(raw_dtcs, raw_freeze_frame, raw_mode06, ...)
  │
  ├─ dtc_ingestion_gate.validate_dtc_list       — format validation × 3 modes
  ├─ freeze_frame_extractor.extract_freeze_frame — 12 PIDs + 6 flags
  ├─ historical_context_classifier              — 4-state temporal context
  ├─ mode06_evaluator.evaluate_monitor × N      — tri-state per MID
  ├─ RoutingTagMapper.map(confirmed_dtcs)        — 18-tag routing (DNA-gated)
  ├─ evaluate_coolant_dtc_context × N            — cross-field coolant/fluid tags
  └─ DTCLabPayload.model_validate               — Pydantic validation
  │
  DTCLabPayload (9 fields)
  │
  ├──────────────► COMLab fault-atlas router (routing_tags, mode_06_monitors,
  │                historical_fault_context, freeze_frame)
  │
  └─ ranking.classify_top3(payload, dna_view=...)  — OPTIONAL Phase-2 scorer
        │  top-3 (canonical_family, confidence ∈ [0,1])
        ▼
     COMLab Bayesian combine() (FU-1), via the Wired adapter (T-DTW-1)
```

Zero cross-lab Python imports. DTCLab mirrors the DNA-view types it needs locally. Isolation
enforced by the `test_dna_view.py` import audit.

---

## 3. Internal Pipeline (Phase 1 — `sanitize`)

```
raw_dtcs + raw_freeze_frame + raw_mode06 + DtcLabDnaView
       │
  [1]  validate_dtc_list  (× 3 modes)
       │  mode "$03" confirmed, "$07" pending, "$0A" permanent
       │  Regex: ^[BCPU][0-3][0-9A-F]{3}$
       │  Fail-fast on first invalid code → DTCFormatError
       │
  [2]  extract_freeze_frame(raw_freeze_frame, codes_cleared)
       │  12 mandatory PIDs checked → FreezeFrameIncompleteError if any absent
       │  String→enum coercion: "OL_FAULT" → FuelSystemStatus.OL_FAULT
       │  6 derived symptom flags (open-loop, load@low-rpm, ECT warm-up,
       │                           IAT/ECT bias, timing retard, codes-cleared)
       │
  [3]  classify_historical_context(ECT, RPM, load)
       │  Priority: COLD_START_TRANSIT_FAULT > HISTORICAL_IDLE_FAULT >
       │            HISTORICAL_LOAD_FAULT > UNKNOWN
       │
  [4]  evaluate_monitor(mid_key, margin_pct)  (× N monitors in raw_mode06)
       │  LRU-cached dictionary load (mode_06_hex_dictionary.json, 33 MIDs)
       │  Tri-state: CRITICAL_FAIL (≤0) / PENDING_FAIL_MARGINAL (1–15) / PASSED (≥16)
       │
  [5]  RoutingTagMapper.map(confirmed_dtcs)
       │  Loads routing_tag_map.yaml: 30 entries (27 ungated + 3 DNA-gated)
       │  DNA confidence three-branch: HIGH strict / PARTIAL log+emit / NONE emit
       │  Result: deduplicated list, enum-definition order
       │  NOTE: POA_HISTORY never emitted here (injected by COMLab, T-FX-3)
       │
  [5b] evaluate_coolant_dtc_context(dtc, fuel_system_status)  (× confirmed DTC)
       │  Cross-field signatures (CoolantLeakSig.md §4):
       │    P0128/P0117 in OL_FAULT → COOLANT_SYSTEM_MALFUNCTION
       │    P030x       in CL       → CYLINDER_FLUID_MISFIRE
       │  Appended to routing_tags if not already present
       │
  [6]  DTCLabPayload.model_validate
       │  Pydantic field validation + ERR-CONTRACT-001 / ERR-CONTRACT-002 error codes
       │
  DTCLabPayload
```

---

## 4. Phase-2 Scorer (`ranking.py`) — optional candidate ranking

`rank_candidates()` / `classify_top3()` turn a `DTCLabPayload` into ranked fault-family
candidates. This surface is **not** called by `sanitize`; the Wired composition layer
(`T-DTW-1`) calls it directly and adapts the result into COMLab's `LabResult` for Bayesian
fusion (`combine()`, FU-1). Its consumers are therefore real and existing once the Wired
adapter is wired.

```
classify_top3(payload, dna_view=…)
  │
  rank_candidates(payload, dna_view=…)
     1. Seed each canonical family reachable from payload.routing_tags
        (family map: routing tag → one of the 16 canonical families | None).
     2. Per family, take the MAX §16 confidence weight across contributing
        DTCs (confirmed/permanent = 1.0, pending = 0.5) and the global-max
        Mode $06 monitor weight (CRITICAL_FAIL = 0.7, MARGINAL = 0.4, PASSED = 0.0).
     3. Multiply by the §14.2 DNA confidence factor for DNA-gated families
        (HIGH = 1.0, PARTIAL = 0.7, NONE/None = 0.5).
     4. Tag each candidate with a MatchType evidence tier from its strongest source.
  │  → CandidateScore(family, raw_confidence, match_type), sorted (-confidence, family)
  ▼
  clamp each raw_confidence to [0,1], dedup families (keep max), return top 3
  → list[(canonical_family, confidence)]   (no sum-1 normalisation — combine() does that)
```

`MatchType` evidence tiers: `DEFINITIVE` (1.0), `INDICATIVE` (0.5), `MONITOR_WEAK` (0.7/0.4),
`MONITOR_PASS` (0.0). The scorer adds **no new numeric literal** — every value is sourced from
`DTC_CONFIDENCE_WEIGHTS` (§16) and the §14.2 DNA factors.

---

## 5. Routing Tag Architecture

18 `DTCRoutingTag` values map DTC families to COMLab fault-atlas nodes:

```
LEAN_HISTORY               ← P0171, P0174, P0100–P0115, P0230–P0233
RICH_HISTORY               ← P0172, P0175
MISFIRE_HISTORY            ← P0300–P0312, P0335/P0340, P0351–P0358
CATALYST_HISTORY           ← P0420, P0430              (DNA-gated: has_catalyst)
EGR_HISTORY                ← P0400–P0409               (DNA-gated: egr_equipped)
O2_HISTORY                 ← P0130–P0167
INJECTOR_HISTORY           ← P0200–P0212
VVT_HISTORY                ← P0010–P0023
EVAP_HISTORY               ← P0440–P0459
THERMAL_HISTORY            ← P0116–P0128
ECU_INTERNAL_HISTORY       ← P0562/P0563, P0600, P0601–P0606, P0641–P0643
POA_HISTORY                ← (COMLab-injected, T-FX-3 — never emitted by DTCLab)
IDLE_CONTROL_HISTORY       ← P0505–P0511
BOOST_HISTORY              ← P0234, P0299, P0235–P0245
KNOCK_HISTORY              ← P0325–P0334
COOLANT_SYSTEM_MALFUNCTION ← P0128/P0117 in OL_FAULT   (cross-field, step 5b)
CYLINDER_FLUID_MISFIRE     ← P030x in CL               (cross-field, step 5b)
```

The 16 directly-pattern-matched tags come from `routing_tag_map.yaml`; the last two are
cross-field signatures from `evaluate_coolant_dtc_context` (step 5b). `POA_HISTORY` carries no
DTC and is injected by COMLab.

---

## 6. DNA-Gate Architecture

Two distinct DNA mechanisms, both keyed on `DtcLabDnaView.confidence`:

**(a) RoutingTagMapper gate — binary emit/suppress.** Three-branch confidence pattern
(identical in shape to GASLab and OBDLab):

```
gate_name is None                     → Always emit (ungated)
dna_view is None                      → Always emit (None ≡ NONE)
confidence == NONE                    → Always emit (pure DTC-pattern routing)
confidence == PARTIAL                 → Emit + logger.info("dna_gate_downgraded")
confidence == HIGH                    → _check_high_confidence_gate(gate_name)
```

HIGH-confidence gate checks (the only three named gates in shipped code):

| Gate name | Condition |
|-----------|-----------|
| `has_catalyst` | `emissions.has_catalyst` |
| `egr_equipped` | `emissions.egr_equipped` |
| unknown gate | Fail-open + `logger.warning("unknown_dna_gate")` |

**(b) Scorer factor — confidence multiplier (`ranking.py`, §14.2).** DNA-gated families are
multiplied by `HIGH = 1.0`, `PARTIAL = 0.7`, `NONE/None = 0.5`. Ungated families always
multiply by 1.0.

---

## 7. Mode $06 Architecture

```
raw_mode06: dict[str, float]    e.g. {"MID_21_TID_81": 45.2, "MID_A1_TID_01": -3.0}
       │
evaluate_monitor(mid_key, margin_pct, dictionary_path)
  │  Validate: mid_key must match ^MID_[0-9A-F]{2}_TID_[0-9A-F]{2}$
  │  Load dict (LRU-cached): mode_06_hex_dictionary.json (33 universal CAN MIDs)
  │  Extract MID hex from key: "MID_21_TID_81" → "21" → "Catalyst OSC Bank 1"
  │  Classify margin:
  │    ≤ 0    → CRITICAL_FAIL
  │    1–15   → PENDING_FAIL_MARGINAL
  │    ≥ 16   → PASSED
  └─ Mode06MonitorResult { monitor_id, state, margin_pct, target_component }
```

`DTC_CONFIDENCE_WEIGHTS` for COMLab scoring and the Phase-2 scorer:

```python
"confirmed": 1.0   "permanent": 1.0   "pending": 0.5
"mode06_critical_fail": 0.7   "mode06_marginal": 0.4   "mode06_passed": 0.0
```

---

## 8. COMLab Integration Points

| `DTCLabPayload` field / scorer output | COMLab consumer |
|----------------------|----------------|
| `routing_tags` | Fault-atlas routing; `POA_HISTORY` appended by COMLab when `GASLab.chemical_state == POA_SIGNATURE` (T-FX-3) |
| `mode_06_monitors` | `DTC_CONFIDENCE_WEIGHTS` applied to produce per-monitor confidence |
| `historical_fault_context` | Temporal dimension for fault ranking |
| `freeze_frame` | `short_term_ft1 + long_term_ft1` for healing delta; PIDs forwarded to OBDLab as `freeze_frame_pids` |
| `confirmed_dtcs` | Passed to OBDLab `AnalyticsPreconditions` gating in COMLab |
| `active_mil` / `mil_flashing` | MIL severity context in COMLab report |
| `classify_top3()` → `(family, confidence)` | COMLab Bayesian `combine()` (FU-1), via Wired adapter `T-DTW-1` |

---

## 9. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Import isolation | 0 cross-lab Python imports (audited in `test_dna_view.py`) |
| DTC format | 100% of valid OBD-II codes pass regex; 100% of invalid forms rejected |
| POA_HISTORY | Never emitted by `RoutingTagMapper` (convention; no automated test in v1) |
| Determinism | Same DTC input → same routing tag order (enum-definition order); scorer sorts `(-confidence, family)` |
| Mode $06 cache | At most 1 dictionary file open per distinct path (LRU-cache maxsize=4) |
| Scorer purity | No new numeric literal; all confidence from §16 weights × §14.2 DNA factor; no clamp before `classify_top3` |

---

## 10. Known Gaps & Proposals

| ID | Description | Status |
|----|-------------|--------|
| `dtc_severity_map.yaml` | File does not exist; `DTCSeverityClass` enum defined but unused (reserved contract surface) | v2 backlog |
| `DTC_CONFIDENCE_WEIGHTS` drift guard | No wiki cross-check test | Open |
| Manufacturer-specific MIDs | No overlay mechanism in current API | v2 backlog |
| T-FX-3 enforcement | `POA_HISTORY` injection is convention; not enforced by DTCLab | Open |
| **EP-DTC-NOSTART-1** | **PROPOSAL** — surface Mode $06 monitor-aborted/Incomplete state (MID $A1/TID $53) + freeze-frame fuel/spark-cut state. Consumer: COMLab `T-COMV2-NOSTART-1`; extends `mode06_evaluator.py` + Mode-06 schemas; CAN-era gated. Registered by `T-OBDV2-5`, tracked as `T-DTCV2-NOSTART-1`. | Proposed (not shipped) |
