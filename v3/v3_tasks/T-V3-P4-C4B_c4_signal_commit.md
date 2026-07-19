### Goal ###
C4 **signal pack COMMIT** — wire the two-point ΔSTFT producer + dilution/bias discriminators LIVE,
sized from `T-V3-P4-C4A-R` (NOT the stale C4A), under the owner's add-column decision
(**2026-07-06: FULL — add the non-corpus columns**). Re-score, mint the new yardstick.
### Owner decision recorded ###
Fork presented from the C4A-R evidence; owner chose **Full signal set**: commit the Scenario-3
producer exactly as simulated. Expected yield: **11/11 C4 top-3 flips** — 10 covered
(7 exhaust_leak + 3 lean_condition) **+ CASE-022 as a MASKED flip** (top-3 hit, stays abstained).
**Metric ruling (review correction, do not re-litigate):** per C3A/SCORERWIN precedent, abstained
top-3 hits BANK `top3_family`. The C4A-R report's "STILL_SHORT" label for CASE-022 and its
simulated 260 undercount by 1 — commit target is `top3_family` 250→**261**/294. If the live run
lands 260, the discrepancy is the C4A-R sim's abstain handling — investigate, don't paper over.
### Success criteria ###
1. **S-COMMIT pre-flight** (the C5B/C6B ritual): re-verify baseline `POST_T_V3_P4_C5B` /
   `V3_YARDSTICK_2026-07-06-C5B` (csv `c49c17af…`) unmoved before any edit; stop and re-pin if not.
2. **Already-live-column audit first:** of the Scenario-3 column set (`co2_idle_pct`,
   `tailpipe_o2_elevation_pct`, `downstream_o2_v`, `propane_trim_shift_pct`; trims already live via
   C2B/C5B), add ONLY those absent from the live schema. Values for the 11 C4 cases from the
   C4-SYNTH seed (owner-pinned value4.1; provisional-synthetic policy: grounded, tolerance-wide,
   `synthetic=true` provenance carried in the side file; evidence-tier **anecdotal** carried as a
   label). Wire payload/composition/load_corpus + the C4 producer state in the registry shim.
3. **Producer gates exactly as C4A-R Scenario 3 simulated** (LEAK: Δ≤−8pt OR co2<12% OR
   tailpipe-O2>2.5%; PERSIST_BIAS: downstream>0.7V ∧ propane>−15%; PERSIST_LEAN: downstream≤0.4V ∧
   propane≤−15%; else ABSTAIN). Consumer deltas per the rebase report's commit-scope section.
4. **Collision/precedence guards disclosed and preserved:** C3 precedence; C5 interaction is NEW
   ground — C4's PERSIST_LEAN overlaps `LeanRootCauseState` territory (both boost LC-00x). Define
   and document the C4/C5 agreement rule (concordant states reinforce; discordant → the
   better-grounded producer wins or both abstain) — surfaced in the commit note, not silent.
5. **FT-8 at commit:** re-derive union live (C4A-R saw 35); full-294 rescore;
   `REGRESSIONS: (empty)` mandatory. Masked split reported (CASE-022 + running abstain-cal tally
   12 C3 + 5 C6 + this pack's contribution).
6. Mint `V3_YARDSTICK_2026-07-06-C4B` (csv hash recorded; oracle + scorer + `run_suite.py`
   untouched, hash lock ok). Ledger + dual-gate note `progress_notes/T-V3-P4-C4B.md`.
7. **Stop-rule re-measure** stated in the note: `top3_on_covered` after commit (C4A-R sim said
   0.90) — feeds the C9/C8/C1/C7 continue-or-stop decision.
### Out of scope ###
No scorer/oracle/`run_suite.py` edit. No abstain-dial change (MARGIN=0.02). No C9 wiring.
`Vault/` untouched. Never re-seed or back-solve CASE-022 to force coverage — masked is the honest
outcome until abstain-cal.
### Context ###
Sizing: `v3/reports/V3_C4_SIGNAL_DRYRUN_REBASE_2026-07-06.{md,json}` (scen3_full). Seed:
`v3/data/c4_synthetic_seed_2026-07-05.*` + bands report. Commit pattern: T-V3-P4-C5B note + diff.
Load skills: wired-signal-pack.
### Depends on ###
T-V3-P4-C4A-R done ✓ · owner sign-off + add-column decision ✓ (2026-07-06, FULL) · FT-8 clean at
commit time (gate 5).
