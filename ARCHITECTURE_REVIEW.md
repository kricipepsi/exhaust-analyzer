# Architecture Review — 4D-Diagnostic-Engine-v2

**Skill applied:** Improve Codebase Architecture (mattpocock/skills)  
**Date:** 2026-05-11  
**Scope:** `engine/v2/` pipeline + `app.py` UI  
**Vocabulary:** module · interface · seam · depth · leverage · locality (see skill LANGUAGE.md)

---

## Executive Summary

The pipeline architecture is sound. The module contract (VL → M0 → M1/M2 → M3 → M4 → M5) is clean, `ValidatedInput` enforces the R4/L04 rule correctly, and every module has a clear output type. The problems are concentrated in three areas: **the UI contract is broken** (app.py reads field names that don't exist on the result dict), **two modules contain dead/stub code** that silently degrades correctness, and **three signal-extraction helpers are duplicated** across modules in a way that violates locality.

---

## Deepening Opportunities

### 1. `app.py` reads a phantom result interface — BROKEN UI CONTRACT

**Files:** `app.py` (results pane, lines 601–658), `engine/v2/ranker.py` (`FaultResult`, `PerceptionGap`), `engine/v2/pipeline.py` (`_result_to_dict`)

**Problem:**  
`app.py` reads four fields that do not exist on the dict produced by `_result_to_dict(asdict(result))`. The result dict is the **interface** between the engine and the UI; it is currently misspecified on the UI side.

Concrete mismatches:

| `app.py` reads | Actual field name in result dict | Effect |
|---|---|---|
| `primary.get("discriminator_tags", [])` | `discriminator_satisfied` (`bool`) | Always renders nothing |
| `primary.get("promotion_tags", [])` | `promoted_from_parent` (`bool`) | Always renders nothing |
| `perception_gap.get("fired")` | does not exist — no `fired` field | Perception gap block **never renders** |
| `perception_gap.get("summary", '')` | `gap_type` (`str`) | Empty string shown |
| `perception_gap.get("delta_lambda", 0)` | must be computed: `abs(analyser_lambda - obd_lambda)` | Always shows Δλ = 0 |
| `ns.get('action', ns)` | `evidence` | Next-steps items render wrong |
| `ns.get('rationale', '')` | `expected_lift` | Next-steps rationale is always blank |

**Root cause:** The result dict is built from `dataclasses.asdict()` using `FaultResult`'s actual field names, but app.py was apparently written against an earlier schema (possibly V1's `discriminator_tags`/`promotion_tags` lists and a `PerceptionGap` with different field names).

**Solution:**  
Fix app.py to match the actual result dict shape. No engine changes needed. Specific fixes:

```python
# Replace:
disc = primary.get("discriminator_tags", [])
prom = primary.get("promotion_tags", [])
# With:
disc_satisfied = primary.get("discriminator_satisfied", False)
was_promoted = primary.get("promoted_from_parent", False)

# Replace:
if perception_gap and perception_gap.get("fired"):
    f"(Δλ = {perception_gap.get('delta_lambda', 0):.3f})"
# With:
if perception_gap:
    delta = abs(perception_gap.get("analyser_lambda", 0) - perception_gap.get("obd_lambda", 0))
    f"(Δλ = {delta:.3f})"
    # use perception_gap.get("gap_type") for the label

# Replace next_steps rendering:
ns.get('action', ns)   →  ns.get('evidence', str(ns))
ns.get('rationale', '') →  f"expected lift: +{ns.get('expected_lift', 0):.0%}"
```

**Benefits — locality:** All mismatches are in one place (app.py results pane). Fixing them here concentrates the contract in the UI. **Leverage:** perception gap is currently invisible to the user despite the engine computing it correctly; fixing this unlocks the Truth-vs-Perception display that is the engine's signature feature.

---

### 2. `_get_cruise_trim_total` is a permanent stub — dead code in trim-trend matrix

**Files:** `engine/v2/arbitrator.py` (lines 299–308), `_classify_trim_full` (lines 311–329)

**Problem:**  
`_get_cruise_trim_total` is hardcoded to return `None`:

```python
def _get_cruise_trim_total(validated_input: ValidatedInput) -> float | None:
    del validated_input
    return None
```

Because of this, the condition at line 284:
```python
if cruise_total is not None and gas_output.analyser_lambda_high is not None:
    _classify_trim_full(...)
else:
    _classify_trim_idle_only(...)
```
…always takes the `else` branch. `_classify_trim_full` is **dead code**. The 4-pattern trim-trend matrix (LEAN_LOAD_BIAS, RICH_STATIC) can never fire. The engine is silently locked into the degraded idle-only path regardless of whether high-idle gas data is present.

