# OBDLab audit backlog — proposed task rows (2026-06-08)

Task specs derived from the 5-lens skills audit (`audit/AUDIT_0[1-5]_*.md`). **Status
reconciled 2026-06-10: all rows below are merged into `tasks/PROGRESS.md` and `done` —
this table is now a historical record, the live ledger is `tasks/PROGRESS.md`.** When the
audit was filed each row carried a disposition for the owner to sequence/ratify; that has
happened. **Test-infrastructure findings are excluded by owner instruction** — they belong
to the future GASLab-parity test-infra build, not this backlog.

## Suggested order

1. **🔴 first:** FIX-2 (dead wideband detector) and FIX-1 (dead Physics Gate 3) — shipped
   features that don't run. FIX-3 (stateful orchestrator) — order-dependent output.
2. **🟡 next:** FIX-4 (bank default), FIX-5 (exception taxonomy), FIX-6 (dead control flow).
3. **🟡 decisions:** ARCH-1 (ranking consumer) and ARCH-2 (orphan members) — owner rulings;
   ARCH-1 should precede any FIX-6 cleanup that touches `ranking.py` internals.
4. **🟢 last / opportunistic:** FIX-7 (hygiene bundle).

## Proposed PROGRESS.md rows

| ID | Task file | Status | Blocked by | Consumer (signal/noise) | Notes |
|---|---|---|---|---|---|
| **T-OBDV2-FIX-1** | `audit_backlog/T-OBDV2-FIX-1_physics_gate_3_dead.md` | done — Option B | — | §4 semantic-gate contract → COMLab fault-atlas routing | 🔴 Gate 3 reads `calculated_ve`, never set pre-semantic → always inert; only unit tests inject it. Recommend **remove** (emitter-consistent) vs move-after-VE; owner ratifies wiki §4. |
| **T-OBDV2-FIX-2** | `audit_backlog/T-OBDV2-FIX-2_wideband_offset_dead.md` | **done** | — | `WIDEBAND_OFFSET_CANDIDATE` → COMLab `T-COMV2-O2OFFSET-1` (already registered) | 🔴 T-OBDV2-6 string→enum migration **missed `o2_normalizer`**; `fuel_status == "Closed_Loop"` always False → T-OBDV2-4 detector dead. Also single-sources the fuel-status map (UB-3). |
| **T-OBDV2-FIX-3** | `audit_backlog/T-OBDV2-FIX-3_destate_orchestrator_linearity.md` | **done** | — | `w_theo`/`sensor_error_delta` → COMLab `T-COMV2-MAF-LIN-1` (recompute only) | 🔴 Two-point linearity uses translator **instance state** → `sensor_error_delta` depends on call order; not thread-safe. Thread the prior band explicitly. |
| **T-OBDV2-FIX-4** | `audit_backlog/T-OBDV2-FIX-4_number_of_banks_default.md` | **done** | — | bank-2 fields → COMLab (T-OBDV2-BANK-ASYM-1); default-fix only | 🟡 `number_of_banks` defaults to **2** in validator, **1** in aggregator/assembly → disagreeing bank semantics on omitted input. Standardise on 1. |
| **T-OBDV2-FIX-5** | `audit_backlog/T-OBDV2-FIX-5_exception_taxonomy.md` | **done** | — | COMLab fusion error-handling path (**name it**) | 🟡 `SemanticConsistencyError(AssertionError)` + gate-4 bare `ValueError` vs gates 1-3; docstring contract mismatch. Add `ObdLabError` root; gate-4 → `SemanticConsistencyError`. |
| **T-OBDV2-FIX-6** | `audit_backlog/T-OBDV2-FIX-6_dead_code_removal.md` | **done** | — | — (behaviour-preserving) | 🟡 No-op `try/except` in `evaluate`; discarded `_evidence_tier(...)` calls + duplicate tier fns in `ranking`. |
| **T-OBDV2-FIX-7** | `audit_backlog/T-OBDV2-FIX-7_code_hygiene_bundle.md` | **done** | — | — (internal) | 🟢 Bundle: `raise … from` (P-2), dup thresholds 70/90 (P-3), dead `total_trim` param (P-4), import-time YAML (P-5), VE-skew doc drift 85 vs 90 (ARCH-3). |
| **T-OBDV2-ARCH-1** | `audit_backlog/T-OBDV2-ARCH-1_ranking_consumer_decision.md` | **done** | — | — (removal) | 🟡 `ranking.py`/`family_map.py` (~346 LOC) imported only by own tests; named consumer (OBDLabSimple→COMLabSimple) is archived. **Owner ruling: excise** with `*Simple` cleanup. Removes `O2FailureMode.DEAD`'s only reader → ARCH-2 re-spec after this lands. |
| **T-OBDV2-ARCH-2** | `audit_backlog/T-OBDV2-ARCH-2_orphan_members_proposal_or_prune.md` | **done** | — | per-member (proposal registry or removal) | 🟡 Orphans: `VERoutingMode`, `cylinder_count`, `O2FailureMode.{SLUGGISH,DEAD,WRONG_CENTERLINE,HEATER_FAULT}`. Proposal (named producer+consumer) or prune, per member. |

## Explicitly deferred (NOT in this backlog — test-infra build)

Per owner instruction (OBDLab lacks GASLab-parity test infrastructure, `labs/gaslab/tests`):
the `ecc-testing` lens items — generative/fuzz/combinatorial stubs (E-1), missing eval
harness (E-5), integration "fault-fires" assertions (ECC-1), conftest fixture hoist (E-3/ECC-2),
and the ruff/pyright ruleset tightening (P-1) — are **deferred to the OBDLab test-infra task**.
When that lands, sequence it **after** FIX-1/FIX-2 so generated cases exercise live, not dead,
fault paths.
