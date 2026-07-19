### Goal ###
Disclose, per case, whether the **20 TUNABLE OUTRANKED** cases can actually be recovered by a
bounded rule-weight change — separating the truly **reweightable** from those that are really
**signal-gated** (the correct discriminator needs a measurement the idle snapshot lacks) or
**FT-8-risky** (the reweight would regress a neighbour). **No weight edits, no engine change** — this
is analysis/simulation only. It sizes and de-risks the actual commit (`T-V3-4B`).

### Progressive-disclosure role — the DISCLOSE step ###
Rank-tuning is the project's discouraged last resort: canon says recover OUTRANKED by *surfacing*
runner-ups, **not** by re-weighting, and any weight change must run the full corpus with **no
regressed family** (audit FT-8). The 20 TUNABLE are the rank-4/5 residual that surfacing (top-3)
cannot reach, so reweight is on the table — but only where the research says the lift is
*diagnostically correct* and FT-8 is safe. This task reveals which of the 20 clear those bars; the
commit `T-V3-4B` applies **only** the cleared set, behind this disclosure + owner sign-off. Reveal
first, commit later — do not touch a weight in this task.

### Why this split (the trap it avoids) ###
Blindly reweighting to pass the 20 would (a) risk shipping a *diagnostically wrong* discriminator
(worse than a miss — it makes the engine confidently wrong), and (b) regress neighbours that share
the reweighted rule (FT-8). The rule JSON makes both checkable offline: each rule declares its
required `chemistry_evidence`/`obd_evidence` (tier + PID) and a `passes_cases` list (the exact
neighbour set at risk). So feasibility is knowable **before** any weight moves.

### Success criteria ###
Produce `v3/reports/V3_TUNABLE_REWEIGHT_MAP_2026-07-01.{md,json}` covering all 20 TUNABLE case_ids
from `v3/reports/V3_OUTRANKED_MAP_2026-06-30.md` (bucket=TUNABLE). Per case, record:
1. `expected_family`/`expected_rule` + `winner_family`/`winner_rule`, current scores, gap, and the
   expected family's current rank (from the frozen trace / OUTRANKED map).
2. **Cluster + diagnostically-correct discriminator:** map the confusion (e.g. lean vs sensor,
   exhaust_leak vs lean, rich vs misfire) to its research cluster in
   `v3/research/research_answers/cluster*.md` and cite the specific discriminator the research says
   separates the two families.
3. **Evidence availability (the signal-gate test):** does the expected rule's required evidence
   (its `chemistry_evidence`/`obd_evidence` state/PID, with tier) actually exist in **this case's**
   inputs? If a DEFINITIVE discriminator's PID is absent (cf. rule `precondition` notes like
   "not in OBDLivePayload"), the case is **SIGNAL-GATED**, not reweightable — re-bucket it to the
   Phase-4 signal packs, don't force it with a weight.
4. **Minimal bounded lift:** the smallest `base_weight` delta on the expected rule that would raise
   the expected family to rank <=3, and whether that delta stays within a stated bound (propose the
   FT-8 bound, e.g. <=0.15, consistent with the TUNABLE gap definition).
5. **FT-8 neighbour risk:** enumerate the `passes_cases` of every rule whose weight the lift would
   change — the concrete cases that could regress. Flag same-`competition_group` collisions.
6. **Per-case verdict:** `REWEIGHTABLE` (cluster-justified + evidence-present + delta in-bound +
   low neighbour risk) / `SIGNAL-GATED` / `RISKY` (would likely regress a neighbour).
Summary headline: of 20 → `R` reweightable, `S` signal-gated (→ signal packs), `K` risky. That
triage is the disclosure that scopes `T-V3-4B`.

- **Self-check (proves the simulation is trustworthy):** with a **zero** weight delta, the simulator
  must reproduce the current ranks exactly for all 294 cases (no drift) before any lift is simulated.
- Inner loop clean on any helper (`py_compile`, `ruff`, `pyright`). No engine test needed (no engine
  change). `top3_family` and the yardstick are untouched by this task.

### Disclosure (what this task must surface, not hide) ###
If fewer than 20 are cleanly reweightable, that shortfall **is** the finding — say how many are
signal-gated (belong to Phase 4, not this pack) and how many are FT-8-risky. Do not present "20
recoverable by reweight" if the evidence isn't there. For every proposed lift, name the neighbour
cases it puts at risk, so `T-V3-4B` looks exactly as expensive/risky as it is.

