### Goal ###
Disclose, read-only, the true current status of the **2 CLASSIFIER_FIXABLE** producer-gap cases
(`era2_008`, `CASE-039`) against the live run — and, for whichever is still failing, the **minimal
classifier fix** (which GASLab/OBDLab bin decision to change, and to what) that would recover it
**without a new measurement**. These two are the only Phase-4-adjacent cases the `T-V3-D2` split
flagged as *not* data-gated: their required upstream state is reachable from the row's existing
inputs, so they may be a cheap engine/classifier fix, not a signal pack. **No engine, lab, or
registry edit in this task** — analysis only. It sizes the commit (`T-V3-P4-0B`).

### Progressive-disclosure role — the DISCLOSE step ###
This is the cheapest, most decision-revealing move in Phase 4, so it runs first. The handoff warns
`era2_008` **may already bank** via the `T-V3-3` differential surfacing — if so, it needs *no* fix
and `T-V3-P4-0B` shrinks to one case (or zero). We do not touch a classifier until this task says
which cases actually still fail on the current `POST_T_V3_3D` run and what the smallest correct
rebin is. Reveal first; commit (`T-V3-P4-0B`) later, behind this + owner sign-off.

### Why this split (the trap it avoids) ###
Jumping straight to a classifier edit risks (a) "fixing" a case that already passes (churn + FT-8
risk for zero gain), and (b) forcing a rebin that recovers these 2 but silently rebins a neighbour
that shares the same GASLab/OBDLab bin threshold. Both are knowable read-only: replay each row in
query mode, check whether the expected state is already emitted / already top-3, and enumerate which
other cases sit inside the same bin boundary before proposing any threshold move.

### Success criteria ###
Produce `v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.{md,json}` covering both case_ids
(`era2_008` → expected `VVT_FAILURE`/cam_timing; `CASE-039` → expected `POA_SIGNATURE`/ecu_fault).
Per case, record:
1. **Current run status:** on `apps/wired/v7/runs/POST_T_V3_3D/results.json` — is the expected family
   in the emitted top-3 already? Is it covered or abstained (MARGIN=0.02)? State top3_family
   membership and rank explicitly. (Resolves the "era2_008 may already bank" question with a number.)
2. **Reachability restated against live inputs:** replay the row in query mode and confirm the
   `T-V3-D2` finding still holds — the required gating state's bound signature is satisfiable from the
   row's actual 5-gas / lambda / sample_validity values (quote the bounds, as the split report does).
3. **The minimal classifier fix (if still failing):** name the exact GASLab/OBDLab bin decision that
   mis-binned the state and the smallest change that emits it — e.g. a `sample_validity` handling
   path or a single bin-threshold/enum, cited to the lab's state definition. Do **not** implement it.
4. **FT-8 neighbour risk of that fix:** enumerate every other case whose row falls inside the same
   bin boundary the fix would move, so `T-V3-P4-0B` looks exactly as risky as it is. Flag same
   `competition_group` collisions.
5. **Per-case verdict:** `ALREADY_BANKS` (no fix needed) / `CLASSIFIER_FIX` (cite the minimal change +
   neighbour set) / `RE-BUCKET_TO_SIGNAL` (recheck shows it actually needs a measurement after all).
Headline: of 2 → how many already bank, how many are a live classifier fix, how many re-bucket.
- **Self-check:** the replay harness must reproduce the current emitted family/rank for **all 294**
  cases with zero drift before any per-case claim is trusted (same discipline as `T-V3-4A`).
- Inner loop clean on any helper (`py_compile`, `ruff`, `pyright`). `top3_family`, the yardstick,
  the corpus, and every registry/lab file are **untouched** by this task.

### Disclosure (what this task must surface, not hide) ###
If `era2_008` already banks, say so plainly — do not pad `T-V3-P4-0B` with a no-op fix. If a proposed
rebin puts any neighbour at risk, name the neighbour case_ids; a "cheap fix" that regresses one case
is not cheap. If a recheck shows either case actually needs a measurement (bound satisfiable but the
*discriminating* quantity still absent), re-bucket it to the signal packs and say which cluster.

### Context ###
- The 2 cases + their reachability evidence: `v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.md`
  (rows `era2_008`, `CASE-039`, label `CLASSIFIER_FIXABLE`, with the passing bound signature).
- Replay-in-query-mode harness pattern: reuse `v3/producer_gap_split.py` (it already replays rows
  through GASLab/OBDLab and inspects the required state's gating condition). Query only.
- Current ranks/scores + abstain state: `apps/wired/v7/runs/POST_T_V3_3D/results.json`; re-score
  helper `apps/wired/fl_tasks/score_v3_yardstick.py`.
- Lab state definitions (to name the minimal rebin): `labs/gaslab/`, `labs/obdlab/` — live source,
  **not** `Vault/`. Query only in this task.

### Consumer (signal/noise) ###
- **Consumer:** the owner's go/no-go on `T-V3-P4-0B` and its exact case scope; the FT-8 gate.
- No new field/enum/fault is introduced (this is not a signal pack). Read-only over reports +
  labs (query mode) + run results. No producer/consumer contract to add.

### Deliverables ###
1. `v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md` — CREATE. Per-case status + verdict.
2. `v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.json` — CREATE.
3. (Optional) a thin read-only recheck helper under `v3/` if `producer_gap_split.py` needs a driver;
   must not import-mutate engine/lab state.

### Files to touch ###
- `v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md` (CREATE)
- `v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.json` (CREATE)
- (optional) `v3/p4_classifier_recheck.py` (CREATE, read-only) — only if a driver is needed.

### Out of scope ###
**No GASLab/OBDLab/engine/registry edit. No oracle/CSV edit. No re-score that mutates a run.** All
classifier changes are `T-V3-P4-0B`, gated behind this + owner sign-off. No abstain changes (dial
stays MARGIN=0.02). Edit live `labs/` only if ever — this task writes only under `v3/`. Never
`Vault/`. GRAPH GUARDRAIL: querying labs / building a fresh offline index is fine; **no `graphify`
or frozen-graph rebuild.** No secrets in files.

### Verification ###
```bash
cd /agent_workspace
# if a helper is created:
/agent_workspace/.venv-wired/bin/python -m py_compile v3/p4_classifier_recheck.py 2>/dev/null || true
/agent_workspace/.venv-wired/bin/python -m ruff check v3/ 2>/dev/null || true
# self-check: replay reproduces current emitted family/rank for all 294 (zero drift):
/agent_workspace/.venv-wired/bin/python v3/producer_gap_split.py --self-check 2>/dev/null || true
# both cases present with a verdict; headline reconciles to 2:
grep -iE 'era2_008|CASE-039|ALREADY_BANKS|CLASSIFIER_FIX|RE-BUCKET' v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md
```
Gate: self-check drift == 0; both case_ids present with a verdict; each `CLASSIFIER_FIX` names the
minimal rebin + its FT-8 neighbour set; `era2_008`'s already-banks question answered with the
POST_T_V3_3D rank. `git status` shows only new files under `v3/` (no registry/lab/engine file).

### Progress hook ###
PROGRESS.md `T-V3-P4-0A`: Status=done, Files changed=N (all new under v3/), Verification="2
CLASSIFIER_FIXABLE recheck vs POST_T_V3_3D: X already-bank / Y classifier-fix / Z re-bucket; each
fix names minimal rebin + neighbour set; self-check drift=0; no engine/lab/registry touched".

### Depends on ###
`T-V3-D2` done (the split that flagged these 2). Research answers present. Runnable now.
