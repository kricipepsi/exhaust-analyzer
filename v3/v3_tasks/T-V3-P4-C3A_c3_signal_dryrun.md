### Goal ###
C3 signal pack, DISCLOSE half. Simulate — **read-only, in memory** — the C3
`ControlPlausibilityState` producer and its EF/SF consumers over the `T-V3-P4-C3-SYNTH` seed,
against the pinned `POST_T_V3_P4_C2B` baseline. Predict exactly which of the 22 C3 cases flip into
top-3 (`WOULD_BANK`), which stay short, and whether any of the 48 FT-8 neighbours regresses. **No
live lab/registry/corpus edit, no yardstick mint.** Sizes the commit `T-V3-P4-C3B`.
### Progressive-disclosure role — the DISCLOSE step ###
The seed says 18/22 are C3-separable on paper; whether those values, run through the concrete
producer gates + consumer overlay, actually move ranks without breaking the 48-case neighbour union
(18 of which are BOTH C3 targets and regression-sensitive neighbours — the largest dual set of any
pack yet) is only knowable by simulating. This task discloses yield + regression risk; C3B commits
only behind it + owner sign-off.
### Data gate (provisional synthetic seed) ###
Runs on `v3/data/c3_synthetic_seed_2026-07-05.{csv,json}` (`synthetic=true`; 18 separable + 4
`stay_abstained` honestly seeded below every gate). Report all flips as **synthetic-driven** (keep
the synthetic-vs-real split). Real owner data, when it lands, replaces the seed (same simulator).
The 22 cases and per-case bands: seed manifest + `V3_C3_REVEAL_CONTRACT_2026-07-05.json`.
### Success criteria ###
Produce `v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.{md,json}` with the 5 reveal-contract sections:
1. **Producer simulation:** per case, the emitted state from the contract §2 gates —
   lean-bias: `dlc_signal_ground_drop_v > 0.20` AND `gas_obd_lambda_delta >= 0.05`;
   rich-bias: `koeo_map_baro_delta_kpa >= 5` AND `gas_obd_lambda_delta >= 0.05`;
   processor: `bidirectional_fuel_response_ok_bool == False` AND `module_voltage_loaded_v < 12.0`.
   Any gate met → `CONTROL_REFERENCE_FAULT` (record which sub-gate); none → `ABSTAIN`.
2. **Scenario ladder (acquisition-cost disclosure):** Scenario 1 = Tier-A/C electrical-only gates
   (KOEO + ground drop + Vmod + bidirectional; **no Δλ** — drops the two-point 5-gas ask);
   Scenario 2 = full contract gates incl. `gas_obd_lambda_delta`. Per scenario: yield + which cases
   differ — this prices whether the owner needs action A6_TWO_POINT_5GAS or A5-electrical alone.
3. **Consumer simulation:** overlay the state onto EF-001/EF-002/EF-003 (+ SF-001/SF-002 only per
   the contract §3 dispersion-as-sensor-bias mapping) and recompute family ranks read-only. Boost
   mechanics mirror `v3/c2_signal_sim.py`/`c4_signal_sim.py` (matching state → DEFINITIVE boost,
   non-matching pruned) — reuse that overlay pattern, adapted to the EF/SF rule files.
4. **Yield disclosure:** 22 → `WOULD_BANK` / `ALREADY_PASS` / `STILL_SHORT` (say why per case) /
   `ABSTAIN_NO_DATA`; the 4 `stay_abstained` seed cases MUST land outside `WOULD_BANK` — if one
   banks, that is a back-solve alarm, surface it loudly.
5. **FT-8 neighbour audit:** re-derive the neighbour union live (expect ≈48 from `ecu_fault.json` +
   `sensor_fault.json` `passes_cases`); full-294 sim; regressions must be listed (target: empty).
   Name the 18 dual target+neighbour cases' outcomes explicitly.