Apply the **deletion test**: deleting `_classify_trim_full` and `_get_cruise_trim_total` concentrates no new complexity — they are pass-throughs that hide nothing. The code looks like it does trim-trend analysis, but it only ever does half of it.

**Solution:**  
Two options with different tradeoffs:

*Option A (minimal):* Remove `_classify_trim_full` and `_get_cruise_trim_total`. Rename `_classify_trim_idle_only` to `_classify_trim_trend` and remove the `* _TRIM_IDLE_ONLY_CF_REDUCTION` penalty (it should not apply when L2 high-idle gas is present). This makes the actual behaviour explicit.

*Option B (correct):* Implement `_get_cruise_trim_total` using the freeze frame fuel-trim fields as a high-load proxy when `gas_high` is present, or source a second OBD snapshot at high-idle. This requires a data-model decision (is there a "high-idle OBD" record in v2.1?) before it can be coded.

The tradeoff is correctness vs scope. Option A is safe now; Option B requires a new data field.

**Benefits — locality:** The current code misleads anyone reading arbitrator.py into believing LEAN_LOAD_BIAS is reachable. Resolving this concentrates the actual behaviour in one place and removes a silent accuracy penalty on cases where L2 gas is present.

---

### 3. `score_root_causes` in `kg_engine.py` is defined but never called

**Files:** `engine/v2/kg_engine.py` (lines 167–194), `engine/v2/pipeline.py` (`diagnose`), `engine/v2/ranker.py` (`_find_root_cause`)

**Problem:**  
`kg_engine.score_root_causes()` applies the 0.80 gate that filters root causes before M5. It is never called from `pipeline.diagnose()`. Instead, `ranker._find_root_cause()` re-implements the gate inline by iterating `root_causes.yaml` directly:

```python
# ranker.py _find_root_cause — duplicates the gate from kg_engine
if raw_score < 0.80:
    return None
for rc_id, rc_def in root_causes.items():
    if rc_def.get("applies_to_fault") == fault_id:
        return rc_id
```

Two modules share responsibility for the same gate. The root cause gate's **locality** is broken — a future change to the threshold or the filtering logic needs to be applied in two places.

Apply the **deletion test** to `score_root_causes`: deleting it moves its complexity into the `_find_root_cause` call site in ranker.py. That complexity doesn't vanish — it's already there. So `score_root_causes` is earning its keep as the intended canonical location, but it isn't being used.

**Solution:**  
Call `score_root_causes()` from the pipeline and pass the qualified root causes into `resolve_conflicts` / `_build_result`, then remove the inline re-implementation in `_find_root_cause`. The gate lives in one place (kg_engine.py), consistent with the M4/M5 split.

**Benefits — locality:** Root cause threshold changes (`ROOT_CAUSE_PARENT_THRESHOLD`) apply once. The seam between M4 and M5 becomes clean: M4 produces both `raw_probs` and `qualified_root_causes`; M5 assembles results.

---

### 4. Signal extraction helpers are duplicated across `dna_core.py` and `digital_parser.py`

**Files:** `engine/v2/dna_core.py` (lines 256–283), `engine/v2/digital_parser.py` (lines 172–208)

**Problem:**  
Both modules implement `_extract_ect`, `_extract_rpm`, and `_extract_fuel_status` with near-identical logic (OBD priority → freeze frame fallback). They differ only in their parameter types: dna_core takes `ValidatedInput`; digital_parser takes `(OBDRecord | None, FreezeFrameRecord | None)` directly.

```python
# dna_core.py
def _extract_ect(vi: ValidatedInput) -> float | None:
    raw = vi.raw
    if raw.obd is not None and raw.obd.ect_c is not None:
        return raw.obd.ect_c
    ...

# digital_parser.py  
def _extract_ect(obd: OBDRecord | None, ff: FreezeFrameRecord | None) -> float | None:
    if obd is not None and obd.ect_c is not None:
        return obd.ect_c
    ...
```

There are six private functions implementing the same "OBD → freeze frame fallback" pattern. A bug or threshold change in one won't automatically propagate to the other.

**Solution:**  
Move the three extractors to `input_model.py` as methods or module-level helpers on `DiagnosticInput` (or a thin `SignalExtractor` helper). Both dna_core and digital_parser import from input_model already. The parameter form `(OBDRecord | None, FreezeFrameRecord | None)` is already more general — use that form in input_model so both callers can use it without unpacking `ValidatedInput`.

**Benefits — locality:** One definition; bug fixes and priority-order changes apply once. The interface stays small (three functions already familiar to both callers).

