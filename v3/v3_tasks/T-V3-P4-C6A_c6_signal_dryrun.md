### Goal ###
C6 signal pack, DISCLOSE half. Simulate — **read-only, in memory** — the C6 `SensorDynamicsState`
producer and its SF/NF consumers over the `T-V3-P4-C6-SYNTH` seed, against the pinned
`POST_T_V3_P4_C3B` baseline. Predict which of the 14 C6 cases flip into top-3, whether any of the
33 FT-8 neighbours regresses (**watch the NF healthy cases — costliest regression kind**), and which
of the 9 columns are actually load-bearing. **No live edit, no yardstick mint.** Sizes `T-V3-P4-C6B`.
### Progressive-disclosure role — the DISCLOSE step ###
The seed says 13/14 are C6-separable on paper (12 O2_LAZY_OR_BIASED + 1 MAF_UNDERREAD). Whether
those values, run through the contract gates + consumer overlay, move ranks without breaking
neighbours — and without the C3-interaction misfiring — is only knowable by simulating. Note from
C3A: paper-separable can exceed actual flips (the +boost may not out-rank competitors); count on it
here too, since 6 of the 14 currently WIN as no_fault and must be out-ranked by sensor_fault.
### Data gate (provisional synthetic seed) ###
Runs on `v3/data/c6_synthetic_seed_2026-07-05.{csv,json}` (`synthetic=true`; 13 separable + 1
stay-abstained `PDF-4G-05` seeded below every gate). Report flips as **synthetic-driven**. Real owner
data replaces the seed later (same simulator).
### Success criteria ###
Produce `v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.{md,json}` with the 5 reveal-contract sections:
1. **Producer simulation:** per case, the emitted state per contract §2 —
   `O2_LAZY_OR_BIASED`: Mode $06 margin at/over the vehicle-relative limit OR response times beyond
   the seeded band; `MAF_UNDERREAD`: sustained shortfall >10–15% at BOTH idle and 2500 (respect
   None MAF columns → gate not applicable); neither → `SENSOR_HEALTH_UNPROVEN_ABSTAIN`. Record the
   sub-gate fired.
2. **Column-subset scenario ladder (the C3A lesson, applied to 9 columns):**
   Scenario 1 = Mode $06 margin only (cheapest — one Tier-a scan read);
   Scenario 2 = + O2 response times (adds the active maneuver);
   Scenario 3 = full contract (+ the 6 MAF/airflow columns).
   Per scenario: yield + which cases differ. This prices C6B's column set — if S1/S2 bank the same
   set as S3, the MAF columns may reduce to the 1 MAF_UNDERREAD case or drop entirely.
3. **Consumer simulation with C3 precedence:** on `O2_LAZY_OR_BIASED`/`MAF_UNDERREAD`: boost
   SF-005/SF-008 (+ SF-001/SF-002 per the contract §3 bias path); on the abstain state: no boost; and
   NF-001/NF-002 must LOSE support only where dynamic evidence contradicts healthy (contract §3).
   **Implement the contract §4 precedence rule in the overlay:** C3's `CONTROL_REFERENCE_FAULT`
   prune of SF-001/002 wins unless decisive dynamic C6 evidence exists — populations are disjoint
   today, assert that in-sim (no case carries both states; if one does, surface it loudly).
4. **Yield disclosure:** 14 → `WOULD_BANK` / `ALREADY_PASS` / `STILL_SHORT` (why, per case — name the
   no_fault-winner cases specifically) / `ABSTAIN_NO_DATA`; `PDF-4G-05` MUST land outside
   `WOULD_BANK` (bank = back-solve alarm). Covered-vs-masked split at MARGIN=0.02 disclosed.
5. **FT-8 neighbour audit:** re-derive the union live from `sensor_fault.json` + `no_fault.json`
   `passes_cases` (expect ≈33, 9 dual); full-294 sim; regressions listed (target empty). **Break out
   the currently-passing no_fault neighbours separately** — a healthy case regressed to a fault
   verdict is the failure mode this pack must not ship.
