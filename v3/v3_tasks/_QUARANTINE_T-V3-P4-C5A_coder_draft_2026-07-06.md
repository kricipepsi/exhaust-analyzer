### Goal ###
C5 signal pack, DISCLOSE half. Simulate — **read-only, in memory** — the C5 `LeanRootCauseState`
producer and its LC/VL/EL consumers over the `T-V3-P4-C5-SYNTH` seed, against the pinned
`POST_T_V3_P4_C6B` baseline. Predict which of the 10 C5 cases flip into top-3, whether any of the
68 FT-8 neighbours regresses, and which of the 11 columns are actually load-bearing. **No live edit,
no yardstick mint.** Sizes `T-V3-P4-C5B`.
### Progressive-disclosure role — the DISCLOSE step ###
The seed says 6/10 are C5-separable on paper (all vacuum leaks `ERR-LC-001`). Whether
those values, run through the contract gates + consumer overlay, move ranks without breaking
neighbours — and without C6-collision or C3-interaction misfiring — is only knowable by simulating.
Note from prior dry-runs: paper-separable can exceed actual flips. Count on it here too, since 5
of the 10 currently WIN as misfire or sensor_fault and must be out-ranked by lean_condition.
### Data gate (provisional synthetic seed) ###
Runs on `v3/data/c5_synthetic_seed_2026-07-06.{csv,json}` (`synthetic=true`; 6 separable + 4
stay-abstained seeded below every gate). Report flips as **synthetic-driven**.
### Success criteria ###
Produce `v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.{md,json}` with the 5 reveal-contract sections:
1. **Producer simulation:** per case, the emitted state per contract §2 —
   `VACUUM_LEAK_TRIM_PATTERN`: idle TFT >= 15% and recovery delta >= 15% (2500 TFT <= 10%);
   `FUEL_DELIVERY_SHORTFALL`: rail pressure drop > 35 kPa and WOT lambda > 1.05;
   `MAF_UNDERREAD`: peak WOT load < 80% with positive trims;
   neither → `SENSOR_HEALTH_UNPROVEN_ABSTAIN`. Record the sub-gate fired and None columns with stated reasons.
2. **Column-subset scenario ladder:**
   Scenario 1 = Trims only (stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct);
   Scenario 2 = Trims plus WOT load & lambda (stft_load_pct, ltft_load_pct, calc_load_wot_pct, wideband_lambda_wot);
   Scenario 3 = Full contract (all 11 columns, adding fuel_rail_pressure_load_kpa and MAF idle/2500).
   Per scenario: yield + which cases differ.
3. **Consumer simulation:** on decisive states: boost LC-001/002/003 (+0.10); and enforce:
   C6-MAF-collision guard: if C6 sensor-dynamics columns are absent, ensure C6's state returns
   `SENSOR_HEALTH_UNPROVEN_ABSTAIN`. When both present, C5's lean root cause takes precedence (prunes C6 boost).
   C3-precedence: if `CONTROL_REFERENCE_FAULT` is present, it prunes/boosts first; static-only C5 evidence does not override.
4. **Yield disclosure:** 10 → `WOULD_BANK` / `ALREADY_PASS` / `STILL_SHORT` / `ABSTAIN_NO_DATA`.
   Covered-vs-masked split at MARGIN=0.02.
5. **FT-8 neighbour audit:** re-derive the union live from `lean_condition.json` + `vacuum_leak.json`
   `passes_cases` (68 cases); full-294 sim; regressions listed (target empty). Break out currently-passing neighbours separately.
6. **Commit scope for C5B, sized not guessed:** exact gates, boost/prune deltas, and the column set.
- **Zero-overlay self-check first:** drift=0 vs `POST_T_V3_P4_C6B/results.json` across 294.
- Inner loop clean; `top3_family` 241/294 and yardstick untouched.
### Context ###
- Contract: `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.{md,json}` (§2 gates, §4 collision/interaction, §5 column audit, §7 FT-8, §8 confounders, §10 abstain).
- Seed: `v3/data/c5_synthetic_seed_2026-07-06.{csv,json}` + `V3_C5_SYNTH_BANDS_2026-07-06.md`.
- Simulator pattern (adapt): `v3/c6_signal_sim.py` (overlay + self-check + FT-8 + scenarios).
- Baseline: `apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json`; ruler `V3_YARDSTICK_2026-07-05-C6B`.
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** the owner (C5B go/no-go + column-set decision) and `T-V3-P4-C5B` (commit sizing).
### Disclosure ###
Surface, don't hide: stay-abstained EGR cases; any neighbour regressions; scenario-ladder results; covered-vs-masked split.
### Deliverables ###
1. `v3/c5_signal_sim.py` — CREATE. Read-only simulator.
2. `v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.md` — CREATE.
3. `v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.json` — CREATE.
### Files to touch ###
- `v3/c5_signal_sim.py` (CREATE)
- `v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.md` (CREATE)
- `v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.json` (CREATE)
### Out of scope ###
No live edits anywhere (corpus, rules, registry, shim, engine, scorer, yardstick). Writes only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/c5_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/c5_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/c5_signal_sim.py
/agent_workspace/.venv-wired/bin/python v3/c5_signal_sim.py            # self-check → scenarios
grep -cE 'WOULD_BANK|STILL_SHORT|abstain|Scenario|drift|regression|precedence' v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.md
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score   # unchanged: 241/294
git status --porcelain   # only new files under v3/
```
### Progress hook ###
PROGRESS.md `T-V3-P4-C5A`: Status=done, Files changed=3 (new under v3/), Verification="C5 dry-run: <n> would-bank / <n> still-short / 4 stay-abstained honoured; Scenario 1/2/3 yield <a>/<b>/<c>; 0 regressions on 68 neighbours; drift=0; no live state mutated".
### Depends on ###
`T-V3-P4-C5-SYNTH` done ✓.
