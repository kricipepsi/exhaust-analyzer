
> **Context:** GASLab PRD v2.1 (2026-06-10) · Module: GASLab · Section: Section 7 — Solution · Parent document: PRD_GASLab.md
## Section 7 — Solution

### Key Features (all P0 unless noted)

- P0: Brettschneider 5-gas lambda computation with NOx correction.
- P0: Exhaust gas triangle validity gate (14 ≤ CO+CO₂+O₂ ≤ 16 → VALID).
- P0: Dilution screen (CO+CO₂ > 6.0 vol% → sample not diluted).
- P0: 34-fault ontology loaded from `gas_lab_ontology.yaml` with version control.
- P0: Priority-override rules (coolant 87, masking 85, cam-timing 82, collision 80, rich-timing 40).
- P0: DNA-gated fault suppression (6 gates: `has_catalyst` × 2, `fuel_delivery_type` × 2, `egr_equipped` × 2).
- P0: Dual-RPM input (`reading_high`) with RPM-differential family separation (cam timing, lean-vs-cam, catalyst weak-vs-dead, mechanical-wear leaves).
- P0: Per-vehicle CoC overrides — `target_lambda_v112` λ window, Euro-scaled CO/HC ceilings, wideband O₂-bias calibration.
- P0: `fuel_trim` context input for EXTERNAL_O2_SUSPECT leak disambiguation and mechanical-wear routing.
- P0: Specificity-based tie-breaking (narrowest signature wins; catch-alls last).
- P0: `GasLabPayload` Pydantic output model (9 fields, including `lambda_measured` for the no-OBD fallback).

### Technology

- Python ≥ 3.11 (project runs 3.14). Pydantic ≥ 2. PyYAML. No cross-lab imports.
- Package: `gaslab`, standalone `pyproject.toml`.
- Entry point: `gaslab.process.process(reading, context) → GasLabPayload`, where `context: GasLabContext` carries `dna`, `engine_state`, and optional `reading_high`, `fuel_trim`, `lambda_measured`, `block_test_passed`.

### Assumptions


*(Table converted to entity blocks — 4dlab-doc-prep Step 2)*

### `Hcv = 1.85` is the correct H:C ratio for petrol
- **Assumption**: `Hcv = 1.85` is the correct H:C ratio for petrol
- **Validation**: `test_brettschneider.py` stoich-unity test vs `GAS_VOCABULARY.md`

### Bound matching is scoped to `STABILIZED_IDLE`; high-idle enters via `reading_high`
- **Assumption**: Bound matching is scoped to `STABILIZED_IDLE`; high-idle enters via `reading_high`
- **Validation**: Per-fault `operating_state: STABILIZED_IDLE`; RPM-differential gates consume `reading_high`

### All 6 DNA-gated faults and every added field have a named COMLab consumer
- **Assumption**: All 6 DNA-gated faults and every added field have a named COMLab consumer
- **Validation**: `test_validators.py` DNA-gate count test + signal/noise review

### The three `CAM_TIMING_*` states need no MAF/MAP DNA field
- **Assumption**: The three `CAM_TIMING_*` states need no MAF/MAP DNA field
- **Validation**: Split carried by the gas-direction discriminator; no field without a consumer


---


## Graph relations (explicit)

**Section 7 — Solution** DESCRIBES **GASLab PRD v2.1**
**gaslab.process.process()** CONSUMES **GasReading, GasLabContext** -- entry point
**GasLabContext** CONSUMES **dna, engine_state, reading_high, fuel_trim, lambda_measured, block_test_passed**


