# T-V7-7 — Investigate the canonical `fault_code` contract (F-V7-CODE-NS)
**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` (runnable now) · **Blocked by:** —
**Mode:** STRICT — **READ-ONLY**, decision memo only; **no source/oracle/wiki edits**. · **Scope owner:** wired-v7.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Why this task exists
F-V7-CODE-NS gates the v7 accuracy % (294/294 `fault_code` FAIL). The engine emits short-form
`MF-001`; the oracle, the KG node keys, and ~6859 in-tree refs use canonical `ERR-MF-001`.
The owner's disposition is **investigate first** — confirm which id is the intended *public
verdict contract* before any fix is authored. This task produces that decision; it changes
nothing.

## Signal/noise
Adds no field. The **named consumer** is the architect, who will author exactly one fix task
from this memo's recommendation (engine-resolve-to-canonical **or** oracle-correct-to-short).
The memo's job is to make that a one-line decision with evidence, not a guess.

## Pinned facts (verified at authoring, 2026-06-30)
- Engine: `DiagnosticVerdict(fault_code=fault_id, ...)` with `confidence_score=winner_score`
  (`labs/comlab/comlab/core/fault_atlas_router.py`, verdict-construction block ~L2197).
  `fault_id = winner.fault_id` (~L2131); `OPTIMAL_HEALTH` sentinel for no-fault (~L2169).
- Actual run `v7/runs/20260630_163900/results.json` emits short codes: `MF-001`, `LC-001`,
  `RM-001`, `SF-002`, `EF-004`, … (so `winner.fault_id` is the **short** candidate id at
  runtime, even though some router comparisons reference `ERR-LC-002` at L1525).
- KG node keys are `ERR-` form: `labs/comlab/comlab/config/kg/*.json` top-level keys =
  `ERR-LC-001`, `ERR-MF-002`, …; oracle CSV `expected_fault_code` = same `ERR-` form.
- Scorer: `run_suite.py:158` case-insensitive equality on `fault_code` — 0/294 match.

## The question to answer (one decision, with evidence)
Which id is the **intended public verdict code** on `DiagnosticVerdict.fault_code`?
- **(A) Canonical `ERR-` KG id** → engine is under-qualified: it surfaces the bare candidate
  id instead of resolving `winner.fault_id` through the KG. Fix = engine-side (changes the
  verdict contract for **every** consumer). Cost/risk: enumerate consumers of
  `diagnostic_verdict.fault_code` and confirm none rely on the short form.
- **(B) Short `MF-001` candidate id** → the verdict is correct; the oracle column is
  over-qualified. Fix = oracle-side (re-pin T-V7-3's `expected_fault_code` to short form).
  Cost/risk: confirm the short id space is stable and unambiguous across families.

## Success criteria (verify against these; loop until all hold)
1. Enumerate every reader of `diagnostic_verdict.fault_code` (UI output schema, COMLab
   consumers, tests, registry) and record which id form each expects — grep evidence, not
   assertion.
2. State whether short `MF-001` ids are **unique** across the corpus's families (i.e. whether
   option B is even safe), with the collision check shown.
3. Confirm whether a short→`ERR-` resolution path already exists in the router/KG (so option A
   is "surface the existing resolved id" vs "build new resolution") — cite the function.
4. Deliver a memo with a **single recommended option (A or B)**, the consumer-impact list, and
   the exact file+symbol the eventual fix would touch. Mark recommendation as architect-input,
   not self-executed.

## Scope
**IN:** read engine/router/KG/registry/UI-schema/tests; grep consumer surfaces; write
`apps/wired/v7_tasks/reports/V7_CODE_NS_DECISION_<date>.md`; update `F-V7-CODE-NS` note in
`V7_PROGRESS.md` with the recommendation + "awaiting owner sign-off".
**OUT:** editing the engine, the oracle CSV, the KG, the wiki, or any test; re-running the
suite (the data is already in the run JSON); `graphify`; `Vault/`.

## Gate (STRICT dual-gate → `progress_notes/T-V7-7.md`)
- **VERIFICATION GATE:** paste the consumer-surface grep table, the short-id collision check,
  and the resolution-path citation.
- **CODE REVIEW:** confirm zero source edits; the memo recommends, it does not implement.
