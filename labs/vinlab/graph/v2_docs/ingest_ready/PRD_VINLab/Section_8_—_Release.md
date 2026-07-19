> **Context:** VINLab PRD v2.1 (2026-06-12) | Module: VINLab | Section: Section 8 — Release | Parent document: PRD_VINLab.md / SEMANTIC_CONTRACT section 4.1

## Section 8 — Release

### v2 Scope

All P0 features above, as shipped after the sibling split (T-RM-2-DNA), the enum-field
cut-over (T-FX-5), the air-metering single-module rework (T-FX-2), and the
cylinder-heuristic fallback (T-VL-7). The CoC overlay is populated from per-engine-code
petrol CSV medians.

### Landed (DNA-family pack — see `labs/dnalab/tasks/PROGRESS.md`)

These tasks are **done**; their dispositions are now shipped behaviour:

- **T-DNA-3 — emit `rated_rpm` (done).** `VinDNA` now emits `rated_rpm` (`int | None`,
  source `DBS/docs/vehicles_petrol_specimens.csv` `P14_rated_rpm`). COMLab's projector
  (`projection.py` → `ObdLabDnaView.rated_rpm`) already reads it as the OBDLab RPM
  ceiling — producer and consumer are now matched.
- **T-DNA-4 — formalize CoC fields + reconcile emissions (VINLab side done).** The CoC
  fields are formalized **top-level** on `VinDNA`; the emissions block is formalized as
  `{upstream_o2_type, downstream_o2_present, downstream_trim_role, has_catalyst,
  egr_equipped}` with `secondary_air_equipped` dropped (no consumer). The projector
  still reads CoC under `emissions{}` → the remaining fix is the paired **COMLab-C** path
  change at Stage 4 (not a VINLab change).
- **T-DNA-5 — `model` disposition (DNA10 Q8) — kept-empty.** No `VinDNA.model` field:
  the DBS specimen file has no repeated engine-code groups, so there is no within-code
  CoC variance to justify the field. DTCLab's mirror relaxation is registered as
  COMLab-D.
- **T-DNA-6 — `fuel_type` proposal (+ `altitude_band` note) — proposal-only.**
  `fuel_type` is registered as **proposal** COMLab-E (future `GasLabDnaView`, E5/E10
  blend-correction context); it is **not** a live `VinDNA` field. `altitude_band` stays
  session/context metadata (lambda math is altitude-invariant), not a schema field.

### Explicitly Deferred

- `mysql_data/` (~484 MB) verbatim copy — Track-2 cleanup candidate; not used at runtime.
- `hc_nox_type_approval` and the three noise fields are not part of the confidence-flag
  CoC-null check (only nine CoC fields downgrade confidence).

### Success Criteria

1. KR1–KR7 all hold.
2. Offline decode produces a valid `VinDNA` for every in-scope fixture VIN.
3. Out-of-scope (non-petrol, year ∉ [1990, 2020], wrong length) raises the correct
   exception subclass.
4. No cross-lab Python imports.
5. Every numeric literal carries a citation; all SQL confined to `db/tecdoc_query.py`.

## Graph relations (explicit)

**Section 8 — Release** DESCRIBES **VINLab PRD v2.1 (2026-06-12)**
**labs/vinlab/tests/unit/test_models.py** VERIFIES **vinlab.models.VinDNA.rated_rpm**
**vinlab.models.VinDNA.fuel_type** PROPOSAL **comlab/comlab/config/proposals/entries.yaml**
