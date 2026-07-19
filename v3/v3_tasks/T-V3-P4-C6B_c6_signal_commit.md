### Goal ###
Commit the C6 **signal pack** (sensor fault under-detection). Write the **7-column set** (Mode $06
margin + the 6 MAF/airflow columns; **O2-timing columns DROPPED** — zero yield on the seed) into the
live corpus for the 14 C6 cases, wire `SensorDynamicsState` + the SF/NF consumer gating (with the C3
precedence rule) into the shim, verify `top3_family` rises to **241/294** with **0 regressions and 0
no_fault-neighbour regressions**, and mint **`V3_YARDSTICK_2026-07-05-C6B`**.
### MANDATORY PRE-FLIGHT — simulate the exact committed config first ###
C6A simulated S1 (margin only, 12) and S3 (full 9 columns, 13); the committed config (margin+MAF,
**no timing**) was not run as its own scenario. Before touching any live file: add that scenario to
`v3/c6_signal_sim.py` and run it. Expected: **13 WOULD_BANK, identical case set to S3, 0 regressions,
0 no_fault regressions**. If it deviates, STOP and surface — do not wire an unsimulated config.
(This is the "nothing unsimulated ships" rule, kept cheap.)
### Progressive-disclosure role — the COMMIT step (ships ONLY the pre-flighted config) ###
1. **Column pricing applied (C6A §6):** Mode $06 margin carries the 12 O2-lazy rows; the 6 MAF
   columns are load-bearing only for `EXP-N020` but are **committed anyway** because they are the
   shared C5/C4 schema (acq-spec §C4/§C6) — landing them here de-risks the next two packs.
   `o2_rich_to_lean_ms`/`o2_lean_to_rich_ms` are deferred (re-openable via the A9 scope fallback if
   real vehicles prove margin-insufficient).
2. **Boost/prune as simulated:** SF-005/SF-008/SF-001/SF-002 +0.10 on decisive dynamic evidence;
   NF-001/NF-002 pruned only on the same; abstain state is a no-op.
