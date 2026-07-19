### Goal ###
Re-pin the **10 ORACLE_SUSPECT** `mechanical_wear → misfire` rows in the oracle so the engine's
single-snapshot misfire answer scores as correct, then **mint a new yardstick** for the changed
oracle. Oracle-data + yardstick-rebind only — **zero engine change**. Banks up to **+10**
`top3_family` (184 → up to 194) and up to +10 single-verdict family+state.

### Progressive-disclosure role — the last research-independent accuracy commit ###
This is the final cheap accuracy lever before the discrimination wall. It's a **commit** (changes the
answer key), sanctioned by `V3_PLAN §5` ("re-pin to misfire for a single-snapshot yardstick") and
backed by Cluster-1 research (mechanical vs misfire). **Owner sign-off: GRANTED (2026-07-01, "do 1").**
After this, remaining gains (HARD, PRODUCER_GAP-signal, DATA_GAP, 12 held TUNABLE) are all Phase-4
signal/owner-data work.

### The exact 10 (do not touch the other 4 mechanical_wear rows) ###
Re-pin **only** these, all routed by the engine to `MF-001` (misfire):
`CSV-118, CSV-119, CSV-120, EXT-222, EXT-223, EXT-224, MECH-002, MECH-006, era1_002, era1_015`.
**Exclude** the 4 non-suspect mechanical_wear rows: `CSV-117`, `EXP-N030`, `MECH-001` (PRODUCER_GAP)
and `case_044` (OUTRANKED) — they are not the "engine says misfire" set and must stay
`mechanical_wear`. (Source: `FL_LOCALIZATION_2026-06-30.md` mode map, ORACLE_SUSPECT=10.)

### Success criteria ###
- In the oracle `apps/wired/v7/data/cases_petrol_v7.csv`, for the 10 rows above, re-pin the expected
  answer from `mechanical_wear` to the engine's misfire read, following the **T-V3-2 Option B
  convention** already applied to SURFACE_DEFECT: `expected_fault_family` → `misfire`;
  `expected_state` → the misfire state the engine emits; `expected_fault_code` → short `MF-001`;
  `expected_confidence*` → the live misfire band. Mirror exactly how `V3_ORACLE_REPIN_2026-06-30.md`
  did the SURFACE_DEFECT rows — same columns, same band source. Do not edit any other row.
- **Mint a new yardstick** (the oracle changed → CSV + oracle-subset SHA move). Follow **T-V3-2R**:
  add a new `V3_YARDSTICK_2026-07-01` name + recompute `ACTIVE_CSV_SHA256` /
  `ACTIVE_ORACLE_SUBSET_SHA256` in `apps/wired/fl_tasks/score_v3_yardstick.py` (not hash-locked);
  keep `FL_YARDSTICK_2026-06-30` and the prior `V3_YARDSTICK_2026-06-30` as historical BEFOREs. Write
  a change-record note like `V3_ORACLE_REPIN_2026-06-30.md`. `run_suite.py` stays untouched
  (hash-locked scorer).
- After re-pin + re-score: `Hash lock: ok` against the **new** yardstick; `top3_family` rises by the
  number of the 10 that now pass (target 184 → 194); single-verdict family+state rises correspondingly
  (target 133 → up to 143) with **no other family regressed** (`diff` REGRESSIONS empty except the 10
  intended flips).
- Inner loop clean on any touched file (`py_compile`, `ruff`, `pyright`); guard/drift test updated to
  the new yardstick (as T-V3-2R did) so the scoreboard refuses on future drift.

### Disclosure (surface, not hide) ###
This re-pin **changes the acceptance answer key** — say so plainly: it is a product-definition call
(single-snapshot misfire is the defensible read; true mechanical_wear needs a Phase-4 mechanical
discriminator), not the engine improving. Record the 10 flipped case_ids, the new yardstick name +
hashes, and confirm exactly 10 rows changed. Any of the 10 that do **not** pass after re-pin is a
finding (engine not actually emitting misfire there) — report it.

### Context ###
- Precedent (mechanism to copy): `T-V3-2_surface_repin_oracle.md` + `V3_ORACLE_REPIN_2026-06-30.md`
  (oracle re-pin) and `T-V3-2R_v3_yardstick_hashlock_rebind.md` (mint + rebind + drift fixture).
- Mode source: `apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md` (ORACLE_SUSPECT list).
- Research disposition: `v3/research/research_answers/cluster1.md` (mechanical vs misfire).
- Hash-lock code: `score_v3_yardstick.py` `ACTIVE_CSV_SHA256`/`ACTIVE_ORACLE_SUBSET_SHA256`/
  `YARDSTICK_NAME` (:41-55, :133 `check_hash_lock`). `SCORER_PATH` = `run_suite.py` (do NOT edit).

### Consumer (signal/noise) ###
- **Consumer:** the v3 acceptance gate (`top3_family`, single-verdict) + the frozen-yardstick guard.
- **Code path:** oracle CSV (10 rows) + scoreboard yardstick constants. No engine, no `run_suite.py`.

### Deliverables ###
1. `apps/wired/v7/data/cases_petrol_v7.csv` — MODIFY (10 rows re-pinned).
2. `apps/wired/fl_tasks/score_v3_yardstick.py` — MODIFY (mint `V3_YARDSTICK_2026-07-01`; new hashes).
3. `v3/reports/V3_ORACLE_REPIN_MW_MISFIRE_2026-07-01.md` — CREATE (change-record: 10 rows, hashes).
4. `apps/wired/v7/runs/POST_ORACLE_MW/results.json` — the AFTER run.
5. drift/guard test — UPDATE to the new yardstick (per T-V3-2R).

### Files to touch ###
- `apps/wired/v7/data/cases_petrol_v7.csv` (MODIFY — 10 rows)
- `apps/wired/fl_tasks/score_v3_yardstick.py` (MODIFY — new yardstick mint)
- `v3/reports/V3_ORACLE_REPIN_MW_MISFIRE_2026-07-01.md` (CREATE)
- the T-V3-2R drift/guard test (UPDATE)

### Out of scope ###
No engine/router/registry edit. **Do NOT edit `run_suite.py`** (hash-locked). Do NOT re-pin the 4
non-suspect mechanical_wear rows. No abstain change (that's T-V3-3D-ABSTAIN-CAL). No `Vault/` edits.
GRAPH GUARDRAIL: no `graphify`/graph rebuild. Never overwrite the frozen `FL_YARDSTICK_2026-06-30`.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --write-results apps/wired/v7/runs/POST_ORACLE_MW/results.json | sed -n '1,16p'
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff \
  --before apps/wired/v7/runs/POST_T_V3_4B/results.json \
  --after  apps/wired/v7/runs/POST_ORACLE_MW/results.json | grep -iE 'REGRESSIONS|newly_pass'
```
Gate: `Hash lock: ok` on `V3_YARDSTICK_2026-07-01`; exactly the 10 re-pinned case_ids in `newly_pass`;
`top3_family` 184 → 194 (or report actual); no unintended family regressed; change-record written.

### Progress hook ###
PROGRESS.md `FL-V3-ORACLE-MW-MISFIRE`: Status=done, Files changed=~5, Verification="re-pinned 10
ORACLE_SUSPECT mw->misfire; minted V3_YARDSTICK_2026-07-01 (csv/oracle SHA updated, run_suite
untouched, Hash lock ok); top3_family 184->1NN; single_verdict 133->1NN; only the 10 flipped;
answer-key-change caveat recorded".

### Depends on ###
T-V3-4B done. Owner sign-off GRANTED (2026-07-01). Independent of T-V3-3D-ABSTAIN-CAL (either order).
