### Goal ###
**Surface the ranked differential the engine already computes**, so the top-3 scorer (T-V3-1) can
count the runner-ups. Two changes, both **surfacing** (no score weights change — audit FT-8 stays
intact):
1. The v2 default output path must **populate `differential_siblings`** from the runtime
   runner-ups. It currently emits `[]` even though the router computes them internally.
2. Add a resolved **`fault_family`** to `DifferentialSiblingOut` (field = data slot on the output
   record) so the scorer/UI read family directly instead of re-deriving it.

Abstain emission was **split out** to `T-V3-3B` (progressive disclosure — see below). This task's
job is to *disclose the true `top3_family`*; abstain policy is calibrated afterward against that
disclosed number.

### Progressive-disclosure role ###
This is the **disclosure step** of the pack. `top3_family` is the single most decision-relevant
number left in v3: it sets the real residual gap and therefore whether T-V3-4 (rank recovery) and
the signal packs are worth their cost. This task reveals it. It ships the smallest, lowest-risk
engine change that moves that number, and nothing that pre-commits a later decision. Its result is
read through `T-V3-D5`, which lays out the next-decision map. Everything downstream (abstain,
T-V3-4, oracle re-pin, signal packs) is the *secondary layer*, decided only after this discloses.

### Why now / measured payoff ###
Measured against the rebound `V3_YARDSTICK_2026-06-30` guard on the frozen baseline run
`apps/wired/v7/runs/20260630_163900/results.json`:
- `top3_family` currently reads **141/294 (47.96%) — identical to top-1**, because
  `differential_siblings` is `[]` on every row (verified: CASE-013, ECU-002, CSV-043, EXP-N010 all
  empty). The scorer has no runner-ups to count.
- T-V3-0's trace measured the correct family is in the engine's **top-3 for 175/294 (59.52%)**.
- The 38 **FREE** OUTRANKED cases (`v3/reports/V3_OUTRANKED_MAP_2026-06-30.md`, bucket=FREE:
  "expected family already rank 1-3, recoverable by surfacing without rank math") are exactly what
  this unlocks.
So the win is directly measurable and is the disclosure: surface the runner-ups and `top3_family`
rises from 141 toward the 175 trace ceiling — the gap between the two, revealed by this task, is the
first thing the owner reviews.

### Success criteria ###
- `DifferentialSiblingOut` gains `fault_family` (typed `FaultFamilyLit`), populated for every
  runtime runner-up via `self._kg.resolve(row.fault_id).fault_family`, and for editor-curated
  siblings via `self._kg.resolve(sibling_id).fault_family`.
- The v2 default output path emits the runtime runner-ups in `differential_siblings` (no longer
  `[]`) for the OUTRANKED FREE cases. Cap and dedupe rules unchanged (≤5, dedupe by `fault_id`).
- A router test proves a known FREE OUTRANKED case (e.g. `CASE-013`, expected `catalyst_failure`
  at trace rank 3) emits `catalyst_failure` as a differential sibling with `fault_family` populated.
- **No regression:** a full re-score shows single-verdict family+state unchanged at **133/294
  (45.24%)** and no per-family primary count drops. `top3_family` strictly increases (target: the
  38 FREE case_ids flip to top3-pass; expected `top3_family` ≈ 175/294).
- Inner loop clean on the changed files: `py_compile`, `ruff`, `pyright`, `pytest -x -q`.

### Disclosure (what this task must surface, not hide) ###
On the re-score, record — for `T-V3-D5` to consume — the **exact** post-change `top3_family` and,
per FREE case_id, whether it banked. Any FREE case that did **not** move, or any non-FREE case that
did, is reported with a one-line reason. Do not round away or summarize past a surprise: if the real
`top3_family` lands below the 175 trace ceiling, that shortfall is the finding.

