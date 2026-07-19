### Goal ###
Emit the **abstain** decision on the verdict — the honesty dial that lets the engine decline a
low-confidence answer instead of guessing. Split out of T-V3-3 by design; **now unblocked** by the
T-V3-D5 disclosure. Ships the verdict-level abstain surface and the fire/no-fire logic, and wires the
scoreboard to read it.

### Progressive-disclosure role — ACTIVE (the deferred secondary layer, now calibrated) ###
This was held until T-V3-D5 disclosed the real post-T-V3-3 numbers so the dial is set against
measured reality, not an estimate. D5 disclosed: `top3_family = 176/294`, `single_verdict = 133/294`,
`coverage = 1.00` (abstain not yet shipped), `total_abstained = 0`. Abstain does **not** change
`top3_family` (the acceptance metric); it changes `coverage` / `top3_on_covered` (the honesty dial).
Calibration is **confirmed at the T-V3-0 defaults** (owner: "as you recommend", 2026-07-01):
`FLOOR = 0.80`, `MARGIN = 0.05` — single source `v3/reports/V3_TOPK_CEILING_2026-06-30.md` §6, which
also matches the scoreboard constants `ABSTAIN_FLOOR` / `ABSTAIN_MARGIN`
(`apps/wired/fl_tasks/score_v3_yardstick.py:61-62`). Cite it; do not reinvent the numbers.

### The wiring seam (read before touching code) ###
The scoreboard currently reads the abstain flag at the **result top level** —
`result.get("abstained", False)` (`score_v3_yardstick.py:381`) — which is **never populated today**,
so coverage always reads 1.00. The engine verdict is serialized into the result **as-is** by the
frozen harness: `run_suite.py:347` sets `"verdict": result_dict.get("diagnostic_verdict")`.
Consequence:
- **`run_suite.py` is HASH-LOCKED** (`SCORER_PATH`, `ACTIVE_SCORER_SHA256`
  `dc47eb4f…`, checked by `check_hash_lock`). **Do not edit it** — any change trips the lock
  (`REFUSED`) and forces a yardstick re-mint. That is out of scope.
- Therefore abstain must ride **inside** `diagnostic_verdict` (which `run_suite` copies through
  untouched → it lands at `result["verdict"]["abstained"]`), and the **scoreboard** read-site
  (`score_v3_yardstick.py`, NOT hash-locked) is updated to read from the verdict. One authoritative
  value (the engine verdict); the harness passes it through; the scoreboard reads it. No `run_suite`
  edit, hash lock stays `ok`.

### Success criteria ###
- `DiagnosticVerdict` carries an **additive/optional** abstain surface (so existing consumers don't
  break): `abstained: bool = False` and `abstain_reason: Optional[Literal["floor","margin"]] = None`.
  It fires when `winner_score < FLOOR` **or** `top1 − top2 ≤ MARGIN` (top1 = `winner_score`, top2 =
  first runner-up score; if there is no runner-up, the margin rule cannot fire). FLOOR/MARGIN are
  named constants in the router citing V3_TOPK_CEILING §6.
- Abstain is emitted on **both** assembly paths — the v1/default `DiagnosticVerdict(...)` build
  (`fault_atlas_router.py:2256`) and the **REG-v2 default path** verdict dict
  (`:2129` `verdict_dict = v2_output.get("diagnostic_verdict", {})`). T-V3-3's lesson: the v2 path is
  the one that ships; emitting on v1 only would be a silent no-op on the scored run.
- The scoreboard reads the engine flag: change `score_v3_yardstick.py:381` from
  `result.get("abstained", False)` to read `result.get("verdict", {}).get("abstained", False)`
  (behaviour-preserving until the engine emits — top-level was always absent). `score_v3_yardstick.py`
  is **not** hash-locked; `run_suite.py` is untouched, so `Hash lock: ok` must still hold.
- **No-regression — stated precisely (this replaces "single_verdict stays 133"):**
  - HARD invariant (unconditional gate): abstain is an additive flag only. No verdict's
    `fault_family`/`fault_code`/dimensions and no differential sibling changes. Therefore
    `top3_family` stays **176/294** and every case's raw dimension PASS/FAIL is unchanged.
  - `single_verdict family+state` is measured on **covered** (non-abstained) cases, so it MAY drop
    from 133 by exactly the number of previously-passing cases the dial now masks. That is the
    honesty tradeoff, not a regression — **but it must reconcile**:
    `covered_single_verdict + (abstained ∩ previously-passing) == 133`. Report that reconciliation.
- A test proves abstain **fires** on a known ambiguous case (winner_score < 0.80 or margin ≤ 0.05)
  and does **not** fire on a clean high-margin case; and that an abstained case keeps its
  `differential_siblings` and `fault_family` (top3 surface intact).
- Inner loop clean on changed files: `py_compile` (compiles), `ruff` (style check), `pyright`
  (type check), `pytest -x -q` (unit tests).

### Disclosure (what this task must surface, not hide) ###
Report the abstained case_ids and, per case, the trigger (`floor` vs `margin`). Split them into:
(a) cases the engine would have gotten **wrong** — abstaining is a correct silence; and
(b) cases the engine would have gotten **right** (in the 133 or in top3_family) — abstaining
**hides a win**, which is a finding, not a success. Record the new `coverage` and `top3_on_covered`,
and the drop in reported `single_verdict` with its reconciliation to 133. If the dial masks more
right-than-wrong answers at 0.80/0.05, say so — that is the signal the owner uses to retune the dial.

