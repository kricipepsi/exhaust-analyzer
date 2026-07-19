# T-FL-3 — Classify each failing case → failure mode + stage of first divergence
**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` · **Blocked by:** T-V7-6, T-FL-2
**Mode:** STRICT — analysis + report; **no engine/oracle edits**. · **Scope owner:** wired-fl.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Why this task exists
This is the pack's headline deliverable: **the exact point of failure for every failing
case**, assigned **mechanically** (not by hand) so v3 gets a precise target list and a
per-mode count. It joins three inputs that now exist: the v7 verdict/score, the upstream
lab states (T-FL-2), and the prune/rank spans (T-V7-6).

## Signal/noise
Adds no domain field. The **named consumer** is the v3 build (which mode dominates decides
whether v3 touches GASLab, rank weights, the corpus, or nothing — see the audit's "fix
layer" column) and T-FL-4 (the scoreboard). Each classification must cite the field/span it
rests on; inferred attributions are marked, not asserted.

## Pinned facts (verified at authoring)
- `phase.prune` span carries per-rule `rule_pruned{rule_id, prune_reason, failed_gating_key}`;
  `phase.rank` carries `rule_scored{rule_id, ...}`, `router.winner_id`, `router.candidates_in/out`,
  `router.threshold_miss` (V7_ACCURACY §6 + T-WTEST-4 span dump).
- The correct family's rule ids are derivable from `labs/comlab/registry/rules/<family>.json`.
- Surface defects (`fault_code` namespace, `confidence` band) are F-V7-CODE-NS / -CONF-SAT —
  classify these as `SURFACE_DEFECT`, never as routing failures.

## The classifier (deterministic; one mode per failing case)
For each accuracy case that fails on **family/state** (surface dims excluded), assign exactly one:
| Mode | Decision rule (evidence required) |
|---|---|
| `SURFACE_DEFECT` | family+state actually PASS; only `fault_code`/`confidence` failed |
| `PRODUCER_GAP` | the correct family's rule(s) appear in `rule_pruned` with `failed_gating_key` = a state the upstream lab did **not** emit (cross-check T-FL-2 capture) |
| `PRUNED_OTHER` | correct rule in `rule_pruned` for a non-producer `prune_reason` (contract/gate) |
| `OUTRANKED` | correct rule present in `rule_scored` but `winner_id` ≠ it; record winner family, winner vs correct score, and the deciding evidence rows |
| `DATA_GAP` | correct family has **no** firing path because the discriminating input is absent (e.g. OBDLab `NO_FAULT`, no DTC) — not merely outranked |
| `ORACLE_SUSPECT` | engine answer is defensible vs the wiki (carry the T-FL-1 adjudication); flag for oracle correction, not engine |

Precedence when ambiguous: `SURFACE_DEFECT` → `ORACLE_SUSPECT` → `PRODUCER_GAP` →
`PRUNED_OTHER` → `OUTRANKED` → `DATA_GAP`. State the precedence applied per case.

## Success criteria (verify against these; loop until all hold)
1. Every failing accuracy case is assigned **exactly one** mode with a cited span/field; the
   per-case table records `case_id, expected, predicted, stage_of_first_divergence
   (gaslab|obdlab|dtc|prune|rank|surface), mode, evidence_ref`.
2. **Stage of first divergence** is named per case from the spans (where the pipeline first
   deviated from the path that would have produced the expected family).
3. Aggregates: **per-family × per-mode** matrix and a **per-mode total**, with the dominant
   mode per dead family called out (expected from the audit: `PRODUCER_GAP`/`OUTRANKED` on
   `mechanical_wear`/`exhaust_leak`; `DATA_GAP` on `ecu_fault`).
4. Cross-checks the audit's row-level claim: confirm or refute that the `mechanical_wear`
   cases are pruned on `WORN_*` GATING and won by misfire on `P0300`+HC — with the span
   evidence (this is the §3 "inferred link" of the rebuild-failure audit, now resolved).
5. Write `apps/wired/fl_tasks/reports/FL_LOCALIZATION_<date>.md`; log no engine fixes (v3 owns those).

## Scope
**IN:** the join + classifier (under `fl_tasks/`); the per-case localization table; the
per-family/per-mode aggregates; the audit cross-check; the report.
**OUT:** editing engine/oracle/lab/wiki; tuning; `graphify`; `Vault/`; committing run/trace JSON.

## Gate (STRICT dual-gate → `progress_notes/T-FL-3.md`)
- **VERIFICATION GATE:** paste the per-mode totals, ≥3 fully-cited per-case classifications
  (one `PRODUCER_GAP`, one `OUTRANKED`, one `DATA_GAP`), and the mechanical_wear cross-check
  with span evidence.
- **CODE REVIEW:** confirm zero source edits; every classification cites observable evidence;
  inferred attributions are marked.
