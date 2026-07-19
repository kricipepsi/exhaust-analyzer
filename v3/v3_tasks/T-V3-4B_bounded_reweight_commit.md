### Goal ###
Apply the **bounded rule-weight lifts** for the **8 REWEIGHTABLE** TUNABLE cases cleared by
`T-V3-4A`, recovering them into the top-3 without regressing any neighbour. This is the **COMMIT**
step: it edits `base_weight` in the live registry rules only, gated by FT-8 (full-corpus, no
regressed family) and **owner sign-off on the exact deltas**.

### Progressive-disclosure role — the COMMIT (gated) ###
`T-V3-4A` disclosed the triage of the 20 TUNABLE: **8 REWEIGHTABLE**, 1 signal-gated, 6 risky
(neighbour regressions), 5 hard (confidence ceiling). This task commits **only the 8**. The other 12
stay out: the signal-gated + hard ones are the discrimination wall (signal packs / owner data); the 6
risky ones would regress neighbours and are not worth the collateral. Do not expand scope here.

### Honesty caveat (must stay visible — do not drop) ###
The cluster discriminators that *diagnostically* separate these families are largely **Phase-4
signals absent from the idle snapshot** (two-point fuel-trim delta idle→2500 RPM, Mode $06, CO₂
dilution). So these lifts are **prior nudges** justified by the oracle ground truth + the cluster
research — **not** by an in-snapshot discriminator the engine can compute. They improve the corpus
score without regressing it (FT-8 clean), but they do **not** add real discrimination; the true fix
for these confusions remains the Phase-4 signal packs. Record this in the progress note so the
corpus gain (+up to 8) is never misread as the engine learning to tell these families apart.

### The commit set (8 cases via 6 rules) — deltas proposed by T-V3-4A, subject to owner sign-off ###
| Rule | base_weight now → proposed | Recovers | Cluster |
|---|---|---|---|
| EL-001 (exhaust_leak) | 0.80 → 0.851 | CSV-095, era1_016, era3_019 (3) | C4 exhaust_leak vs lean |
| RM-001 (rich_mixture) | 0.85 → 0.90 | EXP-N027 | C1 rich vs misfire |
| LC-002 (lean_condition) | 0.80 → 0.81 | era3_007 | C2 lean vs catalyst |
| CF-002 (catalyst_failure) | 0.70 → 0.701 | YAML-PDF_4G_01 | C2 catalyst vs cam_timing |
| MF-001 (misfire) | 0.85 → 0.851 | EXP-N014 | C6 misfire vs sensor |
| CF-001 (catalyst_failure) | 0.85 → 0.851 (ε tie-break) | EXT-207 (gap 0.000) | C2 catalyst vs lean |

`EXT-207` is a **tie** (delta 0.000), not a deficit — the minimal ε that breaks the tie in CF-001's
favour is the fix. If no weight-only ε breaks it FT-8-clean, **drop EXT-207** and disclose (do not add
tie-break engine logic in this task).

### Success criteria ###
- Edit **only** `base_weight` in the six rules above, in the live registry
  (`labs/comlab/registry/rules/{exhaust_leak,rich_mixture,lean_condition,catalyst_failure,misfire}.json`).
  No other rule/field/engine edit. (Confirmed: the router reads `base_weight` live from the registry
  at load — `fault_atlas_router.py:1046`, `:658` — so **no `graphify`/graph rebuild** is needed or
  permitted.)
- **FT-8 gate — combined, not per-rule:** apply **all** deltas together, then run the full corpus and
  `diff` vs the pre-commit run (`POST_T_V3_3C`). `REGRESSIONS:` line **must be empty** and no
  per-family single-verdict count may drop. (T-V3-4A checked deltas individually; interactions must
  be re-verified as a set — the risky-case regressions `CASE-023`/`EXT-217` prove LC-002/MF at higher
  deltas bite, so confirm the small in-bound deltas here stay clean when combined.)
- `top3_family` rises from **176/294** by up to **+8** (target 184/294; report the actual — if
  EXT-207 is dropped, +7). Every recovered case_id is in the `diff` `newly_pass`.
- `Hash lock: ok` (registry JSON is not hash-locked; `run_suite.py` untouched). Abstain unchanged
  (MARGIN=0.05 — owner deferred `T-V3-3D-ABSTAIN-CAL`).
- A test asserts each of the 8 expected families now ranks ≤3 (or is a differential sibling counted
  by the scorer) and that a named neighbour from each touched rule's `passes_cases` still passes.