6. **Commit scope for C6B, sized not guessed:** exact gates, boost/prune deltas, the column set
   (from the scenario ladder), and the C3-precedence implementation point in
   `integration_shim.py::_score_rule`.
- **Zero-overlay self-check first:** drift=0 vs `POST_T_V3_P4_C3B/results.json` across 294.
- Inner loop clean; `top3_family` 228/294 and yardstick untouched.
### Context ###
- Contract: `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.{md,json}` (§2 gates, §3 consumers, §4
  C3-precedence, §6 FT-8).
- Seed: `v3/data/c6_synthetic_seed_2026-07-05.{csv,json}` + `V3_C6_SYNTH_BANDS_2026-07-05.md`
  (per-case bands, σ table, emit-path split).
- Simulator pattern (READ-NARROW, adapt): `v3/c3_signal_sim.py` (overlay + self-check + FT-8 +
  scenario ladder). The C6 overlay adds the NF-support and C3-precedence mechanics — new logic,
  test it in-sim with the zero-overlay check plus a no-C6-columns case asserting NF unaffected.
- Baseline: `apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json`; ruler `V3_YARDSTICK_2026-07-05-C3B`
  (csv `9f530695…`, oracle `3088a7c3…`). **If anything committed since C6-SYNTH, STOP and re-pin.**
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** the owner (C6B go/no-go + column-set decision) and `T-V3-P4-C6B` (commit sizing).
  No live field/state added — producer/consumer exist only inside the sim overlay.
### Disclosure ###
Surface, don't hide: PDF-4G-05 banking (back-solve alarm); ANY no_fault neighbour regression (list
even one); paper-13 vs actual flips; scenario-ladder differences (which columns earn their place);
cases whose bank rides on the weakest-grounded gate (MAF empirical-inferred); covered-vs-masked at
MARGIN=0.02. Tier essential-first: headline yield → scenario table → per-case JSON.
### Deliverables ###
1. `v3/c6_signal_sim.py` — CREATE. Read-only simulator (overlay + self-check + FT-8 + ladder + precedence).
2. `v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.md` — CREATE. 5-section reveal-contract report.
3. `v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.json` — CREATE. Per-case/per-scenario detail.
### Files to touch ###
- `v3/c6_signal_sim.py` (CREATE)
- `v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.md` (CREATE)
- `v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.json` (CREATE)
### Out of scope ###
**No live edit anywhere** (corpus, rules, registry, shim, engine, scorer, yardstick). No seed
regeneration (surface suspect values, don't fix). No abstain-dial change (MARGIN=0.02). No stronger
lift beyond the contract's boost values (if the boost proves insufficient, DISCLOSE it — sizing a
bigger one is a C6B/owner decision). Writes only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no
`graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/c6_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/c6_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/c6_signal_sim.py
/agent_workspace/.venv-wired/bin/python v3/c6_signal_sim.py            # self-check → scenarios
grep -cE 'WOULD_BANK|STILL_SHORT|PDF-4G-05|no_fault|Scenario|drift|regression|precedence' v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.md
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score   # unchanged: 228/294, Hash lock: ok
git status --porcelain   # only new files under v3/
```
Gate: drift=0 over 294; per-case table reconciles to 14; PDF-4G-05 outside WOULD_BANK; no-dual-state
assertion holds; FT-8 over the live union with NF neighbours broken out and regressions listed
(target empty); all 3 scenarios reported; live state untouched.
### Progress hook ###
PROGRESS.md `T-V3-P4-C6A`: Status=done, Files changed=3 (new under v3/), Verification="C6 dry-run:
<n> would-bank / <n> still-short / PDF-4G-05 honoured; Scenario 1/2/3 yield <a>/<b>/<c>; 0
regressions on <k> neighbours (0 no_fault); drift=0; no live state mutated".
### Depends on ###
`T-V3-P4-C6-SYNTH` done ✓. **Unblocks `T-V3-P4-C6B`** (commit — authored in full only after this
disclosure + owner sign-off + FT-8 clean, incl. the no_fault breakout).
