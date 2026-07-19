# T-V7-8 — Investigate `confidence_score` semantics + saturation (F-V7-CONF-SAT)
**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` (runnable now) · **Blocked by:** —
**Mode:** STRICT — **READ-ONLY**, decision memo only; **no source/oracle/wiki edits**. · **Scope owner:** wired-v7.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Why this task exists
F-V7-CONF-SAT is the second P0 gating the v7 accuracy % (273/294 `confidence` FAIL). The engine
passes the winner score straight through (`confidence_score=winner_score`), saturating ≥0.95
(172 cases = exactly 1.0); the oracle bands are calibrated mid-range (e.g. `[0.7,0.9]`), so only
21/294 land in band. The owner's disposition is **investigate first** — determine what
`confidence_score` is *meant to represent* before deciding whether the engine over-states or the
oracle is mis-calibrated.

## Signal/noise
Adds no field. The **named consumer** is the architect, who authors one fix task from this memo:
either recalibrate the engine scorer or re-pin the oracle bands. The memo must make that a
single evidenced decision.

## Pinned facts (verified at authoring, 2026-06-30)
- Engine: `confidence_score=winner_score` raw passthrough
  (`labs/comlab/comlab/core/fault_atlas_router.py` verdict block ~L2204).
- Observed distribution (run `20260630_163900`, 294 accuracy cases): `1.00`×172, `0.95`×79,
  `0.93`×18, `0.90`×22, `0.80`×2, `0.96`×1 → 251/294 ≥0.95.
- Oracle windows pinned by T-V7-3 are mid-band; scorer rule `min ≤ score ≤ max`
  (`run_suite.py:115-116,150`). 21/294 in band.

## The question to answer (one decision, with evidence)
What is `confidence_score` the calibrated probability *of*, and against that definition is the
saturation an **engine** defect or an **oracle** mis-calibration?
- **(A) Engine over-states** → `winner_score` is a raw ranking score, not a calibrated
  confidence; passing it through is wrong. Fix = engine-side recalibration/normalisation. Risk:
  changes confidence on every verdict + any consumer/threshold keyed on it.
- **(B) Oracle bands wrong** → the live scorer's high confidence is the intended semantics; the
  oracle's mid-band windows were pinned to a stale/assumed calibration. Fix = re-pin oracle
  bands to the live scorer's distribution per family.

## Success criteria (verify against these; loop until all hold)
1. Locate where `winner_score` is computed and state its definition/range (is it a normalised
   probability, a margin, an unbounded rank score?) — cite the computation, don't assert.
2. Find any spec/wiki/LLD statement of what `confidence_score` means to a verdict consumer, and
   any downstream threshold that reads it (e.g. demotion/abort gates) — grep evidence.
3. Record where T-V7-3 sourced the oracle bands (wiki? assumed?) — establishes whether band B is
   defensible.
4. Deliver a memo with a **single recommended option (A or B)**, the affected
   files+symbols, and the consumer/threshold impact. Architect-input, not self-executed.

## Scope
**IN:** read the scoring path + verdict consumers + any confidence threshold; trace the oracle
band provenance via T-V7-3 notes; write
`apps/wired/v7_tasks/reports/V7_CONF_DECISION_<date>.md`; update `F-V7-CONF-SAT` note in
`V7_PROGRESS.md` with the recommendation + "awaiting owner sign-off".
**OUT:** editing the scorer, oracle CSV, wiki, or tests; re-running the suite; `graphify`;
`Vault/`.

## Gate (STRICT dual-gate → `progress_notes/T-V7-8.md`)
- **VERIFICATION GATE:** paste the `winner_score` definition citation, the consumer/threshold
  grep, and the oracle-band provenance.
- **CODE REVIEW:** confirm zero source edits; recommendation only.
