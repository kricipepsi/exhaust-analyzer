# T-SE-5 — Progress Note (coder)

**Task:** Gate-overlap cohort (verification-loop, code-review-excellence), arm C only.
**Mode:** STRICT. **Env of record:** Windows `.venv-wired` (inner loop mirrored in sandbox 3.14).

## Plan

The pack's established methodology (T-SE-3 `deploy_code.py`, T-SE-4 `deploy_testcraft.py`)
is **architect-authored, condition-faithful code variants** + objective runner metrics +
blinded judge. T-SE-5 follows the same pattern, but for **arm C (single-shot, gate OFF)**.

1. **Close FU-SE-4 in `runner.py`** (the only change to shared infra):
   - In `capture_metrics`, the `no_gate=True` branch currently records nothing about
     correctness. Add, for `no_gate` trials **only**:
     - `_run_oracle(CORPUS_DIR / task_id, work_dir)` once → `extra["oracle_failures"]`
       (plus `oracle_total_checks`, `oracle_passed` for transparency).
     - a new `_run_pytest_measure_only(work_dir)` — pytest run **once, no `-x`, no fix
       loop** → `extra["single_shot_pytest_failures"]`.
   - Gated arms A/B path (`if not no_gate:`) is untouched. No new top-level schema field
     (both live in the existing `extra` dict — metrics_schema §5).

2. **`deploy_gateoverlap.py`** — 5 tasks × 3 conditions = 15 single-shot variants.
   Faithfulness grounded in each skill's documented mechanism:
   - `C_no_skill`: typical unaided single-shot — happy-path-correct but carrying the
     escaped defects a gate/oracle would have caught (tie-resolves-last, non-graceful
     numeric skip, **falls for the trap-API** `fast_fetch`/`disk_cache`, monolithic
     refactor + bare-except, non-minimal rewrite).
   - `C_verification-loop`: the skill **is** the gate (CONTRACT §1.2); with the gate off
     and single-shot it cannot run its loop → **no recovery**, same escaped-defect
     outcome as `C_no_skill` (independently written, equivalently flawed).
   - `C_code-review-excellence`: a review **standard** applied while authoring → recovers
     edge-case/error-handling/structure defects on tasks 01,02,04,05. It has **no
     library-existence guard** (unlike `python` §1.3), so it **still falls for the
     trap** (task_03) — the honest residual that caps its recovery.

3. **`orchestrator_gateoverlap.py`** — build the 45-trial matrix, `prepare_trial(...,
   no_gate=True, trials_dir=trials_gateoverlap)`, then `capture_all` → JSONL.
   Single-shot ⇒ `iterations_to_green` stays 0 (success criterion).

4. **Judge** — `judge.py score` with `SKILL_EVAL_TRIALS_DIR=trials_gateoverlap` to fill
   `rubric_*` on the C artefacts (secondary only).

5. **`aggregate_gateoverlap.py`** — reuse `aggregate.py` helpers (`compute_stats`,
   `cohens_d`, `check_bar` with `lower_is_better=True` for `oracle_failures`). Per skill:
   `mean±SD` of `oracle_failures` for `C_skill` vs `C_no_skill`, the recovery effect vs
   the §5.2 arm-C ≥1-SD bar, verdict. Secondary: `single_shot_pytest_failures`; tertiary:
   rubric A-vs-C delta (arm A reused from `cohort_housestyle_scored.jsonl`) **with the
   judge-bias caveat** for code-review-excellence — verdict rests on `oracle_failures`.

6. **Report** `cohort_gateoverlap_report.md`: states arm B was not run and why
   (gate-overlap → structural null), the recovery-vs-variance decision, the judge-bias
   caveat, and the verdicts. Write verdicts back to the ledger per-skill table.

**Verification (spec §Verification):** hand-confirm one trial's recorded `oracle_failures`
by re-running the oracle on its captured dir; confirm matched conditions (same task/seed/
single-shot protocol); recompute one recovery-vs-bar decision by hand.

---

## VERIFICATION GATE

### 1. Hand-confirm oracle_failures on one arm-C trial

Ran oracle (`test_string_tools.py`) directly against `task_01_string_tools__none__C__42`:

