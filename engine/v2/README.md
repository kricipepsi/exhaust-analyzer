# Engine V2 — Module Reference

Petrol-only diagnostic inference engine (MY 1990–2020). Seven-module pipeline
implementing the Evidence Arbitrator architecture with combined MYCIN-CF and
subtractive-inhibitory reasoning.

## Pipeline (R1)

```
DiagnosticInput → VL → M0 → M1/M2 → M3 → M4 → M5 → ResultSchema
```

No module may be skipped or re-ordered. VL runs first and is mandatory (R4).

## Modules

| Module | File | Responsibility | Key rules |
|--------|------|---------------|-----------|
| **VL** | `validation.py` | 11-category input validation (R4) | Returns `ValidatedInput`; no module reads raw `DiagnosticInput` |
| **M0** | `dna_core.py` | Tech mask, era mask (R6), engine-state FSM (L15), vref.db lookup | Emits `engine_state` before any other module runs |
| **M1** | `digital_parser.py` | DTC→symptom, freeze-frame→symptom, OBD→symptom | Fuel-status gate fires before trim-derived symptoms (L18) |
| **M2** | `gas_lab.py` | Brettschneider lambda, per-state gas symptoms, dual-state delta | Analyser lambda is ground truth (KR3) |
| **M3** | `arbitrator.py` | Perception-as-symptom (L01), trim-trend, bank symmetry, flood control (R8) | Perception fires as KG symptom only — never global override |
| **M4** | `kg_engine.py` | Tech/era veto pre-pass, CF combination (R2), inhibitory subtraction | Applies vetoes before scoring; `resolve_conflicts()` NOT called here (R7) |
| **M5** | `ranker.py` | `resolve_conflicts()` 8-step ordered loop (R7/L02), confidence ceiling (L16), backward chaining (R3), `next_steps[]` | Only module allowed to call `resolve_conflicts()` |

## Data contracts

- **M0** reads from `vref.db` (the only I/O in the pipeline; all other modules are pure functions).
- **M4** applies tech/era vetoes before scoring — they are NOT M5's job.
- **M5** `resolve_conflicts()` applies the 8-step loop in fixed order. Steps 3–8 are post-M4.
- **Backward chaining** (M5b) fires only if `state == insufficient_evidence` AND UI opt-in is set (R3).

## Result schema (R9)

One JSON shape across all 4 pathways: `named_fault`, `insufficient_evidence`, `invalid_input`.

| Field | Type | Description |
|-------|------|-------------|
| `state` | `str` | One of `named_fault`, `insufficient_evidence`, `invalid_input` |
| `primary` | `dict \| None` | Top-ranked fault with `fault_id`, `raw_score` (gate logic), `confidence` (display) |
| `alternatives` | `list[dict]` | Secondary faults above threshold |
| `perception_gap` | `dict \| None` | Truth-vs-Perception delta when analyser disagrees with ECU |
| `validation_warnings` | `list[str]` | VL soft-mode warning messages |
| `cascading_consequences` | `list[dict]` | Flood control cascade grouping (R8) |
| `confidence_ceiling` | `float` | Evidence-layer cap (L16): gas-only 0.40 / +DTC 0.60 / +FF 0.95 / full 1.00 |
| `next_steps` | `list[dict]` | Backward-chaining investigation steps (empty if opt-in off) |

## Scoring rules

- **`raw_score`** for internal gates and threshold comparisons. **`confidence`** for display only. Never swap (L05).
- **CF combination** uses MYCIN formula bounded to [0, 1] (R2).
- **Subtractive edges** in [−1.0, +1.0] for vetoes. Hard veto (`w == −1.0`) only for tech/era mask or explicit requires-X guards (R2).
- **Weights > 0.30** require a `discriminator_gate` field (R7/L07).
- **Confidence ceiling** keys on evidence layers used, not absolute score alone (L16).

## Hard constraints

- Petrol-only, MY 1990–2020. Non-petrol fuel types are out of scope (R12/L20).
- VL is mandatory and first (R4/L04).
- `resolve_conflicts()` lives in M5 only (R7/L02).
- Every numeric threshold cites a `# source_guide:` master guide section (R10/L08).
- No "healthy engine" pseudo-fault — return `insufficient_evidence` instead (L19).
- `diagnose(DiagnosticInput) → ResultSchema` is a pure function — no server session, no global mutable state.
