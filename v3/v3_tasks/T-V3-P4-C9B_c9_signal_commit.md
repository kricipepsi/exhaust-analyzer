### Goal ###
C9 **signal pack COMMIT** — the last commit of the v3 pack under the owner stop ruling. Wire the
`HealthConfirmationState` producer + NF consumers LIVE, sized from `T-V3-P4-C9A` (C9B-GO: 10/10
would-bank, 0 regressions, era2_016 abstains). Re-score, mint the yardstick, persist the named run.
Owner GO: 2026-07-06 ("author c9b-go").
### Column decision — sized from the ladder, not guessed ###
C9A's scenario ladder banks the SAME 10 cases in Tier-A-only as in the full contract → the 4
gas-delta columns (`gas_delta_hc_ppm/co_pct/co2_pct/o2_pct`, anecdotal-grounded) are **not
load-bearing** and are **deferred, not committed** (C3B Δλ precedent). Commit the **7 Tier-A
columns only** (all standardized-grounded): `readiness_supported_complete_bool`,
`stored_dtc_count`, `pending_dtc_count`, `permanent_dtc_count`, `mode06_min_margin_pct`,
`warmup_cycles_since_clear`, `miles_since_clear`. Producer gates = contract §2 Tier-A subset
exactly as C9A Scenario 1 simulated (no re-tuning — the stop ruling forbids it).
### Success criteria ###
1. **S-COMMIT pre-flight:** baseline `POST_T_V3_P4_C4B` (259/294; csv `1063be61…`) unmoved before
   any edit; re-verify with `score` (Hash lock ok).
2. Add the 7 Tier-A columns to `cases_petrol_v7.csv`; populate the 11 C9 rows from
   `c9_synthetic_seed_2026-07-06` (`synthetic=true` provenance in the side file; Tier-A values
   only); non-C9 rows blank on new columns. **era2_016 gets its seeded UNHEALTHY values** (pending
   DTC=1, margin 1.9%, elevated trims are already-live columns — fill only what the schema takes).
3. Wire payload/composition/ingestion/load_corpus + `HealthConfirmationState` StrEnum and producer
   in the registry shim. Consumer: `SYSTEM_HEALTH_CONFIRMED` boosts NF-001/NF-002 **+0.10**;
   `SENSOR_HEALTH_UNPROVEN_ABSTAIN` = no action (no NF prune — not contracted, don't invent).
   Precedence preserved and tested: C6 decisive prune > C9 boost; C3 CONTROL_REFERENCE_FAULT
   invalidates; no C4 interaction (C9A found none — assert in a test).
4. Tests: producer emit paths, era2_016 abstain, C6-prune-beats-C9-boost, data-presence gate
   (None on non-C9 cases). pytest v7 suite green.
5. Score + diff vs `POST_T_V3_P4_C4B`: expected `top3_family` 259→**269**/294 (10 flips; EXT-216
   banks masked — abstained top-3 hits count, the C4B review ruling), `newly_fail` 0,
   `REGRESSIONS: (empty)`. **era2_016 movement watched explicitly:** its live unhealthy values may
   shift its winner away from the false no_fault — unchanged or improved are both acceptable;
   any NEW family regression anywhere is disqualifying. Explain any deviation from 269 case-by-case
   (the C4B lesson: reconcile per case, don't average).
6. Mint `V3_YARDSTICK_2026-07-06-C9B` (oracle + scorer + `run_suite.py` untouched, hash lock ok);
   rebind scorer read-site. **Persist the named run** `apps/wired/v7/runs/POST_T_V3_P4_C9B/results.json`
   via `score --write-results` — NOT optional (the C4B review remediation).
7. Note reports the closing state of the v3 pack: final `top3_family`, coverage, `top3_on_covered`,
   masked tally (12 C3 + 5 C6 + CASE-022 + EXT-216), and the deferred inventory (gas-delta columns,
   abstain-cal, C8/C1/C7 CLOSED) — the pack's handoff summary, since this is the last commit.
### Out of scope ###
No gas-delta columns. No boost re-sizing, no MARGIN change, no NF prune-on-unproven, no C8/C1/C7.
No scorer/oracle/`run_suite.py` edit. `Vault/` untouched. era2_016 is never made healthier.
### Context ###
Sizing: `v3/reports/V3_C9_SIGNAL_DRYRUN_2026-07-06.{md,json}` (Scenario 1). Contract:
`V3_C9_REVEAL_CONTRACT_2026-07-06`. Seed: `c9_synthetic_seed_2026-07-06`. Pattern: T-V3-P4-C5B/C4B
notes + diffs. Load skills: wired-signal-pack.
### Progress hook ###
Ledger T-V3-P4-C9B → done; dual-gate note `progress_notes/T-V3-P4-C9B.md`.
### Depends on ###
T-V3-P4-C9A done ✓ (C9B-GO) · owner GO ✓ (2026-07-06) · FT-8 clean at commit (gate 5).
