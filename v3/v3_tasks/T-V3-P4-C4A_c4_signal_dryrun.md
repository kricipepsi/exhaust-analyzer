### Goal ###
The C4 **signal pack**, DISCLOSE half. Simulate — **read-only** — the proposed **two-point ΔSTFT
producer** (leak vs persist) plus the C4-distinct dilution/bias discriminators over the shared C5/C6
columns, run the EL/LC/SF consumer rules as an overlay on current scores, and predict exactly which
of the 11 C4 cases flip into top-3 and whether any neighbour regresses (FT-8 = full-corpus
no-regressed-family audit). **No live lab/registry/corpus edit, no yardstick mint.** It proves the C4
ΔSTFT signal actually separates exhaust_leak from true-lean and biased-O2 on the seed **before** the
commit (`T-V3-P4-C4B`) touches the engine.

### Progressive-disclosure role — the DISCLOSE step, with the C4 column-add gate ###
C4 is unusual: **it asks for no new corpus column** (acquisition spec §C4). Its discriminator is the
**interpretation** — ΔSTFT idle→2500 computed from the shared C5 trim columns. This task discloses
two things the commit needs:
1. **ΔSTFT yield:** run over the seeded trims, how many of the 11 flip. Expectation from the oracle
   mix: ΔSTFT-collapse should bank the **7 exhaust_leak** cases (Δ≥8 pt) and separate them from the
   **4 {lean+bias}** (Δ persists). Report actual.
2. **The deferred column-add decision:** ΔSTFT alone likely **cannot** split the 3 lean_condition
   from the 1 biased-O2 (CASE-022) — that needs downstream-O2 V / propane, which are **not corpus
   columns**. This task must name exactly which STILL_SHORT cases would require adding those columns,
   so `C4B` decides **add-column-or-abstain** from evidence, not guesswork. Reveal first; commit later.

### Data gate (provisional synthetic seed) ###
Runs on the **synthetic C4 seed from `T-V3-P4-C4-SYNTH`** (grounded in owner-pinned value4.1,
tolerance-wide, `synthetic=true`, evidence-tier `anecdotal`) — not owner data. value4.1 is the
**definitive** C4 answer (follow-up already resolved); no further C4 research is pending. Report
predicted flips as **synthetic-driven** and carry the value4.1 evidence tier into the report header (a
scoreboard label, not a blocker). Columns consumed: shared `stft_idle_pct, ltft_idle_pct, stft_2500_pct,
ltft_2500_pct` (→ derived `delta_stft_idle_2500_pct`) plus the C4-distinct `co2_idle_pct,
tailpipe_o2_elevation_pct, downstream_o2_v, propane_trim_shift_pct` from the seed side file. Cases the
seed cannot ground stay abstained — do not fill them.
The 11 C4 cases: CSV-129, CSV-130, EXT-238, EXT-239, PDF-HI-007, TC-048, YAML-CSV95, CASE-020,
CASE-022, EXT-211, EXT-212.

### Why this split (the trap it avoids) ###
Wiring a ΔSTFT producer + EL/LC/SF weight straight into the live engine risks (a) shipping a
discriminator that is *diagnostically wrong* on real values — worse than a miss — and doubly risky
here because the C4 bands are **anecdotal** (value4.1); and (b) regressing a neighbour that shares the
`exhaust_leak`/`lean_condition`/`sensor_fault` rules or their `competition_group`. Both are checkable
by simulating the overlay read-only, exactly as `T-V3-4A` simulated reweights. No engine state mutated.

### Success criteria ###
Produce `v3/reports/V3_C4_SIGNAL_DRYRUN_<date>.{md,json}` from the C4 seed:
1. **Producer simulation:** compute `delta_stft_idle_2500_pct` per case; apply the proposed emit rule
   (LEAK when Δ collapses ≥ leak-threshold toward 0 at 2500; PERSIST_LEAN vs PERSIST_BIAS when trims
   stay elevated, split by downstream-O2 V / propane where present — thresholds per value4.1) and
   record the state each case would emit.
2. **Consumer simulation:** overlay the resulting state onto the C4 consumer rules
   (`exhaust_leak.json` EL-001/EL-003, `lean_condition.json` LC-001/LC-002, `sensor_fault.json`
   SF-001/SF-002/SF-008) and recompute each case's family rank read-only. Record predicted new rank +
   top-3 membership.
3. **Yield disclosure:** of 11 → how many flip to top-3 (`WOULD_BANK`), how many still miss
   (`STILL_SHORT` — say why: ΔSTFT ambiguous / needs a non-corpus column / genuine overlap), how many
   ungroundable (`ABSTAIN_NO_DATA`). **Break out the 7 leak / 3 lean / 1 bias groups separately.**
4. **Column-add gate (C4-specific):** name every STILL_SHORT case whose separation requires adding
   `co2_idle_pct` / `downstream_o2_v` / `propane_trim_shift_pct` as a corpus column — this is the
   deferred decision `C4B` must rule on. If ΔSTFT-over-shared-columns alone banks a case, say so (no
   new column needed).
5. **FT-8 neighbour audit:** enumerate every case that shares a touched rule / `competition_group`
   and simulate whether the overlay changes its family — list any predicted regression by case_id.
