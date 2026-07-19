### Goal ###
Commit the C5 **signal pack** (lean-condition root cause). Write the 11-column C5 set into the live
corpus for the 10 C5 cases (5 NEW schema columns + values into the 6 already-live C2B/C6B columns),
wire `LeanRootCauseState` + the LC/VL consumer boost (NO NF prune — stripped at C5R) with the C3
precedence and C6-MAF-collision rules into the shim, verify `top3_family` rises to **246/294** with
**0 regressions**, and mint **`V3_YARDSTICK_2026-07-06-C5B`**.
### MANDATORY PRE-FLIGHT — re-run the exact committed config first ###
Before touching any live file: `v3/c5_signal_sim.py --scenario s_commit` on the current baseline.
Expected: **5 WOULD_BANK (`EXP-N011, EXP-N022, EXP-N029, case_003, case_016`), era3_015
ALREADY_PASS, 4 EGR STILL_SHORT, 0 regressions (68-union FT-8 clean), covered 211→207,
on-covered 177→176.** If it deviates, STOP and surface — nothing unsimulated ships.
### Progressive-disclosure role — the COMMIT step (ships ONLY the pre-flighted config) ###
1. **Column pricing applied (C5A ladder):** trims-only already banks all 5, but ALL 11 columns
   commit anyway — the load-trim/WOT/pressure columns are the shared C4 schema (acq-spec §C4:
   C4 residuals consume C5 trim/load columns; landing them here de-risks C4B), and the full set is
   the contract. State this pricing in the progress note.
2. **Boost as simulated at C5R:** LC-001/002/003 + VL-001/002/003 **+0.10 on decisive C5 state
   only**. **NO NF-001/NF-002 prune** (uncontracted — audit Deviation 5). Abstain state is a no-op.
3. **Precedence implemented where the contract pinned it** — `integration_shim.py::_score_rule`
   AFTER the C3 and C6 branches: (a) C3 `CONTROL_REFERENCE_FAULT` prunes first; static-only C5
   evidence never overrides. (b) C6-MAF collision: C6 sensor attribution requires its Mode $06 /
   dynamics evidence; C5 requires the trim+load pattern; **neither fires on MAF delta alone; C5
   takes precedence when both are decisive.** Populations asserted disjoint today.
4. **Dial untouched + FULL scoreboard disclosure (audit Blocker 3):** all 5 banked cases remain
   ABSTAINED at MARGIN=0.02; coverage falls 71.8%→70.4% (4 newly abstained incl. era3_015, which
   leaves covered-as-passing); on-covered rises 83.89%→85.02%. This picture goes verbatim in the
   progress note and yardstick record — the owner signs off on it, not on "+5" alone.