---

### 5. `_map_dtc` in `digital_parser.py` ignores its own data structure

**Files:** `engine/v2/digital_parser.py` (lines 29–39, 231–257)

**Problem:**  
`_DTC_FAMILY_MAP` is a dict that maps symptom IDs to `(symptom_id, frozenset_of_codes)`. But `_map_dtc` doesn't iterate it — it issues a manual `if dtc in _DTC_FAMILY_MAP["SYM_DTC_CATALYST"][1]:` for each family by name. The dict is a shallow module: it carries no leverage because callers bypass it to hardcode the key names.

Apply the **deletion test** to `_DTC_FAMILY_MAP`: delete it, and `_map_dtc` still works because the frozensets are explicitly embedded in each `if` check. The dict itself is doing nothing.

**Solution:**  
Invert the map to `frozenset → symptom_id` and iterate it in `_map_dtc`. Then `_DTC_FAMILY_MAP` earns its keep — adding a new DTC family requires one dict entry, not two code changes.

```python
_DTC_SET_MAP: list[tuple[frozenset[str], str]] = [
    (frozenset({"P0420", "P0430"}), "SYM_DTC_CATALYST"),
    (frozenset({f"P030{i}" for i in range(8)}), "SYM_DTC_MISFIRE"),
    ...
]

def _map_dtc(dtc: str) -> str | None:
    if dtc in _DTC_EXACT_MAP:
        return _DTC_EXACT_MAP[dtc]
    for codes, symptom in _DTC_SET_MAP:
        if dtc in codes:
            return symptom
    if dtc.startswith("P06"):
        return "SYM_DTC_ECU_INTERNAL"
    ...
```

**Benefits — leverage:** Adding a new DTC family is one dict entry. The current structure requires adding to both the dict definition *and* the if-chain — they are not in sync by construction.

---

### 6. `compute_ceiling` counts layers, not their identity — shallow ceiling model

**Files:** `engine/v2/ranker.py` (lines 191–209), `engine/v2/pipeline.py` (`_derive_evidence_layers`)

**Problem:**  
`compute_ceiling` looks up `len(evidence_layers_used)` in a fixed table:

```python
_CEILING_TABLE: dict[int, float] = {
    1: 0.40,  2: 0.60,  3: 0.95,  4: 1.00,
}
```

L1+L2 (two gas layers) → 0.60 ceiling. L1+L3 (gas + DTCs) → also 0.60. These are meaningfully different evidence profiles. Two gas states without DTCs should likely have a lower ceiling than gas + DTCs. The layer count is a proxy for layer identity, and a coarse one.

This is a design tradeoff, not a clear bug — the current spec source (`v2-result-schema §2`) may intentionally flatten it. Surface it only because the ceiling table interacts directly with what the user sees as "confidence."

**Solution candidates:**
- Assign ceiling by layer *set* (frozenset of layer IDs) rather than count — more discriminating, slightly more complex.
- Keep count-based but adjust the table to distinguish "two gas layers" from "gas + DTCs."

This contradicts the current spec. Flag for discussion rather than immediate change.

---

## Summary Table

| # | Module(s) | Type | Severity | Effort |
|---|---|---|---|---|
| 1 | `app.py` results pane | **Broken contract** — phantom field reads | 🔴 High | Low — UI-only fixes |
| 2 | `arbitrator._get_cruise_trim_total` | **Dead code** — trim-trend matrix always degraded | 🔴 High | Low (option A) / Medium (option B) |
| 3 | `kg_engine.score_root_causes` | **Unused module** — gate duplicated in ranker | 🟡 Medium | Low |
| 4 | `dna_core` + `digital_parser` extractors | **Duplicated logic** — no locality | 🟡 Medium | Low |
| 5 | `digital_parser._map_dtc` | **Shallow module** — dict ignored by its own callers | 🟢 Low | Low |
| 6 | `ranker.compute_ceiling` | **Coarse model** — count vs identity | 🟢 Low | Medium (spec discussion first) |

---

## Recommended sequence

Start with **#1** — it is the only issue that produces wrong output visible to the user right now. Every other issue is an internal correctness or maintainability problem; #1 makes the UI lie.

Then **#2** — the trim-trend degradation silently reduces diagnostic accuracy on every case where L2 high-idle gas is submitted. Users cannot know they're getting a worse result.

Then **#3 + #4** together — both are small locality fixes that reduce future maintenance risk.

**#5 and #6** are lower priority and can be addressed opportunistically.

---

*Ready to explore any of these candidates in depth — pick a number and I'll walk the design.*
