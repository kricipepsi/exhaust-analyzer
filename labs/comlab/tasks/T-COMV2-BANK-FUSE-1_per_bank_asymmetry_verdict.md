# T-COMV2-BANK-FUSE-1 — per-bank asymmetry verdict (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (mirror emitted field + wire its named reader → close anti-orphan).
**Blocked by:** `T-OBDV2-BANK-ASYM-1` (OBD per-bank emitter, **done**). **DEP-3.**
**Drill:** boot order (`COMLAB_TASKS_START_HERE.md`) → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** mirror OBD `per_bank_trim_delta` into the inbound schema and wire a **bank-asymmetry** evidence verdict in the router, behind a default-off flag. Single-bank (`None`) and symmetric (`|Δ| ≤ 5 %`) inputs are inert. This is where the field meets its named reader — it **closes signal/noise** for DEP-3.

### Context
`per_bank_trim_delta` is the signed bank-1−bank-2 trim difference OBDLab emits. Zero live COMLab reads today → orphan. A large asymmetry points to a **bank-localised** cause (one-bank vacuum leak / injector / O₂) rather than a global mixture fault, so it should bias family selection, not assert a verdict.

### What to build
1. **`comlab/schemas/ingestion.py::OBDLiveDataPayload`** — add `per_bank_trim_delta: float | None = None` mirroring the emitter **exact type** (`labs/obdlab/obdlab/schemas/payload.py:71`). Additive, default-absent → omitting it validates byte-identically. Comment the consumer (`# consumer: fault_atlas_router bank-asymmetry verdict — T-COMV2-BANK-FUSE-1`).
2. **`comlab/core/fault_atlas_router.py`** — add `enable_bank_fuse: bool = False` to the constructor (mirror `enable_delta` at `:244–264`). Add a pure helper `_bank_asymmetry_verdict(per_bank_trim_delta: float | None, resolved_horizon: str) -> <small result>`:
   - `None` → `UNAVAILABLE` (single-bank); `|Δ| ≤ 5.0` → `SYMMETRIC` (no-op); `|Δ| > 5.0` → `ASYMMETRIC`.  `# wiki: 08_scoring_to_fusion_rework.md §line95 (±5 % bound) + 02_lab_input_contract.md §2 authority bands`
   - **Confidence caveat uses `resolved_horizon`, not `model_year`** — the router carries `request.metadata.resolved_horizon` (read at `fault_atlas_router.py:588`/`:1239`), not a model year. When `resolved_horizon == "HORIZON_LEGACY"` (Euro 1–2, era mask `model_year_range: 1980–2001`, where "fuel trims unreliable/absent"), **cap the verdict's confidence**. Enum: `comlab/schemas/vocabulary.py::Horizon.LEGACY` (`:85`).  `# wiki: 04_horizon_eras.md §CONCEPT_LEGACY (trims unreliable) + era mask line63 (1980–2001)`
   - In `execute_triage_loop` **Phase 5** (after the routing-tag discriminator `:760`, before `scored.sort` `:762`), behind `self._enable_bank_fuse`: when `ASYMMETRIC`, add a bank-localised **evidence** re-rank term to scored rows whose KG `fault_family` is bank-localised (per `wiki/06_fault_atlas_families.md`) — evidence, **not** an override or flat additive bump (`wiki/08 §graph-relations`). Emit a `bank_asymmetry_applied` span event.
3. Three falsy short-circuits keep single-point byte-identical: flag off · field `None` · `|Δ| ≤ 5 %`.

### Consumer (signal/noise)
`per_bank_trim_delta` → `fault_atlas_router.py::execute_triage_loop` Phase 5 bank-asymmetry term (reachable on the live route). Closes the DEP-3 orphan. Existing-consumer named; not a proposal.

### Tests — `tests/` (ADD)
- `test_bank_fuse_inert_when_off`: a request with `per_bank_trim_delta = 12.0` through the router with `enable_bank_fuse=False` **and** single-bank `None` with it on → identical `OrchestratorFinalUIOutput` to baseline.
- `test_bank_fuse_asymmetric_biases_family`: a 2-bank input where a bank-localised family is a runner-up; `enable_bank_fuse=True` + `per_bank_trim_delta = 12.0` raises its rank + fires `bank_asymmetry_applied`; symmetric `3.0` does not.
- `test_bank_fuse_legacy_caps_confidence`: `resolved_horizon == "HORIZON_LEGACY"` yields the capped-confidence path; `HORIZON_ADAPTIVE`/`MODERN` do not.

### Success criteria (done = all)
- **Consumer-read gate:** two greps — read site + the `enable_bank_fuse` branch — prove `per_bank_trim_delta` read in a reachable path.
- Single-point **byte-identical** with flag off / field absent / symmetric.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-BANK-FUSE-1.md`. **STOP.**

### Files to touch
`comlab/schemas/ingestion.py` · `comlab/core/fault_atlas_router.py` · `tests/` (**ADD**) · `tasks/PROGRESS.md` (flip row) · `progress_notes/T-COMV2-BANK-FUSE-1.md`.

### Out of scope
Live activation / default-on; surfacing the verdict into `ExecutionMeta`; the `_b1`/`_b2` twin-trim path (that is `T-COMV2-ECU-FUSE-1`'s symmetry input, not this); emitter changes; new fault families; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "per_bank_trim_delta" comlab/core/fault_atlas_router.py   # read site
grep -nI "enable_bank_fuse"   comlab/core/fault_atlas_router.py    # the branch that reaches it
"$PY" -m pytest tests/ -q -k "bank_fuse"
```