### Data gate (provisional synthetic seed) ###
Consumes `v3/data/c5_synthetic_seed_2026-07-06.{csv,json}` (`synthetic=true`, post-C5R). The 4 EGR
rows' honest healthy/normal values are written too and must keep emitting **no decisive C5 state**
(mirror C6B's PDF-4G-05 handling). **Q-C5-EGR is HELD (DECISIONS.md):** do not nudge EGR rows, do
not edit the dtclab wiki, do not re-rule the conflict here. None columns stay None (EXP-N022 +
era1_001 rail pressure). Non-C5 rows (284) stay empty on the 5 new columns.
### Success criteria ###
1. **Pre-flight recorded:** s_commit re-run appended to `V3_C5_SIGNAL_DRYRUN_2026-07-06.{md,json}`
   with the expected numbers above.
2. **Corpus updated:** `cases_petrol_v7.csv` gains 5 columns (`stft_load_pct, ltft_load_pct,
   calc_load_wot_pct, fuel_rail_pressure_load_kpa, wideband_lambda_wot`), 10 C5 rows populated
   across all 11 contract columns from the seed; None handling preserved; all other rows empty.
3. **Schemas & ingestion:** fields added to the OBD payload model + mapped through
   `wired/composition.py` and `v7/load_corpus.py` (mirror the C6B diff; `# consumer:` comment on
   every mapped field).
4. **Producer & consumer in the shim:** `LeanRootCauseState` with the pre-flighted gates —
   VACUUM_LEAK_TRIM_PATTERN: idle TFT >= 15 AND 2500 TFT <= 10 AND recovery delta >= 15;
   FUEL_DELIVERY_SHORTFALL: rail drop > 35 kPa below spec AND WOT lambda > 1.05;
   MAF_UNDERREAD: WOT calc load < 80 AND positive trims (None → gate not applicable);
   none/static-only → `SENSOR_HEALTH_UNPROVEN_ABSTAIN` (no-op). Boost per §2; precedence per §3.
   **No registry JSON edits.**
5. **Rescore & verification:** `top3_family` **246/294 (83.67%)**; `diff` vs `POST_T_V3_P4_C6B`
   shows **5 newly_pass / 0 newly_fail / REGRESSIONS: (empty)**; coverage/abstained match the
   pre-flight numbers (assert equality; surface any delta honestly).
6. **Yardstick minted:** `V3_YARDSTICK_2026-07-06-C5B` bound in `score_v3_yardstick.py` (new csv
   hash; oracle `3088a7c3…` unchanged; `run_suite.py` untouched); record at
   `v3/reports/V3_YARDSTICK_2026-07-06-C5B.md` **including the §4 disclosure picture**;
   `Hash lock: ok`.
7. **Inner loop + tests:** `py_compile`+`ruff`+`pyright` clean; `pytest apps/wired/v7/tests/` green,
   including NEW shim tests: each emit path; static-only/idle-only row → abstain no-op; None-column
   paths (rail-pressure None, MAF None); EGR healthy row emits nothing; C3-precedence (synthetic
   both-states row → C3 prune wins); C6-collision (MAF delta alone fires neither; both decisive →
   C5 wins); no-C5-columns row leaves scoring untouched.
### Context ###
- Sizing: `v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.{md,json}` (post-C5R) — gates, ladder, FT-8 68.
- Contract: `V3_C5_REVEAL_CONTRACT_2026-07-05.{md,json}` §2 producer / §3 consumer map / §4
  collision + C3 rule / §10 abstain.
- Audit + open item: `progress_notes/AUDIT_C5-SYNTH_C5A_2026-07-06.md` (§OPEN CONFLICT Q-C5-EGR).
- Wiring pattern (READ-NARROW): the C6B diff across `integration_shim.py` / `ingestion.py` /
  `composition.py` / `load_corpus.py`, and `v3/reports/V3_YARDSTICK_2026-07-05-C6B.md` (mint format).
- Wiki-first: domain facts live in `labs/<lab>/{wiki,docs}` (mirror `Vault/labs/…`, read-only) —
  e.g. dtclab `03_fuel_trim_grammar.md`. Web via firecrawl only for what the repo lacks
  (`firecrawl --status` must say Authenticated — key auto-exported by run-*.sh).
- Baseline: `POST_T_V3_P4_C6B` / `V3_YARDSTICK_2026-07-05-C6B` (csv `bf739368…`). **If anything
  committed after C5R, STOP and re-run the pre-flight on the new baseline.**
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** `LeanRootCauseState` is read by the LC/VL +0.10 branch this task adds, under the
  C3-precedence and C6-collision guards.
- **Code path:** `labs/comlab/registry/integration_shim.py::_score_rule` (after the C3 and C6
  branches), fed by the 11 columns via `load_corpus.py` → `composition.py` → `ingestion.py`. The 5
  new columns have **named future consumers** (C4 ΔSTFT discriminator — acq-spec §C4); their live
  consumer TODAY is this producer — not orphans.
### Deliverables ###
1. `v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.{md,json}` — MODIFY. Record pre-flight re-run.
2. `apps/wired/v7/data/cases_petrol_v7.csv` — MODIFY. 5 new columns; 10 C5 rows × 11 columns filled.
3. `labs/comlab/comlab/schemas/ingestion.py` / `apps/wired/wired/composition.py` /
   `apps/wired/v7/load_corpus.py` — MODIFY. Field mapping chain.
4. `labs/comlab/registry/integration_shim.py` — MODIFY. State emit + LC/VL boost + both guards.
5. `apps/wired/fl_tasks/score_v3_yardstick.py` + `v3/reports/V3_YARDSTICK_2026-07-06-C5B.md` —
   MODIFY/CREATE. Mint + rebind.
6. `apps/wired/v7/tests/` — ADD shim tests per Success 7.
### Files to touch ###
The set above plus `v3/v3_tasks/progress_notes/T-V3-P4-C5B.md` (CREATE).
### Out of scope ###
**No NF prune. No stronger lift** if a case falls short live — disclose, don't tune. **No EGR
nudging / no wiki edit / no Q-C5-EGR re-ruling. No registry JSON edits. No abstain-dial change
(MARGIN=0.02). No oracle/`run_suite.py` edit. No C3 or C6 gate/threshold change** (guards only).
One task, one session. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph rebuild. Run
JSON untracked. No secrets. No task authoring (architect lane).
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python v3/c5_signal_sim.py --scenario s_commit   # PRE-FLIGHT first: +5, 0/0, covered 207
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m pytest apps/wired/v7/tests/
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json
```
Gate: pre-flight matches; `top3_family = 246/294`; `Hash lock: ok` (on `V3_YARDSTICK_2026-07-06-C5B`);
`5 newly_pass / 0 newly_fail`; `REGRESSIONS: (empty)`; coverage 207 matches pre-flight (delta
surfaced if not); EGR rows emit no decisive state; full §4 disclosure present in note + mint record.
### Progress hook ###
PROGRESS note `T-V3-P4-C5B`: Status=done, Files changed=~9, Verification="C5 commit: 5 new columns +
6 shared populated + LeanRootCauseState + LC/VL boost under C3-precedence + C6-collision guards;
pre-flight matched; top3_family 241→246 (+5, all 5 still abstained; covered 211→207, on-covered
85.02%); 0 regressions; Q-C5-EGR held; V3_YARDSTICK_2026-07-06-C5B minted".
### Depends on ###
`T-V3-P4-C5R` done ✓ (audited; Fix-2 provisional — does not gate this diff). Owner go given
2026-07-06. **Unblocks the C4 pack** (C4B consumes the C5 trim/load + C6 dynamics columns — next in
the pinned sequence C2 ✓ C3 ✓ C6 ✓ C5 → **C4** → C9 → C8 → C1 → C7).