6. **Commit scope for C3B, sized not guessed:** exact producer thresholds, consumer changes, and
   which of the 6 columns the corpus needs (is Δλ load-bearing per Scenario 1 vs 2?).
- **Zero-overlay self-check first:** no-overlay sim reproduces `POST_T_V3_P4_C2B/results.json`
  exactly (drift=0) for all 294 before any C3 case is simulated.
- Inner loop clean (`py_compile`+`ruff`+`pyright`); `top3_family` 212/294 and yardstick untouched.
### Context ###
- Contract (gates, consumers, FT-8, baseline pin): `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.{md,json}`.
- Seed: `v3/data/c3_synthetic_seed_2026-07-05.{csv,json}` + `V3_C3_SYNTH_BANDS_2026-07-05.md`.
- Simulator patterns to mirror (READ-NARROW, adapt don't fork blindly): `v3/c2_signal_sim.py`,
  `v3/c4_signal_sim.py` (overlay + self-check + FT-8 audit structure).
- Baseline: `apps/wired/v7/runs/POST_T_V3_P4_C2B/results.json`; ruler `V3_YARDSTICK_2026-07-05`
  (csv `3df2e8cb…`, oracle `3088a7c3…`). If any commit has landed since, STOP and re-pin (the C4A
  stale-baseline lesson).
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** the owner (C3B go/no-go + column-set decision) and `T-V3-P4-C3B` (commit sizing).
  No live field/state added — the producer/consumer exist only inside the sim overlay.
### Disclosure ###
Surface, don't hide: any stay-abstained case that banks (back-solve alarm); any neighbour regression
(especially the 18 dual cases); Scenario-1-vs-2 differences (the Δλ ask is the expensive one and
empirical-anecdotal — if Scenario 1 alone banks the 18, say so); cases whose bank depends on the
weakest-grounded threshold. Tier essential-first: headline yield → scenario table → per-case JSON.
### Deliverables ###
1. `v3/c3_signal_sim.py` — CREATE. Read-only simulator (overlay + zero-overlay self-check + FT-8).
2. `v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.md` — CREATE. 5-section reveal-contract report.
3. `v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.json` — CREATE. Per-case/per-scenario detail.
### Files to touch ###
- `v3/c3_signal_sim.py` (CREATE)
- `v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.md` (CREATE)
- `v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.json` (CREATE)
### Out of scope ###
**No live edit anywhere:** no corpus column, no rule/weight/registry change, no engine/lab code, no
re-score of the live yardstick, no mint. No seed regeneration (consume `c3_synthetic_seed_2026-07-05`
as-is; if a seed value looks wrong, surface it, don't fix it here). No abstain-dial change
(MARGIN=0.02). Writes only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph
rebuild. `run_suite.py` untouched. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/c3_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/c3_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/c3_signal_sim.py
/agent_workspace/.venv-wired/bin/python v3/c3_signal_sim.py            # runs self-check then scenarios
grep -cE 'WOULD_BANK|STILL_SHORT|stay_abstained|Scenario|drift|regression' v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.md
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score   # unchanged: 212/294, Hash lock: ok
git status --porcelain   # only new files under v3/
```
Gate: zero-overlay drift=0 over 294; per-case table reconciles to 22; 4 stay-abstained cases outside
WOULD_BANK; FT-8 audit over the live-derived union with regressions listed (target empty); both
scenarios reported; live state untouched.
### Progress hook ###
PROGRESS.md `T-V3-P4-C3A`: Status=done, Files changed=3 (new under v3/), Verification="C3 dry-run on
synthetic seed: <n> would-bank / <n> still-short / 4 stay-abstained honoured; Scenario 1 vs 2 yield
<x>/<y>; 0 regressions on <k> neighbours; drift=0; no live state mutated".
### Depends on ###
`T-V3-P4-C3-SYNTH` done (seed). **Unblocks `T-V3-P4-C3B`** (commit — authored in full only after
this disclosure + owner sign-off + FT-8 clean).