### Context ###
- TUNABLE set (20): `v3/reports/V3_OUTRANKED_MAP_2026-06-30.{md,json}` (bucket=TUNABLE); carries
  per-case expected/winner rule, scores, gap, base_weight, deciding terms.
- Rule weights + evidence + neighbour sets: `labs/comlab/registry/rules/<family>.json` — fields
  `base_weight`, `chemistry_evidence`, `obd_evidence` (tier/PID/precondition), `competition_group`,
  `passes_cases`. (Query only — do NOT edit these in this task.)
- Research discriminators: `v3/research/research_answers/cluster{1-9}.md` (C1 mech vs misfire, C2
  rich vs catalyst, C3 ecu, C4 exhaust_leak/lean/sensor, C5 lean root cause, C6 sensor
  under-detection, C7 cam/vvt). Cross-family mapping precedent: `v3/producer_gap_split.py` /
  `V3_PRODUCER_GAP_SPLIT` already mapped cases → clusters; reuse its approach.
- Current ranks/scores to simulate against: `apps/wired/v7/runs/POST_T_V3_3C/results.json` and the
  frozen trace the OUTRANKED map was built from. Rank-recovery phase: `V3_PLAN §4` + §5 FT-8 rule.

### Consumer (signal/noise) ###
- **Consumer:** the owner's go/no-go on `T-V3-4B` and its exact case scope; the FT-8 gate.
- **Code path:** read-only analysis over reports + registry JSON + run results. No engine/scorer/
  oracle/CSV edit.

### Deliverables ###
1. `v3/reports/V3_TUNABLE_REWEIGHT_MAP_2026-07-01.{md,json}` — CREATE. Per-case triage + summary.
2. `v3/tunable_reweight_sim.py` — CREATE, read-only rank simulator (zero-delta self-check + per-case
   minimal-lift computation). Does not import or mutate engine state; recomputes ranks from scores.

### Files to touch ###
- `v3/reports/V3_TUNABLE_REWEIGHT_MAP_2026-07-01.md` (CREATE)
- `v3/reports/V3_TUNABLE_REWEIGHT_MAP_2026-07-01.json` (CREATE)
- `v3/tunable_reweight_sim.py` (CREATE, read-only)

### Out of scope ###
**No `base_weight` or any rule/registry edit. No engine, scorer, oracle, or CSV edit. No re-score
that mutates a run.** (All weight changes are `T-V3-4B`, gated behind this + owner sign-off.) No
abstain changes (owner deferred that; dial stays at MARGIN=0.05 — see `T-V3-3D-ABSTAIN-CAL`). Edit
live `labs/comlab/` only if ever — but this task writes only under `v3/`. Never `Vault/`. GRAPH
GUARDRAIL: no `graphify`/graph rebuild.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/tunable_reweight_sim.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/tunable_reweight_sim.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/tunable_reweight_sim.py
# zero-delta self-check must reproduce current ranks for all 294 (no drift):
/agent_workspace/.venv-wired/bin/python v3/tunable_reweight_sim.py --self-check
# produce the map:
/agent_workspace/.venv-wired/bin/python v3/tunable_reweight_sim.py --write v3/reports/V3_TUNABLE_REWEIGHT_MAP_2026-07-01.json
```
Gate: self-check drift == 0; all 20 TUNABLE case_ids present with a verdict
(REWEIGHTABLE/SIGNAL-GATED/RISKY); each REWEIGHTABLE cites its cluster discriminator, confirms
evidence present, states the minimal in-bound delta, and lists its FT-8 neighbour set. No registry/
engine file modified (git status shows only new files under `v3/`).

### Progress hook ###
PROGRESS.md `T-V3-4A`: Status=done, Files changed=3 (all new under v3/), Verification="TUNABLE
reweight feasibility map: of 20 -> R reweightable / S signal-gated / K risky; each reweightable
cluster-justified + evidence-present + delta<=BOUND + neighbour set listed; zero-delta self-check
drift=0; no weights touched".

### Depends on ###
T-V3-3C done (current ranks/scores available). Research answers present
(`v3/research/research_answers/`). Runnable now.