### Context ###
Phase P3 honesty dial, `v3/V3_PLAN.md` §0 (verdict shape = ranked top-3 **+ abstain**). Anchors
re-verified 2026-07-01 **after** T-V3-3's edits (line numbers current):
- `labs/comlab/comlab/schemas/response.py`: `class DiagnosticVerdict` at **:92** (fields :96-104;
  `fault_family` :100, `differential_siblings` :104). Add the abstain fields here. `Optional` /
  `Literal` already imported (used at :87, :34).
- `labs/comlab/comlab/core/fault_atlas_router.py`: `TriageVerdict` :225-229 (`winner_score` :228,
  `runner_ups: list[tuple[RegistryRow, float]]` :229); `winner, winner_score = scored[0]` and
  `runner_ups = scored[1:4]` at **:1654-1655**; `MIN_CONFIDENCE_THRESHOLD` zeroes `winner_score` at
  :1687 (a threshold-miss → `winner_score = 0.0` → floor rule fires; that is intended — note it in
  the test). v1 verdict build `DiagnosticVerdict(` at **:2256** (`differential_siblings=` :2264,
  wrapped `diagnostic_verdict=verdict_obj` :2303); REG-v2 verdict dict at **:2129**.
- `apps/wired/fl_tasks/score_v3_yardstick.py`: read-site **:381**; constants :61-62; the abstain
  values are display-only today (:528-529) — the scoreboard does **not** compute abstain, it reads it.

### Consumer (signal/noise) ###
- **Consumer:** the UI verdict card (PRD §5.2) reads `verdict.abstained` / `verdict.abstain_reason`;
  the scoreboard's `coverage` / `top3_on_covered` read the same flag through the verdict. One
  authoritative value on the verdict — no orphan (T-V3-3's lint lesson).
- **Code path:** `DiagnosticVerdict` abstain fields + emit on both router assembly paths; scoreboard
  read-site rebind. No `run_suite.py` edit (hash-locked).

### Deliverables ###
1. `labs/comlab/comlab/schemas/response.py` — MODIFY (add `abstained` + `abstain_reason` to
   `DiagnosticVerdict`).
2. `labs/comlab/comlab/core/fault_atlas_router.py` — MODIFY (compute abstain from
   `winner_score`/`runner_ups`; set it on BOTH the v1 build :2256 and the REG-v2 verdict dict :2129;
   FLOOR/MARGIN named constants citing V3_TOPK_CEILING §6).
3. `apps/wired/fl_tasks/score_v3_yardstick.py` — MODIFY (one-line read-site rebind :381,
   top-level → verdict). NOT hash-locked.
4. `labs/comlab/.../tests/test_abstain_emit.py` — CREATE.

### Files to touch ###
- `labs/comlab/comlab/schemas/response.py` (MODIFY)
- `labs/comlab/comlab/core/fault_atlas_router.py` (MODIFY)
- `apps/wired/fl_tasks/score_v3_yardstick.py` (MODIFY — read-site only)
- `labs/comlab/.../tests/test_abstain_emit.py` (CREATE)

### Out of scope ###
**Do NOT edit `run_suite.py`** (hash-locked scorer — would force a yardstick re-mint). No surfacing
changes (that was T-V3-3). No score-weight re-tuning (T-V3-4). No change to FLOOR/MARGIN values away
from 0.80/0.05 without a new owner decision. No oracle/CSV edits. No new scoreboard subcommands. Edit
live `labs/comlab/` only — never `Vault/`. GRAPH GUARDRAIL: no `graphify`/graph rebuild.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile labs/comlab/comlab/schemas/response.py labs/comlab/comlab/core/fault_atlas_router.py apps/wired/fl_tasks/score_v3_yardstick.py
/agent_workspace/.venv-wired/bin/python -m ruff check labs/comlab/comlab/schemas/response.py labs/comlab/comlab/core/fault_atlas_router.py apps/wired/fl_tasks/score_v3_yardstick.py
/agent_workspace/.venv-wired/bin/python -m pyright labs/comlab/comlab/schemas/response.py labs/comlab/comlab/core/fault_atlas_router.py apps/wired/fl_tasks/score_v3_yardstick.py
/agent_workspace/.venv-wired/bin/python -m pytest -x -q labs/comlab -k abstain_emit
# Re-run the engine, then score against the rebound V3 guard (no override):
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --write-results apps/wired/v7/runs/POST_T_V3_3B/results.json | sed -n '1,16p'
```
Gate: `Hash lock: ok` (proves `run_suite.py` untouched); `top3_family` == **176/294** (unchanged);
`coverage` < 1.00 and `total_abstained` > 0 (dial now live); reported `single_verdict` reconciles to
133 via the covered + masked-previously-passing identity; abstained case_ids + triggers disclosed.

### Progress hook ###
PROGRESS.md `T-V3-3B`: Status=done, Files changed=4, Verification="abstain emits on floor<0.80/
margin<=0.05 on both v1+v2 paths; scoreboard reads verdict flag (run_suite untouched, Hash lock ok);
top3_family unchanged 176/294; coverage=CC, top3_on_covered=PP, total_abstained=NN; single_verdict
133 reconciled (covered + masked); abstained case_ids + right/wrong split disclosed".

### Depends on ###
T-V3-3 (surfacing) done; **T-V3-D5 disclosure reviewed + calibration confirmed (0.80/0.05, owner
2026-07-01)** — both satisfied; this task is runnable.