3. **C3 precedence implemented where C6A pinned it:** `integration_shim.py::_score_rule`, after the
   live C3 branch (C3's SF prune wins unless decisive dynamic C6 evidence), populations asserted
   disjoint.
4. **Dial untouched:** 5 of the 13 flips stay masked at MARGIN=0.02 (covered/masked 8/5) — noted for
   the parked abstain-cal thread, not this diff.
### Data gate (provisional synthetic seed) ###
Consumes `v3/data/c6_synthetic_seed_2026-07-05.{csv,json}` (`synthetic=true`). `PDF-4G-05`'s
honest-healthy values are written too and must keep emitting no C6 fault state. Non-C6 rows (280)
stay empty (None). Timing columns are NOT written anywhere.
### Success criteria ###
1. **Pre-flight recorded:** committed-config sim result (13 banked, set == S3, 0/0 regressions)
   appended to `V3_C6_SIGNAL_DRYRUN_2026-07-05.{md,json}` as scenario `S-COMMIT`.
2. **Corpus updated:** `cases_petrol_v7.csv` gains 7 columns (`mode06_o2_response_margin_pct`,
   `maf_actual_calc_delta_pct_idle`, `maf_actual_calc_delta_pct_2500`, `maf_gps_idle`, `maf_gps_2500`,
   `calc_airflow_gps_idle`, `calc_airflow_gps_2500`), populated for the 14 C6 cases from the seed;
   `EXP-N020`-style None handling preserved; all other rows empty.
3. **Schemas & ingestion:** fields added to the OBD payload model + mapped through
   `wired/composition.py` and `v7/load_corpus.py` (mirror the C3B diff; `# consumer:` comment on
   every mapped field).
4. **Producer & consumer in the shim:** `SensorDynamicsState` with the pre-flighted gates —
   O2_LAZY_OR_BIASED: `mode06_o2_response_margin_pct <= 10`; MAF_UNDERREAD: MAF delta `<= -15` at
   BOTH points (None → gate not applicable); neither → no decisive state. Boost/prune per §2 above;
   C3 precedence per §3. **No registry JSON edits.**
5. **Rescore & verification:** `top3_family` **241/294 (81.97%)**; `diff` vs `POST_T_V3_P4_C3B`
   shows **13 newly_pass / 0 newly_fail / REGRESSIONS: (empty)**; coverage/abstained match the
   pre-flight numbers (assert equality; surface any delta like C3B's honest 209-vs-210).
6. **Yardstick minted:** `V3_YARDSTICK_2026-07-05-C6B` bound in `score_v3_yardstick.py` (new csv
   hash; oracle `3088a7c3…` unchanged; `run_suite.py` untouched); record at
   `v3/reports/V3_YARDSTICK_2026-07-05-C6B.md`; `Hash lock: ok`, priors immutable.
7. **Inner loop + tests:** `py_compile`+`ruff`+`pyright` clean; `pytest apps/wired/v7/tests/` green,
   including NEW shim tests: each emit path, the None-MAF path, `PDF-4G-05`-style healthy row emits
   nothing, C3-precedence (synthetic both-states row → C3 prune wins), and no-C6-columns row leaves
   NF scoring untouched.
### Context ###
- Sizing: `v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.{md,json}` §2/§6 (gates, deltas, precedence point).
- Contract: `V3_C6_REVEAL_CONTRACT_2026-07-05.{md,json}` §3 (consumer map) + §4 (precedence rule).
- Wiring pattern (READ-NARROW): the C3B diff across `integration_shim.py` / `ingestion.py` /
  `composition.py` / `load_corpus.py`, and `v3/reports/V3_YARDSTICK_2026-07-05-C3B.md` (mint format).
- Baseline: `POST_T_V3_P4_C3B` / `V3_YARDSTICK_2026-07-05-C3B` (csv `9f530695…`). **If anything
  committed after C6A, STOP and re-run the pre-flight on the new baseline.**
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** `SensorDynamicsState` is read by the SF-005/008/001/002 boost + NF-001/002 prune
  branch this task adds, under the C3-precedence guard.
- **Code path:** `labs/comlab/registry/integration_shim.py::_score_rule` (after the C3 branch), fed
  by the 7 columns via `load_corpus.py` → `composition.py` → `ingestion.py`. The 6 MAF columns
  additionally have **named future consumers** (C5 `LeanRootCauseState`, C4 ΔSTFT discriminator —
  acq-spec §C4/§C5); their live consumer TODAY is the MAF_UNDERREAD gate — not orphans.
### Deliverables ###
1. `v3/c6_signal_sim.py` + dry-run report — MODIFY. Add + record scenario `S-COMMIT` (pre-flight).
2. `apps/wired/v7/data/cases_petrol_v7.csv` — MODIFY. 7 C6 columns, 14 cases filled.
3. `labs/comlab/comlab/schemas/ingestion.py` / `apps/wired/wired/composition.py` /
   `apps/wired/v7/load_corpus.py` — MODIFY. Field mapping chain.
4. `labs/comlab/registry/integration_shim.py` — MODIFY. State emit + SF/NF gating + C3 precedence.
5. `apps/wired/fl_tasks/score_v3_yardstick.py` + `v3/reports/V3_YARDSTICK_2026-07-05-C6B.md` —
   MODIFY/CREATE. Mint + rebind.
6. `apps/wired/v7/tests/` — ADD shim tests (emit paths, None-MAF, healthy, precedence, NF-untouched).
### Files to touch ###
The set above plus `v3/v3_tasks/progress_notes/T-V3-P4-C6B.md` (CREATE).
### Out of scope ###
**No O2-timing columns** (deferred, A9 fallback). **No stronger lift** if a case falls short live —
disclose, don't tune. **No registry JSON edits. No abstain-dial change (MARGIN=0.02). No
oracle/`run_suite.py` edit. No C3 gate/threshold change** (precedence guard only). `PDF-4G-05` must
not be nudged toward a sensor pass. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph
rebuild. Run JSON untracked. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python v3/c6_signal_sim.py --scenario s_commit   # PRE-FLIGHT first: 13 banked, 0/0 regressions
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py
/agent_workspace/.venv-wired/bin/python -m pytest apps/wired/v7/tests/
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json
```
Gate: pre-flight matches (13, set==S3, 0/0); `top3_family = 241/294`; `Hash lock: ok` (on
`V3_YARDSTICK_2026-07-05-C6B`); `13 newly_pass / 0 newly_fail`; `REGRESSIONS: (empty)` incl. 0
no_fault neighbours; coverage matches pre-flight (delta surfaced if not).
### Progress hook ###
PROGRESS.md `T-V3-P4-C6B`: Status=done, Files changed=~9, Verification="C6 commit: 7 columns (Mode$06
+ shared MAF; timing dropped) + SensorDynamicsState + SF boost/NF prune under C3 precedence;
pre-flight matched; top3_family 228→241 (+13); 0 regressions (0 no_fault);
V3_YARDSTICK_2026-07-05-C6B minted".
### Depends on ###
`T-V3-P4-C6A` done ✓ (sized this commit; FT-8 clean ✓ incl. NF breakout). Owner go given. **Unblocks
the C5 pack** (next in the pinned sequence — and its `LeanRootCauseState` now inherits the live MAF
columns) and the C4B re-baseline path.
