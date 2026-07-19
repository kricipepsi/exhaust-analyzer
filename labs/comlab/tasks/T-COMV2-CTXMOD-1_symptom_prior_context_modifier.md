# T-COMV2-CTXMOD-1 — symptom-prior context modifier (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (mirror emitted field + wire its named reader → close anti-orphan).
**Blocked by:** `T-DNA-2` (SymptomLab `load_state` emitter, **done**). **DEP-13 · proposal `COMLab-B`** (`entries.yaml`).
**Drill:** boot order → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** read SymptomLab `load_state` from `symptom_dna.environmental_conditions` and use it as a **context modifier** on the symptom-prior weighting — capped at **0.65 trust** — behind a default-off flag. Absent `load_state` is inert. Closes signal/noise for DEP-13.

### Context
`load_state` (IDLE / CRUISE / WOT / …) says under what load the symptom was observed; the same symptom carries a different prior under idle vs load. It modulates (never replaces) the symptom prior, and the modulation is bounded by the **COMLab-B report-trust ceiling** — `max_symptom_prior_weight = 0.65` — so a context modifier can never dominate physical measurement. Zero live COMLab reads today → orphan. **Symptom side**, not OBD: it is carried on the `symptom_dna` dict, not `OBDLiveDataPayload`.

### What to build
1. **No new schema field.** Read the nested key off the existing `OrchestratorInboundRequest.symptom_dna` dict: `symptom_dna.get("environmental_conditions", {}).get("load_state")`. Mirror the SymptomLab vocabulary value (`labs/symptomlab/symptomlab/models.py:37` — `LoadState`) as a **local string compare**, no cross-lab import.
2. **Reader = the router's symptom-prior step (self-contained, mirrors the BANK-FUSE pattern — do NOT route through `route_symptom`).** The prior table and the `0.65` cap already live in **`comlab/core/fault_atlas_router.py`** (`_load_prior_table` `:354`, `config/symptom_prior.yaml` `:80`, applied where `symptom_prior_applied` fires `:~767–779` and in `route()` `:~1115`); `request.symptom_dna` is in scope there (`:767`). Add `enable_ctxmod: bool = False` as a **router constructor arg** (mirror `enable_delta`/`enable_bank_fuse`). When on and `load_state` present, apply a bounded context multiplier to the symptom-prior weight, then **clamp to the cap read from `config/symptom_prior.yaml`** (do not hard-code `0.65`).  `# wiki: 10_differential_and_symptom_prior.md §RULE_SYMPTOM_PRIOR line64 (CTXMOD consumes load_state as context modifier, caps at 65 % trust) + config/proposals/entries.yaml COMLab-B (max_symptom_prior_weight 0.65)`.
   - **Why not `symptom_router.route_symptom`:** it is a free function with three aggregator call sites (`:243/:348/:529`) and does **not** apply the prior weight or the cap — wiring the modifier there would be both dead (the weighting is in the router) and a caller-scope trap. Keep the reader in the router so the flag is a constructor arg and the field flows via `request.symptom_dna`.
3. Falsy short-circuits keep behaviour byte-identical: flag off · `load_state` absent. The cap clamp must also hold on the **flag-on, no-load_state** path (the ceiling is unconditional once symptom-prior is in play — confirm it already does, else this is where it lands).

### Consumer (signal/noise)
`symptom_dna.environmental_conditions.load_state` → symptom-prior weighting in `fault_atlas_router.py` (the `symptom_prior_applied` step), clamped by COMLab-B `0.65`. Closes the DEP-13 orphan. Proposal `COMLab-B` supplies the cap; consumer ships here.

### Tests — `tests/` (ADD)
- `test_ctxmod_inert_when_off`: a payload with `environmental_conditions.load_state` set, flag off → identical output to baseline; flag on, no `load_state` → identical.
- `test_ctxmod_modulates_prior`: same symptom under two `load_state` values, flag on → different (bounded) symptom-prior weight.
- `test_ctxmod_caps_at_065`: a `load_state` that would push the prior past `0.65` → weight clamped to `0.65`.

### Success criteria (done = all)
- **Consumer-read gate:** two greps in `fault_atlas_router.py` — `load_state` read in the symptom-prior step + the `enable_ctxmod` branch that reaches it (a live method; tests construct the router with `enable_ctxmod=True`, mirroring BANK-FUSE).
- Behaviour **byte-identical** with flag off / `load_state` absent.
- Symptom-prior weight provably `≤ 0.65` on every path.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill both gate blocks in `progress_notes/T-COMV2-CTXMOD-1.md`. **STOP.**

### Files to touch
`comlab/core/fault_atlas_router.py` (the symptom-prior step + the `enable_ctxmod` constructor flag) · `comlab/config/symptom_prior.yaml` (read the `0.65` cap from here — confirm/extend, don't hard-code) · `tests/` (**ADD**) · `tasks/PROGRESS.md` · `progress_notes/T-COMV2-CTXMOD-1.md`. *(No `ingestion.py` change — `load_state` rides the existing `symptom_dna` dict. No `symptom_router.py` change — see Deliverable 2.)*

### Out of scope
Live activation / default-on; widening the `load_state` vocabulary; re-deriving the `0.65` cap (COMLab-B-pinned); other `environmental_conditions` keys; emitter changes; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "load_state"   comlab/core/fault_atlas_router.py   # read site (symptom-prior step)
grep -nI "enable_ctxmod" comlab/core/fault_atlas_router.py   # the branch that reaches it
"$PY" -m pytest tests/ -q -k "ctxmod"
```
