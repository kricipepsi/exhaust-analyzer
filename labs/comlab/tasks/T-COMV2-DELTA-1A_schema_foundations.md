# T-COMV2-DELTA-1A — Delta schema & vocabulary foundations (inert input surface)

**Authored:** 2026-06-20 (architect, Cowork). **Stage:** 4 (COMLab rework). **Type:** additive schema/vocab + proposal registration. **Sub-task 1 of 4** of epic `T-COMV2-DELTA-1`.
**Parent (read for full context + locked decisions):** `tasks/T-COMV2-DELTA-1_cross_lab_delta_module.md`.
**Source of truth:** `labs/comlab/research/deltaImplPlan.md` (steps 1–3, 7).
**Drill:** `START_HERE.md` → `ROADMAP.md` → `AGENTS.md` (five rules) → parent epic → **this file**, then post the scope-confirm before code.

> **One-line scope:** add the *input surface* for the cross-lab delta — the `SINGLE_POINT` degradation mode, the widened `DegradationLit`, and the optional `SecondOperatingPointFrame` on the request — plus register the `COMLab-DELTA` proposal. **Nothing reads these yet** (the engine is 1B/1C, the consumer is 1D). Default-`None` everywhere, so every existing case stays byte-identical.

## Why this is safe to ship without a consumer

The field's named consumer lands in **DELTA-1D**, and per `PROGRESS.md` / `CROSS_LAB_DEPENDENCIES.md §Gates` anti-orphan is a **Stage-4-close** gate, not a per-task one. Registering `COMLab-DELTA` now (the proposal that names the consumer + the full 1A→1D arc) keeps the field proposal-bounded from the moment it exists. `entries.yaml` is documentation/registry only — it does **not** gate behaviour — so registering early is harmless.

## Steps (smallest-diff order; green before handing off)

1. **`comlab/schemas/vocabulary.py`** — add a sibling to `DegradationMode` (after the existing members):
   `SINGLE_POINT = "SINGLE_POINT"  # wiki: delta-relations/01 — no second frame; static signature is the fallback`.
   `AirMeteringStrategy` (`:108`) and `InductionType` (`:151`) already exist — **no change**.
2. **`comlab/schemas/response.py`** — widen `DegradationLit` (`:26`) to include `"SINGLE_POINT"`, else `ExecutionMeta` validation rejects the new mode. *Must land with step 1.*
3. **`comlab/schemas/ingestion.py`** —
   - Add `SecondOperatingPointFrame(BaseModel)` after `OBDLiveDataPayload` (`:367`). **All measurement channels optional** (the engine computes only deltas whose channels are present on both frames): `rpm_state_bucket: EngineStateBucket`, `engine_rpm: int`, trim channel (`total_trim_correction_delta`/`shrtft1`/`longft1`), gas channel (`gas_hc`/`gas_co`/`gas_co2`/`gas_o2`/`gas_nox`/`lambda_chem`), validity inputs (`sample_validity: SampleValidity | None`, `rpm_stable: bool = True`), ΔO₂ components (`o2_switch_freq_hz`/`o2_voltage_bias_v`/`o2_downstream_response`, named-only), and **architecture-gate inputs carried on the frame itself** (`air_metering_strategy: AirMeteringStrategy | None`, `induction_type: InductionType | None`) — they ride on VinDNA, which is **not** reachable from the router's request, so they must live here. Reuse existing field-constraint bounds from `GasLabPayload`/`OBDLiveDataPayload`; `# wiki:`-cite each to its chunk.
   - Add the optional request field on `OrchestratorInboundRequest` (after `:412`):
     ```python
     second_operating_point: Optional[SecondOperatingPointFrame] = None
     # T-COMV2-DELTA-1 — additive; absent → byte-identical single-point path.
     # consumer: comlab/analytics/delta_engine.py:DeltaEngine.compute_delta_signature -> fault_atlas_router Phase 5 (DELTA-1D)
     ```
4. **`comlab/config/proposals/entries.yaml`** — append `COMLab-DELTA` in the existing entry shape: `family: "cross-lab-delta-proposal"`, `consumer: "comlab/comlab/core/fault_atlas_router.py:FaultAtlasRouter.execute_triage_loop"  # Reader: T-COMV2-DELTA-1D`, `status: "proposed"`, `owning_ledger: "COMLab T-COMV2-DELTA-1"`, `source:` (delta-relations/01–08 + `research/PROPOSAL_DeltaLab_cross_lab_delta_module.md`), `description:` (names the default-off constructor gate + the `second_operating_point` field + the v2 follow-up `T-COMV2-DELTA-2`), `field.path: OrchestratorInboundRequest.second_operating_point`.

## Success criteria (done = all)

- The full existing `tests/` suite is **green and untouched** — default `None` + last-field position proves every existing JSON fixture validates unchanged (this is the byte-identity proof for this slice).
- `ruff check .` → `pyright comlab/` → `pytest -x -q` clean.
- New enum/field/proposal present; **nothing reads them yet** (no router/engine change in this task — that's out of scope, below).
- `VERIFICATION GATE` + `CODE REVIEW` filled in `progress_notes/T-COMV2-DELTA-1A.md`; flip the `T-COMV2-DELTA-1A` ledger row → `done`. Then **STOP**.

## Files to touch

`comlab/schemas/vocabulary.py` · `comlab/schemas/response.py` · `comlab/schemas/ingestion.py` · `comlab/config/proposals/entries.yaml` · `tasks/PROGRESS.md` (flip row) · `progress_notes/T-COMV2-DELTA-1A.md`.

## Out of scope (other sub-tasks)

- **`delta_engine.py`** (the math) → DELTA-1B + 1C.
- **Router / aggregator wiring** (the consumer read) → DELTA-1D. Do **not** touch `fault_atlas_router.py` or `lab_pipeline_aggregator.py` here.
- Corpus rebuild, emitter changes, graphify — out of the whole epic.

## Verification

```bash
cd labs/comlab
ruff check . && pyright comlab/ && pytest -x -q       # full existing suite must stay green
grep -nI "SINGLE_POINT" comlab/schemas/                # enum + Literal both present
grep -nI "second_operating_point" comlab/schemas/ingestion.py   # field present, default None
```