- Inner loop clean: `py_compile`, `ruff`, `pyright`, `pytest -x -q`.

### Disclosure (surface, not hide) ###
Report the actual `top3_family` gain and the per-case newly_pass; keep the honesty caveat above; and
state that the 12 non-committed TUNABLE (1 signal-gated + 6 risky + 5 hard) remain open and route to
signal packs, **not** to more reweighting. If any delta fails the combined FT-8 check, drop that case
and report it rather than raising the delta to force it.

### Context ###
- Feasibility map + exact deltas/neighbour sets: `v3/reports/V3_TUNABLE_REWEIGHT_MAP_2026-07-01.{md,json}`.
- Touched rules' FT-8 neighbour sets (`passes_cases`): EL-001 {CSV-095,TC-048,YAML-CSV95};
  MF-001 {CSV-101..104,EXT-234..236}; RM-001 {CSV-018,EXP-N003,EXT-203,EXP-N013,EXT-227};
  CF-001 {REAL-005,PDF-4G-01,case_010,case_034}; CF-002 {CSV-121,CSV-122,EXP-N008,EXT-232,EXT-233,CASE-015};
  LC-002 {REAL-002,EXP-N011,case_003}. (Raising a rule can't regress its own passes_cases; the risk is
  cases where the rule is a losing sibling — that is what the corpus `diff` catches.)
- FT-8 rule: `V3_PLAN §5`; instrument = T-V3-D4 `diff` REGRESSIONS. Weight load path:
  `fault_atlas_router.py:1046` (`row.confidence_scoring.base_weight`).

### Consumer (signal/noise) ###
- **Consumer:** the v3 acceptance gate (`top3_family`); the ranker's per-family scores.
- **Code path:** registry `base_weight` values only; re-scored via the existing scoreboard.

### Deliverables ###
1. `labs/comlab/registry/rules/exhaust_leak.json`, `rich_mixture.json`, `lean_condition.json`,
   `catalyst_failure.json`, `misfire.json` — MODIFY (`base_weight` only, per the table).
2. `labs/comlab/.../tests/test_tunable_reweight.py` — CREATE.
3. `apps/wired/v7/runs/POST_T_V3_4B/results.json` — the AFTER run.

### Files to touch ###
- `labs/comlab/registry/rules/exhaust_leak.json` (MODIFY)
- `labs/comlab/registry/rules/rich_mixture.json` (MODIFY)
- `labs/comlab/registry/rules/lean_condition.json` (MODIFY)
- `labs/comlab/registry/rules/catalyst_failure.json` (MODIFY)
- `labs/comlab/registry/rules/misfire.json` (MODIFY)
- `labs/comlab/.../tests/test_tunable_reweight.py` (CREATE)

### Out of scope ###
No engine-logic change (base_weight values only). No touch to the 12 non-committed TUNABLE. No abstain
change. No oracle/CSV/scorer/run_suite edit. No new discriminator/signal. **No `graphify`/graph
rebuild** (not needed — weights load live). Never `Vault/`. If the combined FT-8 check fails for a
case, drop it — do **not** raise the delta beyond the T-V3-4A bound to force a pass.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m pytest -x -q labs/comlab -k tunable_reweight
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --write-results apps/wired/v7/runs/POST_T_V3_4B/results.json | sed -n '1,16p'
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff \
  --before apps/wired/v7/runs/POST_T_V3_3C/results.json \
  --after  apps/wired/v7/runs/POST_T_V3_4B/results.json | grep -iE 'REGRESSIONS|newly_pass'
```
Gate: `Hash lock: ok`; `REGRESSIONS: (empty)`; `top3_family` 176 → 183–184; `newly_pass` = the
committed recovered case_ids; no per-family single-verdict drop.

### Progress hook ###
PROGRESS.md `T-V3-4B`: Status=done, Files changed=6-7, Verification="bounded reweight of 6 rules
recovered N/8 TUNABLE; top3_family 176->1NN; REGRESSIONS empty (FT-8 clean, combined); Hash lock ok;
prior-nudge caveat recorded; 12 non-committed TUNABLE routed to signal packs".

### Depends on ###
T-V3-4A done (feasibility map). **Owner sign-off GRANTED 2026-07-01 — all 8 (6 rules) approved.**
Remaining gate: FT-8 combined-corpus REGRESSIONS-empty check at run time. Runnable now.
