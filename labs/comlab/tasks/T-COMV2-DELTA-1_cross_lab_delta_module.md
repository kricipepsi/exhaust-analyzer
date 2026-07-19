# T-COMV2-DELTA-1 — Cross-lab delta module (FU-2): two-point delta as a proposal-bounded rank input

> ## ⚠ THIS IS AN UMBRELLA / EPIC — DO NOT ASSIGN THIS FILE TO A CODER
> The work below is too large for one session. It is split into **four linear sub-tasks**, each
> independently green, in smallest-diff order. **Assign these, not this file:**
>
> | Order | Sub-task | Ships | Green-state at close |
> |---|---|---|---|
> | 1 | `T-COMV2-DELTA-1A_schema_foundations.md` | `SINGLE_POINT` + `DegradationLit` widen + `SecondOperatingPointFrame` + `COMLab-DELTA` proposal | field unused, default-`None` → existing suite byte-identical |
> | 2 | `T-COMV2-DELTA-1B_engine_models_and_gates.md` | `delta_engine.py` models + architecture/validity gates + sentinel; profiles stubbed → ABSTAIN | engine standalone, not wired |
> | 3 | `T-COMV2-DELTA-1C_engine_profiles.md` | `_delta_trim`/`_delta_gas`/`_delta_o2`/`_assemble` + profile/abstain tests | engine complete, still not wired |
> | 4 | `T-COMV2-DELTA-1D_router_wiring.md` | Phase 5 read + flag + aggregator + e2e | **consumer meets field → signal/noise closes**; epic done |
>
> Dependency chain: **1A → 1B → 1C → 1D** (1D also needs 1A's request field). The follow-up
> `T-COMV2-DELTA-2` (v2-registry path) is blocked on **1D**.
>
> This file remains the **source of shared context** — the locked decisions, named consumer, risks,
> and out-of-scope below apply to all four sub-tasks. Read it, then read your assigned sub-task.

**Authored:** 2026-06-19 (architect, Cowork). **Split into 1A–1D:** 2026-06-20. **Stage:** 4 (COMLab rework). **Type:** COMLab feature (new analytics module + optional additive input schema + ranker consumer).
**Origin:** `labs/comlab/research/PROPOSAL_DeltaLab_cross_lab_delta_module.md`; closes the long-open **FU-2** consumer named throughout `labs/obdlab/research/chunks/delta-relations/` (and `obdlab/research/SWEEP_MANIFEST.md §7`).
**Drill:** read `START_HERE.md` → `ROADMAP.md` → `AGENTS.md` (five rules) → **this file**, then post the scope-confirm before any code.

> **One-line scope:** add a COMLab-owned module that, *when a case carries a second operating-point frame*, computes per-channel deltas (ΔTrim, Δgas, ΔO₂) across the step and feeds a `delta_signature` into the rank step as a **primary** discriminator; when no second frame is present, behaviour is **byte-for-byte the current single-point path**. The delta fields + their ranker consumer ship in the **same** proposal-bounded change — so this is signal/noise-compliant, not a "future use" field.

---

## ⚠ Gate before build — read first

This task is **buildable and testable now against synthetic fixtures**, but its **live diagnostic value is gated** on a decision that is *not* a coding task:

- **Gate 1 (product/data — precedes live activation):** can the field workflow capture a **second operating-point frame** (low/curb idle **and** an elevated/"stress" point)? The current master corpus is **single-point** (`schemas/ingestion.py` carries one `engine_rpm`/`rpm_state_bucket` per case), so the module **cannot move accuracy** until two-point cases exist. See the proposal §3 and `OPEN_LEVERS_COMLab.md` (run **M1** + **F1** first — they are cheaper and may reset the target).

**Therefore:** build the module + schema + tests behind a **default-off** proposal flag, validated on the synthetic two-point fixtures produced by `WEB_RESEARCH_PROMPT_D_delta_test_fixtures.md`. Do **not** rebuild the corpus or change the single-point default in this task. Live activation is a separate Stage-4 follow-up once Gate 1 clears and emitters emit two-point frames.

---

## Goal

1. Define an **optional, additive** second-frame input on the case payload (absent → unchanged behaviour).
2. Implement a stateless **delta-calculation module** in `comlab/comlab/analytics/` that computes, when both frames are present:
   - **ΔTrim** = `total_trim(elevated) − total_trim(low)` (per bank), per `delta-relations/01`.
   - **Δgas** = `{ΔHC, ΔCO, ΔCO₂, ΔO₂, Δλ}` across the step, per `delta-relations/07`.
   - **ΔO₂** = `{Δswitch_freq, Δvoltage_bias, Δdownstream_response}` (O2logic delta feeder).
3. Emit a typed `delta_signature` and route it into `fault_atlas_router.execute_triage_loop` **Phase 5** as a **primary** rank term (static single-point signature becomes the fallback).
4. Gate the profiles on **air-metering architecture** *before* applying them (mandatory — see Risks).
5. Add a new degradation mode `SINGLE_POINT` (sibling to `GAS_DOMINANT`) so the absent-second-frame path is explicit and the confidence ceiling is honest.

## Named signal/noise consumer (rule compliance)

The `delta_signature` field's consumer is **`fault_atlas_router.execute_triage_loop` Phase 5** (the rank step), added **in this same change**. Per `AGENTS.md` / CLAUDE.md ("a new field ships only with a named consumer, or a proposal that ships its consumer in the same change"), this is compliant: the change is **proposal-bounded** (`proposals/entries.yaml` entry `COMLab-DELTA`) and the consumer is live in the same commit. This is exactly what flips every `delta-relations/*` chunk from `consumer: PENDING (FU-2)` to active.

## Dependencies & gates

| Dep | On | Status |
|---|---|---|
| Gate 1 | two-point capture exists in the workflow/corpus | **OPEN** (product decision) — blocks *live* value, not the build |
| Emitter two-point emission | GASLab/OBDLab/DTCLab emit a per-state frame at each operating point (stateless; COMLab does the cross-state math) | **not yet** — emitters are single-point today; needed for live, not for fixture tests |
| Fixture ground-truth | `WEB_RESEARCH_PROMPT_D_delta_test_fixtures.md` answered → canonical bands + per-fault Δ table + tolerances | pending research (run in parallel) |
| Band reconciliation | one canonical low+elevated pair chosen (2500 vs 3500–4500 conflict, `SWEEP_MANIFEST §7`) | decide in scope-confirm, cite source |

## Success criteria (done = all of these)

- A `delta_signature` is computed and **grep-confirmed read** by `fault_atlas_router` Phase 5 in a live code path (not just emitted). *Green pytest alone is not done — the consumer read is the gate.*
- With **no** second frame, the engine's verdict on every current single-point case is **identical** to pre-change (regression-locked: existing `tests/` suite unchanged and green).
- With a second frame, the module reproduces the **expected Δ sign + magnitude within tolerance** for each fixture in the prompt-D master table, including the **abstain** families and the **architecture null/inversion** cases.
- The architecture gate is exercised: a MAP-only (speed-density) leak fixture does **not** trigger the positive-ΔTrim leak profile; a forced-induction post-turbo leak fixture is read with **inverted** sign.
- `delta_signature` is **proposal-bounded** (`COMLab-DELTA` in `proposals/entries.yaml`) and **default-off**; flipping the flag is the only behavioural change.
- Inner loop clean: `ruff check .` → `pyright comlab/` → `pytest -x -q`. Both `VERIFICATION GATE` and `CODE REVIEW` blocks filled in `progress_notes/T-COMV2-DELTA-1.md`.

## Files to touch (additive where possible)

- `labs/comlab/comlab/analytics/delta_engine.py` (**ADD** — the module).
- `labs/comlab/comlab/schemas/ingestion.py` (**MODIFY** — optional second-frame field; default `None`).
- `labs/comlab/comlab/schemas/vocabulary.py` (**MODIFY** — `SINGLE_POINT` degradation mode; reuse existing `STRESS_IDLE`/`REGULATORY_HIGH_IDLE` buckets `:212–213`).
- `labs/comlab/comlab/core/fault_atlas_router.py` (**MODIFY** — Phase 5 reads `delta_signature` when present).
- `labs/comlab/comlab/config/proposals/entries.yaml` (**ADD** — `COMLab-DELTA`, names the consumer path + the `delta-relations` provenance).
- `labs/comlab/tests/unit/test_delta_engine.py` (**ADD** — fixtures from prompt-D master table).
- `labs/comlab/tests/e2e/` (**ADD/MODIFY** — single-point regression-lock + two-point activation case).
- `labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md` (**DEP-14 registered 2026-06-20** — `delta_signature` row, source-of-record; *was mis-pointed at `v2-restructure/` in the original spec*).
- `labs/comlab/tasks/PROGRESS.md` (**already registered** — flip `T-COMV2-DELTA-1` row to `in_progress`/`done`).

## Out of scope (do NOT do here)

- **Rebuilding the corpus** to two-point, or changing the single-point default. (That is the Gate-1 follow-up.)
- **Emitter changes.** GASLab/OBDLab/DTCLab stay stateless and single-point until a separate emitter task; do not add cross-lab imports (mirror types locally per the boundary rule).
- Any **graphify / KG rebuild** (frozen — query, don't rebuild).
- Weight re-tuning of the static ranker (that is `OPEN_LEVERS` F2, a different task).

## Risks / must-design-for (from research)

- **Architecture modifiers are gates, not options** (`delta-relations/06`): speed-density (MAP-only) **nulls** ΔTrim for a real leak → route to IAC/MAP-at-idle; forced induction **inverts** ΔTrim sign (post-turbo leak ≈ −20 % STFT). Applying a profile without first branching on air-metering/induction **creates** misclassifications.
- **Band conflict** (`SWEEP_MANIFEST §7`): stress band is quoted as 2500 RPM (Δgas matrix, O2logic) vs 3500–4500 (ΔTrim FuelTrimW) vs 2500–3000 (fuel-trim/04). Pick one canonical pair (or per-signal bands) in the scope-confirm and cite it; do not silently mix.
- **Validity at the second reading** (`delta-relations/08`): the vsum 14–18 % / dilution gate and RPM-stability/settle must hold on **both** frames before a delta is trusted — include rejection fixtures.
- **Numeric literals carry a wiki citation** (`# wiki: §…`) per house rule — every band/tolerance traces to the prompt-D answer or the delta-relations chunk.

## Verification

```bash
cd labs/comlab
ruff check . && pyright comlab/ && pytest -x -q
# consumer read is the real gate:
grep -nI "delta_signature" comlab/core/fault_atlas_router.py     # must show a live read in Phase 5
# regression lock (single-point unchanged):
pytest tests/e2e -q -k "single_point or regression"
```

## On completion

Fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-DELTA-1.md`; confirm `delta_signature` is grep-read in a live path and the single-point regression is byte-identical; flip the ledger row → `done`. Then **STOP**. Live activation (two-point corpus + emitter emission) is the separate Gate-1 follow-up, not this task.