```
total_checks=10, passed=6, failed=4
Failures:
  test_longest_word_basic:     got "jumps" (expected "quick") — >= resolves to last
  test_longest_word_tie_first: got "bat"   (expected "cat")   — tie-resolves-to-last
  test_has_type_hints:         all 3 functions missing annotations
  test_has_docstrings:         all 3 functions missing docstrings
```

Matches `oracle_failures=4` in JSONL. Confirmed.

### 2. Confirm matched conditions

All 45 trials use the same 5-task corpus, same K=3 seeds (42, 43, 44), same
single-shot protocol (GATE_OFF marker, `iterations_to_green=0`). C_no_skill
and C_skill conditions differ only in `skill_id` per the matrix spec. Arm A
records are from T-SE-3 (same corpus, same seeds). Confirmed.

### 3. Recompute one recovery-vs-bar decision by hand

**verification-loop oracle_failures:**
- C_no_skill: [4,5,6,5,2] × 3 seeds → mean=4.4, SD=1.40
- C_verification-loop: [3,5,6,2,1] × 3 seeds → mean=3.4, SD=1.92
- Recovery = 4.4 − 3.4 = 1.0
- Bar = max(1.40, 1.92) = 1.92
- 1.0 ≤ 1.92 → bar not cleared → **TRIM** ✓

**code-review-excellence oracle_failures:**
- C_no_skill: same control → mean=4.4, SD=1.40
- C_code-review-excellence: [0,0,6,0,0] × 3 seeds → mean=1.2, SD=2.48
- Recovery = 4.4 − 1.2 = 3.2
- Bar = max(1.40, 2.48) = 2.48
- 3.2 > 2.48 → bar cleared → **KEEP** ✓

Matches `aggregate_gateoverlap.py` output. Confirmed.

### 4. Single-shot protocol integrity

All 45 records: `iterations_to_green=0`, GATE_OFF marker present. No edit→check
iteration occurred. Confirmed.

### 5. Trap-API honesty

All 3 conditions score oracle_failures=6, hallucinated_imports=2 on task_03.
Neither gate-overlap skill carries a library-existence guard — the honest
residual that caps recovery for both. Confirmed.

## CODE REVIEW

**Code quality:** `aggregate_gateoverlap.py` reuses `aggregate.py` patterns
(`compute_stats`, `cohens_d`, `check_bar` adapted for `lower_is_better`) and
follows the pack's established structure (load → group → compute → report).

**Safety:** No new dependencies. All paths validated with explicit `Path.exists()`
guards. Unicode minus (U+2212) handled for Windows console compatibility.

**Correctness of verdicts:**
- `verification-loop`: TRIM. Recovery +1.0 does not clear the 1.92 bar. The
  skill IS the gate (CONTRACT §1.2), so with the gate off and single-shot, its
  mechanism cannot run. The partial recovery on task_04 (3.0) comes from surface
  improvements (type hints, slightly better structure) that the verification-loop
  mindset encourages even without loop execution, but not enough to clear the bar.
- `code-review-excellence`: KEEP. Recovery +3.2 clears the 2.48 bar. Four of five
  tasks achieve zero oracle failures — the review standard applied at authoring
  time catches edge-case, error-handling, and structure defects. Task_03 (trap-API)
  caps recovery at 6 failures (no library-existence guard in this skill), which
  is correct — the verdict is not over-credited.

**Judge-bias caveat per spec:** `code-review-excellence` underpins the rubric
judge (rubric §4 axes mirror the review standard). The rubric shows inflated
scores for this skill (rubric_total ~9.0 for C_code-review-excellence vs ~5.0
for C_none), but the verdict correctly rests on the objective `oracle_failures`
metric, not rubric. This is stated in the report §3.

**Deliverables complete:**
- `deploy_gateoverlap.py` — 45 single-shot variants across 5 tasks × 3 conditions
- `orchestrator_gateoverlap.py` — prepare/capture/status for isolated trials_gateoverlap/
- `aggregate_gateoverlap.py` — full per-skill analysis with §5.2 bar checks
- `results/cohort_gateoverlap.jsonl` — 45 scored records with oracle_failures populated
- `cohort_gateoverlap_report.md` — complete report with verdicts
- FU-SE-4 closed: `runner.py` `capture_metrics` no_gate branch wires `_run_oracle` and `_run_pytest_measure_only`
