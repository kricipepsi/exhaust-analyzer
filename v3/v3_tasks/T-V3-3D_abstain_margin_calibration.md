### Goal ###
Close the abstain thread: set the family-aware margin threshold to **MARGIN = 0.02** so the honesty
dial stops being net-harmful. One-constant change + re-score. **Owner-picked operating point** from
the D6 sweep (2026-07-01, "do 2").

### Progressive-disclosure role — the deferred commit (now taken) ###
D6 disclosed the sweep; the owner picked the operating point. At the current 0.05 the dial silences
almost as many right answers as wrong (88 vs 97); D6's sweep showed **0.02** is the elbow: coverage
~0.37 → ~0.78 with the dial finally net-honest (silences more wrong than right). This task commits
that value. Floor stays 0.80 (inert but retained as a safety net if scores are ever recalibrated).

### Success criteria ###
- Change `ABSTAIN_MARGIN` from `0.05` to `0.02` at `fault_atlas_router.py:82` (the single constant
  used by both the REG-v2 site :2154 and the v1 site :2302 — the family-aware selection from T-V3-3C
  is unchanged). Sync the scoreboard's display constant `score_v3_yardstick.py:62` to `0.02` so the
  printed `abstain_margin` header matches (display-only; not hash-locked).
- **No engine-logic change** beyond the constant. Family-aware margin (different-family sibling)
  stays exactly as T-V3-3C shipped.
- Re-score on the **current post-4B engine** (top3_family 184): `top3_family` **unchanged at 184**
  (abstain never changes the verdict); `coverage` rises to ~0.78 (report actual — D6's 0.78 was
  measured on post-3C/176, so re-verify on 184); `total_abstained` drops from 185 toward ~65;
  `Hash lock: ok` (run_suite untouched).
- **Disclosure:** report the new `coverage`, `top3_on_covered`, `total_abstained`, and the abstained
  right/wrong split (expect ~net-honest: more top3-wrong silenced than top3-right hidden). Any case
  the dial still hides that the engine gets right is disclosed per D6's honesty rule.
- A test asserts abstain fires at margin ≤ 0.02 and not above; and that `top3_family` count is
  unchanged by the threshold move.
- Inner loop clean: `py_compile`, `ruff`, `pyright`, `pytest -x -q`.

### Disclosure (surface, not hide) ###
0.02 is a *net-honest* dial, not a perfect one — it still hides some wins and lets some wrong answers
through (see D6 sweep: at 0.02, ~27 hidden / ~38 correctly silenced on the 176 baseline; re-measure
on 184). Report the post-4B numbers; do not present 0.02 as "solved." The residual is the genuine
cross-family ambiguity that only Phase-4 signals resolve.

### Context ###
- Operating point source: `v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.md` (D6 sweep).
- Constant + sites: `fault_atlas_router.py:82` (`ABSTAIN_MARGIN`), used at `:2154` (REG-v2) and
  `:2302` (v1 family-aware). Scoreboard reads `verdict.abstained` (T-V3-3B wiring); its `:62`
  constant is display-only.
- Floor inertness (0/297 < 0.80) is unchanged and expected — leave `ABSTAIN_FLOOR=0.80`.

### Consumer (signal/noise) ###
- **Consumer:** UI verdict card (PRD §5.2) `abstained`/`abstain_reason`; scoreboard `coverage` /
  `top3_on_covered`.
- **Code path:** one router constant (+ display sync). No schema/run_suite/oracle/CSV change.

### Deliverables ###
1. `labs/comlab/comlab/core/fault_atlas_router.py` — MODIFY (`ABSTAIN_MARGIN` 0.05 → 0.02).
2. `apps/wired/fl_tasks/score_v3_yardstick.py` — MODIFY (display constant :62 → 0.02).
3. `labs/comlab/.../tests/test_abstain_margin_002.py` — CREATE.
4. `apps/wired/v7/runs/POST_T_V3_3D/results.json` — the AFTER run.

### Files to touch ###
- `labs/comlab/comlab/core/fault_atlas_router.py` (MODIFY)
- `apps/wired/fl_tasks/score_v3_yardstick.py` (MODIFY — display constant only)
- `labs/comlab/.../tests/test_abstain_margin_002.py` (CREATE)

### Out of scope ###
No family-aware-logic change (T-V3-3C stays). No floor change. No re-pin/oracle/CSV edit. **Do NOT
edit `run_suite.py`** (hash-locked). No `Vault/` edits. GRAPH GUARDRAIL: no `graphify`/graph rebuild.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m pytest -x -q labs/comlab -k abstain_margin_002
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --write-results apps/wired/v7/runs/POST_T_V3_3D/results.json | sed -n '1,16p'
```
Gate: `Hash lock: ok`; `top3_family` == 184/294 (unchanged); `coverage` ≈ 0.78 (report actual);
`total_abstained` ≈ 65; abstained right/wrong split disclosed.

### Progress hook ###
PROGRESS.md `T-V3-3D`: Status=done, Files changed=4, Verification="ABSTAIN_MARGIN 0.05->0.02; top3_family
unchanged 184; coverage 0.37->~0.78, total_abstained 185->~NN; net-honest (more wrong silenced than
right hidden); run_suite untouched, Hash lock ok".

### Depends on ###
T-V3-D6 done (owner picked 0.02). Independent of the oracle re-pin (either order; each re-scores on
the then-current engine).