6. **Commit scope for C4B:** the exact producer threshold + consumer change + **which (if any) new
   column** the commit should make, sized from the simulation (not guessed).
- **Self-check:** zero-overlay (no new state) reproduces current ranks for all 294 (no drift), same
  discipline as `T-V3-4A`, before any C4 case is simulated.
- Inner loop clean on the helper (`py_compile`, `ruff`, `pyright`). `top3_family`, the yardstick, the
  live corpus, and every registry/lab file are **untouched**.

### Disclosure (what this task must surface, not hide) ###
If fewer than 11 flip, that shortfall **is** the finding — separate "ΔSTFT ambiguous on the seed",
"needs a non-corpus column", and "genuine overlap". Because the C4 bands are anecdotal, be especially
careful **not** to tune the ΔSTFT threshold to force the 11 to pass — report what the value4.1 bands
actually yield. Name every neighbour the overlay would regress so `C4B` looks exactly as risky as it
is. Restate that any banked C4 case is **synthetic-driven on anecdotal bands**, not real accuracy.

### Context ###
- C4 contract (shared-column note, producer/consumer path, 11 cases): `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md` §C4 + JSON `contracts.C4`.
- Seed to simulate on: `v3/data/c4_synthetic_seed_2026-07-01.*` (from `T-V3-P4-C4-SYNTH`).
- Read-only rank-overlay precedent: `v3/tunable_reweight_sim.py` (`T-V3-4A`) and `v3/c2_signal_sim.py` (`T-V3-P4-C2A`) — reuse; do not import/mutate engine state.
- Current ranks/scores to overlay against: `apps/wired/v7/runs/POST_T_V3_3D/results.json`.
- Consumer rules + neighbour sets: `labs/comlab/registry/rules/exhaust_leak.json`, `lean_condition.json`, `sensor_fault.json` (`base_weight`, evidence, `competition_group`, `passes_cases`). Query only.
- Reveal-contract template: `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md`.

### Consumer (signal/noise) ###
- **Consumer:** the owner's go/no-go on `T-V3-P4-C4B`, its exact producer/consumer scope, and the
  add-column decision; the FT-8 gate. This task adds **no** live field/state — it *simulates*.

### Deliverables ###
1. `v3/reports/V3_C4_SIGNAL_DRYRUN_<date>.md` — CREATE. Per-case producer/consumer sim + verdict + column-add gate.
2. `v3/reports/V3_C4_SIGNAL_DRYRUN_<date>.json` — CREATE.
3. `v3/c4_signal_sim.py` — CREATE, read-only overlay simulator (zero-overlay self-check + per-case ΔSTFT producer + EL/LC/SF consumer rank recompute). No engine/lab import-mutation.

### Files to touch ###
- `v3/reports/V3_C4_SIGNAL_DRYRUN_<date>.md` (CREATE)
- `v3/reports/V3_C4_SIGNAL_DRYRUN_<date>.json` (CREATE)
- `v3/c4_signal_sim.py` (CREATE, read-only)

### Out of scope ###
**No corpus column committed to the live CSV** (incl. the C4-distinct dilution/bias columns — that is
`C4B`). **No GASLab/OBDLab producer edit. No registry rule edit. No re-score that mutates a run. No
yardstick mint. No new synthesized values** (consume the C4-SYNTH seed only; ungrounded → abstain).
No abstain-dial change (MARGIN=0.02). Writes only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no
`graphify`/frozen-graph rebuild; a fresh offline index for querying is fine. No secrets.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/c4_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/c4_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/c4_signal_sim.py
# zero-overlay self-check reproduces current ranks for all 294 (no drift):
/agent_workspace/.venv-wired/bin/python v3/c4_signal_sim.py --self-check
# simulate on the C4 synthetic seed:
/agent_workspace/.venv-wired/bin/python v3/c4_signal_sim.py --c4-seed v3/data/c4_synthetic_seed_2026-07-01.json --write v3/reports/V3_C4_SIGNAL_DRYRUN_<date>.json
```
Gate: self-check drift == 0; all 11 C4 case_ids present with a verdict
(WOULD_BANK / STILL_SHORT / ABSTAIN_NO_DATA); the 7/3/1 oracle groups broken out; every STILL_SHORT
case needing a non-corpus column named; every predicted FT-8 regression named; the C4B commit scope
(producer threshold + consumer change + which new column, if any) stated from the sim. `git status`
shows only new files under `v3/`.

### Progress hook ###
PROGRESS.md `T-V3-P4-C4A`: Status=done, Files changed=3 (all new under v3/), Verification="C4 ΔSTFT
signal dry-run on synthetic seed (anecdotal bands): of 11 -> W would-bank / S still-short / A
abstain; 7-leak/3-lean/1-bias broken out; column-add gate named the cases needing downstream-O2/
propane; producer/consumer simulated read-only; FT-8 regressions named; C4B scope sized;
zero-overlay self-check drift=0; no engine/lab/registry/corpus/yardstick touched".

### Depends on ###
`T-V3-P4-C4-SYNTH` done (C4 seed exists). Reveal-contract template done. Runnable once the seed lands.
**Blocked on `T-V3-P4-C4-SYNTH`.** Unblocks `T-V3-P4-C4B` (commit), which is gated on this + owner
sign-off + FT-8 clean + the add-column decision.