### Context ###
Phase 3 of `v3/V3_PLAN.md` (§4). Pinned anchors (verified 2026-07-01):
- Schema: `labs/comlab/comlab/schemas/response.py:79` `class DifferentialSiblingOut` — has
  `fault_id`, `fault_name`, `confidence_score`, `source`; **no** `fault_family`. Add it.
  `FaultFamilyLit` is already the type used by `DiagnosticVerdict.fault_family` (same file, ~:99).
- Router computes runner-ups: `runner_ups = scored[1:4]`
  (`labs/comlab/comlab/core/fault_atlas_router.py:1654`), carried on `TriageVerdict` (:225-228).
- Merge/build: `_merge_differential_siblings` (`:1821`) constructs `DifferentialSiblingOut`
  records; assembly sets `differential_siblings=diff_siblings` on the response (`:2144`, `:2207`).
  `self._kg` is available (`:596`); family lives on the KG node
  (`self._kg.resolve(fault_id).fault_family`, cf. `:1093`, `:1096`) — `RegistryRow` does **not**
  carry family, so resolve via `_kg`.
- The empty-`differential_siblings` symptom is on the v2 default path (run built with
  `USE_V2_REGISTRY=<unset>`, label `frozen-v2-baseline`). Locate where the v2 assembly diverges from
  the `:2144` merge and wire the runner-ups through. (Implementation detail — find the branch; do
  not change scoring.)

### Consumer (signal/noise) ###
- **Consumer:** the top-3 scorer (`score_v3_yardstick.py`, reads `sibling.fault_family`) and the UI
  runner-up panel (PRD §5.3). Ship the schema field, both family resolutions, and the v2-path
  population fix in one diff. No score-weight edits.

### Deliverables ###
1. `labs/comlab/comlab/schemas/response.py` — MODIFY. Add `fault_family: FaultFamilyLit` to
   `DifferentialSiblingOut`. (No `DiagnosticVerdict` change — abstain is T-V3-3B.)
2. `labs/comlab/comlab/core/fault_atlas_router.py` — MODIFY. Resolve + set sibling `fault_family`;
   populate `differential_siblings` on the v2 default path.
3. `labs/comlab/.../tests/test_differential_surfacing.py` — CREATE. Sibling-family + v2-population.

### Files to touch ###
- `labs/comlab/comlab/schemas/response.py` (MODIFY)
- `labs/comlab/comlab/core/fault_atlas_router.py` (MODIFY)
- `labs/comlab/.../tests/test_differential_surfacing.py` (CREATE)

### Out of scope ###
No abstain emission (that is `T-V3-3B`, deferred behind the T-V3-D5 disclosure). No score-weight
re-tuning (research-gated T-V3-4). No oracle/CSV edits. No new discriminators/signals
(research-dependent). Edit live `labs/comlab/` only — **never** `Vault/`. GRAPH GUARDRAIL: no
`graphify`/graph rebuild. Do not change the scoreboard output formats.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile labs/comlab/comlab/schemas/response.py labs/comlab/comlab/core/fault_atlas_router.py
/agent_workspace/.venv-wired/bin/python -m ruff check labs/comlab/comlab/schemas/response.py labs/comlab/comlab/core/fault_atlas_router.py
/agent_workspace/.venv-wired/bin/python -m pyright labs/comlab/comlab/schemas/response.py labs/comlab/comlab/core/fault_atlas_router.py
/agent_workspace/.venv-wired/bin/python -m pytest -x -q labs/comlab -k differential_surfacing
# Re-run the engine and score against the rebound V3 guard (no override needed):
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --write-results apps/wired/v7/runs/POST_T_V3_3/results.json | sed -n '1,16p'
# Gate: single_verdict family+state == 133/294 (45.24%); top3_family strictly > 141/294.
```
No-regression on single-verdict is mandatory before this flips to `done`.

### Progress hook ###
PROGRESS.md `T-V3-3`: Status=done, Files changed=3, Verification="differential siblings populated on
v2 path + carry fault_family; single_verdict unchanged 133/294; top3_family 141->NNN (FREE banked)".
