### Goal ###
C9 signal pack, DISCLOSE half — and, under the owner's stop ruling, **the pack's final gatekeeper**.
Simulate — **read-only, in memory** — the C9 `HealthConfirmationState` producer and its NF-001/NF-002
consumers over the `T-V3-P4-C9-SYNTH` seed, against the pinned **`POST_T_V3_P4_C4B`** baseline
(259/294; csv `1063be61…`; `V3_YARDSTICK_2026-07-06-C4B`). No live edit, no yardstick mint.
### OWNER STOP RULING (2026-07-06) — this task's decision frame ###
**89.72% on covered is accepted. No chasing, no tightening.** The sequence tail (C8/C1/C7) is
CLOSED. C9B happens ONLY if this dry-run shows an **obvious** win, defined strictly:
- meaningful yield (several of the 10 no_fault targets flip) **with the contract gates as frozen**
  — if yield appears only after re-sizing boosts, widening bands, or re-tuning thresholds, that is
  chasing → recommend STOP;
- **0 FT-8 regressions** on the full 294, including zero resurrections of NF verdicts that C6/C3
  prunes killed (the guard tension named in C9-PRE §4);
- `era2_016` emits `SENSOR_HEALTH_UNPROVEN_ABSTAIN` (the anti-false-healthy proof) — any C9 state
  that makes it healthier is disqualifying;
- **no abstain-dial change** (MARGIN stays 0.02 — explicitly out of scope under the ruling; report
  masked flips, do not act on them).
End the report with a one-line recommendation: **C9B-GO (obvious win)** or **STOP-CLOSE-PACK
(259/294 stands)** — with the numbers that justify it.
### Success criteria ###
Produce `v3/reports/V3_C9_SIGNAL_DRYRUN_<date>.{md,json}` (simulator `v3/c9_signal_sim.py`, adapt
`c5_signal_sim.py`; py_compile+ruff+pyright clean):
1. **Zero-overlay self-check first:** drift=0 vs `apps/wired/v7/runs/POST_T_V3_P4_C4B/results.json`
   across 294. Non-zero → stop, report.
2. **Producer simulation** per case, gates exactly per contract §2 (all-gates-pass →
   `SYSTEM_HEALTH_CONFIRMED`; any fail/missing → `SENSOR_HEALTH_UNPROVEN_ABSTAIN`). Per-case gate
   trace; era2_016 must fail (pending DTC, margin 1.9%, elevated trims — per seed).
3. **Column-subset scenario ladder** (the cost lens): Scenario 1 = Tier-A OBD-only (readiness,
   DTC counts, Mode $06 margin, reset-age, trims — all standardized-grounded); Scenario 2 = full
   contract (+ Tier-B anecdotal gas deltas). If Tier-A alone banks the same cases, the gas-delta
   columns are not load-bearing — say so (C3A precedent: cheaper commit).
4. **Consumer simulation:** decisive healthy state boosts NF-001/NF-002 (+0.10 per prior packs)
   under LIVE guard semantics read from the shim: C6 decisive prune wins; C3
   CONTROL_REFERENCE_FAULT invalidates; C4 states — disclose any interaction found.
5. **Yield disclosure:** 11 → WOULD_BANK / ALREADY_PASS / STILL_SHORT / ABSTAIN_NO_DATA;
   covered-vs-masked split at MARGIN=0.02 (running masked tally: 12 C3 + 5 C6 + C4B's CASE-022).
   The 10 targets currently lose to catalyst_failure(4)/ecu_fault(2)/rich(1)/sensor(3)/no_fault(1)
   — whether +0.10 outranks them is the yield question; if it doesn't, that is a STOP signal, not
   a request for a bigger boost.
6. **FT-8 neighbour audit:** re-derive the union LIVE post-C4B (contract §7 said 17 — refresh);
   full-294 sim; regressions listed (target empty); currently-passing NF neighbours broken out.
7. Inner loop clean; scoreboard `score` untouched (`top3_family` 259/294, `Hash lock: ok`);
   no engine/lab/registry/corpus/scorer/`run_suite.py`/yardstick/`Vault/` edit.
### Context ###
- Contract: `v3/reports/V3_C9_REVEAL_CONTRACT_2026-07-06.{md,json}` (§2 gates, §4 interactions,
  §7 FT-8, §8 confounders, §10 abstain).
- Seed: `v3/data/c9_synthetic_seed_2026-07-06.{csv,json}` + `V3_C9_SYNTH_BANDS_2026-07-06.md`.
- Live guards: `labs/comlab/registry/integration_shim.py` (read-only).
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
The owner (C9B-GO vs STOP-CLOSE-PACK — final pack decision under the stop ruling).
### Disclosure ###
Surface, don't hide: masked flips; any target where yield would need re-tuning (STOP evidence, not
a to-do); guard interactions; Tier-A vs Tier-B load-bearing split.
### Progress hook ###
Ledger T-V3-P4-C9A → done; dual-gate note `progress_notes/T-V3-P4-C9A.md`.
### Depends on ###
T-V3-P4-C9-SYNTH done ✓ (seed spot-checked at review: era2_016 fails 3 gates honestly) ·
T-V3-P4-C4B done ✓ (baseline `POST_T_V3_P4_C4B` minted at review).
