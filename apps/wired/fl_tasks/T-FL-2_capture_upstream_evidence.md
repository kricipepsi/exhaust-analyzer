# T-FL-2 — Capture per-case upstream evidence (GASLab state + OBDLab mode)
**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` (runnable now) · **Blocked by:** —
**Mode:** STRICT — additive read-only capture; **no engine/lab edits**. · **Scope owner:** wired-fl.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Why this task exists
The proven failure mechanism is a **producer gap**: the correct family's rule is pruned
because the upstream lab never emitted the GATING state it needs (e.g. `MW-001` needs
chemistry `WORN_PISTON_RINGS`; GASLab emits a generic high-HC state instead). But the final
`OrchestratorFinalUIOutput` does **not** expose the GASLab chemistry state or the OBDLab
fault mode (verified: not in `comlab/schemas/response.py`; `run_suite.py` never reads them).
So the evidence that proves producer-gap is currently **invisible**. This task captures it
per case, read-only, so T-FL-3 can classify mechanically instead of by hand.

## Signal/noise
Adds no domain field to the engine. The **named consumer** is T-FL-3's failure-mode
classifier: it needs, per case, *what state GASLab actually emitted* and *what OBDLab
reported* to decide `PRODUCER_GAP` vs `OUTRANKED` vs `DATA_GAP`. Capture only the fields a
classifier consumes — nothing speculative.

## Pinned facts (verified at authoring)
- Final output lacks upstream states; `run_suite.py:87` reads only
  `execution_meta.lab_routing_directive.reasons`.
- The COMLab `phase.prune` span already emits, per pruned rule, a `rule_pruned` event with
  `rule_id`, `prune_reason`, `failed_gating_key` (`fault_atlas_router.py` REG-V2 branch ~L1918).
  This is the **most direct** producer-gap signal — the gating key that wasn't satisfied.
- GASLab emits a `ChemicalSignature` (e.g. `WORN_PISTON_RINGS`, `IGNITION_MISFIRE`,
  `TIMING_RETARDED`); OBDLab emits an `o2_failure_mode`. Both are computed mid-pipeline.

## Success criteria (verify against these; loop until all hold)
1. For all 314 cases, produce a per-case record `{case_id, gas_chemistry_states[],
   obd_o2_failure_mode}` captured **without modifying any engine/lab source** — via a
   read-only replay of the GASLab/OBDLab stage on the same sanitized inputs the composition
   feeds them, or a non-invasive capture hook in the `fl_tasks` harness. State which, and
   prove the captured states match what the live pipeline used (spot-check ≥3 cases against
   the `phase.prune` span's `failed_gating_key`).
2. Join the capture to the run results by `case_id`; write
   `apps/wired/fl_tasks/reports/FL_UPSTREAM_<date>.md` (or a sibling JSON the harness emits)
   with the per-case table + a coverage line (states captured for N/314).
3. For the dead families (`mechanical_wear`, `exhaust_leak`, `non_starter`), explicitly show
   the **emitted** GASLab state vs the **required** GATING state of that family's rules —
   this is the producer-gap proof the audit inferred but did not run.
4. No source file outside `fl_tasks/` (and, if unavoidable, an **additive** read-only helper
   under `apps/wired/v7/` or `apps/wired/trace/`) is changed.

## Scope
**IN:** a read-only capture harness under `apps/wired/fl_tasks/`; the per-case upstream
record + report; the dead-family emitted-vs-required comparison.
**OUT:** editing GASLab/OBDLab/COMLab/engine source; changing the verdict schema; tuning;
`graphify`; `Vault/`; committing run JSON.

## Gate (STRICT dual-gate → `progress_notes/T-FL-2.md`)
- **VERIFICATION GATE:** paste the capture-method proof (≥3 cases matching the prune span),
  the coverage line, and the dead-family emitted-vs-required table.
- **CODE REVIEW:** confirm no engine/lab edit; any helper is additive and read-only; ARCHIVE-free.
