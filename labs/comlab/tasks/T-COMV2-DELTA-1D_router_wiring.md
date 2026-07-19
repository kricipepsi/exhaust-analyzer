# T-COMV2-DELTA-1D — Router + aggregator wiring (consumer; default-off)

**Authored:** 2026-06-20 (architect, Cowork). **Stage:** 4. **Type:** consumer wiring (the signal/noise-closing step). **Sub-task 4 of 4** of epic `T-COMV2-DELTA-1`.
**Blocked by:** `T-COMV2-DELTA-1C` (needs a working engine) **and** `T-COMV2-DELTA-1A` (needs the request field).
**Parent / decisions:** `tasks/T-COMV2-DELTA-1_cross_lab_delta_module.md`. **Source:** `research/deltaImplPlan.md` (steps 5, 6, 8 e2e).
**Drill:** boot order → parent epic → **this file** → scope-confirm before code.

> **One-line scope:** wire `delta_signature` into the **v1** `execute_triage_loop` **Phase 5** as a primary rank term, behind a **default-off** constructor flag. This is the task where the field meets its named consumer — it **closes signal/noise** for the whole epic. Default-off + three falsy short-circuits keep the single-point path byte-identical.

## What to build

1. **`comlab/core/fault_atlas_router.py`**
   - Constructor (`:244–264`): add `enable_delta: bool = False`, store `self._enable_delta` (mirror `use_v2_registry`).
   - In `route()` **v1 branch**, after `request = sanitized["request"]` (`:1155`) and before `execute_triage_loop` (`:1158`): `if self._enable_delta and key absent`, lazy-import `DeltaEngine` and set `sanitized["delta_signature"] = DeltaEngine.compute_delta_signature(request)`.
   - In `execute_triage_loop` **Phase 5**, after the routing-tag discriminator (`:760`) and before `scored.sort` (`:762`), inside the `phase.score` span: read `sanitized.get("delta_signature")`; when `present and confidence > 0 and target_fault_family`, for each scored row whose KG `fault_family` matches, set `score = max(score, delta_sig.confidence)` (**max, not +** — "primary" means it dominates; the unchanged sort then ranks it first). Emit a `delta_signature_applied` span event. **`execute_triage_loop` signature unchanged.**
   - **Byte-identity:** three independent falsy short-circuits keep single-point bit-identical — key absent (flag off), `present=False` (no frame), `confidence==0.0` (untrusted/nulled). Any one leaves `scored` untouched → existing sort runs.
2. **`comlab/core/lab_pipeline_aggregator.py`** — add `enable_delta: bool = False` to `__init__` (after `:95`; optionally resolve from `COMLAB_ENABLE_DELTA` env mirroring `USE_V2_REGISTRY`, default off) and pass `enable_delta=enable_delta` into the `FaultAtlasRouter(...)` build (`:112–117`). **No change to `_map_degradation`** (`:173`) — `SINGLE_POINT` surfacing into `ExecutionMeta` is a live-activation follow-up, not here.

## Tests — `tests/e2e/` (ADD)

- `test_delta_single_point_regression`: a no-second-frame request through `FaultAtlasRouter(use_v2_registry=False)` with `enable_delta=True` **and** `enable_delta=False` → **identical** `OrchestratorFinalUIOutput` (proves the flag is inert without a frame).
- `test_delta_two_point_activation`: an input where the delta-target family is a static runner-up; trusted second frame + `enable_delta=True` **promotes it to winner** (assert winner flips + `delta_signature_applied` fired); `enable_delta=False` leaves the original winner.

## Success criteria (done = all)

- **Consumer-read gate (the real done):** `delta_signature` is **grep-confirmed read** in `execute_triage_loop` Phase 5 on a path reachable with `use_v2_registry=False`. **Two greps** — read site + the v1 branch that reaches it — prove live, not dead, code.
- Single-point path **byte-identical**: existing `tests/` suite green and untouched; `test_delta_single_point_regression` identical under both flag states.
- `test_delta_two_point_activation` shows the winner flip + span event under flag-on.
- `ruff check .` → `pyright comlab/` → `pytest -x -q` clean.
- Update **DEP-14** Status (already registered) if wording needs it; flip **epic `T-COMV2-DELTA-1`** ledger row → `done` once 1A–1D all close. Fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-DELTA-1D.md`. **STOP.**

## Files to touch

`comlab/core/fault_atlas_router.py` · `comlab/core/lab_pipeline_aggregator.py` · `tests/e2e/` (**ADD**) · `tasks/PROGRESS.md` (flip 1D + epic) · `progress_notes/T-COMV2-DELTA-1D.md`.

## Out of scope

- **v2 registry-shim re-rank activation** → the separate follow-up `T-COMV2-DELTA-2` (production-default path; its own `COMLab-DELTA-V2` flag). Do **not** touch the v2 shim here.
- Changing `USE_V2_REGISTRY` default; surfacing `SINGLE_POINT` into `ExecutionMeta`; corpus rebuild; emitter changes; graphify; static-ranker weight re-tuning.

## Verification

```bash
cd labs/comlab
ruff check . && pyright comlab/ && pytest -x -q
# consumer-read gate — two greps (read site + the branch that reaches it):
grep -nI "delta_signature" comlab/core/fault_atlas_router.py     # read inside execute_triage_loop Phase 5
grep -nI "use_v2_registry" comlab/core/fault_atlas_router.py     # the v1 branch that calls Phase 5
# regression lock (single-point byte-identical):
pytest tests/e2e -q -k "single_point or regression"
pytest tests/unit/test_fault_atlas_router.py tests/unit/test_symptom_prior.py tests/unit/test_router_spans.py -q
```
