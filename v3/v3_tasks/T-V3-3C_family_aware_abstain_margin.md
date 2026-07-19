### Goal ###
Fix the abstain **margin definition** so the honesty dial stops silencing cases where the engine
already agrees on the fault family. The margin currently compares the winner to the very next
sibling/rule; change it to compare against the first sibling of a **different family**. This is a
*definition* fix, not a threshold re-tune — `FLOOR=0.80` / `MARGIN=0.05` stay as-is.

### Progressive-disclosure role — the DISCLOSE step ###
T-V3-3B disclosed that at 0.80/0.05 the dial abstains **264/294 (coverage 0.10)** and hides **115
wins**, because the engine emits **174 exact-tie siblings** (same score as the winner). Measured
breakdown of the 276 margin-abstained cases: **126 have a *same-family* top sibling** (family already
agreed — abstaining there throws away a `top3_family` pass for no honesty gain) and **150 are genuine
different-family ambiguity**. This task ships the smallest engine change that acts on that finding and
**re-discloses coverage / hidden-wins under the family-aware margin**. It does **not** commit the
final thresholds, sibling dedupe, or rank work — those are deferred behind the `T-V3-D6` checkpoint,
decided from this task's disclosed numbers. Reveal first; commit later.

### Why now / expected payoff (to be confirmed by the re-score, not assumed) ###
Making the margin family-aware makes up to the **126 same-family** cases eligible to be answered
instead of abstained (exact recovery is the disclosure — a same-family case may still have a
*different*-family sibling within 0.05 and stay abstained). Expected direction: `coverage` rises from
0.10 toward ~0.5, most of the 115 hidden wins return, and residual abstention concentrates on the
~150 genuine cross-family ties. `top3_family` must stay **176/294** (abstain is additive; it changes
no verdict). The exact recovered/residual counts are what `T-V3-D6` reads.

### Success criteria ###
- Abstain margin is computed against the first sibling/rule whose **fault_family differs from the
  winner's**, on **both** assembly paths:
  - **REG-v2** (`fault_atlas_router.py:2137-2143`): the `top2_score` loop currently skips only the
    same `rule_id` (`r_id != winner_rule_id`). Change it to also skip rules whose family equals the
    winner's family — i.e. select the first scored rule with `fault_family != winner_family`
    (winner family = `verdict_dict.get("fault_family")`; rule family = `rule.get("fault_family")`,
    the same key `_build_v2_differential_siblings` reads). If none exists, `top2_score` stays `None`
    (margin rule cannot fire).
  - **v1 default** (`fault_atlas_router.py:2289`): replace `runner_ups[0][1]` with the score of the
    first runner-up whose family differs from the winner's. Resolve family the established way,
    `self._kg.resolve(row.fault_id).fault_family` (cf. :1098), winner family = the `fault_family`
    local in scope. If no different-family runner-up exists, the margin rule cannot fire.
- `FLOOR` / `MARGIN` values unchanged (0.80 / 0.05, still citing `V3_TOPK_CEILING §6`). Floor rule
  unchanged. Only the *selection of top2* changes.
- **No-regression (unconditional):** `top3_family` stays **176/294**; no verdict's
  `fault_family`/`fault_code`/dimensions or differential ordering changes. `Hash lock: ok`
  (`run_suite.py` untouched; scoreboard read-site already reads `verdict.abstained` from T-V3-3B — no
  scorer edit needed).
- **Disclosure reconciliation:** report new `coverage`, `top3_on_covered`, `total_abstained`, and the
  abstained right/wrong split; state how many of T-V3-3B's 115 hidden wins are recovered and how many
  same-family abstentions remain (should trend to ~0; any residual same-family abstention is a
  finding — likely a duplicate-sibling/dedupe artifact for `T-V3-D6`).
- A test proves: (a) a case whose top sibling is the **same family** as the winner is **no longer**
  margin-abstained; (b) a case with a genuine **different-family** tie **still** abstains; (c) floor
  behaviour and `top3_family` surface are unchanged.
