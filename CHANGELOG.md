# Changelog

## [v2.0.1] - 2026-05-12 — VIN-first vehicle context + reference UI

> Hotfix on top of v2.0.0 (`UI_REMEDY_PLAN.md` Path A). Closes a doc-mention-without-module gap surfaced by the 2026-05-10 owner audit: VIN auto-fill — the headline V2 vehicle-context flow — was missing despite being described in HLD prose. v2.0.1 also reverts the UI from a 5-stage stepper (carried over from a V4 prototype) to the canonical V1 reference flat layout.

### Added
- `engine/v2/vin/` — VIN resolver lifted verbatim from `vehicle-data/petrol_vin/` (owner-supplied, 2026-05-10). **14 brand extractors** (VW group, BMW group, Mercedes, Ford, PSA group, Toyota, Hyundai/Kia, Fiat). Returns `EngineDNA(make, engine_code, displacement_l, induction, intercooler, injection, o2_arch, spec_idle_gps, …, confidence ∈ {high, partial, none})`.
- `engine/v2/vin/data/engine_dna.json` — **1,978 petrol engine codes / 110 brands** (~1 MB, OPSI-derived; data lint asserts `fuel_type=='petrol'` on every row, R12).
- `vininfo>=1.7.0` runtime dependency (`requirements.txt`).
- `VehicleContext.vin: str | None` — new optional input field (T-R3, backward-compatible default `None`).
- `validation.py` category 12 — VIN format `^[A-HJ-NPR-Z0-9]{17}$` + ISO 3779 checksum.
- `tests/v2/unit/test_vin_resolver.py`, `tests/v2/unit/test_vehicle_context_vin.py`, `tests/v2/unit/test_validation_vin_cat12.py`, `tests/v2/integration/test_pipeline_vin.py`.
- `app.py` — full UI rewrite to the V1 reference flat layout (sidebar VIN primary + L1..L5 stacked expanders + dx-card results). Plotly confidence gauge.

### Changed
- `dna_core.py` — when `validated.raw.vehicle_context.vin` resolves with confidence ≥ partial, M0 lifts `engine_code`, `displacement_cc`, `induction` from `EngineDNA` before `vref.db` lookup. Manual fields fall back when VIN absent / confidence='none'.
- HLD §7.0a (NEW), §7.8 rewritten, §6.1 / §6.2 diagrams updated, §12 drift entries added (3).
- MASTER_PLAN — added L21 (doc-mention-without-module-section).
- ROADMAP — added phase P5.5 (VIN remediation), 6 v2.1 follow-ups, L01–L21 mapping.

### Removed
- PDF export (`fpdf2` dependency removed). Was in v2.0; reference UI does not have one. Owner direction; PRD §7 Feat 11 carried as drift in HLD §12.
- 5-stage stepper UI (Stage 0 → 4 progressive disclosure). Replaced by flat reference layout.

### Diesel sibling note
v2.0.1's deliverables are the structural template the planned Diesel sibling app forks from: `engine/v2/vin/extractors/` (1:1 reuse), `app.py` sidebar/results layout (fuel-agnostic CSS + helpers), L21 doc-lint principle. Only `engine_dna.json` (→ `engine_dna_diesel.json`) and the M2 Gas Lab equivalent change.

---

## v2.0.0 — Evidence Arbitrator Architecture (2026-05-10)

### Breaking changes from V1

V2 is a ground-up rewrite of the diagnostic inference engine. It is **not
backwards compatible** with V1 inputs, outputs, or schema files.

#### Architecture

| Aspect | V1 | V2 |
|--------|----|----|
| Pipeline | Informal 5-stage cascade | 7-module rigid pipeline: VL → M0 → M1/M2 → M3 → M4 → M5 (R1) |
| Inference | Weighted sum + perception global override | MYCIN-CF combination with subtractive inhibitory edges (R2) |
| Post-inference | Undocumented 5-stage corrector cascade | Single `resolve_conflicts()` in M5, fixed 8-step order (R7/L02) |
| Perception | Global override at 0.70 confidence (L01) | Fires as a KG symptom only — no authority over other layers |
| Validation | Gas-only validation (L04) | 11-category VL mandatory before any module (R4) |
| Schema | Flat node list | Three-tier taxonomy: symptoms / faults / root_causes (R5) |
| Era awareness | None (L06 implied) | 4 era buckets: 1990–1995, 1996–2005, 2006–2015, 2016–2020 (R6) |
| Thresholds | Magic numbers, no sources (L08) | Every numeric cites a `# source_guide:` master guide section (R10) |
| Corpus | 281 cases, no CI replay (L13) | 400 cases, Layer-2 CI from day one (R11) |
| Result schema | Different shapes per pathway (L06) | One unified schema across 4 pathways (R9) |
| Fuel handling | Multi-fuel (petrol + non-petrol) | Petrol-only, MY 1990–2020 (R12) |

#### Key behavioral differences

- **No "healthy engine" pseudo-fault.** V1 returned `Healthy_Engine` for borderline cases (L19). V2 returns `insufficient_evidence` with a confidence ceiling.
- **`raw_score` for gates, `confidence` for display.** V1 used the same scalar for both (L05). V2 separates them — gates never read `confidence`.
- **Engine-state FSM is M0's primary output (L15).** V1 applied cold-start as a late filter. V2 emits `engine_state` before any other module.
- **Fuel-status gate blocks trim symptoms.** V1 scored fuel-trim faults even in open-loop (L18). V2's M1 fuel-status sub-module gates trim-derived symptoms when `fuel_status` is open-loop.
- **Backward chaining is opt-in (R3).** V1 fired backward reasoning on every `insufficient_evidence` result. V2 requires the UI checkbox to be on.
- **Flood control caps cascade scoring (R8).** Root causes firing > 3 sibling symptoms trigger cascade grouping with 30% additive weight reduction.

#### Migration guide for existing V1 consumers

1. **Input:** Use `DiagnosticInput` dataclass (see `engine/v2/input_model.py`). UI fields must derive from it (L17).
2. **Output:** All pathways return the R9 `ResultSchema` shape. Check `state` field first — three values only: `named_fault`, `insufficient_evidence`, `invalid_input`.
3. **Schema references:** V1 node IDs that changed have entries in `schema/v2/label_aliases.yaml` (155 entries). If a V1 fault ID is not resolving, check the alias map.
4. **Corpus:** `cases_petrol_master_v6.csv` (400 cases) replaces `cases_petrol_master_v5.csv` (281 cases). Column schema is backward compatible.
5. **Edge weights:** All re-weighted. V1 tuning values do not apply. See `schema/v2/edges.yaml`.
6. **Thresholds:** All re-calibrated against 7 master guides. V1 magic numbers are invalid. See `schema/v2/thresholds.yaml`.

#### V1 code access

V1 source is archived as git tag `v1-final`:
```bash
git checkout v1-final
```

The V1 schema is frozen at `schema/v1_reference/` for comparison only — it is
not consumed by the V2 engine.

### Known limitations

- Layer-2 corpus accuracy is 4.8% (pre-structural-fix floor). Structural fixes are tracked as unplanned follow-ups T-P6-2b through T-P6-2e in `V2_PROGRESS.md`. The calibration-only ceiling has been reached — further accuracy improvements require edge-weight rebalancing and symptom-detection threshold tightening.
- Perturbation test suite (L14) is not yet built — `tests/v2/perturbation/` is an empty directory.
- Mutation-score gate (≥80%) has not been verified — mutmut requires WSL/Linux.
