# SEMANTIC pack — Progress Ledger

**Pack:** Semantic-vocabulary standardization (cross-lab) · **Mode:** STRICT (both gates clean before `done`).
**Bootstrap:** `labs/semantic/SEMANTIC_START_HERE.md` · **Spec source:** `labs/semantic/SEMANTIC_STANDARDIZATION_PROPOSAL.md`.
**Last updated:** 2026-06-10 (architect: T-SEM-5 authored — OBD vocab reconcile-to-code, from OBDLab handoff TODO-1/2).

## Scope gate (what this pack closes)

Closes "**what is our semantic standard + how do new faults get added**" — L1/L2 dual ISO-primary
standards citations, the EP-DTC-02 taxonomy backbone as the fault-atlas routing/registry spine, the
`comlab/config/proposals/` registry + graduation rule, and a **growth-safe** conformance/extensibility gate.
`FaultFamily` (L3) is **not** touched. Fault *discrimination* implementations stay in their lab ledgers and
flow through the mechanism this pack builds.

## Task log

| ID | Task file | Status | Blocked by | Consumer (signal/noise) | Notes |
|---|---|---|---|---|---|
| **T-SEM-1** | `T-SEM-1_iso_primary_citations.md` | **done** | — | N/A — citation/comment edit, adds no field; feeds T-SEM-4 | dual-anchor ISO-primary citations applied; zero value churn (comments-only diff verified); suite unchanged-green |
| **T-SEM-2** | `T-SEM-2_proposals_registry_taxonomy_backbone.md` | **done** | T-SEM-1 | `fault_atlas_router` (routes against the family registry) | proposals registry + EP-DTC-02 backbone live; router read path verified; graduation rule + citation convention documented; no L3/live-KG change |
| **T-SEM-3** | `T-SEM-3_register_connected_eps.md` | **done** | T-SEM-2 | each entry names its own consumer (EP-COM-05/04/06, EP-OBD-17, EP-DTC-01, …) | connected EPs registered as `proposed` entries with consumer+citation; high-risk index recorded; no implementation, no live-KG/L3 change |
| **T-SEM-4** | `T-SEM-4_conformance_extensibility_gate.md` | **done** | T-SEM-1, T-SEM-3 | CI / inner loop (the gate is the consumer of the citations + registry) | Growth-safe conformance gate green; no hardcoded counts (grep clean); negative proof red on missing-consumer / missing-citation / bogus-P-code |
| **T-SEM-5** | `T-SEM-5_obd_vocab_reconcile_to_code.md` | **done** | — | N/A — adds no field; documents already-shipped+consumed enums (`WIDEBAND_OFFSET_CANDIDATE`→COMLab `T-COMV2-O2OFFSET-1`; `FuelSystemStatus`→COMLab router/analytics + DTCLab) | OBD_VOCABULARY §12.4 `O2FailureMode` 7→4 + §5.2 add `FuelSystemStatus`, synced across all 3 live copies; propagate `SEMANTIC_CONTRACT §4.4` fix to comlab wiki copy. `.md`-only; no proposal needed (consumers already live). From OBDLab handoff TODO-1/2 |

**Unplanned follow-ups (out of scope — surfaced, do not fix in-pack):**

| # | Item | Where it belongs |
|---|---|---|
| 1 | L3 family-count drift: `FaultFamily` StrEnum (12) vs `response.FaultFamilyLit`/`kg.FaultFamilyLit` (16, incl. REG-V2 `invalid_input`/`vacuum_leak`/`overheating`/`charging_system`) vs `SEMANTIC_CONTRACT §8`/`OBD_VOCABULARY §6` (12). Settle before any L3-verdict task. | COMLab ledger (REG-V2) |
| 2 | `ChemicalSignature` count: `GAS_VOCABULARY §3` advertises 34; `comlab` enum still ~32 incl. `WRONG_VALVE_TIMING`. | GASLab v2 slate (32→34) |
| 3 | Discrimination implementations (sensor_fault target split, lean/rich cross-layer, signature matrix) registered here but implemented per-lab. | OBDLab / COMLab ledgers |
| 4 | `TestSuite/COM/SEMANTIC_CONTRACT.md` (frozen May-22 harness fixture) is a 3rd contract copy not covered by T-SEM-5. Owner decision needed: sync to live wikis or leave frozen (risks harness). | Owner / TestSuite ledger |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred` · `void`.

**Runnability (shared — `AGENTS.md` Rule 3):** `pending` = runnable now (spec authored, blockers `done`). Forward-registered/unauthored rows stay `deferred`, never `pending` or a `pending (...)` variant (the deprecated `pending (next)` collapses to plain `pending` — ordering marks "next"). The first `pending` row top-to-bottom is the next runnable task; `deferred`/`blocked` are skipped.
**Sequencing:** T-SEM-1 → T-SEM-2 → T-SEM-3 → T-SEM-4 → T-SEM-5. One task per session; the coder runs the
first `pending` row whose Blocked-by IDs are all `done`, never authors the spec.