- Inner loop clean on changed files: `py_compile`, `ruff`, `pyright`, `pytest -x -q`.

### Disclosure (what this task must surface, not hide) ###
The headline number is the recovered coverage and the remaining hidden-win count. If family-aware
margin still hides wins, say how many and why (same-family duplicates vs genuine ties). Do not present
recovered coverage as "the dial is fixed" if residual abstention still masks correct answers — that
residual is exactly what `T-V3-D6` triages. Keep the abstained case_ids + trigger + right/wrong split
so the owner sees which cases the dial now silences.

### Context ###
Anchors verified 2026-07-01 (post-T-V3-3B):
- `labs/comlab/comlab/core/fault_atlas_router.py`: constants `ABSTAIN_FLOOR`/`ABSTAIN_MARGIN`
  :81-82; REG-v2 abstain block :2132-2156 (top2 selection loop :2138-2143); v1 abstain block
  :2283-2291 (`runner_ups[0][1]` at :2289); `runner_ups = scored[1:4]` :1659; family resolve pattern
  `self._kg.resolve(row.fault_id).fault_family` :1098+.
- `labs/comlab/comlab/schemas/response.py`: `DiagnosticVerdict.abstained` / `abstain_reason` already
  present (added T-V3-3B) — no schema change.
- Distribution (from `apps/wired/v7/runs/POST_T_V3_3B/results.json`): 174 exact-tie top siblings;
  within margin≤0.05, 126 same-family / 150 different-family.

### Consumer (signal/noise) ###
- **Consumer:** the UI verdict card (PRD §5.2) `abstained`/`abstain_reason`; scoreboard
  `coverage`/`top3_on_covered` (reads `verdict.abstained`, unchanged from T-V3-3B).
- **Code path:** margin top2-selection on both router paths only. No schema/scorer/run_suite/oracle/
  CSV change.

### Deliverables ###
1. `labs/comlab/comlab/core/fault_atlas_router.py` — MODIFY (family-aware top2 on both paths).
2. `labs/comlab/.../tests/test_abstain_family_margin.py` — CREATE.

### Files to touch ###
- `labs/comlab/comlab/core/fault_atlas_router.py` (MODIFY)
- `labs/comlab/.../tests/test_abstain_family_margin.py` (CREATE)

### Out of scope ###
No threshold re-tune (0.80/0.05 stay — recalibration is deferred to `T-V3-D6`). No sibling dedupe /
SCORER_WINDOW change (deferred). No rank/score-weight work (T-V3-4). No schema change. **Do NOT edit
`run_suite.py`** (hash-locked) or the scoreboard read-site (already correct). No oracle/CSV edits.
Edit live `labs/comlab/` only — never `Vault/`. GRAPH GUARDRAIL: no `graphify`/graph rebuild.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile labs/comlab/comlab/core/fault_atlas_router.py
/agent_workspace/.venv-wired/bin/python -m ruff check labs/comlab/comlab/core/fault_atlas_router.py
/agent_workspace/.venv-wired/bin/python -m pyright labs/comlab/comlab/core/fault_atlas_router.py
/agent_workspace/.venv-wired/bin/python -m pytest -x -q labs/comlab -k abstain_family_margin
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --write-results apps/wired/v7/runs/POST_T_V3_3C/results.json | sed -n '1,16p'
```
Gate: `Hash lock: ok`; `top3_family` == **176/294** (unchanged); `coverage` materially > 0.10 and
`total_abstained` materially < 264; recovered-hidden-wins count reported; residual same-family
abstentions ≈ 0 (any remainder disclosed for T-V3-D6).

### Progress hook ###
PROGRESS.md `T-V3-3C`: Status=done, Files changed=2, Verification="family-aware abstain margin on both
paths; top3_family unchanged 176/294; Hash lock ok; coverage 0.10->CC, total_abstained 264->NN,
hidden-wins recovered=RR; residual same-family abstain=XX (for T-V3-D6)".

### Depends on ###
T-V3-3B (abstain emit) done. Runnable now.
